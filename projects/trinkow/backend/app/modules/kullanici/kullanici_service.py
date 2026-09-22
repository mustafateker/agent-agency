"""
Kullanıcı iş mantığı: profil okuma, Katman 1/2 kaydetme, plan kurma,
günlük limiti elle ayarlama.

HTTP'den habersizdir — controller bu fonksiyonları çağırıp sonucu HTTP
yanıtına çevirir. Mongo erişimi burada yapılır, bağlantı `app.core`dan
gelir (auth_service.py ile aynı desen, K-068/3).

Plan formülleri (`kalan_gun_hesapla`den `eksik_kurus_hesapla`ya kadar)
`docs/design/delta-v4.md` satır 764-792'deki tabloyu BİREBİR uygular —
o tablo bağlayıcı tek kaynaktır (K-075). İstemcinin `src/lib/plan.ts`
dosyası aynı tabloyu TypeScript'te uygular; ikisi birbirinin kodunu
referans almaz, ikisi de tabloyu referans alır. Sunucu istemciden gelen
türetilmiş değerlere güvenmez: yalnız girdileri (gelir, giderler, birikim
yüzdesi, maaş günü) alır, kendi hesaplar ve hesapladığını döndürür.
"""
from __future__ import annotations

import math
from datetime import date, datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.errors import GelirGerekli, PlanNegatifKalan
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_model import KullaniciProfilBelgesi, Niyet

KULLANICI_PROFILLERI_KOLEKSIYONU = "kullanici_profilleri"

# tokens.md §14.1 — maaş günü "Düzensiz" ise dönem 30 gün kabul edilir.
DUZENSIZ_DONEM_GUN = 30


def _ayin_son_gunu(yil: int, ay: int) -> int:
    if ay == 12:
        return (date(yil + 1, 1, 1) - date(yil, 12, 1)).days
    return (date(yil, ay + 1, 1) - date(yil, ay, 1)).days


def _maas_gunu_tarihi(yil: int, ay: int, hedef_gun: int) -> date:
    """`ay` 1-12 dışına taşarsa (13 → sonraki yılın 1'i) yıl/ay'ı normalize eder."""
    yil_tasma, ay_indeks0 = divmod(ay - 1, 12)
    yil += yil_tasma
    ay = ay_indeks0 + 1
    gun = min(hedef_gun, _ayin_son_gunu(yil, ay))
    return date(yil, ay, gun)


def kalan_gun_hesapla(bugun: date, maas_gunu: int | None) -> int:
    """Formül tablosu #6 — maaş gününden kurulan dönemde bugün DAHİL kalan gün sayısı.

    Maaş günü ayda yoksa (31 → Şubat) ayın son günü kullanılır. `maas_gunu`
    `None` ise ("Düzensiz") dönem 30 gün kabul edilir.
    """
    if maas_gunu is None:
        return DUZENSIZ_DONEM_GUN

    bu_ay_odemesi = _maas_gunu_tarihi(bugun.year, bugun.month, maas_gunu)
    if bugun >= bu_ay_odemesi:
        donem_sonu = _maas_gunu_tarihi(bugun.year, bugun.month + 1, maas_gunu)
    else:
        donem_sonu = bu_ay_odemesi
    return (donem_sonu - bugun).days


def gunluk_limit_hesapla(pay_kurus: int, gun_sayisi: int) -> int:
    """Formül tablosu #7 — payı kalan güne böler, tam liraya AŞAĞI yuvarlar.

    Yukarı yuvarlamak limiti her gün bir miktar aşındırır (bkz. tablo notu).
    """
    if gun_sayisi <= 0:
        return 0
    gunluk_tam_kurus = pay_kurus // gun_sayisi
    return (gunluk_tam_kurus // 100) * 100


def zorunlu_kurus_hesapla(
    kira_aidat_kurus: int | None,
    faturalar_kurus: int | None,
    ulasim_yakit_kurus: int | None,
    kredi_taksit_kurus: int | None,
) -> int:
    """Formül tablosu #1 — yalnız kullanıcı girdisi, boş alan 0 sayılır."""
    return (kira_aidat_kurus or 0) + (faturalar_kurus or 0) + (ulasim_yakit_kurus or 0) + (kredi_taksit_kurus or 0)


def birikim_kurus_hesapla(gelir_kurus: int, birikim_yuzde: int) -> int:
    """Formül tablosu #2."""
    return math.floor((gelir_kurus * birikim_yuzde) / 100 + 0.5)


def sosyal_kurus_hesapla(gelir_kurus: int, zorunlu_kurus: int, birikim_kurus: int) -> int:
    """Formül tablosu #3 — negatif olabilir (plan kurma öncesi #10 ile ele alınır)."""
    return gelir_kurus - zorunlu_kurus - birikim_kurus


def pay_yuzdeleri_hesapla(
    gelir_kurus: int, zorunlu_kurus: int, sosyal_kurus: int, birikim_kurus: int
) -> tuple[int, int, int]:
    """Formül tablosu #5 — en büyük kalan (largest remainder) yöntemi.

    Her pay `floor(pay×100/gelir)`e yuvarlanır; kalan kuruş en büyük kesirli
    paya eklenerek toplam 100'e tamamlanır. İstemcinin `dagitimYuzdeleri`
    fonksiyonuyla (src/lib/plan.ts) aynı algoritma.
    """
    if gelir_kurus <= 0:
        return (0, 0, 0)

    hamlar = {
        "zorunlu": (zorunlu_kurus * 100) / gelir_kurus,
        "sosyal": (max(0, sosyal_kurus) * 100) / gelir_kurus,
        "birikim": (birikim_kurus * 100) / gelir_kurus,
    }
    tabanlar = {anahtar: math.floor(ham) for anahtar, ham in hamlar.items()}
    kesirler = {anahtar: hamlar[anahtar] - tabanlar[anahtar] for anahtar in hamlar}
    kalan = max(0, 100 - sum(tabanlar.values()))
    kesre_gore_sirali = sorted(kesirler, key=lambda anahtar: kesirler[anahtar], reverse=True)

    sonuc = dict(tabanlar)
    for anahtar in kesre_gore_sirali[:kalan]:
        sonuc[anahtar] += 1
    return sonuc["zorunlu"], sonuc["sosyal"], sonuc["birikim"]


def plan_negatif_mi(gelir_kurus: int, zorunlu_kurus: int) -> bool:
    """Formül tablosu #10 — sabit giderler gelirden fazlaysa plan kurulmaz."""
    return zorunlu_kurus > gelir_kurus


def eksik_kurus_hesapla(gelir_kurus: int, zorunlu_kurus: int) -> int:
    """Formül tablosu #10 — eksik tutar; ekranda her zaman POZİTİF gösterilir."""
    return max(0, zorunlu_kurus - gelir_kurus)


class KullaniciService:
    """Kullanıcı profili ve plan işlemlerini yürütür."""

    def __init__(self, veritabani: AsyncIOMotorDatabase, harcama_servisi: HarcamaService | None = None) -> None:
        self._profiller = veritabani[KULLANICI_PROFILLERI_KOLEKSIYONU]
        # Madde 6 (K-085/BE-4b) — `gunluk_limiti_ayarla` limit geçmişine de
        # yazmak için `harcama` modülünün servis arayüzünü kullanır (Kural 1:
        # doğrudan koleksiyona sorgu yok). Enjekte edilmezse kendi üretir —
        # var olan `KullaniciService(get_database())` çağrıları kırılmaz.
        self._harcama = harcama_servisi or HarcamaService(veritabani)

    async def kullanici_verisini_sil(self, kullanici_id: str) -> None:
        """Madde 1 (K-085/BE-4b) — hesap TAMAMEN silinirken profil belgesini kaldırır.

        `AuthService.hesabi_sil` tarafından, kimlik silinmeden ÖNCE çağrılır
        (Kural 1: `auth` bu koleksiyona doğrudan sorgu atmaz, servis
        arayüzünden geçer). `delete_one` eşleşme olmasa da hata vermez
        (profil hiç oluşturulmamış kullanıcı için de güvenli).
        """
        await self._profiller.delete_one({"kullanici_id": kullanici_id})

    async def profili_getir(self, kullanici_id: str) -> KullaniciProfilBelgesi:
        """Profili döner; kullanıcı henüz hiç veri girmemişse varsayılan (boş) profili döner."""
        belge = await self._profiller.find_one({"kullanici_id": kullanici_id})
        if belge is None:
            return KullaniciProfilBelgesi.varsayilan(kullanici_id)
        return KullaniciProfilBelgesi.belgeden_olustur(belge)

    async def katman1_kaydet(
        self,
        kullanici_id: str,
        niyet: Niyet | None,
        gelir_kurus: int | None,
        maas_gunu: int | None,
        maas_duzensiz: bool,
        gunluk_limit_onerisi_kurus: int | None = None,
    ) -> KullaniciProfilBelgesi:
        """E-01..E-03: niyet/gelir/maaş günü kaydeder, onboarding'i tamamlanmış işaretler.

        `gunluk_limit_onerisi_kurus` istemcinin hesapladığı ÖNERİDİR (K-059/5) —
        sunucu bunu olduğu gibi saklar, gerçek limite (`gunluk_limit_kurus`)
        YAZMAZ; öneri yalnız `gunluk_limiti_ayarla` ile kabul edilince gerçek
        limit hâline gelir.
        """
        if maas_duzensiz:
            maas_gunu = None
        return await self._profili_guncelle(
            kullanici_id,
            {
                "niyet": niyet,
                "gelir_kurus": gelir_kurus,
                "maas_gunu": maas_gunu,
                "maas_duzensiz": maas_duzensiz,
                "onboarding_tamamlandi": True,
                "gunluk_limit_onerisi_kurus": gunluk_limit_onerisi_kurus,
            },
        )

    async def katman1_guncelle(self, kullanici_id: str, alanlar: dict[str, Any]) -> KullaniciProfilBelgesi:
        """Madde 5 (K-084/1, BE-4b) — PATCH: yalnız GÖNDERİLEN Katman 1 alanını günceller.

        `katman1_kaydet` (PUT) ilk kurulum içindir, TÜM alanları ister ve
        onboarding'i tamamlanmış işaretler; bu metot zaten tamamlanmış bir
        profili sonradan DÜZENLEMEK içindir — onboarding bayrağına dokunmaz.
        `maas_duzensiz=True` gönderilirse PUT ile AYNI kural uygulanır:
        `maas_gunu` otomatik `None`'lanır (tutarsız veri yazılmasın diye).
        """
        if not alanlar:
            return await self.profili_getir(kullanici_id)
        guncellenecek = dict(alanlar)
        if guncellenecek.get("maas_duzensiz") is True:
            guncellenecek["maas_gunu"] = None
        return await self._profili_guncelle(kullanici_id, guncellenecek)

    async def katman2_kaydet(self, kullanici_id: str, alanlar: dict[str, Any]) -> KullaniciProfilBelgesi:
        """E-25: yalnız isteğin GÖNDERDİĞİ alanları günceller — diğerlerine dokunmaz.

        `alanlar` controller'da yalnız istekte gerçekten geçen üst düzey
        alanlardan üretilir (`Katman2Istegi.model_fields_set`); bir kart
        gönderildiyse o kartın tüm alt alanları (siklik/serbest_sayi/
        fiyat_kurus) birlikte yazılır.
        """
        if not alanlar:
            return await self.profili_getir(kullanici_id)
        return await self._profili_guncelle(kullanici_id, alanlar)

    async def plani_kur(self, kullanici_id: str, bugun: date | None = None) -> KullaniciProfilBelgesi:
        """E-26 "Planı kur": mevcut Katman 1/2 verisinden zorunlu/sosyal/birikim paylarını
        ve günlük limiti sunucu hesaplar, kaydeder ve hesapladığını döndürür (K-075).

        BE-5c/QA-1 — "bugün" istemciden gelir; sunucu saat dilimi varsayımı yapmaz
        (`/ozet/seri`'deki K-087 kuralıyla aynı desen). İSTİSNA: `bugun` verilmezse
        geriye dönük uyumluluk için sunucu UTC gününe düşer (eski istemciler
        kırılmasın) — bu düşüş KALICI bir davranış değildir, istemci bu parametreyi
        HER ZAMAN göndermelidir. Aksi halde maaş günü sınırında (TR 00:00-02:59)
        `kalan_gun`/`gunluk_limit_kurus` istemcinin hesabından 1 gün kayabilir.
        """
        profil = await self.profili_getir(kullanici_id)
        if profil.gelir_kurus is None:
            raise GelirGerekli()

        zorunlu = zorunlu_kurus_hesapla(
            profil.kira_aidat_kurus, profil.faturalar_kurus, profil.ulasim_yakit_kurus, profil.kredi_taksit_kurus
        )
        if plan_negatif_mi(profil.gelir_kurus, zorunlu):
            raise PlanNegatifKalan(eksik_kurus_hesapla(profil.gelir_kurus, zorunlu))

        birikim = birikim_kurus_hesapla(profil.gelir_kurus, profil.birikim_yuzde or 0)
        sosyal = sosyal_kurus_hesapla(profil.gelir_kurus, zorunlu, birikim)
        zorunlu_pay, sosyal_pay, birikim_pay = pay_yuzdeleri_hesapla(profil.gelir_kurus, zorunlu, sosyal, birikim)
        secilen_bugun = bugun or datetime.now(timezone.utc).date()
        kalan_gun = kalan_gun_hesapla(secilen_bugun, profil.maas_gunu)
        gunluk_limit = gunluk_limit_hesapla(sosyal, kalan_gun)

        # QA-1b — `gunluk_limiti_ayarla` ile aynı gün kaynağı (K-064/1): plan
        # kurulduğunda da `limit_gecmisi`ne yazılır, istemcinin `bugun`ü kullanılır.
        await self._harcama.limit_gecmisi_yaz(kullanici_id, secilen_bugun.isoformat(), gunluk_limit)

        return await self._profili_guncelle(
            kullanici_id,
            {
                "plan_kuruldu": True,
                "zorunlu_kurus": zorunlu,
                "zorunlu_pay_yuzde": zorunlu_pay,
                "sosyal_kurus": sosyal,
                "sosyal_pay_yuzde": sosyal_pay,
                "birikim_kurus": birikim,
                "birikim_pay_yuzde": birikim_pay,
                "gunluk_limit_kurus": gunluk_limit,
                "plan_kurulum_tarihi": datetime.now(timezone.utc),
            },
        )

    async def gunluk_limiti_ayarla(
        self, kullanici_id: str, gunluk_limit_kurus: int, bugun: date | None = None
    ) -> KullaniciProfilBelgesi:
        """E-17 "Limitler": günlük limiti plan hesabından bağımsız olarak elle yazar.

        Katman 1'in öneri kartında "Kabul et" ve "Başka bir sayı yaz" da AYNI
        yolu kullanır (istemcideki `oneriKabulEt` ile aynı davranış): gerçek
        limit yazılınca bekleyen öneri artık anlamsızdır, temizlenir.

        Madde 6 (K-085/BE-4b): tek otorite `kullanici_profilleri.gunluk_limit_kurus`dur;
        `limit_gecmisi` onun tarihçesidir. İstemcinin AYRICA
        `POST /harcama/ayar/limit-gecmisi` çağırmasına bağlı KALINMADAN, bugünün
        tarihiyle aynı değer buradan da yazılır — iki yol asla birbirinden
        sapamaz (Kural 1: `harcama` koleksiyonuna doğrudan yazılmaz, servis
        arayüzü `HarcamaService.limit_gecmisi_yaz` üzerinden geçilir).

        QA-1b/K-064 — "bugün" istemciden gelir; sunucu saat dilimi varsayımı
        yapmaz (`/ozet/seri`'deki K-087 kuralıyla aynı desen). İSTİSNA: `bugun`
        verilmezse geriye dönük uyumluluk için sunucu UTC gününe düşer (eski
        istemciler kırılmasın) — bu düşüş KALICI bir davranış değildir, istemci
        bu parametreyi HER ZAMAN göndermelidir. Aksi halde TR 00:00-02:59
        aralığında değişen limit `limit_gecmisi`ne bir önceki güne yazılır ve
        seri hesabı geçmişe dönük yanlış çıkar (K-064/1).
        """
        secilen_bugun = (bugun or datetime.now(timezone.utc).date()).isoformat()
        await self._harcama.limit_gecmisi_yaz(kullanici_id, secilen_bugun, gunluk_limit_kurus)
        return await self._profili_guncelle(
            kullanici_id, {"gunluk_limit_kurus": gunluk_limit_kurus, "gunluk_limit_onerisi_kurus": None}
        )

    async def en_uzun_seriyi_yaz(
        self, kullanici_id: str, en_uzun_seri: int, en_uzun_seri_bitis_gunu: str | None
    ) -> KullaniciProfilBelgesi:
        """K-077 (BE-5b Madde 1) — `ozet` modülünün ratchet KARARINI kalıcılaştırır.

        Ratchet kuralı (yalnız büyür) burada DEĞİL, çağıran `ozet_service`
        tarafında uygulanır (K-048 seri kuralı `ozet`in sorumluluğu) — bu
        metot yalnız verileni olduğu gibi yazan bir arayüz (Kural 1: `ozet`
        bu koleksiyona doğrudan yazmaz, servis arayüzünden geçer).
        """
        return await self._profili_guncelle(
            kullanici_id,
            {"en_uzun_seri": en_uzun_seri, "en_uzun_seri_bitis_gunu": en_uzun_seri_bitis_gunu},
        )

    async def oneriyi_reddet(self, kullanici_id: str) -> KullaniciProfilBelgesi:
        """"Limitsiz devam et" — öneri düşer, gerçek limit YAZILMAZ (istemcideki `oneriReddet`)."""
        return await self._profili_guncelle(kullanici_id, {"gunluk_limit_onerisi_kurus": None})

    async def tercihleri_guncelle(self, kullanici_id: str, alanlar: dict[str, Any]) -> KullaniciProfilBelgesi:
        """E-19 Ayarlar: yalnız gönderilen tercih alanlarını günceller.

        `bildirim_aksam_ozet` gönderildiyse "tercih belirlendi" bayrağı da
        birlikte set edilir (istemcideki `bildirimAksamOzetKaydet` ile aynı
        davranış). `kurulum_gunu` yalnız hiç ayarlanmamışsa yazılır — bir kez
        sabitlenince değişmez (K-049); istemci sabit bir alanı boşuna
        güncellemeye çalışırsa sessizce yok sayılır, hata verilmez.
        """
        if not alanlar:
            return await self.profili_getir(kullanici_id)

        guncellenecek = dict(alanlar)
        if "bildirim_aksam_ozet" in guncellenecek:
            guncellenecek["bildirim_tercih_belirlendi"] = True
        if "kurulum_gunu" in guncellenecek:
            mevcut = await self.profili_getir(kullanici_id)
            if mevcut.kurulum_gunu is not None:
                guncellenecek.pop("kurulum_gunu")

        if not guncellenecek:
            return await self.profili_getir(kullanici_id)
        return await self._profili_guncelle(kullanici_id, guncellenecek)

    async def _profili_guncelle(self, kullanici_id: str, alanlar: dict[str, Any]) -> KullaniciProfilBelgesi:
        await self._profiller.update_one(
            {"kullanici_id": kullanici_id},
            {"$set": {**alanlar, "kullanici_id": kullanici_id}},
            upsert=True,
        )
        return await self.profili_getir(kullanici_id)
