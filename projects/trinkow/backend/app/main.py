"""
Uygulamanın giriş noktası.

Yalnızca modül router'larını toplar ve ortak hata/başlangıç davranışını
bağlar; iş mantığı burada YAZILMAZ (bkz. backend/README.md klasör
yapısı kuralları).
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import get_database, indeksleri_kur
from app.core.errors import UygulamaHatasi
from app.modules.auth.auth_controller import router as auth_router
from app.modules.harcama.harcama_controller import router as harcama_router
from app.modules.katalog.katalog_controller import router as katalog_router
from app.modules.katalog.katalog_service import KatalogService
from app.modules.kullanici.kullanici_controller import router as kullanici_router
from app.modules.ozet.ozet_controller import router as ozet_router


@asynccontextmanager
async def yasam_dongusu(_uygulama: FastAPI) -> AsyncIterator[None]:
    """Açılışta Mongo index'lerini garanti eder ve katalog boşsa tohumlar."""
    await indeksleri_kur()
    await KatalogService(get_database()).tohumla()
    yield


app = FastAPI(title="Trinkow Backend", lifespan=yasam_dongusu)
app.include_router(auth_router)
app.include_router(kullanici_router)
app.include_router(harcama_router)
app.include_router(ozet_router)
app.include_router(katalog_router)


@app.exception_handler(UygulamaHatasi)
async def uygulama_hatasi_isleyici(_istek: Request, hata: UygulamaHatasi) -> JSONResponse:
    """Tüm modüllerin ortak hata sözleşmesini tek bir JSON biçimine çevirir."""
    return JSONResponse(status_code=hata.durum_kodu, content={"hata_kodu": hata.hata_kodu, "mesaj": hata.mesaj})


@app.get("/saglik")
async def saglik_kontrolu() -> dict[str, str]:
    """Servisin ayakta olup olmadığını kontrol etmek için basit uç nokta."""
    return {"durum": "ayakta"}
