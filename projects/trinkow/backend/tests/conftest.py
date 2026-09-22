"""
Test veritabanı bağlamı.

Testler gerçek MongoDB'ye karşı, ama **ayrı bir test veritabanında**
çalışır (dev/prod verisine dokunmamak için). Her testten önce/sonra bu
veritabanı temizlenir; env değişkenleri `app.*` içe aktarılmadan ÖNCE
ayarlanır ki `get_settings()`in önbelleği baştan test değerleriyle dolsun.

`temiz_veritabani` BİLEREK `autouse` DEĞİL: Mongo'ya hiç dokunmayan saf
formül/iş mantığı testleri (ör. `kalan_gun_hesapla`) bu fixture'ı istemez —
autouse olsaydı yerel Mongo kurulu olmayan makinelerde o testler de
bağlantı hatasıyla düşerdi. Mongo'ya ihtiyaç duyan test/dosya bunu açıkça
ister: tek test için parametre olarak (`async def test_x(temiz_veritabani):`)
ya da bir modülün TÜM testleri için `pytestmark = pytest.mark.usefixtures
("temiz_veritabani")`.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

# ÖNCE `.env` yüklenir, SONRA varsayılanlar konur. Sıra önemli:
# `setdefault` önce çalışırsa `.env`'deki gerçek MONGODB_URI'yi gölgeler
# (load_dotenv var olan ortam değişkenlerini ezmez) ve testler Atlas yerine
# localhost'a gitmeye çalışır. Bu hata bir kez yaşandı (K-083).
load_dotenv()

os.environ.setdefault("JWT_SECRET_KEY", "test-suit-icin-gizli-anahtar-asla-prod-degil")
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
# Test veritabanı adı HER ZAMAN ayrıdır: `.env`'deki gerçek veritabanı adı
# ne olursa olsun testler `trinkow_test` üzerinde çalışır, gerçek veriye dokunmaz.
os.environ["MONGODB_DB_NAME"] = os.environ.get("TEST_DB_NAME", "trinkow_test")

import pytest_asyncio  # noqa: E402  (env değişkenlerinden sonra içe aktarılmalı)

from app.core.database import _istemci, get_database, indeksleri_kur  # noqa: E402


_TEMIZLENECEK_KOLEKSIYONLAR = (
    "kullanicilar",
    "yenileme_tokenlari",
    "kullanici_profilleri",
    "harcamalar",
    "kategori_limitleri",
    "gun_durumlari",
    "limit_gecmisleri",
    "urun_kategori_ogrenmeleri",
    "katalog_ogeleri",
)


@pytest_asyncio.fixture
async def temiz_veritabani() -> None:
    """Mongo'ya gerçekten giden testler için: çağrıldığı test/modül öncesi ve
    sonrası `trinkow_test` veritabanındaki modül koleksiyonlarını boşaltır."""
    # Motor istemcisi oluşturulduğu olay döngüsüne bağlanır; pytest-asyncio her
    # teste YENİ bir döngü verdiği için önbellekteki istemci ikinci testte
    # "Event loop is closed" hatası verir. Her testte istemciyi tazeliyoruz.
    _istemci.cache_clear()
    await indeksleri_kur()
    veritabani = get_database()
    for koleksiyon in _TEMIZLENECEK_KOLEKSIYONLAR:
        await veritabani[koleksiyon].delete_many({})
    yield
    for koleksiyon in _TEMIZLENECEK_KOLEKSIYONLAR:
        await veritabani[koleksiyon].delete_many({})
