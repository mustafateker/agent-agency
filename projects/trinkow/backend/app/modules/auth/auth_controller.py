"""
Auth modülünün HTTP katmanı: yol tanımları, durum kodları, istek/yanıt
şemaları arasındaki bağlantı. İş mantığı burada YOK — hepsi
`AuthService`e devredilir (K-068/3).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import get_database
from app.modules.auth.auth_dto import (
    ErisimTokeniYaniti,
    GirisIstegi,
    KayitIstegi,
    KullaniciYaniti,
    OturumKapatmaIstegi,
    TokenCiftiYaniti,
    TokenYenilemeIstegi,
)
from app.modules.auth.auth_service import AuthService, erisim_tokenini_dogrula

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer_semasi = HTTPBearer()


def _servis() -> AuthService:
    return AuthService(get_database())


def gecerli_kullanici_id(
    kimlik_bilgisi: HTTPAuthorizationCredentials = Depends(_bearer_semasi),
) -> str:
    """`Authorization: Bearer <token>` başlığındaki erişim token'ından kullanıcı kimliğini çıkarır."""
    return erisim_tokenini_dogrula(kimlik_bilgisi.credentials)


@router.post("/kayit", response_model=TokenCiftiYaniti, status_code=status.HTTP_201_CREATED)
async def kayit_ol(istek: KayitIstegi, servis: AuthService = Depends(_servis)) -> TokenCiftiYaniti:
    """E-23 Hesap oluştur: yeni kullanıcı açar ve doğrudan oturum açtırır."""
    erisim, yenileme = await servis.kayit_ol(istek.email, istek.sifre)
    return TokenCiftiYaniti(erisim_tokeni=erisim, yenileme_tokeni=yenileme)


@router.post("/giris", response_model=TokenCiftiYaniti)
async def giris_yap(istek: GirisIstegi, servis: AuthService = Depends(_servis)) -> TokenCiftiYaniti:
    """E-22 Oturum aç: e-posta/şifre doğrularsa token çifti döner."""
    erisim, yenileme = await servis.giris_yap(istek.email, istek.sifre)
    return TokenCiftiYaniti(erisim_tokeni=erisim, yenileme_tokeni=yenileme)


@router.post("/token/yenile", response_model=ErisimTokeniYaniti)
async def token_yenile(istek: TokenYenilemeIstegi, servis: AuthService = Depends(_servis)) -> ErisimTokeniYaniti:
    """Süresi geçmemiş erişim token'ı için yenileme token'ıyla yeni bir tane üretir."""
    erisim = await servis.token_yenile(istek.yenileme_tokeni)
    return ErisimTokeniYaniti(erisim_tokeni=erisim)


@router.post("/cikis", status_code=status.HTTP_204_NO_CONTENT)
async def oturum_kapat(istek: OturumKapatmaIstegi, servis: AuthService = Depends(_servis)) -> None:
    """Yenileme token'ını iptal eder; erişim token'ı zaten kısa ömürlü olduğundan kendiliğinden düşer."""
    await servis.oturum_kapat(istek.yenileme_tokeni)


@router.get("/ben", response_model=KullaniciYaniti)
async def ben_kimim(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: AuthService = Depends(_servis)
) -> KullaniciYaniti:
    """Geçerli erişim token'ına karşılık gelen kullanıcı bilgisini döndürür."""
    kullanici = await servis.kullaniciyi_getir(kullanici_id)
    return KullaniciYaniti(
        id=str(kullanici.id),
        email=kullanici.email,
        kimlik_saglayici=kullanici.kimlik_saglayici,
        olusturulma_tarihi=kullanici.olusturulma_tarihi,
    )


@router.delete("/hesap", status_code=status.HTTP_204_NO_CONTENT)
async def hesabi_sil(
    kullanici_id: str = Depends(gecerli_kullanici_id), servis: AuthService = Depends(_servis)
) -> None:
    """App Store zorunluluğu: hesabı ve auth verisini geri alınamaz biçimde siler (K-057)."""
    await servis.hesabi_sil(kullanici_id)
