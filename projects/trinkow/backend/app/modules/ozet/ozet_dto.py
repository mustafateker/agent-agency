"""
`ozet` modülünün dışarıya açtığı yanıt sözleşmesi (yalnız GET — bu modül
veri YAZMAZ, bkz. ozet_model.py).

Alan adları istemcinin bugün SQLite'tan okuduğu şekillerle (`db/seri.ts`
`GunSeriBilgisi`/`SeriDurumu`, `db/usePano.ts` `PanoVerisi`, `db/harcama.ts`
`KategoriDurumu`, `db/ozet.ts` `GunToplami`/`KategoriPayi`/
`KucukHarcamaOzeti`) mümkün olduğunca birebir eşleşecek şekilde (snake_case
çevirisiyle) seçildi — istemci bu API'ye bağlanırken isim uyuşmazlığı
bağlama turunu iki katına çıkarır (görev notu).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

LimitDurumu = Literal["altinda", "asimda", "tanimsiz"]
IzgaraDurumu = Literal["altinda", "disinda", "bos"]


class PanoKategoriDurumuYaniti(BaseModel):
    kategori: str
    limit_kurus: int
    # Ay toplamı (K-056: kart satırının birincil ölçeği daima aylık).
    harcanan_kurus: int
    bugun_kurus: int


class GunSeriBilgisiYaniti(BaseModel):
    harcanan_kurus: int
    kayit_adedi: int
    harcamasiz_isaretli: bool
    # Limit tanımsızsa (limitsiz kip) `None` — seri hiç değerlendirilmez.
    seriye_sayildi_mi: bool | None


class GunlukPanoYaniti(BaseModel):
    """E-10 günlük pano."""

    gun: str
    niyet: str
    limit_kurus: int | None
    harcanan_kurus: int
    kayit_adedi: int
    limit_durumu: LimitDurumu
    kategoriler: list[PanoKategoriDurumuYaniti]
    ay_asimi: int
    seri: GunSeriBilgisiYaniti
    ilk_gun_mu: bool


class KategoriPayiYaniti(BaseModel):
    kategori: str
    toplam_kurus: int
    # Tam sayı, largest-remainder ile 100'e tamamlanır (Float YASAK kuralı).
    yuzde: int


class KucukHarcamaOzetiYaniti(BaseModel):
    esik_kurus: int
    adet: int
    toplam_kurus: int


class OzetYaniti(BaseModel):
    """E-16 dönemsel (haftalık/aylık) özet — dönem çağıran tarafından `baslangic_gun`/`bitis_gun` ile seçilir."""

    baslangic_gun: str
    bitis_gun: str
    toplam_kurus: int
    kategori_dagilimi: list[KategoriPayiYaniti]
    en_cok_harcanan_kategoriler: list[str]
    kucuk_harcama: KucukHarcamaOzetiYaniti


class KategoriSeyriGunuYaniti(BaseModel):
    gun: str
    toplam_kurus: int


class KategoriDetayYaniti(BaseModel):
    """E-15 kategori detayı — kayıt LİSTESİ için `GET /harcama/?kategori=` kullanılır (Madde 3 notu)."""

    kategori: str
    baslangic_gun: str
    bitis_gun: str
    toplam_kurus: int
    gun_bazinda_seyir: list[KategoriSeyriGunuYaniti]


class GunIzgaraHucresiYaniti(BaseModel):
    gun: str
    durum: IzgaraDurumu


class SeriYaniti(BaseModel):
    """E-21 seri ekranı — mevcut seri, en uzun seri, son 30 günün ızgarası, milestone durumu."""

    mevcut_seri: int
    en_uzun_seri: int
    en_uzun_seri_bitis_gunu: str | None
    # Limitsiz kipte True (K-048: "limitsiz kipte seri kapalıdır").
    kapali: bool
    kirildi_mi: bool
    sonraki_durak: int | None
    onceki_durak: int
    kalan_gun: int | None
    aralik_yuzde: float
    gecilen_milestoneler: list[int]
    izgara: list[GunIzgaraHucresiYaniti]
