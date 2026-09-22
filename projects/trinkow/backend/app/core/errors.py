"""
Tüm modüllerin ortak hata sözleşmesi.

Her hata bir HTTP durum kodu + makine tarafından ayırt edilebilen bir
`hata_kodu` + insan-okur bir `mesaj` taşır. İstemci kendi Türkçe metnini
`hata_kodu`na göre seçer (bkz. docs/content/metinler.md § E-22/E-23);
`mesaj` yalnız yedek/log amaçlıdır ve hiçbir zaman "e-posta mı şifre mi
yanlış" gibi ayırt edici bilgi sızdırmaz.
"""
from __future__ import annotations


class UygulamaHatasi(Exception):
    """İş kuralı ihlallerinde fırlatılan, HTTP'den habersiz temel hata.

    Service katmanı HTTP durum kodu bilmek zorunda kalmasın diye bu
    sınıfı fırlatır; controller/main bunu HTTP yanıtına çevirir.
    """

    def __init__(self, hata_kodu: str, mesaj: str, durum_kodu: int) -> None:
        self.hata_kodu = hata_kodu
        self.mesaj = mesaj
        self.durum_kodu = durum_kodu
        super().__init__(mesaj)


class EpostaZatenKayitli(UygulamaHatasi):
    """Kayıt sırasında e-posta zaten kullanımdaysa (auth_dto.KayitIstegi)."""

    def __init__(self) -> None:
        super().__init__("EPOSTA_KAYITLI", "Bu e-posta ile hesap var.", 409)


class GecersizKimlikBilgisi(UygulamaHatasi):
    """Giriş başarısızsa — e-posta mı şifre mi yanlış olduğu bilerek belirtilmez."""

    def __init__(self) -> None:
        super().__init__("GECERSIZ_KIMLIK_BILGISI", "E-posta ya da şifre yanlış.", 401)


class TokenSuresiDolmus(UygulamaHatasi):
    """Erişim ya da yenileme token'ının süresi geçmişse."""

    def __init__(self) -> None:
        super().__init__("TOKEN_SURESI_DOLMUS", "Oturumun süresi doldu, yeniden giriş yap.", 401)


class GecersizToken(UygulamaHatasi):
    """Token biçimi/imzası bozuksa, iptal edilmişse ya da beklenen türde değilse."""

    def __init__(self) -> None:
        super().__init__("GECERSIZ_TOKEN", "Geçersiz oturum bilgisi.", 401)


class KullaniciBulunamadi(UygulamaHatasi):
    """Token geçerli ama kullanıcı silinmiş/bulunamıyorsa."""

    def __init__(self) -> None:
        super().__init__("KULLANICI_BULUNAMADI", "Kullanıcı bulunamadı.", 404)


class GelirGerekli(UygulamaHatasi):
    """Plan kurulurken aylık net gelir hâlâ girilmemişse (kullanici modülü, K-075)."""

    def __init__(self) -> None:
        super().__init__("GELIR_GEREKLI", "Planı kurmak için önce aylık net gelir girilmeli.", 422)


class HarcamaBulunamadi(UygulamaHatasi):
    """İstenen id'de kayıt yok ya da başka kullanıcıya ait (harcama modülü).

    Bilerek tek hata: hangisi olduğu ayırt edilmez — kullanıcı sorgusu zaten
    her zaman `kullanici_id` filtresiyle çalıştığı için başka kullanıcının
    kaydına erişimin yapısal bir yolu yok (kullanici_controller ile aynı ilke).
    """

    def __init__(self) -> None:
        super().__init__("HARCAMA_BULUNAMADI", "Harcama kaydı bulunamadı.", 404)


class TaksitliKayitTutariDegistirilemez(UygulamaHatasi):
    """Taksitli bir harcamanın tutarı tek başına değiştirilemez (Madde 2, seri toplamıyla tutarsızlaşır)."""

    def __init__(self) -> None:
        super().__init__(
            "TAKSITLI_KAYIT_TUTARI_DEGISTIRILEMEZ",
            "Taksitli bir kaydın tutarı düzenlenemez.",
            422,
        )


class TaksitliKayitTekBasinaSilinemez(UygulamaHatasi):
    """Taksitli bir harcama tek satır olarak silinemez; seri bütün olarak silinmeli (Madde 2)."""

    def __init__(self) -> None:
        super().__init__(
            "TAKSITLI_KAYIT_TEK_BASINA_SILINEMEZ",
            "Taksitli bir kayıt tek başına silinemez; taksit serisini silmelisin.",
            422,
        )


class GecersizTarihAraligi(UygulamaHatasi):
    """Başlangıç günü bitiş gününden sonraysa (ör. `ozet` modülü dönem/kategori sorguları)."""

    def __init__(self) -> None:
        super().__init__("GECERSIZ_TARIH_ARALIGI", "Başlangıç günü bitiş gününden sonra olamaz.", 422)


class KatalogOgesiBulunamadi(UygulamaHatasi):
    """İstenen `kod`da bir ürün kataloğu kalemi yoksa (katalog modülü)."""

    def __init__(self) -> None:
        super().__init__("KATALOG_OGESI_BULUNAMADI", "Katalog kalemi bulunamadı.", 404)


class PlanNegatifKalan(UygulamaHatasi):
    """Zorunlu giderler gelirden fazlaysa plan kurulmaz (delta-v4.md formül #10, K-075).

    `eksik_kurus` pozitif bir tutar (kuruş) taşır — istemci bunu
    "X ₺ eksik" biçiminde gösterir; negatif sayı asla üretilmez.
    """

    def __init__(self, eksik_kurus: int) -> None:
        self.eksik_kurus = eksik_kurus
        super().__init__(
            "PLAN_NEGATIF_KALAN",
            f"Zorunlu giderler gelirden {eksik_kurus} kuruş fazla, plan kurulamıyor.",
            422,
        )
