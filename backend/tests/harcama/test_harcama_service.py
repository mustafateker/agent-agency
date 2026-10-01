"""
Harcama servisinin iş kurallarını doğrular.

DTO doğrulama testleri (para integer sınırları, taksit alan tutarlılığı)
ve `_turkce_normalize` saf fonksiyon olduğu için Mongo'ya İHTİYAÇ DUYMAZ.
`HarcamaService` üzerinden Mongo'ya giden testler `temiz_veritabani`
fixture'ını açıkça ister (conftest.py — autouse DEĞİL, bkz. Madde 0(a));
yerel MongoDB kurulu değilse bu testler bağlantı hatasıyla düşer — BEKLENEN.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.database import get_database
from app.core.errors import (
    HarcamaBulunamadi,
    TaksitliKayitTekBasinaSilinemez,
    TaksitliKayitTutariDegistirilemez,
)
from app.modules.harcama.harcama_dto import HarcamaEkleIstegi
from app.modules.harcama.harcama_model import HarcamaBelgesi
from app.modules.harcama.harcama_service import HarcamaService, _turkce_normalize


def _servis() -> HarcamaService:
    return HarcamaService(get_database())


async def _harcama_ekle(servis: HarcamaService, kullanici_id: str, **gecersiz_kilmalar: object) -> HarcamaBelgesi:
    girdi = {
        "tutar_kurus": 5_000,
        "kategori": "market",
        "zaman": "2026-09-19T10:00:00",
        "gun": "2026-09-19",
        "odeme": "kart",
    }
    girdi.update(gecersiz_kilmalar)
    return await servis.harcama_ekle(kullanici_id, **girdi)


# ---------------------------------------------------------------------------
# Saf testler — Mongo'suz (DTO doğrulama + normalize fonksiyonu)
# ---------------------------------------------------------------------------


def test_turkce_normalize_turkce_karakterleri_sadelestirir() -> None:
    assert _turkce_normalize("Çığlıklı Öğütülmüş Şeker İSTANBUL") == "ciglikli ogutulmus seker istanbul"
    assert _turkce_normalize("Sütlü Kahve") == "sutlu kahve"
    assert _turkce_normalize("   ") == ""


def test_harcama_ekle_istegi_tutar_kurus_pozitif_tamsayi_olmali() -> None:
    with pytest.raises(ValidationError):
        HarcamaEkleIstegi(tutar_kurus=0, kategori="market", zaman="z", gun="2026-09-19", odeme="kart")
    with pytest.raises(ValidationError):
        HarcamaEkleIstegi(tutar_kurus=-500, kategori="market", zaman="z", gun="2026-09-19", odeme="kart")


def test_harcama_ekle_istegi_taksit_alanlari_birlikte_gelmeli() -> None:
    with pytest.raises(ValidationError):
        HarcamaEkleIstegi(
            tutar_kurus=1_000, kategori="market", zaman="z", gun="2026-09-19", odeme="kart", taksit_id="t1"
        )


def test_harcama_ekle_istegi_taksit_no_toplamdan_buyuk_olamaz() -> None:
    with pytest.raises(ValidationError):
        HarcamaEkleIstegi(
            tutar_kurus=1_000,
            kategori="market",
            zaman="z",
            gun="2026-09-19",
            odeme="kart",
            taksit_id="t1",
            taksit_no=5,
            taksit_toplam=3,
        )


def test_harcama_ekle_istegi_gun_deseni_dogrulanir() -> None:
    with pytest.raises(ValidationError):
        HarcamaEkleIstegi(tutar_kurus=1_000, kategori="market", zaman="z", gun="19-09-2026", odeme="kart")


# ---------------------------------------------------------------------------
# Mongo'ya karşı servis testleri
# ---------------------------------------------------------------------------


async def test_harcama_ekle_tutar_kurus_integer_olarak_saklanir(temiz_veritabani: None) -> None:
    servis = _servis()
    belge = await _harcama_ekle(servis, "kullanici-1", tutar_kurus=123_45)

    assert isinstance(belge.tutar_kurus, int)
    assert belge.tutar_kurus == 12_345


async def test_taksitli_kayitta_tutar_guncellenemez(temiz_veritabani: None) -> None:
    servis = _servis()
    belge = await _harcama_ekle(
        servis, "kullanici-1", tutar_kurus=100_000, taksit_id="t1", taksit_no=1, taksit_toplam=3
    )

    with pytest.raises(TaksitliKayitTutariDegistirilemez):
        await servis.harcama_guncelle("kullanici-1", str(belge.id), {"tutar_kurus": 999})


async def test_taksitli_olmayan_kayitta_tutar_guncellenebilir(temiz_veritabani: None) -> None:
    servis = _servis()
    belge = await _harcama_ekle(servis, "kullanici-1", tutar_kurus=100_000)

    guncellenmis = await servis.harcama_guncelle("kullanici-1", str(belge.id), {"tutar_kurus": 150_000})

    assert guncellenmis.tutar_kurus == 150_000


async def test_tek_taksit_tek_basina_silinemez(temiz_veritabani: None) -> None:
    servis = _servis()
    belge = await _harcama_ekle(
        servis, "kullanici-1", tutar_kurus=50_000, taksit_id="t1", taksit_no=1, taksit_toplam=3
    )

    with pytest.raises(TaksitliKayitTekBasinaSilinemez):
        await servis.harcama_sil("kullanici-1", str(belge.id))


async def test_taksit_serisi_sil_tum_satirlari_kaldirir(temiz_veritabani: None) -> None:
    servis = _servis()
    for i in range(1, 4):
        await _harcama_ekle(
            servis, "kullanici-1", tutar_kurus=10_000, taksit_id="t1", taksit_no=i, taksit_toplam=3
        )
    await _harcama_ekle(servis, "kullanici-1", tutar_kurus=20_000)  # taksitsiz, dokunulmamalı

    silinen = await servis.taksit_serisi_sil("kullanici-1", "t1")
    kalanlar, toplam = await servis.harcamalari_listele("kullanici-1")

    assert silinen == 3
    assert toplam == 1


async def test_taksit_serisi_sil_olmayan_seride_hata_verir(temiz_veritabani: None) -> None:
    servis = _servis()
    with pytest.raises(HarcamaBulunamadi):
        await servis.taksit_serisi_sil("kullanici-1", "yok-boyle-bir-seri")


async def test_baska_kullanicinin_kaydina_erisilemez(temiz_veritabani: None) -> None:
    servis = _servis()
    belge = await _harcama_ekle(servis, "kullanici-a", tutar_kurus=10_000)

    with pytest.raises(HarcamaBulunamadi):
        await servis.harcama_getir("kullanici-b", str(belge.id))


async def test_gecersiz_id_bicimi_bulunamadi_sayilir(temiz_veritabani: None) -> None:
    servis = _servis()
    with pytest.raises(HarcamaBulunamadi):
        await servis.harcama_getir("kullanici-1", "gecerli-olmayan-id")


async def test_gun_suzgeci_yalniz_o_gunu_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1", gun="2026-09-18", zaman="2026-09-18T10:00:00")
    await _harcama_ekle(servis, "kullanici-1", gun="2026-09-19", zaman="2026-09-19T10:00:00")

    kayitlar, toplam = await servis.harcamalari_listele("kullanici-1", gun="2026-09-19")

    assert toplam == 1
    assert kayitlar[0].gun == "2026-09-19"


async def test_tarih_araligi_suzgeci(temiz_veritabani: None) -> None:
    servis = _servis()
    for gun in ("2026-09-10", "2026-09-15", "2026-09-20"):
        await _harcama_ekle(servis, "kullanici-1", gun=gun, zaman=f"{gun}T10:00:00")

    kayitlar, toplam = await servis.harcamalari_listele(
        "kullanici-1", baslangic_gun="2026-09-12", bitis_gun="2026-09-18"
    )

    assert toplam == 1
    assert kayitlar[0].gun == "2026-09-15"


async def test_kategori_suzgeci(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1", kategori="market")
    await _harcama_ekle(servis, "kullanici-1", kategori="kafe")

    kayitlar, toplam = await servis.harcamalari_listele("kullanici-1", kategori="kafe")

    assert toplam == 1
    assert kayitlar[0].kategori == "kafe"


async def test_sayfalama_toplam_kayit_ve_sayfa_boyutunu_dogru_uygular(temiz_veritabani: None) -> None:
    servis = _servis()
    for i in range(5):
        await _harcama_ekle(servis, "kullanici-1", gun="2026-09-19", zaman=f"2026-09-19T{10 + i}:00:00")

    ilk_sayfa, toplam = await servis.harcamalari_listele("kullanici-1", sayfa=1, sayfa_boyutu=2)
    ikinci_sayfa, _ = await servis.harcamalari_listele("kullanici-1", sayfa=2, sayfa_boyutu=2)

    assert toplam == 5
    assert len(ilk_sayfa) == 2
    assert len(ikinci_sayfa) == 2


async def test_limit_gecmisi_efektif_limit_dogru_gunu_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.limit_gecmisi_yaz("kullanici-1", "2026-09-01", 20_000)
    await servis.limit_gecmisi_yaz("kullanici-1", "2026-09-15", 30_000)

    # 15'inden önce eski limit yürürlükte, 15'i ve sonrası yeni limit.
    assert await servis.limit_gecmisi_efektif_limit("kullanici-1", "2026-09-10", 99_999) == 20_000
    assert await servis.limit_gecmisi_efektif_limit("kullanici-1", "2026-09-15", 99_999) == 30_000
    assert await servis.limit_gecmisi_efektif_limit("kullanici-1", "2026-09-30", 99_999) == 30_000


async def test_limit_gecmisi_kayit_yoksa_guncel_limit_en_iyi_tahmindir(temiz_veritabani: None) -> None:
    servis = _servis()
    assert await servis.limit_gecmisi_efektif_limit("kullanici-1", "2020-01-01", 25_000) == 25_000


async def test_limit_gecmisi_ayni_gunde_ikinci_yazma_ustune_yazar(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.limit_gecmisi_yaz("kullanici-1", "2026-09-19", 20_000)
    await servis.limit_gecmisi_yaz("kullanici-1", "2026-09-19", 35_000)

    assert await servis.limit_gecmisi_efektif_limit("kullanici-1", "2026-09-19", 0) == 35_000


async def test_gun_durumu_isaretle_ve_getir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.gun_durumu_isaretle("kullanici-1", "2026-09-19", True)

    durum = await servis.gun_durumu_getir("kullanici-1", "2026-09-19")
    isaretlenmemis_gun = await servis.gun_durumu_getir("kullanici-1", "2026-09-01")

    assert durum.harcamasiz is True
    assert isaretlenmemis_gun.harcamasiz is False  # hiç işaretlenmemiş gün varsayılan False döner


async def test_kategori_limiti_yaz_ve_getir_siraya_gore_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.kategori_limiti_yaz("kullanici-1", "kafe", 120_000, 2)
    await servis.kategori_limiti_yaz("kullanici-1", "market", 300_000, 1)

    limitler = await servis.kategori_limitlerini_getir("kullanici-1")

    assert [limit.kategori for limit in limitler] == ["market", "kafe"]


async def test_urun_kategori_otomatik_ogrenilir_harcama_eklenince(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1", urun_adi="Sütlü Kahve", kategori="kafe")

    ogrenmeler = await servis.urun_kategori_ogrenmelerini_getir("kullanici-1")

    assert len(ogrenmeler) == 1
    assert ogrenmeler[0].urun_anahtari == "sutlu kahve"
    assert ogrenmeler[0].kategori == "kafe"


async def test_urun_kategori_ogren_bos_urun_adinda_kayit_olusturmaz(temiz_veritabani: None) -> None:
    servis = _servis()
    sonuc = await servis.urun_kategori_ogren("kullanici-1", "   ", "kafe")

    assert sonuc is None
    assert await servis.urun_kategori_ogrenmelerini_getir("kullanici-1") == []


async def test_kategori_limiti_sil_kaldirir(temiz_veritabani: None) -> None:
    servis = _servis()
    await servis.kategori_limiti_yaz("kullanici-1", "market", 300_000, 1)

    await servis.kategori_limiti_sil("kullanici-1", "market")

    assert await servis.kategori_limitlerini_getir("kullanici-1") == []


async def test_kategori_limiti_sil_olmayan_kategoride_hata_vermez(temiz_veritabani: None) -> None:
    # DELETE idempotenttir — hiç var olmayan bir kategori için de sessizce başarılı.
    await _servis().kategori_limiti_sil("kullanici-1", "hic-olmayan")


async def test_en_eski_kayit_gunu_ilk_kaydin_gununu_doner(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1", gun="2026-09-15")
    await _harcama_ekle(servis, "kullanici-1", gun="2026-09-01")
    await _harcama_ekle(servis, "kullanici-1", gun="2026-09-20")

    assert await servis.en_eski_kayit_gunu("kullanici-1") == "2026-09-01"


async def test_en_eski_kayit_gunu_kayit_yoksa_none_doner(temiz_veritabani: None) -> None:
    assert await _servis().en_eski_kayit_gunu("kullanici-1") is None


async def test_kullanici_verisini_sil_tum_koleksiyonlari_temizler(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1")
    await servis.kategori_limiti_yaz("kullanici-1", "market", 300_000, 1)
    await servis.gun_durumu_isaretle("kullanici-1", "2026-09-19", True)
    await servis.limit_gecmisi_yaz("kullanici-1", "2026-09-19", 15_000)
    await servis.urun_kategori_ogren("kullanici-1", "kahve", "kafe")

    await servis.kullanici_verisini_sil("kullanici-1")

    kayitlar, toplam = await servis.harcamalari_listele("kullanici-1")
    assert kayitlar == []
    assert toplam == 0
    assert await servis.kategori_limitlerini_getir("kullanici-1") == []
    assert (await servis.gun_durumu_getir("kullanici-1", "2026-09-19")).harcamasiz is False
    assert await servis.urun_kategori_ogrenmelerini_getir("kullanici-1") == []


async def test_kullanici_verisini_sil_baska_kullaniciyi_etkilemez(temiz_veritabani: None) -> None:
    servis = _servis()
    await _harcama_ekle(servis, "kullanici-1")
    await _harcama_ekle(servis, "kullanici-2")

    await servis.kullanici_verisini_sil("kullanici-1")

    kayitlar, toplam = await servis.harcamalari_listele("kullanici-2")
    assert toplam == 1
    assert kayitlar[0].kullanici_id == "kullanici-2"
