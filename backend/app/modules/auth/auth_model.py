"""
Mongo `kullanicilar` koleksiyonunda saklanan belgenin şeması.

DTO'dan (auth_dto.py) bilerek ayrı tutulur: burası içeride saklanan hâl,
DTO dışarıya açılan sözleşmedir — biri değişince diğeri otomatik kırılmaz
(K-068/3). `kimlik_saglayici` alanı, sonradan Google/Apple girişi
eklenebilsin diye şimdiden var; bu turda yalnız "eposta" değeri üretilir.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

KimlikSaglayici = Literal["eposta", "google", "apple", "demo"]


class KullaniciBelgesi:
    """Mongo `kullanicilar` koleksiyonundaki bir belgeyi Python nesnesine çevirir."""

    def __init__(
        self,
        email: str,
        sifre_hash: str | None,
        kimlik_saglayici: KimlikSaglayici = "eposta",
        _id: Any = None,
        olusturulma_tarihi: datetime | None = None,
    ) -> None:
        self.id = _id
        self.email = email
        self.sifre_hash = sifre_hash
        self.kimlik_saglayici = kimlik_saglayici
        self.olusturulma_tarihi = olusturulma_tarihi or datetime.now(timezone.utc)

    def belgeye_cevir(self) -> dict[str, Any]:
        """Mongo'ya yazılacak sözlük gösterimini üretir."""
        return {
            "email": self.email,
            "sifre_hash": self.sifre_hash,
            "kimlik_saglayici": self.kimlik_saglayici,
            "olusturulma_tarihi": self.olusturulma_tarihi,
        }

    @staticmethod
    def belgeden_olustur(belge: dict[str, Any]) -> "KullaniciBelgesi":
        """Mongo'dan okunan sözlüğü nesneye çevirir."""
        return KullaniciBelgesi(
            _id=belge["_id"],
            email=belge["email"],
            sifre_hash=belge.get("sifre_hash"),
            kimlik_saglayici=belge.get("kimlik_saglayici", "eposta"),
            olusturulma_tarihi=belge.get("olusturulma_tarihi"),
        )
