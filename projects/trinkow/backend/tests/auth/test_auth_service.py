"""
Auth servisinin iş kurallarını gerçek (ayrı) test MongoDB'sine karşı
doğrular: mutlu yol + çakışma/hata durumları.

Veritabanı her test öncesi/sonrası `conftest.temiz_veritabani` tarafından
temizlenir, bu yüzden testler birbirinden bağımsızdır.
"""
from __future__ import annotations

from datetime import timedelta

import pytest

from app.core.database import get_database
from app.core.errors import (
    EpostaZatenKayitli,
    GecersizKimlikBilgisi,
    GecersizToken,
    KullaniciBulunamadi,
    TokenSuresiDolmus,
)
from app.core.security import yenileme_tokeni_olustur
from app.modules.auth.auth_service import AuthService, erisim_tokenini_dogrula
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_service import KullaniciService

# Bu dosyanın TÜM testleri gerçek (ayrı) test Mongo'suna gider (bkz. conftest.py).
pytestmark = pytest.mark.usefixtures("temiz_veritabani")


def _servis() -> AuthService:
    return AuthService(get_database())


async def test_kayit_basarili_token_dondurur() -> None:
    erisim, yenileme = await _servis().kayit_ol("ayse@example.com", "sifre1234")

    assert erisim_tokenini_dogrula(erisim) is not None
    assert yenileme


async def test_ayni_eposta_ile_tekrar_kayit_reddedilir() -> None:
    servis = _servis()
    await servis.kayit_ol("ayse@example.com", "sifre1234")

    with pytest.raises(EpostaZatenKayitli):
        await servis.kayit_ol("ayse@example.com", "baskaSifre1")


async def test_dogru_sifreyle_giris_basarili() -> None:
    servis = _servis()
    await servis.kayit_ol("ayse@example.com", "sifre1234")

    erisim, yenileme = await servis.giris_yap("ayse@example.com", "sifre1234")

    assert erisim
    assert yenileme


async def test_yanlis_sifreyle_giris_genel_hata_verir() -> None:
    servis = _servis()
    await servis.kayit_ol("ayse@example.com", "sifre1234")

    with pytest.raises(GecersizKimlikBilgisi):
        await servis.giris_yap("ayse@example.com", "yanlisSifre")


async def test_kayitli_olmayan_epostayla_giris_ayni_genel_hatayi_verir() -> None:
    with pytest.raises(GecersizKimlikBilgisi):
        await _servis().giris_yap("olmayan@example.com", "herhangibirsey")


async def test_token_yenileme_yeni_erisim_tokeni_uretir() -> None:
    servis = _servis()
    _, yenileme = await servis.kayit_ol("ayse@example.com", "sifre1234")

    yeni_erisim = await servis.token_yenile(yenileme)

    assert erisim_tokenini_dogrula(yeni_erisim) is not None


async def test_suresi_gecmis_yenileme_tokeni_reddedilir() -> None:
    suresi_gecmis_token, _ = yenileme_tokeni_olustur(
        "herhangibirkullanici", gecerlilik=timedelta(seconds=-1)
    )

    with pytest.raises(TokenSuresiDolmus):
        await _servis().token_yenile(suresi_gecmis_token)


async def test_oturum_kapatilan_yenileme_tokeni_tekrar_kullanilamaz() -> None:
    servis = _servis()
    _, yenileme = await servis.kayit_ol("ayse@example.com", "sifre1234")

    await servis.oturum_kapat(yenileme)

    with pytest.raises(GecersizToken):
        await servis.token_yenile(yenileme)


async def test_hesap_silindikten_sonra_kullanici_bulunamaz() -> None:
    servis = _servis()
    erisim, _ = await servis.kayit_ol("ayse@example.com", "sifre1234")
    kullanici_id = erisim_tokenini_dogrula(erisim)

    await servis.hesabi_sil(kullanici_id)

    with pytest.raises(KullaniciBulunamadi):
        await servis.kullaniciyi_getir(kullanici_id)


async def test_olmayan_kullaniciyi_silmek_hata_verir() -> None:
    from bson import ObjectId

    with pytest.raises(KullaniciBulunamadi):
        await _servis().hesabi_sil(str(ObjectId()))


async def test_hesabi_sil_diger_modullerin_verisini_de_temizler() -> None:
    """K-085 Madde 1 — hesap silinince `harcama`/`kullanici` modüllerinin
    sahip olduğu HİÇBİR koleksiyonda bu kullanıcıya ait belge kalmamalı."""
    servis = _servis()
    erisim, _ = await servis.kayit_ol("mehmet@example.com", "sifre1234")
    kullanici_id = erisim_tokenini_dogrula(erisim)

    harcama_servisi = HarcamaService(get_database())
    kullanici_servisi = KullaniciService(get_database())
    await kullanici_servisi.katman1_kaydet(kullanici_id, "tasarruf", 3_200_000, 15, False)
    await harcama_servisi.harcama_ekle(kullanici_id, 5_000, "market", "2026-09-19T10:00:00", "2026-09-19", "kart")
    await harcama_servisi.kategori_limiti_yaz(kullanici_id, "market", 300_000, 1)
    await harcama_servisi.gun_durumu_isaretle(kullanici_id, "2026-09-19", True)
    await harcama_servisi.limit_gecmisi_yaz(kullanici_id, "2026-09-19", 15_000)
    await harcama_servisi.urun_kategori_ogren(kullanici_id, "ekmek", "market")

    await servis.hesabi_sil(kullanici_id)

    veritabani = get_database()
    for koleksiyon, sorgu in (
        ("kullanicilar", {"_id": _object_id_cevir_test_yardimcisi(kullanici_id)}),
        ("yenileme_tokenlari", {"kullanici_id": kullanici_id}),
        ("kullanici_profilleri", {"kullanici_id": kullanici_id}),
        ("harcamalar", {"kullanici_id": kullanici_id}),
        ("kategori_limitleri", {"kullanici_id": kullanici_id}),
        ("gun_durumlari", {"kullanici_id": kullanici_id}),
        ("limit_gecmisleri", {"kullanici_id": kullanici_id}),
        ("urun_kategori_ogrenmeleri", {"kullanici_id": kullanici_id}),
    ):
        assert await veritabani[koleksiyon].count_documents(sorgu) == 0, koleksiyon


def _object_id_cevir_test_yardimcisi(kullanici_id: str) -> object:
    from bson import ObjectId

    return ObjectId(kullanici_id)
