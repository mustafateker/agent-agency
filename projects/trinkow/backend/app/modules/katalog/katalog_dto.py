"""
Katalog modülünün dışarıya açtığı yanıt sözleşmesi.

Yazma isteği DTO'su bilerek YOK: bu turda katalog yalnız sunucudan
istemciye tek yönlü akar (tohumlama dışında hiçbir uç nokta kalem
eklemez/değiştirmez — görev kapsamı budur).

Kategori kodu `harcama_dto.py`deki gerekçeyle aynı sebepten `str` bırakıldı:
kategori kataloğunu burada `Literal` ile sabitlemek modüller arası gizli
bağ kurar.
"""
from __future__ import annotations

from pydantic import BaseModel


class KatalogOgesiYaniti(BaseModel):
    kod: str
    ad: str
    kategori: str


class KatalogListesiYaniti(BaseModel):
    """`surum`, kataloğun o anki içeriğinden türetilmiş bir özettir (ETag ile aynı değer).

    İstemci daha önce gördüğü `surum`ü sakladıysa ve değişmediyse yeniden
    indirmeyi atlayabilir; sunucu ayrıca standart HTTP `ETag`/`If-None-Match`
    ile 304 de döner (bkz. katalog_controller.py).
    """

    ogeler: list[KatalogOgesiYaniti]
    surum: str
