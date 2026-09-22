"""
Harcama modülünün HTTP katmanı: harcama CRUD'u, taksit serisi silme, gün
durumu işaretleme, kategori limitleri, limit geçmişi yazma, ürün-kategori
öğrenmesi. İş mantığı burada YOK — hepsi `HarcamaService`e devredilir
(kullanici_controller.py ile aynı desen, K-068/3).

Yetkilendirme `auth` modülünün mevcut `gecerli_kullanici_id` bağımlılığıyla
yapılır: her uç nokta yalnız token'daki kullanıcının KENDİ verisine erişir
(Madde 2) — IDOR yüzeyi yok.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.core.database import get_database
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.harcama.harcama_dto import (
    EnEskiKayitGunuYaniti,
    GunDurumuIsaretleIstegi,
    GunDurumuYaniti,
    HarcamaEkleIstegi,
    HarcamaGuncellemeIstegi,
    HarcamaListesiYaniti,
    HarcamaYaniti,
    KategoriLimitiYaniti,
    KategoriLimitiYaziIstegi,
    LimitGecmisiYaniti,
    LimitGecmisiYaziIstegi,
    UrunKategoriOgrenmeYaniti,
    UrunKategoriOgrenmeYaziIstegi,
)
from app.modules.harcama.harcama_model import (
    GunDurumuBelgesi,
    HarcamaBelgesi,
    KategoriLimitiBelgesi,
    LimitGecmisiBelgesi,
    UrunKategoriOgrenmeBelgesi,
)
from app.modules.harcama.harcama_service import VARSAYILAN_SAYFA_BOYUTU, HarcamaService

router = APIRouter(prefix="/harcama", tags=["harcama"])


def _servis() -> HarcamaService:
    return HarcamaService(get_database())


def _harcama_yanitina_cevir(belge: HarcamaBelgesi) -> HarcamaYaniti:
    return HarcamaYaniti(
        id=str(belge.id),
        tutar_kurus=belge.tutar_kurus,
        kategori=belge.kategori,
        urun_adi=belge.urun_adi,
        zaman=belge.zaman,
        gun=belge.gun,
        odeme=belge.odeme,
        not_metni=belge.not_metni,
        taksit_id=belge.taksit_id,
        taksit_no=belge.taksit_no,
        taksit_toplam=belge.taksit_toplam,
    )


def _gun_durumu_yanitina_cevir(belge: GunDurumuBelgesi) -> GunDurumuYaniti:
    return GunDurumuYaniti(gun=belge.gun, harcamasiz=belge.harcamasiz)


def _kategori_limiti_yanitina_cevir(belge: KategoriLimitiBelgesi) -> KategoriLimitiYaniti:
    return KategoriLimitiYaniti(kategori=belge.kategori, limit_kurus=belge.limit_kurus, sira=belge.sira)


def _limit_gecmisi_yanitina_cevir(belge: LimitGecmisiBelgesi) -> LimitGecmisiYaniti:
    return LimitGecmisiYaniti(yururluk_tarihi=belge.yururluk_tarihi, kurus=belge.kurus)


def _urun_kategori_yanitina_cevir(belge: UrunKategoriOgrenmeBelgesi) -> UrunKategoriOgrenmeYaniti:
    return UrunKategoriOgrenmeYaniti(urun_anahtari=belge.urun_anahtari, kategori=belge.kategori)


@router.post("/", response_model=HarcamaYaniti, status_code=status.HTTP_201_CREATED)
async def harcama_ekle(
    istek: HarcamaEkleIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> HarcamaYaniti:
    """Tek bir harcama satırı ekler (taksit serisi ise istemci bunu taksit sayısı kadar çağırır)."""
    belge = await servis.harcama_ekle(
        kullanici_id,
        istek.tutar_kurus,
        istek.kategori,
        istek.zaman,
        istek.gun,
        istek.odeme,
        istek.urun_adi,
        istek.not_metni,
        istek.taksit_id,
        istek.taksit_no,
        istek.taksit_toplam,
    )
    return _harcama_yanitina_cevir(belge)


@router.get("/", response_model=HarcamaListesiYaniti)
async def harcamalari_listele(
    gun: str | None = None,
    baslangic_gun: str | None = None,
    bitis_gun: str | None = None,
    kategori: str | None = None,
    sayfa: int = Query(default=1, ge=1),
    sayfa_boyutu: int = Query(default=VARSAYILAN_SAYFA_BOYUTU, ge=1, le=200),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> HarcamaListesiYaniti:
    """Gün / tarih aralığı / kategori süzgeciyle sayfalanmış listeleme."""
    kayitlar, toplam_kayit = await servis.harcamalari_listele(
        kullanici_id, gun, baslangic_gun, bitis_gun, kategori, sayfa, sayfa_boyutu
    )
    return HarcamaListesiYaniti(
        kayitlar=[_harcama_yanitina_cevir(k) for k in kayitlar],
        toplam_kayit=toplam_kayit,
        sayfa=sayfa,
        sayfa_boyutu=sayfa_boyutu,
    )


@router.get("/{harcama_id}", response_model=HarcamaYaniti)
async def harcama_getir(
    harcama_id: str,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> HarcamaYaniti:
    """Tek kayıt okur (E-12 detay ekranı)."""
    belge = await servis.harcama_getir(kullanici_id, harcama_id)
    return _harcama_yanitina_cevir(belge)


@router.patch("/{harcama_id}", response_model=HarcamaYaniti)
async def harcama_guncelle(
    harcama_id: str,
    istek: HarcamaGuncellemeIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> HarcamaYaniti:
    """E-12 "Kaydet": yalnız gönderilen alanlar güncellenir; taksitli kayıtta tutar reddedilir."""
    alanlar = {alan: getattr(istek, alan) for alan in istek.model_fields_set}
    belge = await servis.harcama_guncelle(kullanici_id, harcama_id, alanlar)
    return _harcama_yanitina_cevir(belge)


@router.delete("/{harcama_id}", status_code=status.HTTP_204_NO_CONTENT)
async def harcama_sil(
    harcama_id: str,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> None:
    """Kalıcı silme — istemci 6 sn "geri al" penceresini kendi tarafında bekletir (K-029, bkz. servis notu)."""
    await servis.harcama_sil(kullanici_id, harcama_id)


@router.delete("/taksit/{taksit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def taksit_serisi_sil(
    taksit_id: str,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> None:
    """E-13 — taksit serisini TAMAMEN siler (onaylıdır, geri alma yoktur)."""
    await servis.taksit_serisi_sil(kullanici_id, taksit_id)


@router.put("/gun-durumu", response_model=GunDurumuYaniti)
async def gun_durumu_isaretle(
    istek: GunDurumuIsaretleIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> GunDurumuYaniti:
    """K-048 hile kapısı (b): bir günü "harcamasız" işaretler/kaldırır."""
    belge = await servis.gun_durumu_isaretle(kullanici_id, istek.gun, istek.harcamasiz)
    return _gun_durumu_yanitina_cevir(belge)


@router.get("/gun-durumu/{gun}", response_model=GunDurumuYaniti)
async def gun_durumu_getir(
    gun: str,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> GunDurumuYaniti:
    """Bir günün "harcamasız" işaretli olup olmadığını döner."""
    belge = await servis.gun_durumu_getir(kullanici_id, gun)
    return _gun_durumu_yanitina_cevir(belge)


@router.get("/ayar/kategori-limitleri", response_model=list[KategoriLimitiYaniti])
async def kategori_limitlerini_getir(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: HarcamaService = Depends(_servis)
) -> list[KategoriLimitiYaniti]:
    """E-17 — yalnız değeri olan kategori limitlerini `sira`ya göre döner."""
    belgeler = await servis.kategori_limitlerini_getir(kullanici_id)
    return [_kategori_limiti_yanitina_cevir(b) for b in belgeler]


@router.put("/ayar/kategori-limitleri", response_model=KategoriLimitiYaniti)
async def kategori_limiti_yaz(
    istek: KategoriLimitiYaziIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> KategoriLimitiYaniti:
    """E-17 — bir kategorinin limitini yazar/günceller."""
    belge = await servis.kategori_limiti_yaz(kullanici_id, istek.kategori, istek.limit_kurus, istek.sira)
    return _kategori_limiti_yanitina_cevir(belge)


@router.delete("/ayar/kategori-limitleri/{kategori}", status_code=status.HTTP_204_NO_CONTENT)
async def kategori_limiti_sil(
    kategori: str,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> None:
    """Madde 2 (K-085/BE-4b) — bir kategorinin limitini kaldırır (PUT'un
    `limit_kurus>0` zorunluluğu "sil"i temsil edemiyordu)."""
    await servis.kategori_limiti_sil(kullanici_id, kategori)


@router.post("/ayar/limit-gecmisi", response_model=LimitGecmisiYaniti, status_code=status.HTTP_201_CREATED)
async def limit_gecmisi_yaz(
    istek: LimitGecmisiYaziIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> LimitGecmisiYaniti:
    """K-064/1 — günlük limit değiştiğinde yürürlük tarihiyle birlikte bir satır yazar."""
    belge = await servis.limit_gecmisi_yaz(kullanici_id, istek.yururluk_tarihi, istek.kurus)
    return _limit_gecmisi_yanitina_cevir(belge)


@router.get("/ayar/urun-kategori-ogrenme", response_model=list[UrunKategoriOgrenmeYaniti])
async def urun_kategori_ogrenmelerini_getir(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: HarcamaService = Depends(_servis)
) -> list[UrunKategoriOgrenmeYaniti]:
    """Tüm öğrenilmiş ürün→kategori eşlemeleri — arama ekranı bir kerede yükler."""
    belgeler = await servis.urun_kategori_ogrenmelerini_getir(kullanici_id)
    return [_urun_kategori_yanitina_cevir(b) for b in belgeler]


@router.put("/ayar/urun-kategori-ogrenme", response_model=UrunKategoriOgrenmeYaniti)
async def urun_kategori_ogren(
    istek: UrunKategoriOgrenmeYaziIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> UrunKategoriOgrenmeYaniti:
    """Bir ürün adı için kategoriyi elle (harcama eklemeden) öğretir/düzeltir."""
    belge = await servis.urun_kategori_ogren(kullanici_id, istek.urun_adi, istek.kategori)
    assert belge is not None  # DTO `min_length=1` + validator zaten boş anahtarı engeller
    return _urun_kategori_yanitina_cevir(belge)


@router.get("/ayar/en-eski-kayit-gunu", response_model=EnEskiKayitGunuYaniti)
async def en_eski_kayit_gunu(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: HarcamaService = Depends(_servis)
) -> EnEskiKayitGunuYaniti:
    """Madde 4 (K-085/BE-4b) — istemcinin seri sınırı hesabı için ilk harcama kaydının günü."""
    return EnEskiKayitGunuYaniti(gun=await servis.en_eski_kayit_gunu(kullanici_id))


@router.delete("/ayar/tum-veriler", status_code=status.HTTP_204_NO_CONTENT)
async def tum_verileri_sil(
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: HarcamaService = Depends(_servis),
) -> None:
    """Madde 3 (K-085/BE-4b) — Ayarlar'daki yüksek etkili eylem: harcama/limit/gün
    durumu/limit geçmişi/ürün öğrenme verisini siler; HESABI VE PROFİLİ SİLMEZ
    (kullanıcı uygulamada kalır, sıfırdan başlar) — `DELETE /auth/hesap` (Madde 1)
    ile farkı budur. Aynı `kullanici_verisini_sil` metodunu yeniden kullanır."""
    await servis.kullanici_verisini_sil(kullanici_id)
