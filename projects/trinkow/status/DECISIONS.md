# Kararlar

Bu dosya, PM ajanının Mustafa'nın onayını beklediği veya Mustafa'nın verdiği
kararları içerir. Her madde: tarih, konu, seçenekler, (varsa) karar.

---

## K-001 — Proje dökümanı eksik
- Tarih: 2026-09-09
- Durum: ✅ **KAPANDI (2026-09-10)** — Mustafa
  `projects/trinkow/docs/Harcama Takip Uygulaması Rapor ve Dökümantasyonu.txt` dosyasını ekledi.
  PM okudu, `projects/trinkow/docs/CONTEXT.md` (P-1) üretildi, MVP kapsamı BACKLOG'a işlendi.

### Sorun
`projects/trinkow/docs/` klasöründe bir proje tanımı yok. İçindeki iki dosya sistemin kendi
referansları (brandbook şablonu ve anti-pattern listesi), proje dökümanı değil.
Ne inşa edileceği bilinmediği için ne MVP kapsamı çıkarılabiliyor ne de
brand-strategist görevlendirilebiliyor.

### Mustafa'dan istenen
`projects/trinkow/docs/` klasörüne bir döküman ekle (ör. `projects/trinkow/docs/proje.md`). İçinde en az şunlar olsun:

1. **Ürün nedir?** 2-3 cümlelik tanım. Ne yapar, hangi problemi çözer?
2. **Kim kullanacak?** Hedef kitle / kullanıcı profili.
3. **MVP kapsamı.** İlk sürümde MUTLAKA olması gereken özellikler
   (ve varsa açıkça "şimdilik yok" denen şeyler).
4. **Ürün tipi.** Web uygulaması mı, pazarlama sitesi mi, iç araç mı,
   mobil mi? (UI/UX ve teknoloji kararlarını bu belirliyor.)
5. **Marka ipuçları.** Varsa isim, ton (ciddi/samimi/teknik), rakipler,
   beğendiğin/beğenmediğin örnekler. Yoksa brand-strategist sıfırdan önerir.
6. **Kısıtlar.** Deadline, bütçe, kullanılması/kullanılmaması gereken
   teknolojiler, dil (TR/EN/çift dil).

Eksik madde olursa sorun değil — PM eksikleri soru olarak buraya yazar.
Belirsizlik kalırsa CLAUDE.md gereği tahmin yürütülmez, sorulur.

### Alternatif
Yazılı döküman hazırlamak istemezsen, projeyi sohbette anlat; PM bunu
`projects/trinkow/docs/proje.md` olarak yazıp onayına sunar, onay sonrası Aşama 0 kapanır.


---

## K-002 — React hangi hedefe? ✅ KARAR VERİLDİ
- Tarih: 2026-09-10
- Durum: ✅ **KAPANDI (2026-09-10).** Mustafa: *"Direct React Native'de
  yapalım. Mac'im ve emülatörüm var."*
- **KARAR: Seçenek A — React Native.** Hedef gerçek mobil uygulama.
  Mac + simülatör mevcut → iOS tarafında hiçbir engel yok.
- Bloklayıcı kalktı; Aşama 3'ün önü açık (Aşama 2 tamamlanınca).

### Çelişki
Mustafa "React'ta yazılsın" dedi. Rapor ise ısrarla **mobil uygulama**
diyor: "yeni nesil bir mobil uygulama", **iOS Live Activities** ile kilit
ekranı çubuğu, "metrodan geçerken giriş" (offline), yerel **SQLite**.

"React" iki farklı ürüne çıkar. İkisi de React'tir, ama **UI kodu birbirine
taşınmaz** (React DOM ↔ React Native primitifleri). Sonradan dönmek,
arayüzü yeniden yazmak demektir. Bu yüzden şimdi karar verilmeli.

### Seçenek A — Expo (React Native)  ⭐ PM ÖNERİSİ
Gerçek mobil uygulama, App Store/Play Store'a çıkabilir.
- ✅ Rapordaki mimariyle birebir örtüşür: `expo-sqlite` ile offline-first,
  gerçek bildirim, ileride Live Activities mümkün.
- ✅ **Geliştirme maliyeti $0.** `npx expo start` → telefonda Expo Go
  uygulamasıyla QR okutup canlı çalışır. Mac/Xcode gerekmez.
- ✅ `react-native-web` ile **web'e de export edilebilir** — tek kod tabanı,
  iki hedef. Yani web seçeneğini kapatmıyoruz.
- ✅ Faz 2 (streak/XP) bildirim gerektirir; native bildirim burada hazır.
- ❌ Mağazaya çıkmak ücretli: Apple $99/yıl, Google $25 (tek sefer).
  **Ama bu Faz 1'de gerekmiyor** — test cihaza doğrudan kurulur.
- ❌ Web'e göre biraz daha ağır kurulum.

### Seçenek B — React + Vite (web PWA)
Tarayıcıda çalışır, telefon ana ekranına eklenebilir.
- ✅ En hızlı başlangıç, `npm run dev` ve bitti. Dağıtım ücretsiz statik
  hosting; mağaza onayı/bekleme yok, anında güncelleme.
- ✅ Gerçekten $0 — mağaza ücreti bile yok.
- ❌ iOS'ta sınırlı: **Live Activities yok**, bildirimler zayıf ve ancak
  kullanıcı "ana ekrana ekle" derse çalışır → funnel'da ciddi kayıp.
- ❌ SQLite yerine IndexedDB (Dexie) gibi bir çözüm gerekir.
- ❌ Faz 2'ye geçerken native'e dönülürse **arayüz baştan yazılır.**

### PM önerisi ve gerekçesi
**Seçenek A (Expo).** Üç sebep:
1. Ürünün tezi "satın alma anında farkındalık". Bu, telefonun kilit
   ekranında/bildiriminde var olmayı gerektirir — web'in iOS'ta en zayıf
   olduğu nokta tam olarak burası.
2. Geliştirme aşamasında maliyet **her iki seçenekte de $0.** Para sadece
   mağaza dağıtımında devreye giriyor ve o Faz 1'de gerekmiyor. Yani
   "PWA daha ucuz" avantajı pratikte yok.
3. `react-native-web` sayesinde web'i sonradan açabiliriz; tersi mümkün
   değil. A seçeneği B'yi kapsıyor, B seçeneği A'yı kapsamıyor.

### Kararı belirleyen soru (Mustafa'ya)
**Bu uygulamayı gerçekten mağazaya koyup insanların telefonuna kurmasını mı
istiyorsun, yoksa önce 10-20 kişiyle link üzerinden hızlı test mi?**
- Mağaza / gerçek ürün hedefi → **A (Expo)**
- Önce hızlı doğrulama, link yeter → **B (PWA)**

---

## K-003 — Faz 1'de Python yok (BİLGİ — onay gerekmiyor)
- Tarih: 2026-09-10
- CLAUDE.md "backend/iş mantığı Python" diyor. Ancak Faz 1 **sunucusuz ve
  offline-first**; backend yok. Dolayısıyla Faz 1'de `python-developer`
  devrede olmayacak, iş tamamen `frontend-developer`'da.
- Python, Faz 3'te (fiş okuma API'si, açık bankacılık) devreye girer.
- **Sistem etkisi:** `qa-engineer` preprompt'u sadece `pytest` biliyordu;
  TS/JS test koşucusunu (Vitest/Jest) de tanıyacak şekilde güncellendi.
  Aksi halde Faz 1'de test edilecek Python kodu olmadığı için QA aşaması
  boşa düşerdi.


---

## K-004 — Emoji: uygulamada KULLANILMAZ (Mustafa kararı, kesin)
- Tarih: 2026-09-10 (güncellendi)
- Mustafa: *"Emoji falan kullanma uygulamada."*
- **Kural:** Uygulama arayüzünde, metinlerinde, bildirimlerinde emoji yok.
  Rapordaki emoji'li onboarding örnekleri geçersiz.
- Ayırt edicilik gereken yerde emoji değil **ikon seti** (P-6) kullanılır —
  ikon markanın çizgi kalınlığına/rengine uyar, emoji her cihazda farklı
  görünür ve markayı taşımaz.
- `projects/trinkow/docs/CONTEXT.md`'ye bağlayıcı kural olarak yazıldı → tüm ajanlar okur.
- Not: Global `jenerik-ai-ui-anti-pattern-listesi.md`'deki emoji maddesi
  Mustafa tarafından kaldırılmıştı; o dosya TÜM projeler için geçerli
  olduğundan bu proje-özel kural CONTEXT.md'de tutuluyor. İleride başka
  projede emoji serbest kalabilir.

### (Önceki kayıt — geçersiz)
- Tarih: 2026-09-10
- Mustafa `agency/reference/jenerik-ai-ui-anti-pattern-listesi.md`'den
  "Başlıklarda/ikonlarda emoji kullanımı" maddesini çıkardı.
- Gerekçe (PM yorumu): fizibilite raporu onboarding'de emoji'li niyet
  butonları öneriyor ("🚀 Yatırım İçin / 🛡️ Borç Kapatmak / 📊 Sadece
  Takip"); emoji burada dekorasyon değil hızlı ayırt edici işlevi görüyor.
- **Uygulandı:** `projects/trinkow/docs/CONTEXT.md` buna göre güncellendi. Tasarımcıya not:
  emoji serbest ama ölçülü — ayırt edicilik sağladığı yerde kullanılır,
  her başlığa serpiştirilmez. Kullanım kuralını brandbook netleştirecek.


---

## K-005 — React Native kurulumu: Expo (PM teknik kararı)
- Tarih: 2026-09-10
- Durum: **UYGULANACAK.** Ücretli bağımlılık içermediği için CLAUDE.md
  uyarınca PM kararıdır; itirazın varsa değiştiririz.

### Karar
**Expo** (managed + dev build) kullanılacak, çıplak React Native CLI değil.

### Gerekçe
- `expo-sqlite` (offline-first veritabanı — F-13'ün temeli),
  `expo-notifications` (Faz 2 streak hatırlatmaları) hazır ve bakımlı gelir.
  Çıplak RN'de bunların her biri ayrı native kurulum işi.
- Mac + simülatör olduğu için **dev build** kullanabiliriz: Expo Go'nun
  kısıtlarına takılmadan istediğimiz native modülü ekleriz.
- **Kilitlenme yok:** `npx expo prebuild` ile `ios/` ve `android/` klasörleri
  üretilir, istenirse çıplak RN'e geçilir. Tek yönlü kapı değil.
- Tek kişilik geliştirici + $0 bütçe kısıtına en uygun seçenek: native
  yapılandırmayla uğraşmak yerine ürün mantığına vakit kalır.

### Faz 1'de kullanılacak (hepsi ücretsiz)
`expo`, `expo-sqlite`, `expo-router` (navigasyon), `react-native-svg`
(ilerleme çubuğu için), TypeScript. **Ücretli servis yok, sunucu yok.**

### Not
Mağaza dağıtımı (Apple $99/yıl, Google $25) Faz 1 kapsamında DEĞİL;
gerektiğinde ayrı onay maddesi açılacak (CLAUDE.md → ücretli servis).


---

## K-006 — BRANDBOOK ONAYI ✅ ONAYLANDI (Aşama 1 → 2 geçişi)
- Tarih: 2026-09-10
- Dosya: `projects/trinkow/docs/brand/brandbook.md` (868 satır, TASLAK)
- Durum: ✅ **ONAYLANDI (2026-09-10).** Mustafa: *"Trinkow Uygulama ismi
  olsun. onaylıyorum diğer adımlara başla"*
- **Aşama 1 kapandı. Aşama 2 + Aşama 6 açıldı.**

### VERİLEN KARARLAR
1. **Ürün adı: Trinkow** (Mustafa'nın kararı).
2. **Yön A — "Defter"** seçildi. Yön B arşive alındı.
3. Karanlık mod **Faz 1'de YOK** (PM önerisi onaylandı) → Faz 2'ye bırakıldı.
4. Kategoriler **renk taşımaz**, ikon+metinle ayrışır (§3.4 onaylandı).
5. Faz 2 oyunlaştırma kuralı **şimdi genişletilmeyecek**; Faz 2'ye gelince
   oyuncaklaştırmayan bir "ilerleme dili" ayrıca tanımlanacak.

> PM notu: Mustafa "onaylıyorum" derken 1 numaralı soruya (yön) ayrı yanıt
> vermedi. PM görüşü A idi ve toptan onay olarak yorumlandı. Yanlışsa
> geri dönüş maliyeti düşük — tasarım henüz başlamadı.

### Yapılacak düzeltmeler (brand-strategist'e iletildi)
- Ürün adı Trinkow her yere işlenecek, §5 Logo bölümü artık doldurulabilir.
- Yön B arşiv olarak işaretlenecek (silinmeyecek — gerekçe kalsın).
- İki sayı düzeltmesi: `accent-soft` 7.8 → **8.06:1**, karanlık yüzey
  ayrımı 1.4 → **1.09:1**.
- `projects/trinkow/docs/brand/tokens.md` (P-2) üretilecek.

### PM kalite denetimi: GEÇTİ
- Şablonun 7 bölümü + karar maddeleri + anti-pattern uyum tablosu dolu.
- Emoji yasağı §2.6'da kesin kural olarak yazılmış; dokümandaki tek 🚀
  rapordan alıntı ve açıkça "geçersiz" etiketli. Uygulamaya emoji girmiyor.
- Inter/Poppins/Montserrat sadece "neden bunlar değil" bağlamında geçiyor.
- **Kontrast iddiaları bağımsız doğrulandı:** 15 renk çiftinin tamamı
  PM tarafından yeniden hesaplandı, brandbook'un yazdığı oranlarla tutuyor
  (ör. 15.4 / 9.0 / 6.4 / 5.2 / 14.6 / 6.8). Ajan "AA" diye yazıp geçmemiş,
  gerçekten hesaplamış.
- İki önemsiz sayısal düzeltme (bloklamaz, tasarım öncesi düzeltilir):
  `accent-soft` çifti 7.8 değil **8.06:1**; karanlık mod yüzey ayrımı
  1.4 değil **1.09:1** (zaten "kasıtlı zayıf" olarak işaretli).
- Ücretli bağımlılık yok: fontlar OFL, ikon setleri MIT/ISC.

### Karar 1 — Hangi yön?
**A) "Defter"** (ajanın önerisi) — kağıt+mürekkep, açık tema.
Kağıt `#F4F1EA` / mürekkep `#1B1A17` / vurgu Petrol `#14484C` /
limit-dışı Kiremit `#A24A2A`. Source Serif 4 + Public Sans.
Kişilik: Sakin · Dürüst · Yargısız · Ölçülü.

**B) "Ölçüm Aleti"** — grafit, karanlık-öncelikli, telemetri estetiği.
`#0E1110` / metin `#E8EDEB` / vurgu Sinyal Amber `#E8A33D`.
IBM Plex Sans + Plex Mono. Kişilik: Kesin · Nötr · Teknik · Sessiz.

**PM görüşü:** A. Pazar (YNAB/Copilot/Monarch) parlak-kurumsal veya
steril-beyaz; sıcak kağıt+serif alanı boş → ayrışma buradan gelir.
Ayrıca projenin en kritik kısıtı olan "yargısız, utandırmayan" ton bir
defterden doğal çıkıyor, bir ölçüm aletinden çıkmıyor.
**B'nin tek somut avantajı:** karanlık-öncelikli olduğu için tek tema
geliştirmek yeterli → tek kişilik ekipte gerçek maliyet avantajı.

### Karar 2 — ÜRÜN ADI YOK (kritik)
Ne fizibilite raporunda ne CONTEXT.md'de ürün adı var. Ajan **uydurmadı**
(doğru davranış). Logo bölümü (§5) bu karara bağlı, tasarım da adsız
ilerleyemez.
Ajanın önerileri: **"Kalan"** · **"Çentik"** · **"Eşik"**.
Kendi adın varsa o geçerli. Seçilince App Store'da isim çakışması ve
marka tescili ayrıca kontrol edilmeli.

### Karar 3 — Karanlık mod Faz 1'de olacak mı?
Ayrı tasarım gerektirir (renk ters çevirme yasak) → ek tasarım+kod maliyeti.
**PM görüşü:** Yön A seçilirse Faz 1'de ATLA, Faz 2'ye bırak. Yön B
seçilirse zaten karanlık-öncelikli, soru ortadan kalkıyor.

### Karar 4 — Kategoriler renk taşımasın (§3.4)
Öneri: her kategoriye ayrı renk verilmez; ikon + metinle ayrışır.
**PM görüşü:** Onayla. 10+ kategoriye renk vermek paleti dağıtır ve
"limit aşımı" sinyalinin gücünü çalar — o sinyal ürünün çekirdeği.

### Karar 5 — Faz 2 oyunlaştırma sınırı
Marka şu haliyle rozet/seviye/karakter'e KAPALI. Faz 2'de XP/streak
gelecekse kural şimdi genişletilmeli.
**PM görüşü:** Şimdi genişletme. Faz 2'ye gelince markayı oyuncaklaştırmayan
bir "ilerleme dili" ayrıca tanımlanır — erken açarsak tam da kaçındığımız
Fortune City ucuna kayarız.


---

## K-007 — Ücretli sosyal dinleme aracı ❌ REDDEDİLDİ
- Tarih: 2026-09-10
- Kaynak: social-media-analyst raporu. Hashtag/format performansı ve rakip
  etkileşim verisi web aramasıyla erişilemiyor; ancak platform-içi veri
  veren ücretli bir araçla (sosyal dinleme) alınabilir.
- Ücretli bağımlılık = CLAUDE.md onay maddesi.
- **KARAR (2026-09-10): HAYIR.** Mustafa: *"şu anda paralı olan rakip
  analizi falan hiçbir şeye onay vermiyorum."*
- Kapsam sadece bu araç değil → **K-009**'a bakınız (genel kural).

**PM önerisi: ŞİMDİ ALMA.** Gerekçe:
1. Trinkow yayında değil, kullanıcısı ve hesabı yok. Ölçülecek kendi
   verimiz yok; araç sadece rakip verisi verir.
2. Faz 1 kısıtı **$0**. İlk harcama kalemi bir analiz aracı olmamalı.
3. Analistin bulduğu tek somut ayrışma noktası (Bütçem'in emoji+motivasyonel
   tonu) zaten ücretsiz doğrulandı — strateji kurmak için yeterli.
4. Doğru sıra: önce ucuz A/B testi yap, **kendi** verini üret; araç ancak
   optimize edilecek gerçek bir hesap varken anlamlı.

**Yeniden değerlendirme:** Trinkow yayına girip sosyal hesap açtıktan sonra.

---

## K-008 — Pazar analizinin sığlığı (BİLGİ — aksiyon gerekmiyor)
- Tarih: 2026-09-10
- social-media-analyst yalnızca **n=2** rakip doğrulayabildi (Bütçem,
  Fast Budget). Hashtag performansı, Reddit/Ekşi tartışmaları, App Store TR
  keşif mekanizması → **veri yok**, uydurulmadı.
- **PM değerlendirmesi: çıktı KABUL EDİLDİ.** Ajan doğru davrandı; boşluğu
  spekülasyonla doldurmadı ve her bulguyu kaynak/güven etiketiyle verdi
  (5 kez açıkça "[veri yok]"). Bu tam olarak istenen davranıştır —
  dürüstlüğü cezalandırıp tekrar görevlendirmek, sistemi uydurmaya iter.
- Tekrar denenmedi: eksik veri (Instagram/TikTok platform-içi metrikleri)
  web aramasıyla erişilebilir değil; aynı görevi tekrarlamak aynı sonucu
  verirdi.
- **Stratejiste bağlayıcı not:** "ton boşluğu" bulgusu *kanıtlanmış trend*
  değil **gözlemlenen fırsat** olarak kullanılacak. Strateji buna göre
  temkinli kurulacak, kesin pazar iddiası yazılmayacak.


---

## K-009 — ÜCRETLİ HİÇBİR ŞEY YOK (kalıcı kural, Faz 1 boyunca)
- Tarih: 2026-09-10
- Mustafa: *"şu anda paralı olan rakip analizi falan hiçbir şeye onay
  vermiyorum."*

### Kural
Faz 1 boyunca **hiçbir ücretli servis, araç, API, kütüphane, font, ikon
seti, hosting veya abonelik kullanılmaz.** Varsayılan cevap HAYIR'dır.
Bu tek bir aracın reddi değil, genel bir duruştur.

### Ajanlar için bağlayıcı
- Ücretli bir şeye **ihtiyaç duyan çözüm önerme.** Ücretsiz yol yoksa
  önce "bu özellik Faz 1'den çıkarılabilir mi?" diye sor.
- Ücretli araç, "şuna da bakılabilir" diye seçenek olarak bile sunulmaz —
  PM'in önüne getirilmez, doğrudan elenir.
- Lisans kontrolü zorunlu: font OFL, ikon MIT/ISC/Apache gibi ücretsiz ve
  ticari kullanıma açık olmalı. Şüpheliyse kullanma.
- **Zaten uyumlu olanlar:** brandbook fontları (Source Serif 4, Public Sans)
  OFL; ikon setleri MIT/ISC; Expo + expo-sqlite + expo-router +
  react-native-svg ücretsiz; sunucu yok, backend yok → hosting maliyeti yok.

### Faz 1 dışına ertelenenler (şimdi gündeme getirilmeyecek)
- Apple Developer $99/yıl + Google Play $25 (mağaza dağıtımı)
- Sosyal dinleme / analitik araçları (K-007)
- GPT-4o-mini fiş okuma API'si (rapordaki Faz 3 özelliği)
- Açık bankacılık / BDDK sağlayıcı entegrasyonu (Faz 3)

### Yeniden değerlendirme
Ürün yayına girip gelir üretmeye başladığında (raporun Faz 3 tanımı).
O zamana kadar bu maddeler PM tarafından yeniden açılmaz.


---

## K-010 — Sosyal medya: takvim hazır ✅ (3 madde karara bağlandı)
- Tarih: 2026-09-10
- Dosya: `projects/trinkow/docs/social/icerik-takvimi.md` (4 hafta, 16 içerik)
- PM denetimi GEÇTİ: emoji 0 · marka adı 24/24 doğru · ücretli araç önerisi
  yok · yapılmayan özellik vaadi yok · rakip adı gönderi metinlerinde yok.

### Seçilen platformlar
**Instagram (birincil)** — tek doğrulanmış rakip orada + tipografik kart
formatı brandbook'un "fotoğraf/illüstrasyon yok" kuralına zaten uyuyor,
ek üretim yükü doğurmuyor. **X (ikincil)** — salt metin, en düşük
prodüksiyon maliyeti, marka sesiyle örtüşüyor.
Dışarıda bırakılanlar gerekçeli: TikTok (video yükü + gösterecek gerçek
ekran yok), LinkedIn (kitle uyumsuz), Threads/Facebook (tekrar üretim yükü).

### Mustafa'dan gereken 5 madde + PM görüşü
1. **IG + X hesabı açılması** — senin aksiyonun.
2. **Bekleme listesi formu** — Google Form (ücretsiz, K-009 uyumlu). ✔ uygun.
3. **Tipografik kart şablonu kim üretecek?**
   **PM önerisi: Canva/Figma DEĞİL.** Elimizde tokens.md ve gömülü fontlar
   zaten var; kartları `ui-ux-designer`'a HTML/CSS şablon olarak ürettirelim.
   Böylece marka tutarlılığı otomatik korunur (aynı token dosyası), üçüncü
   bir araca bağımlılık doğmaz ve şablon versiyonlanabilir.
4. **IG profil görseli** — brandbook §5'te monogram ("T" + çentik) tam
   geometrisiyle tanımlı; üretmek için yeni tasarım kararı gerekmiyor.
5. **Rakip adını sosyal medyada anmama** — **PM: KATILIYORUM.** İki sebep:
   (a) rakibe bedava bilinirlik verilmiş olur, (b) marka kişiliği
   "sakin/ölçülü/yargısız" — rakibe saldırmak markanın kendisiyle çelişir.
   Dolaylı ton karşılaştırması doğru yaklaşım.

### KARARA BAĞLANANLAR (2026-09-10, Mustafa "başlayalım" dedi)
- **Madde 3 → Canva/Figma DEĞİL.** Tipografik kart şablonu `ui-ux-designer`
  TUR 2 kapsamına eklendi: `tokens.md`'den beslenen HTML/CSS şablon.
  Marka tutarlılığı otomatik korunur, üçüncü araca bağımlılık yok.
- **Madde 5 → Rakip adı anılmayacak.** Onaylandı. Dolaylı ton
  karşılaştırması kalıyor, doğrudan isim yok.
- **Madde 4 → Profil görseli** brandbook §5 monogramından üretilecek
  (yeni tasarım kararı gerekmiyor), TUR 2'de kart şablonuyla birlikte.

### HÂLÂ MUSTAFA'DA (aksiyon gerektiren)
- **Madde 1:** IG + X hesaplarının açılması — bunu ben yapamam.
- **Madde 2:** Bekleme listesi formu (Google Form, ücretsiz) + bio linki.

### PM'in ayrıca dikkat çektiği nokta — ZAMANLAMA
Takvim hazır olması ile **yayına başlamak** aynı şey değil. Ürün henüz
kodlanmadı. Tek kişilik ekipte haftalık içerik üretmek, uygulama
geliştirmeden dikkat çalar. Takvim rafta beklerse maliyeti sıfır.
**PM önerisi:** hesapları ve yayını, Faz 1 geliştirmesi bitmeye
yaklaşınca başlat. Karar senin — istersen hemen de başlanabilir.


---

## K-011 — Font dosyaları ✅ ÇÖZÜLDÜ (@expo-google-fonts statik TTF)
- Tarih: 2026-09-10
- **Ücretsiz** → K-009 ihlali değil, PM kararıdır.

**Sorun:** tokens.md 4 adet **statik** font dosyası istiyor (Source Serif 4
Regular/SemiBold, Public Sans Regular/SemiBold). `google/fonts` deposu bu iki
aile için yalnızca **variable** dosya barındırıyor. Statikleri Adobe ve USWDS
release'lerinden elle indirmek gerekir; dosya adları ve uzantı (`.otf` vs
`.ttf`) tokens.md'deki isimlerle uyuşmayabilir.

**Karar:** `@expo-google-fonts/source-serif-4` ve `@expo-google-fonts/public-sans`
paketleri kullanılacak.
- Ücretsiz, OFL, Expo'nun kendi ekosistemi, statik TTF sağlıyor.
- Elle dosya indirme/isimlendirme derdini ve sürüm kaymasını ortadan kaldırır.
- Yalnızca ihtiyaç duyulan 2 ağırlık import edilir → tokens.md'nin
  "4 dosya, artırılamaz" kuralı korunur.
- `frontend-developer` gerçek dosya adlarını gördüğünde tokens.md §2.1'deki
  uzantı/isim satırını buna göre düzeltecek (yalnızca dosya adı; token
  isimleri, ağırlıklar ve tip ölçeği DEĞİŞMEZ).

### SONUÇ (2026-09-10) — çözüldü ve doğrulandı
4 statik TTF `@expo-google-fonts/source-serif-4@0.4.1` ve
`@expo-google-fonts/public-sans@0.4.2` içinden alınıp
`projects/trinkow/docs/design/prototip/fonts/` altına kondu. Hepsi geçerli TTF, OFL 1.1.
**Kabul testi geçti:** `fontTools` ile doğrulandı — `ğ Ğ ı I i İ ş Ş ç Ç
ö Ö ü Ü â î û` + **`₺`** + rakamlar dört dosyada da tam.
Bu, daha önce "₺ eksikse ürünün kalbi bozulur" diye işaretlenen riski kapatır.

**Ayrıca:** `expo-haptics` onaylandı — Expo SDK içinde, ek maliyet yok.
Kullanım ölçülü olacak: yalnızca kayıt onayı ve limit eşiği geçildiğinde.
Marka "sakin/ölçülü" — her dokunuşta titreşim marka ihlalidir.

---

## K-012 — "Sigara" kategorisi ✅ KARAR: B — "Alışkanlıklar" içine
- Tarih: 2026-09-10
- Tasarımcı 13 kategori tanımladı, içinde **"Sigara"** var.

**Gerilim:** Fizibilite raporu "günde 125 TL'lik sigara" örneğini
Latte Faktörü'nün başlıca vakası olarak veriyor — yani ürünün hedefindeki
davranış tam olarak bu. Ayrı kategori, etkisini görünür kılar.

**Ama:** markanın en kritik kısıtı "kullanıcıyı utandırma". Bağımlılık
içeren bir alışkanlığı ayrı kalem olarak listelemek, diğer kategorilerden
farklı bir yargı tonu taşıyabilir.

**Seçenekler:**
- **A)** Kalsın — rapordaki asıl hedef bu, görünürlük ürünün işlevi.
- **B)** Çıkarılsın, "Alışkanlıklar" veya "Kişisel" içine girsin — daha
  yumuşak, ama etki ölçülemez hale gelir.
- **C)** Kalsın ama **varsayılan listede olmasın**; kullanıcı isterse
  kendi ekler. Utandırma riski kullanıcının kendi seçimine devredilir.

**PM önerisi: C.** (Ürünün işlevini korur, markanın tonunu da korur.)

### KARAR (2026-09-10) — Mustafa: *"Kalsın ya alışkanlıkların içerisine koyun"*
**Seçenek B.** "Sigara" ayrı kategori olmaktan çıkarıldı; yerine
**"Alışkanlıklar"** kategorisi geliyor. Sigara harcaması bunun içinde izlenir.
Kategori sayısı 13'te kalıyor.

**PM notu — Mustafa'nın kararı benimkinden isabetliydi:** C seçeneği
("kullanıcı isterse kendi ekler") aslında Faz 1'de **uygulanamazdı** —
`metinler.md` §17'de "Kullanıcı kategorisi ekleme **Faz 2**" yazıyor,
Faz 1'de 13 kategori sabit. C'yi önerirken bunu atlamışım; B tek
uygulanabilir yumuşak çözümdü.

**Uygulama (TUR 2'de yapılacak):**
- `projects/trinkow/docs/content/metinler.md` §17: "Sigara" → "Alışkanlıklar"
- `projects/trinkow/docs/design/varliklar.md` §1.1: `cigarette`/`Cigarette` ikonu, kapsamı
  genişleyen kategoriye uygun nötr bir ikonla değiştirilecek (tasarımcı
  seçecek; `cigarette` artık fazla dar ve fazla işaret edici).
- Kategori adları yargı içermez kuralı korunuyor (§17).


---

## K-013 — Sosyal medya dışa aktarım ölçeği (PM kararı, onay gerekmiyor)
- Tarih: 2026-09-10
- design-reviewer, sosyal kart tipografisinin (`40/30/14px`) tokens.md'deki
  9 tip rolünün dışında olduğunu tespit etti ve "Mustafa onayıyla eklensin"
  dedi.
- **PM kararı: onaya gerek yok, ilan edilerek çözülür.** Sosyal kartlar
  1080×1080 tuvale çıkıyor; uygulama 390pt genişlikte. Uygulama tip
  ölçeğini 1080 tuvale zorlamak yanlış olur — farklı ortam, farklı ölçek.
- **Çözüm:** `tokens.md`'ye "§2.5 Sosyal medya dışa aktarım ölçeği
  (1080 ızgarası)" eklenip bu ölçüler orada **ilan edilecek.** İlan edilmiş
  ölçü "rastgele değer" değildir; anti-pattern ihlali böylece kapanır.
- Ücretli bağımlılık yok, marka kararı değişmiyor → Mustafa'yı meşgul
  etmeye gerek görmedim.

---

## K-014 — Aşama 2 denetim sonucu: REVİZE (1. tur)
- Tarih: 2026-09-10
- `design-reviewer` kararı: **REVİZE GEREKİYOR** — 3 blocker, 2 önemli.
- PM üç blocker'ı da **bağımsız doğruladı** (grep ile):
  1. `#5FA79E` (Faz 2 karanlık mod accent'i) sosyal kartta 18 çizgide
     kullanılmış — Faz 1 paletinde yok. Uygulama ekranları (01-06) temiz.
  2. `.focusring` CSS'te tanımlı, **HTML'de 0 kullanım.** `focused` durumu
     bileşen envanterinde "kaldırılmaz" diye bağlı.
  3. `E-15` ve `E-18` için zorunlu `yükleniyor` durumu çizilmemiş.
- **Mustafa'ya götürülmedi** — REVİZE bloklayıcıdır, yarım iş onaya sunulmaz.
  Tasarımcıya somut madde listesiyle geri gönderildi.
- Düzeltmeler **üreteçten** (`_uret/*.py`) yapılacak, sadece HTML'den değil —
  aksi halde kaynak ile çıktı ayrışır ve hata bir sonraki üretimde geri gelir.

### Denetimin doğruladığı güçlü yanlar (kayda geçsin)
- İlerleme çubuğu %0/%60/%100/%120/limitsiz — **renk dönmüyor**, %120'de
  ayrı `bar-over` segmenti. Marka kararı doğru uygulanmış.
- `danger #8E2F20` yalnızca silme onayı + form hatasında.
- Emoji yok · "Sigara" yok · gradient yok · uppercase yok · saf siyah/beyaz yok.
- Metinler `metinler.md`'den birebir. Ton yargısız — Geçiş 3 geçti.
- Anti-pattern: 17/19 madde temiz. Kapsam: 15 yüzeyin 15'i mevcut.


---

## K-015 — Aşama 2 delta denetim (2. tur): REVİZE, 1 blocker
- Tarih: 2026-09-10
- 1. tur: 3 blocker + 2 önemli → 2. tur: **1 blocker + 1 önemli.** Daralıyor.
- Kapananlar: B1 (palet dışı renk), B3 (eksik yükleniyor kareleri),
  Ö2 (skala dışı boşluk). `index.html` denetimden temiz geçti.

### Kalan blocker — TabItem odak halkası taşması
`.tabitem` 56px + `.focusring` (2px kenarlık + 2px padding) = **64px** →
sekme barından üstte/altta 4'er pt taşıyor. PM aritmetiği doğruladı.
Tasarımcının "RN'de `View` varsayılan `overflow: visible`" savunması
**reddedildi:** Android'de ebeveyn sınırını aşan çocuk güvenilir biçimde
kırpılır (RN'in bilinen sınırı) + alt taşma home indicator şeridine giriyor.
`focused` envanterde "kaldırılmaz" → Android'de görünmezse a11y kapısı kapanır.
**Çözüm:** TabItem içerik kutusu 44pt'ye insin (dokunma hedefi korunur),
halka 44+8=52 ≤ 56 → bar içinde kalır, kırpma bağımlılığı biter.

### Kalan önemli — §2.5 türetme kuralı uydurma
"≈2,5 katı, 5'in katına yuvarlanır" kuralı kendi tablosunu üretmiyor.
**PM hesapladı:** 44×2,5=110 (tabloda 100, kat 2,27) · 28×2,5=70
(tabloda 75, kat 2,68) · 13×2,5=32,5 (tabloda 35, kat 2,69).
Tablonun `Kat` sütunu 2,27–2,69 aralığını zaten itiraf ediyor.
**Risk:** yanlış kural bırakılırsa ileride yeni değer türetilince kayma
geri gelir. **Çözüm:** kural dürüst haliyle yeniden yazılsın — "roller
bağımsız seçildi, Kat sütunu bilgi amaçlıdır, yeni rol üretilmez".
Boşluk kuralı doğru (32→80, 12→30 tam 2,5×), korunacak.

### PM notu — bu bir döngü değil
İki revizyon turu oldu ama bulgular daralıyor (3→1 blocker) ve her tur
somut/kanıtlı. Kalite kapısı tasarlandığı gibi çalışıyor; "aynı görevde
2 başarısız deneme" kuralı burada geçerli değil — bunlar başarısızlık
değil, denetim döngüsünün normal işleyişi.


---

## K-016 — TabItem 48pt: tasarımcı PM'in talimatını gerekçeli reddetti (DOĞRU)
- Tarih: 2026-09-10
- PM, blocker düzeltmesi için "TabItem içerik kutusu **44pt**'ye insin" dedi.
- Tasarımcı uygulamadı ve gerekçesini yazdı: **44pt aritmetik olarak
  imkânsız.** Sekme ikonu `varliklar.md:23`'te **28pt**'ye kilitli
  ("ara boyut yok"), etiket satır kutusu `tokens.md:106`'da **18pt**
  → içerik 46pt > 44.
- **PM doğruladı: tasarımcı haklı, talimatım hatalıydı.** Token dosyalarını
  kontrol etmeden ölçü verdim.
- Uygulanan: TabItem **48pt** (dokunma hedefi 48 ≥ 44 ✅), halka
  48 + 2×2 padding + 2×2 kenarlık = **56 = bar yüksekliği** → bar içinde,
  kırpma bağımlılığı yok. PM aritmetiği bağımsız doğruladı.
- Sığdırmak için ikon–etiket arasındaki 4pt boşluk kaldırıldı; o boşluk
  hiçbir token'da tanımlı değildi → token ihlali yok. Tasarımcı ikonu
  28→24 yapmayı **reddetti** (gerçek token ihlali olurdu) — doğru karar.

### PM notu — sistem açısından önemli
Bu, alt-ajanın PM'e gerekçeli itiraz ettiği ilk vaka ve **istenen davranış.**
Ajan talimatı körü körüne uygulasaydı token sistemini bozacaktı. Ajan
promptlarındaki "sapmak zorunda kaldığın noktalar + teknik gerekçe" maddesi
tam da bunun için var; çalıştığı görüldü.
**PM dersi:** ölçü içeren talimat vermeden önce ilgili token dosyası
okunmalı. Bu turda okumadım.


---

## K-017 — TASARIM ONAYI ❌ REDDEDİLDİ (Mustafa: "fazla amatör, ruhsuz")
- Tarih: 2026-09-10
- Prototip: `projects/trinkow/docs/design/prototip/index.html` (tarayıcıda aç)
- **design-reviewer kararı: ✅ PASS** (3 denetim turu sonunda)

### Denetim geçmişi — kapı çalıştı
| Tur | Sonuç |
|---|---|
| 1 | REVİZE — 3 blocker + 2 önemli |
| 2 (delta) | REVİZE — 1 blocker + 1 önemli |
| 3 (delta) | **PASS** — yan etki yok |

Kapatılan gerçek kusurlar: palet dışı Faz 2 rengi (18 kullanım) · `focused`
durumunun hiç çizilmemiş olması · 2 eksik `yükleniyor` karesi · skala dışı
boşluk · uydurma türetme kuralı · Android'de kırpılacak odak halkası ·
**ölü `index.html` bağlantıları** (7 sayfada bağlantı vardı, dosya yoktu).

### Denetimin doğruladığı marka kararları
- İlerleme çubuğu %0/%60/%100/%120/limitsiz — **renk dönmüyor**, taşma ayrı
  `bar-over` segmenti. En kritik marka kararımız doğru uygulanmış.
- Kırmızı `danger` yalnızca silme onayı + form hatasında.
- Ton yargısız ("Limitin 60 ₺ üzerindesin.") — Geçiş 3 geçti, tasarım
  jenerik SaaS şablonundan ayırt edilebilir.
- Emoji · "Sigara" · gradient · uppercase · saf siyah/beyaz · "Henüz veri
  yok" — hiçbiri yok. Anti-pattern 17/19 → düzeltmelerle temiz.
- Kapsam: ekran envanterindeki **15 yüzeyin 15'i** mevcut.
- Tüm HEX'ler tokens.md'de ilan edilmiş (PM bağımsız taradı).

### MUSTAFA'NIN KARARI GEREKEN
**Prototipi aç ve görsel onay ver.** CLAUDE.md gereği bu geçiş PM tarafından
varsayılamaz. Onay verilirse Aşama 3 (Geliştirme) başlar:
Expo projesi kurulur, tokenlar `src/theme/tokens.ts`'e çevrilir,
ekranlar React Native'e kodlanır.

### Aşama 3'e devredilen notlar (frontend-developer için)
- Odak halkası **dokunmatikte gösterilmez** — yalnız klavye/Switch
  Control/TalkBack.
- **Gölge/elevation hiçbir yerde kullanılmaz.**
- Sekme ikonu **28pt sabit**, sekme içerik kutusu **48**.
- ⚠ Bar `height:56` + `borderTopWidth:1` olursa iç alan 55 kalır ve halka
  0,5pt taşar → hairline **ayrı 1px View** olsun ya da `height:57`.
  (tokens.md §7.7'ye kodlama notu olarak işlendi.)
- Para **kuruş cinsinden integer**, float değil.


---

## K-018 — TASARIM REDDEDİLDİ: marka yönü değişiyor 🔴 KARAR GEREKİYOR
- Tarih: 2026-09-11
- Mustafa: *"Tasarımlar fazla amatör geldi… ruhsuz bir UI/UX istemiyorum…
  bu videodaki gibi bir UI/UX istiyorum… tasarımların tamamını değiştirsin."*
- Referans: Dribbble kalori takip uygulaması videosu.
  **PM videoyu indirip kare kare izledi**; analiz `projects/trinkow/docs/design/referans-analizi.md`,
  görseller `projects/trinkow/docs/design/referans-gorseller/`.

### Kök sebep — bu bir uygulama hatası DEĞİL
Referans, onaylı brandbook'un (Yön A "Defter") neredeyse her eksende zıddı:
dairesel halka↔düz çubuk · kategori rengi↔renk yok · gölge↔gölge yok ·
gradyan↔gradyan yasak · geometrik sans↔serif · fotoğraf↔fotoğraf yok ·
çok vurgu rengi↔tek vurgu rengi.

**Ekranları yeniden çizmek yetmez; brandbook aynı kalırsa aynı his çıkar.**
Bu yüzden iş Aşama 2'ye değil **Aşama 1'e (Marka) geri dönüyor.**

### PM'in özeleştirisi
"Jenerik AI görünümü" kısıtını fazla dar yorumlayıp gölge/gradyan/renk/
animasyonu topluca yasakladık. Sonuç jenerik olmadı ama **cansız** oldu.
Anti-pattern listesi "neyi yapma"yı söylüyor, "ruhu nasıl verirsin"i değil.
Bu boşluk yeni marka yönünde kapatılmalı.

### Mustafa'dan gereken 3 karar
1. **Anti-pattern listesi gevşetilecek mi?** Referansın kullandığı bazı
   öğeler bizim yasak listemizde: mor-lavanta gradyan arka plan (liste
   maddesi #1), her karta yumuşak gölge, 3'lü eşit kart dizilimi.
   Emoji maddesinde yaptığın gibi bunları da gevşetebilirsin — ama
   **bilerek**. PM önerisi: **gölge ve gradyanı serbest bırak**
   (derinlik ruhun kaynağı), "mor-mavi varsayılan gradyan" yasağını
   **koru** (o gerçekten jenerik AI imzası).
2. **Renk: referanstaki mor/lavantayı mı alalım, kendi rengimizi mi?**
   PM önerisi: **tasarım dilini al, rengi alma.** Mor/lavanta bir Dribbble
   sunum estetiği; kopyalarsak "bir başka mor SaaS" oluruz. Trinkow'un
   kendi paleti yeni yönde belirlenir.
3. **REPO PAYLAŞILMADI.** *"ben bir repo paylaşıyorum seninle ordan ilgili
   uygun skill'i alsın"* dedin ama mesajda yalnızca video linki vardı.
   Repo/skill linkini gönder; ui-ux-designer'a girdi olarak bağlayayım.

### Ayrıca kesinleşen (onay gerekmiyor)
**UI'da teknik açıklama yasak.** Kullanıcıya verinin nerede saklandığı,
sunucu/cihaz mimarisi anlatılmaz. `metinler.md`'de 4 satır temizlenecek
(:312, :329, :361, :363). Hata mesajı ne olduğunu değil **ne yapacağını**
söyler.


---

## K-019 — Yeni marka yönü: renk + görsel dil gevşetmesi
- Tarih: 2026-09-11
- Mustafa: *"bizim renkte çok katı, farklı bir renk seçelim, piyasaya uygun
  bir şekilde olsun."*

### Karar 1 — Palet değişiyor
Yön A "Defter" paleti (Petrol `#14484C` + kağıt `#F4F1EA`) **terk edildi**;
fazla katı/ağırbaşlı. Yeni palet **piyasaya uygun** olacak: kişisel finans
kategorisinde çağdaş, canlı, yaklaşılabilir.
**Sınır:** referanstaki mor/lavantayı **birebir kopyalama.** O bir Dribbble
sunum estetiği; kopyalanırsa "bir başka mor SaaS" oluruz. Renk, rakip
haritasına göre **ayrışacak şekilde** seçilecek ve gerekçelendirilecek.

### Karar 2 — Görsel dil gevşetildi (PM kararı, Mustafa'nın yönüne uygun)
Bu proje için `jenerik-ai-ui-anti-pattern-listesi.md`'nin şu maddeleri
**gevşetiliyor** (global liste değişmiyor; kapsam proje-özel, emoji
kararındaki (K-004) yöntemin aynısı):
- ✅ **Gölge serbest** — derinlik "ruh"un kaynağı. Ama amaçlı olacak:
  yükseklik/katman anlatacak, her karta refleksle uygulanmayacak.
- ✅ **Gradyan serbest** — grafik dolgusu, kahraman gösterge, ortam zemini.
- ✅ **Kategori renkleri serbest** — her kategori kendi tonunu taşıyabilir
  (K-006'daki "kategoriler renk taşımaz" kararı **iptal**).
- ✅ **Yüksek köşe yarıçapı serbest** — dostane geometri.
- ✅ **Görsel/illüstrasyon serbest** — markaya özel olmak kaydıyla.

### KORUNAN yasaklar (gevşetilmedi)
- ❌ **Mor-mavi (indigo/violet) VARSAYILAN gradyan** — jenerik AI imzası.
  Mor bir marka rengi olabilir, ama "düşünmeden seçilmiş mor-mavi gradyan
  arka plan" olamaz; seçilirse gerekçesi yazılacak.
- ❌ **Emoji** (K-004, Mustafa'nın kesin kararı).
- ❌ Inter/Poppins/Montserrat varsayılanı, gerekçesiz.
- ❌ "Daire içinde ikon + başlık + 1 cümle" 3'lü kart şablonu.
- ❌ Lorem ipsum / stok illüstrasyon / jenerik pazarlama dili.
- ❌ Düşük kontrast (WCAG AA korunuyor).
- ❌ **Kullanıcıyı utandıran ton** — bu marka kararı değil, ürün kararı.

### Karar 3 — UI'da teknik açıklama yasak (kesin)
Kullanıcıya depolama/mimari anlatılmaz. `metinler.md`:312, :329, :361, :363
temizlenecek. Hata mesajı ne olduğunu değil **ne yapacağını** söyler.

### Hâlâ eksik
**Repo/skill linki paylaşılmadı.** İki kez soruldu. Gelmediği için
ui-ux-designer'a bağlanamıyor; iş bunsuz ilerliyor, link gelirse
sonraki tura eklenir.


---

## K-020 — open-design (Claude Design) entegre edildi
- Tarih: 2026-09-11
- Mustafa: *"https://github.com/nexu-io/open-design claude design'i kullan
  işte mobil tasarım için"*
- Repo doğrulandı: gerçek, **Apache-2.0 (ücretsiz)**, 95k yıldız.
  **K-009 uyumlu** — ücretli bağımlılık yok.
- İlgili parça indirilip `agency/vendor/open-design/` altına alındı (ajanlar ağdan
  tekrar çekmesin): `mobile-app/SKILL.md`, `assets/template.html`,
  `references/layouts.md`, `references/checklist.md`, `_schema/`, `LICENSE`.
- Entegrasyon kuralları: `agency/reference/open-design-entegrasyon.md`

### Ne kazandırıyor
Önceki prototipin "amatör" bulunmasının bir sebebi **sunum kalitesiydi**:
çıplak 390×844 kutular. Şablon gerçek iPhone 15 Pro çerçevesi, Dynamic Island,
SVG durum çubuğu ve home indicator getiriyor. Ayrıca 6 ekran arketipi ve
sıkı bir P0 kontrol listesi.

### 🔴 Çözülen kritik çatışma
Şablon **web için** yazılmış ve RN'de karşılığı olmayan CSS kullanıyor:
`grid` 13×, `::before`/`::after` 7×, `z-index`, `backdrop-filter`.
Bizim prototipimiz ise **RN'e çevrilebilir** kalmak zorunda.

**Çözüm — çerçeve/içerik ayrımı (bağlayıcı):**
- **Çerçeve/kabuk** (telefon gövdesi, island, durum çubuğu, sayfa zemini):
  asla RN'e kodlanmayacak → **CSS serbest**, şablon olduğu gibi kullanılır.
- **Ekran içeriği** (`<main class="content">` içi): gerçek ürün →
  **RN kuralları geçerli**, sadece flexbox, yasak CSS yok.
- `design-reviewer` yasak CSS taramasını **yalnızca `<main>` içinde** yapar.

### Şablondan bilinçli sapmalar (denetimde ihlal sayılmaz)
- Şablon "başlıklar serif olsun" diyor → **brandbook ne derse o.** Uyarı
  *sistem* sans'ı içindir; bilinçli seçilmiş karakterli sans başka şeydir.
- Şablon "tek accent, en fazla 2 kez" diyor → 1 birincil accent (eylemler)
  **+ işlevsel kategori tonları.** Kategori renkleri bilgi taşıyor
  (K-019'da serbest bırakıldı), dekorasyon değil, accent bütçesine sayılmaz.
- Şablon `<artifact>` çıktısı istiyor → biz **dosyaya yazıyoruz.**

### Şablonun benimsenen kuralları
Dokunma hedefi ≥44px · gerçek/spesifik metin · **UI'da emoji yok, sadece SVG
monoline ikon** (K-004 ile birebir aynı) · gövde ≥14px · içerik kayar çerçeve
kaymaz · birincil eylem katlamanın üstünde.

### Arketip eşleştirmesi
Bugün/pano → **F Focus** (dairesel kahraman gösterge) · Harcama ekle →
**E Checkout** · Onboarding → **C** · Kayıtlar → **A Feed** ·
Harcama detayı → **B Detail** · Ayarlar → **E**.


---

## K-021 — YENİ BRANDBOOK v2.0 ✅ ONAYLANDI (Yön C)
- Tarih: 2026-09-11
- `projects/trinkow/docs/brand/brandbook.md` v2.0 (1284 satır) + `projects/trinkow/docs/brand/tokens.md` (571 satır)
- Yön A/B arşivlendi, silinmedi.

### PM denetimi: GEÇTİ
Kontrast iddiaları bağımsız hesaplandı, **tamamı tutuyor**:
amber `#D9661A`/bg = **3.26:1** (metin değil, yalnız yay/dolgu — doğru tespit) ·
`accent-deep #A8500C` = **5.01:1** (metin için) · ink buton = **17.34:1** ·
**6 kategori renginin hepsi AA metin eşiğini (≥4.5) geçiyor.**
Fontlar Google Fonts'ta, **OFL, ücretsiz** → K-009 uyumlu.

### Rakip renk haritası — en güçlü bulgu
Lacivert (İş, Garanti, YNAB) · mor (Papara, QNB, Cleo — **ayrıca jenerik AI
imzası**) · kırmızı (Akbank, Ziraat) · turkuaz (Enpara, N26 — *v1.0'ın petrolü
tam buraya düşüyordu*) · koyu yeşil (Monarch) → hepsi DOLU.
**Sıcak amber/mandalina ailesi TR kişisel finansta BOŞ.** Küreselde yalnız
Monzo mercanı yakın. Ruh eşi finans değil **Headspace**: günlük alışkanlık +
yargısız ton + sıcak turuncu.

### Yön C — "Gün Işığı" (PM önerisi)
`bg #F6F4F1` · `surface #FFFCF8` · `ink #17181C` · **accent Mandalina `#D9661A`**
· limit dışı **Mürdüm `#6E3B6B`** · 6 kategori rengi + pastel tint'leri.
Tipografi: **Space Grotesk Bold** (yalnız rakam — "sayaç" hissi, tabular) +
**Figtree** 400/600 (arayüz). 3 dosya, OFL.
Kişilik: **Sıcak · Odaklı · Net · Yargısız** — "sakin ≠ cansız" ayrımı §2.1'de
kural olarak yazılmış (önceki turun asıl hatası buydu).

### Yön D — "Gece Sayacı" (alternatif)
`#0E1214` + Nane `#4ADEA8` + Şeftali `#FFB07C`, Manrope.
Artı: tek tema geliştirilir, anında ayrışır. Eksi: referansın havadar ruhuna
ters, "trading terminali" çağrışımı, güneşte okunurluk.

### Kahraman gösterge
200pt çap, 270° yay, 18pt kalınlık, ucunda **22pt topuz** (zorunlu), ortada
56pt sayı + 13pt sessiz etiket (oran ≥4× bağlayıcı). **Taşma kırmızıya
dönmez** — ana yayın 6pt dışında ayrı mürdüm yay. Marka rengi veriye ve
FAB'a ayrıldı; birincil buton mürekkep hap.

### ✅ KARAR (2026-09-11) — Mustafa: *"C'den devam et bi deneyelim bakalım tasarımı göreyim"*
**Yön C "Gün Işığı" onaylandı.** Diğer 7 madde için PM önerileri toptan onay
sayıldı (K-006'daki yöntemin aynısı). Özetle: amber `#D9661A` tonunda kalınıyor ·
limit dışı **mürdüm** (kırmızı değil) · birincil buton **mürekkep** ·
6 renk **aile** olarak kullanılıp 13 kategoriye dağıtılacak, aile içinde ikonla
ayrışacak · uygulamada fotoğraf yok · karanlık mod Faz 2 · monogram iki renkli.
Yanlış yorum varsa geri dönüş ucuz — ekranlar henüz çizilmedi.

### MUSTAFA'NIN 8 KARARI (PM önerileriyle)
1. **Yön C mi D mi?** → PM: **C**.
2. **Amber tonu:** `#D9661A` alt sınır; daha parlağı WCAG 3:1'i düşürür ve yay
   geometrisi yeniden hesaplanır. → PM: **bu tonda kal**.
3. **Limit dışı = mürdüm (kırmızı değil)?** → PM: **evet, kesinlikle.**
   "Utandırma" ilkesinin doğrudan karşılığı.
4. **Birincil buton mürekkep kalsın mı?** (amber üzerine beyaz AA'yı geçmiyor)
   → PM: **evet**, erişilebilirlik zorunluluğu.
5. **6 kategori rengi yeterli mi?** ⚠️ **GERÇEK BOŞLUK:** ürün **13 kategoriyle**
   çıkıyor, palet 6 renk veriyor. → PM önerisi: 6 rengi **aile** olarak kullan
   (yeme-içme, ulaşım, faturalar, sağlık, kişisel, diğer), 13 kategori bu
   ailelere dağılsın, aile içinde **ikonla** ayrışsın. Palet disiplini bozulmaz.
6. **Uygulamada fotoğraf yok kararı sürsün mü?** → PM: **sürsün.** Harcama
   takibinin doğal görseli yok (yemek uygulamasından farkı bu).
7. **Karanlık mod hâlâ Faz 2 mi?** → PM: **evet.**
8. **Logo monogramı iki renkli olsun mu** (T ışık + topuz amber)? → PM: **evet**,
   kahraman göstergeyle görsel bağ kurar.


---

## K-022 — Tasarım TUR A/B'ye bölündü (PM kararı)
- Tarih: 2026-09-11
- Mustafa: *"bi deneyelim bakalım tasarımı göreyim"*

**Karar:** 15 ekran birden çizilmeyecek. Önce **TUR A — 3 kilit ekran**
(Bugün/pano, Harcama ekle, Onboarding), Mustafa görsel yönü onaylarsa
**TUR B — kalan 12 ekran.**

**Gerekçe:**
1. Önceki turda 15 ekran çizildi ve yön beğenilmediği için **tamamı çöp oldu.**
   Aynı riski ikinci kez almanın anlamı yok.
2. Mustafa "göreyim" diyor — en hızlı yol 3 ekranı iyi yapmak, 15'i orta yapmak
   değil. Yargı bu 3 ekranda zaten verilebilir: kahraman gösterge, form akışı
   ve onboarding ürünün görsel dilinin tamamını taşıyor.
3. Önceki turda 2 API kesintisi yaşandı; küçük parça = düşük risk.

Ek: `projects/trinkow/docs/content/metinler.md`'deki teknik açıklamalar (K-019) bu turda
temizlenecek — :312, :329, :361, :363.


---

## K-023 — TUR A ❌ REDDEDİLDİ (Mustafa: "rezalet olmuş") — kayıt amaçlı duruyor
- Tarih: 2026-09-11
- Çıktı: `projects/trinkow/docs/design/prototip-v2/index.html` (giriş) + 3 ekran, toplam 16 durum.
- PM üç ekranı da headless tarayıcıda render edip **gözle inceledi.**

### PM kararları (ücretsiz/küçük kapsam → Mustafa'ya sorulmadı)
1. **İkon seti 31 → 34.** Lucide `route`, `piggy-bank`, `trending-down`
   (onboarding niyet seçenekleri). Üçü de npm'de doğrulandı, ISC, ücretsiz.
   Emoji yasağı (K-004) nedeniyle ikon zaten tek seçenek. **ONAYLANDI.**
2. **Taksitte "Uygula" butonu kaldırıldı** → taksitli yol +3 değil **+2 dokunuş.**
   Sürtünme azaltan doğru karar. `ekran-envanteri.md §4` bu yönde güncellenecek
   (TUR B'de). **ONAYLANDI.**
3. `varliklar.md §2` (fontlar) reddedilen v1.0 kalıntısıydı → TUR B'de P-6
   güncellemesiyle temizlenecek. **Not alındı.**

### 🔴 KRİTİK TEKNİK BULGU — `₺` glifi
**Figtree'de `₺` glifi YOK** (PM fontTools ile bağımsız doğruladı:
Figtree-Regular ve SemiBold → `₺` YOK; SpaceGrotesk-Bold → VAR).
Web'de aile sırası Space Grotesk'e düşerek kurtarıyor, ama **React Native'de
fallback yok** → uygulamada `₺` yerine tofu kutusu (□) çıkardı.
**Çözüm:** `₺` ayrı bir `<Text>` içinde Space Grotesk ile dizilecek.
`varliklar.md` ve `LISANS.md`'ye yazıldı. Bir para uygulamasında bu bulgu
geliştirmede yakalansaydı çok daha pahalı olurdu.

### Gösterge yön kararı (tasarımcı gerekçelendirdi, PM kabul etti)
Yay **harcanan**ı gösterir (dolar), ortadaki sayı **kalan**ı gösterir.
Gerekçe: (1) `metinler.md §20` erişilebilirlik değeri zaten `{harcanan}/{limit}`,
(2) taşma yayı ve %100 eşiği, dolan yay olmadan anlamsız kalır,
(3) **topuz** ikiliği tek okumaya çeviriyor — turuncu = geçilen yol,
gri = önündeki yol, ortadaki sayı gri kısmın ₺ karşılığı (yakıt göstergesi
mantığı). Boşalan halka reddedildi: gün başında dolu halka "tamamlandı" diye
okunur ve en kritik anda ekranda hiç renk kalmaz. `aria-valuetext` eklendi.

### Tasarımcının kendi bulduğu 3 CSS hatası (kapsam dışı, düzeltti)
`t-hero/display/amount`'ta `margin:0` eksikti (UA 1em sızıyordu) ·
`.mtX` yardımcıları `t-*`'ın öncesindeydi (tüm boşluklar eziliyordu) ·
mini göstergede ratio 0'da yuvarlak uç nokta bırakıyordu.

### Bilinen eksikler (TUR B'ye devredildi)
E-11'de not alanı açıkken QWERTY klavye çizilmedi · E-03 Takip'te "en fazla üç"
kuralı sonrası pasif çip durumu yok · E-11 sheet varsayılan akışta kaymıyor.


---

## K-024 — GÖRSEL OTORİTE DEĞİŞTİ: Claymorphism
- Tarih: 2026-09-12
- Mustafa: *"2. prototip tasarımları da rezalet olmuş… skill kullan…
  claymorphism olsun, attığım dosyada design md'si mevcut:
  `agency/vendor/design-systems/library/claymorphism/DESIGN.md`"*
- Mustafa 138 design system içeren kütüphaneyi projeye import etti
  (`agency/vendor/design-systems/` — `library/`, `crosswalk.md`,
  `interop-protocol.md`).

### Karar — yeni hiyerarşi
**`library/claymorphism/DESIGN.md` artık GÖRSEL OTORİTEDİR.**
Brandbook v2 "Gün Işığı"nın **görsel katmanı** (palet, tipografi, gölge
stratejisi, geometri) **geçersizdir**. Brandbook'un yalnızca **ürün katmanı**
geçerli kalır: ton of voice, kişilik, metin kuralları, yasaklar.

Uygulama yöntemi `interop-protocol.md` → **Yön A** ("map FROM an external
system → our tokens / adopt their look"): claymorphism değerleri bizim
semantik token yapımıza yeniden bağlanır, yapı korunur, değerler değişir.

### Claymorphism'den gelen değerler
Primary `#3B82F6` · Text `#1C398E` · Surface `#FFFFFF` · Success `#16A34A` ·
Warning `#D97706` · Danger `#DC2626` · spacing 4/8/12/16/24/32 ·
tipografi Montserrat (primary) + Poppins (display) + JetBrains Mono (mono).
Stil: yumuşak, yuvarlak, 3B benzeri, kabarık (puffy), oyuncu, renkli yüzeyler.

### 🔴 PM'in doğruladığı 2 kritik teknik gerçek

**1. Claymorphism RN'de inşa EDİLEBİLİR — ama koşullu.**
Clay görünümünün imzası **iç gölge (inset shadow)**. RN'de tarihsel olarak yoktu.
PM `reactnative.dev/projects/trinkow/docs/view-style-props`'tan doğruladı: `boxShadow` **inset
dahil** destekleniyor, ancak:
- **Yalnızca New Architecture'da** → Expo kurulumu New Arch ile yapılmalı (K-005 eki)
- Outset gölge **Android 9+**, **inset gölge Android 10+**
- iOS'ta sorun yok · Birden fazla gölge birleştirilebilir (clay için şart)
Bu doğrulanmadan çizilseydi tasarım yine inşa edilemez çıkardı.

**2. `JetBrains Mono`'da `₺` GLİFİ YOK.**
PM fontTools ile üç fontu da ölçtü:
- Montserrat → `₺` **VAR**, tüm TR karakterleri tam ✅
- Poppins → `₺` **VAR**, tüm TR karakterleri tam ✅
- **JetBrains Mono → `₺` YOK** ❌
Para rakamları mono ile dizilecekti; tam da `₺`'nin geçtiği yerde tofu (□)
çıkardı. → **Para rakamlarında JetBrains Mono KULLANILMAYACAK**; rakamlar
Montserrat (tabular) ile dizilecek. Mono yalnızca `₺` içermeyen yerlerde.
(Aynı tuzak Figtree'de de çıkmıştı — K-023.)

### Anti-pattern listesi geçersiz kılmaları (proje kapsamlı)
- **Poppins/Montserrat yasağı KALDIRILDI.** Gerekçe: burada tembel varsayılan
  değil, seçilen stil sisteminin parçası; geometrik yuvarlaklık clay
  estetiğiyle örtüşüyor.
- **Gölge/gradyan/yüksek radius** zaten K-019'da serbestti — claymorphism
  bunları merkeze alıyor.

### KORUNAN ürün kuralları (stil değişse de değişmez)
❌ EMOJI · ❌ kullanıcıyı utandırma · ❌ UI'da teknik açıklama ·
❌ ücretli bağımlılık · ✅ WCAG AA · ✅ dokunma hedefi ≥44pt ·
✅ gerçek Türkçe metin, lorem yok · ✅ harcama girişi 3 dokunuş ·
✅ karanlık mod Faz 2.

### Renk rol eşlemesi (utandırmama ilkesi korunuyor)
- Limit aşımı → **Warning `#D97706`** (amber), kırmızı DEĞİL
- Silme onayı / yıkıcı işlem → **Danger `#DC2626`**
- Birincil eylem → **Primary `#3B82F6`**


---

## K-025 — Boşluk standardı düzeltmesi (Mustafa geri bildirimi)
- Tarih: 2026-09-12
- Mustafa: *"Güzel tasarım fakat paddingler falan çok uçuk, yapışık birbirine,
  bir standartı olsun. design.md'den bakıp ayarlasın."*
- **Görsel yön KABUL EDİLDİ** (claymorphism tuttu). Sorun yalnızca ölçü/ritim.

### PM'in ölçtüğü somut bulgular

**1. Boşlukların %26'sı skala dışı.**
`stil.css`'teki padding/margin/gap değerleri sayıldı:
skala içi (4/8/12/16/24/32) → 37 kullanım · **skala dışı → 13 kullanım**:
`6px`, `18px`, `26px`, `40px`, `56px`, `64px`, `2px`, `-4px`.
DESIGN.md §4 net: **"Spacing scale: 4/8/12/16/24/32 · avoid ad-hoc offsets."**

**2. Kahraman gösterge ekranı yutuyor — "yapışık" hissinin kök sebebi.**
`.hero-daire` = **296×296px**, ekran genişliği 390px → **%76'sı.**
Geriye kalan alanda "Kategori limitleri" kartı sıkışıyor ve `.content`'in
`overflow:hidden`'ı satırı **ortasından kesiyor** ("Market 2.180 ₺" satırı
yarım görünüyor). Kullanıcıya kesik/yapışık geliyor — haklı.

**3. Skala dışı küçük değerler** `.fab right:10px`, `.sekme-bosluk 60px`.

### Düzeltme talimatı (ajana verilecek)
- Boşluk skalası **katı**: 4/8/12/16/24/32. Daha büyüğü gerekiyorsa skala
  **ilan edilerek** genişletilir (40/48/64) — keyfi değer yok.
- Kahraman gösterge küçültülecek (296 → ~224, skalaya oturan bir değer) ki
  ikinci kart **kesilmeden** görünsün.
- **Tek bir dikey ritim seti tanımlanacak** ve tokens.md'ye yazılacak:
  ekran kenar boşluğu · kart iç boşluğu · kartlar arası · bölüm arası ·
  içerik alt boşluğu (sekme çubuğunu temizleyecek kadar).
- Hiçbir satır ortasından kesilmeyecek.

### Not
Ajan bu geri bildirim geldiğinde 3. ekranı (onboarding) yazıyordu.
Çalışan ajana mesaj gönderilemediği için düzeltme, o bitince ayrı bir
tur olarak verilecek — yarıda kesmek emeği çöpe atardı.


---

## K-026 — Boşluk ritmi düzeltildi + 2 ölçüm hatası bulundu
- Tarih: 2026-09-12

### Sonuç (PM bağımsız doğruladı)
- **Kahraman gösterge 296 → 224px.** "Kategori limitleri" kartı artık
  2 satırıyla **tam görünüyor**, satır ortasından kesme yok.
- **Skala dışı boşluk: 0.** Kalan 3 değer usulüne uygun ilan edildi:
  `-4` → §3.3 "negatif oluk telafisi" (izinli: −4/−8, başkası üretilemez) ·
  `48/64` → §3.2 kabuk ölçeği (yalnız masaüstü sahne, **RN'e kodlanmaz**).
- **`tokens.md §3.1` DİKEY RİTİM SETİ ilan edildi**, her değerin tek işi var:
  `4` aynı nesnenin iki satırı · `8` başlık↔gövde, etiket↔girdi, tekrarlayan
  öğeler · `12` kart içinde iki blok · `16` iç boşluk (kart + ekran kenarı,
  kahraman kart dahil istisnasız) · `24` ekran düzeyinde iki blok + içerik
  alt boşluğu. Üç ekranda da aynı set. Tablo bağlayıcı: "aynı işi yapan
  ikinci bir boşluk üretilemez."

### 🔴 Ajanın yol boyunca bulduğu 2 ÖLÇÜM HATASI (bunlar olmadan ölçüm anlamsızdı)
1. **Prototip yanlış boyutta çiziliyordu.** `.device` 390×844 iken 12px
   çerçeve payı yüzünden ekran gerçekte **366×820** render ediliyordu.
   Yani şimdiye kadarki tüm tasarımlar **yanlış ekran boyutunda**
   değerlendirilmiş. Dış ölçü 414×868'e çekildi, ekran artık tam 390×844.
2. **Prototip yalan söylüyordu.** `.kaydir` bir flex sütun olduğu için
   tarayıcı boşluk `div`'lerini sessizce **eziyordu**; RN'de `flexShrink`
   varsayılanı **0**'dır, yani gerçek uygulamada boşluklar prototipte
   göründüğünden **daha geniş** çıkacaktı. `flex:0 0 auto` eklendi.
   Bu düzeltilmeden yapılan her boşluk ölçümü yanıltıcıydı.

### Tasarımcının bilinçli kararı
Kategori limitleri kartı **3 → 2 satır**. Gerekçe: kabarık kil kart fiziksel
bir nesnedir, katlama çizgisinde dilimlenmesi clay metaforunu bozar; 3 satır
hiçbir düzenlemede tam sığmıyordu. "Tümünü gör" zaten mevcut. PM kabul etti.

### Durum
Görsel yön Mustafa tarafından beğenildi ("güzel tasarım"), ritim düzeltildi.
Sıradaki: Mustafa'nın onayı → kalan 12 ekran → design-reviewer tam denetim.


---

## K-027 — ✅ GÖRSEL YÖN ONAYLANDI (claymorphism)
- Tarih: 2026-09-12
- Mustafa: *"tamam tüm ekranları oluştur beğendim son halini"*
- **Claymorphism yönü + boşluk ritmi onaylandı.** Üç tur reddedilme sonrası
  (Yön A "Defter" → Yön C "Gün Işığı" → Claymorphism) görsel dil oturdu.
- `projects/trinkow/docs/design/prototip-v3/` referans kabul edilir; `prototip/` ve
  `prototip-v2/` arşivdir.

### Kalan iş: 10 yüzey
Biten 5: E-01, E-02, E-03 (onboarding), E-10 (Bugün), E-11 (Harcama ekle).
Kalan 10: E-00 Splash · E-12 Harcama detayı · E-13 Silme onayı ·
E-14 Kayıtlar · E-15 Kategori detayı · E-16 Özet · E-17 Limitler ·
E-18 Taksitler · E-19 Ayarlar · E-20 Profilleme sorusu.

### PM kararı — iki tura bölünüyor
**TUR D (5):** E-14 Kayıtlar · E-16 Özet · E-12 Harcama detayı ·
E-13 Silme onayı · E-00 Splash → yüksek trafikli/kritik yüzeyler önce.
**TUR E (5):** E-15 · E-17 · E-18 · E-19 · E-20.

Gerekçe: bu projede büyük turlar **iki kez** yarıda kesildi (API hatası,
oturum limiti). 5'erli tur hem riski düşürür hem ara kontrol imkânı verir.
Paralel çalıştırılamaz — ikisi de aynı `stil.css` ve `_uret/lib.py`'ye yazar.

### Ayrıca güncellenecek (TUR E'de)
- `bilesen-envanteri.md` hâlâ v2 değerleriyle duruyor → v3.1'e çekilecek.
- `ekran-envanteri.md §4` — taksit yolu +3 değil **+2 dokunuş** (K-023).


---

## K-028 — TUR D tamam (4 dosya, 19 yüzey) + 1 karar gerekiyor
- Tarih: 2026-09-12
- `04-kayitlar.html` (E-14, 6 durum) · `05-ozet.html` (E-16, 5) ·
  `06-harcama-detay.html` (E-12+E-13, 7) · `07-acilis.html` (E-00, 1)
- Toplam prototip: **7 dosya, 31 yüzey.**

### PM doğrulaması
- Ajanın yazdığı `_uret/denetim.py` mekanik tarayıcısı: **31 yüzey, 0 bulgu.**
- PM bağımsız boşluk denetimi: skala dışı **yalnız ilan edilmiş 3 değer**
  (48/64 kabuk, −4 negatif telafi). Kural tutuyor.
- **`#DC2626` gerçekten yalnız `06-harcama-detay.html`'de** — "kırmızı
  sadece silme onayında" kuralı 7 dosyada korunmuş.
- Özet ekranı gözle incelendi: limit dışı gün **amber**, kırmızı değil;
  "Bu hafta 6 gün limit altında" — olumlu çerçeveleme, suçlama yok.

### Ajanın bulup düzelttiği 2 gerçek render hatası
1. Dikey `<line>`'ın sınır kutusu 0 genişlikte olduğu için `objectBoundingBox`
   gradyanı **hiç çizilmiyordu** → `userSpaceOnUse` (RN'de de aynı sorun olurdu).
2. Yuvarlak uç değerin üstüne taşıyordu; **290 ₺'lik sütun 300 ₺ limit
   çizgisini aşıyor görünüyordu** — veri yanlış okunuyordu. Aralık düzeltildi.

### Dürüstlük kararı (takdire değer)
Hafta ortası görünümünde gelmemiş günler **uydurulmuyor**: oluk boş kalıyor,
ortalama "geçen 4 güne" bölünüyor ve etiketi de öyle yazıyor
("Geçen 4 günün ortalaması"). 7'ye bölseydi sayı yalan olurdu.

---

## K-029 — Silme: geri alınabilir mi? ✅ KARAR: C (etkiye göre ayrıştır)
- Tarih: 2026-09-12
- Ajan `metinler.md`'de **gerçek bir çelişki** buldu:
  - `:207` `sil.govde` → **"Geri alınamaz."**
  - `:465` §20 ekran okuyucu duyurusu → **"Harcama silindi. Geri almak için
    Geri al düğmesi."**
  - `:65` ve `:397` zaten `eylem.geri_al` / `toast.geri_al` anahtarları var.
- Prototip `:207`'yi uyguladı (onay diyaloğu var, geri al toast'ı yok).

### Seçenekler
**A) Diyalog kalsın, "Geri al" metinleri silinsin.** En ucuz; prototip zaten
böyle. Ama her yanlış yazılmış harcamayı silmek için onay ekranı → sürtünme.

**B) Geri al toast'ı olsun, diyalog kalksın.** Modern ve sakin kalıp; yanlış
girilen harcamayı silmek sık bir iş. Ama E-13 yüzeyi (7 durum) çöpe gider.

**C) İkisi de — etkiye göre ayrıştır.** ⭐ PM ÖNERİSİ
- **Tek harcama silme → geri al toast'ı**, diyalog yok. Düşük riskli, sık
  yapılan iş; markanın "sakin, yargısız" tonuna uyar, kullanıcıyı her
  seferinde onay ekranına sokmaz.
- **Taksit serisi silme → onay diyaloğu kalır.** Aylara yayılan birden çok
  kayıt siliniyor; yüksek etki, onay hak ediyor. `sil.govde_taksit` zaten
  "Kalan {adet} taksit de silinecek" diyor.
- Maliyeti: E-13 "yalnız seri silme" yüzeyine dönüşür, tek harcama akışına
  toast eklenir. Küçük bir düzeltme turu.

### ✅ KARAR (2026-09-12) — Mustafa: *"C seçeneğinden devam edelim"*
**Seçenek C onaylandı.** Uygulama TUR E'ye dahil edildi:
- **Tek harcama silme** → onay diyaloğu YOK, **geri al toast'ı** var.
  `sil.govde` ("Geri alınamaz.") bu akıştan kaldırılır; `toast.geri_al`
  ve §20 duyurusu ("Harcama silindi. Geri almak için Geri al düğmesi.")
  geçerli metin olur. Geri alma penceresi tanımlanacak (öneri: 5-7 sn).
- **Taksit serisi silme** → onay diyaloğu KALIR. `sil.govde_taksit`
  ("Kalan {adet} taksit de silinecek. Geri alınamaz.") geçerli.
- `06-harcama-detay.html`'deki E-13 yüzeyi **"yalnız seri silme"**ye dönüşür.
- `metinler.md` §5/§20 çelişkisi bu ayrıma göre düzeltilir.
- `ekran-envanteri.md`'de E-13'ün kapsamı güncellenir.

### PM görüşü
**C.** Ürün kararı olarak da doğru: onayın değeri, gerçekten geri alınamaz ve
yüksek etkili işlemlere saklandığında artar. Her silmede onay istemek onayı
anlamsızlaştırır ve kullanıcı refleksle "Sil"e basmaya başlar.


---

## K-030 — Ürün arama / barkod ile fiyat çekme (TARTIŞMA — Faz 1'e GİRMİYOR)
- Tarih: 2026-09-12
- Mustafa: *"Ürün eklerken kategori kategori veriyoruz… Ürünü direkt arasın
  ve bulsun, mesela Marlboro Touch Blue aradığı anda güncel fiyatı da gelsin.
  Bulamazsa manuel eklesin. Hatta barkod taratarak… Komplekse kaçarsa bu
  aşamada girişmeyelim, backlog'a ekleyelim. Yarın backend kodlanırken
  ürün barkodları için API gerekir o da ücretlidir falan sıkıntı olmasın."*
- **Uygulanmıyor. Bu bir araştırma + karar kaydıdır.**

### PM araştırması (canlı API'ler sorgulandı)

**Bulgu 1 — Zor olan kısım fiyat, ürün tanıma değil.**
- `Open Food Facts` (ücretsiz, açık veri, barkod→ürün): Türkiye'de
  **11.386 ürün**. İşe yarar ama **yalnızca gıda** — sigara/tütün kapsam dışı.
- `Open Prices` (OFF'un fiyat projesi): **TRY para biriminde yalnızca 27
  fiyat kaydı.** Yani Türkiye fiyat kapsaması pratikte **sıfır.**
  (`location_osm_country=Turkey` 311.808 döndürüyor ama `Türkiye` de aynı
  sayıyı veriyor → filtre uygulanmıyor, bu global toplam. PM doğruladı.)

**Bulgu 2 — Market fiyatı doğası gereği API'leşmiyor.**
Fiyat mağazaya, şehre, kampanyaya ve güne göre değişir. "Güncel fiyat"
vaat eden ücretsiz ve güvenilir bir TR perakende API'si yok. Ücretli olanlar
da genelde kurumsal/pahalı ve K-009'a takılır.

**Bulgu 3 — Sigara istisna.**
TR'de tütün fiyatları ilan edilir ve **ülke genelinde tek fiyattır** —
markete göre değişmez. Yani raporun amiral örneği (*"günde 125 TL'lik
sigara"*) **API olmadan**, küçük bir yerel listeyle çözülebilir.

**Bulgu 4 — Barkod taramanın kendisi ücretsiz.**
`expo-camera` (MIT, Expo SDK içinde) barkod taramayı kapsıyor. Maliyet
taramada değil, **taranan barkodun karşılığını bulmakta.**

### 🔑 PM'in asıl görüşü — soruyu yeniden çerçeveleyelim
"Latte Faktörü" tanımı gereği **tekrarlayan** küçük harcamalardır: her gün
aynı kahve, aynı sigara. Bunu izlemek için **küresel ürün veritabanına
ihtiyaç yok** — uygulamanın *senin* ne aldığını hatırlaması yeterli.

**Önerilen çözüm: "Sık alınanlar" (kullanıcının kendi ürün hafızası)**
- Kullanıcı bir harcamayı kaydederken isteğe bağlı ürün adı yazar
  ("Marlboro Touch Blue", "sütlü kahve") ve tutarı girer.
- Uygulama bunu hatırlar. İkinci kez yazmaya başlayınca **önerir, fiyatı da
  önceki kayıttan doldurur.**
- Tek dokunuşla tekrar eklenir → 3 dokunuş kuralı **bozulmaz, iyileşir.**
- **Maliyet: 0.** Sunucu yok, API yok, offline çalışır, K-009 uyumlu.
- Fiyat her zaman **kullanıcının gerçekten ödediği** tutardır — bir API'nin
  tahmininden daha doğru.

Bu, istenen değerin büyük kısmını sıfır maliyet ve sıfır risk ile verir.

### Kademeli plan (backlog)
- **Faz 1: GİRMİYOR.** Mevcut kategori akışı korunur. Gerekçe: 3 dokunuş
  kuralı ürünün çekirdeği; olgunlaşmamış ürün arama bunu yavaşlatır.
- **Faz 2 — "Sık alınanlar":** yukarıdaki kullanıcı hafızası. Ücretsiz,
  offline, yüksek değer. **Önerilen ilk adım.**
- **Faz 2.5 — Sigara/tütün fiyat listesi:** küçük, elle bakımı yapılan
  yerel liste (ulusal tek fiyat olduğu için mümkün). Raporun amiral
  senaryosunu API'siz çözer. Fiyat değişince uygulama güncellemesiyle gelir.
- **Faz 3 — Barkod tarama:** `expo-camera` ile tarama (ücretsiz) →
  Open Food Facts'ten **yalnız ürün ADI** (ücretsiz, gıdada kısmi kapsama).
  **Fiyat yine kullanıcıdan / kendi hafızasından.** Barkod→fiyat vaat edilmez.
- **ASLA (bu bütçede):** ücretli perakende fiyat API'si.

### Mustafa'nın endişesine doğrudan cevap
*"Yarın backend kodlanırken ürün barkodları için API gerekir, o da ücretlidir"*
→ Bu riski **tasarım kararıyla** ortadan kaldırıyoruz: hiçbir aşamada
ücretli fiyat API'sine bağımlılık kurulmuyor. Fiyatın kaynağı ya kullanıcının
kendisi ya da ulusal tek fiyatlı tütün listesi. Barkod yalnızca **isim**
getirir ve o da ücretsizdir.


---

## K-031 — Ücretsiz ürün/fiyat entegrasyonu: ikinci tur araştırma
- Tarih: 2026-09-12
- Mustafa: *"şu anda da ürün alırken verirken eğer ücretsizse bir çözüm bul,
  sigara için de öyle entegrasyonunu yapalım"* + *"yarın kullanıcı artınca
  API ile halletmemiz gerekebilir"*

### Araştırma sonuçları (canlı sorgulandı)

| Kaynak | Sonuç | Kullanılabilir mi? |
|---|---|---|
| Open Food Facts — TR gıda | 11.386 ürün | Kısmen (yalnız gıda) |
| **Open Products Facts — TR gıda dışı** | **98 ürün** | ❌ Pratikte boş |
| OFF `tobacco` / `cigarettes` kategorisi | boş | ❌ Tütün yok |
| Marlboro (global, tüm markalar) | 101 kayıt, **fiyat yok**, isimler tutarsız ("cigarette", "Cigarettes") | ❌ |
| Open Prices — TRY | **27 kayıt** | ❌ |
| Resmi TR tütün fiyat API'si | Makine okunur kaynak yok (fiyatlar ilan ediliyor ama PDF/HTML) | ❌ API olarak |

### 🔴 KRİTİK BULGU — ücretsiz veritabanlarında veri kalitesi sorunu
PM **uydurma bir barkod** girdi (`8691234567890`) ve Open Food Facts
**"riso basmati raja"** döndürdü — Türk GS1 önekine (869) atanmış bir İtalyan
pirinci kaydı, tamlık %48.
**Sonuç:** barkod→isim bile güvenilir değil. Kullanıcı sigara paketi okutup
ekranda "riso basmati raja" görürse ürüne olan güven anında biter.
Kalabalık kaynaklı (crowd-sourced) veri **doğrulanmadan kullanılamaz.**

### PM önerisi — şimdi entegre edilebilecek ÜCRETSİZ çözüm
**Barkod/dış veritabanı YOK. İki yerel çözüm, ikisi de sıfır maliyet:**

1. **Ü-1 "Sık alınanlar"** (Faz 2'nin ilk maddesi olmalı)
   Kullanıcı ürün adı + tutar girer, uygulama hatırlar, ikinci kez tek
   dokunuşla gelir. Fiyat **kullanıcının gerçekten ödediği** tutardır —
   herhangi bir API'den daha doğru. Offline, sunucusuz, K-009 uyumlu.

2. **Ü-2 "Tütün fiyat listesi" — uygulama paketinin İÇİNDE**
   TR'de tütün fiyatı **ülke genelinde tek**, markete göre değişmez.
   30-60 SKU (popüler markalar) sigara içenlerin büyük çoğunluğunu kapsar.
   Liste uygulama paketiyle gelir, **sunucu ve API gerekmez**; zam olunca
   uygulama güncellemesiyle yenilenir.
   → Mustafa'nın "sigara için de entegrasyonunu yapalım" isteğinin
   **ücretsiz ve uygulanabilir** karşılığı budur.

3. **Barkod tarama → ERTELENDİ.** Tarama bedava (`expo-camera`) ama
   taranan barkodun karşılığı güvenilir değil (yukarıdaki bulgu). Güven
   riski, sağladığı kolaylıktan büyük.

### "Kullanıcı artınca ne olacak?" — dürüst cevap
Ölçeklenince ücretsiz üçüncü taraf fiyat API'si yine **olmayacak** (TR
perakende fiyatı doğası gereği mağazaya/güne göre değişiyor). Ölçekteki
gerçek çözüm **kendi kullanıcı verimiz**: binlerce kullanıcı "Marlboro Touch
Blue = 135 ₺" girdiğinde bu veri **bizim** olur ve üçüncü taraftan daha
güncel olur.
Maliyeti: küçük bir veritabanı + basit bir toplama servisi (ücretli üçüncü
taraf API'si değil, kendi altyapımız). Bu **Faz 3** konusudur ve gelir
üretmeye başladıktan sonra ele alınır. Şimdi karar verilmesi gerekmiyor;
önemli olan **o yola çıkışı kapatmamak** — Ü-1'in veri modeli buna hazır
tasarlanacak (ürün adı + tutar + tarih ayrı alanlar, serbest metin değil).


---

## K-032 — Aşama 2 tam denetim: REVİZE (5 blocker) ama marka hissi GEÇTİ
- Tarih: 2026-09-12
- `design-reviewer` kararı: **REVİZE GEREKİYOR.**

### ✅ En önemli sonuç: Geçiş 3 (marka hissi) GEÇTİ
Denetçi: *"bu prototip canlı."* Kahraman gösterge tek SVG halka değil —
çukur oluk + iç koyu saç teli + iç beyaz parlama + gradyanlı dolgu +
speküler şerit + dört katmanlı topuz. **"Seçili = çukur, seçilebilir =
kabarık"** tek tutarlı fizik kuralı; onay ikonu yerine derinlik kullanılmış.
12 dosya klon değil, her ekranın mood'u ayrı. Utandırmama ilkesi tutarlı.
→ Mustafa'nın iki kez reddettiği "ruhsuz/amatör" sorunu **çözüldü.**

### Blockerlar — hepsi tutarlılık/kapsam, stil değil
1. **🔴 Onaylı karar sessizce tersine çevrilmiş.** `02-harcama-ekle.html:60`
   "Kafe" çipi **önceden seçili** geliyor. `ekran-envanteri.md:135` ise
   açıkça: *"Kategori önceden seçili gelmez. Gelseydi 2 dokunuşa inerdi ama
   yanlış kategoriye sessizce kayıt riski doğardı."* Tipik akış 3→**4
   dokunuşa çıkıyor.** PM doğruladı. → Onaylı karara dönülecek.
2. **🔴 Varsayılan ödeme tipi 3 farklı değer gösteriyor.** PM doğruladı:
   `11-ayarlar.html`'de **3 "Kart" + 3 "Nakit"**, `02`'de Nakit ama not
   "Kart seçili" diyor. Geliştirici varsayılanı spec'ten okuyamaz.
   → Tek değere sabitlenecek: **Kart** (`ekran-envanteri.md §4`).
3. E-17 **"hiç kategori limiti yok"** boş durumu çizilmemiş (ajan dürüstçe
   bildirmişti, doğrulandı).
4. E-11 **"Taksit açık"** özel durumu yok — taksit sayısı seçici hiç çizilmemiş.
5. E-10 **"limitsiz"** varyantı yok (`limitsiz` dizesi dosyada hiç geçmiyor).

### Önemli (blocker değil)
6. `danger` kapsamı notları çelişiyor (06 ve stil.css "yalnız 2 bağlam" diyor,
   artık 4 bağlam var) · 7. `denetim.py` `--danger-ink`/`--danger-soft`
   taramıyor · 8. E-11 hata yüzeyi matristeki 3 hatayı çizmiyor, "gelecek
   tarih" hatası hiç yok · 9. `stil.css` başlığı v3.0 diyor, sözleşme v3.1 ·
   10. E-17'nin 3 yüzeyinde kaydırma kesimi ölçülmedi.

### Tartışmalı kararların hepsi KABUL edildi (1-5)

---

## K-033 — Ürün adı + gömülü tütün listesi FAZ 1'E ALINDI
- Tarih: 2026-09-12
- Mustafa: *"Tamam gömülü liste ve kullanıcının manuel girmesi mevzusunu
  halledelim. Ekranları buna göre güncelleyelim."*
- K-030/K-031'de **Faz 2** olarak planlanan Ü-1 ve Ü-2 → **Faz 1'e alındı.**

### Kapsam
1. **Ürün adı alanı (opsiyonel)** — harcama eklerken kullanıcı ürün adı
   yazabilir ("Marlboro Touch Blue", "sütlü kahve"). Zorunlu değil.
2. **Sık alınanlar (kullanıcı hafızası)** — yazmaya başlayınca kendi
   geçmişinden öneri gelir, **tutar önceki kayıttan dolar.**
3. **Gömülü tütün fiyat listesi** — uygulama paketi içinde, sunucu/API yok.
   TR'de tütün ulusal tek fiyat olduğu için mümkün.
4. **Manuel giriş** — bulamazsa adı kendi yazar, tutarı kendi girer.

### 🔴 BAĞLAYICI TASARIM KISITLARI
- **3 dokunuş kuralı BOZULMAYACAK.** Ürün adı **opsiyonel** bir alandır;
  kullanılmadığında akış aynen tutar → kategori → Kaydet.
  Kullanıldığında akışı **kısaltmalı** (öneri seç → tutar otomatik → Kaydet
  = 2 dokunuş), uzatmamalı.
- **Fiyat otoriter sunulmaz.** Gömülü liste zamla eskir. Fiyat **ön-dolgu**
  olarak gelir ve **her zaman düzenlenebilir.** "Güncel fiyat" iddiası
  yazılmaz — uygulamanın yalan söylememesi ürünün çekirdek ilkesi
  (bkz. K-028 grafik hatası, K-026 hafta ortası ortalaması).
- **UI'da teknik açıklama YOK** (K-019) — "liste uygulamaya gömülüdür",
  "sunucudan çekilir" gibi ifadeler geçmez.
- **Veri modeli Ü-5'e hazır olsun:** ürün adı · tutar · tarih **ayrı
  alanlar**, serbest metin değil. İleride kendi fiyat verimizi toplamak
  istersek dönüşüm gerekmesin.
- Tütün listesi **fiyat kaynağı/tarihi** koda not olarak yazılır (kullanıcıya
  değil), güncelleme sorumluluğu belli olsun.

### Blocker 1 ile ilişkisi — birlikte çözülüyor
Tasarımcı kategoriyi "son kullanılanla" doldurmak istemişti (onaylı kararı
sessizce çiğneyerek). O ihtiyacın **doğru çözümü sık alınanlardır**: ürün
seçilince kategori de onunla gelir — tahminle değil, kullanıcının kendi
geçmişiyle. Yani blocker 1'i onaylı karara döndürüyoruz **ve** tekrar giriş
sorununu bu özellikle gerçekten çözüyoruz.


---

## K-034 — Blocker turu tamam + ürün girişi beklenmedik şekilde canlı
- Tarih: 2026-09-12

### Sonuçlar (PM doğruladı)
- ✅ **A1 kapandı:** açılış yüzeyinde seçili kategori çipi **0**. Onaylı karara
  dönüldü, tipik akış yine **3 dokunuş**. Prototip notu artık gerekçeyi
  doğru yazıyor.
- ✅ **A2 kapandı:** 11 ödeme yüzeyinin tamamı **Kart**. Tutarsızlık bitti.
- ✅ `danger` 4 bağlam notları · `denetim.py` yaması · E-11 gelecek-tarih
  hatası · `05-ozet` basılı durumu · `stil.css` v3.1 → hepsi yapıldı.
- `denetim.py`: **60 yüzey, 0 bulgu.**

### 🔴 PM'İN HATASI — üreteç sistemi yanlış teşhis ettirdi
Önceki tur limitle ölünce PM "diskte hiçbir şey değişmemiş" dedi. **Yanlıştı.**
PM yalnızca **çıktı HTML'lerini** kontrol etti; oysa ölen ajan
`_uret/s02_harcama_ekle.py` ve `lib.py`'yi **düzenlemiş**, sadece HTML'i
yeniden üretmeye yetişememişti.
Bu turda HTML yeniden üretilince **K-033'ün ürün girişi yüzeyleri (C/D/E/F)
kendiliğinden yayına girdi** — E-11 artık 11 yüzey.
**Ders:** üreteç tabanlı sistemde "iş yapıldı mı?" sorusu **kaynak**
(`_uret/*.py`) kontrol edilerek yanıtlanır; çıktıya bakmak yetmez.
Ajan bu durumu dürüstçe bildirdi ve onaylı+tamamlanmış işi geri almayarak
doğru karar verdi (K-033 zaten onaylıydı).

### PM'in ikinci hatası — yanlış alarm
PM ilk render'da "hiç metin görünmüyor" diye hata sandı. Sebep prototipte
değil **render ayarındaydı**: headless tarayıcı fontlar yüklenmeden ekran
görüntüsü alıyordu. `--virtual-time-budget=6000` ile düzeldi.
(Bu, PM'in kendi ölçüm hatasını tasarım kusuru sanmasının 3. vakası —
44pt aritmetiği, CSS grep yorum satırları, şimdi font yüklemesi.
**Kural: bir kusur bildirmeden önce ölçüm aracını doğrula.**)

### Ürün girişi — gözle doğrulandı, çalışıyor
E-11'de: **"Ne aldın? (isteğe bağlı)"** alanı · **Sık alınanlar** şeridi
("Sütlü kahve · 95 ₺", "Marlboro Touch Blue", "İstanbulkart · 100 ₺") ·
tütün eşleşmesi yüzeyi · manuel giriş. Opsiyonel alan akışı bozmuyor;
"3 dokunuş tamam" yüzeyinde sık alınanlar şeridi **kapanıyor**.

### 🟡 YENİ BULGU — sık alınanlar çipinde metin taşması
Açılış yüzeyinde "Sık alınanlar" çipleri **3 satıra sarıyor ve ilk satır
kırpılıyor**: "Marlboro Touch Blue" çipinde "Marlboro" üstten kesilmiş,
`₺` görünmüyor. "Sütlü kahve · 95 ₺" de 3 satıra bölünmüş.
→ Sonraki turda düzeltilecek: çip tek satıra kırpılsın (ellipsis) veya
çip genişliği/ürün adı kısaltma kuralı tanımlansın. Ürün adları uzun
olabileceği için bu kural `tokens.md`'ye yazılmalı.


---

## K-035 — AŞAMA 2 TASARIM ONAYI ✅ ONAYLANDI (Aşama 2 → 3)
- Tarih: 2026-09-12
- Prototip: `projects/trinkow/docs/design/prototip-v3/index.html`
- **design-reviewer kararı: ✅ PASS**

### Kapsam
**13 dosya · 62 yüzey.** Faz 1'in 15 ekranının tamamı, zorunlu durum
matrisiyle birlikte. Ürün adı + sık alınanlar + gömülü tütün listesi dahil.

### Yolculuk (kayda geçsin)
| Tur | Sonuç |
|---|---|
| Yön A "Defter" | ❌ Mustafa: "ruhsuz, amatör" |
| Yön C "Gün Işığı" | ❌ Mustafa: "rezalet olmuş" |
| **Claymorphism** | ✅ "güzel tasarım" → boşluk ritmi düzeltmesi → "beğendim" |
| Tam denetim | REVİZE (5 blocker) |
| Blocker turu + ürün girişi | A1/A2 + küçük maddeler kapandı |
| Kapsam turu | A3/A4/A5 + çip taşması kapandı |
| **Delta denetim** | ✅ **PASS** |

### Denetimin doğruladıkları
- **Geçiş 3 (marka hissi) GEÇTİ:** *"bu prototip canlı."* Kahraman
  göstergenin katmanlı fiziği, "seçili = çukur / seçilebilir = kabarık"
  tutarlı kuralı, 12 dosyanın ayrı mood'u.
- 11 blocker/önemli maddenin **tamamı** kapandı, kod okunarak doğrulandı.
- Utandırmama ilkesi tutarlı: limit dışı amber, kırmızı yalnız 4 izinli
  bağlamda, ünlem yok.
- **Metin kaldırma kararı ONAYLANDI:** limitsizliği "kapatılması gereken
  açık" gibi konumlayan metinler çıkarıldı. Denetçi: farkındalık kaybı yok
  (limitsizlik iki yerde okunuyor + "Limitleri aç" yolu açık), yargı kalktı.
- Bloklayan yeni bulgu: **yok.**
- Tek öneri (bloklamaz): `.cip`'te `overflow:hidden` yok → yalnız prototip
  fidelity; RN'de `numberOfLines=1` bunu zaten kapatıyor.

### ✅ ONAYLANDI (2026-09-12) — Mustafa: *"devam o zaman, yap"*
**Aşama 2 kapandı. Aşama 3 (Geliştirme) açıldı.**
PM'in önerdiği yaklaşım da onaylandı: 15 ekran birden kodlanmayacak,
önce **yürüyen iskelet** (bkz. K-036).

### Aşama 3 devir notu (design-reviewer'dan, frontend-developer'a)
1. `tokens.md §7.6` bağlayıcı: her çip `numberOfLines={1}`, `maxWidth 240`;
   ad `maxWidth 120` + `ellipsizeMode="tail"`, tutar `flexShrink:0`,
   `accessibilityLabel` daima tam ad. **`₺` kırpılamaz.**
2. **`HeroPlain` ayrı bileşendir**, `LimitGauge`ın varyantı değil. Yay,
   `EmptyGauge`, `warning` rengi ve "Limit belirle" birincil çağrısı YASAK.
3. `danger #DC2626` yalnız 4 bağlam. `_uret/denetim.py` **gerçek bir sızıntı
   yakalamış bir kapıdır** — RN tarafında eşdeğerini CI'a bağla.
4. Ödeme tipi tek varsayılan: **Kart.** Taksit yolu ayrı "Uygula" adımı
   almaz (+2 dokunuş) ve yalnız Kart seçiliyken görünür.
5. **Tutar boşken Kaydet `disabled`** olmalı — "boş tutar" hata durumu
   bilinçli tasarlanmadı; kod tarafında da doğurma.
6. `stil.css`'teki çerçeve/kabuk katmanı (`grid`/`::before`/`z-index`)
   **RN'e port edilmez**; yalnız `.pad` içi flexbox katmanı port edilir.


---

## K-036 — Aşama 3 stratejisi: YÜRÜYEN İSKELET önce (PM kararı, onaylandı)
- Tarih: 2026-09-12
- Mustafa PM'in önerisini onayladı.

### Karar
15 ekran birden kodlanmayacak. İlk tur **tek ekranlık çalışan uygulama**:
Expo kurulumu (New Architecture) + `tokens.md` → `src/theme/tokens.ts` +
**yalnız E-10 Bugün/pano** + `expo-sqlite` ile bir harcama yaz/oku.
Hedef: **Mustafa'nın simülatöründe gerçekten açılması.**

### Gerekçe — dört teknik bilinmez henüz test edilmedi
Prototip HTML'dir; RN'de aynı görünüp görünmeyeceği **kanıtlanmadı**:
1. **Clay'in iç gölgesi (inset).** Dokümantasyondan "New Architecture'da
   çalışır" diye doğrulandı ama **gerçek ekranda görülmedi.** Claymorphism'in
   bütün ruhu o kabarıklıkta; RN'de sönük çıkarsa tasarım dili çöker.
2. **Kahraman gösterge.** HTML'de inline SVG → RN'de `react-native-svg`.
   Gradyan + topuz + katmanlı yay aynı çıkacak mı?
3. **`₺` + Montserrat.** Glif doğrulandı ama gömülü font + tabular rakam
   hizalaması RN'de test edilmedi.
4. **Ritim.** Prototip bir kez yalan söylemişti (flex-shrink; K-026).
   RN'de ölçüler kayabilir.

Bu dördü tek ekranda ortaya çıkar. **Clay RN'de tutmuyorsa 1 ekranlık emek
gider, 15 değil.** Tasarımda aynı yaklaşım (3 ekranla test) doğru çıkmıştı.

### İkinci gerekçe — kesinti örüntüsü
Bu oturumda ajanlar **5 kez** yarıda kesildi (2 API hatası, 3 oturum limiti).
Kodlama tasarımdan büyük bir iş; küçük parçalar zorunlu. İlk parça en
değerli yere konuyor.

### Bağımlılıklar (hepsi ücretsiz, K-009 uyumlu)
`expo` · `expo-sqlite` · `expo-router` · `react-native-svg` ·
`@expo-google-fonts/montserrat` · `@expo-google-fonts/poppins` ·
`expo-haptics` (K-011'de onaylı) · TypeScript. Sunucu yok, backend yok.

---

## K-037 — Tütün fiyat listesi için GERÇEK VERİ gerekiyor (AÇIK, acil değil)
- Tarih: 2026-09-12
- Ü-2 (gömülü tütün fiyat listesi) Faz 1 kapsamında (K-033).
- **PM güvenilir fiyat verisi çekemiyor** — K-031'de araştırıldı, ücretsiz
  ve güvenilir TR kaynağı yok.
- **Mustafa'dan gereken:** 20-30 popüler markanın güncel fiyatı.
- Alternatif: yapı boş kurulur, fiyatlar sonra doldurulur.
- **Zamanlama:** Faz 1'in sonuna doğru, E-11 kodlanırken. Şimdi bloklamıyor.


---

## K-038 — Repo yeniden yapılandırıldı: AJANS / PROJELER ayrımı
- Tarih: 2026-09-12
- Mustafa: *"Dosyalama karman çorman oldu. Otomasyon ajans dosyaları AYRI
  olsun, trinkow AYRI olsun. Toparla."*

### Yeni yapı
```
ai-ajans/
├── CLAUDE.md · .claude/agents/     ← kökte kalmak ZORUNDA (Claude Code buradan okur)
├── agency/                          ← otomasyon (tüm projelerde ortak)
│   ├── templates/ reference/ vendor/
└── projects/trinkow/                ← ürün
    ├── docs/ status/ app/
```

### Taşınanlar
- `docs/templates/`, `brandbook-template.md` → `agency/templates/`
- anti-pattern listesi, `referans-repolar.md`, `rn-tasarim-kisitlari.md`,
  `open-design-entegrasyon.md` → `agency/reference/`
- `vendor/open-design`, `docs/design/design-systems` → `agency/vendor/`
- `docs/*` (CONTEXT, brand, design, content, social) → `projects/trinkow/docs/`
- `status/` → `projects/trinkow/status/` · `src/mobile` → `projects/trinkow/app`

### Ayrım kuralı (belgelendi)
> *"İkinci bir proje başlasa bu dosyayı kopyalar mıydım?"*
> Evet → `agency/` · Hayır → `projects/<ad>/`
Proje-özel kural geçersiz kılmaları `agency/`'de DEĞİL, o projenin
`CONTEXT.md`'sinde yaşar (örnek: emoji yasağı K-004, gölge serbestliği
K-019, Poppins izni K-024).

### Uygulama
- **287 yol referansı / 62 dosya** sıralı dönüşümle güncellendi (özelden
  genele; `referans-repolar.md` ile `referans-repolar-trinkow.md`
  karışmasın diye tam dosya adıyla eşleşme).
- `.claude/agents/pm-orchestrator.md`'ye yapı notu eklendi; **aktif proje
  `CLAUDE.md`'de ilan ediliyor** → ikinci proje geldiğinde ajan yolları
  hardcode etmiyor.
- `agency/README.md` ve `projects/README.md` yazıldı.
- `.gitignore`'a Expo girdileri (`node_modules/`, `.expo/`, `dist/`).

### Doğrulama
- ✅ Üreteçler çalışıyor (`Path(__file__).parent` kullandıkları için taşımaya
  dayanıklıydı) — `denetim.py` → 62 yüzey, 0 bulgu.
- ✅ Gerçek kırık referans **yok** (ilk taramam yanlış alarm verdi:
  `projects/trinkow/docs/X` içindeki `docs/X` parçasını yakalıyordu).
- ✅ Prototip, Expo projesi, tüm status/docs dosyaları yerinde.

### PM notu
Bu, PM'in **beşinci** ölçüm-aracı hatasıydı (44pt aritmetiği · CSS yorum
satırları · font yüklemesi · üreteç kaynak/çıktı ayrımı · şimdi alt-dizgi
eşleşmesi). Kural pekişti: **bir sorun bildirmeden önce ölçüm aracını
doğrula.**


---

## K-039 — ✅ YÜRÜYEN İSKELET ÇALIŞIYOR — dört bilinmez de kapandı
- Tarih: 2026-09-12
- Uygulama simülatörde çalışıyor (iPhone 17, iOS 26.5, Expo Go 57).
- Ekran görüntüleri: `projects/trinkow/app/.onizleme/` — **PM gözle doğruladı.**

### Dört bilinmeze cevap (ajan piksel ölçtü, PM görselden teyit etti)
1. **Clay inset TUTUYOR.** ✅ Kahraman kartın üst iç kenarı `255,255,255`
   (beyaz inset), alt iç kenarı kararıyor (koyu inset), altında dış gölge
   `198,210,236`. 4 katmanlı `boxShadow` iOS'ta bekleneni veriyor.
   **Tasarım dilini değiştirmeye gerek yok** — 14 ekranın önü açık.
2. **Kahraman gösterge** `react-native-svg` ile prototiple **ayırt edilemiyor**:
   gradyan dolgu, çukur oluk, kabarık topuz, limit dışında ikinci amber yay.
3. **`₺` + Montserrat tabular sorunsuz.** Metin genişlikleri piksel düzeyinde
   örtüşüyor: "3.000 ₺" 50,3pt (prototip 50,7) · "1.200 ₺" 47,0 (47,0) ·
   "940 ₺" 51,3 (51,3). Tutarlar sağa hizalı.
4. **Ritim kaymıyor.** Çubuk yüksekliği 18,0pt (prototip 18,3), çubuk arası
   58,3 (58,0), kart içi sol ofset ikisinde de 45,0. 4/8/12/16/24 tutuyor.

### 🔴 Ajanın bulup düzelttiği gerçek hata — SVG alfa tuzağı
`ClayGloss`'ta `stopColor="rgba(255,255,255,0)"` yazılmıştı.
**SVG `stop-color` alfa taşımaz** → parlama opak beyaz çıkıyor ve kahraman
kartın `primary-soft` zeminini tamamen örtüyordu (kart beyaz görünüyordu).
`stopOpacity`'ye taşındı. Şimdi kart zemini `#E4EEFE` — prototiple aynı piksel.
Bu, tarayıcıda fark edilmeyip yalnız RN'de çıkan türden bir hata; yürüyen
iskeletin var olma sebebi tam olarak budur.

### Seed verisi düzeltildi
`semasi.ts` yeniden yazıldı, gün planı tablosu (kuruş integer, float yok).
Market **2.180/3.000 ₺**, Kafe **940/1.200 ₺** (limit 800→1.200 hatalıydı),
bugün 95+42+43=180/300, dün 360 (limit dışı), ay içi aşım **6**.
`ORNEK_VERI_SURUMU` eklendi: eski kurulumdaki yanlış sayılar kendiliğinden
tazeleniyor, **kullanıcı verisi bayrağı varsa dokunmuyor.**

### PM'in görselden teyit ettikleri
- Limit dışı yüzeyinde **kırmızı yok, ünlem yok**. Ana yay dolu kalıyor,
  dışına amber yay çıkıyor, sayı amber.
- *"Limitin 60 ₺ üzerindesin."* — olgu bildirimi, suçlama yok.
- *"Bu ay 6. limit aşımı · Limit gerçekçi mi. Birlikte bakalım."* +
  "Limiti gözden geçir" — destekleyici, azarlayıcı değil.
- **Utandırmama ilkesi gerçek uygulamada çalışıyor.**

---

## K-040 — Seçili çipte halka var mı? (PM kararı)
- Ajan çelişki bildirdi: prototipte `.cip.secili` 2pt `primary-text` halkası
  var (`inset 0 0 0 2px`); `tokens.md §7.6` ise seçili durumu yalnız
  `primary-soft` + `clay.sunken` + nokta olarak tanımlıyor, halkadan söz etmiyor.
  Ajan token'ı otorite kabul edip halkayı koymamış.

### KARAR: halka YOK — token otoritedir
Gerekçe:
1. `tokens.md` bu projede **tek kaynak** olarak ilan edildi; `design-reviewer`
   mekanik denetimi de ona karşı yapıyor. Prototip token'ı geçersiz kılamaz.
2. Clay'in kendi kuralı zaten seçimi anlatıyor: **"seçili = çukur,
   seçilebilir = kabarık."** Halka bu bilgiyi tekrar ediyor.
3. PM ekran görüntüsünde doğruladı: "Takip" çipi halkasız da net biçimde
   seçili okunuyor (yumuşak zemin + nokta + çukurluk).

### Yapılacak — sapma kapatılsın
`tokens.md §7.6`'ya **"seçili çipte halka YOKTUR"** açıkça yazılacak ve
**prototip üreteci de halkayı bırakacak**, böylece prototip ile kod ayrışmaz.
(Ayrışma bu projede daha önce pahalıya mal olmuştu — K-032'de tasarımcı
onaylı bir kararı sessizce tersine çevirmişti.)


---

## K-041 — D-2a denetimi: 4 sapma kabul, 2 reddedildi (PM kararı)
- Tarih: 2026-09-17
- Durum: ✅ PM kararı, Mustafa onayı gerekmiyor (tasarım dili değişmiyor).

`frontend-developer` D-2a'yı tamamladı: E-11 harcama ekle · E-12 detay ·
E-13 taksit silme onayı · E-14 kayıtlar + sekme navigasyonu. PM bağımsız
doğruladı: `tsc` 0 hata · 5 rota dosyası yerinde · **yeni bağımlılık yok** ·
para integer korunmuş · UI'da emoji yok (K-004).

Ajan 6 sapmayı **sessizce çözmek yerine bildirdi** — K-032'de yaktığımız
dersin tuttuğunun kanıtı.

### KABUL EDİLEN (4)
1. **E-11'de sistem tarih seçici yok, "Bugün/Dün" çipi var.**
   `@react-native-community/datetimepicker` yeni bağımlılık olacağı için
   eklenmedi. PM: doğru karar — Faz 1'de dünden eskiye giriş kapsam dışı,
   ayrıca çip çözümü E-11'in dokunuş bütçesini koruyor. Yan etki:
   "gelecek tarih" hata durumu artık ulaşılamaz, sorun değil.
2. **Kategori ızgarasında seçili halkanın kaldırılması** — K-040'ın doğru
   genişletilmesi. Çipte yasaklanan halka ızgarada da olmamalı.
3. `.expo/types/router.d.ts` elle güncellendi — gitignored, otomatik üretilen.
4. **Ürün adı canlı araması (`urunAra`) bağlanmadı** — Faz 2 (Ü-1) işi.
   E-11'deki sabit "sık alınanlar" listesi Faz 1 için yeterli.

### REDDEDİLEN (2) → düzeltme turuna gönderildi
1. **E-12'de tutar salt okunur bırakılmıştı.** Ajanın gerekçesi "prototipin
   hiçbir durumu tutar düzenleme akışını çizmiyor" idi. **Geçersiz:**
   prototipte çizilmemiş olmak yasak anlamına gelmez, ürün gereksinimi kazanır.
   **F-8** ("harcama düzenleme/silme — yanlış giriş kaçınılmaz") tam olarak
   bunun için var; kullanıcının en olası hatası tutarı yanlış girmektir
   (150 yerine 1500). Tutar düzenlenemezse kullanıcı silip baştan girecek —
   F-8'in çözmek için var olduğu sorunun kendisi.
2. **Akış C (sola/sağa kaydırma) hiç uygulanmamıştı.** `ekran-envanteri.md`
   §C/§D'de tanımlı ve K-035 ile onaylı. Sola kaydır → "Tekrarla"
   ("Latte Faktörü akışı" — ürünün imza davranışı), sağa kaydır → "Sil"
   (K-029'un iki yolu geçerli). `gesture-handler` + `reanimated` zaten
   `package.json`'da → yeni bağımlılık gerekmiyor, uygulanmaması için
   teknik gerekçe yok. `ExpenseRow` tek yerden çözer (E-10 + E-14 ortak).

### Ayrıca — metin senkronu istendi
Kodda `metinler.md`'de anahtarı olmayan iki metin kullanılmış
("Ne aldın? (isteğe bağlı)", "Sık alınanlar"). Metin hem `metinler.md`'ye
hem `metinler.ts`'ye yazılacak. **P-4 kuralı:** `metinler.md` metnin tek
kaynağıdır; koda yazıp dokümana yazmamak K-040'ın tekrarıdır.


---

## K-042 — Kesilen oturumdan raporlanmamış bir çelişki bulundu (tutar eşiği)
- Tarih: 2026-09-17
- Durum: ✅ Çözüm doğru, **doküman senkronu D-1b'ye eklendi.**

12 Eylül'de kesilen oturum bir `tokens.md` ↔ prototip çelişkisini çözmüş
ama rapor edemeden sonlanmış. PM kodu tararken buldu —
`src/components/AmountWell.tsx` içindeki yorumda duruyordu:

> `tokens.md §7.11`: gösterim 7 karakteri AŞARSA (8+) tutar `hero` (56pt) →
> `display` (32pt) rolüne iner. Prototipte ise "1.250,50" (8 karakter) hâlâ
> `t-hero` ile çizili — yani prototip kendi kuralını çiğniyor.

### KARAR: token otoritedir, çözüm doğru — değişiklik yok
Ajan 8+ karakterde küçültmeyi uygulamış, prototip görüntüsünü yok saymış.
Bu K-040 ile aynı karar hattı ve doğrusu budur.

### Çıkarılan ders (süreç)
Bir oturum kesildiğinde ajanın bildirmek üzere tuttuğu çelişkiler kaybolur.
Bu sefer kodda yorum olarak kaldığı için yakalandı — şansa kalmamalı.
**Kural:** PM bir oturumu devralırken `src/` içinde çelişki işaretlerini
(🔴 / "çelişki" / "rapora bildirildi") tarar.

### Yapılacak — D-1b'ye eklendi
`tokens.md §7.11`'e "prototip 8 karakterde küçültmeyi göstermiyor, **kural
geçerlidir**" notu düşülecek ve prototip üreteci düzeltilecek; böylece
prototip ile kod ayrışmaz.


---

## K-043 — Kaydırarak silmenin rengi: `tokens.md` kendi içinde çelişiyor
- Tarih: 2026-09-17
- Durum: ✅ PM kararı verildi. **Uygulaması D-2b'ye devredildi** (tek başına
  bir ajan turunu hak etmeyecek kadar küçük: iki renk sabiti).

### Çelişki (ajan bildirdi, PM doğruladı — gerçek)
| Yer | Ne diyor |
|---|---|
| `tokens.md` §1.3 (`danger` satırı) | "**Yalnız dört bağlam:** E-13 · E-19 · form hatası kenarlığı · silme toast'ının göstergesi. Ortak ölçüt (K-029): **yüksek etkili + geri alınamaz.** Tek harcama silme onaysızdır, **kırmızı görmez**." |
| `tokens.md` §7.3 (harcama satırı tablosu) | "Kaydırarak silme: sağa kaydırma → **`danger` zeminli** 'Sil'." |

İkisi aynı anda doğru olamaz: tek harcamayı kaydırarak silmek hem
"kırmızı görmez" hem "danger zeminli" olamaz.

Ajan §1.3'e uydu ve nötr `groove` zemini kullandı. Bu **benim talimatım**
doğrultusundaydı, ajanın hatası değil — ve çelişkiyi sessizce yutmayıp
bildirdi (doğru davranış).

### KARAR: ikisi de tam doğru değil → `danger-soft` + `danger-ink`
Gerekçe: **doygunluk, riskle orantılı olmalı.**
1. Nötr `groove` zeminli bir "Sil" **yetersiz uyarı.** Kaydırmada ortaya
   çıkan bir eylemde rengin kendisi birincil sinyaldir; gri "Sil" kullanıcıya
   eylemin yıkıcı olduğunu söylemez.
2. Tam doygunlukta `danger #DC2626` ise **fazla.** §1.3'ün ölçütü sağlam:
   kırmızıyı her yere serperseniz E-13'te (geri alınamaz seri silme) hiçbir
   şey ifade etmez. Tek harcama silme geri alınabilir (6 sn toast, K-029).
3. `danger-soft #FAE1E1` zemin + `danger-ink #C62222` metin/ikon: kırmızı
   ailesinde olduğu için yıkıcılığı tereddütsüz okutur, ama tam doygunluğu
   geri alınamaz onaylara saklar. Risk arttıkça doygunluk artar — tutarlı,
   öğrenilebilir bir kural.
4. "Tekrarla" tarafı `primary-soft`/`primary-text` olarak kalır — doğru.

### Yapılacak
- (kod, D-2b) `src/components/ExpenseRow.tsx`: sil tarafı zemin `groove` →
  `danger-soft`, metin/ikon → `danger-ink`.
- (doküman, D-1b) `tokens.md` §1.3'e beşinci bağlam olarak
  "kaydırarak silme affordance'ı — **`danger-soft`/`danger-ink`**, tam
  doygunluk değil" eklensin; §7.3 satırı "`danger` zeminli" → "`danger-soft`
  zeminli" olarak düzeltilsin. İki bölüm birbirine referans versin ki
  çelişki geri gelmesin.

### Not — erişilebilirlik (ajan bildirdi)
Yalnız-kaydırmayla erişilen eylemler VoiceOver/TalkBack'te zor tetiklenir.
Ajan `accessibilityActions`/`onAccessibilityAction` ekledi (rotor eylemi).
Bu doğru ama bir yama; kalıcı çözüm görsel bir "daha fazla eylem"
affordance'ı olabilir. **D-3'te qa-engineer'ın bakması için not düşüldü**,
şimdi tasarım turu açmıyoruz.


---

## K-044 — 🔴 Giriş/kayıt + Google/Apple ile oturum açma: ONAY GEREKİYOR
- Tarih: 2026-09-17
- Durum: 🔴 **AÇIK — Mustafa'da.** Yapılmadı, yapılmayacak (karar gelene kadar).

### İstek
Mustafa: "Bir giriş ekranı, kayıt ekranı, google, apple ile girişleri halledelim."

### Neden duruyorum
Bu bir özellik eklemesi değil, **ürün temelinin tersine çevrilmesi.**
`CONTEXT.md` iki ayrı yerde (satır 37 ve 52) şunu söylüyor:

> "**Offline-first**, veri cihazda (SQLite). **Sunucu yok, hesap yok.**"

Ve `BACKLOG.md` **F-13**: "Offline-first yerel veritabanı, **sunucu yok, hesap yok**."

CLAUDE.md gereği dökümanla çelişen gereksinimde otomatik ilerlenmez.

### Bu değişikliğin gerçek bedeli
1. **Sunucu gerekir.** Google/Apple token'ını doğrulayacak bir arka uç olmadan
   "giriş" güvenlik tiyatrosudur. Şu an backend YOK (K-003) ve Faz 1'de
   `python-developer` bilerek devre dışı.
2. **Apple Developer Program ücretli ($99/yıl).** "Sign in with Apple" buna
   bağlı. Ayrıca App Store kuralı 4.8: üçüncü taraf girişi (Google) sunuyorsan
   Apple girişi sunmak **zorundasın**. Yani Google'ı eklemek Apple'ı mecbur kılar.
   → Ücretli bağımlılık = CLAUDE.md onay kapısı.
3. **Sürtünme, ürünün en kırılgan yerinde artar.** F-9 onboarding'i **en fazla
   3 soruyla** sınırlıyor; F-2 "her fazladan tık kullanıcı kaybı" diyor.
   Giriş duvarı, kullanıcının daha hiçbir değer görmeden karşılaştığı ilk
   ekran olur. Terk oranının en yüksek olduğu nokta tam orası.
4. **Marka konumlandırması buna dayanıyor.** "Hesap yok, sunucu yok" bir
   teknik detay değil, satış argümanı — finansal veride mahremiyet vaadi.
5. **Onaylı tasarım (K-035) etkilenir.** E-00/E-01/E-02/E-03 giriş akışı
   hesapsız tasarlandı ve onaylandı. Auth girerse bu akış yeniden tasarlanır.

### Seçenekler

**A — Hesap yok, onaylı giriş akışı kodlanır. (ÖNERİM)**
E-00 açılış + E-01/02/03 onboarding zaten tasarlandı ve onaylandı; "giriş
ekranı" ihtiyacını hesap olmadan karşılar. Sürtünme sıfır, ücret sıfır,
sunucu sıfır, marka tutarlı. Bugün kodlanabilir.

**B — Hesap opsiyonel, sonradan ve yalnız yedekleme için. (Faz 3)**
Uygulama hesapsız tam çalışır; hesap yalnız "verimi yedekle/başka cihaza taşı"
isteyen için. Giriş duvarı YOK. Ü-5 (kendi fiyat verimiz) zaten Faz 3'te
altyapı gerektiriyor — hesap da o zaman gelir, aynı altyapıyı paylaşır.

**C — Tam dönüş: hesap zorunlu, Google/Apple girişi, backend.**
Dürüst maliyet: backend kurulumu + Apple Developer $99/yıl + gizlilik
politikası + App Store "hesap silme" zorunluluğu + onboarding'in yeniden
tasarlanması + brandbook'un mahremiyet iddiasının geri çekilmesi.
Faz 1 MVP'yi haftalarca geciktirir.

### Önerim: A (şimdi) → B (Faz 3)
Gerekçe: Ürünün tezi "sürtünmesiz, mahrem, anında değer". Giriş duvarı bu
tezin üçünü birden zayıflatır ve karşılığında Faz 1'de hiçbir şey kazandırmaz —
senkronlanacak ikinci bir cihaz, korunacak bir sunucu verisi yok.
Hesap, **yedekleme ihtiyacı doğduğunda** anlamlı olur; o da Faz 3.

**Soru: A ile devam edeyim mi, yoksa C'yi mi istiyorsun?**
C dersen itiraz etmem, ama önce backend + ücret kalemini ayrıca onaylatırım.

## K-045 — "Halka yok" kuralı seçim kartlarına da uzanır (PM kararı)
- Tarih: 2026-09-17
- Durum: ✅ PM kararı, Mustafa onayı gerekmiyor (K-040'ın aynı gerekçesi:
  tasarım dili değişmiyor, var olan kural tutarlı uygulanıyor).

### Bulgu
D-1b turunda ajan, K-040 kapsamı dışında bir yer bildirdi: `stil.css`'de
`.secim-kart.secili` (onboarding/profilleme seçim kartları) hâlâ aynı
`inset 0 0 0 2px` halka desenini taşıyor. K-040 yalnız `.cip` ve
`.kat-sec-kutu`'yu adlandırmıştı.

### Karar
K-040'ın kuralı **bir bileşen listesi değil, bir ilkedir**: seçili durum
halkayla değil, **yüzey tonu + metin rengiyle** verilir. `.secim-kart` da
seçili-durum bileşenidir → halka kalkar.

### Uygulama
Ayrı tur açılmadı. **D-2c'ye devredildi** — o ekranlar (E-01/02/03 onboarding,
E-20 profilleme) zaten D-2c'de kodlanacak; `tokens.md §7.6` notu ve
`stil.css` düzeltmesi o turda birlikte yapılır.
⚠️ D-2c şu an **K-044 nedeniyle bloklu**; bu madde onunla birlikte bekliyor.

## K-046 — `metinler.md` aynı ekranı İKİ KEZ tanımlıyor (PM kararı)
- Tarih: 2026-09-17
- Durum: ✅ PM kararı. Kod doğru, **doküman hatalı** → düzeltmesi D-2c'ye devredildi.

### Bulgu
D-2b ajanı "prototip ile `metinler.md` çelişiyor, prototipi esas aldım" diye
bildirdi. Denetledim: çelişki prototiple değil, **`metinler.md`'nin kendi içinde.**
`docs/content/metinler.md` E-15 (Kategori detayı) ekranını **iki ayrı bölümde**
tanımlıyor:
- `§7` satır 279 → `kategori.limit_var` = "Aylık limit {tutar} · kalan {kalan}"
- `§22.1` satır 628 → `kategori.limit_ust` = "Aylık limit {tutar}"

Aynı elemanın iki farklı metni, iki farklı anahtar adıyla.

### Karar
Ajanın seçimi **DOĞRU**: `§22.1`/`limit_ust` geçerlidir — prototip (K-035 ile
onaylı) bu formu gösteriyor ve kodda uygulanan bu. `§7` eski bir taslak kalıntısı.

### Neden önemli
Bu, K-040/K-042 ile aynı aileden bir tuzak: **bir doküman kendi içinde
çelişiyorsa sonraki ajan yanlış yarısını seçebilir.** `tokens.md` için "tek
otorite" kuralı konmuştu; aynı disiplin `metinler.md` için de gerekiyor.

### Uygulama (D-2c'de, ayrı tur açılmadı)
`metinler.md §7`'deki E-15 bloğu kaldırılır veya "ARŞİV — §22.1 geçerlidir"
diye işaretlenir. Tüm dosya aynı gözle taranır: **başka çift-tanımlı ekran
var mı?** Varsa hangi bölümün geçerli olduğu tek tek işaretlenir.

## K-047 — Giriş/Kayıt: TASARIM açıldı, auth ALTYAPISI hâlâ açık (K-044 devamı)
- Tarih: 2026-09-17 · Durum: 🟡 Kısmi karar (Mustafa direktifi) + 1 açık kalem

Mustafa: "Login ve Kaydolma ekranlarını tasarımcıya yaptır."
→ **Tasarım yapılır** (E-22 Giriş, E-23 Kayıt). Tasarımın maliyeti yok, riski yok.

Ama K-044'teki iki kalem KAPANMADI ve tasarım onları varsaymayacak:
1. **Google/Apple ile oturum** = backend + Apple Developer $99/yıl (ücretli
   bağımlılık, CLAUDE.md onay kapısı). Bu onay gelmedi.
2. Hesap zorunluysa "sunucu yok, hesap yok" mahremiyet vaadi geri çekilir.

**PM kararı (tasarımı bloke etmemek için):** ekranlar şöyle tasarlanır —
- E-22/E-23 e-posta + şifre alanlarıyla tasarlanır (görsel olarak tam).
- Her iki ekranda **"Hesapsız devam et"** çıkışı bulunur → onboarding'e gider.
  Giriş duvarı YOK; sürtünme kuralı (F-2/F-9) korunur.
- Sosyal giriş satırı (Google/Apple) **ayrı bir DURUM varyantı** olarak çizilir,
  varsayılan akışta kapalı. Onay gelirse yerine oturur, gelmezse çizim çöp olmaz.
- Faz 1'de kodlanacak davranış: hesap **yerel** (cihazda), sunucuya hiçbir şey
  gitmez. Gerçek auth = backend onayı gelince.

Açık kalan tek soru: **Google/Apple + backend'e onay veriyor musun?**
Hayır/sessizlik → Faz 1 yerel hesapla gider, kimse beklemez.

## K-048 — Oyunlaştırma + Seri (streak) MVP'ye ALINDI · kural seti
- Tarih: 2026-09-17 · Durum: ✅ Karar (Mustafa direktifi + PM kural seti)

Mustafa: "Oyunlaştırma istiyorum. Streak mantığı olmalı." + "Streak'te belli
milestone'lar tamamlandığında ekranda bir animasyon belirmesi lazım."

Bu, `CONTEXT.md`'deki "MVP'de oyunlaştırma YOK" satırını **geçersiz kılar.**
CONTEXT.md güncellendi. Kapsam etkisi: Faz 1 MVP'ye +1 alt sistem.

**Seri kuralları (PM kararı — tasarım ve kod bunlara uyar):**
- **Tanım:** Seri = günlük limitin ALTINDA kapatılan üst üste gün sayısı.
- **Hile kapısı:** Bir gün seriye sayılır ancak (a) o gün en az bir harcama
  kaydı varsa YA DA (b) kullanıcı günü **"Harcamasız gün"** olarak işaretlediyse.
  Gerekçe: hiç kayıt girmeyen kullanıcı ₺0 ile seri kazanmamalı — bu ürünün
  tezini (kayıt alışkanlığı) çürütür. Kalori uygulamalarının "günü kapat"
  mekaniğinin doğru uyarlaması budur.
- **Limitsiz mod:** günlük limit yoksa seri işlemez; kullanıcıya "Seri için
  günlük limit gerekir" denir (F-1'e bağlanır).
- **Milestone:** 3 · 7 · 14 · 30 · 60 · 100 · 180 · 365 gün. Kutlama yalnız o
  gün, bir kez, dokunmayla atlanabilir, ≤1.2 sn. Emoji/konfeti klişesi YOK
  (K-004 + anti-pattern listesi) — kutlama clay diliyle yapılır.
- **Kırılma:** suçlayıcı dil yok. "En uzun seri" saklanır ve gösterilir, böylece
  kırılma yıkıcı olmaz. Faz 1'de **seri dondurma/kalkan YOK** (karmaşıklık).
- **Rozet/puan/seviye/lig YOK.** Oyunlaştırma = seri + milestone kutlaması +
  seri yüzeyi. Puan ekonomisi bütçe uygulamasında sahte motivasyon üretir.

## K-049 — Sekme 1 "Günlük" + tarih sayfalama (E-10 revizyonu)
- Tarih: 2026-09-17 · Durum: ✅ Karar (Mustafa direktifi)

- Alt sekme çubuğunda **en sol sekme = "Günlük"** (E-10). Sekme sayısı 3'te
  kalır: Günlük · Kayıtlar · Özet. Etiket "Bugün" → "Günlük" olur çünkü ekran
  artık yalnız bugünü değil, herhangi bir günü gösterir.
- Ekran yatay **sayfalanabilir**: sola kaydır → bir önceki gün.
  **Yön — NİHAİ (K-055):** bugün **en sağdaki** sayfadır, geçmiş günler **sola**
  doğru dizilir (takvim konvansiyonu). Geçmişe gitmek için parmak **sağa**
  kaydırılır. Mustafa 2026-09-17'de "çevir" dedi → konvansiyon kazandı.
- Başlık: bugün → **"Bugün"**, bir önceki → **"Dün"**, daha öncesi →
  **"17/09 Çarşamba"** (gün/ay + gün ismi).
- **Sınırlar:** geleceğe gidilmez (bugün en sağdaki sayfa); geriye ilk kayıt
  gününden (yoksa kurulum gününden) öncesine gidilmez — "başlangıcından itibaren".
- Geçmiş gün sayfasında o günün limiti/toplamı görünür ve **o güne harcama
  eklenebilir** (geç kayıt sorununu çözer).

## K-050 — "Kalori uygulaması mantığı" uyarlama kuralları + ürün arama
- Tarih: 2026-09-17 · Durum: ✅ Karar (Mustafa direktifi + PM yasak listesi)

Mustafa: "bütçe takip uygulaması ama bir kalori takip uygulaması ile aynı
mantıkta olacak... Uyarlama yapmayı unutmasın, sonra saçma sapan kalori
hesapları falan görmeyelim." + harcama eklemede ürün arama, fiyat girme,
istenirse kategori dropdown.

**Alınan mekanikler:** günlük hedefe karşı ilerleme · gün gün loglama ·
seri/milestone · "öğe ara → ekle" hızlı giriş · günü kapatma.

**YASAKLAR (uyarlama hataları):**
- UI'ın hiçbir yerinde kcal/besin/porsiyon/makro/barkod analojisi veya
  "kalori" kelimesi geçmez.
- Ürün kataloğu **fiyat GÖSTERMEZ.** Fiyat kullanıcıdan alınır; yanlış/eski
  fiyat göstermek güveni tek seferde bitirir (K-037'nin sebebi de bu).
  Doğru uyarlama: **"geçen sefer ₺45"** — kullanıcının kendi son fiyatı.
- Ürün seçmek **zorunlu değildir.** Kategori + tutar ile 2 adımda ekleme her
  zaman açık kalır (F-2 sürtünme kuralı bağlayıcı).
- Ürün kataloğu yerel ve sabit (~60-80 yaygın kalem), her kalem bir kategoriye
  bağlı → ürün seçilince kategori otomatik dolar, dropdown'la değiştirilebilir.
- Sunucu/servis yok; katalog uygulamayla gelir.

## K-051 — Kalori-app referans görselleri: uyarlama haritası (bağlayıcı)
- Tarih: 2026-09-17 · Durum: ✅ Karar (PM, Mustafa'nın referansına dayanarak)

Mustafa `/Users/mustafa/Documents/template` altındaki 9 ekran görüntüsünü referans
verdi ("bu şekilde benzetilebilir"). Repoya kalıcı olarak kopyalandı:
`docs/design/referans-gorseller/kalori-app-referans/` (01-09).

**Kural (CLAUDE.md):** bilgi mimarisi ve mekanik ALINIR, görsel stil ALINMAZ.
Referans Material/flat + emoji; Trinkow claymorphism, emoji yasak (K-004).

**ALINAN mekanikler**
- Tarih sol üstte + sağ üstte seri göstergesi ve takvim ikonu.
- Öğün grupları (Kahvaltı/Öğle/Akşam + halka + "+") → **kategori grupları**:
  kategori bazında günlük toplam, limite göre ilerleme, hızlı "+" ekleme.
  F-4 zihinsel muhasebe ile birebir örtüşüyor; en güçlü uyarlama bu.
- Makro çubukları → en çok harcanan 3 kategori + limit çubuğu.
- Seri ekranı: büyük seri sayısı, 7 günlük şerit, "en uzun seri".
- Ay takvimi → **yeni E-24 Gün seçici** (gün durumları: limit altı / aşıldı /
  kayıt yok; geleceğe ve ilk kayıt öncesine gidilemez; alt istatistikler
  Aktif gün · Limit altı gün · Tasarruf ₺).

**BİLİNÇLİ ALINMAYANLAR**
- **Elmas/puan sayacı (1030)** — puan ekonomisi K-048 ile yasak.
- **"Yakılan" (kalori) karşılığı İCAT EDİLMEZ.** Gösterge Harcanan/Kalan(/Limit).
  Mustafa'nın "saçma sapan kalori hesapları görmeyelim" uyarısının hedefi budur.
- **Seri Dondurma hakkı** — Faz 1'de yok (K-048). Mustafa isterse tek satırlık ek.
- **Başarını Paylaş / Arkadaşlar** — sosyal katman sunucu gerektirir, Faz 1'de yok.
- **Profil sekmesi ve Pro/paywall ekranları** — sekme sayısı 3'te kalıyor (K-049)
  ve monetizasyon için ürün kararı YOK. 🟡 Mustafa isterse ayrı iş kalemi.
- Mor gradyan hero, emoji alev, konfeti, siyah pill CTA — marka dili dışı.

## K-052 — Google + Apple ile giriş ONAYLANDI (K-044/K-047 kapandı)
- Tarih: 2026-09-17 · Durum: ✅ Mustafa onayı: "Google ile Apple ile giriş olacak tabi ki."

K-044 ve K-047 bununla **kapanıyor.** Ama onayın kapsamını daraltarak yazıyorum,
çünkü "giriş var" demek "tüm veri sunucuya gidiyor" demek değil:

**Mimari kural (PM kararı):**
- **Harcama verisi cihazda kalır** (`expo-sqlite`). Faz 1'de sunucuya harcama
  senkronu YOK. Hesap yalnız **kimlik** içindir; yedekleme/senkron Faz 3 (K-047-B).
  Gerekçe: finansal veriyi sunucuya taşımak gizlilik politikası, veri saklama,
  ihlal sorumluluğu ve App Store hesap-silme zorunluluğu getirir. Kimlik için
  bunların hiçbiri gerekmiyor. Ürünün mahremiyet vaadi böylece ayakta kalır.
- **Giriş duvarı YOK.** "Hesapsız devam et" kalıyor (F-2/F-9 sürtünme kuralı).
  Hesap, kullanıcı isterse açılır; açmayan kullanıcı uygulamayı tam kullanır.
- Kimlik doğrulama için yönetilen servis kullanılır (**Supabase Auth** önerim —
  ücretsiz katman, kendi sunucumuzu yönetmiyoruz, Faz 3 yedekleme yolunu da
  aynı altyapı açar). Firebase alternatif. Ücretsiz katman aşılırsa tekrar sorulur.
- `expo-apple-authentication` + Google sign-in paketleri eklenir.

**Bedeller (kayda geçiyor, sürpriz olmasın):**
- **Apple Developer Program $99/yıl** — zaten App Store'a çıkmak için kaçınılmaz,
  auth'a özel ek bir kalem değil. Onaylandı kabul ediyorum.
- App Store kuralı 4.8: üçüncü taraf girişi sunuyorsan Apple girişi **zorunlu** →
  ikisi birlikte yapılıyor, sorun yok.
- **Gizlilik politikası + kullanım şartları metni gerekir** (App Store şartı).
- **brandbook + CONTEXT.md'deki "hesap yok" ifadesi revize edilmeli** →
  yeni ifade: "harcama verin cihazında kalır, hesap yalnız kimlik için".
  Bu bir marka mesajı değişikliği → `brand-strategist`'e kısa görev (B-1).

## K-053 — Onboarding profilleme genişliyor · F-9 "3 soru" çelişkisinin çözümü
- Tarih: 2026-09-17 · Durum: ✅ Karar (Mustafa direktifi + PM çözümü)

Mustafa: kullanıcıyı ilk girişte tanıyalım — kahve/sigara/alkol alışkanlıkları ve
sıklıkları, dışarıda yemek, aylık gelir, yatırım niyeti; sonra kullanıcıya en uygun
**para yönetim modeli** verilsin (zorunlu harcamalar/kira/fatura, sosyal harcamalar,
maaşın yüzde kaçı birikim).

**🔴 Çelişki:** `BACKLOG.md` F-9 ve rapor, onboarding'i **"en fazla 3 soru"** ile
sınırlıyor; F-2 "her fazladan tık kullanıcı kaybı" diyor. 12+ soruluk anket bu
kuralı ihlal eder. Sessizce çözmüyorum, çözümü öneriyorum:

**Çözüm — iki katmanlı onboarding (F-9 korunur, F-12 genişler):**
- **Katman 1 · Zorunlu, 3 soru** (F-9/F-10/F-11 aynen): (1) ana niyet
  Takip/Tasarruf/Borçtan çıkış · (2) aylık net gelir (atlanabilir) · (3) maaş günü.
  Bu üç cevaptan sonra uygulama **çalışır durumda** — kullanıcı değeri hemen görür.
- **Katman 2 · "Seni tanıyalım", ATLANABİLİR, her an yarıda bırakılabilir** (~8 kart,
  ilerleme göstergeli, ayarlardan sonra da tamamlanabilir — "aşamalı profilleme" F-12):
  - Sabit giderler: kira/aidat · faturalar · ulaşım/yakıt · kredi-taksit toplamı
  - Alışkanlıklar: **sıklık + kullanıcının kendi fiyatı** → kahve, sigara, alkol,
    dışarıda yemek, abonelikler
  - Yatırım: yapıyor musun / yapmayı düşünüyor musun
  - Birikim hedefi: kaydırıcı (%)
- **Çıktı ekranı "Planın hazır" (yeni ekran):**
  - Zorunlu · Sosyal/keyfi · Birikim(+yatırım payı) dağılımı, ₺ ve % olarak
  - **Günlük limit buradan türetilir:** sosyal/keyfi pay ÷ maaş döngüsünde kalan gün.
    Böylece anket F-1'e bağlanır, havada kalmaz.
  - **"Alışkanlık maliyeti" kartı:** kullanıcının girdiği sıklık × kendi fiyatı →
    "kahve: ayda ₺X". Ürünün "ödeme acısı" tezini doğrudan besleyen en güçlü kart.
  - Yüzdeler kaydırıcıyla değiştirilebilir, toplam %100 kilidi. Gelir girilmediyse
    yüzde modeli kapanır, limit elle girilir (model zarif şekilde küçülür).
  - **"Nasıl hesaplandı?"** açıklaması zorunlu — kara kutu çıktı güven kaybettirir.

**YASAKLAR:**
- **Yatırım tavsiyesi YOK.** Enstrüman adı, getiri tahmini, "şuna yatır" yok.
  Türkiye'de yatırım tavsiyesi SPK düzenlemesine tabidir; yapabileceğimiz tek şey
  birikimin bir kısmını "yatırım payı" olarak **etiketlemek**. Bu sınır aşılmayacak.
- **Fiyat uydurma YOK** (K-050). Kahvenin/sigaranın fiyatını biz varsaymayız,
  kullanıcı girer.
- Gelir sorusu **atlanabilir** olmak zorunda; zorunlu yapmak en yüksek terk noktası.
- Anket sonunda kullanıcıya **kilo/kalori benzeri sahte skor** üretilmez (K-050).

## K-054 — Tur 1 delta bulgularının karara bağlanması (PM)
- Tarih: 2026-09-17 · Durum: ✅ Karar · Kaynak: `docs/design/delta-v4.md` 🔴 7 madde

1. **K-049 yön tutarsızlığı** → Mustafa'ya soruldu, **K-055 ile çözüldü**
   (aşağıda). Bu maddedeki ilk yorumum (bugün en solda) geçersizdir.
2. **brandbook §2.3 "seri Faz 2'de"** → K-048 ile geçersiz. `brand-strategist`
   görevine (B-1) eklendi. Tasarımcının kullandığı ton satırları geçerli kalır.
3. **`bilesen-envanteri.md` §6 "takvim ızgarası / rozet-başarım Faz 1'de
   üretilmez"** → K-048/K-051 bu maddeyi **kısmen geçersiz kılar**: takvim
   ızgarası ve `StreakDayGrid` artık MVP'de (seri ve E-24 gün seçici bunu
   gerektiriyor). **Rozet/başarım hâlâ üretilmez.** T-5 birleştirmesinde §6
   bu ayrımla yeniden yazılacak.
4. **Buton kelime sınırı** → kabul: butonda **"Harcamasız işaretle"**, tam cümle
   kart gövdesinde.
5. **Limitsiz modda tek nötr "Limit belirle" kapısı** → kabul. Gerekçe: seri
   limite bağlı (K-048); limit yoksa kullanıcıya çıkış yolu gösterilmezse özellik
   sessizce ölür. v3'ün "limitsiz modda limit çağrısı yok" kararı bu tek nötr
   kapıyla sınırlı olarak gevşetilir — ısrarlı/ikna edici dil YOK.
6. **Paralel ajanın token ihlalleri** → düzeltilecek (T-4 öncesi):
   `.imza-kare{border-radius:4px}` tokens §4'e aykırı ·
   `.gun-kutu.pasif{box-shadow:none}` tokens §6'ya aykırı (pasif = renk +
   clay.sunken). **`.gun-kutu.secili` halkası → HALKA YOK** (K-045'in doğal
   uzantısı): seçili gün dolgu/kil kabartma ile belirtilir, halka ile değil.
7. **Başlıktaki takvim düğmesi KALIR** (E-24'e giriş, K-051 ile ben ekledim) ve
   **seri çipinde birim geri konur: "Seri 12 gün"** (ölçüm 338 ≤ 358 px sığıyor).
   Başlıkta 3 dokunma hedefi kabul: tarih · seri çipi · takvim. Her biri ≥44pt
   ve çakışmasız olacak.

## K-055 — Gün sayfalamasının yönü: takvim konvansiyonu (NİHAİ)
- Tarih: 2026-09-17 · Durum: ✅ Mustafa kararı: "çevir"

**Bugün en sağdaki sayfadır; geçmiş günler sola doğru dizilir.** Geçmişe gitmek
için parmak **sağa** kaydırılır; sola kaydırma bugüne doğru ilerletir ve bugünde
durur (gelecek yok). Sol uç sınırı = ilk kayıt günü (K-049).

Gerekçe: Mustafa'nın ilk tarifi ("sola kaydırınca dün") jest yönüydü, ama takvim
konvansiyonunda geçmiş solda durur; ikisi çakıştığında **konvansiyon kazanır.**
Sorulduğunda "çevir" dedi.

**Tasarım etkisi:** prototip-v4'te oklar, `disabled` uçları ve kaydırma ipucu
metni bu yöne göre çevrilecek (T-2 brief'ine eklendi). Kod etkisi: henüz
kodlanmadı, maliyet yok.

## K-056 — Kategoriler kartında zaman ölçeği + "Tasarruf" tanımı (PM)
- Tarih: 2026-09-17 · Durum: ✅ Karar (tur 1 çıktısının revizyonu)

1. Günlük ekranındaki **Kategoriler kartı** referanstaki "öğün grupları + makro
   çubukları" birleşiminden geldi ama satırda **bugünün tutarı** ile **aylık limit
   çubuğu** yan yana duruyordu → iki zaman ölçeği aynı satırda. Düzeltme:
   **çubuk aylık/aylık** (ayın kategori toplamı ÷ aylık kategori limiti),
   **bugünün tutarı ikincil satıra** iner. Uydurma "günlük kategori limiti" YOK (K-050).
   Gerekçe: iki ölçeği yazıyla ayırmak kavrama yükünü çözmüyor; ölçeği eşitlemek çözüyor.
2. E-24'te gösterilen **"Tasarruf"** metriğinin tanımı hiçbir dökümanda yazılı
   değildi → tasarımcı formülü delta'ya yazacak, PM `metinler.md`'ye işleyecek.
   Yazılı tanımı olmayan sayı, kodda iki farklı şekilde hesaplanır (K-040 dersi).

## K-057 — T-2 (giriş/kayıt) sonrası 8 PM kararı
- Tarih: 2026-09-17 · Durum: ✅ Karar · Kaynak: `delta-v4.md` → `# T-2` 🔴 bölümü

1. **"Mimari anlatan metin yasak" ↔ K-052 mahremiyet cümlesi** → İSTİSNA VERİLDİ,
   ama biçim kilitli: **kullanıcı faydası dili** izinli ("Harcamaların telefonunda
   kalır"), **mimari sözcükleri yasak** (SQLite, sunucu, senkron, şifreleme, token).
   Bu istisna B-1 ile brandbook §2.8'e yazılacak.
2. **`varliklar.md` → "üçüncü taraf marka varlıkları" bölümü** şart: Google/Apple
   logoları, izinli renk/biçim kısıtları, hangi dosyada durdukları. T-5'te yazılacak.
   Yoksa sonraki denetim bunları palet ihlali okur.
3. **Apple girişi Android'de:** GÖSTERİLMEZ. App Store 4.8 yalnız iOS'u bağlar;
   Android'de e-posta + Google yeter. Düğme platforma göre koşullu.
4. **Hesap silme Supabase'de Edge Function ister** → kabul; iş kalemi F-19f'e
   yazıldı. "Kendi sunucumuzu yönetmiyoruz" ifadesi geçerli kalır (yönetilen
   serverless ≠ sunucu işletmek), ama App Store hesap-silme şartı bu fonksiyon
   olmadan karşılanamaz → yayın öncesi zorunlu.
5. **Buton kelime sınırı istisnası:** üçüncü taraf düğmeleri ("Google ile devam et",
   "Apple ile devam et") sınırdan muaf — etiket sahibinin kılavuzuna tabi.
6. **"giriş" sözcüğü çakışması** → istisna vermek yerine sözcük değişti:
   kimlik doğrulama **"Oturum aç"**, veri girme "giriş" (harcama girişi) olarak
   kalır. E-22 adı "Oturum aç" olur. Gerekçe: aynı sözcüğün iki anlamı, istisna
   satırıyla değil sözcüğü ayırarak çözülür. T-3'te metin güncellemesi yapılacak.
7. **Gizlilik politikası + kullanım şartları metinleri YOK** → 🟡 gerçek boşluk,
   yayın bloklayıcısı. Tasarımda bağlantılar yer tutucu kalır. Bu metinleri
   tasarımcı yazmaz; ajansta hukuk ajanı yok. **Mustafa'ya soru:** (A) sade dilde
   taslağı biz yazalım, sen gözden geçir · (B) hazır şablon/servis · (C) avukat.
   Önerim A — Supabase'in kimlik verisi işlediğini dürüstçe yazan kısa bir metin,
   yayın öncesi bir hukukçuya okutulur.
8. **`01-gunluk` A2'de kaydırma kesmesi liste satırının ortasında** → prototip
   kozmetiği: kesme satır ARASINA hizalanır. Gerçek uygulamada liste kaydırılabilir,
   içerik kaybı yok. Yarım satır bırakmak "devamı var" sinyali olarak izinli,
   ama kesilen satırda **tutar yarısı görünmeyecek** (yanlış okunur).

**Kabul edilen tartışmalı kararlar (itirazım yok):** "Hesap oluştur" adlandırması ·
şifre gücü göstergesi yok (tek kural + onay satırı) · çıkışta diyalog yok, hesap
silmede var · Hesap bölümü Veri'nin üstünde · "ya da" ayracında çizgi yok ·
Apple düğmesinin RN'de `AppleAuthenticationButton` ile çizilmesi.

## K-058 — Oturum açma platform kuralı + Apple hesabının Android'de kurtarılması
- Tarih: 2026-09-17 · Durum: ✅ Karar (K-057/3'ün uygulanmış hâli, tasarım bitti)

- **iOS:** Apple + Google + e-posta/şifre. **Android:** Google + e-posta/şifre
  (Apple düğmesi yok — App Store kuralı 4.8 yalnız iOS'u bağlar).
  Tek parametreyle iki hâl üretiliyor; Android'de sosyal küme 120→56pt'ye iniyor,
  E-23 tek ekrana sığıyor. RN'de `Platform.select`; Apple paketi Android'e bağlanmaz.
- **Kurtarma yolu (önemli):** iOS'ta Apple ile hesap açan kullanıcı Android'de
  kilitli kalmaz. Apple'ın verdiği e-posta (gerekirse `privaterelay`) hesabın
  kimliğidir → **"Şifremi unuttum"** ile şifre belirlenir, e-posta/şifre ile girilir.
  Supabase'de tek kullanıcı kaydı kalır. **Yeni ekran gerekmedi.**

## K-059 — T-3 (profilleme + plan) sonrası 7 PM kararı
- Tarih: 2026-09-18 · Durum: ✅ Karar · Kaynak: `delta-v4.md` → `# T-3` 🔴 bölümü

1. **`metinler.md` §18 "yüzde Faz 1'de kullanılmaz" ↔ K-053** → **K-053 kazanır.**
   Mustafa açıkça yüzde istedi ("maaşın yüzde kaçı birikim"). §18 T-5'te güncellenecek.
2. **§2'deki E-02/E-03 metin anahtarları geçersiz** → T-5 temizliğine alındı.
3. **v3'ün "kategori limiti tohumlama" sorusu düştü** → **soru olarak GERİ EKLENMEYECEK.**
   Yerine: kategori limitleri **plan ekranından otomatik tohumlanır** (sabit giderler +
   alışkanlık cevapları ilgili kategorilere düşer), kullanıcı E-17 Limitler'den düzeltir.
   Gerekçe: F-4 karşılanıyor ve Katman 2'ye 9. kart eklenmiyor (sürtünme).
4. **`success #16A34A` birikim segmenti** → ONAYLANDI. Anlamsal olarak tutarlı
   (birikim = olumlu sonuç). T-5'te `tokens.md` §1.3'e **"grafik/segment bağlamı"**
   olarak yazılacak; design-reviewer anlam tutarlılığını ayrıca denetler.
5. **E-10 varsayılanı limitsiz** → kabul, ama **tek boşlukla:** limitsiz kipte seri
   çalışmıyor (K-048), dolayısıyla Katman 2'yi atlayan kullanıcı seriyi hiç görmez.
   Düzeltme: **Katman 1'de gelir girildiyse**, varsayılan dağılımla (zorunlu/sosyal/
   birikim) bir **günlük limit ÖNERİSİ** hesaplanır ve kullanıcı tek dokunuşla onaylar.
   Şartlar: açıkça "öneri" etiketi + "Nasıl hesaplandı?" + tek dokunuşla değiştirilebilir.
   Gelir girilmediyse limitsiz kip aynen kalır. Bu sayı **uydurma değildir** —
   belgelenmiş bir varsayılan dağılımdır ve kullanıcı onayından geçer.
6. **"Kalan gün" tanımı** hiçbir belgede yoktu → tasarımcının yazdığı formül kabul,
   T-5'te `metinler.md`/`tokens.md`'ye geçecek.
7. **Gizlilik/kullanım şartları metni** → K-057/7 ile Mustafa'da, tasarım tarafında
   yer tutucu kalıyor. Yayın bloklayıcısı olarak izleniyor.

**Kabul edilen tartışmalı kararlar:** tek kaydırıcı (zorunlu pay olgu, fark sosyal
paydan iner) · Katman 1 sonunda limit uydurulmaması ("Henüz yok") · negatif kalanın
`warning` ile ve "1.400 ₺ eksik" biçiminde gösterilmesi + üç çıkış yolu ·
A2 kesme hizasının içerikle çözülmesi (bu arada başlık/liste tutar tutarsızlığı da kapandı).

## K-060 — T-4 (ürün arama + limit önerisi) sonrası 5 PM kararı
- Tarih: 2026-09-18 · Durum: ✅ Karar

1. **K-033/3 gömülü tütün fiyat listesi → RESMEN KAPATILDI.** K-050 kazanır:
   uygulama hiçbir ürünün fiyatını bilmez/göstermez. Tasarım listeyi zaten kaldırdı.
   **K-037** (Mustafa'dan 20-30 tütün markası fiyatı) böylece Faz 1 için
   **gereksizleşti** — Faz 2.5'te "kendi fiyat verimiz" konusu açılırsa fiyat
   gösterme kararı sıfırdan alınacak. Mustafa'nın bu iş kalemi düştü.
2. **Varsayılan dağılım %50/%30/%20 → ONAYLANDI.** Yerleşik bütçe kuralıdır,
   uydurma değildir. Şartlar: ekranda "öneri" pulu · kaynağın kullanıcının kendi
   cevabı OLMADIĞI açıkça yazılı · tek dokunuşla değiştirilebilir · reddedilebilir.
   Sabit giderler biliniyorsa onlar **olgu** olarak kullanılır, yüzde yalnız
   bilinmeyen kısma uygulanır.
3. **Öneriyi kabul eden kullanıcıda kategori limiti oluşmaması** → kabul.
   Kategori limitleri opsiyoneldir (F-4); plan yapılırsa otomatik tohumlanır
   (K-059/3), yapılmazsa kullanıcı E-17'den kurar. Ek tasarım gerekmiyor.
4. "Kalan gün" tanımı → T-5'te `tokens.md`/`metinler.md`'ye taşınacak (K-059/6 ile aynı).
5. `metinler.md` §18 "yüzde kullanılmaz" → K-059/1 ile zaten geçersiz, T-5 temizliğinde.

## K-061 — design-reviewer REVİZE kararı (v4) ve PM hükümleri
- Tarih: 2026-09-18 · Durum: 🔄 Düzeltme turu verildi
- Rapor: `docs/design/denetim-raporu-v4.md` · Karar: **REVİZE — 3 bloklayıcı**

1. **B-1 kontrast** → düzeltilecek: gün kutusundan `grad-action` kaldırılır, düz
   `primary-deep` kalır (5.37 ✅). v4'ün en çok tekrarlanan elemanı olduğu için
   en yüksek öncelik. Ders: **delta'da ilan edilen kontrast değeri CSS'te
   doğrulanmamış** — ilan ≠ uygulama.
2. **B-2 üç farklı "seçili" dili** → `.secim-kart.secili` halkası kaldırılır
   (K-045/K-054-6 çizgisinin doğal sonucu). Kalan iki dil tokens'a yazılır.
3. **B-3 gelir sorusu çelişkisi** → **E-20'nin gelir sorusu EMEKLİYE AYRILIR.**
   Gerekçe: Katman 1 geliri tam tutar olarak alıyor ve plan formülleri tam tutar
   istiyor; aynı olguyu iki farklı biçimde sormak veri tutarsızlığı üretir.
   Eksik profili tamamlama yolu zaten "Ayarlar > Plan ve profil" (K-053/F-12).
   Yerine E-25'in cevaplanmamış kartlarından biri gösterilir.
4. **"Bir öğün kaç lira" → "Bir yemek kaç lira"** (K-051: kalori uygulamasının
   bilgi mimarisi izini taşımayacağız). Delta'daki yanlış öz-denetim satırı düzeltilir.
5. `denetim.py`'den **radius "4" izni kaldırılır**; ayrıca betiğe **`stil.css`
   hex/radius taraması** eklenir — "0 bulgu" iddiası paleti kapsamıyordu.
6. `tokens.md` §12'ye **"işletim sistemi çizimleri palet/ölçek dışıdır"** istisnası
   yazılır (sistem klavyesi, durum çubuğu, home indicator) — T-5.
7. Devralınan `<title>` "prototip v3" başlıkları v4'e çekilir.
   ⏸️ Yinelenen `fonts/fonts/` dizininin **silinmesi Mustafa onayına bağlı**
   (geri dönüşsüz silme kuralı). Onay gelene kadar duruyor, zararsız.

## K-062 — Gradyan zeminde metin kuralı (birincil düğme dahil)
- Tarih: 2026-09-18 · Durum: ✅ Karar (PM)

Düzeltme turunda `.btn-primary` için aynı fizik bulundu: beyaz metin `grad-action`
üstünde ortalanınca üst kenarda **4.25 ❌**, alt kenarda 4.61. `tokens.md` §1.8
"metin alt-koyu yarıya hizalanır" diyor ama CSS metni ortalıyor. Bu, uygulamanın
en çok görünen düğmesi.

**Kural (genelleştirildi):** `grad-action` **metin TAŞIMAYAN** yüzeylerde kullanılır
(kahraman gösterge, dekoratif dolgu). **Metin taşıyan** her yüzeyde düz
`primary-deep` + clay gölge kullanılır (beyazla 5.37 ✅).

Gerekçe: B-1'de gün kutusu için verilen kararın aynısı; iki farklı kural tutmak
yerine tek kural. Metni düğmenin ortasından kaydırmak (tokens §1.8'in harfi)
optik olarak yanlış görünür ve her düğme boyutunda yeniden ayar ister.
Gradyanın kendisini koyulaştırmak ise **onaylı görsel kimliği ve halihazırda
kodlanmış ekranları** etkiler — kapsamı en dar çözüm bu.

**Etki:** düğmelerin dolgusu düz renge döner, derinlik gölgeden gelir. Kodda
`Button.tsx` dolgusu değişir (küçük). `tokens.md` §1.8 bu kuralla yeniden yazılır.
Mustafa görsel onayda bunu görecek.

## K-063 — 🔵 AŞAMA 2 → 3 GEÇİŞİ: Mustafa'nın görsel onayı bekleniyor
- Tarih: 2026-09-18 · Durum: 🔵 **AÇIK — Mustafa'da**

`design-reviewer` **PASS** verdi (`docs/design/denetim-raporu-v4.md` → DELTA 2. tur).
3/3 bloklayıcı + 5/5 önemli madde kapandı, anti-pattern 20/20 temiz, doküman↔prototip
senkronu doğrulandı. **PASS tek başına yeterli değildir** (STAGE.md Aşama 2 çıkış
kriteri): kodlamaya dönmek için Mustafa'nın görsel onayı şart.

**Açılacak dosya:** `projects/trinkow/docs/design/prototip-v4/index.html`
(18 ekran · 122 yüzey · fontlar gömülü, internet gerekmez)

**Mustafa'nın özellikle bakması istenen iki yüzey:**
1. **Seçili seçim kartı** (E-03/E-17/E-20) — halka kaldırıldı, seçim yalnız derinlik +
   ikon kabarmasıyla anlatılıyor, zemin sayfa zeminine çok yakın. 1:1 ölçekte
   okunuyor mu? Okunmuyorsa çözüm `surface` zemin — **halka değil** (tokens §5.4).
2. **Birincil düğme** — gradyan kalktı, düz koyu mavi + gölge (K-062, erişilebilirlik
   zorunluluğu). Uygulamanın en çok görünen yüzeyinde gözle görülür değişiklik.

Onay gelirse: Aşama 3 (Geliştirme) yeniden açılır, D-2c + D-2d kodlanır.

## K-063 · GÜNCELLEME — Mustafa onayı verildi, Aşama 3 yeniden açıldı
- Tarih: 2026-09-18 · Durum: ✅ **ONAYLANDI**

Mustafa: "şimdilik frontend olarak sen bunu kodla. bir an önce ürüne ulaşalım.
Sonrasında eklemeler yaparız."
→ Aşama 2 **kapandı** (design-reviewer PASS + Mustafa onayı). Aşama 3 açıldı.

**Yorum notu:** Mustafa "tasarımı onaylıyorum" cümlesini kurmadı, "kodla" dedi;
pratikte geçiş onayıdır ve öyle işlendi. Denetçinin 1:1 bakılmasını istediği iki
yüzey (halkasız seçim kartı · düz dolgulu birincil düğme) **kodda simülatörde
görüldüğünde** tekrar değerlendirilecek — tasarımda değil, üründe.

**Kodlama sırası (hız önceliği — Mustafa "bir an önce ürüne ulaşalım" dedi):**
- **D-2d-1** Günlük sekmesi + tarih sayfalama + seri sistemi + gün seçici
  → yeni bağımlılık YOK, çekirdek döngü, en yüksek değer. ÖNCE BU.
- **D-2d-2** E-11 ürün arama + yerel katalog (80 kalem)
- **D-2d-3** Profilleme Katman 1+2 + "Planın hazır" + limit önerisi + kategori tohumlama
- **D-2c** Oturum aç / Hesap oluştur + Supabase Auth + Ayarlar hesap bölümü
  → tek yeni bağımlılık kümesi burada; en sona bırakıldı ki ürün onsuz da çalışsın.
- **D-3** QA (Aşama 4) — kodlama bitince.

Sıralamanın gerekçesi: uygulama D-2d-1 bittiğinde **elle tutulur şekilde yeni**
olur; auth en sonda çünkü ürün değeri üretmiyor, yalnız kapı açıyor.

## K-064 — D-2d-1 (Günlük + seri) sonrası 2 PM kararı
- Tarih: 2026-09-19 · Durum: ✅ Karar

1. 🔴 **Geçmiş günler GÜNCEL limitle değerlendiriliyor** (geliştiricinin bildirdiği
   sapma 1). Bu, seri sisteminin güvenilirliğini bozar: kullanıcı limitini
   değiştirince **geçmiş serisi geriye dönük değişir** — "13 gün" bir sabah
   "4 gün" olabilir. Oyunlaştırmanın tek sermayesi güven olduğu için kabul edilemez.
   **Karar:** `limit_gecmisi` tablosu eklenecek (yürürlük tarihi + kuruş). Seri
   hesabı her gün için **o gün yürürlükte olan** limiti kullanacak. Tablodan önceki
   dönem için güncel limit "en iyi tahmin" olarak kalır ve bu davranış kodda
   belgelenir. D-2d-2 turuna eklendi.
2. 🟡 **`gunsec.alt.acik_gun` metni yanlış yorumlandı.** Geliştirici "{n} gün
   kayıtlı" yazmış. Doğrusu: gün seçicide **seçim halkası kaldırıldığı için**
   (K-061/B-2) o anda **açık/görüntülenen günün yazıyla** belirtilmesi. Metin
   ızgaradaki seçili günün yerine geçiyor; kaldırılırsa kullanıcı hangi günde
   olduğunu göremez. **Düzeltme D-2d-2'ye eklendi.**

**Kabul edilen sapmalar:** kaydırma ipucunun "3 açılış sayacı" yerine tek kalıcı
kapatma bayrağı olması · hata durumunun paylaşılan `ErrorState` ile verilmesi ·
FAB gizleme kuralının tüm boş-bugün durumlarına genellenmesi.
**QA'ya not:** 300+ günlük geçmişte `FlatList` pencereleme senaryosu denenecek.
