"""
Kullanici servisinin iş kurallarını doğrular.

Formül testleri (kalan_gun_hesapla → eksik_kurus_hesapla) saf fonksiyon
olduğu için Mongo'ya ihtiyaç DUYMAZ — deterministik `date` ile çalışırlar.
`KullaniciService` üzerinden Mongo'ya giden testler `conftest.temiz_veritabani`
ile temizlenen ayrı test veritabanına karşı çalışır (auth ile aynı desen);
yerel MongoDB kurulu değilse bu testler bağlantı hatasıyla düşer — bu
BEKLENEN bir durumdur (bkz. görev notu).
"""
from __future__ import annotations

from datetime import date

import pytest

from app.core.database import get_database
from app.core.errors import GelirGerekli, PlanNegatifKalan
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_model import KullaniciProfilBelgesi
from app.modules.kullanici.kullanici_service import (
    KullaniciService,
    birikim_kurus_hesapla,
    eksik_kurus_hesapla,
    gunluk_limit_hesapla,
    kalan_gun_hesapla,
    pay_yuzdeleri_hesapla,
    plan_negatif_mi,
    sosyal_kurus_hesapla,
    zorunlu_kurus_hesapla,
)


def _servis() -> KullaniciService:
    return KullaniciService(get_database())


# ---------------------------------------------------------------------------
# Formül testleri — Mongo'suz, saf fonksiyon (delta-v4.md satır 764-792)
# ---------------------------------------------------------------------------


def test_kalan_gun_maas_gununden_once_bu_ayki_odemeye_kadar_sayar() -> None:
    # Örnek: maaş günü 15, bugün 17 Eylül → sonraki ödeme 15 Ekim, kalan 28 gün.
    assert kalan_gun_hesapla(date(2024, 9, 17), 15) == 28


def test_kalan_gun_tam_maas_gununde_yeni_donem_baslar() -> None:
    # Bugün maaş günüyse dönem sıfırlanır, bir sonraki maaş gününe kadar sayılır.
    assert kalan_gun_hesapla(date(2024, 9, 15), 15) == 30  # Eylül 15 -> Ekim 15


def test_kalan_gun_ayda_olmayan_gun_ayin_sonuna_duser() -> None:
    # Maaş günü 31, Şubat'ta 29 (2024 artık yıl) gün var -> o günde ödenir.
    assert kalan_gun_hesapla(date(2024, 2, 1), 31) == 28


def test_kalan_gun_duzensiz_maasta_30_gun_sabit() -> None:
    assert kalan_gun_hesapla(date(2024, 9, 17), None) == 30


def test_gunluk_limit_asagi_yuvarlanir() -> None:
    # 8.400 TL / 28 gün = 300 TL tam; küsuratlı bir örnek aşağı yuvarlamayı kanıtlar.
    assert gunluk_limit_hesapla(840_000, 28) == 30_000
    assert gunluk_limit_hesapla(840_050, 28) == 30_000  # 30.001,78 -> aşağı 30.000
    assert gunluk_limit_hesapla(100, 3) == 0  # 33 kuruş -> tam liraya yuvarlanınca 0


def test_gunluk_limit_sifir_gunde_sifir_doner() -> None:
    assert gunluk_limit_hesapla(840_000, 0) == 0


def test_plan_hesap_zinciri_prototip_ornegiyle_birebir_eslesir() -> None:
    """delta-v4.md satır 781-787'deki örnek kullanıcı: gelir 32.000 ₺, giderler
    18.800 ₺, birikim %15, maaş günü 15, 17 Eylül'de kalan gün 28 → limit 300 ₺."""
    gelir = 3_200_000
    zorunlu = zorunlu_kurus_hesapla(1_250_000, 284_000, 190_000, 156_000)
    assert zorunlu == 1_880_000
    assert plan_negatif_mi(gelir, zorunlu) is False

    birikim = birikim_kurus_hesapla(gelir, 15)
    assert birikim == 480_000

    sosyal = sosyal_kurus_hesapla(gelir, zorunlu, birikim)
    assert sosyal == 840_000

    zorunlu_pay, sosyal_pay, birikim_pay = pay_yuzdeleri_hesapla(gelir, zorunlu, sosyal, birikim)
    assert (zorunlu_pay, sosyal_pay, birikim_pay) == (59, 26, 15)

    kalan_gun = kalan_gun_hesapla(date(2024, 9, 17), 15)
    assert gunluk_limit_hesapla(sosyal, kalan_gun) == 30_000


# ---------------------------------------------------------------------------
# QA-1/K-087 deseni: "bugün" istemciden gelir, sunucu UTC'den TÜRETMEZ.
# TR saatiyle 00:00-02:59 arası UTC hâlâ bir önceki güne bakar (UTC+3 farkı);
# maaş günü sınırında istemcinin günü ile sunucunun UTC günü farklı
# `kalan_gun`/`gunluk_limit_kurus` üretmemeli — hesap İSTEMCİNİN gününe göre.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("istemci_bugunu", "sunucu_utc_bugunu", "beklenen_kalan_gun"),
    [
        # Maaş günü 15; istemci (TR yereli) 14 Eylül'de, sunucu UTC'de henüz
        # 13 Eylül gece yarısını yeni geçmiş olabilir -> istemci gününe göre
        # dönem hâlâ 15 Eylül'e kadar (1 gün kalan), UTC günüyle 2 gün kalırdı.
        (date(2024, 9, 14), date(2024, 9, 13), 1),
        # İstemci TAM maaş gününde (15) -> yeni dönem başlar (30 gün), ama
        # sunucu UTC'ye göre hâlâ 14'te kalsaydı eski dönemde 1 gün kalırdı.
        (date(2024, 9, 15), date(2024, 9, 14), 30),
        # İstemci maaş gününü YENİ geçmiş (16) -> yeni dönemde 29 gün kalan;
        # sunucu UTC'de hâlâ 15'teyse (tam maaş günü) 30 gün hesaplardı.
        (date(2024, 9, 16), date(2024, 9, 15), 29),
    ],
)
def test_kalan_gun_maas_sinirinda_istemcinin_gunune_gore_hesaplanir(
    istemci_bugunu: date, sunucu_utc_bugunu: date, beklenen_kalan_gun: int
) -> None:
    maas_gunu = 15
    # İstemcinin gönderdiği gün doğru sonucu üretir.
    assert kalan_gun_hesapla(istemci_bugunu, maas_gunu) == beklenen_kalan_gun
    # Sunucunun kendi UTC "bugünü" ile hesaplarsa (düzeltme öncesi hatalı
    # davranış) FARKLI bir sonuç çıkar — iki günün asla karışmaması gerektiğini
    # kanıtlar.
    assert kalan_gun_hesapla(sunucu_utc_bugunu, maas_gunu) != beklenen_kalan_gun


def test_gunluk_limit_maas_sinirinda_istemcinin_gunune_gore_farklilasir() -> None:
    """`kalan_gun` istemci/sunucu gününe göre ayrışınca `gunluk_limit_kurus` da
    ayrışır — QA'nın işaret ettiği kullanıcı etkisi budur (ekrandakinden
    farklı limitle plan kurulması)."""
    sosyal_pay_kurus = 840_000
    maas_gunu = 15

    istemci_kalan_gun = kalan_gun_hesapla(date(2024, 9, 16), maas_gunu)  # 29
    sunucu_utc_kalan_gun = kalan_gun_hesapla(date(2024, 9, 15), maas_gunu)  # 30

    istemci_limit = gunluk_limit_hesapla(sosyal_pay_kurus, istemci_kalan_gun)
    sunucu_limit = gunluk_limit_hesapla(sosyal_pay_kurus, sunucu_utc_kalan_gun)

    assert istemci_limit != sunucu_limit


def test_negatif_kalan_plan_kurulamaz_ve_eksik_tutar_pozitif() -> None:
    gelir = 1_000_000
    zorunlu = zorunlu_kurus_hesapla(1_200_000, None, None, None)
    assert plan_negatif_mi(gelir, zorunlu) is True
    assert eksik_kurus_hesapla(gelir, zorunlu) == 200_000


def test_katman2_dolan_kart_sayisi_bos_profilde_sifir() -> None:
    profil = KullaniciProfilBelgesi.varsayilan("kullanici-x")
    assert profil.katman2_dolan_kart_sayisi() == 0


def test_katman2_dolan_kart_sayisi_dolu_alanlari_sayar() -> None:
    profil = KullaniciProfilBelgesi(
        kullanici_id="kullanici-x",
        kira_aidat_kurus=100_000,
        kahve={"siklik": "gun1", "serbest_sayi": None, "fiyat_kurus": 5000},
        birikim_yuzde=15,
    )
    assert profil.katman2_dolan_kart_sayisi() == 3  # sabit giderler + kahve + birikim kartları


# ---------------------------------------------------------------------------
# Mongo'ya karşı servis testleri (bkz. modül docstring — yerel Mongo gerekir)
# ---------------------------------------------------------------------------


async def test_bos_profil_varsayilan_degerlerle_doner(temiz_veritabani: None) -> None:
    profil = await _servis().profili_getir("kullanici-hic-veri-girmemis")

    assert profil.onboarding_tamamlandi is False
    assert profil.gelir_kurus is None


async def test_katman1_kaydet_onboardingi_tamamlanmis_isaretler(temiz_veritabani: None) -> None:
    servis = _servis()

    profil = await servis.katman1_kaydet("kullanici-1", "tasarruf", 3_200_000, 15, False)

    assert profil.niyet == "tasarruf"
    assert profil.gelir_kurus == 3_200_000
    assert profil.onboarding_tamamlandi is True


async def test_katman1_duzensiz_maasta_maas_gunu_temizlenir(temiz_veritabani: None) -> None:
    servis = _servis()

    profil = await servis.katman1_kaydet("kullanici-1", "takip", 1_000_000, 15, True)

    assert profil.maas_duzensiz is True
    assert profil.maas_gunu is None


async def test_katman2_kismi_guncelleme_diger_alanlari_ezmez(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman2_kaydet("kullanici-1", {"kira_aidat_kurus": 100_000, "birikim_yuzde": 15})

    guncellenmis = await servis.katman2_kaydet(
        "kullanici-1", {"kahve": {"siklik": "gun1", "serbest_sayi": None, "fiyat_kurus": 3000}}
    )

    assert guncellenmis.kira_aidat_kurus == 100_000  # önceki tur ezilmedi
    assert guncellenmis.birikim_yuzde == 15
    assert guncellenmis.kahve["siklik"] == "gun1"


async def test_plani_kur_hesaplayip_kaydeder(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-plan", "tasarruf", 3_200_000, 15, False)
    await servis.katman2_kaydet(
        "kullanici-plan",
        {
            "kira_aidat_kurus": 1_250_000,
            "faturalar_kurus": 284_000,
            "ulasim_yakit_kurus": 190_000,
            "kredi_taksit_kurus": 156_000,
            "birikim_yuzde": 15,
        },
    )

    profil = await servis.plani_kur("kullanici-plan", bugun=date(2024, 9, 17))

    assert profil.plan_kuruldu is True
    # Yeni otomatik bütçe takvim ayına yayılır: (3.200.000 - 1.880.000 - 480.000) / 30.
    assert profil.gunluk_limit_kurus == 28_000
    assert profil.zorunlu_pay_yuzde == 59
    assert profil.plan_kurulum_tarihi is not None


async def test_plani_kur_gelir_yokken_zarif_hata_verir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman2_kaydet("kullanici-gelirsiz", {"kira_aidat_kurus": 100_000})

    with pytest.raises(GelirGerekli):
        await servis.plani_kur("kullanici-gelirsiz")


async def test_plani_kur_negatif_kalanda_kurulmaz(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-negatif", "borc", 1_000_000, 15, False)
    await servis.katman2_kaydet("kullanici-negatif", {"kira_aidat_kurus": 1_200_000})

    with pytest.raises(PlanNegatifKalan) as hata_bilgisi:
        await servis.plani_kur("kullanici-negatif")

    assert hata_bilgisi.value.eksik_kurus == 200_000


async def test_gunluk_limiti_ayarla_plani_bozmadan_limiti_degistirir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-limit", "tasarruf", 3_200_000, 15, False)
    await servis.katman2_kaydet("kullanici-limit", {"birikim_yuzde": 15})
    await servis.plani_kur("kullanici-limit", bugun=date(2024, 9, 17))

    profil = await servis.gunluk_limiti_ayarla("kullanici-limit", 25_000)

    assert profil.gunluk_limit_kurus == 25_000
    assert profil.plan_kuruldu is True  # elle limit değişikliği planı bozmaz


async def test_baska_kullanicinin_profiline_erisilemez(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-a", "tasarruf", 5_000_000, 1, False)
    await servis.katman1_kaydet("kullanici-b", "borc", 1_000_000, 10, False)

    profil_a = await servis.profili_getir("kullanici-a")
    profil_b = await servis.profili_getir("kullanici-b")

    assert profil_a.gelir_kurus == 5_000_000
    assert profil_b.gelir_kurus == 1_000_000  # kullanici-a'nın güncellemesi b'ye sızmadı


# ---------------------------------------------------------------------------
# Madde 0(b) — gunluk_limit_onerisi_kurus / son_kart + Madde 0(c) — tercihler
# ---------------------------------------------------------------------------


async def test_katman1_oneriyi_saklar_ama_gercek_limite_yazmaz(temiz_veritabani: None) -> None:
    servis = _servis()

    profil = await servis.katman1_kaydet("kullanici-oneri", "tasarruf", 3_200_000, 15, False, 30_000)

    assert profil.gunluk_limit_onerisi_kurus == 30_000
    assert profil.gunluk_limit_kurus is None  # kabul edilmeden gerçek limit yazılmaz (K-059/5)


async def test_gunluk_limiti_ayarla_bekleyen_oneriyi_temizler(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-oneri", "tasarruf", 3_200_000, 15, False, 30_000)

    profil = await servis.gunluk_limiti_ayarla("kullanici-oneri", 30_000)

    assert profil.gunluk_limit_kurus == 30_000
    assert profil.gunluk_limit_onerisi_kurus is None


async def test_oneriyi_reddet_gercek_limite_dokunmaz(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-oneri", "tasarruf", 3_200_000, 15, False, 30_000)

    profil = await servis.oneriyi_reddet("kullanici-oneri")

    assert profil.gunluk_limit_onerisi_kurus is None
    assert profil.gunluk_limit_kurus is None  # "Limitsiz devam et" — gerçek limit yazılmadı


async def test_katman2_son_kart_kaydedilir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-kart", "tasarruf", 3_200_000, 15, False)

    profil = await servis.katman2_kaydet("kullanici-kart", {"son_kart": 4})

    assert profil.son_kart == 4


async def test_tercihler_varsayilan_degerlerle_doner(temiz_veritabani: None) -> None:
    profil = await _servis().profili_getir("kullanici-hic-tercih-girmemis")

    assert profil.bildirim_aksam_ozet is True
    assert profil.bildirim_tercih_belirlendi is False
    assert profil.bildirim_saati == "21.00"
    assert profil.gun_siniri == 0
    assert profil.varsayilan_odeme == "kart"
    assert profil.kurulum_gunu is None


async def test_tercihleri_guncelle_bildirim_tercihini_belirlenmis_isaretler(temiz_veritabani: None) -> None:
    servis = _servis()

    profil = await servis.tercihleri_guncelle("kullanici-tercih", {"bildirim_aksam_ozet": False})

    assert profil.bildirim_aksam_ozet is False
    assert profil.bildirim_tercih_belirlendi is True


async def test_kurulum_gunu_bir_kez_yazilinca_sabitlenir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tercihleri_guncelle("kullanici-kurulum", {"kurulum_gunu": "2026-09-19"})

    profil = await servis.tercihleri_guncelle("kullanici-kurulum", {"kurulum_gunu": "2026-10-01"})

    assert profil.kurulum_gunu == "2026-09-19"  # K-049 — bir kez sabitlenince değişmez


async def test_tercihleri_guncelle_bos_alanlarla_profili_degistirmeden_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tercihleri_guncelle("kullanici-tercih-bos", {"gun_siniri": 3})

    profil = await servis.tercihleri_guncelle("kullanici-tercih-bos", {})

    assert profil.gun_siniri == 3


# ---------------------------------------------------------------------------
# Madde 5 — PATCH Katman 1 (K-084/1, BE-4b)
# ---------------------------------------------------------------------------


async def test_katman1_guncelle_yalniz_gonderilen_alani_degistirir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-k1-patch", "tasarruf", 3_200_000, 15, False)

    profil = await servis.katman1_guncelle("kullanici-k1-patch", {"gelir_kurus": 4_000_000})

    assert profil.gelir_kurus == 4_000_000
    assert profil.niyet == "tasarruf"  # gönderilmeyen alan dokunulmadan kalır
    assert profil.maas_gunu == 15


async def test_katman1_guncelle_duzensiz_maasta_maas_gunu_temizlenir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-k1-duzensiz", "tasarruf", 3_200_000, 15, False)

    profil = await servis.katman1_guncelle("kullanici-k1-duzensiz", {"maas_duzensiz": True})

    assert profil.maas_duzensiz is True
    assert profil.maas_gunu is None


async def test_katman1_guncelle_onboarding_bayragina_dokunmaz(temiz_veritabani: None) -> None:
    servis = _servis()
    profil_once = await servis.profili_getir("kullanici-k1-onboard")
    assert profil_once.onboarding_tamamlandi is False

    profil = await servis.katman1_guncelle("kullanici-k1-onboard", {"gelir_kurus": 1_000_000})

    assert profil.onboarding_tamamlandi is False  # yalnız PUT (katman1_kaydet) bunu işaretler


# ---------------------------------------------------------------------------
# Madde 6 — elle günlük limit değişikliği `limit_gecmisi`ne de yazılır (K-085, BE-4b)
# ---------------------------------------------------------------------------


async def test_gunluk_limiti_ayarla_limit_gecmisine_ayni_degeri_yazar(temiz_veritabani: None) -> None:
    servis = _servis()

    profil = await servis.gunluk_limiti_ayarla("kullanici-limit-gecmis", 18_000)

    harcama_servisi = HarcamaService(get_database())
    bugun = date.today().isoformat()
    efektif = await harcama_servisi.limit_gecmisi_efektif_limit("kullanici-limit-gecmis", bugun, 0)
    assert efektif == profil.gunluk_limit_kurus == 18_000


async def test_gunluk_limiti_ayarla_istemcinin_gunune_yazar_sunucu_utcsine_degil(temiz_veritabani: None) -> None:
    """QA-1b/K-064 — TR 00:00-02:59 sınırında istemcinin günü ile sunucu UTC günü
    farklıyken `limit_gecmisi` satırı istemcinin gününe düşmeli, sunucununkine değil."""
    servis = _servis()
    istemci_bugunu = date(2026, 1, 2)  # sunucu UTC'de henüz 1 Ocak olabilir

    profil = await servis.gunluk_limiti_ayarla("kullanici-limit-tz", 22_000, bugun=istemci_bugunu)

    harcama_servisi = HarcamaService(get_database())
    efektif_istemci_gunu = await harcama_servisi.limit_gecmisi_efektif_limit(
        "kullanici-limit-tz", istemci_bugunu.isoformat(), 0
    )
    efektif_sunucu_utc_gunu = await harcama_servisi.limit_gecmisi_efektif_limit(
        "kullanici-limit-tz", date(2026, 1, 1).isoformat(), 0
    )
    assert efektif_istemci_gunu == profil.gunluk_limit_kurus == 22_000
    assert efektif_sunucu_utc_gunu == 0  # 1 Ocak'a yazılmamış olmalı


# ---------------------------------------------------------------------------
# Madde 1 — hesap silinirken kullanılan profil temizleme arayüzü (K-085, BE-4b)
# ---------------------------------------------------------------------------


async def test_kullanici_verisini_sil_profili_kaldirir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.katman1_kaydet("kullanici-sil", "tasarruf", 3_200_000, 15, False)

    await servis.kullanici_verisini_sil("kullanici-sil")

    profil = await servis.profili_getir("kullanici-sil")
    assert profil.onboarding_tamamlandi is False  # varsayılan (boş) profile döndü


async def test_kullanici_verisini_sil_hic_profili_olmayan_kullanicida_hata_vermez(
    temiz_veritabani: None,
) -> None:
    # delete_one eşleşme bulamasa da hata vermez — idempotent.
    await _servis().kullanici_verisini_sil("hic-profili-olmayan")
