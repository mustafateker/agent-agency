"""
Özet servisinin iş kurallarını doğrular.

Saf hesap fonksiyonları (`gun_seriye_sayilir_mi` → `en_buyuk_kalan_yuzdeler`)
Mongo'ya ihtiyaç DUYMAZ — deterministik girdiyle çalışırlar (kullanici
modülünün formül testleriyle aynı desen). `OzetService` üzerinden Mongo'ya
giden testler `conftest.temiz_veritabani` ile temizlenen ayrı test
veritabanına karşı çalışır; yerel MongoDB kurulu değilse bu testler
bağlantı hatasıyla düşer — bu BEKLENEN bir durumdur (bkz. görev notu).
"""
from __future__ import annotations

from datetime import date

import pytest

from app.core.database import get_database
from app.core.errors import GelirGerekli
from app.modules.harcama.harcama_model import HarcamaBelgesi, LimitGecmisiBelgesi
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_service import KullaniciService
from app.modules.ozet.ozet_service import (
    GunNitelik,
    OzetService,
    ay_son_gunu,
    efektif_limit_cozucu_olustur,
    en_buyuk_kalan_yuzdeler,
    en_uzun_seri_ratchet,
    esik_alti_toplam,
    gun_araligi_uret,
    gun_izgara_durumu,
    gun_seriye_sayilir_mi,
    gunluk_toplamlari_hesapla,
    izgara_uret,
    limit_durumu_hesapla,
    onceki_durak,
    seri_hesapla,
    seri_sinir_gunu_belirle,
    sonraki_durak,
)

# ---------------------------------------------------------------------------
# Saf hesap testleri — Mongo'suz
# ---------------------------------------------------------------------------


def _harcama(gun: str, tutar_kurus: int, kategori: str = "market") -> HarcamaBelgesi:
    return HarcamaBelgesi(
        kullanici_id="k1", tutar_kurus=tutar_kurus, kategori=kategori, zaman=f"{gun}T10:00:00", gun=gun, odeme="kart"
    )


def test_limit_durumu_limit_tanimsizsa_tanimsiz_doner() -> None:
    assert limit_durumu_hesapla(5_000, None) == "tanimsiz"


def test_limit_durumu_asim_ve_altinda() -> None:
    assert limit_durumu_hesapla(10_000, 10_000) == "altinda"  # tam limitte hâlâ altında
    assert limit_durumu_hesapla(10_001, 10_000) == "asimda"


def test_gun_izgara_durumu_kayitsiz_gun_bos() -> None:
    assert gun_izgara_durumu(0, 0, 10_000) == "bos"


def test_gun_izgara_durumu_asim_disinda_digeri_altinda() -> None:
    assert gun_izgara_durumu(15_000, 2, 10_000) == "disinda"
    assert gun_izgara_durumu(5_000, 2, 10_000) == "altinda"
    assert gun_izgara_durumu(15_000, 2, None) == "altinda"  # limit yoksa aşım hiç değerlendirilmez


def test_seriye_sayilir_kayitsiz_gun_hile_kapisini_gecemez() -> None:
    assert gun_seriye_sayilir_mi(0, 0, harcamasiz_isaretli=False, limit_kurus=10_000) is False


def test_seriye_sayilir_harcamasiz_isaretli_gun_sayilir() -> None:
    assert gun_seriye_sayilir_mi(0, 0, harcamasiz_isaretli=True, limit_kurus=10_000) is True


def test_seriye_sayilir_limit_asilirsa_sayilmaz() -> None:
    assert gun_seriye_sayilir_mi(15_000, 3, harcamasiz_isaretli=False, limit_kurus=10_000) is False


def test_seriye_sayilir_tam_limitte_sayilir() -> None:
    assert gun_seriye_sayilir_mi(10_000, 1, harcamasiz_isaretli=False, limit_kurus=10_000) is True


def test_milestone_sonraki_ve_onceki_durak_sinirlari() -> None:
    assert onceki_durak(0) == 0
    assert sonraki_durak(0) == 3
    assert onceki_durak(3) == 3  # tam milestone gününde "önceki" kendisi
    assert sonraki_durak(3) == 7
    assert onceki_durak(364) == 180
    assert sonraki_durak(364) == 365
    assert onceki_durak(365) == 365
    assert sonraki_durak(365) is None  # son milestone'ı geçince sonraki durak yok


def _nitelik(gun: str, harcanan: int, adet: int, harcamasiz: bool, limit: int) -> GunNitelik:
    return GunNitelik(gun=gun, harcanan_kurus=harcanan, kayit_adedi=adet, harcamasiz_isaretli=harcamasiz, efektif_limit_kurus=limit)


def test_seri_hesapla_limitsiz_kipte_kapali_doner() -> None:
    sonuc = seri_hesapla([_nitelik("2026-09-17", 0, 1, False, 10_000)], limitsiz_mi=True)
    assert sonuc.kapali is True
    assert sonuc.mevcut_seri == 0
    assert sonuc.en_uzun_seri == 0


def test_seri_hesapla_kayitsiz_gun_seriyi_kirar() -> None:
    nitelikler = [
        _nitelik("2026-09-15", 5_000, 1, False, 10_000),
        _nitelik("2026-09-16", 0, 0, False, 10_000),  # kayıtsız ve işaretsiz -> kırar
        _nitelik("2026-09-17", 5_000, 1, False, 10_000),
    ]
    sonuc = seri_hesapla(nitelikler, limitsiz_mi=False)
    assert sonuc.mevcut_seri == 1  # yalnız son gün
    assert sonuc.en_uzun_seri == 1
    assert sonuc.kirildi_mi is False  # mevcut > 0 olduğu için "kırıldı" değil


def test_seri_hesapla_harcamasiz_isaretli_gun_seriyi_korur() -> None:
    nitelikler = [
        _nitelik("2026-09-15", 5_000, 1, False, 10_000),
        _nitelik("2026-09-16", 0, 0, True, 10_000),  # hile kapısı (b): işaretli
        _nitelik("2026-09-17", 5_000, 1, False, 10_000),
    ]
    sonuc = seri_hesapla(nitelikler, limitsiz_mi=False)
    assert sonuc.mevcut_seri == 3
    assert sonuc.en_uzun_seri == 3


def test_seri_hesapla_gecmis_gun_kendi_yururlukteki_limitiyle_degerlendirilir() -> None:
    """K-064/1 — eski limit düşükken aşım sayılan bir gün, GÜNCEL limitle yeniden değerlendirilmez."""
    nitelikler = [
        # O gün yürürlükteki limit 5.000 kuruştu, 6.000 harcanmış -> aşım, seriyi kırar.
        _nitelik("2026-09-10", 6_000, 1, False, 5_000),
        # Limit sonradan 10.000'e çıktı; bu günden itibaren yeni limitle değerlendirilir.
        _nitelik("2026-09-11", 8_000, 1, False, 10_000),
        _nitelik("2026-09-12", 8_000, 1, False, 10_000),
    ]
    sonuc = seri_hesapla(nitelikler, limitsiz_mi=False)
    assert sonuc.mevcut_seri == 2  # yalnız 11-12, 10'u limit aşımıyla kırıldı
    assert sonuc.en_uzun_seri == 2


def test_seri_hesapla_kirildi_mi_ve_gecilen_milestoneler() -> None:
    nitelikler = [_nitelik(f"2026-09-{gun:02d}", 1_000, 1, False, 10_000) for gun in range(1, 8)]
    sonuc = seri_hesapla(nitelikler, limitsiz_mi=False)
    assert sonuc.mevcut_seri == 7
    assert sonuc.gecilen_milestoneler == [3, 7]
    assert sonuc.sonraki_durak == 14
    assert sonuc.onceki_durak == 7
    assert sonuc.kalan_gun == 7

    # Seri kırılınca "en uzun seri" saklanır, `kirildi_mi` suçlayıcı olmayan bayrak olur.
    nitelikler.append(_nitelik("2026-09-08", 0, 0, False, 10_000))
    kirilmis = seri_hesapla(nitelikler, limitsiz_mi=False)
    assert kirilmis.mevcut_seri == 0
    assert kirilmis.en_uzun_seri == 7
    assert kirilmis.kirildi_mi is True


def test_seri_hesapla_bos_liste_kapali_gibi_davranir() -> None:
    sonuc = seri_hesapla([], limitsiz_mi=False)
    assert sonuc.kapali is True
    assert sonuc.mevcut_seri == 0


# ---------------------------------------------------------------------------
# BE-5c (K-087) — "bugün" istemciden gelir, sunucu UTC türetmez — saf, Mongo'suz
# ---------------------------------------------------------------------------


def test_bugun_utc_ile_istemci_yerel_gunu_farkliysa_seri_istemci_gununu_esas_almali() -> None:
    """Sınır durumu: sunucu saati UTC 21:30 (TR'de 00:30 — takvim zaten 18'e geçti).

    İstemci 18'inde bir harcama kaydetti (`harcama` kuralı: gün alanı
    istemciden gelir). Eski davranış "bugün"ü sunucu UTC'sinden türetirdi
    (hâlâ 17) — bu durumda 18'deki kayıt aralığın DIŞINDA kalır ve seriye HİÇ
    girmezdi. Düzeltme (K-087): "bugün" istemciden `bugun_gun` olarak
    verilir; bu test aynı ham kayıt kümesiyle iki farklı `bugun_gun`
    değerinin (eski hatalı UTC günü / doğru istemci günü) seri sonucunu
    NASIL değiştirdiğini kanıtlar — `OzetService.seri_getir` bu tarafa (18)
    düşen değeri kullanacak şekilde düzeltildi.
    """
    limit_kurus = 10_000
    ilk_gun = "2026-09-17"
    harcama_18 = _harcama("2026-09-18", 4_000)

    def _nitelikleri_olustur(bugun_gun: str) -> list[GunNitelik]:
        gunler = gun_araligi_uret(ilk_gun, bugun_gun)
        kayitlar = [harcama_18] if bugun_gun >= "2026-09-18" else []
        gunluk_toplamlar = gunluk_toplamlari_hesapla(kayitlar)
        return [
            GunNitelik(
                gun=gun,
                harcanan_kurus=gunluk_toplamlar.get(gun, (0, 0))[0],
                kayit_adedi=gunluk_toplamlar.get(gun, (0, 0))[1],
                harcamasiz_isaretli=False,
                efektif_limit_kurus=limit_kurus,
            )
            for gun in gunler
        ]

    # Eski (hatalı) davranış: sunucu "bugün"ü UTC'den türetseydi hâlâ 17'ydi.
    hatali_utc_gunu_sonucu = seri_hesapla(_nitelikleri_olustur("2026-09-17"), limitsiz_mi=False)
    assert hatali_utc_gunu_sonucu.mevcut_seri == 0  # 18'deki kayıt aralığa hiç girmedi

    # Düzeltilmiş davranış: istemcinin gönderdiği yerel gün (18) esas alınır.
    dogru_istemci_gunu_sonucu = seri_hesapla(_nitelikleri_olustur("2026-09-18"), limitsiz_mi=False)
    assert dogru_istemci_gunu_sonucu.mevcut_seri == 1  # 18'deki kayıt seriye girdi


# ---------------------------------------------------------------------------
# BE-5b Madde 1 — "en uzun seri" ratchet (K-077) — saf, Mongo'suz
# ---------------------------------------------------------------------------


def test_en_uzun_seri_ratchet_aday_buyukse_gunceller() -> None:
    yeni, bitis, guncellenmeli_mi = en_uzun_seri_ratchet(7, "2026-08-01", 40, "2026-09-09")
    assert (yeni, bitis, guncellenmeli_mi) == (40, "2026-09-09", True)


def test_en_uzun_seri_ratchet_aday_kucukse_kayitli_deger_korunur() -> None:
    """Ratchet yalnız BÜYÜR — limitsiz kipe geçip mevcut seri sıfırlansa da rekor küçülmez."""
    yeni, bitis, guncellenmeli_mi = en_uzun_seri_ratchet(40, "2026-09-09", 0, None)
    assert (yeni, bitis, guncellenmeli_mi) == (40, "2026-09-09", False)


def test_en_uzun_seri_ratchet_esitse_guncellenmez() -> None:
    yeni, bitis, guncellenmeli_mi = en_uzun_seri_ratchet(7, "2026-08-01", 7, "2026-09-01")
    assert guncellenmeli_mi is False
    assert (yeni, bitis) == (7, "2026-08-01")


# ---------------------------------------------------------------------------
# BE-5b Madde 2 — seri sınır günü (kurulum vs. ilk kayıt) — saf, Mongo'suz
# ---------------------------------------------------------------------------


def test_seri_sinir_gunu_ilk_kayit_kurulumdan_onceyse_ilk_kayit_secilir() -> None:
    sinir = seri_sinir_gunu_belirle("2026-09-10", "2026-08-20", "2026-09-19")
    assert sinir == "2026-08-20"


def test_seri_sinir_gunu_kurulum_daha_erkense_kurulum_secilir() -> None:
    sinir = seri_sinir_gunu_belirle("2026-08-01", "2026-09-05", "2026-09-19")
    assert sinir == "2026-08-01"


def test_seri_sinir_gunu_kayit_yoksa_kurulum_kullanilir() -> None:
    sinir = seri_sinir_gunu_belirle("2026-08-01", None, "2026-09-19")
    assert sinir == "2026-08-01"


def test_seri_sinir_gunu_kurulum_yoksa_bugun_varsayilir() -> None:
    sinir = seri_sinir_gunu_belirle(None, None, "2026-09-19")
    assert sinir == "2026-09-19"


# ---------------------------------------------------------------------------
# BE-5b Madde 3 — toplu limit-geçmişi çözücüsü — saf, Mongo'suz
# ---------------------------------------------------------------------------


def _limit_satiri(yururluk_tarihi: str, kurus: int) -> LimitGecmisiBelgesi:
    return LimitGecmisiBelgesi(kullanici_id="k1", yururluk_tarihi=yururluk_tarihi, kurus=kurus)


def test_efektif_limit_cozucu_tarihceden_onceki_gunler_guncel_limiti_kullanir() -> None:
    tarihce = [_limit_satiri("2026-09-10", 5_000)]
    cozucu = efektif_limit_cozucu_olustur(tarihce, guncel_limit_kurus=10_000)
    assert cozucu("2026-09-05") == 10_000  # göçten önce -> "en iyi tahmin" güncel limit


def test_efektif_limit_cozucu_artan_gun_sirasiyla_dogru_deger_doner() -> None:
    tarihce = [_limit_satiri("2026-09-05", 3_000), _limit_satiri("2026-09-12", 8_000)]
    cozucu = efektif_limit_cozucu_olustur(tarihce, guncel_limit_kurus=10_000)
    assert cozucu("2026-09-01") == 10_000
    assert cozucu("2026-09-05") == 3_000
    assert cozucu("2026-09-08") == 3_000
    assert cozucu("2026-09-12") == 8_000
    assert cozucu("2026-09-19") == 8_000


def test_izgara_uret_son_30_gunu_alir_ve_durumlari_dogru_sinifllandirir() -> None:
    # Çift günler: 1.000 kuruş harcanmış, 500 limitin üstünde -> "disinda". Tek günler: kayıtsız -> "bos".
    nitelikler = [_nitelik(f"gun-{i}", 1_000 if i % 2 == 0 else 0, 1 if i % 2 == 0 else 0, False, 500) for i in range(40)]
    izgara = izgara_uret(nitelikler)
    assert len(izgara) == 30
    assert izgara[0].gun == "gun-10"  # kuyruktan son 30
    assert izgara[0].durum == "disinda"
    assert izgara[-1].gun == "gun-39"
    assert izgara[-1].durum == "bos"


def test_en_buyuk_kalan_yuzdeler_toplam_100e_tamamlanir() -> None:
    yuzdeler = en_buyuk_kalan_yuzdeler({"market": 1_000, "kahve": 1_000, "ulasim": 1_000})
    assert sum(yuzdeler.values()) == 100
    # Eşit üç pay: 33/33/33 taban + 1 kalan en büyük kesirliye (sözlük sırasına göre ilk eşite) gider.
    assert sorted(yuzdeler.values()) == [33, 33, 34]


def test_en_buyuk_kalan_yuzdeler_bos_veya_sifir_toplamda_hepsi_sifir() -> None:
    assert en_buyuk_kalan_yuzdeler({}) == {}
    assert en_buyuk_kalan_yuzdeler({"market": 0, "kahve": 0}) == {"market": 0, "kahve": 0}


def test_esik_alti_toplam_latte_faktoru() -> None:
    adet, toplam = esik_alti_toplam([1_000, 6_000, 4_999, 5_000], esik_kurus=5_000)
    assert adet == 2  # 1.000 ve 4.999 eşiğin altında (5.000 dahil değil)
    assert toplam == 5_999


def test_gunluk_toplamlari_hesapla_ayni_gunun_kayitlarini_toplar() -> None:
    kayitlar = [_harcama("2026-09-17", 1_000), _harcama("2026-09-17", 2_000), _harcama("2026-09-18", 500)]
    toplamlar = gunluk_toplamlari_hesapla(kayitlar)
    assert toplamlar["2026-09-17"] == (3_000, 2)
    assert toplamlar["2026-09-18"] == (500, 1)


def test_gun_araligi_uret_baslangic_ve_bitis_dahildir() -> None:
    gunler = gun_araligi_uret("2026-09-17", "2026-09-19")
    assert gunler == ["2026-09-17", "2026-09-18", "2026-09-19"]


def test_ay_son_gunu_artik_yil_subat() -> None:
    assert ay_son_gunu("2024-02") == "2024-02-29"
    assert ay_son_gunu("2026-09") == "2026-09-30"


# ---------------------------------------------------------------------------
# Mongo gerektiren entegrasyon testi (harcama + kullanici servisleri üzerinden)
# ---------------------------------------------------------------------------


def _ozet_servisi() -> OzetService:
    veritabani = get_database()
    return OzetService(HarcamaService(veritabani), KullaniciService(veritabani))


async def test_gunluk_pano_ve_seri_uctan_uca_akis(temiz_veritabani: None) -> None:
    kullanici_servisi = KullaniciService(get_database())
    harcama_servisi = HarcamaService(get_database())
    ozet_servisi = _ozet_servisi()
    kullanici_id = "kullanici-ozet-1"

    with pytest.raises(GelirGerekli):
        await kullanici_servisi.plani_kur(kullanici_id, bugun=date(2026, 9, 17))
    await kullanici_servisi.gunluk_limiti_ayarla(kullanici_id, 10_000)
    await kullanici_servisi.tercihleri_guncelle(kullanici_id, {"kurulum_gunu": "2026-09-15"})

    await harcama_servisi.harcama_ekle(kullanici_id, 4_000, "market", "2026-09-17T10:00:00", "2026-09-17", "kart")
    await harcama_servisi.gun_durumu_isaretle(kullanici_id, "2026-09-16", True)
    # 15'inde hiç kayıt/işaret yok -> seri o günden başlamaz.

    pano = await ozet_servisi.gunluk_pano_getir(kullanici_id, "2026-09-17")
    assert pano.harcanan_kurus == 4_000
    assert pano.limit_durumu == "altinda"
    assert pano.seri.seriye_sayildi_mi is True

    gorunum = await ozet_servisi.seri_getir(kullanici_id, bugun=date(2026, 9, 17))
    assert gorunum.seri.kapali is False
    assert gorunum.seri.mevcut_seri == 2  # 16 (işaretli) + 17 (kayıtlı); 15 kırık başlangıç
