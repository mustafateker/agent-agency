# QA Raporu — Aşama 4 / D-3 (İlk tam QA turu)
Tarih: 2026-09-20 · Kapsam: backend (FastAPI+Mongo Atlas) + istemci (Expo/TS)

## 1. Test sonucu
- Backend: `cd backend && .venv/bin/python -m pytest -q` → **118 passed** (223s, Atlas uzak olduğu için yavaş — beklenen).
- İstemci: `cd app && npx tsc --noEmit` → **0 hata**.
- İstemci otomatik test: **YOK** (Vitest/Jest kurulu değil). Bulgu — bkz. §4.

## 2. BLOCKER

### B1 — Plan kurma UTC gün kullanıyor, K-087'nin kuralı burada uygulanmamış
`backend/app/modules/kullanici/kullanici_service.py:222,238` `plani_kur(...)`
çağrıldığında `bugun` verilmezse `datetime.now(timezone.utc).date()` kullanılır.
`POST /kullanici/plan/kur` **gövde almaz** (`app/src/lib/api.ts:234-236`,
`kullanici_controller.py:153-158`) — yani istemci hiçbir zaman kendi yerel
gününü göndermiyor. K-087'de aynı sınıf hata `/ozet/seri` için tam olarak
bu gerekçeyle bloklayıcı sayılıp düzeltilmişti ("sunucu 'bugün'ü kendisi
türetmez, gün istemciden gelir"); bu kural `plani_kur`e hiç taşınmamış.
**Tetikleme:** TR saatiyle 00:00–02:59 arası "Planı kur"a basan bir kullanıcı
için `kalan_gun_hesapla` bir gün önceki UTC tarihiyle hesaplanır → maaş günü
sınırında (`bugün >= ödeme günü mü?`) yanlış dala düşebilir, `kalan_gun` ve
dolayısıyla `gunluk_limit_kurus` müşterinin `plan.ts` ile hesapladığından
1 gün kayar. Kod incelemesiyle doğrulandı (kuramsal değil — controller'da
literal olarak gün parametresi yok); saat dilimi senaryosunu canlı tetiklemek
bu turda denenmedi. **→ python-developer.**

### B2 — Yanlış mahremiyet metni tek yerde değil, 5 yerde
K-082 yalnız `hesap.mahremiyet` metnini "yanıltıcı, düzeltilecek" diye
bloklayıcı listesine almıştı. Kod taramasında **4 ek metin** aynı yanlış
iddiayı taşıyor ve hepsi gerçekten ekranda gösteriliyor:
- `src/content/metinler.ts:505` `ayar.hesap.cikis_not` "Çıkınca kayıtların
  sende kalır." → `app/ayarlar.tsx:460` civarı, signed-in çıkış sonrası.
- `src/content/metinler.ts:507` `ayar.hesap.kapali` "**Hesap isteğe bağlı.**
  Kayıtların sende kalır." → `AccountSection.tsx:35`, `signed-out` dalı.
  Bu ayrıca **K-080 ile çelişiyor** (hesap artık ZORUNLU, "isteğe bağlı" değil).
- `src/content/metinler.ts:553` `ayar.veri_aciklama` "Kayıtların sende kalır."
  → `app/ayarlar.tsx:470`, Ayarlar > Veri bölümü, normal akışta her zaman görünür.
- `src/content/metinler.ts:1154` `hesapsilVeri(n)` "{n} kayıt sende kalır…"
  → `app/ayarlar.tsx:537`, **hesap silme onay diyaloğunda**. Burada özellikle
  ağır: K-086'dan beri hesap silme TÜM sunucu verisini siliyor; bu metin
  kullanıcıya tam tersini ("veri kalır") söylüyor.
**Tetikleme:** Ayarlar ekranı açık, kod okunarak doğrulandı; `signed-out`
dalı K-082'nin kendi bulgusuna göre yalnız çıkış-sonrası geri tuşu gibi bir
kenar durumda ulaşılabilir (teorik ama sıfır değil), diğer üçü **normal akışta
her zaman görünür**. **→ frontend-developer** (metin kaynağı `metinler.md`
olmalı, K-065/3 kuralı gereği koddan değil dokümandan başlanmalı).

## 3. ÖNEMLİ
- Bilinen açık borçlar hâlâ geçerli (kod okunarak doğrulandı, yenisi eklenmedi):
  "Şifremi unuttum" sahte (backend'de sıfırlama ucu yok) · bildirim anahtarı
  gerçek izin isteyemiyor (Expo bildirim eklenmedi, K-081) · refresh token
  rotasyonu yok (`auth_service.py:118` `token_yenile` yalnız yeni access token
  döndürüyor, refresh aynı kalıyor) · token'lar `expo-sqlite`'ta
  (`oturumDeposu.ts:19`), güvenli depoda değil · E-00 açılış ekranı yok.
- Diğer risk alanları (para, seri/ratchet, yetkilendirme, taksit bütünlüğü,
  hesap silme) kod incelemesinde **sağlam** bulundu: `kullanici_id` her uçta
  JWT bağımlılığından geliyor (URL'den değil) · taksitli kayıtta tutar
  değişikliği 422 ile reddediliyor · taksit serisi silme atomik (`delete_many`
  tek `taksit_id` filtresiyle) · en uzun seri ratchet olarak saklanıyor ve
  yalnız büyüyor · hesap silme artık tüm koleksiyonları sırayla siliyor
  (K-086) · para her yerde kuruş `int`, float kullanımı görülmedi.

## 4. TEST BOŞLUKLARI
İstemcide hiç otomatik test yok. En yüksek değerli 6 modül (öneri, kod değil):
1. `src/lib/plan.ts` — largest-remainder yüzde dağıtımı + aşağı yuvarlama;
   sunucu formülüyle **altın (golden) vaka** karşılaştırması (K-075 sözleşmesi).
2. `src/lib/tarih.ts` — `gunAnahtari` gün sınırı (00:00/03:00/06:00), `kalanGun`
   ay sonu / 31→Şubat / "Düzensiz" 30 gün.
3. `src/lib/api.ts` — 401 → tek seferlik `tokenYenile` → ikinci 401'de oturum
   silme; ağ hatasında `ApiAgHatasi` fırlatıldığını doğrulayan testler.
4. `src/lib/harcamaEylemleri.ts` — taksit serisi kısmi hata senaryosu (seri
   silme ile geri alma).
5. `src/db/seri.ts` — sunucu yanıtının ratchet/limitsiz-kapalı alanlarını
   olduğu gibi yansıttığını doğrulayan ince entegrasyon testi.
6. `src/lib/oturumDeposu.ts` — token yenileme/çıkış sırasında yarım kalan
   yazma senaryoları.

Backend tarafında Python testleri kapsamlı (118); ayrıca yazılmasını önerdiğim
tek şey: `plani_kur` için **gece 00:00–03:00 UTC sınırı** ve ödeme günü sınırını
aynı anda test eden bir vaka (B1'i kalıcı olarak kapatacak regresyon testi).

## 5. Denenemeyenler (dürüstlük notu)
Simülatörde uçtan uca gezinme yapılmadı (yalnız kod incelemesi + `pytest`/`tsc`).
B1'in gerçek saat diliminde tetiklenmesi ve `signed-out` AccountSection dalının
gerçekten ulaşılabilir olup olmadığı canlı denenmedi — B1 "kod kanıtlı, saat
dilimi senaryosu kuramsal"; B2'nin 3/4 metni ise normal akışta kanıtlı.

## SONUÇ
**GEÇMEDİ** — yayına hazır değil. 2 blocker kapanmadan olmaz: (B1) plan kurma
UTC/yerel gün ayrışması, (B2) 4 ek yerde yanlış mahremiyet/hesap-isteğe-bağlı
metni. İkisi de küçük, hedefli düzeltmeler; mimari değişiklik gerektirmiyor.

---

# DELTA — Aşama 4 / D-3b (K-089/K-090/K-091 sonrası)
Tarih: 2026-09-20 · Kapsam: yalnız blocker kapanışı + değişen yüzeyler (baştan denetim değil)

## 1. Test sonucu
- Backend: `.venv/bin/python -m pytest -q` → **123 passed** (283s, Atlas uzak, beklenen).
- İstemci: `npx tsc --noEmit` → **0 hata**.

## 2. Bloklayıcı durumu

**B1 (saat dilimi) — KAPANDI.** Üç uç da `bugun`u sorgu parametresi olarak alıyor
(`backend/app/modules/kullanici/kullanici_controller.py:159,179` `Query(...)`;
`backend/app/modules/ozet/ozet_controller.py:181` aynı). İstemci üçünü de sorgu
olarak gönderiyor: `app/src/lib/api.ts:242-244` (`planiKurIstegi`), `:256-258`
(`gunlukLimitiAyarlaIstegi`), `:573-574` (`ozetSeriGetir`) — hepsi `sorguDizesi({ bugun })`
kullanıyor, K-090'daki gövde/sorgu karışıklığı sınıfı tekrar etmiyor. Çağıranlar
(`src/db/limitler.ts:90`, `src/db/profil.ts:155,373`, `src/db/seri.ts:141`) hepsi
`gunAnahtari(new Date())` (yerel gün) geçiyor. K-091'in curl kanıtı (iki farklı gün →
iki farklı Mongo satırı) tutarlı, kod incelemesiyle doğrulandı.
Kalan `datetime.now(timezone.utc)` örnekleri (`kullanici_service.py:246,293`,
`ozet_controller.py:146`, `ozet_service.py:495`) yalnız **belgelenmiş geriye-dönük
uyumluluk düşüşü** (`bugun=None` istisnası, K-087 desenine uygun) — istemci bu
parametreyi her zaman gönderdiği için pratikte tetiklenmiyor; `security.py`/`auth_*`
içindeki `datetime.now()` kullanımları token zaman damgası, meşru sunucu zamanı.
Yeni bulgu yok.

**B2 (yanıltıcı metin) — KAPANDI.** `src/content/metinler.ts` taramasında "sende kalır /
cihazında kalır / sunucuya gitmez / isteğe bağlı (hesap bağlamında) / bağlantısız çalışır"
kalıntısı yok; kalan "isteğe bağlı" kullanımları form alanı bağlamında (not/ürün adı),
hesapla ilgisiz. `hesapsilVeri()` (`metinler.ts:1153`) artık "tüm verilerin silinir"
diyor (K-086 ile tutarlı). `docs/content/metinler.md` de aynı ifadelerle güncel
(§`ayar.hesap.kapali`, `ayar.veri_aciklama`, `hesap.mahremiyet`, `ob.gelir.mahremiyet`).

## 3. Çift sorumluluk taraması — ÖNEMLİ yeni bulgu

**Dead code + stale docstring, çift-yazar riski taşıyor.**
`src/db/limitler.ts:90-103`: `gunlukLimitKaydet` tek çağrılan fonksiyon
(`gunlukLimitiAyarlaIstegi` ile sunucudaki tek-otorite `PUT /gunluk-limit`'e gider).
`gunlukLimitGecmisiKaydet` (satır 101-103, `limitGecmisiYazIstegi`'ni sarar) artık
**hiçbir yerden çağrılmıyor** — `grep` doğrulandı, tek referans kendi tanımı.
`src/db/profil.ts:40`'taki dosya-üstü docstring hâlâ "Yazma
`db/limitler.ts#gunlukLimitKaydet`/`gunlukLimitGecmisiKaydet` üzerinden" diyor; bu
yanlış/eski bilgi — `planKur` (profil.ts:368-374) fonksiyonunun kendi docstring'i
(satır 362-364) doğru şekilde artık ikinci yazma yapmadığını söylüyor, ama dosya
başındaki genel docstring güncellenmemiş. Şu an fonksiyonel bir çift-yazma YOK
(ölü kod çağrılmıyor) ama risk: biri "eksik" sanıp `gunlukLimitGecmisiKaydet`'i
geri bağlarsa K-064/1 sınıfı hata sessizce geri döner. **→ frontend-developer**:
ölü fonksiyonu (`limitler.ts:101-103`) ve kullanılmayan `limitGecmisiYazIstegi`
(`api.ts:426`) sil, `profil.ts:40` docstring'ini güncelle.

Backend tarafında `limit_gecmisi`ye tek yazan `HarcamaService.limit_gecmisi_yaz`
üzerinden, iki çağıran (`plani_kur`, `gunluk_limiti_ayarla`) — ikisi de sunucu
tarafında, çift yazar riski yok. Günlük limitin otoritesi tek: sunucu
(`kullanici_profilleri.gunluk_limit_kurus`); istemci ikinci bir kaynak tutmuyor
(BE-6d, `profil.ts:33-36` doğrulandı).

## 4. Regresyon
Değişen dosyalarda (`api.ts`, `profil.ts`, `limitler.ts`, `metinler.ts`,
`kullanici_service.py`, `kullanici_controller.py`) gözle regresyon bulunmadı;
docstring'ler genelde değişiklikle senkron, tek istisna yukarıdaki `profil.ts:40`.

## SONUÇ (delta)
**Aşama 4 geçti** — iki blocker (B1, B2) kapandı, kanıtlı. Bir ÖNEMLİ (bloklayıcı
olmayan) bulgu var: ölü kod + yanlış docstring (`limitler.ts:101-103`,
`profil.ts:40`) — küçük temizlik, sonraki turda yapılabilir, yayını engellemez.


# 2026-09-22 — çalışma zamanı / geçici test girişi

## Kanıt
- Mevcut Atlas bağlantısında gerçek test çalıştırması: TLS el sıkışması hatası,
  `ServerSelectionTimeoutError`; üç test fixture aşamasında durdu. Atlas üzerinde
  bu tur başarılı doğrulama YOK. Mevcut `.env` ve Atlas verileri değiştirilmedi.
- Ayrı yerel MongoDB 8.0.30, port 27018, `trinkow_test` üzerinde tam pytest:
  **128 passed in 4.21s** (önceki 123 + 5 yeni test).
- `npm test`: **8 passed**. API adres çözümü, geliştirme/üretim giriş ayrımı,
  eşzamanlı 401 tek yenileme, ağ/503 hatasında oturumu koruma, ikinci 401'de
  çıkış, eski isteğin yeni hesabı kapatamaması, oturumsuz istek ve katalog 304.
- `npm run typecheck`: 0 hata. iOS ve Android Metro export başarılı.
- Yeni ASGI entegrasyon testi: rastgele `abc` / `x` → JWT → ben → profil →
  onboarding → 12345 kuruş harcama → pano toplamı → kayıt silme → hesap silme.
- iOS 26.5 / iPhone 17 Pro Max / Expo Go: giriş, onboarding yönlendirmesi,
  günlük, kayıtlar, özet ve ayarlar açılışları kontrol edildi. API istekleri
  200/304 döndü. Test oturumu geçici olarak SQLite'a yerleştirildi; formun
  klavye/dokunma akışı otomatik sürülmedi. Expo Go tanıtım penceresi ekranın
  altını örttüğünden bu kontrol tam görsel veya uçtan uca UI onayı değildir.
  Geçici hesap silindi ve önceki cihaz oturumu geri yüklendi.
- Android cihaz/emülatör etkileşim testi yapılmadı; Android paketleme geçti.

## Düzeltilenler
- Expo ile backend'in ayrı süreçler olması görünür kılındı; `npm run dev`
  yerel MongoDB + API + Expo'yu birlikte başlatır. Veriler `.local/data`da kalıcı.
- Telefonda localhost hatası: Expo host adresi; Android emülatöründe 10.0.2.2.
- Açılışta oturum kontrolü ve gün sınırı yükleme sırası, yönlendirme yarışları,
  giriş/kayıt sonrası çift oturum yayını ve çıkış sonrası korunan rota geçmişi.
- Geçici ağ hatasında oturumun silinmesi; eşzamanlı token yenilemeleri;
  yenilenmiş token tekrar 401 döndüğünde kapanmayan oturum.
- Oturum deposunun DB barrel import döngüsü ve başarısız açılışı tekrar deneyememesi.
- Günlük sınırı, harcama detayı, kaydırarak sil/tekrarla, taksit silme, toast geri alma,
  ayarlar ve profilleme işlemlerinde yakalanmayan Promise hataları.
- Gün sınırı yazımı başarısız olduğunda yalnız cihazdaki günün değişmesi.
- Kayıt yarışında Mongo DuplicateKeyError'ın 500 yerine 409'a çevrilmesi.
- Gerçek e-posta göndermeyen şifre sıfırlamanın sahte başarı ekranı kaldırıldı;
  henüz bağlı olmayan Apple/Google girişleri sessiz kalmak yerine bilgi verir.

## 2026-09-22 tarihsel sınırlar

Bu bölüm önceki çalışma turunun kaydıdır. Aşağıdaki parola sıfırlama ve güvenli
depo maddeleri, 2026-09-23 kabul turunda kapatıldı; güncel durum bir sonraki
bölümdedir.
- Backend test girişi varsayılan kapalı; `TRINKOW_DEV_LOGIN=1` gerekir.
  `dev.py` bunu yalnız ayrı yerel geliştirme DB'siyle açar. Normal giriş değişmedi.
  İstemci üretim derlemesinde test ucunu çağırmaz. Demo şifreleri saklanmaz.
- Atlas erişimi/TLS sorunu dış ortamda hâlâ çözülmeli; yerel geliştirme çalışıyor.
- Apple/Google entegrasyonu, gerçek şifre sıfırlama, bildirim izinleri ve güvenli
  token deposu mevcut açık işlerdir. Bu tur bunları tamamlanmış saymaz.
- Yerel oturum açılışlarını ve API entegrasyonlarını doğrulamak bütün cihazlarda
  her etkileşimin hatasız olduğu anlamına gelmez. Yayın onayı verilmedi.

## 2026-09-23 — Trinkow Rev kabul kanıtı

- Backend: ayrı yerel Mongo test DB'sinde **139/139** geçti.
- Mobil: TypeScript temiz; **14/14** test geçti. Dönen token yarışları, hatırlanan/hatırlanmayan oturum, SQLite→SecureStore göçü, para virgül/nokta/yapıştırma ve negatif biçim kapsandı.
- Finans: Şubat kuruş dağılımı, tarihli bütçe, manuel limit, kategori toplamı, rutin alım/vazgeçme, gelecekteki bütçenin tasarruf sayılmaması, ayrı birikim defteri ve hesap silme koleksiyonları doğrulandı.
- Seri: ilk harcama, ikinci harcamanın aynı günü tekrar saymaması, limit aşımı, son kaydın silinmesi, boş bugün ve kaçırılmış gün senaryoları geçti.
- HTTP smoke: ayrı `trinkow_smoke` DB ve yerel outbox ile kayıt → bütçe → rutin → harcama → tasarruf → reset e-postası → eski oturum iptali → yeni giriş → hesap silme geçti.
- Paket: Expo Doctor **21/21**; iOS ve Android Metro export başarıyla üretildi.
- Native simülatör bundle açıldı ve kırmızı hata ekranı oluşmadı. Expo Go ilk kullanım turu dokunma otomasyonunu örttüğü için gerçek cihaz odak/klavye/küçük ekran matrisi yayın öncesi manuel görev olarak kaldı.
- `npm audit --omit=dev`: high/critical yok; Expo araç zincirinde 14 moderate transitif bulgu var. Audit'in sunduğu çözüm Expo 46'ya uyumsuz düşürme olduğu için uygulanmadı.
