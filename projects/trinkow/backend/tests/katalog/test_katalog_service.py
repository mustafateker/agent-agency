"""
Katalog servisinin iş kurallarını doğrular.

`_surum_hesapla` saf fonksiyon olduğu ve `VARSAYILAN_KATALOG` sabiti Mongo
gerektirmediği için ilk grup test Mongo'suz koşar. `KatalogService` üzerinden
Mongo'ya giden testler `temiz_veritabani` fixture'ını açıkça ister
(conftest.py); yerel MongoDB kurulu değilse bu testler bağlantı hatasıyla
düşer — BEKLENEN.
"""
from __future__ import annotations

import pytest

from app.core.database import get_database
from app.core.errors import KatalogOgesiBulunamadi
from app.modules.katalog.katalog_model import KatalogOgesiBelgesi
from app.modules.katalog.katalog_service import (
    VARSAYILAN_KATALOG,
    KatalogService,
    _surum_hesapla,
)


def _servis() -> KatalogService:
    return KatalogService(get_database())


# ---------------------------------------------------------------------------
# Saf testler — Mongo'suz
# ---------------------------------------------------------------------------


def test_varsayilan_katalog_seksen_kalem_tasir() -> None:
    assert len(VARSAYILAN_KATALOG) == 80


def test_varsayilan_katalogda_fiyat_marka_gorsel_miktar_alani_yoktur() -> None:
    """K-050/K-037: her kalem yalnız (kod, ad, kategori, sira) dörtlüsüdür."""
    for kalem in VARSAYILAN_KATALOG:
        assert len(kalem) == 4
        kod, ad, kategori, sira = kalem
        assert isinstance(kod, str) and kod
        assert isinstance(ad, str) and ad
        assert isinstance(kategori, str) and kategori
        assert isinstance(sira, int)


def test_katalog_ogesi_belgesi_fiyat_alani_kabul_etmez() -> None:
    """Şema seviyesinde de fiyat alanı yok: `belgeye_cevir` yalnız bilinen dört anahtarı üretir."""
    belge = KatalogOgesiBelgesi(kod="test-kod", ad="Test", kategori="market", sira=0)
    assert set(belge.belgeye_cevir().keys()) == {"kod", "ad", "kategori", "sira"}


def test_surum_hesapla_sira_bagimsizdir_ama_icerige_duyarlidir() -> None:
    ogeler_a = [
        KatalogOgesiBelgesi(kod="a", ad="A", kategori="market", sira=0),
        KatalogOgesiBelgesi(kod="b", ad="B", kategori="market", sira=1),
    ]
    ogeler_b = list(reversed(ogeler_a))  # aynı içerik, ters sıra
    assert _surum_hesapla(ogeler_a) == _surum_hesapla(ogeler_b)

    ogeler_degisik = [
        KatalogOgesiBelgesi(kod="a", ad="A", kategori="market", sira=0),
        KatalogOgesiBelgesi(kod="b", ad="B DEĞİŞTİ", kategori="market", sira=1),
    ]
    assert _surum_hesapla(ogeler_a) != _surum_hesapla(ogeler_degisik)


def test_surum_hesapla_bos_katalogda_da_calisir() -> None:
    assert isinstance(_surum_hesapla([]), str)
    assert _surum_hesapla([]) != ""


# ---------------------------------------------------------------------------
# Mongo'ya giden testler
# ---------------------------------------------------------------------------


async def test_tohumlama_bos_koleksiyonu_seksen_kalemle_doldurur(temiz_veritabani: None) -> None:
    servis = _servis()
    eklenen = await servis.tohumla()
    assert eklenen == 80

    ogeler, _surum = await servis.katalogu_listele()
    assert len(ogeler) == 80


async def test_tohumlama_idempotenttir_ikinci_cagri_kalem_eklemez(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tohumla()
    ikinci_cagri_eklenen = await servis.tohumla()

    assert ikinci_cagri_eklenen == 0
    ogeler, _surum = await servis.katalogu_listele()
    assert len(ogeler) == 80


async def test_katalogu_listele_kaynak_sirasiyla_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tohumla()

    ogeler, _surum = await servis.katalogu_listele()
    assert ogeler[0].kod == "filtre-kahve"
    assert ogeler[-1].kod == "sans-oyunu"


async def test_oge_getir_bulunan_kalemi_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tohumla()

    belge = await servis.oge_getir("sigara-paketi")
    assert belge.ad == "Sigara paketi"
    assert belge.kategori == "aliskanliklar"


async def test_oge_getir_olmayan_koda_hata_verir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tohumla()

    with pytest.raises(KatalogOgesiBulunamadi):
        await servis.oge_getir("fotokopi")  # bilerek katalogda yok


async def test_surum_katalog_icerigi_degisince_degisir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.tohumla()

    _ogeler, ilk_surum = await servis.katalogu_listele()

    veritabani = get_database()
    await veritabani["katalog_ogeleri"].update_one(
        {"kod": "filtre-kahve"}, {"$set": {"ad": "Filtre kahve (güncellendi)"}}
    )

    _ogeler_yeni, yeni_surum = await servis.katalogu_listele()
    assert yeni_surum != ilk_surum
