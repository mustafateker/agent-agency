# Trinkow Backend

Mobil uygulamadan (`projects/trinkow/app`) **tamamen ayrı** çalışan Python servisi.
Ayrı süreç, ayrı bağımlılıklar, ayrı çalıştırma komutu.

**Veri sunucudadır** (K-068). Cihaz yalnız oturum token'ını ve görüntülenen verinin
geçici önbelleğini tutar; çelişki hâlinde **sunucu üstündür**. Yerel SQLite bir
"ikinci gerçek" olarak kullanılmaz.

Stack: **FastAPI · Uvicorn · Pydantic v2 · Motor (async MongoDB) · pytest ·
passlib[bcrypt] · pyjwt**. Kimlik **kendi `auth` modülümüzde, JWT ile** (K-068).
Prod barındırma yok; yerel MongoDB + Compass.

## Klasör yapısı (bağlayıcı)

Her backend sistemi **bir modüldür** ve kendi klasöründe kapalıdır:

```
backend/
├── README.md
├── pyproject.toml            # bağımlılıklar (onaylandıktan sonra)
├── .env.example              # gerçek .env asla commit edilmez
├── app/
│   ├── main.py               # modül router'larını toplar, başka iş yapmaz
│   ├── core/                 # config · mongo bağlantısı · güvenlik · hata tipleri
│   ├── shared/               # modüller arası ortak yardımcılar (mümkün olduğunca boş)
│   └── modules/
│       ├── auth/
│       │   ├── auth_controller.py   # HTTP katmanı: yol, doğrulama, yanıt kodu
│       │   ├── auth_service.py      # iş mantığı — HTTP'den ve Mongo'dan habersiz
│       │   ├── auth_dto.py          # istek/yanıt şemaları (Pydantic)
│       │   └── auth_model.py        # Mongo belge modeli
│       └── <modul>/                 # aynı dört dosya
└── tests/
    └── <modul>/                     # her modülün kendi pytest dosyaları
```

### Kurallar
1. **Bir modül, bir klasör.** Modüller birbirinin iç dosyasını import etmez;
   ihtiyaç varsa servis arayüzü üzerinden konuşur. Amaç: bir modülü ayrı bir
   servise taşımak gerektiğinde klasörü taşımanın yetmesi.
2. **DTO ≠ veritabanı modeli.** DTO dışarıya açılan sözleşmedir, model içeride
   saklanan belgedir. İkisi aynı dosyada tutulmaz.
3. **Controller iş mantığı içermez**; service HTTP bilmez. Mongo erişimi
   service katmanında, bağlantı `core`'dan gelir.
4. **Para kuruş cinsinden integer.** Float yasak (uygulamayla aynı kural).
5. Her yeni modül için **pytest testi** zorunlu (CLAUDE.md standardı).
6. `.env` commit edilmez; örnek değerler `.env.example`'da durur.

## Veritabanı
MongoDB — **MongoDB Atlas** (bulut) kullanılıyor; bağlantı dizesi `.env`de
hazır (bkz. `MONGODB_URI`), yerelde Mongo kurmaya gerek yok. İnceleme için
Compass'a Atlas bağlantı dizesiyle bağlanılır. Prod barındırma kararı ayrı
bir karardır (ücretli servis onay kapısından geçmiştir — bkz.
`status/DECISIONS.md`).

## Modül haritası (taslak — Mustafa ile tek tek kararlaştırılacak)
| Modül | Ne yapar | Durum |
|---|---|---|
| `auth` | Kayıt, oturum açma, token yenileme, hesap silme | ✅ hazır (Google/Apple ayrı tur: BE-2d) |
| `kullanici` | Profil ve plan verisi (niyet, gelir, maaş günü, paylar) | ✅ hazır |
| `harcama` | Harcama kayıtları, taksitler, kategori limitleri — **sunucuda** | ✅ hazır |
| `ozet` | Pano/özet/kategori dağılımı/seri — **kendi koleksiyonu yok**, `harcama`+`kullanici`yi okur | ✅ hazır |
| `katalog` | Ürün kataloğunun sunucudan güncellenmesi | ✅ hazır |
| `bildirim` | Hatırlatma/limit bildirimleri | acelesi yok, tasarlanacak |

## Çalıştırma

### 1. Ortam kurulumu
```bash
cd projects/trinkow/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env      # JWT_SECRET_KEY'i gerçek bir rastgele değerle değiştir
```

### 2. Veritabanı bağlantısı
Proje **MongoDB Atlas** kullanıyor — `cp .env.example .env` sonrası
`MONGODB_URI`yi Atlas bağlantı dizesiyle değiştirmen yeterli, ayrıca bir
kurulum adımı YOK. Bağlantıyı doğrulamak için `mongosh "<Atlas URI'n>"` ya da
Compass ile bağlan.

> **Dipnot — yerel Mongo alternatifi:** Atlas'a erişimin yoksa (ör. tamamen
> çevrimdışı geliştirme) yerelde de çalıştırabilirsin, `MONGODB_URI`yi
> `mongodb://localhost:27017` yapman yeterli:
> ```bash
> # Homebrew ile
> brew tap mongodb/brew && brew install mongodb-community
> brew services start mongodb-community
>
> # ya da Docker ile (repoya Docker dosyası eklenmedi, yalnız yerel bir kısayol)
> docker run -d --name trinkow-mongo -p 27017:27017 mongo:7
> ```

### 3. Uygulamayı çalıştır
```bash
uvicorn app.main:app --reload
```
`http://127.0.0.1:8000/saglik` → `{"durum": "ayakta"}` dönerse servis ayaktadır.
`http://127.0.0.1:8000/docs` üzerinden uç noktaları deneyebilirsin.

### 4. Testleri çalıştır
Testler **gerçek MongoDB'ye karşı**, ama ayrı bir veritabanında (`trinkow_test`)
çalışır ve her testten önce/sonra kendini temizler — geliştirme verine dokunmaz.
Mongo 2. adımdaki gibi ayakta olmalı:
```bash
pytest
```
Farklı bir test veritabanı adı/URI'si istersen testten önce ortam değişkeniyle geç:
```bash
MONGODB_DB_NAME=baska_test_db pytest
```

## Uç noktalar (`auth` modülü)
| Yol | Yöntem | Ne yapar |
|---|---|---|
| `/auth/kayit` | POST | E-posta/şifre ile hesap açar, doğrudan token çifti döner (201) |
| `/auth/giris` | POST | E-posta/şifre doğrularsa token çifti döner |
| `/auth/token/yenile` | POST | Geçerli yenileme token'ı ile yeni erişim token'ı üretir |
| `/auth/cikis` | POST | Yenileme token'ını iptal eder (204) |
| `/auth/ben` | GET | `Authorization: Bearer <erişim token>` ile mevcut kullanıcıyı döner |
| `/auth/hesap` | DELETE | Hesabı VE kullanıcıya ait TÜM veriyi (profil, harcama, kategori limiti, gün durumu, limit geçmişi, ürün öğrenme) geri alınamaz biçimde siler (204, App Store zorunluluğu — K-085 Madde 1) |

Hata yanıtları tek biçimdedir: `{"hata_kodu": "...", "mesaj": "..."}` (bkz. `app/core/errors.py`).
Giriş hatasında hangi alanın (e-posta/şifre) yanlış olduğu **bilerek belirtilmez**.

**Hesap silme sırası (K-085 Madde 1):** Mongo'da tek-belge işlemi (transaction)
yok, bu yüzden `AuthService.hesabi_sil` önce diğer modüllerin verisini
(`HarcamaService.kullanici_verisini_sil` · `KullaniciService.kullanici_verisini_sil`
— servis arayüzü üzerinden, Kural 1 ihlal edilmez), **en son** kimlik kaydını
(`kullanicilar`) siler. Yarıda kesilirse kullanıcı hâlâ giriş yapıp silmeyi
TEKRAR deneyebilir; alt adımlar idempotenttir.

## Uç noktalar (`kullanici` modülü)
Hepsi oturum gerektirir (`Authorization: Bearer <erişim token>`); kullanıcı URL'de kimlik
taşımadığı için yalnız KENDİ profiline erişebilir (başka kullanıcıya erişimin yapısal yolu yok).

| Yol | Yöntem | Ne yapar |
|---|---|---|
| `/kullanici/profil` | GET | Profili döner; hiç veri girilmemişse varsayılan (boş) profil döner |
| `/kullanici/profil/katman1` | PUT | E-01..E-03: niyet, gelir, maaş günü kaydeder; onboarding'i tamamlanmış işaretler |
| `/kullanici/profil/katman1` | PATCH | K-084/1 (BE-4b Madde 5): yalnız gönderilen Katman 1 alanı güncellenir; onboarding bayrağına dokunmaz (bu yalnız PUT'un işi) |
| `/kullanici/profil/katman2` | PATCH | E-25'in 8 kartı — yalnız gönderilen alanlar güncellenir (kısmi güncelleme) |
| `/kullanici/plan/kur` | POST | E-26: zorunlu/sosyal/birikim paylarını ve günlük limiti **sunucu hesaplar** (K-075), kaydeder, hesapladığını döner. Opsiyonel `?bugun=YYYY-MM-DD` sorgu parametresi: "bugün" istemciden gelir, sunucu saat dilimi varsayımı yapmaz (`/ozet/seri`'deki K-087 deseniyle aynı, QA-1). Verilmezse geriye dönük uyumluluk için sunucu UTC gününe düşer — bu düşüş kalıcı değildir, istemci her zaman göndermeli |
| `/kullanici/plan/gunluk-limit` | PUT | E-17: günlük limiti plan hesabından bağımsız, elle yazar; bekleyen Katman 1 önerisini temizler; **aynı değeri** `harcama` modülünün `limit_gecmisi`ne de yazar (K-085 Madde 6 — tek otorite `gunluk_limit_kurus`, `limit_gecmisi` onun tarihçesi). Opsiyonel `?bugun=YYYY-MM-DD` sorgu parametresi: `limit_gecmisi` satırının hangi güne yazılacağını istemci belirler, sunucu saat dilimi varsayımı yapmaz (`/ozet/seri`'deki K-087 deseniyle aynı, QA-1b). Verilmezse geriye dönük uyumluluk için sunucu UTC gününe düşer — bu düşüş kalıcı değildir, istemci her zaman göndermeli |
| `/kullanici/plan/gunluk-limit-onerisi` | DELETE | "Limitsiz devam et": Katman 1 önerisini gerçek limite dönüştürmeden düşürür |
| `/kullanici/tercihler` | GET | E-19 Ayarlar: bildirim/gün sınırı/varsayılan ödeme/kurulum günü tercihlerini döner |
| `/kullanici/tercihler` | PATCH | E-19 Ayarlar: yalnız gönderilen tercih alanı güncellenir; `kurulum_gunu` bir kez yazılınca sabitlenir (K-049) |

Plan formülleri `docs/design/delta-v4.md` satır 764-792'deki tabloyu birebir uygular
(`app/modules/kullanici/kullanici_service.py`); istemcinin `src/lib/plan.ts` dosyası aynı
tabloyu ayrıca uygular, ikisi birbirinin kodunu değil tabloyu referans alır (K-075).
Zorunlu giderler gelirden fazlaysa (`PLAN_NEGATIF_KALAN`, 422) plan kurulmaz.

Katman 1'in önerdiği günlük limit (`gunluk_limit_onerisi_kurus`) K-059/5 gereği kabul
edilene kadar gerçek limit değildir; `KullaniciProfilYaniti.son_kart` Katman 2'nin
"kaldığın yerden" pozisyonudur (varsayılan 1).

## Uç noktalar (`harcama` modülü)
Hepsi oturum gerektirir; her sorgu `kullanici_id` ile filtrelenir — başka kullanıcının
kaydına erişimin yapısal bir yolu yoktur (bulunamayan/başkasına ait kayıt aynı `HARCAMA_BULUNAMADI`
404'ünü döner, ayırt edilmez).

| Yol | Yöntem | Ne yapar |
|---|---|---|
| `/harcama/` | POST | Tek bir harcama satırı ekler (201); ürün adı verilmişse ürün→kategori öğrenmesini de günceller |
| `/harcama/` | GET | `gun` / `baslangic_gun`+`bitis_gun` / `kategori` süzgeciyle **sayfalanmış** listeleme (`sayfa`, `sayfa_boyutu` ≤ 200) |
| `/harcama/{id}` | GET | Tek kayıt okur |
| `/harcama/{id}` | PATCH | Yalnız gönderilen alanları günceller; taksitli kayıtta `tutar_kurus` gönderilirse 422 |
| `/harcama/{id}` | DELETE | Kalıcı siler (204) — geri alma istemci tarafındaki 6 sn toast'ta (K-029); taksitliyse 422 |
| `/harcama/taksit/{taksit_id}` | DELETE | Taksit serisini TAMAMEN siler (204) |
| `/harcama/gun-durumu` | PUT | K-048 hile kapısı: bir günü "harcamasız" işaretler/kaldırır |
| `/harcama/gun-durumu/{gun}` | GET | Bir günün "harcamasız" işaretli olup olmadığını döner |
| `/harcama/ayar/kategori-limitleri` | GET | Yalnız değeri olan kategori limitlerini `sira`ya göre döner |
| `/harcama/ayar/kategori-limitleri` | PUT | Bir kategorinin limitini yazar/günceller |
| `/harcama/ayar/kategori-limitleri/{kategori}` | DELETE | K-085 Madde 2: bir kategorinin limitini kaldırır (204) — `PUT`'un `limit_kurus>0` zorunluluğu "sil"i temsil edemiyordu, idempotent |
| `/harcama/ayar/limit-gecmisi` | POST | K-064/1: günlük limit değiştiğinde yürürlük tarihiyle bir satır yazar (201) |
| `/harcama/ayar/urun-kategori-ogrenme` | GET | Tüm öğrenilmiş ürün→kategori eşlemelerini döner |
| `/harcama/ayar/urun-kategori-ogrenme` | PUT | Bir ürün adı için kategoriyi elle öğretir/düzeltir |
| `/harcama/ayar/en-eski-kayit-gunu` | GET | K-085 Madde 4: kullanıcının ilk harcama kaydının günü (`gun: string \| null`) — istemcinin seri sınırı hesabı için |
| `/harcama/ayar/tum-veriler` | DELETE | K-085 Madde 3: Ayarlar'daki "Tüm verileri sil" — harcama/kategori limiti/gün durumu/limit geçmişi/ürün öğrenmeyi siler (204); **hesabı ve profili SİLMEZ** (bkz. `/auth/hesap` ile farkı) |

Para her yerde **kuruş cinsinden integer**. Taksit alanları (`taksit_id`/`taksit_no`/
`taksit_toplam`) ya birlikte gelir ya hiç gelmez; bir taksit serisi oluşturmak için
istemci `/harcama/` uç noktasını taksit sayısı kadar aynı `taksit_id` ile çağırır (ayrı bir
"seri oluştur" uç noktası yok — istemcideki `taksitSerisiOlustur` bugün de aynı döngüyü
yerelde yapıyor). `limit_gecmisi`nin "o gün yürürlükteki limiti" okuma mantığı
(`HarcamaService.limit_gecmisi_efektif_limit`) servis katmanında hazır ama HTTP'ye AÇILMADI
— `ozet` modülü bu metodu servis-arayüzü üzerinden çağırarak seri hesabında kullanır
(bkz. aşağıdaki `ozet` bölümü).

**BE-5b (K-077) ile eklenen, yalnız servis-arayüzünde duran uç** (HTTP'ye açılmadı —
yukarıdaki `limit_gecmisi_efektif_limit` ile aynı desen, `ozet` bunu doğrudan Python
metodu olarak çağırır; `HarcamaService.en_eski_kayit_gunu` ise BE-4b/Madde 4 ile
`GET /harcama/ayar/en-eski-kayit-gunu` olarak HTTP'ye açıldı, artık burada listelenmiyor):
- `HarcamaService.limit_gecmisi_araligi_getir(kullanici_id, bitis_gun)` — `bitis_gun`e
  kadarki TÜM limit değişiklik geçmişini ARTAN tarihle TEK sorguda döner (Madde 3);
  `ozet` bunu bir kez çekip `efektif_limit_cozucu_olustur` ile bellekte gün gün çözer —
  300+ günlük seri hesabında O(gün) yerine O(1) Mongo sorgusu.

## Uç noktalar (`ozet` modülü)
Hepsi oturum gerektirir. Bu modülün **kendi Mongo koleksiyonu YOK** (K-076/BE-5) —
yalnız `HarcamaService`/`KullaniciService`nin servis arayüzlerini çağırır, hiçbir
koleksiyona doğrudan sorgu atmaz (Kural 1).

| Yol | Yöntem | Ne yapar |
|---|---|---|
| `/ozet/pano` | GET | E-10: `gun` (verilmezse bugün) için toplam · limit durumu (`altinda`/`asimda`/`tanimsiz`) · aylık kategori kırılımı · ay aşım sayısı · o günün seri bilgisi |
| `/ozet/donem` | GET | E-16: `baslangic_gun`+`bitis_gun` arası toplam · kategori dağılımı (₺+% — en büyük kalan yöntemi) · en çok harcanan 3 kategori · Latte Faktörü (`esik_kurus`, varsayılan 5.000) |
| `/ozet/kategori/{kategori}` | GET | E-15: bir kategorinin `baslangic_gun`+`bitis_gun` arası günlük seyri + toplamı; kayıt LİSTESİ için mevcut `GET /harcama/?kategori=` kullanılır (kasıtlı — sorumluluk çakışmasın diye burada tekrarlanmadı) |
| `/ozet/seri` | GET | E-21 (K-048 + K-064/1 + K-087): `bugun` (`YYYY-MM-DD`, opsiyonel — istemci yerel günü göndermeli; verilmezse **istisna olarak** sunucu UTC gününe düşer) için mevcut seri · en uzun seri (+ bittiği gün) · son 30 günün ızgarası · geçilen milestone'lar · sonraki/önceki durak |

**Seri hesabı (BE-5b/K-077 düzeltme turuyla güncellendi):**
- **En uzun seri KALICI** (Madde 1, K-048/F-16f) — `kullanici_profilleri.en_uzun_seri` +
  `en_uzun_seri_bitis_gunu` alanlarında saklanır ve yalnız BÜYÜR (ratchet,
  `en_uzun_seri_ratchet`). Limitsiz kipte mevcut seri kapalı/0'dır ama kayıtlı rekor
  döner ve KAYBOLMAZ — istemcinin `ayar.seri_en_uzun_gun` anahtarıyla aynı davranış,
  saklandığı yer kullanıcı profili (tek kullanıcı için tek kalıcı sayaç, `gunluk_limit_kurus`
  ile aynı doğada) — ayrı bir `ozet` koleksiyonu açmaya gerek yok.
- Sınır günü (Madde 2) `kurulum_gunu` ile `HarcamaService.en_eski_kayit_gunu`nun daha
  ERKEN olanıdır (`seri_sinir_gunu_belirle` — istemcideki `ilkSinirGunu` ile aynı kural).
- Her günün efektif limiti (Madde 3) artık TEK TEK sorgulanmıyor —
  `HarcamaService.limit_gecmisi_araligi_getir` ile TEK seferde çekilip
  `efektif_limit_cozucu_olustur` ile bellekte gün gün çözülüyor (K-064/1 davranışı
  AYNI: tablodan önceki günler için güncel limit "en iyi tahmin"); 300+ günlük
  geçmişte Mongo sorgu sayısı O(gün)'den O(1)'e düştü.

## Uç noktalar (`katalog` modülü)
Hepsi oturum gerektirir. Kalemler yalnız **tohumlama** ile oluşur; yazma ucu YOKTUR.

| Yol | Yöntem | Ne yapar |
|---|---|---|
| `/katalog/` | GET | 80 kalemlik kataloğu + `surum` döner. İstemci `If-None-Match` gönderir ve katalog değişmemişse gövdesiz **304** döner |
| `/katalog/{kod}` | GET | Tek kalemi koduna göre okur |

**Bilinçli sınırlar (K-050 · K-037):** katalogda **fiyat yoktur** (ne ödendiğini
yalnız kullanıcı söyler) · **marka adı yoktur** (jenerik kalem: "Sigara paketi" ✅,
marka adı yalnız kullanıcının kendi geçmişinde) · ürün görseli, barkod, miktar/adet
alanı yoktur. **Arama istemcide kalır** — 80 kalem RAM'de, çevrimdışı ve anlık;
bu yüzden sunucuda arama ucu açılmadı.
