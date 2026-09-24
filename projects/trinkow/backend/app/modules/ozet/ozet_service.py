"""
Özet iş mantığı: günlük pano (E-10), dönemsel özet (E-16), kategori detayı
(E-15) ve seri/streak (E-21).

`ozet` modülünün kendi koleksiyonu YOK (bkz. ozet_model.py) — bu modül
YALNIZ `harcama` ve `kullanici` modüllerinin servis arayüzlerini
(`HarcamaService` / `KullaniciService`) çağırır, hiçbir Mongo koleksiyonuna
doğrudan sorgu atmaz (backend/README.md Kural 1).

Dosya iki bölüme ayrılır:
  1. SAF HESAP fonksiyonları — Mongo'dan habersiz, deterministik girdiyle
     çalışır, Mongo olmadan pytest ile test edilebilir (görev notu).
  2. `OzetService` — yalnız bu bölüm async'tir ve `harcama`/`kullanici`
     servislerini çağırıp saf fonksiyonlara girdi hazırlar.

Seri kuralları (K-048 + K-064/1) `app/src/db/seri.ts`nin davranış
referansıdır (kopyalanmaz, davranış karşılaştırması için kullanılır).
"""
from __future__ import annotations

import math
from calendar import monthrange
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta, timezone
from typing import Callable, Literal

from app.modules.harcama.harcama_model import HarcamaBelgesi, LimitGecmisiBelgesi
from app.modules.harcama.harcama_service import AZAMI_SAYFA_BOYUTU, HarcamaService
from app.modules.kullanici.kullanici_service import KullaniciService

# ---------------------------------------------------------------------------
# Saf hesap — Mongo'suz, pytest ile doğrudan test edilir
# ---------------------------------------------------------------------------

# K-048 — milestone dizisi. Artırılamaz/uydurulmaz (bağlayıcı liste, tokens.md §14.5).
MILESTONES: tuple[int, ...] = (3, 7, 14, 30, 60, 100, 180, 365)

# Latte Faktörü eşiği — istemcideki `haftaKucukHarcamaOzeti`nin varsayılanıyla aynı (50 ₺).
VARSAYILAN_KUCUK_HARCAMA_ESIGI_KURUS = 5_000

LimitDurumu = Literal["altinda", "asimda", "tanimsiz"]
IzgaraDurumu = Literal["altinda", "disinda", "bos"]


def limit_durumu_hesapla(harcanan_kurus: int, limit_kurus: int | None) -> LimitDurumu:
    """E-10 günlük pano — bir günün harcaması limitin neresinde. Limit yoksa 'tanimsiz'."""
    if limit_kurus is None:
        return "tanimsiz"
    return "asimda" if harcanan_kurus > limit_kurus else "altinda"


def gun_izgara_durumu(harcanan_kurus: int, kayit_adedi: int, limit_kurus: int | None) -> IzgaraDurumu:
    """E-21/E-24 ortak sınıflandırma — istemcideki `db/seri.ts#gunSeriDurumu` ile birebir aynı kural."""
    if kayit_adedi == 0:
        return "bos"
    if limit_kurus is not None and harcanan_kurus > limit_kurus:
        return "disinda"
    return "altinda"


def gun_seriye_sayilir_mi(
    harcanan_kurus: int, kayit_adedi: int, harcamasiz_isaretli: bool, limit_kurus: int
) -> bool:
    """K-048 hile kapısı — istemcideki `db/seri.ts#gunSeriyeSayilirMi` ile birebir aynı kural.

    Bir gün seriye ancak (a) o gün en az bir kayıt varsa YA DA (b)
    "harcamasız gün" işaretlenmişse VE harcanan tutar o günün limitini
    aşmıyorsa sayılır.
    """
    kayitli_ya_da_isaretli = kayit_adedi > 0 or harcamasiz_isaretli
    return kayitli_ya_da_isaretli


def sonraki_durak(mevcut_seri: int) -> int | None:
    """Mevcut seriden büyük ilk milestone; hiçbiri yoksa (365'i geçtiyse) `None`."""
    for milestone in MILESTONES:
        if milestone > mevcut_seri:
            return milestone
    return None


def onceki_durak(mevcut_seri: int) -> int:
    """Mevcut seriye ulaşılmış son milestone; hiçbiri geçilmediyse 0."""
    onceki = 0
    for milestone in MILESTONES:
        if milestone <= mevcut_seri:
            onceki = milestone
        else:
            break
    return onceki


def esik_alti_toplam(tutarlar_kurus: list[int], esik_kurus: int = VARSAYILAN_KUCUK_HARCAMA_ESIGI_KURUS) -> tuple[int, int]:
    """Latte Faktörü — eşiğin ALTINDAKİ harcamaların (adet, toplam_kurus) çifti."""
    kucukler = [tutar for tutar in tutarlar_kurus if tutar < esik_kurus]
    return len(kucukler), sum(kucukler)


def en_buyuk_kalan_yuzdeler(tutarlar_kurus: dict[str, int]) -> dict[str, int]:
    """Kategori yüzdeleri — en büyük kalan (largest remainder) yöntemi (delta-v4.md formül #5).

    Her pay `floor(tutar×100/toplam)`e yuvarlanır; kalan yüzde puanı en
    büyük kesirli paylara eklenerek toplam TAM 100'e tamamlanır. Toplam
    0/negatifse (kayıt yoksa) tüm yüzdeler 0 döner — bölme hatası olmaz.
    """
    toplam = sum(tutarlar_kurus.values())
    if toplam <= 0:
        return {anahtar: 0 for anahtar in tutarlar_kurus}

    hamlar = {anahtar: (tutar * 100) / toplam for anahtar, tutar in tutarlar_kurus.items()}
    tabanlar = {anahtar: math.floor(ham) for anahtar, ham in hamlar.items()}
    kesirler = {anahtar: hamlar[anahtar] - tabanlar[anahtar] for anahtar in hamlar}
    kalan = 100 - sum(tabanlar.values())
    kesre_gore_sirali = sorted(kesirler, key=lambda anahtar: kesirler[anahtar], reverse=True)

    sonuc = dict(tabanlar)
    for anahtar in kesre_gore_sirali[:kalan]:
        sonuc[anahtar] += 1
    return sonuc


def gunluk_toplamlari_hesapla(kayitlar: list[HarcamaBelgesi]) -> dict[str, tuple[int, int]]:
    """Bir aralıktaki harcama kayıtlarını `gun -> (toplam_kurus, kayit_adedi)` sözlüğüne indirger."""
    toplamlar: dict[str, tuple[int, int]] = {}
    for kayit in kayitlar:
        onceki_toplam, onceki_adet = toplamlar.get(kayit.gun, (0, 0))
        toplamlar[kayit.gun] = (onceki_toplam + kayit.tutar_kurus, onceki_adet + 1)
    return toplamlar


def gun_araligi_uret(baslangic_gun: str, bitis_gun: str) -> list[str]:
    """`baslangic_gun`dan `bitis_gun`a (ikisi de dahil) ISO gün dizisi üretir."""
    baslangic = date.fromisoformat(baslangic_gun)
    bitis = date.fromisoformat(bitis_gun)
    gunler: list[str] = []
    gun = baslangic
    while gun <= bitis:
        gunler.append(gun.isoformat())
        gun += timedelta(days=1)
    return gunler


def seri_sinir_gunu_belirle(kurulum_gunu: str | None, en_eski_kayit_gunu: str | None, bugun_gun: str) -> str:
    """Madde 2 (K-077) — seri sınır günü, istemcideki `db/seri.ts#ilkSinirGunu` ile
    AYNI kural: kurulum günü ile ilk kayıt gününün daha ERKEN olanı.

    `kurulum_gunu` hiç ayarlanmamışsa (yeni kullanıcı) `bugun_gun` varsayılır.
    Hiç kayıt yoksa yalnız kurulum günü kullanılır — icat edilen bir tarih yok.
    """
    kurulum = kurulum_gunu or bugun_gun
    if en_eski_kayit_gunu is None or en_eski_kayit_gunu >= kurulum:
        return kurulum
    return en_eski_kayit_gunu


def efektif_limit_cozucu_olustur(
    tarihce: list[LimitGecmisiBelgesi], guncel_limit_kurus: int
) -> Callable[[str], int]:
    """Madde 3 (K-077) — ARTAN gün sırasıyla çağrılacak "o gün yürürlükteki limit"
    çözücüsü üretir; istemcideki `db/seri.ts#gunlukLimitCozucuOlustur` ile
    birebir aynı algoritma.

    `tarihce`, `HarcamaService.limit_gecmisi_araligi_getir`den (artan
    `yururluk_tarihi` sırasıyla) gelir. Dönen kapanış yalnız İLERİ gider —
    O(gün + değişiklik) toplam maliyet, her gün için tarihçe baştan
    taranmaz. `tarihce` boşsa (göçten önce hiç değişiklik yoksa) her gün
    `guncel_limit_kurus` "en iyi tahmin" olarak döner (K-064/1).
    """
    indeks = 0
    mevcut = guncel_limit_kurus

    def cozucu(gun: str) -> int:
        nonlocal indeks, mevcut
        while indeks < len(tarihce) and tarihce[indeks].yururluk_tarihi <= gun:
            mevcut = tarihce[indeks].kurus
            indeks += 1
        return mevcut

    return cozucu


def en_uzun_seri_ratchet(
    kayitli_en_uzun_seri: int,
    kayitli_bitis_gunu: str | None,
    aday_en_uzun_seri: int,
    aday_bitis_gunu: str | None,
) -> tuple[int, str | None, bool]:
    """Madde 1 (K-048/F-16f + K-077) — saf ratchet kararı: yalnız BÜYÜRSE günceller,
    asla küçülmez. `(yeni_en_uzun_seri, yeni_bitis_gunu, guncellenmeli_mi)` döner;
    çağıran `guncellenmeli_mi=True` ise `KullaniciService.en_uzun_seriyi_yaz`ı çağırır.
    """
    if aday_en_uzun_seri > kayitli_en_uzun_seri:
        return aday_en_uzun_seri, aday_bitis_gunu, True
    return kayitli_en_uzun_seri, kayitli_bitis_gunu, False


def ay_son_gunu(ay: str) -> str:
    """`YYYY-MM` biçimindeki bir ayın son gününü `YYYY-MM-DD` olarak döner."""
    yil, ay_no = int(ay[:4]), int(ay[5:7])
    son_gun = monthrange(yil, ay_no)[1]
    return f"{ay}-{son_gun:02d}"


@dataclass(frozen=True)
class GunNitelik:
    """Seri hesabına giren tek bir günün ÖNCEDEN ÇÖZÜLMÜŞ verisi.

    `efektif_limit_kurus` o gün YÜRÜRLÜKTE olan limittir (K-064/1) — bu
    değerin çözümü `HarcamaService.limit_gecmisi_efektif_limit` ile (Mongo
    gerektirir) `OzetService` tarafında yapılır; bu sınıf ve `seri_hesapla`
    saf kalır.
    """

    gun: str
    harcanan_kurus: int
    kayit_adedi: int
    harcamasiz_isaretli: bool
    efektif_limit_kurus: int


@dataclass(frozen=True)
class SeriSonucu:
    mevcut_seri: int
    en_uzun_seri: int
    en_uzun_seri_bitis_gunu: str | None
    kapali: bool
    kirildi_mi: bool
    sonraki_durak: int | None
    onceki_durak: int
    kalan_gun: int | None
    aralik_yuzde: float
    gecilen_milestoneler: list[int]


_KAPALI_SERI_SONUCU = SeriSonucu(
    mevcut_seri=0,
    en_uzun_seri=0,
    en_uzun_seri_bitis_gunu=None,
    kapali=True,
    kirildi_mi=False,
    sonraki_durak=None,
    onceki_durak=0,
    kalan_gun=None,
    aralik_yuzde=0.0,
    gecilen_milestoneler=[],
)


def seri_hesapla(nitelikler: list[GunNitelik], limitsiz_mi: bool) -> SeriSonucu:
    """K-048/§14.5 seri hesabı — istemcideki `db/seri.ts#seriDurumuHesapla`nın saf çekirdeği.

    `limitsiz_mi=True` ise (K-048: "limitsiz kipte seri kapalıdır") günlük
    veri hiç değerlendirilmez — `nitelikler` boş geçilebilir. `nitelikler`
    ARTAN gün sırasıyla (en eski → bugün) verilmelidir; her günün
    `efektif_limit_kurus`ü ÇAĞIRAN tarafından zaten çözülmüş olmalıdır
    (K-064/1 — geçmiş gün kendi yürürlükteki limitiyle değerlendirilir).

    Server her çağrıda TÜM geçmişi yeniden tarar ve döndürdüğü `en_uzun_seri`
    yalnız bu taramanın ADAYIDIR — kalıcı ratchet kararı (Madde 1, K-077)
    `OzetService.seri_getir` içinde `en_uzun_seri_ratchet` ile verilir, bu
    saf fonksiyon Mongo'dan/kalıcı durumdan habersizdir.
    """
    if not nitelikler:
        return replace(_KAPALI_SERI_SONUCU, kapali=False)

    sayilir_mi_dizisi = [
        gun_seriye_sayilir_mi(n.harcanan_kurus, n.kayit_adedi, n.harcamasiz_isaretli, n.efektif_limit_kurus)
        for n in nitelikler
    ]

    mevcut_seri = 0
    # Today is pending until its first entry; yesterday's streak survives.
    mevcut_dizi = sayilir_mi_dizisi if sayilir_mi_dizisi[-1] else sayilir_mi_dizisi[:-1]
    for sayildi in reversed(mevcut_dizi):
        if not sayildi:
            break
        mevcut_seri += 1

    calisan_kosu = 0
    en_uzun_kosu = 0
    en_uzun_bitis_indeksi = -1
    for indeks, sayildi in enumerate(sayilir_mi_dizisi):
        if not sayildi:
            calisan_kosu = 0
            continue
        calisan_kosu += 1
        if calisan_kosu > en_uzun_kosu:
            en_uzun_kosu = calisan_kosu
            en_uzun_bitis_indeksi = indeks

    en_uzun_seri_bitis_gunu = nitelikler[en_uzun_bitis_indeksi].gun if en_uzun_bitis_indeksi >= 0 else None
    kirildi_mi = mevcut_seri == 0 and en_uzun_kosu > 0
    sonraki = sonraki_durak(mevcut_seri)
    onceki = onceki_durak(mevcut_seri)
    aralik_yuzde = (mevcut_seri - onceki) / (sonraki - onceki) if sonraki else 1.0
    gecilen_milestoneler = [milestone for milestone in MILESTONES if milestone <= mevcut_seri]

    return SeriSonucu(
        mevcut_seri=mevcut_seri,
        en_uzun_seri=en_uzun_kosu,
        en_uzun_seri_bitis_gunu=en_uzun_seri_bitis_gunu,
        kapali=False,
        kirildi_mi=kirildi_mi,
        sonraki_durak=sonraki,
        onceki_durak=onceki,
        kalan_gun=(sonraki - mevcut_seri) if (mevcut_seri > 0 and sonraki) else None,
        aralik_yuzde=aralik_yuzde,
        gecilen_milestoneler=gecilen_milestoneler,
    )


@dataclass(frozen=True)
class GunIzgaraHucresi:
    gun: str
    durum: IzgaraDurumu


@dataclass(frozen=True)
class SeriGorunumu:
    seri: SeriSonucu
    izgara: list[GunIzgaraHucresi]


_IZGARA_GUN_SAYISI = 30


def izgara_uret(nitelikler: list[GunNitelik]) -> list[GunIzgaraHucresi]:
    """Son `_IZGARA_GUN_SAYISI` günün ızgara durumu (E-21) — `nitelikler`in kuyruğundan üretilir."""
    kuyruk = nitelikler[-_IZGARA_GUN_SAYISI:]
    return [
        GunIzgaraHucresi(gun=n.gun, durum=gun_izgara_durumu(n.harcanan_kurus, n.kayit_adedi, n.efektif_limit_kurus))
        for n in kuyruk
    ]


@dataclass(frozen=True)
class PanoKategoriDurumu:
    kategori: str
    limit_kurus: int
    harcanan_kurus: int
    bugun_kurus: int


@dataclass(frozen=True)
class GunSeriBilgisi:
    harcanan_kurus: int
    kayit_adedi: int
    harcamasiz_isaretli: bool
    seriye_sayildi_mi: bool | None


@dataclass(frozen=True)
class GunlukPano:
    gun: str
    niyet: str
    limit_kurus: int | None
    harcanan_kurus: int
    kayit_adedi: int
    limit_durumu: LimitDurumu
    kategoriler: list[PanoKategoriDurumu]
    ay_asimi: int
    seri: GunSeriBilgisi
    ilk_gun_mu: bool


@dataclass(frozen=True)
class KategoriPayi:
    kategori: str
    toplam_kurus: int
    yuzde: int


@dataclass(frozen=True)
class KucukHarcamaOzeti:
    esik_kurus: int
    adet: int
    toplam_kurus: int


@dataclass(frozen=True)
class OzetGorunumu:
    baslangic_gun: str
    bitis_gun: str
    toplam_kurus: int
    kategori_dagilimi: list[KategoriPayi]
    en_cok_harcanan_kategoriler: list[str]
    kucuk_harcama: KucukHarcamaOzeti


@dataclass(frozen=True)
class KategoriSeyriGunu:
    gun: str
    toplam_kurus: int


@dataclass(frozen=True)
class KategoriDetayGorunumu:
    kategori: str
    baslangic_gun: str
    bitis_gun: str
    toplam_kurus: int
    gun_bazinda_seyir: list[KategoriSeyriGunu]


# ---------------------------------------------------------------------------
# Async orkestrasyon — yalnız burası Mongo gerektirir (harcama/kullanici üzerinden)
# ---------------------------------------------------------------------------


class OzetService:
    """Pano/özet/kategori-detayı/seri görünümlerini `harcama` ve `kullanici`
    servis arayüzlerinden topladığı veriyle üretir; kendi koleksiyonu yok."""

    def __init__(self, harcama_servisi: HarcamaService, kullanici_servisi: KullaniciService) -> None:
        self._harcama = harcama_servisi
        self._kullanici = kullanici_servisi

    async def _araligin_tum_kayitlarini_getir(
        self, kullanici_id: str, baslangic_gun: str, bitis_gun: str, kategori: str | None = None
    ) -> list[HarcamaBelgesi]:
        """`HarcamaService.harcamalari_listele`yi sayfalayarak aralıktaki TÜM kayıtları toplar.

        `harcama` modülü sayfalama sınırını (AZAMI_SAYFA_BOYUTU=200) HTTP
        istemcisi için koyuyor; özet/seri hesapları toplama yapmak için
        aralığın TAMAMINA ihtiyaç duyar, bu yüzden burada döngüyle toplanır.
        """
        tum_kayitlar: list[HarcamaBelgesi] = []
        sayfa = 1
        while True:
            kayitlar, toplam_kayit = await self._harcama.harcamalari_listele(
                kullanici_id,
                None,
                baslangic_gun,
                bitis_gun,
                kategori,
                sayfa,
                AZAMI_SAYFA_BOYUTU,
            )
            tum_kayitlar.extend(kayitlar)
            if not kayitlar or len(tum_kayitlar) >= toplam_kayit:
                break
            sayfa += 1
        return tum_kayitlar

    async def _gun_nitelikleri_hesapla(
        self, kullanici_id: str, ilk_gun: str, bugun_gun: str, guncel_limit_kurus: int
    ) -> list[GunNitelik]:
        """`ilk_gun`den `bugun_gun`e (dahil) her günün seri değerlendirmesi için gerekli verisini toplar.

        Madde 3 (K-077): her günün efektif limiti artık TEK TEK sorgulanmaz —
        `limit_gecmisi_araligi_getir` ile `bugun_gun`e kadarki TÜM tarihçe TEK
        seferde çekilir, `efektif_limit_cozucu_olustur` ile ARTAN gün
        sırasıyla (aşağıdaki döngü zaten `gunler`i artan üretir) bellekte
        çözülür — davranış (K-064/1) AYNI kalır, yalnız Mongo sorgu sayısı
        O(gün)'den O(1)'e düşer.
        "Harcamasız" bayrağı yalnız kaydı OLMAYAN günler için sorgulanır —
        kayıt varsa zaten hile kapısını (a) şıkkıyla geçer.
        """
        gunler = gun_araligi_uret(ilk_gun, bugun_gun)
        kayitlar = await self._araligin_tum_kayitlarini_getir(kullanici_id, ilk_gun, bugun_gun)
        gunluk_toplamlar = gunluk_toplamlari_hesapla(kayitlar)
        limit_tarihcesi = await self._harcama.limit_gecmisi_araligi_getir(kullanici_id, bugun_gun)
        efektif_limit_cozucu = efektif_limit_cozucu_olustur(limit_tarihcesi, guncel_limit_kurus)

        nitelikler: list[GunNitelik] = []
        for gun in gunler:
            harcanan_kurus, kayit_adedi = gunluk_toplamlar.get(gun, (0, 0))
            harcamasiz_isaretli = False
            if kayit_adedi == 0:
                gun_durumu = await self._harcama.gun_durumu_getir(kullanici_id, gun)
                harcamasiz_isaretli = gun_durumu.harcamasiz
            efektif_limit = efektif_limit_cozucu(gun)
            nitelikler.append(GunNitelik(gun, harcanan_kurus, kayit_adedi, harcamasiz_isaretli, efektif_limit))
        return nitelikler

    async def seri_getir(self, kullanici_id: str, bugun: date | None = None) -> SeriGorunumu:
        """E-21 — mevcut seri, en uzun seri, son 30 günün ızgarası, milestone durumu.

        Sınır günü (Madde 2, K-077) `kurulum_gunu` ile `harcama`nın en eski
        kayıt gününün daha ERKEN olanıdır (`seri_sinir_gunu_belirle` —
        istemcideki `ilkSinirGunu` ile aynı kural, K-049).

        "En uzun seri" (Madde 1, K-048/F-16f + K-077) `kullanici_profilleri`nde
        KALICI saklanır ve yalnız BÜYÜR (ratchet, bkz. `en_uzun_seri_ratchet`):
        limitsiz kipte mevcut seri kapalı/0 olsa da kayıtlı rekor kaybolmaz.

        `bugun` — K-087: "bugün" artık sunucu tarafından TÜRETİLMEZ, çağıran
        (controller) istemciden gelen yerel günü buraya geçirir (`harcama`
        modülündeki "gün istemciden gelir" kuralıyla aynı). `bugun=None`
        YALNIZ geriye dönük uyumluluk İSTİSNASIdır (eski istemci/parametresiz
        çağrı) ve bu durumda sunucu UTC gününe düşer — bu düşüş kalıcı bir
        tasarım kararı DEĞİL, geçiş kolaylığıdır. Gelecek gün koruması
        BİLEREK eklenmedi: `bugun` gerçek "şimdi"den ileriyse mevcut davranış
        (aşağıdaki `ilk_gun > bugun_gun` kısaltması dışında sınırsız kabul)
        aynen sürer — kapsam BE-5c'de bilinçli olarak dışarıda bırakıldı.
        """
        bugun_gun = (bugun or datetime.now(timezone.utc).date()).isoformat()
        profil = await self._kullanici.profili_getir(kullanici_id)
        guncel_limit = profil.gunluk_limit_kurus

        en_eski_kayit_gunu = await self._harcama.en_eski_kayit_gunu(kullanici_id)
        ilk_gun = seri_sinir_gunu_belirle(profil.kurulum_gunu, en_eski_kayit_gunu, bugun_gun)
        if ilk_gun > bugun_gun:
            ilk_gun = bugun_gun

        nitelikler = await self._gun_nitelikleri_hesapla(kullanici_id, ilk_gun, bugun_gun, guncel_limit or 0)
        seri_sonucu = seri_hesapla(nitelikler, limitsiz_mi=False)

        yeni_en_uzun, yeni_bitis, guncellenmeli_mi = en_uzun_seri_ratchet(
            profil.en_uzun_seri, profil.en_uzun_seri_bitis_gunu, seri_sonucu.en_uzun_seri, seri_sonucu.en_uzun_seri_bitis_gunu
        )
        if guncellenmeli_mi:
            await self._kullanici.en_uzun_seriyi_yaz(kullanici_id, yeni_en_uzun, yeni_bitis)
        seri_sonucu = replace(seri_sonucu, en_uzun_seri=yeni_en_uzun, en_uzun_seri_bitis_gunu=yeni_bitis)

        return SeriGorunumu(seri=seri_sonucu, izgara=izgara_uret(nitelikler))

    async def gunluk_pano_getir(self, kullanici_id: str, gun: str) -> GunlukPano:
        """E-10 — seçilen günün toplamı, limit durumu, kategori kırılımı, o günün seri durumu."""
        ay = gun[:7]
        ay_baslangic = f"{ay}-01"
        ay_bitis = ay_son_gunu(ay)

        profil = await self._kullanici.profili_getir(kullanici_id)
        limit_kurus = profil.gunluk_limit_kurus

        ay_kayitlari = await self._araligin_tum_kayitlarini_getir(kullanici_id, ay_baslangic, ay_bitis)
        gunluk_toplamlar = gunluk_toplamlari_hesapla(ay_kayitlari)
        harcanan_kurus, kayit_adedi = gunluk_toplamlar.get(gun, (0, 0))

        butce_surumleri = await self._kullanici._butce.surumler(kullanici_id)
        from app.modules.tasarruf.tasarruf_service import efektif_surum
        from app.modules.butce.butce_service import butce_hesapla
        surum = efektif_surum(butce_surumleri, gun)
        gun_butcesi = butce_hesapla(surum, gun) if surum else None
        if butce_surumleri:
            limit_kurus = gun_butcesi['gunluk_limit_kurus'] if gun_butcesi else None
        kategori_gun_toplam: dict[str, int] = {}
        for kayit in (x for x in ay_kayitlari if x.gun == gun):
            kategori_gun_toplam[kayit.kategori] = kategori_gun_toplam.get(kayit.kategori, 0) + kayit.tutar_kurus
        kategoriler = [PanoKategoriDurumu(kategori=kod, limit_kurus=tutar,
            harcanan_kurus=kategori_gun_toplam.get(kod, 0), bugun_kurus=kategori_gun_toplam.get(kod, 0))
            for kod, tutar in (gun_butcesi or {}).get('kategori_limitleri', {}).items()]
        ay_asimi = 0
        for gun_anahtari, (toplam, _) in gunluk_toplamlar.items():
            tarihli = efektif_surum(butce_surumleri, gun_anahtari)
            gun_limiti = butce_hesapla(tarihli, gun_anahtari)['gunluk_limit_kurus'] if tarihli else None
            if gun_limiti is not None and toplam > gun_limiti:
                ay_asimi += 1

        harcamasiz_isaretli = False
        if kayit_adedi == 0:
            gun_durumu = await self._harcama.gun_durumu_getir(kullanici_id, gun)
            harcamasiz_isaretli = gun_durumu.harcamasiz

        seriye_sayildi_mi = gun_seriye_sayilir_mi(harcanan_kurus, kayit_adedi, harcamasiz_isaretli, limit_kurus or 0)

        ilk_gun_mu = profil.kurulum_gunu is not None and gun <= profil.kurulum_gunu

        return GunlukPano(
            gun=gun,
            niyet=profil.niyet or "takip",
            limit_kurus=limit_kurus,
            harcanan_kurus=harcanan_kurus,
            kayit_adedi=kayit_adedi,
            limit_durumu=limit_durumu_hesapla(harcanan_kurus, limit_kurus),
            kategoriler=kategoriler,
            ay_asimi=ay_asimi,
            seri=GunSeriBilgisi(harcanan_kurus, kayit_adedi, harcamasiz_isaretli, seriye_sayildi_mi),
            ilk_gun_mu=ilk_gun_mu,
        )

    async def ozet_getir(
        self,
        kullanici_id: str,
        baslangic_gun: str,
        bitis_gun: str,
        esik_kurus: int = VARSAYILAN_KUCUK_HARCAMA_ESIGI_KURUS,
    ) -> OzetGorunumu:
        """E-16 — dönem toplamı, kategori dağılımı (₺+%), en çok harcanan kategoriler, Latte Faktörü."""
        kayitlar = await self._araligin_tum_kayitlarini_getir(kullanici_id, baslangic_gun, bitis_gun)
        toplam_kurus = sum(kayit.tutar_kurus for kayit in kayitlar)

        kategori_toplamlari: dict[str, int] = {}
        for kayit in kayitlar:
            kategori_toplamlari[kayit.kategori] = kategori_toplamlari.get(kayit.kategori, 0) + kayit.tutar_kurus

        yuzdeler = en_buyuk_kalan_yuzdeler(kategori_toplamlari)
        kategori_dagilimi = sorted(
            (
                KategoriPayi(kategori=kategori, toplam_kurus=tutar, yuzde=yuzdeler[kategori])
                for kategori, tutar in kategori_toplamlari.items()
            ),
            key=lambda payi: payi.toplam_kurus,
            reverse=True,
        )
        en_cok_harcanan = [payi.kategori for payi in kategori_dagilimi[:3]]

        adet, kucuk_toplam = esik_alti_toplam([kayit.tutar_kurus for kayit in kayitlar], esik_kurus)

        return OzetGorunumu(
            baslangic_gun=baslangic_gun,
            bitis_gun=bitis_gun,
            toplam_kurus=toplam_kurus,
            kategori_dagilimi=kategori_dagilimi,
            en_cok_harcanan_kategoriler=en_cok_harcanan,
            kucuk_harcama=KucukHarcamaOzeti(esik_kurus=esik_kurus, adet=adet, toplam_kurus=kucuk_toplam),
        )

    async def kategori_detayi_getir(
        self, kullanici_id: str, kategori: str, baslangic_gun: str, bitis_gun: str
    ) -> KategoriDetayGorunumu:
        """E-15 — tek kategorinin zaman içindeki seyri (o kategorideki kayıt LİSTESİ `/harcama/?kategori=`de)."""
        kayitlar = await self._araligin_tum_kayitlarini_getir(kullanici_id, baslangic_gun, bitis_gun, kategori)
        gunluk_toplamlar = gunluk_toplamlari_hesapla(kayitlar)
        seyir = sorted(
            (
                KategoriSeyriGunu(gun=gun, toplam_kurus=toplam)
                for gun, (toplam, _adet) in gunluk_toplamlar.items()
            ),
            key=lambda gunu: gunu.gun,
        )
        toplam_kurus = sum(toplam for toplam, _adet in gunluk_toplamlar.values())
        return KategoriDetayGorunumu(
            kategori=kategori,
            baslangic_gun=baslangic_gun,
            bitis_gun=bitis_gun,
            toplam_kurus=toplam_kurus,
            gun_bazinda_seyir=seyir,
        )
