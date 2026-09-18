# HANDOFF — Aşama Devir-Teslim Günlüğü (P-3)

> Aşama başına **3-5 satır.** Karar var, anlatı yok.
> PM'in alt-ajana verdiği brief'in "Bağlam" maddesi buradan kopyalanır —
> ajan geçmişi kazmak zorunda kalmasın diye.

---

## Aşama 0 — Keşif ✅ (kapandı 2026-09-10)
- Proje: Harcama Takip Uygulaması. Harcamayı "kalori sayar gibi" takip
  ettiren davranışsal finans ürünü; günlük limit + kalan limit çubuğu.
- Kapsam **Faz 1 MVP** ile sınırlı: manuel giriş, limit çubuğu, 3 soruluk
  onboarding, offline-first. Oyunlaştırma Faz 2, fiş okuma/açık bankacılık Faz 3.
- `projects/trinkow/docs/CONTEXT.md` (P-1) üretildi — sonraki tüm ajanlar uzun raporu değil
  bunu okur.
- MVP 15 maddelik F-serisi olarak kırıldı (BACKLOG).

## Stack kararı (aşama dışı, 2026-09-10)
- **React Native (Expo) + TypeScript.** Mustafa'da Mac + simülatör var.
- Expo seçildi (çıplak RN değil): `expo-sqlite` + `expo-notifications` hazır
  gelir; `expo prebuild` ile geri çıkış mümkün → tek yönlü kapı değil.
- Faz 1'de **backend YOK** → Python bileşeni yok, iş tamamen frontend'de.
- Sonuç: `agency/reference/rn-tasarim-kisitlari.md` bağlayıcı oldu (hover yok,
  CSS Grid yok, gölge platforma göre değişir, 44pt dokunma hedefi).

## Bağlayıcı kurallar (her aşama için geçerli)
- **EMOJI YASAK** — uygulamanın hiçbir yerinde. Ayırt edicilik gerekiyorsa
  ikon seti kullanılır. (K-004)
- **ÜCRETLİ HİÇBİR ŞEY YOK** (K-009) — servis/araç/API/font/ikon/hosting.
  Ajanlar ücretli çözümü seçenek olarak bile sunmaz. Ücretsiz yol yoksa
  özelliği Faz 1'den çıkarmayı öner. Mağaza ücretleri de Faz 1 dışı.
- **Ton:** limit aşımında kullanıcıyı utandırma. Farkındalık veren, sakin,
  yargısız. Finans uygulamalarının suçlayıcı dil + kırmızı-ünlem refleksine
  düşme.
- **Konumlandırma:** YNAB'ın katılığı ile Fortune City'nin oyuncaklığı
  ARASINDA. "Basit ve günlük ama oyuncak değil."
- **Para float ile tutulmaz** (kuruş integer). Gün sınırı/saat dilimi mantığı
  ürünün çekirdeği — "bugün" ne zaman biter?

## Aşama 1 — Marka ✅ (ONAYLANDI 2026-09-10)
- `projects/trinkow/docs/brand/brandbook.md` TASLAK üretildi (868 satır, 7 bölüm + ekler).
- İki yön sunuldu: **A "Defter"** (kağıt/mürekkep, açık tema, Source Serif 4
  + Public Sans) ve **B "Ölçüm Aleti"** (grafit, karanlık-öncelikli,
  IBM Plex). Ajan ve PM A'yı öneriyor.
- PM denetimi GEÇTİ: 15 kontrast çifti bağımsız yeniden hesaplandı, tutuyor.
  Emoji yasağı §2.6'da kesin. Ücretli bağımlılık yok (OFL/MIT).
- **Bloklayıcı: ÜRÜN ADI YOK.** Logo ve tasarım adsız ilerleyemez.
  Öneriler: Kalan / Çentik / Eşik.
- **ONAYLANDI (K-006).** Kararlar: ürün adı **Trinkow** · **Yön A "Defter"** ·
  karanlık mod Faz 1'de YOK · kategoriler renk taşımaz · Faz 2 oyunlaştırma
  kuralı şimdi genişletilmeyecek.
- ✅ **Brandbook v1.0 NİHAİ** (1060 satır) + **`projects/trinkow/docs/brand/tokens.md` (P-2)**
  üretildi (434 satır, 46 aktif token + 13 kontrast çifti + 9 bileşen ölçü
  tablosu + design-reviewer için 15 maddelik grep denetim listesi).
- **Logo:** wordmark = Source Serif 4 SemiBold, tracking −1.8%, canlı metin
  (ek font dosyası yok). Monogram = "T" + tek dikey çentik, hikâye
  "eşik ve kalan" — cüzdan/kumbara/yükselen ok klişesine girilmedi.
  App icon daima monogram (wordmark 60pt'de okunmaz). Splash Kağıt zeminli.
- Yön B ve karanlık mod ARŞİV/FAZ 2 olarak işaretli, silinmedi.
- Fontlar OFL, ikonlar MIT/ISC → **ücretli bağımlılık yok** (K-009 uyumlu).

### tokens.md kullanım notu (sonraki ajanlar için)
- Değerlerin **tek kaynağı** tokens.md. Düzyazı brandbook'u ayrıştırma.
- Bilinen iki istisna (denetimde takılma): splash'teki 32pt wordmark tip
  ölçeği dışıdır (bilinçli); `screen-padding-x: 20` spacing skalası
  dışıdır (taslakta onaylanmıştı). İkisi de denetim listesinde izinli.
- Faz 2 uyarısı: karanlık mod `surface/bg` ayrımı 1.09:1 — Faz 2'ye
  geçildiğinde tek başına yetmeyecek, hairline gerekecek.

### Sonraki aşamaların bilmesi gerekenler (BAĞLAYICI)
- İlerleme çubuğu **doluluğa göre renk değiştirmez.** Trafik ışığı
  (yeşil→sarı→kırmızı) marka kararıyla reddedildi; taşma ayrı segment
  olarak Kiremit ile çizilir. Kırmızı yalnızca silme onayına ayrılmıştır.
- Gölge kullanılmıyor (§6.4) — katman ayrımı yüzey tonu ve çizgiyle.
- Kategoriler renk taşımaz, ikon+metinle ayrışır (§3.4).


## Aşama 2 — UI/UX Tasarım 🔄 + Aşama 6 — Büyüme 🔄 (paralel, başladı 2026-09-10)
- Aşama 6: ✅ analiz bitti → `projects/trinkow/docs/social/analiz-raporu.md`.
  **Tek somut bulgu:** yerel rakip **Bütçem** (butcemapp.com) — "siz" hitabı,
  yoğun emoji, motivasyonel/oyunlaştırılmış ton. Trinkow'un sen/emojisiz/
  yargısız sesi buna karşı net ayrışıyor. Bu **doğrulanmış** (tahmin değil).
  Kalan veri (hashtag, etkileşim, Ekşi/Reddit) erişilemedi → veri yok.
  Stratejist "ton boşluğunu" kanıtlanmış trend değil, gözlemlenen fırsat
  olarak kullanacak. Ücretli araç alınmadı (K-007).
- Aşama 2: brandbook nihai olur olmaz ui-ux-designer devreye alınacak
  (P-4 metinler, P-5 referans seti, P-6 varlık kilidi, P-7 bileşen envanteri
  → sonra ekran tasarımı → design-reviewer denetimi).
- Tasarımcıya bağlayıcı: `agency/reference/rn-tasarim-kisitlari.md` (hover yok,
  CSS Grid yok, 390×844, 44pt dokunma hedefi, safe area).


## Aşama 2 TUR 1 (temel) + Aşama 6 (takvim) 🔄 başladı 2026-09-10
- ✅ **ui-ux-designer TUR 1 bitti** — 5 dosya, 1185 satır, tek ekran çizilmedi.
  `bilesen-envanteri.md` (27 bileşen + durum sözlüğü) · `varliklar.md`
  (Lucide 1.43.0, ISC, 1.75 çizgi) · `metinler.md` (20 bölüm, i18n anahtarlı,
  gerçek Türkçe, placeholder yok, emoji yok) · `referans-repolar-trinkow.md`
  (12 kalem) · `ekran-envanteri.md` (15 yüzey, 7 akış, ekran×durum matrisi).
- **Harcama girişi: 3 dokunuş** (Ekle → kategori → Kaydet; tutar alanı
  otomatik odaklı). "Tekrarla" kısayolu 2 dokunuş.
- PM doğrulaması: `lucide-react-native@1.43.0` npm'de gerçek, en güncel, ISC.
  **Ancak** ajanın "eski ikon isimleri kaldırıldı" uyarısı FAZLA KESİNDİ —
  `Home`/`Trash2`/`HelpCircle` alias olarak hâlâ export ediliyor (paket
  indirilip doğrulandı). `varliklar.md` düzeltildi: yeni isimleri kullan,
  ama eski isimli kodu "bozuk" sanıp acele düzeltme.
- **K-011:** fontlar `@expo-google-fonts/*` ile gelecek (ücretsiz, statik TTF).
  `expo-haptics` onaylandı — ölçülü kullanılacak (yalnızca kayıt onayı +
  limit eşiği; her dokunuşta titreşim marka ihlali).
- **K-012 AÇIK:** "Sigara" kategorisi kalsın mı? PM önerisi: varsayılan
  listede olmasın, kullanıcı isterse kendi eklesin.
- ✅ **social-media-strategist bitti** → `projects/trinkow/docs/social/icerik-takvimi.md`
  4 hafta / 16 içerik. Instagram (birincil) + X (ikincil); TikTok, LinkedIn,
  Threads gerekçeli olarak dışarıda. 4 içerik sütunu, her biri test edilebilir
  bir hipoteze bağlı. Ölçüm: takipçi değil — bekleme listesi kaydı,
  kaydetme/paylaşma oranı, yorum niteliği.
  PM denetimi geçti (emoji 0, marka adı doğru, ücretsiz, yalan vaat yok).
  5 madde Mustafa'da → K-010. Yayın zamanlaması önerisi: Faz 1 kodlaması
  bitmeye yaklaşınca başlat (şimdi başlamak solo geliştiriciden dikkat çalar).


## Aşama 2 TUR 2 🔄 (başladı 2026-09-10)
- 15 yüzeyin 390×844 HTML/CSS prototipi. Öncelik: Bugün/pano (ilerleme
  çubuğu), harcama girişi (3 dokunuş), onboarding — bunlar kusursuz olacak.
- K-012 uygulanıyor: "Sigara" → "Alışkanlıklar", ikon da değişiyor.
- Ek çıktı: sosyal medya tipografik kart şablonu (tokens.md'den beslenen
  HTML/CSS — Canva değil) + monogramdan profil görseli.
- ✅ **Prototip üretildi:** `projects/trinkow/docs/design/prototip/` — 7 HTML + `stil.css` +
  4 gömülü TTF. Ekranlar Python üreteçle (`_uret/*.py`) üretilmiş; HTML
  elle değil kodla yazılmış, tekrar üretilebilir.
- **PM ön taraması TEMİZ:** yasak CSS kalıplarının (`:hover`, `grid`,
  `::before`, `calc(`, `z-index`, `transition`…) tamamı yalnızca
  `stil.css` satır 4-5'teki "bilinçli kullanılmayanlar" yorum bloğunda.
  Gerçek ihlal yok. Emoji yok, lorem yok.
- İki API kesintisi yaşandı (biri bağlantı, biri stall) — ikisi de altyapı
  kaynaklı, ajan hatası değil. İkinci turda "parça parça yaz, her ekranı
  anında kaydet" talimatı verildi; iş tamamlandı.
- 🔄 **design-reviewer denetimde.** REVİZE bloklayıcıdır; PASS almadan
  Mustafa'ya görsel onaya gidilmez.


## Aşama 2 — TASARIM ÜRETİMİ TAMAM (2026-09-12)
- **`projects/trinkow/docs/design/prototip-v3/` — 12 ekran + index, 53 yüzey.** Faz 1'in
  15 yüzeyinin tamamı çizildi.
- Görsel dil: **claymorphism** (K-024). Üç yön denendi: Yön A "Defter"
  (reddedildi, "ruhsuz") → Yön C "Gün Işığı" (reddedildi, "rezalet") →
  **claymorphism (onaylandı)**. Boşluk ritmi ayrı turda düzeltildi (K-025/26).
- `tokens.md` v3.1 · `bilesen-envanteri.md` v3.1 (33 bileşen) ·
  `varliklar.md` v3.1 · `ekran-envanteri.md` güncel.
- Denetim: `_uret/denetim.py` → 53 yüzey, 0 bulgu. PM bağımsız doğruladı.

### Sonraki aşamanın (Aşama 3 / frontend) bilmesi gerekenler
- **Expo New Architecture ŞART** — clay'in inset gölgesi buna bağlı.
  Outset Android 9+, **inset Android 10+**, iOS sorunsuz.
- Clay gölge katmanları `tokens.md §5`'te `boxShadow` dizesi olarak hazır:
  kabarık 4 katman · basılı 3 · çukur 2. **Birebir kopyalanacak**, `elevation`
  kullanılmıyor.
- **`₺` glifi:** Montserrat ✅ · Poppins ✅ · JetBrains Mono ❌ (projeden
  çıkarıldı). Rakamlar **Montserrat tabular**.
- **Para kuruş cinsinden integer**, float değil.
- Birincil buton zemini `primary-deep #2F68C5` (AA için); `#3B82F6` yalnız
  metinsiz dolgu.
- Silme: tek harcama → **6 sn geri al toast'ı**, diyalog yok. Taksit serisi →
  diyalog var (K-029).
- `<main>` içi flexbox-only; inline SVG → `react-native-svg`,
  `overflow-y:auto` → `ScrollView` (`.kaydir` olarak işaretli).

### Ürün backlog'u (Faz 2+, K-030/K-031)
Ürün arama/barkod araştırıldı: TR'de ücretsiz güvenilir fiyat verisi YOK
(Open Prices'ta TRY cinsinden 27 kayıt). Barkod→isim bile güvenilmez
(uydurma barkod "riso basmati raja" döndürdü). Çözüm: **Ü-1 sık alınanlar**
(kullanıcı hafızası, 0 maliyet) + **Ü-2 gömülü tütün fiyat listesi**
(TR'de tütün ulusal tek fiyat). Ücretli fiyat API'si reddedildi.


## Aşama 3 — Yürüyen iskelet ✅ (2026-09-12)
- Uygulama simülatörde çalışıyor. `projects/trinkow/app` · 31 dosya · tsc temiz.
- **Clay RN'de tuttu** (K-039) → kalan 14 ekranın önü açık, tasarım dili
  değişmiyor.
- Çalıştırma: `cd projects/trinkow/app && npx expo start --ios`
- Ekran görüntüleri: `app/.onizleme/` (gitignore'da)
- **RN'e özgü tuzak (tekrarlamasın):** SVG `stop-color` **alfa taşımaz** →
  saydamlık `stopOpacity` ile verilir. Tarayıcıda fark edilmez, RN'de opak çıkar.
- Örnek veri `ORNEK_VERI_SURUMU` ile sürümlü; kullanıcı verisi varsa dokunulmaz.


## Aşama 3 — D-2a günlük döngü ✅ (2026-09-17)
- E-11 ekle · E-12 detay/düzenle · E-13 taksit silme onayı · E-14 kayıtlar ·
  sekme navigasyonu · **Akış C** kaydırma. 51 dosya, `tsc` 0 hata,
  **yeni bağımlılık yok** (20'de sabit). Uygulama günlük kullanım için tam.
  ⏳ Mustafa'nın simülatörde gözle doğrulaması bekliyor.
- İki tur sürdü: 1. turda E-12'de **tutar salt okunurdu** (F-8'i boşa
  çıkarıyordu) ve **Akış C hiç yoktu** — ikisi de geri gönderilip kapatıldı (K-041).
- Sil/Tekrarla mantığı tek yerde: `src/lib/harcamaEylemleri.ts`.
  Kaydırma `gesture-handler`'ın `Swipeable`'ı; `_layout.tsx`'te
  `GestureHandlerRootView` **şart** (eksikti, eklendi).
- **Taksitli kayıtta tutar düzenlenemez** — tek taksitin tutarını değiştirmek
  serinin toplamıyla tutarsızlaşır. Kilit nedeni `InfoStrip` ile söyleniyor.
- Metin senkronu yapıldı: `metinler.md` ↔ `metinler.ts` (P-4 kuralı).

### Sonraki turun (D-2b) bilmesi gerekenler
- **K-043 devri:** `ExpenseRow` kaydırmalı sil zemini `groove` → `danger-soft`,
  metin/ikon → `danger-ink`. Sebep: `tokens.md` §1.3 ile §7.3 çelişiyordu;
  karar "doygunluk riskle orantılı" — kırmızı ailesi evet, tam doygunluk hayır.
- **D-1b doküman senkronu 3 maddeye çıktı:** K-040 (çip halkası) +
  K-042 (8+ karakterde tutar küçültme) + K-043 (kaydırma rengi).
- Devralma kuralı (K-042): oturum devralırken `src/` içinde çelişki
  işaretlerini tara (🔴 / "çelişki" / "rapora bildirildi") — kesilen bir
  oturumun bulguları rapora hiç ulaşmamış olabilir.

## Aşama 3 — Geliştirme, 2. tur (2026-09-17)
- **D-1b ✅** doküman↔kod senkronu kapandı. `tokens.md` artık iki kuralı açıkça
  yazıyor: seçili çipte/kategori kutusunda **halka yoktur** (§7.6), 8+ karakterli
  tutarda tip ölçeği **`hero`→`display` iner** (§7.11).
- **D-2b ✅** anlama ekranları kodlandı (E-15/16/17/18), 8 yeni bileşen,
  `db/limitler.ts` + `db/ozet.ts`. tsc 0 hata, yeni bağımlılık yok.
- **Ders (K-046):** Bir ajan "prototip ile metin dosyası çelişiyor" dedi; denetleyince
  çelişki **`metinler.md`'nin kendi içindeydi** (E-15 iki kez tanımlı, §7 vs §22.1).
  → Ajanın "çelişki" raporunu olduğu gibi kabul etme, **nerede olduğunu doğrula.**
- **Bloklu:** D-2c, K-044 (giriş/kayıt + Google/Apple) kararı gelene kadar başlamaz.
  Bu karar açılış + onboarding akışının tamamını belirliyor.
- Sıradaki iş **D-3 (qa-engineer)** — D-2c'yi beklemez, 8 kodlanmış ekran test edilebilir.
