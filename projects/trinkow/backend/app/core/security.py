"""
Şifre hashleme ve JWT üretme/doğrulama işlemleri.

Bu modül kriptografi ile ilgili tüm kodu tek yerde toplar; auth_service
kendi hash/imza mantığını yazmaz, yalnız buradaki fonksiyonları çağırır.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

_sifre_baglami = CryptContext(schemes=["bcrypt"], deprecated="auto")

TokenTuru = Literal["erisim", "yenileme"]


def sifre_hashle(duz_sifre: str) -> str:
    """Kullanıcı şifresini geri döndürülemez biçimde hashler; ham şifre asla saklanmaz/loglanmaz."""
    return _sifre_baglami.hash(duz_sifre)


def sifre_dogrula(duz_sifre: str, hashli_sifre: str) -> bool:
    """Girilen düz şifreyi saklanan hash ile karşılaştırır."""
    return _sifre_baglami.verify(duz_sifre, hashli_sifre)


def erisim_tokeni_olustur(kullanici_id: str, gecerlilik: timedelta | None = None) -> str:
    """Kısa ömürlü erişim token'ı üretir (varsayılan ömür ayarlardan gelir)."""
    ayarlar = get_settings()
    sure = gecerlilik if gecerlilik is not None else timedelta(minutes=ayarlar.erisim_token_dakika)
    return _token_olustur(kullanici_id, sure, "erisim")


def yenileme_tokeni_olustur(
    kullanici_id: str, jti: str | None = None, gecerlilik: timedelta | None = None
) -> tuple[str, str]:
    """Uzun ömürlü yenileme token'ı üretir; iptal edilebilmesi için benzersiz `jti` taşır."""
    ayarlar = get_settings()
    sure = gecerlilik if gecerlilik is not None else timedelta(days=ayarlar.yenileme_token_gun)
    token_kimligi = jti or str(uuid.uuid4())
    token = _token_olustur(kullanici_id, sure, "yenileme", token_kimligi)
    return token, token_kimligi


def _token_olustur(kullanici_id: str, gecerlilik: timedelta, tur: TokenTuru, jti: str | None = None) -> str:
    ayarlar = get_settings()
    simdi = datetime.now(timezone.utc)
    yuk: dict[str, Any] = {
        "sub": kullanici_id,
        "tur": tur,
        "iat": simdi,
        "exp": simdi + gecerlilik,
    }
    if jti is not None:
        yuk["jti"] = jti
    return jwt.encode(yuk, ayarlar.jwt_gizli_anahtar, algorithm=ayarlar.jwt_algoritma)


def token_coz(token: str) -> dict[str, Any]:
    """Token'ı doğrular ve içeriğini döndürür.

    Süresi geçmişse `jwt.ExpiredSignatureError`, biçimi/imzası bozuksa
    `jwt.InvalidTokenError` fırlatır — çağıran taraf (auth_service) bunları
    kendi hata sözleşmesine (app.core.errors) çevirir.
    """
    ayarlar = get_settings()
    return jwt.decode(token, ayarlar.jwt_gizli_anahtar, algorithms=[ayarlar.jwt_algoritma])
