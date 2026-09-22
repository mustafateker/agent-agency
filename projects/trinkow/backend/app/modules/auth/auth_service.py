"""
Auth iş mantığı: kayıt, giriş, token yenileme, oturum kapatma,
"ben kimim" ve hesap silme.

HTTP'den habersizdir — controller bu fonksiyonları çağırıp sonucu HTTP
yanıtına çevirir. Mongo erişimi burada yapılır, bağlantı `app.core`dan
gelir (K-068/3: repository katmanı yok).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.errors import (
    EpostaZatenKayitli,
    GecersizKimlikBilgisi,
    GecersizToken,
    KullaniciBulunamadi,
    TokenSuresiDolmus,
)
from app.core.security import (
    erisim_tokeni_olustur,
    sifre_dogrula,
    sifre_hashle,
    token_coz,
    yenileme_tokeni_olustur,
)
from app.modules.auth.auth_model import KullaniciBelgesi
from app.modules.harcama.harcama_service import HarcamaService
from app.modules.kullanici.kullanici_service import KullaniciService

KULLANICILAR_KOLEKSIYONU = "kullanicilar"
YENILEME_TOKENLARI_KOLEKSIYONU = "yenileme_tokenlari"


def erisim_tokenini_dogrula(erisim_tokeni: str) -> str:
    """Erişim token'ını doğrular ve içindeki kullanıcı kimliğini döndürür.

    Veritabanına ihtiyaç duymaz; "ben kimim" gibi uç noktalarda FastAPI
    bağımlılığı (dependency) olarak controller katmanından çağrılır.
    """
    yuk = _token_coz_ve_hataya_cevir(erisim_tokeni)
    if yuk.get("tur") != "erisim":
        raise GecersizToken()
    return yuk["sub"]


def _token_coz_ve_hataya_cevir(token: str) -> dict[str, Any]:
    try:
        return token_coz(token)
    except jwt.ExpiredSignatureError as hata:
        raise TokenSuresiDolmus() from hata
    except jwt.InvalidTokenError as hata:
        raise GecersizToken() from hata


def _object_id_cevir(kullanici_id: str) -> ObjectId:
    try:
        return ObjectId(kullanici_id)
    except InvalidId as hata:
        raise GecersizToken() from hata


class AuthService:
    """Kullanıcı kimlik doğrulama işlemlerini yürütür."""

    def __init__(
        self,
        veritabani: AsyncIOMotorDatabase,
        harcama_servisi: HarcamaService | None = None,
        kullanici_servisi: KullaniciService | None = None,
    ) -> None:
        self._kullanicilar = veritabani[KULLANICILAR_KOLEKSIYONU]
        self._yenileme_tokenlari = veritabani[YENILEME_TOKENLARI_KOLEKSIYONU]
        # Madde 1 (K-085/BE-4b) — hesap silinirken diğer modüllerin verisini de
        # silmek için servis arayüzleri (Kural 1: doğrudan koleksiyon erişimi
        # yok). Enjekte edilmezse kendi üretir — var olan
        # `AuthService(get_database())` çağrıları kırılmaz.
        self._harcama = harcama_servisi or HarcamaService(veritabani)
        self._kullanici = kullanici_servisi or KullaniciService(veritabani)

    async def kayit_ol(self, email: str, duz_sifre: str) -> tuple[str, str]:
        """Yeni kullanıcı oluşturur ve doğrudan oturum açtırır (token çifti döner).

        E-posta benzersizliği Mongo unique index ile garanti edilir; bu
        `find_one` kontrolü yalnız daha okunur bir hata mesajı için,
        yarış durumunda index zaten ikinci kaydı reddeder.
        """
        mevcut = await self._kullanicilar.find_one({"email": email})
        if mevcut is not None:
            raise EpostaZatenKayitli()

        kullanici = KullaniciBelgesi(email=email, sifre_hash=sifre_hashle(duz_sifre))
        ekleme_sonucu = await self._kullanicilar.insert_one(kullanici.belgeye_cevir())
        return await self._token_cifti_uret(str(ekleme_sonucu.inserted_id))

    async def giris_yap(self, email: str, duz_sifre: str) -> tuple[str, str]:
        """E-posta/şifre doğrularsa token çifti döner.

        Hatalıysa **genel** hata verir: e-posta mı şifre mi yanlış olduğu
        sızdırılmaz (hesap sayımı saldırısına karşı, bkz. metinler.md § E-22).
        """
        belge = await self._kullanicilar.find_one({"email": email})
        if belge is None or belge.get("sifre_hash") is None:
            raise GecersizKimlikBilgisi()

        if not sifre_dogrula(duz_sifre, belge["sifre_hash"]):
            raise GecersizKimlikBilgisi()

        return await self._token_cifti_uret(str(belge["_id"]))

    async def token_yenile(self, yenileme_tokeni: str) -> str:
        """Geçerli ve iptal edilmemiş bir yenileme token'ı ile yeni erişim token'ı üretir."""
        yuk = self._yenileme_tokenini_dogrula(yenileme_tokeni)
        kayit = await self._yenileme_tokenlari.find_one({"jti": yuk["jti"]})
        if kayit is None or kayit.get("iptal_edildi_mi", False):
            raise GecersizToken()

        return erisim_tokeni_olustur(yuk["sub"])

    async def oturum_kapat(self, yenileme_tokeni: str) -> None:
        """Verilen yenileme token'ını iptal ederek oturumu geçersiz kılar."""
        yuk = self._yenileme_tokenini_dogrula(yenileme_tokeni)
        await self._yenileme_tokenlari.update_one({"jti": yuk["jti"]}, {"$set": {"iptal_edildi_mi": True}})

    async def kullaniciyi_getir(self, kullanici_id: str) -> KullaniciBelgesi:
        """Erişim token'ındaki kimlikten kullanıcı belgesini getirir ("ben kimim")."""
        belge = await self._kullanicilar.find_one({"_id": _object_id_cevir(kullanici_id)})
        if belge is None:
            raise KullaniciBulunamadi()
        return KullaniciBelgesi.belgeden_olustur(belge)

    async def hesabi_sil(self, kullanici_id: str) -> None:
        """Kullanıcıya ait TÜM veriyi geri alınamaz biçimde siler (K-057 App
        Store zorunluluğu + K-085 Madde 1 — veri koruma mevzuatı).

        SIRA ÖNEMLİ: Mongo'da tek-belge işlemi (transaction) YOK, bu yüzden
        önce diğer modüllerin verisi, EN SON kimlik kaydı (`kullanicilar`)
        silinir. Böylece işlem yarıda kesilirse (ör. süreç çöker, ağ
        koparsa) kullanıcı hâlâ giriş yapabilir ve silme işlemini TEKRAR
        deneyebilir — kimlik önce silinseydi bu imkânsız olurdu (401,
        kurtarılamaz yarım durum). Alt adımlar (`delete_many`/`delete_one`)
        eşleşme bulamasa da hata vermediği için idempotenttir; tekrar
        çağrıldığında zaten silinmiş kısımlar sessizce atlanır.
        """
        if await self._kullanicilar.find_one({"_id": _object_id_cevir(kullanici_id)}, {"_id": 1}) is None:
            raise KullaniciBulunamadi()

        # 1) Diğer modüllerin verisi (servis arayüzü üzerinden, Kural 1).
        await self._harcama.kullanici_verisini_sil(kullanici_id)
        await self._kullanici.kullanici_verisini_sil(kullanici_id)

        # 2) Kimlik EN SON: önce oturumlar (yenileme token'ları) iptal edilir
        #    ki silinmiş bir kullanıcı adına yeni erişim token'ı üretilemesin,
        #    ardından kullanıcı kaydının kendisi silinir.
        await self._yenileme_tokenlari.delete_many({"kullanici_id": kullanici_id})
        await self._kullanicilar.delete_one({"_id": _object_id_cevir(kullanici_id)})

    async def _token_cifti_uret(self, kullanici_id: str) -> tuple[str, str]:
        erisim = erisim_tokeni_olustur(kullanici_id)
        yenileme, jti = yenileme_tokeni_olustur(kullanici_id)
        yenileme_omru_gun = get_settings().yenileme_token_gun
        await self._yenileme_tokenlari.insert_one(
            {
                "jti": jti,
                "kullanici_id": kullanici_id,
                "olusturulma_tarihi": datetime.now(timezone.utc),
                "son_kullanma_tarihi": datetime.now(timezone.utc) + timedelta(days=yenileme_omru_gun),
                "iptal_edildi_mi": False,
            }
        )
        return erisim, yenileme

    def _yenileme_tokenini_dogrula(self, yenileme_tokeni: str) -> dict[str, Any]:
        yuk = _token_coz_ve_hataya_cevir(yenileme_tokeni)
        if yuk.get("tur") != "yenileme" or "jti" not in yuk:
            raise GecersizToken()
        return yuk
