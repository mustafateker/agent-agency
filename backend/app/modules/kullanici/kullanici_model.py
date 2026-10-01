"""
Mongo `kullanici_profilleri` koleksiyonunda saklanan belgenin şeması.

DTO'dan (kullanici_dto.py) bilerek ayrı tutulur — auth_model.py ile aynı
ilke (K-068/3): burası içeride saklanan hâl, DTO dışarıya açılan
sözleşmedir. Alan adları istemcideki `profil` tablosuyla (app/src/db/
semasi.ts, şema sürümü 5) birebir eşleşecek şekilde seçildi. Cevaplanmamış
alan `None`dır, `0` ile DOLDURULMAZ (istemciyle aynı kural — 0 "hiç
harcamıyorum", null "cevaplamadım" demektir).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

Niyet = Literal["takip", "tasarruf", "borc"]
Siklik = Literal["gun1", "gun2", "hafta2_3", "hafta1", "ay1_2", "hic", "serbest"]
YatirimNiyet = Literal["yapiyorum", "dusunuyorum", "ilgilenmiyorum"]
TaksitSiklik = Literal["sik_sik", "bazen", "nadiren"]
GunSiniriSaat = Literal[0, 3, 6]
OdemeTipi = Literal["nakit", "kart"]

_BOS_ALISKANLIK: dict[str, Any] = {"siklik": None, "serbest_sayi": None, "fiyat_kurus": None}


class KullaniciProfilBelgesi:
    """Mongo `kullanici_profilleri` koleksiyonundaki bir belgeyi Python nesnesine çevirir.

    Tek kullanıcı = tek belge; `kullanici_id` üstünde unique index vardır
    (bkz. `app.core.database.indeksleri_kur`). Belge yoksa `varsayilan()`
    ile istemcideki `VARSAYILAN`/`DETAY_VARSAYILAN` karşılığı üretilir.
    """

    def __init__(
        self,
        kullanici_id: str,
        niyet: Niyet | None = None,
        gelir_kurus: int | None = None,
        maas_gunu: int | None = None,
        maas_duzensiz: bool = False,
        onboarding_tamamlandi: bool = False,
        kira_aidat_kurus: int | None = None,
        faturalar_kurus: int | None = None,
        ulasim_yakit_kurus: int | None = None,
        kredi_taksit_kurus: int | None = None,
        kahve: dict[str, Any] | None = None,
        sigara: dict[str, Any] | None = None,
        alkol: dict[str, Any] | None = None,
        yemek: dict[str, Any] | None = None,
        abonelik_adet: int | None = None,
        abonelik_ortalama_kurus: int | None = None,
        yatirim_niyet: YatirimNiyet | None = None,
        birikim_yuzde: int | None = None,
        taksit_siklik: TaksitSiklik | None = None,
        plan_kuruldu: bool = False,
        zorunlu_kurus: int | None = None,
        zorunlu_pay_yuzde: int | None = None,
        sosyal_kurus: int | None = None,
        sosyal_pay_yuzde: int | None = None,
        birikim_kurus: int | None = None,
        birikim_pay_yuzde: int | None = None,
        gunluk_limit_kurus: int | None = None,
        plan_kurulum_tarihi: datetime | None = None,
        gunluk_limit_onerisi_kurus: int | None = None,
        son_kart: int | None = None,
        bildirim_aksam_ozet: bool = True,
        bildirim_tercih_belirlendi: bool = False,
        bildirim_saati: str = "21.00",
        gun_siniri: GunSiniriSaat = 0,
        varsayilan_odeme: OdemeTipi = "kart",
        kurulum_gunu: str | None = None,
        en_uzun_seri: int = 0,
        en_uzun_seri_bitis_gunu: str | None = None,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.niyet = niyet
        self.gelir_kurus = gelir_kurus
        self.maas_gunu = maas_gunu
        self.maas_duzensiz = maas_duzensiz
        self.onboarding_tamamlandi = onboarding_tamamlandi
        self.kira_aidat_kurus = kira_aidat_kurus
        self.faturalar_kurus = faturalar_kurus
        self.ulasim_yakit_kurus = ulasim_yakit_kurus
        self.kredi_taksit_kurus = kredi_taksit_kurus
        self.kahve = kahve or dict(_BOS_ALISKANLIK)
        self.sigara = sigara or dict(_BOS_ALISKANLIK)
        self.alkol = alkol or dict(_BOS_ALISKANLIK)
        self.yemek = yemek or dict(_BOS_ALISKANLIK)
        self.abonelik_adet = abonelik_adet
        self.abonelik_ortalama_kurus = abonelik_ortalama_kurus
        self.yatirim_niyet = yatirim_niyet
        self.birikim_yuzde = birikim_yuzde
        self.taksit_siklik = taksit_siklik
        self.plan_kuruldu = plan_kuruldu
        self.zorunlu_kurus = zorunlu_kurus
        self.zorunlu_pay_yuzde = zorunlu_pay_yuzde
        self.sosyal_kurus = sosyal_kurus
        self.sosyal_pay_yuzde = sosyal_pay_yuzde
        self.birikim_kurus = birikim_kurus
        self.birikim_pay_yuzde = birikim_pay_yuzde
        self.gunluk_limit_kurus = gunluk_limit_kurus
        self.plan_kurulum_tarihi = plan_kurulum_tarihi
        # K-059/5 — onaylanana kadar GERÇEK limit değildir; yalnız Katman 1'in
        # önerisidir. Kabul edilince gunluk_limit_kurus'a yazılır ve bu alan
        # temizlenir (bkz. kullanici_service.gunluk_limiti_ayarla/oneriyi_reddet).
        self.gunluk_limit_onerisi_kurus = gunluk_limit_onerisi_kurus
        # Katman 2'de "kaldığın yerden" — en son açık bırakılan kart (1-8).
        self.son_kart = son_kart
        # D-2c-1 · E-19 uygulama tercihleri (istemcideki `ayar` tablosunun
        # sunucudaki karşılığı, K-068: veri sunucuda).
        self.bildirim_aksam_ozet = bildirim_aksam_ozet
        self.bildirim_tercih_belirlendi = bildirim_tercih_belirlendi
        self.bildirim_saati = bildirim_saati
        self.gun_siniri = gun_siniri
        self.varsayilan_odeme = varsayilan_odeme
        # Yalnız İLK kez ayarlanır, bir daha DEĞİŞMEZ (K-049 sınırı) —
        # bkz. kullanici_service.tercihleri_guncelle.
        self.kurulum_gunu = kurulum_gunu
        # K-048/F-16f + K-077 (BE-5b Madde 1) — seri kırılsa/limitsiz kipe
        # geçilse de en uzun seri KAYBOLMAZ. `kullanici_profilleri`nde
        # saklanır (ayrı bir `ozet` koleksiyonu yerine): tek kullanıcı için
        # tek kalıcı sayaç olduğundan `gunluk_limit_kurus` gibi diğer profil
        # alanlarıyla aynı doğaya sahip; istemcideki karşılığı da genel
        # `ayar` anahtar-değer tablosunda (`seri_en_uzun_gun`) tutuluyor.
        # RATCHET kuralı (yalnız büyür) burada DEĞİL, `ozet_service`de
        # uygulanır — bu alan yalnız SON DEĞERİ taşır.
        self.en_uzun_seri = en_uzun_seri
        self.en_uzun_seri_bitis_gunu = en_uzun_seri_bitis_gunu

    def belgeye_cevir(self) -> dict[str, Any]:
        """Mongo'ya yazılacak sözlük gösterimini üretir."""
        return {
            "kullanici_id": self.kullanici_id,
            "niyet": self.niyet,
            "gelir_kurus": self.gelir_kurus,
            "maas_gunu": self.maas_gunu,
            "maas_duzensiz": self.maas_duzensiz,
            "onboarding_tamamlandi": self.onboarding_tamamlandi,
            "kira_aidat_kurus": self.kira_aidat_kurus,
            "faturalar_kurus": self.faturalar_kurus,
            "ulasim_yakit_kurus": self.ulasim_yakit_kurus,
            "kredi_taksit_kurus": self.kredi_taksit_kurus,
            "kahve": self.kahve,
            "sigara": self.sigara,
            "alkol": self.alkol,
            "yemek": self.yemek,
            "abonelik_adet": self.abonelik_adet,
            "abonelik_ortalama_kurus": self.abonelik_ortalama_kurus,
            "yatirim_niyet": self.yatirim_niyet,
            "birikim_yuzde": self.birikim_yuzde,
            "taksit_siklik": self.taksit_siklik,
            "plan_kuruldu": self.plan_kuruldu,
            "zorunlu_kurus": self.zorunlu_kurus,
            "zorunlu_pay_yuzde": self.zorunlu_pay_yuzde,
            "sosyal_kurus": self.sosyal_kurus,
            "sosyal_pay_yuzde": self.sosyal_pay_yuzde,
            "birikim_kurus": self.birikim_kurus,
            "birikim_pay_yuzde": self.birikim_pay_yuzde,
            "gunluk_limit_kurus": self.gunluk_limit_kurus,
            "plan_kurulum_tarihi": self.plan_kurulum_tarihi,
            "gunluk_limit_onerisi_kurus": self.gunluk_limit_onerisi_kurus,
            "son_kart": self.son_kart,
            "bildirim_aksam_ozet": self.bildirim_aksam_ozet,
            "bildirim_tercih_belirlendi": self.bildirim_tercih_belirlendi,
            "bildirim_saati": self.bildirim_saati,
            "gun_siniri": self.gun_siniri,
            "varsayilan_odeme": self.varsayilan_odeme,
            "kurulum_gunu": self.kurulum_gunu,
            "en_uzun_seri": self.en_uzun_seri,
            "en_uzun_seri_bitis_gunu": self.en_uzun_seri_bitis_gunu,
        }

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "KullaniciProfilBelgesi":
        """Mongo'dan okunan sözlüğü nesneye çevirir."""
        return KullaniciProfilBelgesi(
            _id=belge.get("_id"),
            kullanici_id=belge["kullanici_id"],
            niyet=belge.get("niyet"),
            gelir_kurus=belge.get("gelir_kurus"),
            maas_gunu=belge.get("maas_gunu"),
            maas_duzensiz=belge.get("maas_duzensiz", False),
            onboarding_tamamlandi=belge.get("onboarding_tamamlandi", False),
            kira_aidat_kurus=belge.get("kira_aidat_kurus"),
            faturalar_kurus=belge.get("faturalar_kurus"),
            ulasim_yakit_kurus=belge.get("ulasim_yakit_kurus"),
            kredi_taksit_kurus=belge.get("kredi_taksit_kurus"),
            kahve=belge.get("kahve"),
            sigara=belge.get("sigara"),
            alkol=belge.get("alkol"),
            yemek=belge.get("yemek"),
            abonelik_adet=belge.get("abonelik_adet"),
            abonelik_ortalama_kurus=belge.get("abonelik_ortalama_kurus"),
            yatirim_niyet=belge.get("yatirim_niyet"),
            birikim_yuzde=belge.get("birikim_yuzde"),
            taksit_siklik=belge.get("taksit_siklik"),
            plan_kuruldu=belge.get("plan_kuruldu", False),
            zorunlu_kurus=belge.get("zorunlu_kurus"),
            zorunlu_pay_yuzde=belge.get("zorunlu_pay_yuzde"),
            sosyal_kurus=belge.get("sosyal_kurus"),
            sosyal_pay_yuzde=belge.get("sosyal_pay_yuzde"),
            birikim_kurus=belge.get("birikim_kurus"),
            birikim_pay_yuzde=belge.get("birikim_pay_yuzde"),
            gunluk_limit_kurus=belge.get("gunluk_limit_kurus"),
            plan_kurulum_tarihi=belge.get("plan_kurulum_tarihi"),
            gunluk_limit_onerisi_kurus=belge.get("gunluk_limit_onerisi_kurus"),
            son_kart=belge.get("son_kart"),
            bildirim_aksam_ozet=belge.get("bildirim_aksam_ozet", True),
            bildirim_tercih_belirlendi=belge.get("bildirim_tercih_belirlendi", False),
            bildirim_saati=belge.get("bildirim_saati", "21.00"),
            gun_siniri=belge.get("gun_siniri", 0),
            varsayilan_odeme=belge.get("varsayilan_odeme", "kart"),
            kurulum_gunu=belge.get("kurulum_gunu"),
            en_uzun_seri=belge.get("en_uzun_seri", 0),
            en_uzun_seri_bitis_gunu=belge.get("en_uzun_seri_bitis_gunu"),
        )

    @staticmethod
    def varsayilan(kullanici_id: str) -> "KullaniciProfilBelgesi":
        """Kullanıcı henüz hiç veri girmemişse döndürülecek boş profil."""
        return KullaniciProfilBelgesi(kullanici_id=kullanici_id)

    def katman2_dolan_kart_sayisi(self) -> int:
        """E-25'in 8 kartından kaçının doldurulduğunu sayar.

        İstemcideki `katman2DolanKartSayisi` (db/profil.ts) ile AYNI kural —
        kod tekrarı bilinçli, oradaki yorumla aynı gerekçe: iki tarafın da
        aynı ekranı türetmesi gerekiyor ama dosyalar birbirini import etmiyor.
        """
        sayac = 0
        if (
            self.kira_aidat_kurus is not None
            or self.faturalar_kurus is not None
            or self.ulasim_yakit_kurus is not None
            or self.kredi_taksit_kurus is not None
        ):
            sayac += 1
        if self.kahve.get("siklik") is not None:
            sayac += 1
        if self.sigara.get("siklik") is not None:
            sayac += 1
        if self.alkol.get("siklik") is not None:
            sayac += 1
        if self.yemek.get("siklik") is not None:
            sayac += 1
        if self.abonelik_adet is not None or self.abonelik_ortalama_kurus is not None:
            sayac += 1
        if self.yatirim_niyet is not None:
            sayac += 1
        if self.birikim_yuzde is not None:
            sayac += 1
        return sayac
