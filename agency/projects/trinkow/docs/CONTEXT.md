# CONTEXT — Bağlam Paketi (P-1)

## Ürün adı: **Trinkow**

> Bu dosya projenin **tek sayfalık özetidir.** Tüm alt-ajanlar bunu okur.
> Kaynak: `projects/trinkow/docs/Harcama Takip Uygulaması Rapor ve Dökümantasyonu.txt`
> (fizibilite raporu). Uzun rapora ancak burada cevabı olmayan bir şey
> varsa git. Son güncelleme: 2026-09-10

## Ürün nedir?
**Trinkow** — harcamaları **kalori sayar gibi** takip ettiren davranışsal finans
uygulaması. Kullanıcı günlük bir harcama limiti belirler; her harcamayı
manuel girer; kalan limit bir ilerleme çubuğunda anlık görünür.

Amaç muhasebe değil **davranış değiştirmek**: dijital ödemenin yok ettiği
"ödeme acısını" (pain of paying) anlık farkındalıkla geri getirmek.
Hedeflenen sızıntı: "Latte Faktörü" denen küçük ve fark edilmeyen
mikro-harcamalar (günlük kahve, sigara, dışarıda yemek).

## Kim kullanacak?
Davranışsal tanım (demografik değil): büyük giderlerinin farkında ama
parasının günlük olarak nereye gittiğini bilmeyen, dijital ödemeye alışmış
kullanıcı. Üç farklı niyetle geliyor — ürün bu niyete göre kişiselleşir:
1. **Sadece Takip** — "param nereye gidiyor?"
2. **Tasarruf / Yatırım** — bütçe yaratmak
3. **Borç Kapatma** — borç eritmek

## MVP kapsamı (Faz 1)
**İÇİNDE:**
- Hızlı, düşük sürtünmeli **manuel harcama girişi** (nakit + kart + taksitli)
- **Günlük harcama limiti** ve kalan limiti gösteren ilerleme çubuğu
- **Onboarding: ZORUNLU katman en fazla 3 soru** (K-053 ile iki katmanlı oldu:
  Katman 1 zorunlu 3 soru → uygulama çalışır hâle gelir; Katman 2 "Seni tanıyalım"
  ~8 kart **atlanabilir** ve ayarlardan sonra tamamlanabilir. Zorunlu sınır bozulmadı.)
- (eski ifade, bağlam için)**Onboarding: en fazla 3 soru.** Ana niyet ilk kayıtta alınır; geri kalan
  (gelir düzeyi, taksit alışkanlığı, bildirim tercihi) sonraki günlere
  yayılır → "aşamalı profilleme"
- Seçilen niyete göre **anında kişiselleşen** pano (ör. "Borç Avcısı Modu")
- Adım göstergesi ("Adım 1/3") — belirsizliği kaldırır, tamamlanma artırır
- **Veri sunucuda** (kendi Python backend'imiz + MongoDB). 2026-09-19 direktifi
  K-068: "cihazda bilgi tutma muhabbeti yok". Cihaz yalnız oturum token'ını ve
  görüntülenen verinin geçici önbelleğini tutar; **tek gerçek kaynak sunucudur**.
- Kategori bazlı takip (zihinsel muhasebe: her kategorinin kendi limiti)
- **Seri (streak) + milestone kutlaması** — 2026-09-17'de Mustafa'nın direktifiyle
  Faz 2'den MVP'ye ALINDI. Kural seti: `status/DECISIONS.md` K-048. Kapsam
  yalnız seri + milestone + seri yüzeyi; puan/seviye/rozet DEĞİL.
- **Ürün arama ile hızlı giriş** — harcama eklerken yerel ürün kataloğundan
  arama, fiyatı kullanıcı girer. Uyarlama yasakları: K-050.
- **Günlük sekmesi tarih sayfalamalı** (Bugün / Dün / 17/09 Çarşamba): K-049.
- **Giriş/Kayıt zorunlu hâle geldi** (K-068): hesap sunucuda, kimlik **kendi
  `auth` modülümüz + JWT**. Supabase düştü (K-052 geçersiz).

**KAPSAM DIŞI (Faz 2/3 — MVP'ye sokma):**
- Oyunlaştırma: XP, seviye, rozet, lig → **Faz 2+ / bir kısmı kalıcı olarak dışı**
  (K-048: puan ekonomisi bütçe uygulamasında sahte motivasyon üretir)
- Fiş fotoğrafından okuma (GPT-4o-mini) → **Faz 3**
- Açık bankacılık / otomatik kart okuma (BDDK) → **Faz 3**
- iOS Live Activities (kilit ekranı çubuğu) → raporda "ek olarak" geçiyor,
  MVP çekirdeği değil
- Çoklu kullanıcı, aile paylaşımı (bulut senkronu artık kapsam İÇİNDE — K-068)

## Ürün tipi ve stack — KESİNLEŞTİ
**React Native (Expo)** ile gerçek mobil uygulama. Karar: K-002 + K-005.
Geliştirme ortamı: Mac + iOS simülatörü mevcut.

- Veri: **kendi backend'imiz** (Python · FastAPI · MongoDB) — `../backend/`.
  İstemcideki `src/db/*` modülleri veri erişiminin tek dikişidir; API'ye onlar bağlanır.
- Navigasyon: `expo-router` · Dil: TypeScript
- **Backend: Python (FastAPI) + MongoDB** — modüler yapı, her modülde
  `controller` · `service` · `dto` · `model`. Mustafa direktifi, K-067/K-068.
  Şimdilik yalnız yerelde çalışır; prod barındırma kararı ertelendi.

**Tasarım ve kod için bağlayıcı sonuç — burası önemli:**
Bu bir web sitesi değil. CSS yok, HTML yok, **hover state yok** (dokunmatik:
`pressed` var). Layout **sadece flexbox** (CSS Grid yok). Gölge iOS ve
Android'de farklı çalışır. Fontlar uygulamaya gömülür, CDN'den çekilmez.
Detaylı kısıt listesi: `reference/rn-tasarim-kisitlari.md`

## Kısıtlar
- **Bütçe: $0 — ÜCRETLİ HİÇBİR ŞEY YOK.** (K-009, Mustafa'nın kesin kararı)
  Servis, araç, API, kütüphane, font, ikon seti, hosting, abonelik — hiçbiri.
  **Ajanlar ücretli bir çözümü seçenek olarak bile sunmaz**, doğrudan eler.
  Ücretsiz yol yoksa önce "bu özellik Faz 1'den çıkarılabilir mi?" diye sorulur.
  Lisans zorunluluğu: font OFL, ikon MIT/ISC/Apache. Şüpheliyse kullanılmaz.
- **Tek kişilik geliştirici** + AI kod asistanı senaryosu. Kapsamı buna göre
  küçük tut; "büyük finansal uygulama" mimarisi kurma.
- **Dil: Türkçe** (pazar Türkiye, para birimi TL).
- Faz sırası bozulmaz: önce davranışsal döngü çalışsın, sonra oyunlaştırma,
  en son otomasyon.

## Ürün sözlüğü
- **Latte Faktörü** — küçük, tekrarlayan, fark edilmeyen harcamaların
  kümülatif yükü. Ürünün varlık sebebi.
- **Ödeme Acısı (Pain of Paying)** — para harcarken hissedilen psikolojik
  rahatsızlık. Nakitte yüksek, dijitalde neredeyse yok.
- **Spendception (Harcama Yanılsaması)** — dijital ödemenin kayıp hissini
  köreltmesi. Ürün bunun panzehiri.
- **Zihinsel Muhasebe** — insanın parayı tek havuz değil, ayrı ayrı
  hesaplar olarak görmesi. Kategori limitlerinin psikolojik temeli.
- **Aşamalı Profilleme** — kullanıcıyı ilk gün sorularla yormayıp bilgiyi
  zamana yayarak toplamak.
- **Streak** — zinciri kırmama serisi (Faz 2).

## ⚠️ MARKA YENİDEN KURULUYOR (2026-09-11, K-018/K-019)
Aşağıdaki "Yön A Defter" paleti **TERK EDİLDİ** — Mustafa fazla katı ve
ruhsuz buldu. Yeni yön `projects/trinkow/docs/design/referans-analizi.md`'deki tasarım dili
üzerine kuruluyor: dairesel kahraman gösterge, derinlik, kategori renkleri,
yumuşak geometri, geometrik sans.
**Gevşetilenler:** gölge · gradyan · kategori renkleri · yüksek radius · görsel.
**Korunanlar:** emoji yasağı · utandırmayan ton · WCAG AA · mor-mavi
VARSAYILAN gradyan yasağı · jenerik şablon yasağı.
**Yeni:** UI'da teknik açıklama (veri nerede saklanıyor vb.) YASAK.

## Marka (ESKİ — Yön A, artık geçersiz)
Brandbook: `projects/trinkow/docs/brand/brandbook.md` · Yön **A "Defter"** seçildi.
- Palet: kağıt `#F4F1EA` · mürekkep `#1B1A17` · ikincil `#5C574C` ·
  vurgu Petrol `#14484C` · limit-dışı Kiremit `#A24A2A` · yıkıcı `#8E2F20`
- Tipografi: **Source Serif 4** (400/600, başlık + tabular rakam) +
  **Public Sans** (400/600, gövde). Fontlar gömülü, 4 dosya.
- Kişilik: Sakin · Dürüst · Yargısız · Ölçülü
- **Karanlık mod Faz 1'de YOK** (Faz 2'ye bırakıldı).
- **Kategoriler renk taşımaz** — ikon + metinle ayrışır.
- **İlerleme çubuğu doluluğa göre renk değiştirmez.** Trafik ışığı
  (yeşil→sarı→kırmızı) reddedildi; taşma ayrı segment (Kiremit).
  Kırmızı yalnızca silme onayına ayrılmıştır.
- Gölge kullanılmaz; katman ayrımı yüzey tonu + çizgiyle.

## Rakip konumu (marka için kritik)
Pazar iki uçta: **YNAB** gibi katı disiplin isteyen ciddi araçlar
(~$99/yıl, zorlayıcı) ve **Fortune City** gibi oyunlaştırmada boğulan,
finansal olarak yüzeysel kalanlar. Copilot/Monarch estetik ama pasif takip.

**Bizim boşluğumuz:** ikisinin ortası — kalori takibi kadar basit ve
günlük, ama oyuncak gibi değil. Ton: suçlayıcı değil, farkındalık veren.
Marka bu "ciddi ama ezici değil / basit ama çocukça değil" dengesinde
kurulmalı.

## ⛔ EMOJI YASAK (Mustafa kararı, 2026-09-10)
**Uygulamada emoji KULLANILMAZ.** Ne buton etiketinde, ne başlıkta, ne
onboarding'de, ne boş durum metninde, ne bildirimde.

Fizibilite raporu onboarding butonlarını emoji'li örnekliyor
("🚀 Yatırım İçin Bütçe Yaratmak"). **Bu örnek geçersizdir** — rapor
yazımıdır, tasarım kararı değil.

Niyet seçimi gibi ayırt edicilik gereken yerlerde emoji yerine **ikon
seti** kullanılır (P-6 ile kilitlenen tek set). İkon, emoji'nin aksine
markanın çizgi kalınlığına ve rengine uyar; emoji her cihazda farklı
render edilir ve markayı taşımaz.

Bu kural marka metinleri ve sosyal medya içeriği için de geçerli sayılır;
aksi yönde bir istisna gerekirse Mustafa'ya sorulur.
