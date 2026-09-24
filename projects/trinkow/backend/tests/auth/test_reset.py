from datetime import datetime, timedelta, timezone
from email import message_from_string
from hashlib import sha256
import re
import pytest
from app.core.database import get_database
from app.core.errors import GecersizToken, GecersizKimlikBilgisi, UygulamaHatasi
from app.modules.auth.auth_service import AuthService

pytestmark = pytest.mark.usefixtures("temiz_veritabani")

@pytest.fixture
async def posta(monkeypatch, tmp_path):
    monkeypatch.setenv("MAIL_MODE", "outbox")
    monkeypatch.setenv("MAIL_OUTBOX_DIR", str(tmp_path))
    await get_database()["auth_hiz_siniri"].delete_many({})
    return tmp_path

def _token(klasor):
    mesaj = message_from_string(next(klasor.glob("*.eml")).read_text())
    return re.search(r"token=([\w-]+)", mesaj.get_payload(decode=True).decode()).group(1)

async def test_reset_single_use_revokes_access_and_refresh(posta):
    servis = AuthService(get_database())
    erisim, yenileme = await servis.kayit_ol("reset@example.com", "eskiSifre123")
    await servis.sifirlama_iste("RESET@example.com")
    token = _token(posta)
    belge = await get_database().kullanicilar.find_one({"email": "reset@example.com"})
    assert belge["sifirlama_hash"] == sha256(token.encode()).hexdigest()
    await servis.sifre_sifirla(token, "yeniSifre123")
    with pytest.raises(UygulamaHatasi):
        await servis.sifre_sifirla(token, "yeniden123")
    with pytest.raises(GecersizToken):
        await servis.erisim_dogrula(erisim)
    with pytest.raises(GecersizToken):
        await servis.token_yenile(yenileme)
    with pytest.raises(GecersizKimlikBilgisi):
        await servis.giris_yap("reset@example.com", "eskiSifre123")
    yeni, _ = await servis.giris_yap("reset@example.com", "yeniSifre123")
    assert await servis.erisim_dogrula(yeni)

async def test_reset_expiry_and_rate_limit(posta):
    servis = AuthService(get_database())
    await servis.kayit_ol("reset@example.com", "eskiSifre123")
    await servis.sifirlama_iste("reset@example.com")
    token = _token(posta)
    await servis.sifirlama_iste("reset@example.com")
    assert len(list(posta.glob("*.eml"))) == 1
    await get_database().kullanicilar.update_one({"email": "reset@example.com"}, {"$set": {"sifirlama_son": datetime.now(timezone.utc)-timedelta(seconds=1)}})
    with pytest.raises(UygulamaHatasi):
        await servis.sifre_sifirla(token, "yeniSifre123")

async def test_unknown_email_and_missing_sender(posta, monkeypatch):
    servis = AuthService(get_database())
    await servis.sifirlama_iste("unknown@example.com")
    assert not list(posta.glob("*.eml"))
    monkeypatch.setenv("MAIL_MODE", "smtp")
    monkeypatch.delenv("SMTP_HOST", raising=False)
    with pytest.raises(UygulamaHatasi) as hata:
        await servis.sifirlama_iste("unknown@example.com")
    assert hata.value.durum_kodu == 503

async def test_refresh_rotation_consumes_old_token():
    servis = AuthService(get_database())
    _, eski = await servis.kayit_ol("rotation@example.com", "sifre1234")
    yeni_erisim, yeni = await servis.token_yenile(eski)
    assert yeni != eski
    assert await servis.erisim_dogrula(yeni_erisim)
    with pytest.raises(GecersizToken):
        await servis.token_yenile(eski)
    assert await servis.token_yenile(yeni)
