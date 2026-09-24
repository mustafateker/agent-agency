"""
Motor (async MongoDB sürücüsü) bağlantısını tek yerden yönetir.

Her modül kendi bağlantısını açmak yerine `get_database()` ile paylaşılan
veritabanı nesnesini alır; bağlantı ayarları `app.core.config`ten gelir.
"""
from __future__ import annotations

from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


@lru_cache
def _istemci() -> AsyncIOMotorClient:
    ayarlar = get_settings()
    return AsyncIOMotorClient(ayarlar.mongo_uri, serverSelectionTimeoutMS=10000, connectTimeoutMS=10000)


def get_database() -> AsyncIOMotorDatabase:
    """İstek başına yeni bağlantı açmadan paylaşılan veritabanı nesnesini döndürür."""
    ayarlar = get_settings()
    return _istemci()[ayarlar.mongo_veritabani]


async def indeksleri_kur() -> None:
    """Uygulama açılışında gerekli benzersizlik/TTL index'lerini garanti eder.

    E-posta benzersizliği yalnız uygulama kontrolüyle değil, Mongo unique
    index ile garanti edilir (görev gereği). Yenileme token'ları süresi
    dolunca TTL index ile kendiliğinden silinir.
    """
    veritabani = get_database()
    await veritabani["auth_hiz_siniri"].create_index("son", expireAfterSeconds=3600)
    await veritabani["kullanicilar"].create_index("email", unique=True)
    await veritabani["yenileme_tokenlari"].create_index("jti", unique=True)
    await veritabani["yenileme_tokenlari"].create_index("son_kullanma_tarihi", expireAfterSeconds=0)
    await veritabani["kullanici_profilleri"].create_index("kullanici_id", unique=True)
    await veritabani["harcamalar"].create_index([("kullanici_id", 1), ("gun", 1)])
    await veritabani["harcamalar"].create_index([("kullanici_id", 1), ("taksit_id", 1)])
    await veritabani["kategori_limitleri"].create_index([("kullanici_id", 1), ("kategori", 1)], unique=True)
    await veritabani["gun_durumlari"].create_index([("kullanici_id", 1), ("gun", 1)], unique=True)
    await veritabani["limit_gecmisleri"].create_index([("kullanici_id", 1), ("yururluk_tarihi", 1)], unique=True)
    await veritabani["urun_kategori_ogrenmeleri"].create_index(
        [("kullanici_id", 1), ("urun_anahtari", 1)], unique=True
    )
    await veritabani["katalog_ogeleri"].create_index("kod", unique=True)

    for koleksiyon in ("butce_surumleri", "butce_gocleri", "rutin_surumleri", "rutin_vazgecmeleri", "favori_kalemler", "birikim_defterleri"):
        await veritabani[koleksiyon].create_index("kullanici_id")
    for koleksiyon in ("butce_surumleri", "rutin_surumleri"):
        await veritabani[koleksiyon].create_index([("kullanici_id", 1), ("yururluk_gunu", 1)])
    await veritabani["rutin_vazgecmeleri"].create_index([("kullanici_id", 1), ("gun", 1)])

    await veritabani["harcamalar"].create_index([("kullanici_id", 1), ("istemci_id", 1)], unique=True, partialFilterExpression={"istemci_id": {"$type": "string"}})
