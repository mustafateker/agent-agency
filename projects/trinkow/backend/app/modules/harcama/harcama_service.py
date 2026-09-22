"""
Harcama iş mantığı: kayıt ekleme/güncelleme/silme, sayfalanmış listeleme,
taksit serisi silme, gün durumu (K-048 hile kapısı), kategori limitleri,
limit geçmişi (K-064/1) ve ürün→kategori öğrenmesi (F-18).

HTTP'den habersizdir — controller bu fonksiyonları çağırıp sonucu HTTP
yanıtına çevirir (kullanici_service.py ile aynı desen, K-068/3). Her sorgu
`kullanici_id` ile filtrelenir; kullanıcı yalnız KENDİ verisine erişebilir
(Madde 2) — başka kullanıcının kaydına erişimin yapısal bir yolu yoktur.
"""
from __future__ import annotations

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.errors import (
    HarcamaBulunamadi,
    TaksitliKayitTekBasinaSilinemez,
    TaksitliKayitTutariDegistirilemez,
)
from app.modules.harcama.harcama_model import (
    GunDurumuBelgesi,
    HarcamaBelgesi,
    KategoriLimitiBelgesi,
    LimitGecmisiBelgesi,
    UrunKategoriOgrenmeBelgesi,
)

HARCAMALAR_KOLEKSIYONU = "harcamalar"
KATEGORI_LIMITLERI_KOLEKSIYONU = "kategori_limitleri"
GUN_DURUMLARI_KOLEKSIYONU = "gun_durumlari"
LIMIT_GECMISLERI_KOLEKSIYONU = "limit_gecmisleri"
URUN_KATEGORI_OGRENMELERI_KOLEKSIYONU = "urun_kategori_ogrenmeleri"

VARSAYILAN_SAYFA_BOYUTU = 50
AZAMI_SAYFA_BOYUTU = 200

# İstemcinin `lib/urunArama.ts#turkceNormalize` fonksiyonuyla BİREBİR aynı
# kural — iki tarafın da aynı ürün için aynı anahtarı üretmesi gerekiyor.
_TURKCE_KUCUK_HARF = str.maketrans("İIŞÇĞÜÖ", "iışçğüö")
_KARAKTER_DONUSUMU = str.maketrans({"ı": "i", "ş": "s", "ç": "c", "ğ": "g", "ü": "u", "ö": "o"})


def _turkce_normalize(metin: str) -> str:
    """Türkçe karakterleri sadeleştirir + küçük harfe çevirir (arama/öğrenme anahtarı)."""
    kucuk = metin.translate(_TURKCE_KUCUK_HARF).lower()
    return kucuk.translate(_KARAKTER_DONUSUMU).strip()


def _nesne_kimligi(harcama_id: str) -> ObjectId:
    """`harcama_id`yi Mongo ObjectId'sine çevirir; biçimi bozuksa "bulunamadı" sayılır (bilgi sızdırmaz)."""
    try:
        return ObjectId(harcama_id)
    except (InvalidId, TypeError, ValueError) as hata:
        raise HarcamaBulunamadi() from hata


class HarcamaService:
    """Harcama kayıtları ve ilişkili tabloların (limit/gün durumu/öğrenme) işlemlerini yürütür."""

    def __init__(self, veritabani: AsyncIOMotorDatabase) -> None:
        self._harcamalar = veritabani[HARCAMALAR_KOLEKSIYONU]
        self._kategori_limitleri = veritabani[KATEGORI_LIMITLERI_KOLEKSIYONU]
        self._gun_durumlari = veritabani[GUN_DURUMLARI_KOLEKSIYONU]
        self._limit_gecmisleri = veritabani[LIMIT_GECMISLERI_KOLEKSIYONU]
        self._urun_kategori_ogrenmeleri = veritabani[URUN_KATEGORI_OGRENMELERI_KOLEKSIYONU]

    async def en_eski_kayit_gunu(self, kullanici_id: str) -> str | None:
        """Madde 2 (K-077/BE-5b) — kullanıcının İLK harcama kaydının günü.

        `ozet` seri sınırını (K-049) yalnız `kurulum_gunu` ile değil, bu
        değerle de karşılaştırır (istemcideki `db/harcama.ts#ilkKayitGunu` +
        `db/seri.ts#ilkSinirGunu` ile aynı sözleşme). Hiç kayıt yoksa `None`
        döner — çağıran bu durumda yalnız `kurulum_gunu`na düşer.
        """
        belge = await self._harcamalar.find_one({"kullanici_id": kullanici_id}, sort=[("gun", 1)])
        return belge["gun"] if belge is not None else None

    async def kullanici_verisini_sil(self, kullanici_id: str) -> None:
        """Madde 1 + Madde 3 (K-085/BE-4b) — bu modülün sahip olduğu TÜM
        koleksiyonlardan kullanıcıya ait veriyi siler: harcamalar, kategori
        limitleri, gün durumları, limit geçmişi, ürün-kategori öğrenmesi.

        İki çağıran var: `AuthService.hesabi_sil` (hesap TAMAMEN silinirken,
        Madde 1 — Kural 1 gereği `auth` bu koleksiyonlara doğrudan sorgu
        atmaz, bu servis arayüzünden geçer) ve bu modülün kendi
        `DELETE /harcama/ayar/tum-veriler` ucu (hesap/profil KALIR, yalnız
        veri sıfırlanır, Madde 3). `delete_many` eşleşme olmasa da hata
        vermediği için idempotenttir — Madde 1'de kısmi silme sonrası
        yeniden denemede güvenlidir.
        """
        await self._harcamalar.delete_many({"kullanici_id": kullanici_id})
        await self._kategori_limitleri.delete_many({"kullanici_id": kullanici_id})
        await self._gun_durumlari.delete_many({"kullanici_id": kullanici_id})
        await self._limit_gecmisleri.delete_many({"kullanici_id": kullanici_id})
        await self._urun_kategori_ogrenmeleri.delete_many({"kullanici_id": kullanici_id})

    # ------------------------------------------------------------------ harcama

    async def harcama_ekle(
        self,
        kullanici_id: str,
        tutar_kurus: int,
        kategori: str,
        zaman: str,
        gun: str,
        odeme: str,
        urun_adi: str | None = None,
        not_metni: str | None = None,
        taksit_id: str | None = None,
        taksit_no: int | None = None,
        taksit_toplam: int | None = None,
    ) -> HarcamaBelgesi:
        """Tek bir harcama satırı ekler; ürün adı verilmişse öğrenme tablosunu da günceller (F-18)."""
        belge = HarcamaBelgesi(
            kullanici_id=kullanici_id,
            tutar_kurus=tutar_kurus,
            kategori=kategori,
            urun_adi=urun_adi,
            zaman=zaman,
            gun=gun,
            odeme=odeme,  # type: ignore[arg-type]
            not_metni=not_metni,
            taksit_id=taksit_id,
            taksit_no=taksit_no,
            taksit_toplam=taksit_toplam,
        )
        sonuc = await self._harcamalar.insert_one(belge.belgeye_cevir())
        belge.id = sonuc.inserted_id

        if urun_adi:
            await self.urun_kategori_ogren(kullanici_id, urun_adi, kategori)

        return belge

    async def harcama_getir(self, kullanici_id: str, harcama_id: str) -> HarcamaBelgesi:
        """Tek kayıt okur (E-12 detay ekranı); bulunamazsa/başka kullanıcıya aitse `HarcamaBulunamadi`."""
        belge = await self._harcamalar.find_one({"_id": _nesne_kimligi(harcama_id), "kullanici_id": kullanici_id})
        if belge is None:
            raise HarcamaBulunamadi()
        return HarcamaBelgesi.belgeden_olustur(belge)

    async def harcamalari_listele(
        self,
        kullanici_id: str,
        gun: str | None = None,
        baslangic_gun: str | None = None,
        bitis_gun: str | None = None,
        kategori: str | None = None,
        sayfa: int = 1,
        sayfa_boyutu: int = VARSAYILAN_SAYFA_BOYUTU,
    ) -> tuple[list[HarcamaBelgesi], int]:
        """Gün / tarih aralığı / kategori süzgeciyle sayfalanmış listeleme (300+ günlük geçmiş senaryosu).

        `gun` verilirse tek günün kayıtları (eski→yeni, tarih sırasıyla);
        aralık/kategori süzgeciyle çağrılırsa en yeni kayıt önce döner —
        geçmiş taraması bu şekilde en son harcamadan geriye gider.
        """
        sayfa = max(1, sayfa)
        sayfa_boyutu = min(max(1, sayfa_boyutu), AZAMI_SAYFA_BOYUTU)

        sorgu: dict[str, object] = {"kullanici_id": kullanici_id}
        if gun is not None:
            sorgu["gun"] = gun
        elif baslangic_gun is not None or bitis_gun is not None:
            aralik: dict[str, str] = {}
            if baslangic_gun is not None:
                aralik["$gte"] = baslangic_gun
            if bitis_gun is not None:
                aralik["$lte"] = bitis_gun
            sorgu["gun"] = aralik
        if kategori is not None:
            sorgu["kategori"] = kategori

        toplam_kayit = await self._harcamalar.count_documents(sorgu)
        siralama = [("gun", 1), ("zaman", 1)] if gun is not None else [("gun", -1), ("zaman", -1)]
        imlec = (
            self._harcamalar.find(sorgu)
            .sort(siralama)
            .skip((sayfa - 1) * sayfa_boyutu)
            .limit(sayfa_boyutu)
        )
        belgeler = [HarcamaBelgesi.belgeden_olustur(satir) async for satir in imlec]
        return belgeler, toplam_kayit

    async def harcama_guncelle(self, kullanici_id: str, harcama_id: str, alanlar: dict[str, object]) -> HarcamaBelgesi:
        """E-12 "Kaydet" — yalnız gönderilen alanları günceller.

        Taksitli bir kayıtta `tutar_kurus` gönderilirse reddedilir (Madde 2) —
        seri toplamıyla tutarsızlaşmaması için mevcut kayıt önce okunur.
        """
        mevcut = await self.harcama_getir(kullanici_id, harcama_id)
        if "tutar_kurus" in alanlar and mevcut.taksitli_mi:
            raise TaksitliKayitTutariDegistirilemez()

        if not alanlar:
            return mevcut

        await self._harcamalar.update_one(
            {"_id": _nesne_kimligi(harcama_id), "kullanici_id": kullanici_id}, {"$set": alanlar}
        )
        return await self.harcama_getir(kullanici_id, harcama_id)

    async def harcama_sil(self, kullanici_id: str, harcama_id: str) -> None:
        """Kalıcı silme (K-029: istemci 6 sn "geri al" toast'ını KENDİ tarafında bekletir,
        sunucu geri alınabilir bir "işaretle" durumu tutmaz — bkz. görev notu).

        Taksitli bir kayıt tek başına silinemez (Madde 2); seri
        `taksit_serisi_sil` ile bütün olarak silinmelidir.
        """
        mevcut = await self.harcama_getir(kullanici_id, harcama_id)
        if mevcut.taksitli_mi:
            raise TaksitliKayitTekBasinaSilinemez()
        await self._harcamalar.delete_one({"_id": _nesne_kimligi(harcama_id), "kullanici_id": kullanici_id})

    async def taksit_serisi_sil(self, kullanici_id: str, taksit_id: str) -> int:
        """E-13 — aynı `taksit_id`ye sahip TÜM satırları siler (K-029: onaylıdır, geri alma yoktur)."""
        sonuc = await self._harcamalar.delete_many({"kullanici_id": kullanici_id, "taksit_id": taksit_id})
        if sonuc.deleted_count == 0:
            raise HarcamaBulunamadi()
        return sonuc.deleted_count

    # ------------------------------------------------------------- gün durumu

    async def gun_durumu_isaretle(self, kullanici_id: str, gun: str, harcamasiz: bool) -> GunDurumuBelgesi:
        """K-048 hile kapısı (b) — bir günü "harcamasız" işaretler/kaldırır."""
        await self._gun_durumlari.update_one(
            {"kullanici_id": kullanici_id, "gun": gun},
            {"$set": {"kullanici_id": kullanici_id, "gun": gun, "harcamasiz": harcamasiz}},
            upsert=True,
        )
        return GunDurumuBelgesi(kullanici_id=kullanici_id, gun=gun, harcamasiz=harcamasiz)

    async def gun_durumu_getir(self, kullanici_id: str, gun: str) -> GunDurumuBelgesi:
        """Bir günün durumu; hiç işaretlenmemişse `harcamasiz=False` varsayılan döner."""
        belge = await self._gun_durumlari.find_one({"kullanici_id": kullanici_id, "gun": gun})
        if belge is None:
            return GunDurumuBelgesi(kullanici_id=kullanici_id, gun=gun, harcamasiz=False)
        return GunDurumuBelgesi.belgeden_olustur(belge)

    # --------------------------------------------------------- kategori limiti

    async def kategori_limitlerini_getir(self, kullanici_id: str) -> list[KategoriLimitiBelgesi]:
        """Yalnız değeri OLAN kategori limitlerini `sira`ya göre döner (istemcideki `tumKategoriLimitleri`)."""
        imlec = self._kategori_limitleri.find({"kullanici_id": kullanici_id}).sort("sira", 1)
        return [KategoriLimitiBelgesi.belgeden_olustur(satir) async for satir in imlec]

    async def kategori_limiti_yaz(
        self, kullanici_id: str, kategori: str, limit_kurus: int, sira: int
    ) -> KategoriLimitiBelgesi:
        """Kategori limiti yaz/güncelle — `(kullanici_id, kategori)` üstünde upsert."""
        await self._kategori_limitleri.update_one(
            {"kullanici_id": kullanici_id, "kategori": kategori},
            {"$set": {"kullanici_id": kullanici_id, "kategori": kategori, "limit_kurus": limit_kurus, "sira": sira}},
            upsert=True,
        )
        return KategoriLimitiBelgesi(kullanici_id=kullanici_id, kategori=kategori, limit_kurus=limit_kurus, sira=sira)

    async def kategori_limiti_sil(self, kullanici_id: str, kategori: str) -> None:
        """Madde 2 (K-085/BE-4b) — bir kategorinin limitini kaldırır.

        `PUT`in `limit_kurus > 0` zorunluluğu "limiti sil"i temsil edemiyordu;
        silme ayrı bir eylem. İdempotent: kategori için hiç limit yoksa da
        sessizce başarılı sayılır (DELETE'in doğal semantiği).
        """
        await self._kategori_limitleri.delete_one({"kullanici_id": kullanici_id, "kategori": kategori})

    # ---------------------------------------------------------- limit geçmişi

    async def limit_gecmisi_yaz(self, kullanici_id: str, yururluk_tarihi: str, kurus: int) -> LimitGecmisiBelgesi:
        """K-064/1 — günlük limit her değiştiğinde bir satır düşer.

        `(kullanici_id, yururluk_tarihi)` üstünde upsert: aynı günde birden
        çok değişiklik olursa o günün yürürlükteki değeri son yazılanla
        değiştirilir (istemciyle aynı kural — `INSERT OR REPLACE`).
        """
        await self._limit_gecmisleri.update_one(
            {"kullanici_id": kullanici_id, "yururluk_tarihi": yururluk_tarihi},
            {"$set": {"kullanici_id": kullanici_id, "yururluk_tarihi": yururluk_tarihi, "kurus": kurus}},
            upsert=True,
        )
        return LimitGecmisiBelgesi(kullanici_id=kullanici_id, yururluk_tarihi=yururluk_tarihi, kurus=kurus)

    async def limit_gecmisi_efektif_limit(self, kullanici_id: str, gun: str, guncel_limit_kurus: int) -> int:
        """K-064/1 — bir günün YÜRÜRLÜKTEKİ limiti (istemcideki `efektifLimitKurus`).

        O güne kadarki (dahil) en son değişikliği arar; hiç kayıt yoksa
        (göçten önceki günler) güncel limit "en iyi tahmin" olarak kullanılır
        — geçmiş değer icat edilmez, yalnız bilinen en yakın değer geriye
        doğru uzatılır.
        """
        satir = await self._limit_gecmisleri.find_one(
            {"kullanici_id": kullanici_id, "yururluk_tarihi": {"$lte": gun}},
            sort=[("yururluk_tarihi", -1)],
        )
        return satir["kurus"] if satir is not None else guncel_limit_kurus

    async def limit_gecmisi_araligi_getir(self, kullanici_id: str, bitis_gun: str) -> list[LimitGecmisiBelgesi]:
        """Madde 3 (K-077/BE-5b) — `bitis_gun` dahil TÜM limit değişiklik geçmişini
        TEK sorguda, ARTAN `yururluk_tarihi` sırasıyla döner.

        Seri hesabı (300+ günlük geçmiş) `limit_gecmisi_efektif_limit`i her
        gün için ayrı ayrı çağırmak yerine bunu bir kez çeker ve bellekte
        gün gün çözer (istemcideki `db/seri.ts#limitGecmisi` +
        `gunlukLimitCozucuOlustur` ile aynı sözleşme) — davranış aynı kalır,
        yalnız Mongo sorgu sayısı O(gün)'den O(1)'e düşer.
        """
        imlec = self._limit_gecmisleri.find(
            {"kullanici_id": kullanici_id, "yururluk_tarihi": {"$lte": bitis_gun}}
        ).sort("yururluk_tarihi", 1)
        return [LimitGecmisiBelgesi.belgeden_olustur(satir) async for satir in imlec]

    # ------------------------------------------------------ ürün-kategori öğrenme

    async def urun_kategori_ogren(self, kullanici_id: str, urun_adi: str, kategori: str) -> UrunKategoriOgrenmeBelgesi | None:
        """O ürün adı için son seçilen kategoriyi kalıcılaştırır (F-18); boş anahtar sessizce yok sayılır."""
        anahtar = _turkce_normalize(urun_adi)
        if not anahtar:
            return None
        await self._urun_kategori_ogrenmeleri.update_one(
            {"kullanici_id": kullanici_id, "urun_anahtari": anahtar},
            {"$set": {"kullanici_id": kullanici_id, "urun_anahtari": anahtar, "kategori": kategori}},
            upsert=True,
        )
        return UrunKategoriOgrenmeBelgesi(kullanici_id=kullanici_id, urun_anahtari=anahtar, kategori=kategori)

    async def urun_kategori_ogrenmelerini_getir(self, kullanici_id: str) -> list[UrunKategoriOgrenmeBelgesi]:
        """Tüm öğrenilmiş eşlemeler — arama ekranı bir kerede yükler (istemcideki `tumOgrenilenKategoriler`)."""
        imlec = self._urun_kategori_ogrenmeleri.find({"kullanici_id": kullanici_id})
        return [UrunKategoriOgrenmeBelgesi.belgeden_olustur(satir) async for satir in imlec]
