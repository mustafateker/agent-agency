"""
Uygulama ayarlarını ortam değişkenlerinden okur.

Gizli anahtarlar/koda gömülmez (CLAUDE.md kuralı); `.env` dosyası varsa
otomatik yüklenir, yoksa gerçek ortam değişkenleri kullanılır.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Ayarlar:
    """Tek bir istekte defalarca ortam değişkeni okumamak için sabitlenmiş ayar demeti."""

    mongo_uri: str
    mongo_veritabani: str
    jwt_gizli_anahtar: str
    jwt_algoritma: str
    erisim_token_dakika: int
    yenileme_token_gun: int
    gelistirme_girisi: bool = False


def _pozitif_int_oku(anahtar: str, varsayilan: int) -> int:
    """Ortam değişkenini tamsayıya çevirir; boşsa varsayılanı kullanır."""
    ham_deger = os.environ.get(anahtar)
    if ham_deger is None or ham_deger.strip() == "":
        return varsayilan
    try:
        deger = int(ham_deger)
    except ValueError as hata:
        raise RuntimeError(f"{anahtar} ortam değişkeni sayı olmalı, gelen değer: {ham_deger!r}") from hata
    if deger <= 0:
        raise RuntimeError(f"{anahtar} ortam değişkeni pozitif olmalı, gelen değer: {deger}")
    return deger


@lru_cache
def get_settings() -> Ayarlar:
    """Ayarları bir kez okuyup önbelleğe alır (her istekte ortamı yeniden taramamak için)."""
    jwt_gizli_anahtar = os.environ.get("JWT_SECRET_KEY")
    if not jwt_gizli_anahtar:
        raise RuntimeError(
            "JWT_SECRET_KEY ortam değişkeni tanımlı değil. "
            ".env dosyasını .env.example'dan kopyalayıp doldur."
        )

    return Ayarlar(
        mongo_uri=os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        mongo_veritabani=os.environ.get("MONGODB_DB_NAME", "trinkow"),
        jwt_gizli_anahtar=jwt_gizli_anahtar,
        jwt_algoritma=os.environ.get("JWT_ALGORITHM", "HS256"),
        erisim_token_dakika=_pozitif_int_oku("ACCESS_TOKEN_EXPIRE_MINUTES", 15),
        yenileme_token_gun=_pozitif_int_oku("REFRESH_TOKEN_EXPIRE_DAYS", 30),
        gelistirme_girisi=os.environ.get("TRINKOW_DEV_LOGIN") == "1",
    )
