# Trinkow — Varlık Kilidi (P-6)

> **Bu dosya kilittir.** Buradaki ikon seti, font ve çizim primitifi
> dışında hiçbir görsel varlık projeye giremez. Yeni bir set/font/paket
> eklemek Mustafa onayı gerektirir (CLAUDE.md → onay gerektiren işlemler).
>
> Bütçe kuralı (K-009): **her varlık ücretsiz ve ticari kullanıma açık
> lisanslı** olmak zorunda. Aşağıdaki her kalemin lisansı doğrulanmıştır.
> Doğrulama tarihi: 2026-09-10.

---

## 1. İKON SETİ — **Lucide** (kilitli, tek set)

| Alan | Değer |
|---|---|
| Set | **Lucide** |
| Paket | `lucide-react-native` |
| Sürüm | **1.43.0** (pin'lenir, `^` ile açık bırakılmaz) |
| Lisans | **ISC** — ücretsiz, ticari kullanıma açık, atıf zorunluluğu yok |
| Bağımlılık | `react-native-svg` (MIT, 15.x) — `LimitBar` için zaten gerekli |
| Çizgi kalınlığı | **2.0** — tek değer (tokens.md v3.1 §9: clay'in yumuşak yüzeyine karşı net kontur gerekir; v2'deki 1.75 iptal) |
| Boyutlar | 24pt varsayılan · 20pt liste içi · 28pt sekme. **Ara boyut yok** |
| Renk | `text` · `text-2` · `primary-text` · `#FFFFFF` · `cat.*.solid` · `warning-ink` · `danger-ink` (tokens.md §9). Başka renk yok |
| Dolgulu ikon | Kullanılmaz |

**Neden Lucide (Tabler/Feather yerine):** brandbook §6.3'te zaten
kilitlendi. Gerekçe: `strokeWidth` prop'u ile 1.75'e ayarlanabiliyor
(Feather 2.0'a sabit çizilmiştir ve ince ayarı yoktur), set 1818 ikonla
Faz 2/3 ihtiyaçlarını da karşılıyor, RN paketi ikon başına ağaç
sallanabiliyor (tek tek import → uygulama boyutu şişmiyor).

> **Sürüm tuzağı (frontend-developer için önemli):** Lucide 1.x'te bazı
> isimler değişti: `trash-2` → `trash`, `home` → `house`,
> `help-circle` → `circle-question-mark`.
>
> **PM düzeltmesi (2026-09-10):** Eski isimler **kaldırılmadı** — 1.43.0
> paketinde geriye dönük alias olarak hâlâ export ediliyor (`Home`, `Trash2`,
> `HelpCircle` ve yeni karşılıkları birlikte mevcut; npm paketi indirilip
> doğrulandı). Yani eski isimli kod **çalışır, patlamaz.**
> Kural yine de geçerli: **yeni isimleri kullan** — alias'lar ileride
> kaldırılabilir ve tek isimlendirme düzeni tutarlılık sağlar.
> Ama çalışan eski isimli kodu "bozuk" sanıp acil düzeltmeye kalkma.

### 1.1 Kategori ikonları (13 — kategoriler renk taşımaz, ayrım BUNLARLA olur)

| Kategori (kullanıcıya görünen) | Lucide adı | RN import |
|---|---|---|
| Market | `shopping-basket` | `ShoppingBasket` |
| Kafe | `coffee` | `Coffee` |
| Restoran | `utensils` | `Utensils` |
| Ulaşım | `bus` | `Bus` |
| Akaryakıt | `fuel` | `Fuel` |
| Fatura | `receipt-text` | `ReceiptText` |
| Kira ve ev | `house` | `House` |
| Abonelik | `repeat` | `Repeat` |
| Sağlık | `pill` | `Pill` |
| Giyim | `shirt` | `Shirt` |
| Eğlence | `ticket` | `Ticket` |
| Alışkanlıklar | `footprints` | `Footprints` |
| Diğer | `circle-dashed` | `CircleDashed` |

**v3.1 düzeltmesi:** kategori ikonu 20pt olarak **44×44, radius 16, çukur
(`clay.sunken`) bir kabın** içine konur ve rengi `cat.*.solid`'dir
(tokens.md §7.3). Bu, yasaklanan kalıp **değildir**: anti-pattern listesi
"daire içinde ikon + başlık + tek cümle"den oluşan **3'lü özellik kartını**
yasaklar; liste satırındaki kategori kabı bilgi taşır (kategori kimliği) ve
dairesel değil, köşeli-yumuşak bir kaptır. v1/v2'deki "ikonsuz, `text-2`
renginde" kural iptal edildi — clay dilinde renksiz ikon satırı düz kalıyordu.

### 1.2 Arayüz ikonları (18)

| İş | Lucide adı | Nerede | `accessibilityLabel` |
|---|---|---|---|
| Bugün sekmesi | `gauge` | TabBar | "Bugün sekmesi" |
| Kayıtlar sekmesi | `notebook-text` | TabBar | "Kayıtlar sekmesi" |
| Özet sekmesi | `chart-no-axes-column` | TabBar | "Özet sekmesi" |
| Harcama ekle | `plus` | Pano birincil buton | "Harcama ekle" |
| Kapat | `x` | BottomSheet | "Kapat" |
| Geri | `chevron-left` | Alt sayfa başlığı | "Geri dön" |
| İleri / detay | `chevron-right` | Liste satırı, ayarlar | "Ayrıntıyı aç" |
| Aç / genişlet | `chevron-down` | Tüm kategoriler | "Listeyi genişlet" |
| Seçili ayar | `check` | Ayarlar listesi | "Seçili" |
| Sil | `trash-2` | Kaydırma eylemi, detay, ayarlar | "Harcamayı sil" |
| Düzenle | `pencil` | Harcama detayı, limit kuyusu | "Değiştir" |
| Ayarlar | `settings` | Pano sağ üst | "Ayarları aç" |
| Tekrarla | `rotate-cw` | Kaydırma eylemi | "Bu harcamayı tekrarla" |
| Geri al | `undo-2` | Toast | "İşlemi geri al" |
| Taksit | `layers` | Taksitli satır, taksit sayfası | "Taksitli işlem" |
| Nakit | `banknote` | SegmentedControl | "Nakit" |
| Kart | `credit-card` | SegmentedControl | "Kart" |
| Bildirim | `bell` | Ayarlar | "Bildirim ayarları" |

### 1.2b Tur A'da eklenen ikonlar (3) — **PM onayı bekliyor**

Kurulum ekranındaki niyet seçimi için gerekti. CONTEXT.md emojiyi yasaklıyor,
brandbook §6.1 "önce metinle çözülebilir mi" diyor; üç seçenek metinle de
çalışıyor ama satırın solunda bir tutamaç olmadan liste cansız kalıyordu.
Üçü de aynı setten (Lucide, ISC) ve kilitli çizgi kalınlığında.

| İş | Lucide adı | Nerede | `accessibilityLabel` |
|---|---|---|---|
| Niyet: Takip | `route` | E-01 seçim satırı | — (satır metni okunur) |
| Niyet: Tasarruf | `piggy-bank` | E-01 seçim satırı | — |
| Niyet: Borç | `trending-down` | E-01 seçim satırı | — |

Onaylanırsa Faz 1 toplamı **34** olur. Reddedilirse E-01 seçim satırları
ikonsuz kurulur; başka hiçbir ekran etkilenmez.

### 1.2c Tur E'de eklenen ikonlar (2) — prototip v3'te kullanıldı

| İş | Lucide adı | Nerede | `accessibilityLabel` |
|---|---|---|---|
| Limiti kaldır | `circle-slash` | E-17 limit satırı eylemi | "{kategori} limitini kaldır" |
| Taksit takvimi | `calendar-clock` | E-18 boş durum illüstrasyonu | — (dekoratif) |

> Prototipte ayrıca `info`, `list-x`, `refresh`, `clock`, `sliders`,
> `target`, `landmark`, `calendar-days`, `delete` (tuş takımı geri sil) ve
> `circle-dashed` kullanıldı; hepsi Lucide'dir. **Kullanılmayan hiçbir ikon
> projeye alınmadı** — Tur E'de eklenip kullanılmayan 5 ikon (`settings`,
> `sunrise`, `wallet`, `arrow-right`, `database-zap`) üreteçten silindi.
>
> Özet sekmesi ikonu prototipte `chart-no-axes-column` adıyla çizilir
> (RN: `ChartNoAxesColumn`) — `chart-column` eksenli çizer, bizim çizim
> eksensizdir.

### 1.2d v4'te eklenen ikonlar (5) — prototip v4'te kullanıldı

| İş | Lucide adı | Nerede | `accessibilityLabel` |
|---|---|---|---|
| Şifreyi göster / gizle | `eye` · `eye-off` | E-22 · E-23 şifre alanı sağ yuvası | "Şifreyi göster" · "Şifreyi gizle" |
| Çıkış yap | `log-out` | E-19 Hesap bölümü | "Çıkış yap" |
| Bağlantı yok | `wifi-off` | E-22 · E-23 ağ hatası şeridi | — (şerit metni taşır) |
| Bağlantı gönderildi | `mail-check` | E-22 şifre sıfırlama kartı | — (dekoratif) |
| Ürün ara | `search` | E-11 arama alanı | "Ürün ara, isteğe bağlı" |

> Dayanak: K-057/2 (ilk dördü) · K-050 (`search`). **Yeni set yok, yeni
> boyut yok, yeni çizgi kalınlığı yok** (tokens §9: 20/22/24/28pt · 2.0).

**Toplam Faz 1 ikon sayısı: 45** (prototip v4'te fiilen çizilen glif
sayısı; kaynak `prototip-v4/_uret/lib.py` ikon sözlüğü — sayım mekanik
olarak doğrulanabilir, iki yerde tutulmaz). Hepsi Lucide'dir.
Bu listede olmayan bir ikon gerekiyorsa
önce "metinle çözülebilir mi?" sorulur (brandbook §6.1: tipografi öncelikli).

### 1.3 İkonda yasaklar
- İkinci bir setten **tek ikon bile** karıştırılmaz (Tabler, Feather,
  Heroicons, Material Icons, Font Awesome — hiçbiri).
- Emoji ikon yerine kullanılmaz (CONTEXT.md kesin kural).
- İkon renklendirilerek kategori ayrımı yapılmaz.
- Uyarı ikonu (`triangle-alert`, `circle-alert`) **limit aşımında
  kullanılmaz** — marka yargısız (brandbook §2.1). Bu iki ikon Faz 1
  listesinde bilinçli olarak yoktur.

---

## 2. FONTLAR — **v3.1 · kilitli (4 dosya)**

> Tek otorite: `projects/trinkow/docs/brand/tokens.md` §2.1. Dosyalar indirildi, `fontTools`
> ile glif doğrulaması yapıldı (2026-09-12):
> `projects/trinkow/docs/design/prototip-v3/fonts/LISANS.md`.
> v1.0 (Source Serif 4 / Public Sans) ve v2.0 (Space Grotesk / Figtree)
> yönleri **reddedildi**; o dosyalar projeye kopyalanmaz.

| Token | Dosya | Rol | Lisans |
|---|---|---|---|
| `font.ui.regular` | `Montserrat-Regular.ttf` | Gövde, liste, ikincil satır | OFL 1.1 |
| `font.ui.semibold` | `Montserrat-SemiBold.ttf` | Buton etiketi, etiket, vurgu | OFL 1.1 |
| `font.num.bold` | `Montserrat-Bold.ttf` | **Tüm rakamlar** (hero/display/amount) | OFL 1.1 |
| `font.display` | `Poppins-SemiBold.ttf` | **Yalnız başlık** (`h1`, `h2`) | OFL 1.1 |

**Bağlayıcı kurallar (tokens.md §2.1 ile birebir):**

1. **Mono font YOKTUR.** JetBrains Mono projeye alınmadı: `₺` (U+20BA)
   glifi yok. Denetimde `JetBrains` / `monospace` / `font-mono` aranır,
   bulunmamalıdır.
2. **Tüm rakamlar Montserrat** + `fontVariant: ['tabular-nums']`.
   Montserrat `tnum` + `lnum` + `locl` taşır (doğrulandı).
3. **Poppins `tnum` taşımaz** → rakam içeren hiçbir `Text`'te kullanılmaz.
   Başlıklar bu yüzden rakam içeremez ("Eylül 2026" başlık değil, etikettir).
4. Variable font gömülmez · italik yok · `fontWeight` sayısıyla ağırlık
   üretilmez — ağırlık **dosya seçimiyle** gelir.
5. Toplam **4 dosya**. Artırmak PM onayı gerektirir.

### 2.1 `₺` doğrulaması (2026-09-12, `fontTools`)

| Font | `₺` U+20BA | Türkçe glifler | `tnum` | Karar |
|---|---|---|---|---|
| Montserrat 400/600/700 | ✅ | ✅ | ✅ | Alındı |
| Poppins SemiBold | ✅ | ✅ | ❌ | Alındı — yalnız başlık |
| JetBrains Mono | ❌ | ✅ | ❌ | **Alınmadı** |

### 2.2 Kabul testi (font reddedilme kriteri)

Her font yüklendikten sonra şu dizgeyle test edilir; bir glif eksikse font
reddedilir: `ğ Ğ ı I i İ ş Ş ç Ç ö Ö ü Ü â î û` + `₺` + `0123456789`
(tabular kontrolü: `1111` ile `0000` aynı genişlikte olmalı).

### 2.3 Dosyalar nereden alınır

Her iki aile de `google/fonts` deposunda **statik** TTF olarak bulunur
(`ofl/montserrat`, `ofl/poppins`) — variable dosya indirmeye gerek yoktur.
Yalnız yukarıdaki 4 dosya `assets/fonts/` altına kopyalanır; diğer
ağırlıklar (Light, Black, Italic…) **projeye alınmaz** (uygulama boyutu).
npm paketi (`@expo-google-fonts/*`) kullanılmaz — depoya ikili dosya
koymak yeni bağımlılıktan ucuzdur.

---

## 3. ÇİZİM / GRAFİK VARLIKLARI

Tek primitif: **`EmptyGauge`** (bileşen envanteri §5 · eski adı
`TallyGraphic`).
- `react-native-svg` ile çizilir, hazır dosya indirilmez.
- Kahraman gösterge yayı ve boş gösterge aynı primitiften türer; çizgi
  kalınlığı ve renkler `tokens.md` §7.5'ten gelir (bu dosyada tekrar
  edilmez).
- Kullanım yeri: boş durumlar ve onboarding.

**Yasak (brandbook §6.2 + anti-pattern listesi):** stok illüstrasyon
(unDraw, Storyset, Humaaans…), maskot, karakter, avatar, fotoğraf,
3B render, ikon paketi illüstrasyonu, Lottie animasyonu.

---

## 4. LOGO VE UYGULAMA VARLIKLARI (üretilecek dosya listesi)

tokens.md §10'daki spesifikasyona göre üretilir. Faz 1'de gereken dosyalar:

> **v4 düzeltmesi:** bu tablo v1.0 "Defter" yönünün değerleriyle
> (`#14484C`, Source Serif 4, çentikli monogram) kalmıştı. Tek otorite
> `tokens.md` §10'dur (K-040); aşağıdaki satırlar ona göre düzeltildi.

| Dosya | Ölçü | Not |
|---|---|---|
| `icon.png` | 1024×1024 | Saydamlık yok, zemin `grad.action`, T `#FFFFFF`, topuz `#FFFFFF` (tokens §10). Metin taşımaz → gradyan izinli (§1.8 · K-062) |
| `adaptive-icon.png` | 1024×1024 | Android foreground; monogram 66dp güvenli alanda |
| `notification-icon.png` | 96×96 | Saydam zemin, beyaz silüet, 24px iç boşluk |
| `splash.png` | 1242×2688 | Zemin `bg`, ortada kelime markası 26pt `text`, "w" sağında topuz `primary`. Animasyon yok |
| `wordmark.svg` | vektör | **Poppins SemiBold**, tracking −2.0%, yazıya çevrilmiş |
| `monogram.svg` | 100×100 ızgara | T + topuz (tokens §10 geometrisi: T cap-height 58, baseline y=79, kol x 18→72, topuz çap 18, merkez 78/26.5) |

Bu dosyalar **Tur 2'de değil**, tasarım onayından sonra üretilir.

---

## 5. SES / TİTREŞİM

- Ses **yok**.
- Titreşim (haptic): yalnızca **iki** yerde — harcama kaydedildiğinde
  `Haptics.impactAsync(Light)` ve silme onaylandığında `Warning`.
  `expo-haptics` (MIT) Expo SDK içinde gelir, ek bağımlılık değildir.
  Limit aşımında titreşim **yoktur** (ceza sinyali üretir, brandbook §2.1).

---

## 6. KİLİT ÖZETİ (tek bakışta)

| Kalem | Karar | Lisans | Ücret |
|---|---|---|---|
| İkon | Lucide, **tek set**, çizgi kalınlığı **2.0** (tokens §9) | ISC | 0 |
| Başlık fontu | **Poppins** SemiBold (600) | OFL 1.1 | 0 |
| Gövde fontu | **Montserrat** (400/600/700) | OFL 1.1 | 0 |
| Çizim | `EmptyGauge` (kendi ürettiğimiz SVG) | — | 0 |
| Üçüncü taraf marka varlığı | Apple + Google oturum açma logoları (§7) | sahibinin kılavuzu | 0 |
| İllüstrasyon | Yok | — | 0 |
| Animasyon paketi | Yok (RN `Animated` yeterli) | — | 0 |

---

## 7. ÜÇÜNCÜ TARAF MARKA VARLIKLARI — **kilidin tek istisnası**

> Dayanak: **K-052** (Google + Apple ile oturum açma onaylandı) ·
> **K-057/2** (bu bölüm şart koşuldu) · **K-058** (platform kuralı).
> Kural tek cümlede: **kap bizim, içerik onların.** Ölçü, geometri ve
> gölge `tokens.md` §7.1 `button.social`'dan; dolgu, logo ve etiket
> sahibinin kılavuzundan gelir. Bu varlıklar **tema değildir** —
> kodda `src/theme/` altında değil, `src/theme/brand.ts` gibi ayrı bir
> marka dosyasında durur.

| Varlık | Kaynak | Lisans / kural | Ücret |
|---|---|---|---|
| **Apple ile Devam Et** düğmesi | `expo-apple-authentication` → `AppleAuthenticationButton` (style `BLACK`, type `CONTINUE`, cornerRadius 28) | Apple Human Interface Guidelines · "Sign in with Apple" · App Store 4.8 | 0 |
| **Google ile devam et** logosu ("G") | `react-native-svg` ile 4 `Path`; SDK `@react-native-google-signin/google-signin` | Google Identity — Branding Guidelines | 0 |

### 7.1 İzinli değerler (değiştirilemez)

| | Zemin | Metin / glif | Basılı | Kontur |
|---|---|---|---|---|
| Apple | `#000000` | `#FFFFFF` (21:1) | `#1A1A1A` | yok |
| Google | `#FFFFFF` | etiket `#1F1F1F` · G glifi `#4285F4` `#34A853` `#FBBC05` `#EA4335` | `#F2F2F2` | 1px `#747775` |

### 7.2 Yasaklar

- Logoyu **yeniden renklendirmek**, palete uydurmak, tek renge indirmek.
- Logoyu esnetmek, döndürmek, gölgelendirmek, kırpmak, kendi ikon setimizden
  bir karşılık çizmek.
- Etiketi kısaltmak / yeniden yazmak ("Apple ile gir", "Google girişi").
  Metin sahibinin yerelleştirmesidir (metinler §0 buton kuralının tek istisnası).
- Apple düğmesini **iOS'ta biz çizmek** — `expo-apple-authentication`
  bileşeni kullanılır (doğru glif, doğru yerelleştirme, doğru davranış).
- Apple düğmesini **Android'de göstermek** (K-058: Android'de yalnız Google).

### 7.3 Nerede durur

| Yer | Dosya |
|---|---|
| Prototip | `prototip-v4/stil.css` · "ÜÇÜNCÜ TARAF" bloğu (`.btn-apple`, `.btn-google`, `.g-*`), `@denetim-disi` işaretleri arasında |
| Prototip yüzeyleri | `15-giris.html` (E-22) · `16-kayit.html` (E-23) |
| Uygulama | `src/theme/brand.ts` (renkler) · `src/components/SocialAuthButton.tsx` (kap) |

Bu değerler `tokens.md` §1 paletine **girmez** ve denetim beyaz listesini
genişletmez: `denetim.py` istisnayı yapıdan (`@denetim-disi` bloğu) okur,
paletten değil (tokens §12.0).

