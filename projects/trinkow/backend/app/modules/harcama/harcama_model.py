"""
Mongo'da harcama modülünün beş koleksiyonunda saklanan belge şemaları:
`harcamalar` · `kategori_limitleri` · `gun_durumlari` · `limit_gecmisleri` ·
`urun_kategori_ogrenmeleri`.

DTO'dan (harcama_dto.py) bilerek ayrı tutulur (K-068/3). Alan adları
istemcideki `app/src/db/semasi.ts` (şema sürümü 5) ve `db/harcama.ts` ·
`db/limitler.ts` · `db/seri.ts` · `db/urunKategori.ts` dosyalarındaki
karşılıklarıyla BİREBİR eşleşecek şekilde seçildi (yalnız `kullanici_id`
sunucuya özgü bir eklemedir — istemcide tek kullanıcı vardı, sunucuda çok
kullanıcı olduğu için satırlar bununla ayrıştırılır).
"""
from __future__ import annotations

from typing import Any, Literal

OdemeTipi = Literal["nakit", "kart"]


class HarcamaBelgesi:
    """Mongo `harcamalar` koleksiyonundaki tek bir harcama kaydı.

    Taksitli bir kayıt `taksit_id` doluyken tek başına silinemez/tutarı
    değiştirilemez (bkz. harcama_service — Madde 2, K-029 ile aynı ilke).
    """

    def __init__(
        self,
        kullanici_id: str,
        tutar_kurus: int,
        kategori: str,
        zaman: str,
        gun: str,
        odeme: OdemeTipi,
        urun_adi: str | None = None,
        not_metni: str | None = None,
        taksit_id: str | None = None,
        taksit_no: int | None = None,
        taksit_toplam: int | None = None,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.tutar_kurus = tutar_kurus
        self.kategori = kategori
        self.urun_adi = urun_adi
        self.zaman = zaman
        self.gun = gun
        self.odeme = odeme
        self.not_metni = not_metni
        self.taksit_id = taksit_id
        self.taksit_no = taksit_no
        self.taksit_toplam = taksit_toplam

    @property
    def taksitli_mi(self) -> bool:
        return self.taksit_id is not None

    def belgeye_cevir(self) -> dict[str, Any]:
        """Mongo'ya yazılacak sözlük gösterimini üretir."""
        return {
            "kullanici_id": self.kullanici_id,
            "tutar_kurus": self.tutar_kurus,
            "kategori": self.kategori,
            "urun_adi": self.urun_adi,
            "zaman": self.zaman,
            "gun": self.gun,
            "odeme": self.odeme,
            "not_metni": self.not_metni,
            "taksit_id": self.taksit_id,
            "taksit_no": self.taksit_no,
            "taksit_toplam": self.taksit_toplam,
        }

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "HarcamaBelgesi":
        """Mongo'dan okunan sözlüğü nesneye çevirir."""
        return HarcamaBelgesi(
            _id=belge["_id"],
            kullanici_id=belge["kullanici_id"],
            tutar_kurus=belge["tutar_kurus"],
            kategori=belge["kategori"],
            urun_adi=belge.get("urun_adi"),
            zaman=belge["zaman"],
            gun=belge["gun"],
            odeme=belge["odeme"],
            not_metni=belge.get("not_metni"),
            taksit_id=belge.get("taksit_id"),
            taksit_no=belge.get("taksit_no"),
            taksit_toplam=belge.get("taksit_toplam"),
        )


class KategoriLimitiBelgesi:
    """Mongo `kategori_limitleri` koleksiyonundaki bir belge — bir kullanıcının bir kategorideki aylık limiti."""

    def __init__(
        self,
        kullanici_id: str,
        kategori: str,
        limit_kurus: int,
        sira: int = 0,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.kategori = kategori
        self.limit_kurus = limit_kurus
        self.sira = sira

    def belgeye_cevir(self) -> dict[str, Any]:
        return {
            "kullanici_id": self.kullanici_id,
            "kategori": self.kategori,
            "limit_kurus": self.limit_kurus,
            "sira": self.sira,
        }

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "KategoriLimitiBelgesi":
        return KategoriLimitiBelgesi(
            _id=belge.get("_id"),
            kullanici_id=belge["kullanici_id"],
            kategori=belge["kategori"],
            limit_kurus=belge["limit_kurus"],
            sira=belge.get("sira", 0),
        )


class GunDurumuBelgesi:
    """Mongo `gun_durumlari` koleksiyonundaki bir belge.

    K-048 hile kapısının (b) şıkkı — harcama satırı DEĞİLDİR, bir günün
    "harcamasız" işaretlendiğini tutar (bkz. istemci `db/seri.ts`).
    """

    def __init__(
        self,
        kullanici_id: str,
        gun: str,
        harcamasiz: bool = True,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.gun = gun
        self.harcamasiz = harcamasiz

    def belgeye_cevir(self) -> dict[str, Any]:
        return {"kullanici_id": self.kullanici_id, "gun": self.gun, "harcamasiz": self.harcamasiz}

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "GunDurumuBelgesi":
        return GunDurumuBelgesi(
            _id=belge.get("_id"),
            kullanici_id=belge["kullanici_id"],
            gun=belge["gun"],
            harcamasiz=belge.get("harcamasiz", False),
        )


class LimitGecmisiBelgesi:
    """Mongo `limit_gecmisleri` koleksiyonundaki bir belge (K-064/1).

    `yururluk_tarihi`, seri hesabının "o gün yürürlükteki limit neydi"
    sorusunu doğru cevaplayabilmesi için günlük limit her değiştiğinde bir
    satır düşer. Bu tablodan ÖNCESİ için geçmiş limit bilinmiyor — güncel
    limit geriye doğru "en iyi tahmin" olarak kullanılır (istemciyle aynı
    kural, bkz. `db/seri.ts#efektifLimitKurus`).
    """

    def __init__(
        self,
        kullanici_id: str,
        yururluk_tarihi: str,
        kurus: int,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.yururluk_tarihi = yururluk_tarihi
        self.kurus = kurus

    def belgeye_cevir(self) -> dict[str, Any]:
        return {"kullanici_id": self.kullanici_id, "yururluk_tarihi": self.yururluk_tarihi, "kurus": self.kurus}

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "LimitGecmisiBelgesi":
        return LimitGecmisiBelgesi(
            _id=belge.get("_id"),
            kullanici_id=belge["kullanici_id"],
            yururluk_tarihi=belge["yururluk_tarihi"],
            kurus=belge["kurus"],
        )


class UrunKategoriOgrenmeBelgesi:
    """Mongo `urun_kategori_ogrenmeleri` koleksiyonundaki bir belge (F-18).

    `urun_anahtari` Türkçe-normalize edilmiş üründür (bkz.
    harcama_service._turkce_normalize — istemcinin `lib/urunArama.ts#
    turkceNormalize` fonksiyonuyla birebir aynı kural).
    """

    def __init__(
        self,
        kullanici_id: str,
        urun_anahtari: str,
        kategori: str,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kullanici_id = kullanici_id
        self.urun_anahtari = urun_anahtari
        self.kategori = kategori

    def belgeye_cevir(self) -> dict[str, Any]:
        return {"kullanici_id": self.kullanici_id, "urun_anahtari": self.urun_anahtari, "kategori": self.kategori}

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "UrunKategoriOgrenmeBelgesi":
        return UrunKategoriOgrenmeBelgesi(
            _id=belge.get("_id"),
            kullanici_id=belge["kullanici_id"],
            urun_anahtari=belge["urun_anahtari"],
            kategori=belge["kategori"],
        )
