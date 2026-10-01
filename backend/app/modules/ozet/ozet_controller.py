"""
Özet modülünün HTTP katmanı: günlük pano, dönemsel özet, kategori detayı,
seri. İş mantığı burada YOK — hepsi `OzetService`e devredilir (harcama_
controller.py ile aynı desen, K-068/3).

`OzetService`, `harcama` ve `kullanici` modüllerinin servis arayüzlerini
Depends zinciriyle alır; bu modüllerin iç dosyalarına dokunulmadı (Madde 2).

Yetkilendirme `auth` modülünün `gecerli_kullanici_id` bağımlılığıyla
yapılır: her uç nokta yalnız token'daki kullanıcının KENDİ verisine erişir.
"""
from __future__ import annotations

from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Query

from app.core.database import get_database
from app.core.errors import GecersizTarihAraligi
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_service import KullaniciService
from app.modules.ozet.ozet_dto import (
    GunIzgaraHucresiYaniti,
    GunlukPanoYaniti,
    GunSeriBilgisiYaniti,
    KategoriDetayYaniti,
    KategoriPayiYaniti,
    KategoriSeyriGunuYaniti,
    KucukHarcamaOzetiYaniti,
    OzetYaniti,
    PanoKategoriDurumuYaniti,
    SeriYaniti,
)
from app.modules.ozet.ozet_service import (
    VARSAYILAN_KUCUK_HARCAMA_ESIGI_KURUS,
    GunlukPano,
    KategoriDetayGorunumu,
    OzetGorunumu,
    OzetService,
    SeriGorunumu,
)

router = APIRouter(prefix="/ozet", tags=["ozet"])

_GUN_DESENI = r"^\d{4}-\d{2}-\d{2}$"


def _harcama_servisi() -> HarcamaService:
    return HarcamaService(get_database())


def _kullanici_servisi() -> KullaniciService:
    return KullaniciService(get_database())


def _servis(
    harcama_servisi: HarcamaService = Depends(_harcama_servisi),
    kullanici_servisi: KullaniciService = Depends(_kullanici_servisi),
) -> OzetService:
    return OzetService(harcama_servisi, kullanici_servisi)


def _araligi_dogrula(baslangic_gun: str, bitis_gun: str) -> None:
    if baslangic_gun > bitis_gun:
        raise GecersizTarihAraligi()


def _pano_yanitina_cevir(pano: GunlukPano) -> GunlukPanoYaniti:
    return GunlukPanoYaniti(
        gun=pano.gun,
        niyet=pano.niyet,
        limit_kurus=pano.limit_kurus,
        harcanan_kurus=pano.harcanan_kurus,
        kayit_adedi=pano.kayit_adedi,
        limit_durumu=pano.limit_durumu,
        kategoriler=[
            PanoKategoriDurumuYaniti(
                kategori=k.kategori, limit_kurus=k.limit_kurus, harcanan_kurus=k.harcanan_kurus, bugun_kurus=k.bugun_kurus
            )
            for k in pano.kategoriler
        ],
        ay_asimi=pano.ay_asimi,
        seri=GunSeriBilgisiYaniti(
            harcanan_kurus=pano.seri.harcanan_kurus,
            kayit_adedi=pano.seri.kayit_adedi,
            harcamasiz_isaretli=pano.seri.harcamasiz_isaretli,
            seriye_sayildi_mi=pano.seri.seriye_sayildi_mi,
        ),
        ilk_gun_mu=pano.ilk_gun_mu,
    )


def _ozet_yanitina_cevir(ozet: OzetGorunumu) -> OzetYaniti:
    return OzetYaniti(
        baslangic_gun=ozet.baslangic_gun,
        bitis_gun=ozet.bitis_gun,
        toplam_kurus=ozet.toplam_kurus,
        kategori_dagilimi=[
            KategoriPayiYaniti(kategori=p.kategori, toplam_kurus=p.toplam_kurus, yuzde=p.yuzde)
            for p in ozet.kategori_dagilimi
        ],
        en_cok_harcanan_kategoriler=ozet.en_cok_harcanan_kategoriler,
        kucuk_harcama=KucukHarcamaOzetiYaniti(
            esik_kurus=ozet.kucuk_harcama.esik_kurus,
            adet=ozet.kucuk_harcama.adet,
            toplam_kurus=ozet.kucuk_harcama.toplam_kurus,
        ),
    )


def _kategori_detay_yanitina_cevir(detay: KategoriDetayGorunumu) -> KategoriDetayYaniti:
    return KategoriDetayYaniti(
        kategori=detay.kategori,
        baslangic_gun=detay.baslangic_gun,
        bitis_gun=detay.bitis_gun,
        toplam_kurus=detay.toplam_kurus,
        gun_bazinda_seyir=[KategoriSeyriGunuYaniti(gun=g.gun, toplam_kurus=g.toplam_kurus) for g in detay.gun_bazinda_seyir],
    )


def _seri_yanitina_cevir(gorunum: SeriGorunumu) -> SeriYaniti:
    seri = gorunum.seri
    return SeriYaniti(
        mevcut_seri=seri.mevcut_seri,
        en_uzun_seri=seri.en_uzun_seri,
        en_uzun_seri_bitis_gunu=seri.en_uzun_seri_bitis_gunu,
        kapali=seri.kapali,
        kirildi_mi=seri.kirildi_mi,
        sonraki_durak=seri.sonraki_durak,
        onceki_durak=seri.onceki_durak,
        kalan_gun=seri.kalan_gun,
        aralik_yuzde=seri.aralik_yuzde,
        gecilen_milestoneler=seri.gecilen_milestoneler,
        izgara=[GunIzgaraHucresiYaniti(gun=h.gun, durum=h.durum) for h in gorunum.izgara],
    )


@router.get("/pano", response_model=GunlukPanoYaniti)
async def gunluk_pano(
    gun: str | None = Query(default=None, pattern=_GUN_DESENI),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: OzetService = Depends(_servis),
) -> GunlukPanoYaniti:
    """E-10 — seçilen günün (verilmezse bugünün) panosu: toplam, limit durumu, kategori kırılımı, seri."""
    secilen_gun = gun or datetime.now(timezone.utc).date().isoformat()
    pano = await servis.gunluk_pano_getir(kullanici_id, secilen_gun)
    return _pano_yanitina_cevir(pano)


@router.get("/donem", response_model=OzetYaniti)
async def donem_ozeti(
    baslangic_gun: str = Query(pattern=_GUN_DESENI),
    bitis_gun: str = Query(pattern=_GUN_DESENI),
    esik_kurus: int = Query(default=VARSAYILAN_KUCUK_HARCAMA_ESIGI_KURUS, ge=0),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: OzetService = Depends(_servis),
) -> OzetYaniti:
    """E-16 — haftalık/aylık özet: dönem toplamı, kategori dağılımı (₺+%), Latte Faktörü."""
    _araligi_dogrula(baslangic_gun, bitis_gun)
    ozet = await servis.ozet_getir(kullanici_id, baslangic_gun, bitis_gun, esik_kurus)
    return _ozet_yanitina_cevir(ozet)


@router.get("/kategori/{kategori}", response_model=KategoriDetayYaniti)
async def kategori_detayi(
    kategori: str,
    baslangic_gun: str = Query(pattern=_GUN_DESENI),
    bitis_gun: str = Query(pattern=_GUN_DESENI),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: OzetService = Depends(_servis),
) -> KategoriDetayYaniti:
    """E-15 — tek kategorinin zaman içindeki seyri; kayıt LİSTESİ için `GET /harcama/?kategori=` kullanılır."""
    _araligi_dogrula(baslangic_gun, bitis_gun)
    detay = await servis.kategori_detayi_getir(kullanici_id, kategori, baslangic_gun, bitis_gun)
    return _kategori_detay_yanitina_cevir(detay)


@router.get("/seri", response_model=SeriYaniti)
async def seri(
    bugun: str | None = Query(default=None, pattern=_GUN_DESENI),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: OzetService = Depends(_servis),
) -> SeriYaniti:
    """E-21 — mevcut seri, en uzun seri, son 30 günün ızgarası, milestone durumu.

    K-087 — "bugün" istemciden `bugun` sorgu parametresiyle gelir; sunucu saat
    dilimi varsayımı yapmaz (harcama modülündeki "gün istemciden gelir"
    kuralıyla aynı). İSTİSNA: parametre gönderilmezse geriye dönük uyumluluk
    için sunucu UTC gününe düşer (eski istemciler kırılmasın) — istemci bu
    parametreyi HER ZAMAN göndermeli, UTC düşüşü kalıcı bir davranış değildir.
    Biçim `_GUN_DESENI` ile doğrulanır; uymayan değer FastAPI/Pydantic
    tarafından otomatik 422 üretir (mevcut hata sözleşmesiyle aynı desen,
    bkz. `gunluk_pano`'daki `gun` parametresi).
    """
    secilen_bugun = date.fromisoformat(bugun) if bugun else None
    gorunum = await servis.seri_getir(kullanici_id, bugun=secilen_bugun)
    return _seri_yanitina_cevir(gorunum)
