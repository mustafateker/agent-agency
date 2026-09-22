"""
Katalog iş mantığı: koleksiyon boşsa tohumlama, listeleme + sürüm (ETag)
hesabı, tek kalem okuma.

HTTP'den habersizdir (kullanici_service.py / harcama_service.py ile aynı
desen, K-068/3). Bu modülün amacı bir ürün veritabanı DEĞİL, kullanıcının
harcama girerken seçtiği "ne aldın" kısayoludur (görev notu) — bu yüzden
BAĞLAYICI olarak fiyat/marka/görsel/miktar alanı YOKTUR ve eklenmez
(K-050 · K-037).

Kaynak veri istemcideki `app/src/content/urunKatalogu.ts` dosyasının bire
bir kopyasıdır (80 kalem). TypeScript dosyası Python tarafından import
edilemediği için burada elle senkron bir sabit olarak tutulur — istemci
listesi değişirse bu sabitin de elle güncellenmesi gerekir (bilinen sınır,
bkz. backend/README.md § katalog).
"""
from __future__ import annotations

import hashlib

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.errors import KatalogOgesiBulunamadi
from app.modules.katalog.katalog_model import KatalogOgesiBelgesi

KATALOG_KOLEKSIYONU = "katalog_ogeleri"

# (kod, ad, kategori, sira) — istemcideki `URUN_KATALOGU` ile birebir aynı
# sırada ve içerikte (kategoriye göre gruplanmış kaynak listeyle eşleşir).
VARSAYILAN_KATALOG: tuple[tuple[str, str, str, int], ...] = (
    ("filtre-kahve", "Filtre kahve", "kafe", 0),
    ("turk-kahvesi", "Türk kahvesi", "kafe", 1),
    ("latte", "Latte", "kafe", 2),
    ("sutlu-kahve", "Sütlü kahve", "kafe", 3),
    ("soguk-kahve", "Soğuk kahve", "kafe", 4),
    ("cay", "Çay", "kafe", 5),
    ("simit", "Simit", "kafe", 6),
    ("pogaca", "Poğaça", "kafe", 7),
    ("tatli", "Tatlı", "kafe", 8),
    ("doner", "Döner", "restoran", 9),
    ("lahmacun", "Lahmacun", "restoran", 10),
    ("pide", "Pide", "restoran", 11),
    ("kebap", "Kebap", "restoran", 12),
    ("tost", "Tost", "restoran", 13),
    ("hamburger", "Hamburger", "restoran", 14),
    ("pizza", "Pizza", "restoran", 15),
    ("ogle-yemegi", "Öğle yemeği", "restoran", 16),
    ("kahvalti-tabagi", "Kahvaltı tabağı", "restoran", 17),
    ("yemek-siparisi", "Yemek siparişi", "restoran", 18),
    ("haftalik-market", "Haftalık market", "market", 19),
    ("ekmek", "Ekmek", "market", 20),
    ("sut", "Süt", "market", 21),
    ("yumurta", "Yumurta", "market", 22),
    ("peynir", "Peynir", "market", 23),
    ("meyve-sebze", "Meyve ve sebze", "market", 24),
    ("et-tavuk", "Et ve tavuk", "market", 25),
    ("su-damacanasi", "Su damacanası", "market", 26),
    ("temizlik-malzemesi", "Temizlik malzemesi", "market", 27),
    ("kisisel-bakim", "Kişisel bakım", "market", 28),
    ("atistirmalik", "Atıştırmalık", "market", 29),
    ("toplu-tasima-yuklemesi", "Toplu taşıma yüklemesi", "ulasim", 30),
    ("sehirlerarasi-otobus-bileti", "Şehirlerarası otobüs bileti", "ulasim", 31),
    ("taksi", "Taksi", "ulasim", 32),
    ("otopark", "Otopark", "ulasim", 33),
    ("kopru-otoyol-gecisi", "Köprü ve otoyol geçişi", "ulasim", 34),
    ("ucak-bileti", "Uçak bileti", "ulasim", 35),
    ("kargo", "Kargo", "ulasim", 36),
    ("arac-bakimi", "Araç bakımı", "ulasim", 37),
    ("benzin", "Benzin", "akaryakit", 38),
    ("motorin", "Motorin", "akaryakit", 39),
    ("lpg", "LPG", "akaryakit", 40),
    ("elektrik-faturasi", "Elektrik faturası", "fatura", 41),
    ("su-faturasi", "Su faturası", "fatura", 42),
    ("dogalgaz-faturasi", "Doğalgaz faturası", "fatura", 43),
    ("internet-faturasi", "İnternet faturası", "fatura", 44),
    ("telefon-faturasi", "Telefon faturası", "fatura", 45),
    ("aidat", "Aidat", "fatura", 46),
    ("motorlu-tasitlar-vergisi", "Motorlu taşıtlar vergisi", "fatura", 47),
    ("kira", "Kira", "kiraev", 48),
    ("ev-esyasi", "Ev eşyası", "kiraev", 49),
    ("mobilya", "Mobilya", "kiraev", 50),
    ("tadilat-usta", "Tadilat ve usta", "kiraev", 51),
    ("ev-tekstili", "Ev tekstili", "kiraev", 52),
    ("muzik-aboneligi", "Müzik aboneliği", "abonelik", 53),
    ("dizi-film-aboneligi", "Dizi ve film aboneliği", "abonelik", 54),
    ("spor-salonu-uyeligi", "Spor salonu üyeliği", "abonelik", 55),
    ("bulut-depolama", "Bulut depolama", "abonelik", 56),
    ("oyun-aboneligi", "Oyun aboneliği", "abonelik", 57),
    ("yazilim-aboneligi", "Yazılım aboneliği", "abonelik", 58),
    ("sinema-bileti", "Sinema bileti", "eglence", 59),
    ("konser-bileti", "Konser bileti", "eglence", 60),
    ("mac-bileti", "Maç bileti", "eglence", 61),
    ("oyun-ici-satin-alma", "Oyun içi satın alma", "eglence", 62),
    ("kitap", "Kitap", "eglence", 63),
    ("muze-sergi", "Müze ve sergi", "eglence", 64),
    ("ust-giyim", "Üst giyim", "giyim", 65),
    ("pantolon", "Pantolon", "giyim", 66),
    ("ayakkabi", "Ayakkabı", "giyim", 67),
    ("dis-giyim", "Dış giyim", "giyim", 68),
    ("eczane", "Eczane", "saglik", 69),
    ("doktor-muayenesi", "Doktor muayenesi", "saglik", 70),
    ("dis-hekimi", "Diş hekimi", "saglik", 71),
    ("gozluk-lens", "Gözlük ve lens", "saglik", 72),
    ("tahlil-goruntuleme", "Tahlil ve görüntüleme", "saglik", 73),
    ("vitamin-takviye", "Vitamin ve takviye", "saglik", 74),
    ("sigara-paketi", "Sigara paketi", "aliskanliklar", 75),
    ("sarma-tutun", "Sarma tütün", "aliskanliklar", 76),
    ("nargile", "Nargile", "aliskanliklar", 77),
    ("bira", "Bira", "aliskanliklar", 78),
    ("sans-oyunu", "Şans oyunu", "aliskanliklar", 79),
)


def _surum_hesapla(ogeler: list[KatalogOgesiBelgesi]) -> str:
    """Katalogdaki her kalemin içeriğinden bir sürüm/ETag değeri türetir.

    `kod` ile sıralanıp özetlenir (Mongo sorgu sırası garanti olmasa da
    sürüm kararlı kalsın diye) — herhangi bir kalem eklenir/silinir/
    değişirse özet değişir, istemci bu değeri önceki `surum`üyle
    karşılaştırıp yeniden indirip indirmeyeceğine karar verir.
    """
    siralanmis = sorted(ogeler, key=lambda oge: oge.kod)
    ozet_girdisi = "|".join(f"{oge.kod}:{oge.ad}:{oge.kategori}" for oge in siralanmis)
    return hashlib.sha256(ozet_girdisi.encode("utf-8")).hexdigest()[:16]


class KatalogService:
    """Ürün kataloğu koleksiyonunun tohumlama/okuma işlemlerini yürütür."""

    def __init__(self, veritabani: AsyncIOMotorDatabase) -> None:
        self._katalog = veritabani[KATALOG_KOLEKSIYONU]

    async def tohumla(self) -> int:
        """Koleksiyon BOŞSA varsayılan 80 kalemi yükler; doluysa dokunmaz.

        İdempotenttir: ikinci çağrıda koleksiyon zaten dolu olduğu için hiç
        yazma yapılmaz (kullanıcı tarafından yapılmış olabilecek sunucu içi
        güncellemelere dokunulmaz — görev notu, harcama/kullanici'deki
        göç/tohum deseniyle aynı ilke).
        """
        mevcut_sayi = await self._katalog.count_documents({})
        if mevcut_sayi > 0:
            return 0
        belgeler = [
            KatalogOgesiBelgesi(kod=kod, ad=ad, kategori=kategori, sira=sira).belgeye_cevir()
            for kod, ad, kategori, sira in VARSAYILAN_KATALOG
        ]
        sonuc = await self._katalog.insert_many(belgeler)
        return len(sonuc.inserted_ids)

    async def katalogu_listele(self) -> tuple[list[KatalogOgesiBelgesi], str]:
        """Tüm kalemleri kaynak sırasıyla + o anki sürüm/ETag değeriyle döner."""
        imlec = self._katalog.find({}).sort("sira", 1)
        ogeler = [KatalogOgesiBelgesi.belgeden_olustur(belge) async for belge in imlec]
        return ogeler, _surum_hesapla(ogeler)

    async def oge_getir(self, kod: str) -> KatalogOgesiBelgesi:
        """Tek bir kalemi `kod`una göre okur; yoksa `KatalogOgesiBulunamadi` fırlatır."""
        belge = await self._katalog.find_one({"kod": kod})
        if belge is None:
            raise KatalogOgesiBulunamadi()
        return KatalogOgesiBelgesi.belgeden_olustur(belge)
