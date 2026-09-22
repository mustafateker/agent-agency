"""
Kullanıcı modülünün dışarıya açtığı istek/yanıt sözleşmesi.

Alan adları istemcideki `profil` tablosuyla (app/src/db/semasi.ts, şema
sürümü 5) birebir eşleşir. Mongo şeması (kullanici_model.py) değişse bile
bu sözleşme kararlı kalmalıdır (auth_dto.py ile aynı ilke, K-068/3).
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Niyet = Literal["takip", "tasarruf", "borc"]
Siklik = Literal["gun1", "gun2", "hafta2_3", "hafta1", "ay1_2", "hic", "serbest"]
YatirimNiyet = Literal["yapiyorum", "dusunuyorum", "ilgilenmiyorum"]
TaksitSiklik = Literal["sik_sik", "bazen", "nadiren"]
GunSiniriSaat = Literal[0, 3, 6]
OdemeTipi = Literal["nakit", "kart"]


class AliskanlikGirdisi(BaseModel):
    """Kahve/sigara/alkol/dışarıda yemek kartlarının ortak biçimi (E-25)."""

    siklik: Siklik | None = None
    serbest_sayi: int | None = Field(default=None, ge=0)
    fiyat_kurus: int | None = Field(default=None, ge=0)


class Katman1Istegi(BaseModel):
    """E-01..E-03 Katman 1 formunun gönderdiği alanlar."""

    niyet: Niyet | None = None
    gelir_kurus: int | None = Field(default=None, ge=0)
    maas_gunu: int | None = Field(default=None, ge=1, le=31)
    maas_duzensiz: bool = False
    # K-059/5 — istemcinin Katman 1 sonunda hesapladığı ÖNERİ; onay bekler,
    # kabul edilene kadar gunluk_limit_kurus'a yazılmaz (bkz. PUT /plan/gunluk-limit).
    gunluk_limit_onerisi_kurus: int | None = Field(default=None, ge=0)


class Katman2Istegi(BaseModel):
    """E-25 Katman 2'nin 8 kartı — tümü opsiyonel, yalnız GÖNDERİLEN alan güncellenir.

    Kısmi güncelleme, alanın Python tarafında `None` olup olmamasına değil
    (`0` ile `None` anlamca farklıdır), isteğe GERÇEKTEN dahil edilip
    edilmediğine göre çalışır (bkz. kullanici_controller.katman2_alanlarini_ayikla).
    """

    kira_aidat_kurus: int | None = Field(default=None, ge=0)
    faturalar_kurus: int | None = Field(default=None, ge=0)
    ulasim_yakit_kurus: int | None = Field(default=None, ge=0)
    kredi_taksit_kurus: int | None = Field(default=None, ge=0)
    kahve: AliskanlikGirdisi | None = None
    sigara: AliskanlikGirdisi | None = None
    alkol: AliskanlikGirdisi | None = None
    yemek: AliskanlikGirdisi | None = None
    abonelik_adet: int | None = Field(default=None, ge=0)
    abonelik_ortalama_kurus: int | None = Field(default=None, ge=0)
    yatirim_niyet: YatirimNiyet | None = None
    birikim_yuzde: int | None = Field(default=None, ge=0, le=100)
    taksit_siklik: TaksitSiklik | None = None
    # "Kaldığın yerden" — en son açık bırakılan kart (1-8), 8 karta dahil değil.
    son_kart: int | None = Field(default=None, ge=1, le=8)


class GunlukLimitIstegi(BaseModel):
    """E-17 Limitler — günlük limiti elle yazma."""

    gunluk_limit_kurus: int = Field(gt=0)


class AliskanlikYaniti(BaseModel):
    siklik: Siklik | None
    serbest_sayi: int | None
    fiyat_kurus: int | None


class KullaniciProfilYaniti(BaseModel):
    """Profil okuma ve her kaydetme/hesaplama uç noktasının döndürdüğü tam profil."""

    niyet: Niyet | None
    gelir_kurus: int | None
    maas_gunu: int | None
    maas_duzensiz: bool
    onboarding_tamamlandi: bool
    kira_aidat_kurus: int | None
    faturalar_kurus: int | None
    ulasim_yakit_kurus: int | None
    kredi_taksit_kurus: int | None
    kahve: AliskanlikYaniti
    sigara: AliskanlikYaniti
    alkol: AliskanlikYaniti
    yemek: AliskanlikYaniti
    abonelik_adet: int | None
    abonelik_ortalama_kurus: int | None
    yatirim_niyet: YatirimNiyet | None
    birikim_yuzde: int | None
    taksit_siklik: TaksitSiklik | None
    plan_kuruldu: bool
    zorunlu_kurus: int | None
    zorunlu_pay_yuzde: int | None
    sosyal_kurus: int | None
    sosyal_pay_yuzde: int | None
    birikim_kurus: int | None
    birikim_pay_yuzde: int | None
    gunluk_limit_kurus: int | None
    plan_kurulum_tarihi: datetime | None
    katman2_dolan_kart_sayisi: int
    gunluk_limit_onerisi_kurus: int | None
    son_kart: int


class TercihlerGuncellemeIstegi(BaseModel):
    """E-19 Ayarlar — yalnız GÖNDERİLEN alan güncellenir (Katman2Istegi ile aynı desen).

    `kurulum_gunu` yalnız hiç ayarlanmamışsa yazılır; bir kez ayarlandıktan
    sonra sunucu tarafında sabittir (K-049 seri hesabı sınırı) — tekrar
    gönderilirse sessizce yok sayılır (bkz. kullanici_service.tercihleri_guncelle).
    """

    bildirim_aksam_ozet: bool | None = None
    bildirim_saati: str | None = None
    gun_siniri: GunSiniriSaat | None = None
    varsayilan_odeme: OdemeTipi | None = None
    kurulum_gunu: str | None = None


class TercihlerYaniti(BaseModel):
    """Uygulama tercihleri okuma/güncelleme yanıtı — istemcideki `ayar` tablosunun karşılığı."""

    bildirim_aksam_ozet: bool
    bildirim_tercih_belirlendi: bool
    bildirim_saati: str
    gun_siniri: GunSiniriSaat
    varsayilan_odeme: OdemeTipi
    kurulum_gunu: str | None
