"""
Katalog modülünün HTTP katmanı: kataloğu (sürüm/ETag ile) listeleme + tek
kalem okuma. İş mantığı burada YOK — `KatalogService`e devredilir
(harcama_controller.py ile aynı desen, K-068/3).

Ürün arama istemcide kalır (görev notu) — bu yüzden sunucuda arama ucu
YOK, yalnız listeleme + tekil okuma var. Yazma ucu da YOK: kalemler yalnız
tohumlama ile oluşur (bkz. katalog_service.tohumla + main.py yaşam
döngüsü).

Yetkilendirme diğer modüllerle aynı: `auth`ın `gecerli_kullanici_id`
bağımlılığı — katalog kullanıcıya özgü veri taşımasa da uygulamanın geri
kalanıyla aynı oturum kuralına tabidir (token'sız erişilemez).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse, Response

from app.core.database import get_database
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.katalog.katalog_dto import KatalogListesiYaniti, KatalogOgesiYaniti
from app.modules.katalog.katalog_model import KatalogOgesiBelgesi
from app.modules.katalog.katalog_service import KatalogService

router = APIRouter(prefix="/katalog", tags=["katalog"])


def _servis() -> KatalogService:
    return KatalogService(get_database())


def _oge_yanitina_cevir(belge: KatalogOgesiBelgesi) -> KatalogOgesiYaniti:
    return KatalogOgesiYaniti(kod=belge.kod, ad=belge.ad, kategori=belge.kategori)


@router.get("/")
async def katalogu_listele(
    if_none_match: str | None = Header(default=None, alias="If-None-Match"),
    _kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KatalogService = Depends(_servis),
) -> Response:
    """Tüm katalog kalemlerini + sürüm bilgisini döner.

    İstemci önceki isteğinden aldığı `ETag`i `If-None-Match` ile gönderirse
    ve katalog değişmemişse gövde YOLLANMADAN 304 döner (bant genişliği
    tasarrufu); `surum` alanı, HTTP önbelleğini kullanmayan istemciler için
    aynı bilgiyi gövdede de taşır.
    """
    ogeler, surum = await servis.katalogu_listele()
    etiket = f'"{surum}"'
    if if_none_match is not None and if_none_match.strip('"') == surum:
        return Response(status_code=304, headers={"ETag": etiket})
    yanit = KatalogListesiYaniti(ogeler=[_oge_yanitina_cevir(o) for o in ogeler], surum=surum)
    return JSONResponse(content=yanit.model_dump(), headers={"ETag": etiket})


@router.get("/{kod}", response_model=KatalogOgesiYaniti)
async def katalog_ogesi_getir(
    kod: str,
    _kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KatalogService = Depends(_servis),
) -> KatalogOgesiYaniti:
    """Tek bir katalog kalemini `kod`una göre okur."""
    belge = await servis.oge_getir(kod)
    return _oge_yanitina_cevir(belge)
