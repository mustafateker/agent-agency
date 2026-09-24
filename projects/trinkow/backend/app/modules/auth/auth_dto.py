"""
Auth uç noktalarının dışarıya açtığı istek/yanıt sözleşmesi.

Mobil uygulama bu alanlara göre form gönderir (bkz.
docs/design/prototip-v4/15-giris.html, 16-kayit.html) ve bu şemaya göre
yanıt bekler. Mongo şeması (auth_model.py) değişse bile bu sözleşme
kararlı kalmalıdır.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class KayitIstegi(BaseModel):
    """E-23 Hesap oluştur formunun gönderdiği alanlar."""

    email: EmailStr
    sifre: str = Field(min_length=8, max_length=128)


class GirisIstegi(BaseModel):
    """E-22 Oturum aç formunun gönderdiği alanlar."""

    email: EmailStr
    sifre: str = Field(min_length=1, max_length=128)


class GelistirmeGirisIstegi(BaseModel):
    """Geçici test girişi; e-posta biçimi ve şifre doğrulanmaz."""

    email: str = Field(min_length=1, max_length=320)
    sifre: str = Field(min_length=1, max_length=128)


class TokenYenilemeIstegi(BaseModel):
    yenileme_tokeni: str


class OturumKapatmaIstegi(BaseModel):
    yenileme_tokeni: str


class TokenCiftiYaniti(BaseModel):
    """Kayıt ve giriş sonrası döndürülen token çifti."""

    erisim_tokeni: str
    yenileme_tokeni: str
    token_turu: str = "bearer"


class ErisimTokeniYaniti(BaseModel):
    """Token yenileme sonrası döndürülen tek erişim token'ı."""

    erisim_tokeni: str
    token_turu: str = "bearer"


class KullaniciYaniti(BaseModel):
    """"Ben kimim" uç noktasının döndürdüğü kullanıcı bilgisi."""

    id: str
    email: EmailStr
    kimlik_saglayici: str
    olusturulma_tarihi: datetime


class SifreSifirlamaIstegi(BaseModel):
    email: EmailStr


class SifreYenilemeIstegi(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    sifre: str = Field(min_length=8, max_length=128)


class MesajYaniti(BaseModel):
    mesaj: str
