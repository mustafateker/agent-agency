"""
Harcama modülünün dışarıya açtığı istek/yanıt sözleşmesi.

Alan adları istemcideki `harcama` / `kategori_limiti` / `gun_durumu` /
`limit_gecmisi` / `urun_kategori_ogrenme` tablolarıyla (app/src/db/semasi.ts,
şema sürümü 5) birebir eşleşir — bir sonraki turda istemci bu API'ye
bağlanacağı için isim uyuşmazlığı bağlama turunu iki katına çıkarır (bkz.
görev notu). Mongo şeması (harcama_model.py) değişse bile bu sözleşme
kararlı kalmalıdır (K-068/3).

Kategori kodu bilerek `str` bırakıldı, `Literal` YAPILMADI: kategori
kataloğu `katalog` modülünün konusu (bu turun kapsamı DIŞINDA) — kategori
listesini burada sabitlemek iki modülü gizlice birbirine bağlar.
"""
from __future__ import annotations

from typing import Literal
from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

OdemeTipi = Literal["nakit", "kart"]

_GUN_DESENI = r"^\d{4}-\d{2}-\d{2}$"


class HarcamaEkleIstegi(BaseModel):
    """Tek bir harcama satırı ekler.

    Taksitli bir seri oluşturmak için istemci bu uç noktayı taksit sayısı
    kadar çağırır (`taksit_id` aynı, `taksit_no`/`taksit_toplam` ile) —
    istemcideki `taksitSerisiOlustur` bugün de aynı şekilde `harcamaEkle`yi
    döngüyle çağırıyor, sunucu tarafında ayrı bir "seri oluştur" uç noktası
    AÇILMADI (Madde 3 uç nokta listesinde de yok).
    """

    istemci_id: UUID | None = None
    rutin_id: str | None = None
    adet: int = Field(default=1, gt=0, strict=True)
    sabit_gider_kodu: Literal["kira", "fatura", "ulasim", "kredi"] | None = None
    tutar_kurus: int = Field(gt=0)
    kategori: str = Field(min_length=1)
    urun_adi: str | None = None
    # ISO 8601 yerel damga — istemciden geldiği gibi saklanır, sunucu saat
    # dilimi VARSAYMAZ (Madde 2).
    zaman: str = Field(min_length=1)
    gun: str = Field(pattern=_GUN_DESENI)
    odeme: OdemeTipi
    not_metni: str | None = None
    taksit_id: str | None = None
    taksit_no: int | None = Field(default=None, ge=1)
    taksit_toplam: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def _taksit_alanlari_tutarli_mi(self) -> "HarcamaEkleIstegi":
        alanlar = (self.taksit_id, self.taksit_no, self.taksit_toplam)
        if any(a is not None for a in alanlar) and not all(a is not None for a in alanlar):
            raise ValueError("Taksit alanları (taksit_id, taksit_no, taksit_toplam) birlikte gelmeli.")
        if self.taksit_no is not None and self.taksit_toplam is not None and self.taksit_no > self.taksit_toplam:
            raise ValueError("taksit_no, taksit_toplam'dan büyük olamaz.")
        return self


class HarcamaGuncellemeIstegi(BaseModel):
    """E-12 "Kaydet" — yalnız gönderilen alanlar güncellenir (Katman2Istegi ile aynı desen).

    `tutar_kurus` BİLEREK burada da var: taksitli bir kayıtta gönderilirse
    servis katmanı reddeder (Madde 2) — DTO seviyesinde taksitli/taksitsiz
    ayrımı yapılamaz çünkü mevcut kaydı bilmeden karar verilemez.
    """

    rutin_id: str | None = None
    adet: int | None = Field(default=None, gt=0, strict=True)
    sabit_gider_kodu: Literal["kira", "fatura", "ulasim", "kredi"] | None = None
    tutar_kurus: int | None = Field(default=None, gt=0)
    kategori: str | None = Field(default=None, min_length=1)
    urun_adi: str | None = None
    zaman: str | None = Field(default=None, min_length=1)
    gun: str | None = Field(default=None, pattern=_GUN_DESENI)
    odeme: OdemeTipi | None = None
    not_metni: str | None = None


class HarcamaYaniti(BaseModel):
    rutin_id: str | None = None
    adet: int = 1
    sabit_gider_kodu: str | None = None
    id: str
    tutar_kurus: int
    kategori: str
    urun_adi: str | None
    zaman: str
    gun: str
    odeme: OdemeTipi
    not_metni: str | None
    taksit_id: str | None
    taksit_no: int | None
    taksit_toplam: int | None


class HarcamaListesiYaniti(BaseModel):
    """Sayfalanmış harcama listesi (300+ günlük geçmiş senaryosu, Madde 3)."""

    kayitlar: list[HarcamaYaniti]
    toplam_kayit: int
    sayfa: int
    sayfa_boyutu: int


class KategoriLimitiYaziIstegi(BaseModel):
    kategori: str = Field(min_length=1)
    limit_kurus: int = Field(gt=0)
    sira: int = Field(default=0, ge=0)


class KategoriLimitiYaniti(BaseModel):
    kategori: str
    limit_kurus: int
    sira: int


class GunDurumuIsaretleIstegi(BaseModel):
    """K-048 hile kapısı (b) — bir günü "harcamasız" olarak işaretler/kaldırır."""

    gun: str = Field(pattern=_GUN_DESENI)
    harcamasiz: bool = True


class GunDurumuYaniti(BaseModel):
    gun: str
    harcamasiz: bool


class LimitGecmisiYaziIstegi(BaseModel):
    """K-064/1 — günlük limit değiştiğinde yürürlük tarihiyle birlikte yazılır."""

    yururluk_tarihi: str = Field(pattern=_GUN_DESENI)
    kurus: int = Field(gt=0)


class LimitGecmisiYaniti(BaseModel):
    yururluk_tarihi: str
    kurus: int


class UrunKategoriOgrenmeYaziIstegi(BaseModel):
    """Ham ürün adını alır; anahtar sunucuda normalize edilir (bkz. harcama_service._turkce_normalize)."""

    urun_adi: str = Field(min_length=1)
    kategori: str = Field(min_length=1)

    @field_validator("urun_adi")
    @classmethod
    def _bos_olmayan_metin(cls, deger: str) -> str:
        if not deger.strip():
            raise ValueError("urun_adi boş olamaz.")
        return deger


class UrunKategoriOgrenmeYaniti(BaseModel):
    urun_anahtari: str
    kategori: str


class EnEskiKayitGunuYaniti(BaseModel):
    """Madde 4 (K-085/BE-4b) — istemcinin seri sınırı hesabı için ilk harcama
    kaydının günü; hiç kayıt yoksa `gun=None` döner."""

    gun: str | None
