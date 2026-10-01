"""
Mongo `katalog_ogeleri` koleksiyonundaki tek bir ürün kataloğu belgesi.

DTO'dan (katalog_dto.py) bilerek ayrı tutulur (K-068/3, harcama_model.py ile
aynı ilke). `kod`, istemcideki `app/src/content/urunKatalogu.ts#id` alanının
karşılığıdır — Mongo'nun kendi `_id`sini DEĞİL, bu kararlı metin anahtarını
kullanmak tohumlamayı ve tek kalem okumayı basitleştirir (ObjectId çeviren
bir aracı katmana gerek kalmaz).

BAĞLAYICI (K-050 · K-037, görev notu): şemada fiyat, marka adı, fotoğraf/
logo, miktar/adet/birim alanı YOKTUR ve eklenmeyecektir — katalog yalnız
"ne alındığını" isimlendirir.
"""
from __future__ import annotations

from typing import Any


class KatalogOgesiBelgesi:
    """Bir ürün kataloğu kalemi: jenerik ürün adı + bağlı olduğu kategori.

    `sira`, istemcideki kaynak listenin (kategoriye göre gruplanmış) sırasını
    korur — sunucu bu sırayla döner ki istemci tarafında grup gösterimi
    kaynaktakiyle aynı kalsın.
    """

    def __init__(
        self,
        kod: str,
        ad: str,
        kategori: str,
        sira: int,
        _id: Any = None,
    ) -> None:
        self.id = _id
        self.kod = kod
        self.ad = ad
        self.kategori = kategori
        self.sira = sira

    def belgeye_cevir(self) -> dict[str, Any]:
        """Mongo'ya yazılacak sözlük gösterimini üretir."""
        return {"kod": self.kod, "ad": self.ad, "kategori": self.kategori, "sira": self.sira}

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "KatalogOgesiBelgesi":
        """Mongo'dan okunan sözlüğü nesneye çevirir."""
        return KatalogOgesiBelgesi(
            _id=belge.get("_id"),
            kod=belge["kod"],
            ad=belge["ad"],
            kategori=belge["kategori"],
            sira=belge.get("sira", 0),
        )
