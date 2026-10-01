"""Şifre kurtarma e-postası; yerel outbox açıkça seçilmedikçe SMTP gerekir."""
from __future__ import annotations

import asyncio
import os
import smtplib
import ssl
import uuid
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlencode

from app.core.errors import UygulamaHatasi


def posta_ayarlarini_dogrula() -> None:
    mod = os.environ.get("MAIL_MODE", "smtp")
    if mod == "outbox" and os.environ.get("MAIL_OUTBOX_DIR"):
        return
    if mod == "smtp" and os.environ.get("SMTP_HOST") and os.environ.get("SMTP_FROM"):
        return
    raise UygulamaHatasi("POSTA_HAZIR_DEGIL", "Şifre kurtarma şu anda kullanılamıyor. Daha sonra tekrar dene.", 503)


async def sifirlama_postasi_gonder(email: str, token: str) -> None:
    posta_ayarlarini_dogrula()
    adres = os.environ.get("PASSWORD_RESET_URL", "trinkow://sifre-sifirla")
    baglanti = adres + ("&" if "?" in adres else "?") + urlencode({"token": token})
    mesaj = EmailMessage()
    mesaj["Subject"] = "Trinkow şifreni yenile"
    mesaj["From"] = os.environ.get("SMTP_FROM", "test@trinkow.example")
    mesaj["To"] = email
    mesaj.set_content(f"Şifreni yenilemek için bağlantıyı aç: {baglanti}\nBağlantı 30 dakika geçerlidir ve bir kez kullanılabilir.\nBu isteği sen yapmadıysan e-postayı yok sayabilirsin.")
    try:
        await asyncio.to_thread(_gonder, mesaj)
    except (OSError, smtplib.SMTPException, ValueError) as hata:
        raise UygulamaHatasi("POSTA_GONDERILEMEDI", "E-posta gönderilemedi. Daha sonra tekrar dene.", 503) from hata


def _gonder(mesaj: EmailMessage) -> None:
    if os.environ.get("MAIL_MODE") == "outbox":
        klasor = Path(os.environ["MAIL_OUTBOX_DIR"])
        klasor.mkdir(parents=True, exist_ok=True, mode=0o700)
        hedef = klasor / f"{uuid.uuid4()}.eml"
        with hedef.open("x") as dosya:
            hedef.chmod(0o600)
            dosya.write(mesaj.as_string())
        return
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587")), timeout=15) as smtp:
        smtp.starttls(context=ssl.create_default_context())
        if os.environ.get("SMTP_USER"):
            smtp.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASSWORD", ""))
        smtp.send_message(mesaj)
