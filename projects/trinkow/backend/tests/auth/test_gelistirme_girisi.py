import asyncio
import json

import pytest

from app.core.config import get_settings
from app.core.database import get_database
from app.core.errors import EpostaZatenKayitli, GecersizKimlikBilgisi, UygulamaHatasi
from app.main import app
from app.modules.auth.auth_service import AuthService, erisim_tokenini_dogrula


@pytest.fixture
def demo_acik(monkeypatch):
    monkeypatch.setenv("TRINKOW_DEV_LOGIN", "1")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


async def istek(method, path, body=None, token=None):
    """HTTP sözleşmesini gerçek ASGI uygulamasından geçirir."""
    headers = [(b"content-type", b"application/json")]
    if token:
        headers.append((b"authorization", f"Bearer {token}".encode()))
    messages = []

    async def receive():
        return {"type": "http.request", "body": json.dumps(body).encode() if body else b"", "more_body": False}

    async def send(message):
        messages.append(message)

    route, _, query = path.partition("?")
    await app({"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
               "method": method, "scheme": "http", "path": route, "raw_path": route.encode(),
               "query_string": query.encode(), "root_path": "", "headers": headers,
               "server": ("test", 80), "client": ("127.0.0.1", 1)}, receive, send)
    status = next(m["status"] for m in messages if m["type"] == "http.response.start")
    content = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
    return status, json.loads(content) if content else None


async def test_demo_varsayilan_kapali(monkeypatch):
    monkeypatch.delenv("TRINKOW_DEV_LOGIN", raising=False)
    get_settings.cache_clear()
    try:
        with pytest.raises(UygulamaHatasi) as hata:
            await AuthService(get_database()).gelistirme_girisi("rastgele")
        assert hata.value.durum_kodu == 404
    finally:
        get_settings.cache_clear()


async def test_rastgele_bilgi_ayni_demo_hesabi_acar(temiz_veritabani, demo_acik):
    servis = AuthService(get_database())
    bir, iki = await asyncio.gather(servis.gelistirme_girisi(" rastgele "), servis.gelistirme_girisi("RASTGELE"))
    assert erisim_tokenini_dogrula(bir[0]) == erisim_tokenini_dogrula(iki[0])
    assert await get_database().kullanicilar.count_documents({}) == 1
    user = await servis.kullaniciyi_getir(erisim_tokenini_dogrula(bir[0]))
    assert user.kimlik_saglayici == "demo"
    assert user.sifre_hash is None
    assert erisim_tokenini_dogrula((await servis.token_yenile(bir[1]))[0]) == str(user.id)


async def test_demo_gercek_hesaba_giremez(temiz_veritabani, demo_acik):
    servis = AuthService(get_database())
    real = await servis.kayit_ol("mustafa@example.com", "gercek-sifre")
    demo = await servis.gelistirme_girisi("mustafa@example.com")
    assert erisim_tokenini_dogrula(real[0]) != erisim_tokenini_dogrula(demo[0])
    with pytest.raises(GecersizKimlikBilgisi):
        await servis.giris_yap("mustafa@example.com", "rastgele")


async def test_eszamanli_kayit_409_verir(temiz_veritabani):
    servis = AuthService(get_database())
    sonuclar = await asyncio.gather(*(servis.kayit_ol("test@example.com", "test-sifre") for _ in range(2)), return_exceptions=True)
    assert sum(isinstance(s, EpostaZatenKayitli) for s in sonuclar) == 1
    assert sum(isinstance(s, tuple) for s in sonuclar) == 1


async def test_http_demo_profil_harcama_ozet_ve_hesap_silme(temiz_veritabani, demo_acik):
    status, tokens = await istek("POST", "/auth/gelistirme-giris", {"email": "abc", "sifre": "x"})
    assert status == 200
    token = tokens["erisim_tokeni"]
    status, user = await istek("GET", "/auth/ben", token=token)
    assert status == 200 and user["kimlik_saglayici"] == "demo"
    status, profil = await istek("GET", "/kullanici/profil", token=token)
    assert status == 200 and not profil["onboarding_tamamlandi"]
    status, _ = await istek("PUT", "/kullanici/profil/katman1", {"niyet": "takip", "gelir_kurus": None, "maas_gunu": None, "maas_duzensiz": True}, token)
    assert status == 200
    status, butce = await istek("PUT", "/butce?bugun=2026-09-22", {
        "gelir_kurus": 300000, "sabit_giderler": {"kira": 0, "fatura": 0, "ulasim": 0, "kredi": 0},
        "hedef_birikim_kurus": 0, "borc_kurus": None, "limit_modu": "otomatik",
        "manuel_limit_kurus": None, "kategori_limitleri": {"market": 5000},
    }, token)
    assert status == 200 and butce["butce"]["gunluk_limit_kurus"] == 10000
    status, _ = await istek("PUT", "/butce/rutinler/kahve?bugun=2026-09-22", {
        "ad": "Kahve", "kategori": "kafe", "gunluk_adet": 1, "birim_fiyat_kurus": 5000, "aktif": True,
    }, token)
    assert status == 200
    status, kayit = await istek("POST", "/harcama/", {"tutar_kurus": 12345, "kategori": "market", "gun": "2026-09-22", "zaman": "2026-09-22T12:00:00Z", "odeme": "kart"}, token)
    assert status == 201, kayit
    status, pano = await istek("GET", "/ozet/pano?gun=2026-09-22", token=token)
    assert status == 200 and pano["harcanan_kurus"] == 12345
    status, ay = await istek("GET", "/tasarruf/ay?ay=2026-09&bugun=2026-09-22", token=token)
    assert status == 200 and ay["harcanan_kurus"] == 12345
    status, _ = await istek("DELETE", f'/harcama/{kayit["id"]}', token=token)
    assert status == 204
    status, _ = await istek("DELETE", "/harcama/ayar/tum-veriler", token=token)
    assert status == 204
    status, butce = await istek("GET", "/butce?bugun=2026-09-22", token=token)
    assert status == 200 and butce["butce"] is None
    status, profil = await istek("GET", "/kullanici/profil", token=token)
    assert status == 200 and not profil["onboarding_tamamlandi"]
    status, _ = await istek("DELETE", "/auth/hesap", token=token)
    assert status == 204
    status, _ = await istek("GET", "/auth/ben", token=token)
    assert status == 401
