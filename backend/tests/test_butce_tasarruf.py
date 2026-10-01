from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.core.database import get_database
from app.modules.butce.butce_dto import ButceIstegi, RutinIstegi
from app.modules.butce.butce_service import ButceService, gunluk_pay
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.tasarruf.tasarruf_dto import BirikimIstegi
from app.modules.tasarruf.tasarruf_service import TasarrufService


def test_takvim_ayi_payinda_kurus_farki_son_gune_deterministik_gider() -> None:
    assert gunluk_pay(100_00, "2026-02-01") == 357
    assert gunluk_pay(100_00, "2026-02-28") == 361
    assert 27 * 357 + 361 == 100_00


async def test_butce_surumleri_gecmis_gunu_degistirmez(temiz_veritabani: None) -> None:
    servis = ButceService(get_database())
    await servis.yaz("u1", "2026-09-01", ButceIstegi(gelir_kurus=300_000))
    await servis.yaz("u1", "2026-09-15", ButceIstegi(gelir_kurus=600_000))

    eski = await servis.getir("u1", "2026-09-15", "2026-09-14")
    yeni = await servis.getir("u1", "2026-09-15", "2026-09-15")
    assert eski["butce"]["gunluk_limit_kurus"] == 10_000
    assert yeni["butce"]["gunluk_limit_kurus"] == 20_000


async def test_manuel_limit_korunur_ve_kategori_toplami_asamaz(temiz_veritabani: None) -> None:
    servis = ButceService(get_database())
    await servis.yaz("u1", "2026-09-01", ButceIstegi(
        gelir_kurus=300_000, limit_modu="manuel", manuel_limit_kurus=15_000,
        kategori_limitleri={"market": 9_000},
    ))
    sonuc = await servis.yaz("u1", "2026-09-02", ButceIstegi(
        gelir_kurus=900_000, limit_modu="manuel", manuel_limit_kurus=15_000,
        kategori_limitleri={"market": 9_000},
    ))
    assert sonuc["butce"]["gunluk_limit_kurus"] == 15_000
    with pytest.raises(HTTPException) as hata:
        await servis.yaz("u1", "2026-09-03", ButceIstegi(
            gelir_kurus=900_000, limit_modu="manuel", manuel_limit_kurus=15_000,
            kategori_limitleri={"market": 10_000, "kafe": 6_000},
        ))
    assert hata.value.status_code == 422


async def test_rutin_vazgecme_ayni_gun_guncellenir_ve_satin_alimla_sinirlanir(temiz_veritabani: None) -> None:
    db = get_database(); butce = ButceService(db); harcama = HarcamaService(db)
    await butce.rutin_yaz("u1", "2026-09-01", "kahve", RutinIstegi(
        ad="Kahve", kategori="kafe", gunluk_adet=2, birim_fiyat_kurus=5_000,
    ))
    await harcama.harcama_ekle("u1", 5_000, "kafe", "2026-09-10T09:00:00", "2026-09-10", "kart", rutin_id="kahve", adet=1)
    kayit = await butce.vazgecme_yaz("u1", "2026-09-10", "kahve", "2026-09-10", 1)
    assert kayit["tasarruf_kurus"] == 5_000
    tekrar = await butce.vazgecme_yaz("u1", "2026-09-10", "kahve", "2026-09-10", 1)
    assert tekrar == kayit
    with pytest.raises(HTTPException):
        await butce.vazgecme_yaz("u1", "2026-09-10", "kahve", "2026-09-10", 2)


async def test_rutinler_gecmis_gunun_vazgecme_durumunu_geri_okur(temiz_veritabani: None) -> None:
    butce = ButceService(get_database())
    await butce.rutin_yaz("u1", "2026-09-01", "kahve", RutinIstegi(
        ad="Kahve", kategori="kafe", gunluk_adet=1, birim_fiyat_kurus=5_000,
    ))
    await butce.vazgecme_yaz("u1", "2026-09-10", "kahve", "2026-09-10", 1)

    ayni_gun = {r["id"]: r for r in await butce.rutinler("u1", "2026-09-10", "2026-09-10")}
    assert ayni_gun["kahve"]["vazgecilen_adet"] == 1
    # Mevcut alanlar korunmuş olmalı (geriye uyumluluk).
    assert ayni_gun["kahve"]["ad"] == "Kahve"
    assert ayni_gun["kahve"]["aktif"] is True

    farkli_gun = {r["id"]: r for r in await butce.rutinler("u1", "2026-09-11", "2026-09-11")}
    assert farkli_gun["kahve"]["vazgecilen_adet"] == 0


async def test_ayni_gun_vazgecme_sonra_satin_alma_tasarrufu_sisirmez(temiz_veritabani: None) -> None:
    db = get_database(); butce = ButceService(db); harcama = HarcamaService(db)
    await butce.rutin_yaz("u1", "2026-09-01", "kahve", RutinIstegi(
        ad="Kahve", kategori="kafe", gunluk_adet=1, birim_fiyat_kurus=5_000,
    ))
    await butce.vazgecme_yaz("u1", "2026-09-10", "kahve", "2026-09-10", 1)
    # Kullanıcı sonradan fikrini değiştirip aynı gün rutini fiilen satın alıyor.
    await harcama.harcama_ekle("u1", 5_000, "kafe", "2026-09-10T09:00:00", "2026-09-10", "kart", rutin_id="kahve", adet=1)

    liste = {r["id"]: r for r in await butce.rutinler("u1", "2026-09-10", "2026-09-10")}
    assert liste["kahve"]["vazgecilen_adet"] == 0

    vazgecmeler = await butce.vazgecmeler("u1", "2026-09-10", "2026-09-10")
    assert vazgecmeler[0]["adet"] == 0
    assert vazgecmeler[0]["tasarruf_kurus"] == 0


async def test_ayni_gun_kismi_satin_alma_vazgecmeyi_kismen_gecersiz_kilar(temiz_veritabani: None) -> None:
    db = get_database(); butce = ButceService(db); harcama = HarcamaService(db)
    await butce.rutin_yaz("u1", "2026-09-01", "sigara", RutinIstegi(
        ad="Sigara", kategori="aliskanliklar", gunluk_adet=2, birim_fiyat_kurus=3_000,
    ))
    await butce.vazgecme_yaz("u1", "2026-09-10", "sigara", "2026-09-10", 2)
    await harcama.harcama_ekle("u1", 3_000, "aliskanliklar", "2026-09-10T09:00:00", "2026-09-10", "kart", rutin_id="sigara", adet=1)

    liste = {r["id"]: r for r in await butce.rutinler("u1", "2026-09-10", "2026-09-10")}
    assert liste["sigara"]["vazgecilen_adet"] == 1


async def test_tasarruf_tamamlanan_gunleri_sayar_gelecegi_saymaz(temiz_veritabani: None) -> None:
    db = get_database(); butce = ButceService(db); harcama = HarcamaService(db); tasarruf = TasarrufService(db)
    await butce.yaz("u1", "2026-09-01", ButceIstegi(gelir_kurus=300_000))
    await harcama.harcama_ekle("u1", 4_000, "market", "2026-09-01T09:00:00", "2026-09-01", "kart")
    await harcama.harcama_ekle("u1", 5_000, "market", "2026-09-10T09:00:00", "2026-09-10", "kart")
    sonuc = await tasarruf.ay_getir("u1", "2026-09", "2026-09-10")
    assert sonuc["harcanabilir_kurus"] == 300_000
    assert sonuc["harcanan_kurus"] == 9_000
    assert sonuc["tamamlanan_gun_sayisi"] == 9
    assert sonuc["hesaplanan_tasarruf_kurus"] == 86_000


async def test_gercek_birikim_ayri_defterdir_ve_negatife_inmez(temiz_veritabani: None) -> None:
    servis = TasarrufService(get_database())
    await servis.birikim_yaz("u1", "ekleme", "2026-09-10", BirikimIstegi(gun="2026-09-05", tutar_kurus=20_000))
    await servis.birikim_yaz("u1", "cekme", "2026-09-10", BirikimIstegi(gun="2026-09-06", tutar_kurus=-7_000))
    assert (await servis.birikimler("u1"))["toplam_kurus"] == 13_000
    with pytest.raises(HTTPException):
        await servis.birikim_yaz("u1", "fazla", "2026-09-10", BirikimIstegi(gun="2026-09-07", tutar_kurus=-14_000))
