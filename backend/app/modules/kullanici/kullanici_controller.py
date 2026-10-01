"""
Kullanıcı modülünün HTTP katmanı: profil okuma, Katman 1/2 kaydetme, plan
kurma, günlük limiti elle ayarlama. İş mantığı burada YOK — hepsi
`KullaniciService`e devredilir (auth_controller.py ile aynı desen, K-068/3).

Yetkilendirme ikinci bir mekanizma kurmadan `auth` modülünün mevcut
`gecerli_kullanici_id` bağımlılığıyla yapılır: her uç nokta yalnız
token'daki kullanıcının KENDİ belgesine erişir, URL'de kullanıcı kimliği
taşınmaz — bu yüzden başka bir kullanıcının profiline erişmenin yapısal
olarak bir yolu yoktur (IDOR yüzeyi yok).
"""
from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.core.database import get_database
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.kullanici.kullanici_dto import (
    AliskanlikYaniti,
    GunlukLimitIstegi,
    Katman1Istegi,
    Katman2Istegi,
    KullaniciProfilYaniti,
    TercihlerGuncellemeIstegi,
    TercihlerYaniti,
)
from app.modules.kullanici.kullanici_model import KullaniciProfilBelgesi
from app.modules.kullanici.kullanici_service import KullaniciService

router = APIRouter(prefix="/kullanici", tags=["kullanici"])

# QA-1/K-087 — `ozet_controller.py`'deki aynı desen: "bugün" istemciden gelir.
_GUN_DESENI = r"^\d{4}-\d{2}-\d{2}$"


def _servis() -> KullaniciService:
    return KullaniciService(get_database())


def katman2_alanlarini_ayikla(istek: Katman2Istegi) -> dict[str, Any]:
    """İstekte GERÇEKTEN geçen üst düzey alanları çıkarır (kısmi güncelleme).

    `model_fields_set`, Pydantic'in varsayılanla değil istekte fiilen
    gönderilen alanları söylediği kümedir. Bir kart (ör. `kahve`)
    gönderildiyse alt alanlarının tamamı (siklik/serbest_sayi/fiyat_kurus)
    birlikte yazılır — kart formu tek seferde gönderilir (E-25).
    """
    alanlar: dict[str, Any] = {}
    for alan_adi in istek.model_fields_set:
        deger = getattr(istek, alan_adi)
        alanlar[alan_adi] = deger.model_dump() if isinstance(deger, BaseModel) else deger
    return alanlar


def _yanita_cevir(profil: KullaniciProfilBelgesi) -> KullaniciProfilYaniti:
    return KullaniciProfilYaniti(
        niyet=profil.niyet,
        gelir_kurus=profil.gelir_kurus,
        maas_gunu=profil.maas_gunu,
        maas_duzensiz=profil.maas_duzensiz,
        onboarding_tamamlandi=profil.onboarding_tamamlandi,
        kira_aidat_kurus=profil.kira_aidat_kurus,
        faturalar_kurus=profil.faturalar_kurus,
        ulasim_yakit_kurus=profil.ulasim_yakit_kurus,
        kredi_taksit_kurus=profil.kredi_taksit_kurus,
        kahve=AliskanlikYaniti(**profil.kahve),
        sigara=AliskanlikYaniti(**profil.sigara),
        alkol=AliskanlikYaniti(**profil.alkol),
        yemek=AliskanlikYaniti(**profil.yemek),
        abonelik_adet=profil.abonelik_adet,
        abonelik_ortalama_kurus=profil.abonelik_ortalama_kurus,
        yatirim_niyet=profil.yatirim_niyet,
        birikim_yuzde=profil.birikim_yuzde,
        taksit_siklik=profil.taksit_siklik,
        plan_kuruldu=profil.plan_kuruldu,
        zorunlu_kurus=profil.zorunlu_kurus,
        zorunlu_pay_yuzde=profil.zorunlu_pay_yuzde,
        sosyal_kurus=profil.sosyal_kurus,
        sosyal_pay_yuzde=profil.sosyal_pay_yuzde,
        birikim_kurus=profil.birikim_kurus,
        birikim_pay_yuzde=profil.birikim_pay_yuzde,
        gunluk_limit_kurus=profil.gunluk_limit_kurus,
        plan_kurulum_tarihi=profil.plan_kurulum_tarihi,
        katman2_dolan_kart_sayisi=profil.katman2_dolan_kart_sayisi(),
        gunluk_limit_onerisi_kurus=profil.gunluk_limit_onerisi_kurus,
        son_kart=profil.son_kart or 1,
    )


def _tercihlere_cevir(profil: KullaniciProfilBelgesi) -> TercihlerYaniti:
    return TercihlerYaniti(
        bildirim_aksam_ozet=profil.bildirim_aksam_ozet,
        bildirim_tercih_belirlendi=profil.bildirim_tercih_belirlendi,
        bildirim_saati=profil.bildirim_saati,
        gun_siniri=profil.gun_siniri,
        varsayilan_odeme=profil.varsayilan_odeme,
        kurulum_gunu=profil.kurulum_gunu,
    )


@router.get("/profil", response_model=KullaniciProfilYaniti)
async def profili_getir(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: KullaniciService = Depends(_servis)
) -> KullaniciProfilYaniti:
    """Oturumdaki kullanıcının profilini döner; hiç doldurulmamışsa varsayılan (boş) profil döner."""
    profil = await servis.profili_getir(kullanici_id)
    return _yanita_cevir(profil)


@router.put("/profil/katman1", response_model=KullaniciProfilYaniti)
async def katman1_kaydet(
    istek: Katman1Istegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> KullaniciProfilYaniti:
    """E-01..E-03 Katman 1: niyet, gelir, maaş günü — kaydeder ve onboarding'i tamamlanmış işaretler."""
    profil = await servis.katman1_kaydet(
        kullanici_id,
        istek.niyet,
        istek.gelir_kurus,
        istek.maas_gunu,
        istek.maas_duzensiz,
        istek.gunluk_limit_onerisi_kurus,
    )
    return _yanita_cevir(profil)


@router.patch("/profil/katman1", response_model=KullaniciProfilYaniti)
async def katman1_guncelle(
    istek: Katman1Istegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> KullaniciProfilYaniti:
    """Madde 5 (K-084/1, BE-4b) — Katman 1'in TEK bir alanını PATCH ile günceller;
    `Katman1Istegi`nin tüm alanları zaten opsiyonel, yalnız GÖNDERİLEN alan yazılır
    (Katman 2'deki kısmi güncelleme deseninin aynısı)."""
    alanlar = {alan: getattr(istek, alan) for alan in istek.model_fields_set}
    profil = await servis.katman1_guncelle(kullanici_id, alanlar)
    return _yanita_cevir(profil)


@router.patch("/profil/katman2", response_model=KullaniciProfilYaniti)
async def katman2_kaydet(
    istek: Katman2Istegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> KullaniciProfilYaniti:
    """E-25 Katman 2 kartları: yalnız gönderilen alanlar güncellenir, diğerleri dokunulmadan kalır."""
    profil = await servis.katman2_kaydet(kullanici_id, katman2_alanlarini_ayikla(istek))
    return _yanita_cevir(profil)


@router.post("/plan/kur", response_model=KullaniciProfilYaniti)
async def plani_kur(
    bugun: str | None = Query(default=None, pattern=_GUN_DESENI),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> KullaniciProfilYaniti:
    """E-26 Planı kur: mevcut Katman 1/2 verisinden zorunlu/sosyal/birikim paylarını ve günlük limiti sunucu hesaplar (K-075).

    QA-1/K-087 — "bugün" istemciden `bugun` sorgu parametresiyle gelir; sunucu
    saat dilimi varsayımı yapmaz (`/ozet/seri`'deki desenle aynı). İSTİSNA:
    parametre gönderilmezse geriye dönük uyumluluk için sunucu UTC gününe
    düşer (eski istemciler kırılmasın) — bu düşüş kalıcı bir davranış değildir,
    istemci bu parametreyi HER ZAMAN göndermelidir.
    """
    secilen_bugun = date.fromisoformat(bugun) if bugun else None
    profil = await servis.plani_kur(kullanici_id, bugun=secilen_bugun)
    return _yanita_cevir(profil)


@router.put("/plan/gunluk-limit", response_model=KullaniciProfilYaniti)
async def gunluk_limiti_ayarla(
    istek: GunlukLimitIstegi,
    bugun: str | None = Query(default=None, pattern=_GUN_DESENI),
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> KullaniciProfilYaniti:
    """E-17 Limitler: günlük limiti plan hesabından bağımsız olarak elle yazar.

    Katman 1'in "Öneriyi kabul et" / "Başka bir sayı yaz" adımları da bunu
    çağırır — bekleyen öneri bu uç noktada otomatik temizlenir.

    QA-1b/K-087 — "bugün" istemciden `bugun` sorgu parametresiyle gelir; sunucu
    saat dilimi varsayımı yapmaz (`/ozet/seri`'deki desenle aynı). İSTİSNA:
    parametre gönderilmezse geriye dönük uyumluluk için sunucu UTC gününe
    düşer (eski istemciler kırılmasın) — istemci bu parametreyi HER ZAMAN
    göndermelidir, `limit_gecmisi`nin doğru güne yazılması buna bağlıdır.
    """
    secilen_bugun = date.fromisoformat(bugun) if bugun else None
    profil = await servis.gunluk_limiti_ayarla(kullanici_id, istek.gunluk_limit_kurus, bugun=secilen_bugun)
    return _yanita_cevir(profil)


@router.delete("/plan/gunluk-limit-onerisi", response_model=KullaniciProfilYaniti)
async def oneriyi_reddet(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: KullaniciService = Depends(_servis)
) -> KullaniciProfilYaniti:
    """"Limitsiz devam et": Katman 1'in önerisini gerçek limite dönüştürmeden düşürür."""
    profil = await servis.oneriyi_reddet(kullanici_id)
    return _yanita_cevir(profil)


@router.get("/tercihler", response_model=TercihlerYaniti)
async def tercihleri_getir(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: KullaniciService = Depends(_servis)
) -> TercihlerYaniti:
    """E-19 Ayarlar: bildirim/gün sınırı/varsayılan ödeme/kurulum günü tercihlerini döner."""
    profil = await servis.profili_getir(kullanici_id)
    return _tercihlere_cevir(profil)


@router.patch("/tercihler", response_model=TercihlerYaniti)
async def tercihleri_guncelle(
    istek: TercihlerGuncellemeIstegi,
    kullanici_id: str = Depends(gecerli_kullanici_id),
    servis: KullaniciService = Depends(_servis),
) -> TercihlerYaniti:
    """E-19 Ayarlar: yalnız gönderilen tercih alanları güncellenir (kısmi güncelleme)."""
    alanlar = {alan: getattr(istek, alan) for alan in istek.model_fields_set}
    profil = await servis.tercihleri_guncelle(kullanici_id, alanlar)
    return _tercihlere_cevir(profil)
