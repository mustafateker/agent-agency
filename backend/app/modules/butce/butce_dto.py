"""Versioned budget and reusable spending input contracts."""
from __future__ import annotations
from typing import Annotated, Literal
from pydantic import BaseModel, Field, model_validator

Para = Annotated[int, Field(strict=True, ge=0)]
Pozitif = Annotated[int, Field(strict=True, gt=0)]
KATEGORILER = frozenset(('market','saglik','kafe','restoran','ulasim','akaryakit','fatura','kiraev','abonelik','eglence','giyim','aliskanliklar','diger'))

class SabitGiderler(BaseModel):
    kira: Para = 0
    fatura: Para = 0
    ulasim: Para = 0
    kredi: Para = 0

class ButceIstegi(BaseModel):
    gelir_kurus: Para | None = None
    sabit_giderler: SabitGiderler = Field(default_factory=SabitGiderler)
    hedef_birikim_kurus: Para = 0
    borc_kurus: Para | None = None
    limit_modu: Literal['otomatik','manuel'] = 'otomatik'
    manuel_limit_kurus: Pozitif | None = None
    kategori_limitleri: dict[str, Para] = Field(default_factory=dict)

    @model_validator(mode='after')
    def tutarlilik(self) -> 'ButceIstegi':
        if self.limit_modu == 'manuel' and self.manuel_limit_kurus is None:
            raise ValueError('Manuel günlük limit gerekli.')
        if set(self.kategori_limitleri) - KATEGORILER:
            raise ValueError('Bilinmeyen kategori.')
        return self

class RutinIstegi(BaseModel):
    ad: str = Field(min_length=1, max_length=80)
    kategori: str
    gunluk_adet: Pozitif = 1
    birim_fiyat_kurus: Pozitif
    aktif: bool = True

    @model_validator(mode='after')
    def kategori_gecerli(self) -> 'RutinIstegi':
        if self.kategori not in KATEGORILER or not self.ad.strip():
            raise ValueError('Geçerli ad ve kategori gerekli.')
        return self

class VazgecmeIstegi(BaseModel):
    gun: str
    adet: Para

class FavoriIstegi(BaseModel):
    ad: str = Field(min_length=1, max_length=80)
    kategori: str
    tutar_kurus: Pozitif

    @model_validator(mode='after')
    def kategori_gecerli(self) -> 'FavoriIstegi':
        if self.kategori not in KATEGORILER or not self.ad.strip():
            raise ValueError('Geçerli ad ve kategori gerekli.')
        return self
