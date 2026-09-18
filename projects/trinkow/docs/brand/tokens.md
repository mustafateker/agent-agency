# Trinkow — Tasarım Tokenları (**TASLAK v4.0 · Claymorphism**)

> **v4.0 (2026-09-18 · v4 birleştirmesi, T-1…T-5 delta'ları işlendi).**
> Her madde dayanak karar numarasıyla yazıldı; yeni renk / punto / radius /
> boşluk **üretilmedi**.
>
> | Değişen | Dayanak |
> |---|---|
> | §1.3 `success` grafik/segment bağlamı · `primary-deep` düz zemin | K-059/4 · K-062 |
> | §1.6 + §1.8 **gradyan zeminde metin yasağı** (birincil düğme düz renge döndü) | **K-062** |
> | §1.9 v4 kontrast çiftleri (hesaplandı + render edilen pikselden örneklendi) | K-061/1 · K-062 |
> | §2.2 `amount` rolüne gün sayısı değeri · §2.3 üçüncü taraf etiket istisnası | T-1 · K-057/2 |
> | §3.1 `12`'nin rolü forma uzadı · §3.3 `.gun-ag` telafisi | T-2 · T-1 |
> | §5.4 **seçim dili / dolgu dili** ayrımı (halka yok) | K-045 · K-054/6 · K-061/2 |
> | §7.1 `button.primary` düz `primary-deep` · `button.social` varyantı · `secondary.disabled` | K-062 · K-057/2 |
> | §7.13 v4 bileşen ölçüleri (seri · gün ızgarası · ay ızgarası · kaydırıcı · pay çubuğu · arama) | T-1…T-4 |
> | §8 `motion.celebrate.hold` · §9 beş yeni Lucide glifi | K-048 · K-057/2 |
> | §12 **işletim sistemi çizimleri** ve **üçüncü taraf marka varlıkları** istisnaları | K-061/6 · K-057/2 |
> | §14 **türetilmiş değerler** — kalan gün, günlük limit, biriken, öneri | K-059/6 · K-060/4 |
>
> **v3.1 (boşluk ritmi turu):** §3.1 dikey ritim seti ilan edildi · §3.2 kabuk
> ölçeği · §3.3 negatif oluk telafisi · §7.2 kart iç boşluğu tek değer ·
> §7.5 gösterge 296 → 224 (+ boş durum 176) · §7.7 FAB taşması 16.

> **Bu dosya değer tablosudur, gerekçe içermez.**
>
> ## Otorite hiyerarşisi (v3'te DEĞİŞTİ — önce bunu oku)
>
> | Katman | Kaynak | Durum |
> |---|---|---|
> | **Görsel** (renk, tipografi, geometri, gölge, hareket) | `agency/vendor/design-systems/library/claymorphism/DESIGN.md` | **TEK OTORİTE** |
> | **Ürün** (ton, kişilik, metin kuralları, yasaklar, para biçimi) | `projects/trinkow/docs/brand/brandbook.md` §2, §7-§8 | Geçerli |
> | Brandbook'un görsel katmanı (v2 "Gün Işığı": amber palet, Space Grotesk/Figtree, gölge stratejisi, geometri) | — | **İPTAL** |
>
> Çelişkide: görsel soru → `DESIGN.md`; metin/ton sorusu → brandbook.
> Eşleme yöntemi: `agency/vendor/design-systems/interop-protocol.md` **Yön A**
> (dış sistemden bizim token yapımıza). Yapı korundu, değerler değişti.
>
> **Durum: TASLAK — Mustafa onayı bekliyor.** v1.0 (Defter) ve v2.0
> (Gün Işığı) reddedildi. v2.0 değerleri §13 ARŞİV'de.
>
> **Kapsam:** Faz 1 · React Native (Expo) · tek tema: **açık**.
> Karanlık mod **Faz 2** — bu dosyada tokenı yoktur, üretilmez.
>
> Kullanım: `design-reviewer` mekanik denetimi bu dosyaya karşı yapar ·
> `frontend-developer` değerleri `src/theme/tokens.ts`'e çevirir.
>
> Prototip: `projects/trinkow/docs/design/prototip-v3/` · Tarih: 2026-09-12

---

## 0. YÖN A EŞLEME TABLOSU (DESIGN.md → bizim tokenlar)

| DESIGN.md rolü | Değer | Bizim token(lar)ımız | Not |
|---|---|---|---|
| Primary | `#3B82F6` | `primary` | Yalnız **grafik/dolgu**. Küçük beyaz metin ardında kullanılamaz (bkz. §1.6). |
| Secondary / Surface / Neutral | `#FFFFFF` | `surface` | Kart, sheet, yüzen çubuk. |
| Text | `#1C398E` | `text` | Gövde + başlık. |
| Success | `#16A34A` | `success` | Grafik. Metin varyantı `success-text`. |
| Warning | `#D97706` | `warning` | **Limit dışı sinyali.** Metin varyantı `warning-ink`. |
| Danger | `#DC2626` | `danger` | Yalnız yıkıcı işlem. |
| Spacing 4/8/12/16/24/32 | — | §3 (birebir) | Ara değer üretilmez. |
| Type: Montserrat / Poppins / JetBrains Mono | — | §2 | **JetBrains Mono düşürüldü** (`₺` glifi yok — §2.1). |
| Radius (belirtilmemiş, "consistent radii") | — | §4 | Clay → yüksek yarıçap ailesi 16/24/32/tam. |
| Elevation ("consistent elevation strategy") | — | §5 | Clay: çok katmanlı outset + inset. |
| Motion 150–250ms | — | §8 | Birebir alındı (yay animasyonu istisna). |

**Boşluk (gap) — DESIGN.md'de olmayıp bizde olan roller:** `bg` (sayfa
zemini), `groove`/`well` (oluk), `text-2`/`text-3`, kategori aileleri,
`pressed` durumları. Hepsi **mevcut 6 tokenden türetilmiştir** (tint /
shade / desatürasyon) — palet dışı hue yoktur. Türetme yöntemi §1.7'de.

---

## 1. RENK — Faz 1 (tek tema: açık)

### 1.1 Zemin ve yüzey

| Token | HEX | Kullanım kuralı |
|---|---|---|
| `bg` | `#E6EFFE` | Sayfa zemini. `primary`'nin %13 tint'i. Tek zemin rengi. |
| `surface` | `#FFFFFF` | Kabarık (raised) clay yüzey: kart, sheet, yüzen sekme çubuğu, çip. |
| `groove` | `#F2F7FE` | Basılı (`pressed`) yüzey zemini, hata illüstrasyonu dairesi, kategori çubuğu oluğu. |
| `well` | `#E6EFFE` | Çukur yüzey: tutar kuyusu, segment track, **kahraman yay oluğu**, adım göstergesi oluğu, iskelet blokları. |
| `line` | `#DCE6F9` | 1px hairline. **Dekoratif** — anlam taşımaz, gölge yerine geçmez. |
| `disabled-bg` | `#DCE6F9` | Pasif buton/çip zemini. |
| `scrim` | `rgba(28, 57, 142, 0.38)` | Yalnız modal/bottom sheet arkası. |

> **Kasıtlı zayıf çift:** `surface` ↔ `bg` = **1.16:1**, `groove` ↔
> `surface` = **1.09:1**. Ayrım **renkle değil, clay gölgesiyle** kurulur
> (§5). Claymorphism'in tanımı budur; katman bilgisi yükseklikten gelir.

### 1.2 Metin

| Token | HEX | Nerede | En düşük kontrast |
|---|---|---|---|
| `text` | `#1C398E` | Başlık, tutar, birincil metin | 7.96:1 (`groove` üzerinde) |
| `text-2` | `#4961A5` | İkincil satır, etiket, tarih, pasif ikon | 4.56:1 |
| `text-3` | `#556AAA` | Placeholder. **Yalnız `surface` / `groove` üzerinde** — `well` üzerinde 4.50 ile sınırda kalır, orada `text-2` kullanılır. | 4.85:1 |
| `on-primary` | `#FFFFFF` | `primary-deep` / `danger` zemin üstü metin | 4.83:1 |

### 1.3 Eylem ve durum

| Token | HEX | Kullanım kuralı |
|---|---|---|
| `primary` | `#3B82F6` | **Grafik/dolgu**: yay dolgusu açık ucu, nokta, çip solid, FAB yüzeyi açık ucu. **Altına küçük beyaz metin konmaz.** |
| `primary-deep` | `#2F68C5` | **Metin taşıyan mavi yüzeylerin tek zemini** (K-062): birincil buton (düz, gradyansız), dolu gün kutusu, geçilmiş durak, seçili gün. Ayrıca FAB/yay gradyanının koyu ucu. Beyaz metin 5.37:1. |
| `primary-press` | `#295BAC` | Birincil buton / FAB `pressed`. Beyaz metin 6.59:1. |
| `primary-text` | `#2C62B8` | Mavi **metin/ikon** gerektiğinde (bağlantı, aktif sekme). 5.92:1. |
| `primary-soft` | `#E4EEFE` | **Kahraman kart zemini**, seçili çip zemini, aktif sekme ikon dairesi, bilgi kutusu. `text` 8.87:1 · `text-2` 5.24:1. |
| `warning` | `#D97706` | **Limit dışı sinyali** — taşma yayı, taşma çubuğu, toast şeridi. Grafik. |
| `warning-ink` | `#8A4B04` | Limit dışı **metin/ikon**. 6.80:1 (`surface`), 5.86:1 (`warning-soft`). |
| `warning-soft` | `#FAECDC` | Limit dışı satır zemini, limit dışı bilgi şeridi. |
| `danger` | `#DC2626` | **Yalnız dört bağlam:** taksit serisi silme onayı (E-13) · tüm verileri silme onayı (E-19) · form hatası kenarlığı · silme toast'ının 8pt göstergesi (§7.9). Ortak ölçüt (K-029): **yüksek etkili + geri alınamaz**. Tek harcama silme onaysızdır, kırmızı görmez (K-029). Beyaz metin 4.83:1. |
| `danger-ink` | `#C62222` | Hata metni. 5.75:1. |
| `danger-soft` | `#FAE1E1` | Silme onayı sheet zemini vurgusu. |
| `success` | `#16A34A` | Grafik: onay ikonu dolgusu, limit altı mini gösterge, **plan pay çubuğunun birikim segmenti** (K-059/4 · E-26). **Metin olarak kullanılmaz** — `bg` üstünde 2.85 ❌ (§1.9). |
| `success-ink` | `#12823B` | Başarı metni. **Yalnız `surface` üzerinde** (4.90:1). |
| `success-soft` | `#DEF2E6` | Başarı bilgi zemini. `success-ink` bu zeminde **metin olarak kullanılmaz** (4.19:1). Üzerine `text` yazılır. |

### 1.4 Kategori renkleri — **6 aile · 13 kategori**

Aile rengi **grup** bilgisi taşır; kategoriyi ayıran şey **ikon + ad**tır
(WCAG 1.4.1: renk tek başına bilgi taşımaz).

| Aile | `solid` (ikon/nokta) | `soft` (çip zemini) | ikon/soft | solid/beyaz |
|---|---|---|---|---|
| `cat.mavi` | `#306BCA` | `#E4EEFE` | 4.40:1 | 5.15:1 |
| `cat.lacivert` | `#172F74` | `#DFE3EF` | 9.66:1 | 12.39:1 |
| `cat.yesil` | `#12863D` | `#DEF2E6` | 3.99:1 | 4.66:1 |
| `cat.amber` | `#B26205` | `#FAECDC` | 3.90:1 | 4.52:1 |
| `cat.kiremit` | `#B41F1F` | `#FAE1E1` | 5.36:1 | 6.65:1 |
| `cat.duman` | `#2E3A5C` | `#DEDFE5` | 8.42:1 | 11.19:1 |

| Aile | Kategoriler (ikonla ayrışır) |
|---|---|
| `cat.yesil` | Market (`shopping-basket`) · Sağlık (`pill`) |
| `cat.amber` | Kafe (`coffee`) · Restoran (`utensils`) |
| `cat.mavi` | Ulaşım (`bus`) · Akaryakıt (`fuel`) |
| `cat.lacivert` | Fatura (`receipt-text`) · Kira ve ev (`house`) · Abonelik (`repeat`) |
| `cat.kiremit` | Eğlence (`ticket`) · Giyim (`shirt`) |
| `cat.duman` | Alışkanlıklar (`footprints`) · Diğer (`circle-dashed`) |

| Kural | Değer |
|---|---|
| `solid` nerede | 8pt nokta, kategori ikonu, kategori çubuğu dolgusu, grafik serisi |
| `soft` nerede | Çip zemini, kategori ikon kabı (44×44, radius 16), seçili kategori zemini |
| Kategori rengi **metin** olarak | **Kullanılamaz.** `soft` zemin üstüne daima `text #1C398E` (en kötü 7.80:1) |
| 7. aile | **Üretilmez.** Yeni kategori mevcut altı aileden birine ikonla girer. |
| `cat.amber` ↔ `warning` ayrımı | Bkz. §1.5 — bilinçli karar, denetimde ihlal değildir |

### 1.5 Amber çakışmasının çözümü (bilinçli karar)

`cat.amber` (Kafe/Restoran) ile `warning` (limit dışı) aynı hue ailesinden.
Sinyal karışmasın diye **üç ayrım** zorunludur:

| | Kategori ambe­ri | Limit dışı ambe­ri |
|---|---|---|
| Değer | `#B26205` ikon · `#FAECDC` çip | `#D97706` yay · `#8A4B04` metin |
| Yer | Yalnız **liste satırı ve çip** içinde | Yalnız **kahraman gösterge, toast şeridi, tutar etiketi** |
| Eşlik eden | Kategori adı ("Kafe") | Birebir **"limit dışı"** sözcüğü |

Kahraman göstergede ve tutar etiketlerinde kategori rengi **hiç görünmez**;
liste satırında taşma yayı **hiç görünmez**. İki bağlam kesişmez.

### 1.6 🔴 Kritik kontrast düzeltmesi — `primary` üzerinde beyaz metin

`#FFFFFF` / `#3B82F6` = **3.68:1 → WCAG AA'yı (4.5:1) GEÇMİYOR.**

| Yapılamaz | Yapılan |
|---|---|
| Birincil butonu `#3B82F6` zeminle + beyaz metinle çizmek | Buton zemini **`primary-deep #2F68C5`** (5.37:1 ✅), `pressed` **`primary-press #295BAC`** (6.59:1 ✅) |
| `#3B82F6` üzerine `text #1C398E` yazmak (2.82:1) | Yasak |

`primary #3B82F6` yalnız **metin taşımayan** yüzeylerde kalır: yay
dolgusunun açık ucu, ilerleme/kaydırıcı dolgusu, kategori noktası, mini
gösterge. Bu kural denetimde aranır.

**K-062 genellemesi (2026-09-18) — kural gradyanı da kapsar.** Ölçüm:
`grad.action`'ın üst yarısı (%28-40) `rgb(55,121,229)`…`rgb(54,120,226)`
arasıdır ve beyaz metinle **4.18 – 4.25 ❌**. *(Ara durak değerleri bilerek
`rgb()` yazıldı: bunlar jeton değil, ölçüm sonucudur — palet beyaz listesine
girmemeleri gerekir.)* Dolayısıyla "metin gradyanın koyu yarısına
hizalanır" varsayımı bırakıldı (CSS/RN metni **ortalar**; hizalama her
buton boyunda yeniden ayar isterdi ve optik olarak yanlış görünür).

| Yüzey metin taşıyor mu? | Zemin |
|---|---|
| **Evet** (buton etiketi, kutu içi sayı, durak sayısı) | **Düz `primary-deep`** + `clay.action`/`clay.raised`. Hacim **gölgeden** gelir. `pressed` → düz `primary-press` (6.59:1) |
| **Hayır** (yay, ilerleme/kaydırıcı dolgusu, anahtar track'i, FAB'ın ikonu, app icon) | `grad.action` serbest — grafik eşiği 3:1 (en kötü nokta `#3B82F6` = 3.68 ✅) |

### 1.7 Türetme yöntemi (palet dışı hue yoktur)

| Türev | Formül | Örnek |
|---|---|---|
| `*-soft` / `bg` | sRGB'de token + beyaz karışımı (%13–16 token) | `primary` %13 → `bg #E6EFFE` |
| `*-deep` / `*-ink` | sRGB'de token + siyah karışımı (%15–30) | `warning` %35 → `warning-ink #8A4B04` |
| `text-2` / `text-3` | `text` + beyaz (%80 / %75 beyaz) | `#4961A5` / `#556AAA` |
| `cat.duman` | `text`'in %60 desatüre edilmiş hâli (luma'ya doğru) | `#2E3A5C` |

### 1.8 İzinli gradyanlar (yalnız 4 tane — clay'in hacim hissi)

| # | Token | Duraklar | Yön | Nerede |
|---|---|---|---|---|
| 1 | `grad.arc` | `#3B82F6` → `#2F68C5` | yay boyunca | Kahraman yay dolgusu |
| 2 | `grad.arc-over` | `#D97706` → `#B45309` | yay boyunca | Taşma yayı (yalnız limit dışı) |
| 3 | `grad.action` | `#3B82F6` → `#2F68C5` | dikey (üst→alt) | **Yalnız metin taşımayan yüzeyler** (K-062): FAB (28pt beyaz ikon — grafik), açık anahtar track'i, ilerleme/yük/kaydırıcı dolgusu, adım çubuğu, durak bağı, app icon zemini. **Birincil buton bu listede DEĞİLDİR** → düz `primary-deep`. |
| 4 | `grad.clay-face` | `rgba(255,255,255,0.9)` → `rgba(255,255,255,0)` | dikey, üst %45 | Kabarık yüzeyin üst parlaması (kart, çip, topuz) |

| Yasak | |
|---|---|
| Mor-mavi / indigo-violet gradyan | Yasak (anti-pattern §1) |
| Tam ekran arka plan gradyanı | Yasak |
| 3+ duraklı, hue değiştiren gradyan | Yasak |
| Metin gradyanı | Yasak |
| **Gradyan zeminde metin** (K-062) | **Yasak.** Metin taşıyan yüzey düz renk alır; gradyan yalnız metinsiz yüzeyde kalır. Gerekçe ve ölçüm §1.6 |
| Glassmorphism / `blur` katmanı | Yasak (`<main>` içinde) |

Kütüphane: `expo-linear-gradient` · yay için `react-native-svg`
`<LinearGradient>`. İkisi de ücretsiz.

### 1.9 Onaylı kontrast çiftleri (hesaplandı, 2026-09-12)

| Ön plan | Arka plan | Oran | Sonuç |
|---|---|---|---|
| `text` | `surface` | **10.37** | AAA |
| `text` | `bg` | **8.96** | AAA |
| `text` | `groove` | **9.63** | AAA |
| `text` | `well` | **8.96** | AAA |
| `text-2` | `surface` | **5.94** | AA |
| `text-2` | `bg` | **5.13** | AA |
| `text-2` | `well` | **5.13** | AA |
| `text-2` | `disabled-bg` | **4.73** | AA |
| `text-3` | `surface` | **5.21** | AA |
| `text-3` | `groove` | **4.85** | AA (alt sınır) |
| `#FFFFFF` | `primary-deep` | **5.37** | AA |
| `#FFFFFF` | `primary-press` | **6.59** | AA |
| `#FFFFFF` | `danger` | **4.83** | AA |
| `primary-text` | `surface` | **5.92** | AA |
| `primary-text` | `primary-soft` | **5.06** | AA |
| `warning-ink` | `surface` | **6.80** | AA |
| `warning-ink` | `warning-soft` | **5.86** | AA |
| `warning-ink` | `bg` | **5.87** | AA |
| `danger-ink` | `surface` | **5.75** | AA |
| `danger-ink` | `danger-soft` | **4.63** | AA |
| `success-ink` | `surface` | **4.90** | AA |
| `text` | `cat.*.soft` (en kötü `cat.duman`) | **7.80** | AAA |
| **Tur E'de eklenen çiftler (2026-09-12)** | | | |
| `text` | `danger-soft` (E-19 silme özeti) | **8.36** | AAA |
| `text-2` | `groove` (basılı satırın ikincil metni) | **5.52** | AA |
| `text-2` | `well` (`Limit yok` etiketi, E-17) | **5.13** | AA |
| `warning-ink` | `groove` | **6.32** | AA |
| **Grafik (3:1 eşiği)** | | | |
| `primary` yay dolgusu | `well` (yay oluğu) | **3.18** | ✅ ≥3 |
| `warning` taşma yayı | `surface` | **3.19** | ✅ ≥3 |
| `cat.*.solid` ikon | `cat.*.soft` | **3.90 – 9.66** | ✅ ≥3 |
| `cat.*.solid` | `surface` | **4.52 – 12.39** | ✅ ≥3 |
| `text-2` kesikli limit çizgisi (E-16) | `surface` | **5.94** | ✅ ≥3 |
| `primary` sütun dolgusu (E-16) | `well` (sütun oluğu) | **3.18** | ✅ ≥3 |
| `warning` sütun dolgusu (E-16) | `surface` (sütunun sağı/solu) | **3.19** | ✅ ≥3 |
| `cat.*.solid` çubuk dolgusu (E-15) | `groove` (çubuk oluğu) | **4.20 – 4.78** | ✅ ≥3 |
| `ClaySwitch` topuzu `#FFFFFF` | açık track `primary` | **3.68** | ✅ ≥3 (grafik; metin değil) |
| `grad.action` yük çubuğu (E-18) | `well` (oluk) | **3.18** | ✅ ≥3 |
| `#FFFFFF` | `danger-ink` (Sil butonu `pressed`) | **5.75** | ✅ AA |
| **BİLİNEN SINIR** | | | |
| `#FFFFFF` | `primary` | **3.68** | ❌ metin için **YASAK** (§1.6) |
| `success-ink` | `success-soft` | **4.19** | ❌ metin için yasak |
| `warning` sütun dolgusu | `well` (sütunun ÜSTÜNDE kalan oluk) | **2.75** | ⚠️ tek başına <3 — kabul edildi: sütun oluğu tam kaplar, **yanal komşusu `surface` (3.19 ✅)**. WCAG 1.4.11 "adjacent color(s)" koşulu beyaz komşulukla sağlanır. Amberi koyultmak (`warning-deep`, 4.34) mavi sütunlarla aynı ışık yönünü bozardı. |
| `primary` yay | `surface` doğrudan | 3.68 | ✅ ama yay daima `groove` üstünde çizilir |

| **v4'te eklenen çiftler (2026-09-18 · hesaplandı + render edilen pikselden örneklendi)** | | | |
| `#FFFFFF` | `primary-deep` (birincil buton gövdesi, dolu gün kutusu, geçilmiş durak) | **5.37** | AA (K-062 · K-061/1) |
| `#FFFFFF` | `primary-press` (birincil buton `pressed`) | **6.59** | AA |
| `primary-text` | `bg` (yasal bağlantı, E-23) | **5.12** | AA |
| `danger-ink` | `bg` (alan hatası metni, E-22/E-23) | **4.97** | AA |
| `warning-ink` | `warning-soft` (limit dışı gün kutusu) | **5.86** | AA |
| `text-2` | `well` (kayıt yok kutusu) | **5.13** | AA |
| `text-2` | `disabled-bg` (pasif `IconButton` ikonu) | **4.73** | AA |
| **Grafik / pasif (3:1 eşiği ya da kapsam dışı)** | | | |
| `success-ink` | `bg` (E-23 kural onay ikonu) | **4.24** | ✅ grafik — **metin olarak kullanılmadı** |
| `text-3` | `disabled-bg` (yalnız **pasif ve dokunulmaz** gün sayısı, E-24) | **3.40** | ✅ WCAG 1.4.3 pasif bileşenleri kapsam dışı bırakır; etkin hiçbir metin bu çiftle çizilmez |
| **v4 BİLİNEN SINIRLAR** | | | |
| `#FFFFFF` | `grad.action` üst yarısı (`rgb(55,121,229)` → `rgb(54,120,226)`) | **4.18 – 4.25** | ❌ metin için yasak → §1.6 / K-062 |
| `#FFFFFF` | `grad.action` ortası (`rgb(53,117,222)`) | **4.42** | ❌ AA altı |
| `success` `#16A34A` | `bg` | **2.85** | ❌ ham yeşil bu zeminde **metin olarak** kullanılmaz |
| `line` | `bg` | **1.08** | ⚠️ sayfa zemininde hairline ayraç **görünmez** → üretilmez ("ya da" ayracı çizgisiz) |

### 1.10 Renk yasakları (denetimde aranır)

| Yasak | Kural |
|---|---|
| Saf siyah `#000000` | Yasak (`<main>` içinde). Çerçevede serbest. |
| `#FFFFFF` üzerine `#3B82F6` zeminli küçük metin | Yasak — `primary-deep` kullanılır |
| Mor-mavi/indigo-violet gradyan, tam ekran gradyan | Yasak |
| Limit aşımında **kırmızı** | Yasak. Limit dışı = `warning` ailesi |
| `danger` ile limit aşımı anlatmak | Yasak |
| Kategori paletinde `primary` ham hâli (`#3B82F6`) | Yasak — `cat.mavi.solid #306BCA` kullanılır |
| Palet dışı hue | Yasak. Yeni değer önce §1.7 formülüyle türetilir + §1.9'a oranıyla eklenir |
| Doluluğa göre renk değiştiren gösterge (trafik ışığı) | Yasak. Yay limit içinde **her oranda** `grad.arc` |
| Gün/takvim ızgarasında yeşil-kırmızı (ya da yeşil-amber) ikilisi | Yasak — aynı trafik ışığı semantiği. Izgara dili: **mavi = limit altı**, **amber = limit dışı**, **boş çukur = kayıt yok** |
| Gradyan zeminde metin | Yasak (§1.6 · §1.8 · K-062) |

---

## 2. TİPOGRAFİ

### 2.1 🔴 Font dosyaları — `₺` doğrulaması yapıldı

`fontTools` ile ölçüldü (2026-09-12, `projects/trinkow/docs/design/prototip-v3/fonts/LISANS.md`):

| Font | `₺` U+20BA | Türkçe glifler | `tnum` | Karar |
|---|---|---|---|---|
| Montserrat 400/600/700 | ✅ | ✅ | ✅ (+`lnum`,`locl`) | **Alındı** |
| Poppins SemiBold | ✅ | ✅ | ❌ | **Alındı — yalnız başlık** |
| JetBrains Mono | **❌ YOK** | ✅ | ❌ | **PROJEYE ALINMADI** |

| Token | Dosya | Lisans |
|---|---|---|
| `font.ui.regular` | `Montserrat-Regular.ttf` | OFL 1.1 |
| `font.ui.semibold` | `Montserrat-SemiBold.ttf` | OFL 1.1 |
| `font.num.bold` | `Montserrat-Bold.ttf` | OFL 1.1 |
| `font.display` | `Poppins-SemiBold.ttf` | OFL 1.1 |

**Bağlayıcı kurallar:**
1. **Mono font yoktur.** `₺` glifi olmadığı için JetBrains Mono para
   rakamlarında kullanılamaz; başka bir ihtiyacı da yoktu, düşürüldü.
   Denetimde `JetBrains`/`monospace` aranır → bulunmamalı.
2. **Tüm rakamlar Montserrat** + `fontVariant: ['tabular-nums']`
   (web prototipte `font-variant-numeric: tabular-nums`).
3. **Poppins `tnum` taşımaz** → rakam içeren hiçbir `Text`'te kullanılmaz.
   Yalnız `h1` / `h2` başlık rolü.
4. Variable font gömülmez, italik yok, `fontWeight` sayısıyla ağırlık
   üretilmez — ağırlık **dosya seçimiyle** gelir.
5. Toplam **4 dosya** (v2'de 3'tü). Artırılamaz.

### 2.2 Ölçek (10 rol — ara değer üretilemez)

| Token | Font | Ağırlık | Boyut (pt) | Satır y. | Harf ar. | Kullanım |
|---|---|---|---|---|---|---|
| `hero` | Montserrat | 700 | **56** | 60 | −2.0 | Kahraman gösterge sayısı. Ekranda **1 tane**. Tabular. |
| `display` | Montserrat | 700 | **32** | 38 | −1.0 | Tutar girişi, kart içi büyük sayı. Tabular. |
| `amount` | Montserrat | 700 | **17** | 24 | −0.2 | Liste tutarı **ve gün sayısı değeri** ("21 gün", E-21 · E-24 özeti). Tabular, sağa hizalı. |
| `h1` | Poppins | 600 | **26** | 32 | −0.6 | Ekran başlığı. Rakam içeremez. |
| `h2` | Poppins | 600 | **19** | 25 | −0.3 | Kart/bölüm başlığı. Rakam içeremez. |
| `body` | Montserrat | 400 | **16** | 24 | 0 | Gövde, liste birincil satır. |
| `body-strong` | Montserrat | 600 | **16** | 24 | 0 | Buton etiketi, vurgulu gövde. |
| `label` | Montserrat | 600 | **13** | 18 | +0.2 | Etiket, çip, sekme adı, gösterge altı etiket. |
| `caption` | Montserrat | 400 | **13** | 18 | 0 | Tarih, ikincil satır, hata metni. |
| `micro` | Montserrat | 400 | **12** | 16 | +0.2 | Adım sayacı, yasal metin. **Mutlak alt sınır.** |

İzinli punto: **12 · 13 · 16 · 17 · 19 · 26 · 32 · 56**.

### 2.3 Tipografi kuralları

| Kural | Değer |
|---|---|
| Kahraman sayı / etiket oranı | **≥ 4×** (56 ↔ 13) |
| Minimum punto | **12** |
| Uppercase / `textTransform` | **Kullanılmaz** (Türkçe `i/İ`) |
| İtalik | Kullanılmaz |
| Para tutarı | `tabular-nums` zorunlu (Montserrat) |
| Para biçimi | `1.250,50 ₺` — binlik nokta, kuruş virgül, simge sonda, tek boşluk. Liste ve kahraman sayıda kuruş yok. |
| `hero` rolünde `₺` | 56pt değil **32pt** (`display` ölçüsü), taban çizgisine hizalı, sayıyla aynı renk. Gerekçe: yayın iç alanı 198px; `1.250 ₺` 56pt'de sığmaz. Yalnız `hero` rolüne özgüdür. |
| Negatif tutar | `-60 ₺` yazılmaz → `60 ₺ limit dışı` |
| `TL` yazımı | Kullanılmaz, `₺` |
| Arayüz cümlesi | En fazla 12 kelime |
| Ünlem `!` | **Yasak** |
| Emoji | **Yasak** (tüm yüzeyler) |
| Teknik açıklama (depolama/mimari) | **Yasak** |
| Marka adı | Yalnız `Trinkow`, ek kesme işaretiyle |
| **Üçüncü taraf düğme etiketi** (K-057/2) | Kural dışı: "Apple ile Devam Et" ve "Google ile devam et" sağlayıcının yerelleştirmesidir — kısaltılamaz, yeniden yazılamaz, büyük/küçük harf düzeni değiştirilemez. "Buton 1-3 kelime, fiil önce" kuralı bu iki etikette geçmez. |

Metinlerin tek kaynağı: `projects/trinkow/docs/content/metinler.md`.

---

## 3. SPACING — DESIGN.md'den birebir

| Token | Değer (pt) |
|---|---|
| `space.1` | 4 |
| `space.2` | 8 |
| `space.3` | 12 |
| `space.4` | 16 |
| `space.5` | 24 |
| `space.6` | 32 |

**Taban 4pt. Bu altı değerin dışında boşluk kullanılamaz** (v2'deki
20/48/64 düşürüldü — DESIGN.md skalası 4/8/12/16/24/32).

| Uygulama | Değer |
|---|---|
| `screen-padding-x` | **16** — tüm ekranlarda sabit |
| Bölümler arası dikey boşluk | 24 |
| Kart içi iç boşluk | 16 (kahraman kart 24) |
| Kartlar arası dikey boşluk | 12 |
| Liste satırları arası | 8 (clay'de satırlar ayrı kabarık yüzeydir, hairline değil) |
| Safe area üst / alt | `insets.top` / `insets.bottom` (home indicator) |
| Yüzen sekme çubuğu yan boşluğu | 16 |
| İkon ↔ metin (buton içi) | 8 |
| Etiket ↔ girdi | 8 |
| Çipler arası | 8 |

### 3.1 DİKEY RİTİM SETİ — **her değerin tek bir işi vardır**

> Bu tablo bağlayıcıdır. Aynı işi yapan ikinci bir boşluk üretilemez.
> Denetim: üç ekranda da yalnız bu değerler görünmelidir.

| Değer | Tek işi | Nerede |
|---|---|---|
| **4** | Aynı nesnenin iki satırı | Tutar ↔ "limit dışı" · çubuk ↔ "aylık / limit" satırı |
| **8** | Başlık ↔ gövde · etiket ↔ girdi · alan ↔ satır içi mesajı · aynı grubun tekrarlayan öğeleri | Kart başlığı ↔ içeriği · liste satırları arası · seçenek kartları arası · çipler arası · tuş takımı satırları arası · kaydırılan içerik ↔ sabit alt blok |
| **12** | Kartın **ya da formun** İÇİNDE iki bağımsız blok | Kategori satırları arası · metin ↔ eylem butonu · tuş takımı ↔ Kaydet · **iki etiketli form alanı arası** · **"ya da" ayracının iki yanı** (E-22/E-23) |
| **16** | **İç boşluk** (padding) — dikey ritim değil | Kart iç boşluğu · ekran kenar boşluğu (yatay) · sekme çubuğu yan boşluğu |
| **24** | **Ekran düzeyinde** iki bağımsız blok · içerik alt boşluğu | Bölümler arası · ekran düzeyindeki kartlar arası · kaydırılan içeriğin sonu |

| Ekran çerçevesi rolleri | Değer |
|---|---|
| Ekran kenar boşluğu (yatay) | **16** — üç ekranda da aynı |
| Ekran başlığı: üst / alt | **8 / 16** (`.ekran-basi`) |
| Kart iç boşluğu | **16** — istisnasız (kahraman kart dahil; v3.0'daki 24 kaldırıldı) |
| İçerik alt boşluğu | **24** — sekme çubuğu/sabit alt blok kaydırma alanının DIŞINDADIR, bu yüzden telafi payı gerekmez |
| Sabit alt blok üst boşluğu | **8** (`.alt-sabit`) · altında ayrıca home indicator 28 vardır, ikinci bir boşluk eklenmez |

**Ölçüldü (390×844, headless Chromium, 12 durum):** kaydırma alanında satır/nesne
ortasından kesilen eleman **yok**. Tek kasıtlı kesme: E-10 "limit dışı"
durumunda Kategori limitleri kartı **başlık ile ilk satır arasındaki 8'lik
boşlukta** kesilir — kaydırma ipucudur, nesne dilimlenmez.

### 3.2 KABUK (bölge [A]) ÖLÇEĞİ — **RN'e kodlanmaz**

Prototip sahnesi (telefon çerçevelerinin dizildiği masaüstü sayfa) ekran
içeriği değildir. Yalnız burada iki değer daha kullanılabilir:

| Token | Değer | Nerede |
|---|---|---|
| `shell.7` | **48** | `.sahne` satırlar arası |
| `shell.8` | **64** | `body` alt boşluğu |

Cihaz çerçevesi 12pt kalındır; **ekranın kendisi tam 390×844** olsun diye
`.device` dış ölçüsü 414×868'dir.

### 3.3 NEGATİF OLUK TELAFİSİ — yeni boşluk değeri değildir

Sarmalayan satır/ızgara kaplarında çocukların gutter'ı kabın dışına taşar;
kap bunu **aynı değerin negatifiyle** geri alır. İzinli: **−4** ve **−8**.
Başka negatif marj üretilemez.

| Kap | Çocuk gutter | Kap telafisi |
|---|---|---|
| `.tus-satir` (tuş takımı) | `margin: 0 4px` | `−4` |
| `.kat-sec` (kategori ızgarası) | `padding: 4px` | `−4` |
| Onboarding adım çubuğu | ardından `w8` | `−8` |
| `.gun-ag` (E-21 gün ızgarası · `StreakDayGrid`) | `margin-right/bottom: 8` | `−8` |

---

## 4. RADIUS — tek kural: eleman tipinden türer

> Tasarımcı radius seçmez; elemanın **tipine** bakar. Clay dili yüksek
> yarıçap ister; aile **8'in katları** üzerinden tek ailedir.

| Token | Değer | Nerede |
|---|---|---|
| `radius.hero` | **32** | Kahraman kart, bottom sheet üst köşeleri, tam genişlik ekran kartı |
| `radius.card` | **24** | Kart, toast, modal, yüzen sekme çubuğu dış köşesi |
| `radius.tile` | **16** | Küçük kutu, ikon kabı, metin girişi, çip dışı kutucuk |
| `radius.pill` | **999** | Buton, çip, ilerleme çubuğu, segment |
| `radius.circle` | yükseklik ÷ 2 | FAB, avatar, gösterge topuzu, kategori noktası |
| `radius.arc` | `strokeLinecap: 'round'` | Yay/çubuk uçları |
| Odak halkası | eleman radius + **4** |  |

**İzinli değerler: 16 · 24 · 32 · 999 · 0** (+ odak halkası 20/28/36).
**Yasak:** 4 / 6 / 8 / 10 / 12 / 14 / 18 / 20 / 28 gibi serbest değerler.

---

## 5. 🔴 CLAY ELEVATION — gölge sistemi + RN karşılıkları

> Claymorphism'in kalbi burası. Gölge **dekorasyon değil**, yüzeyin
> *hacmi*: dış gölge yüksekliği, iç gölge kabarıklığı anlatır.
>
> **PM'in doğruladığı RN gerçeği:** React Native `boxShadow` prop'u
> **inset dahil** destekleniyor, ancak **yalnız New Architecture**'da;
> outset **Android 9+**, **inset Android 10+**, iOS sorunsuz. Birden
> fazla gölge virgülle birleştirilebilir — clay için zorunlu.
>
> **frontend-developer için:** aşağıdaki `boxShadow` dizeleri React
> Native'e **birebir** yazılır (`style={{ boxShadow: '...' }}`).
> Eski `shadowColor/shadowOffset/...` API'si clay'i **üretemez**
> (tek katman + inset yok). Bu yüzden New Architecture şarttır.

### 5.1 Seviyeler

| Token | Katman | `boxShadow` (RN'e birebir) | Nerede |
|---|---|---|---|
| `clay.raised` | **4** | `0 8px 16px -4px rgba(28,57,142,0.16)`, `0 2px 4px -1px rgba(28,57,142,0.10)`, `inset 0 -5px 8px -4px rgba(28,57,142,0.14)`, `inset 0 5px 8px -4px rgba(255,255,255,0.95)` | Kart, liste satırı, kategori kutusu, çip |
| `clay.raised-lg` | **4** | `0 16px 32px -8px rgba(28,57,142,0.22)`, `0 4px 8px -2px rgba(28,57,142,0.12)`, `inset 0 -8px 12px -6px rgba(28,57,142,0.16)`, `inset 0 8px 12px -6px rgba(255,255,255,0.98)` | Kahraman kart, bottom sheet, yüzen sekme çubuğu, toast |
| `clay.pressed` | **3** | `0 1px 2px 0 rgba(28,57,142,0.10)`, `inset 0 3px 6px -2px rgba(28,57,142,0.20)`, `inset 0 -2px 4px -2px rgba(255,255,255,0.60)` | **Her** basılı etkileşimli yüzey |
| `clay.sunken` | **2** | `inset 0 3px 6px -2px rgba(28,57,142,0.18)`, `inset 0 -2px 3px -2px rgba(255,255,255,0.80)` | Oluk (`groove`), metin girişi kuyusu, segment track, ilerleme oluğu |
| `clay.action` | **4** | `0 8px 16px -4px rgba(47,104,197,0.42)`, `0 2px 4px -1px rgba(47,104,197,0.28)`, `inset 0 -4px 8px -3px rgba(28,57,142,0.34)`, `inset 0 4px 8px -3px rgba(255,255,255,0.42)` | Birincil buton, FAB — gölge zeminin rengini alır |
| `clay.action-pressed` | **3** | `0 2px 4px -2px rgba(47,104,197,0.30)`, `inset 0 4px 8px -2px rgba(28,57,142,0.42)`, `inset 0 -2px 4px -2px rgba(255,255,255,0.22)` | Birincil buton / FAB `pressed` |

### 5.2 Kurallar

| Kural | Değer |
|---|---|
| Gölge rengi | **Daima `rgba(28,57,142,α)`** (= `text` tonu). Saf siyah gölge **yasak** — clay'i çamura çevirir. |
| Renkli gölge | Yalnız `clay.action` (buton zemininin kendi rengi). Başka renkli glow yasak. |
| Katman sayısı | Kabarık yüzey **4**, basılı **3**, çukur **2**. Beşinci katman üretilmez. |
| İç gölge (inset) | Clay'de **zorunlu** — tek outset gölge clay değil, "yumuşak kart"tır (v1/v2'nin hatası). |
| Gölgeli yüzey şartı | Radius ≥ 16 ve zemin `surface` / `primary-deep` olmalı. |
| Hairline `line` | Gölgenin **yerine geçmez**; yalnız liste içi mantıksal ayraç. |
| Android < 10 geri düşüşü | Inset desteklenmiyorsa: outset katmanları kalır + yüzeye `grad.clay-face` üst parlaması eklenir. Görsel hiyerarşi korunur, hacim zayıflar. Bu **kabul edilmiş** bir bozulmadır. |
| `elevation` (eski Android API) | Kullanılmaz — `boxShadow` ile birlikte çift gölge üretir. |

### 5.3 Kabarıklığın ikinci bileşeni: yüzey parlaması

Her `clay.raised*` yüzeyin üst %45'inde `grad.clay-face` (§1.8 #4)
uygulanır. Gölge + parlama birlikte "3B kabarık" hissi verir; ikisinden
biri eksikse yüzey düz görünür.

---

### 5.4 SEÇİM DİLİ ve DOLGU DİLİ — **halka yoktur**

> Kaynak: K-040 → K-045 → K-054/6 → K-061/2. Bu üründe seçili durum
> **halkayla anlatılmaz**; `stil.css`'te 2pt `inset` halka kalmadı.
> Tek cümlelik kural: **seçimde derinlik, gün ızgarasında dolgu.**

| Dil | Görünüm | Anlamı | Nerede |
|---|---|---|---|
| **Seçim dili** | Zemin `primary-soft` + `clay.sunken`; yüzeyde ikon kabı varsa **tersine kabarır** (`groove`+sunken → `surface`+`clay.raised`) | *"Bunu ben seçtim, geri alabilirim."* | Çip, `OptionCard`, kategori ızgarası, segment, sıklık çipleri |
| **Dolgu dili** | Zemin **düz `primary-deep`** + kabartma (beyaz sayı 5.37 ✅, K-062) | *"Burada bir olgu var"* — kullanıcının seçimi değil, **verinin durumu** | Dolu gün kutusu (E-21/E-24), geçilmiş durak, maaş günü seçimi (E-03) |

| Kural | Değer |
|---|---|
| İki dil aynı elemanda birleşmez | `.gun-kutu.altinda` (veri) ve `.gun-kutu.secili` (seçim) **ayrı sınıf** olarak durur |
| Renk tek kanal değildir | Seçim ayrıca `accessibilityState={{selected:true}}`; veri durumu ayrıca `accessibilityLabel` ile söylenir (WCAG 1.4.1) |
| Bilinen sınır | Seçili kart `bg #E6EFFE` üstünde `primary-soft #E4EEFE` ile durur — iki renk neredeyse aynı. Ayrımı **derinlik + ikon kabarması** taşır. Gerekirse çözüm "seçili kart zeminini `surface`'e çıkarmak"tır, **halka değil** |
| Üçüncü bir "seçili" dili | Üretilemez |

---

## 6. DOKUNMA HEDEFİ VE ERİŞİLEBİLİRLİK

| Kural | Değer |
|---|---|
| Minimum dokunma hedefi | **44 × 44 pt** — görsel eleman küçükse `hitSlop` ile tamamlanır |
| Odak halkası | 2pt `primary-text #2C62B8` dış çizgi, elemandan 2pt boşlukla, radius + 4. Koyu zeminde `#FFFFFF`. **Kaldırılmaz.** |
| `pressed` durumu | Her etkileşimli eleman için **zorunlu** (hover yoktur) → `clay.pressed` / `clay.action-pressed` + zemin tonu |
| İkon-buton etiketi | `accessibilityLabel` Türkçe ve fiille |
| Pasif eleman | `accessibilityState={{ disabled: true }}` |
| Kahraman gösterge | `accessibilityRole="progressbar"` + `accessibilityValue={{min,max,now}}` + `accessibilityLabel="Günlük limit kullanımı"` |
| Kategori | Renk tek başına bilgi taşımaz: **renk + ikon + metin** |
| Reduce motion | Açıkken tüm süreler **0ms** |
| Opaklık ile pasiflik | **Kullanılmaz** — pasif durum renkle + `clay.sunken` ile verilir |
| Pasif `IconButton` (E-10 gün okları) | Zemin `disabled-bg`, gölge `clay.sunken`, ikon `text-2` (4.73 ✅). Pasif ok **gizlenmez** — gizlenen ok düzeni kaydırır |
| Pasif `DayBox` (E-24 seçilemez gün) | Zemin `disabled-bg` + `clay.sunken` + sayı `text-3` (3.40 · §1.9 pasif istisnası). Gölge **kaldırılmaz** |
| Pasif `button.secondary` (E-22 "Yeniden gönder") | Zemin `disabled-bg`, metin `text-2`, gölge `clay.sunken`; gerekçe satırı altında yazılır |

---

## 7. BİLEŞEN ÖLÇÜLERİ

### 7.1 Buton (**dört** varyant)

| Varyant | Yükseklik | Radius | Zemin | Metin | Gölge | Pressed |
|---|---|---|---|---|---|---|
| `button.primary` | **56** | 999 | **düz `primary-deep #2F68C5`** (gradyan YOK — K-062) | `#FFFFFF` / `body-strong` (5.37 ✅) | `clay.action` | zemin düz `primary-press` (6.59 ✅), `clay.action-pressed` |
| `button.secondary` | **52** | 999 | `surface` | `text` / `body-strong` | `clay.raised` | zemin `well`, `clay.pressed` |
| `button.ghost` | **44** | 999 | şeffaf | `text-2` / `body-strong` | yok | zemin `well`, `clay.pressed` |
| `button.social` (K-057/2) | **56** | 999 | **palet dışı — sağlayıcının**: Apple `#000000` · Google `#FFFFFF` + 1px `#747775` kontur | Apple `#FFFFFF` · Google `#1F1F1F`, `body-strong` | `clay.raised` | Apple `#1A1A1A` · Google `#F2F2F2` (+ `clay.pressed`) |

| Ortak | Değer |
|---|---|
| Yatay iç boşluk | 24 (`ghost` **16** — çerçevesiz olduğu için dar durur) |
| Metin | Tek satır, kırpılmaz; sığmazsa metin kısaltılır, buton büyümez |
| Ekran başına birincil buton | **En fazla 1** |
| İkon | Solda 20pt, metinle arası 8 |
| `disabled` | Zemin `disabled-bg`, metin `text-2`, gölge `clay.sunken`. **Opaklık yok.** `primary`, `secondary` (E-22 "Yeniden gönder") ve `ghost` için aynı |
| `loading` | Metin "Kaydediliyor" + sağda 20pt spinner, genişlik sabit, `disabled` |
| `scale` animasyonu | **Yok** — geri bildirim gölgenin çökmesiyle verilir |
| `button.social` istisnası | **Kap bizim, içerik sahibinin.** Ölçü/geometri/gölge buradan; dolgu, logo (20pt + 8 boşluk) ve etiket sağlayıcının kılavuzundan. iOS'ta Apple düğmesi `expo-apple-authentication`'ın kendi bileşenidir (biz çizmeyiz). Ham değerler `<main>` içinde değil, sınıf olarak `stil.css`'te durur (§12 istisnası) |

### 7.2 Kart

| Özellik | Değer |
|---|---|
| Zemin | `surface` + `grad.clay-face` |
| Radius | 24 (kahraman kart / sheet 32) |
| Kart İÇİNDE iki blok arası | 12 |
| Gölge | `clay.raised` (kahraman/sheet: `clay.raised-lg`) |
| Kenarlık | Yok |
| İç boşluk | **16 — istisnasız** (v3.1: kahraman karttaki 24 kaldırıldı) |
| Kartlar arası | **24** (ekran düzeyinde iki bağımsız blok — §3.1) |
| `pressed` (tıklanabilirse) | `clay.pressed` + zemin `groove` |
| Yasak | "Daire içinde ikon + başlık + tek cümle" 3'lü özellik kartı |

### 7.3 Liste satırı (`FlatList`)

| Özellik | Değer |
|---|---|
| Minimum yükseklik | **68** |
| Yapı | Her satır **ayrı kabarık yüzey** (`surface`, radius 16, `clay.raised`), aralarında 8 |
| Dikey / yatay iç boşluk | 12 / 16 |
| Sol kategori kabı | 44 × 44, radius 16, zemin `cat.*.soft`, `clay.sunken`, içinde 20pt ikon `cat.*.solid` |
| Birincil satır | `body` / `text` |
| İkincil satır | `caption` / `text-2` |
| Sağ tutar | `amount` / `text`, sağa hizalı, tabular |
| Gölge | `clay.raised` (v1/v2'de yoktu — clay'de satır da bir nesnedir) |
| Limit dışı satır | Zemin `warning-soft`, tutarın altında `caption` / `warning-ink` "limit dışı". Ünlem/üstü çizili/kırmızı yok. |
| Kaydırarak silme | Sağa kaydırma → `danger` zeminli "Sil". Tek harcama: **onay yok**, 6 sn geri al toast'ı. Taksitli kayıt: onay diyaloğu (K-029). |

### 7.4 Metin girişi

| Özellik | Değer |
|---|---|
| Yükseklik | **56** · Radius **16** · Zemin `well` · Gölge `clay.sunken` |
| Kenarlık (normal) | Yok — çukurluk gölgeyle anlatılır |
| Kenarlık (odaklı) | 2pt `primary-text #2C62B8` + `clay.sunken` |
| Kenarlık (hatalı) | 2pt `danger #DC2626` + altında `caption` / `danger-ink` hata metni, 8 boşlukla |
| Etiket | Girişin üstünde `label` / `text-2`, arası 8. Placeholder'a gömülmez. |
| Placeholder | `text-3` |
| Tutar alanı | **Sistem klavyesi kullanılmaz** — §7.11 kil tuş takımı. Kuyu `well` + `clay.sunken`, tutar `hero` (56pt) ortalı, `₺` `display` (32pt) `text-2`, imleç 3pt `primary`. |
| "Kaydet" konumu | Tuş takımının **altında sabit** — `KeyboardAvoidingView` gerekmez, sistem klavyesi hiç açılmaz. |
| Harcama girişi hedefi | **En fazla 3 dokunuş** |

### 7.5 Kahraman gösterge (clay dairesel yay)

| Özellik | Değer |
|---|---|
| Çizim | `react-native-svg` + kabarık DOM/View katmanları |
| Kahraman kart | Tam genişlik, radius 32, zemin **`primary-soft`**, `clay.raised-lg` — mavi kil panel |
| Dış kabarık disk | **224** çap (v3.1: 296 ekranın %76'sıydı, altındaki kartı eziyordu), `surface`, `clay.raised-lg`. Ortadaki boş alan **156px** |
| Oluk | Merkez yarıçapı **86** (78..94), kalınlık **16** (296'daki 22'nin orantılı karşılığı), renk **`well #E6EFFE`** (dolguyla 3.18:1 ✅). Çukurluk iki ince kenar yayıyla: dış kenar `rgba(28,57,142,0.13)` 2.5pt (r 92.5), iç kenar `rgba(255,255,255,0.95)` 2.5pt (r 79.5) |
| Yay açıklığı | **270°**, boşluk altta, başlangıç saat 7 |
| Dolgu | `grad.arc` · kalınlık 16 · `strokeLinecap: 'round'` — **doluluktan bağımsız** |
| Dolgu parlaması | Dolgunun üstüne 5pt `rgba(255,255,255,0.30)` ikinci yay (yuvarlaklık hissi) |
| Topuz | 26pt `surface` daire (r 13) + 4pt `primary-deep` halka + altına kaydırılmış `rgba(28,57,142,0.18)` gölge dairesi + üstte `rgba(255,255,255,0.55)` parlama yayı. **Zorunlu.** |
| Ortada | `hero` 56pt sayı (tabular) + altında `label` 13pt `text-2` |
| **Uzun tutar** | İç alan 156px. Ölçüldü: `1.250 ₺` = 137px ✅, `12.500 ₺` = 163px ❌. Sayı **6+ karakterse** rol bir basamak iner: `hero` 56 → `display` 32, `₺` 32 → `amount` 17. §7.11'deki kuralla aynıdır; keyfi ara punto üretilmez. |
| Eşik işareti | **Yok.** Oluğun kendisi 0→%100 aralığını temsil eder; ayrı bir çentik gereksiz işaret gürültüsüdür. |
| Taşma yayı | Merkez yarıçapı **102** (ana yayın 8pt dışında, diskten 6 içeride), 8pt kalınlık, `grad.arc-over`, saat 12'den saat yönünde, zemini `surface` (3.19:1 ✅) |
| Limit dışı | Ana yay %100 dolu kalır + taşma yayı çıkar + `hero` sayı `warning-ink` olur + altında "limit dışı" |
| Animasyon | 250ms ease-out (DESIGN.md 150–250ms), sayı eş zamanlı sayar |
| %100+ | Renk **kırmızıya dönmez**, yanıp sönmez, titremez, ikon değişmez |

**Mini gösterge:** çap **56**, kalınlık 8, topuz yok, dolgu `cat.*.solid`,
oluk `groove`, ortada `label`. Ekranda en fazla **3 tane**.
**Kategori çubuğu:** yükseklik 12, radius 999, oluk `groove` + `clay.sunken`,
dolgu `cat.*.solid`, taşma `warning`.

### 7.6 Çip

| Özellik | Değer |
|---|---|
| Yükseklik | **40** → radius 999 (`hitSlop` ile 44) |
| Pasif | Zemin `surface`, `clay.raised`, `label` / `text-2` |
| Seçili | Zemin `primary-soft` (kategori çipi: `cat.*.soft`), `clay.sunken`, metin `text`, solda 8pt `solid` nokta |
| `pressed` | `clay.pressed` + zemin `well` |
| Yatay iç boşluk | 16 · nokta ↔ metin 8 |
| Aralarında | 8 |
| Onay ikonu | Yok — seçili durum çukurlukla anlaşılır |
| **Halka (ring)** | **Yoktur.** Seçili çipte kenarlık/halka (`inset ring`, `outline`) kullanılmaz; seçim yalnız yüzey tonu (`primary-soft` / `cat.*.soft`) + `clay.sunken` çukurluk + metin rengiyle verilir (K-040). Aynı kural **kategori ızgarası** (`kat-sec-kutu.secili`) için de geçerlidir. |
| **Maks. genişlik** | **240** · çip `flexShrink: 0` — yatay şeritte asla daralmaz |
| **Taşma davranışı** | Çip **tek satırdır, sarmaz** (`numberOfLines={1}`). Ad bölümü maks. **120** genişlikte `ellipsizeMode="tail"` ile kırpılır; tutar bölümü `flexShrink: 0` ile **hiç kırpılmaz** |
| **Değişmez kural** | **`₺` asla kırpılmaz.** Tutar okunamayan çip karar vermeye yaramaz; kırpılacak tek şey addır |
| Tam ad nerede | Çipe dokunulduktan sonra ürün alanında tam görünür · `accessibilityLabel` daima **tam** adı taşır ("{ad}, {tutar}") |

> **Neden kural:** ürün adları uzundur ("Marlboro Touch Blue 20'lik").
> Sarma serbest bırakıldığında 40pt yüksekliğindeki çipte metin üç satıra
> çıkıp **üstten kırpılıyordu** (2026-09-12 render bulgusu). RN'de bu
> `Text` sarmasıdır, CSS hilesiyle değil `numberOfLines`/`flexShrink` ile
> çözülür. Kural **tüm çip türleri** için geçerlidir: sık alınanlar,
> kategori, taksit sayısı, tarih.

### 7.7 Yüzen sekme çubuğu + merkez eylem

| Özellik | Değer |
|---|---|
| Konum | Yüzen: alttan `insets.bottom + 8`, yanlardan 16 |
| Yükseklik | **68** · radius 999 · zemin `surface` · gölge `clay.raised-lg` |
| Sekme sayısı | Faz 1: **3** + merkez FAB |
| Sekme içerik kutusu | 64 × 56 (dokunma hedefi 44'ün üstünde) |
| İkon / etiket | 24pt / `label` 13pt — **etiketsiz ikon yok** |
| Aktif | `primary-text` + SemiBold + ikon arkasında 40pt `primary-soft` daire (`clay.sunken`) |
| Pasif | `text-2` + Regular |
| FAB | **64 × 64 daire**, `grad.action`, 28pt `#FFFFFF` ikon, `clay.action`, bar üst kenarından **16** yukarı taşar (alan yüksekliği 68 + 16 = **84**), bar iç boşluğuyla hizalı olarak sağdan **8** |
| FAB `pressed` | Zemin `primary-press` + `clay.action-pressed` |
| FAB etiketi | `accessibilityLabel="Harcama ekle"` |

### 7.8 Boş durum

| Özellik | Değer |
|---|---|
| Sıra | Boş clay yay illüstrasyonu → `h2` → `body` tek satır → birincil buton |
| İllüstrasyon | **176pt** kabarık disk + oluk r 70 / kalınlık 12 (`groove` + `clay.sunken`), dolgu yok, topuz yok, taşma yayı yok. İç alan 128px — `hero` sayı yerinde kalır (limitin tamamı duruyor). |
| Aralar | **12 / 8 / 12** (§3.1 — kart içi blok / başlık↔gövde) |
| Yasak metin | "Henüz veri yok" · teknik açıklama |

### 7.9 Toast

| Özellik | Değer |
|---|---|
| Zemin | `surface`, radius 24, iç boşluk 16, gölge `clay.raised-lg` |
| Sol gösterge | 8pt daire: `primary` (bilgi) · `warning` (limit dışı) · `danger` (yıkıcı) |
| Konum | Üstte, `insets.top + 8` |
| Süre | **4 sn** (bilgi) · **6 sn** (geri al taşıyan) — otomatik kaybolur · eylem hedefi 44 × 44 |
| **Geri alma penceresi** | **6 sn** — toast'ın ömrüyle **birebir aynı**. Görünmeyen geri alma süresi oluşturulmaz: düğme kaybolduğu an işlem kalıcıdır. |
| Geri al nerede | **Tek harcama silme** (onay diyaloğu yoktur) · hızlı tekrar. **Taksit serisi silmede yoktur** — o akış onay diyaloğuyla korunur (K-029). |
| Yasak | Limit aşımını ekran ortasında modal ile bildirmek |

### 7.10 Yükleniyor (skeleton)

| Özellik | Değer |
|---|---|
| Yapı | Gerçek düzenin kabarık kutuları yerinde durur, içleri `clay.sunken` çukur bloklara döner |
| Renk | Blok zemini `well`, animasyon yok (yalnız 250ms fade-in) |
| Yasak | Parıldayan (shimmer) süpürme, dönen spinner ile tam ekran kaplama |
| Spinner | Yalnız buton içinde (`loading`) |

### 7.11 Kil tuş takımı (tutar girişi — sistem klavyesi yerine)

| Özellik | Değer |
|---|---|
| Neden | Clay dili fiziksel tuş ister; sistem klavyesi platforma göre zıplar, 3 dokunuş hedefini bozar, `₺`/virgül düzeni Türkçe klavyede değişir. |
| Düzen | 4 satır × 3 sütun: `1 2 3` / `4 5 6` / `7 8 9` / `,` `0` `⌫` |
| Tuş | Yükseklik **56**, radius **16**, zemin `surface` + `grad.clay-face`, gölge `clay.raised`, metin Montserrat 600 / 26pt |
| Tuş `pressed` | Zemin `groove`, gölge `clay.pressed` |
| Tuşlar arası | Yatay 8 (`margin: 0 4px`, satır kabı `-4px` negatif kenar), dikey 8 |
| Silme tuşu | Lucide `delete`, 24pt, `accessibilityLabel="Son rakamı sil"` |
| Nokta tuşu | **Yok** — binlik ayracı otomatik eklenir, kullanıcı yalnız `,` yazar |
| Nerede | E-11 Harcama ekle · E-02 Onboarding günlük limit · E-17 Limitler |
| Tutar 7 karakteri aşarsa | `hero` (56pt) → `display` (32pt). Kuyu yüksekliği sabit kalır, düzen kaymaz. |

> **K-042:** 8+ karakterli tutarda tip ölçeği `hero` → `display` iner.
> Prototip v3'ün bazı örnek ekranlarında bu görsel olarak yansımıyordu —
> **kural geçerlidir, prototip değil.** Kod (`AmountWell.tsx`) ve
> prototip üreteci bu kurala göre düzeltildi.

### 7.12 Tur E bileşenleri (E-15 · E-17 · E-18 · E-19)

| Bileşen | Değer |
|---|---|
| `ValueWell` (dokunulabilir değer satırı) | Yükseklik **68** (iç boşluk 12/16) · radius 16 · zemin `well` · `clay.sunken` · sağda değer (`amount`) + 20pt `chevron-right` ya da `pencil`. `pressed`: `groove` + `clay.pressed`. Hatalı: + 2pt `danger` |
| `SettingRow` (kabarık karar satırı) | Minimum **68** · iç boşluk 12/16 · radius 16 · `surface` + `clay.raised`. Başlık `body-strong`, altında 4 boşlukla `caption` |
| `ClaySwitch` | Track **56 × 32**, radius 999, iç boşluk 4 · kapalı: `well` + `clay.sunken` · açık: `grad.action` + `clay.action` · topuz **24pt** daire `surface` + `clay.raised`. Geçiş 150ms. **Platform `Switch` kullanılmaz.** Dokunma hedefi satırın tamamı |
| `DayBox` (E-15 sol sütun) | **44 × 44**, radius 16, `well` + `clay.sunken`; üstte gün `label`, altında ay kısaltması `micro`/`text-2` |
| `LoadBar` (E-18 ay yükü) | Yükseklik **12**, radius 999, oluk `well` + `clay.sunken`, dolgu `grad.action`. Satır düzeni: ay adı 56pt sabit · çubuk esner · tutar 88pt sabit sağa hizalı |
| `PushHeader` | `.ekran-basi` ile aynı ölçü (üst/alt 8/16): solda 44pt geri `IconButton`, ortada `h1` tek satır, sağda eylem ya da 44pt denge kutusu |

**Kural:** bu altı bileşen yeni bir ölçü ailesi açmaz — hepsi mevcut
44/56/68 yükseklik, 16/24/999 radius ve §5.1 gölge katmanlarıyla kurulur.

### 7.13 v4 bileşenleri (E-10 · E-21 · E-24 · E-22/E-23 · E-25/E-26 · E-11)

> Aynı kural burada da geçerli: **yeni ölçü ailesi açılmadı.** Hepsi
> 8/12/24/32/44/56/68/96 ölçüleri ve 16/24/32/999 radius ile kurulur.

| Bileşen | Değer | Dayanak |
|---|---|---|
| `MilestoneRail` durağı | Daire **44** · yol **24 × 8** (radius 999) · geçilmiş durak düz `primary-deep` + beyaz `label` | T-1 · K-062 |
| `StreakDayGrid` | Kutu **44** (mevcut `DayBox`, sayı-only varyant) · 7 sütun `flexWrap` · gutter 8, kap telafisi −8 (§3.3) · lejant karesi **24**, radius 16 | T-1 |
| Kutlama kartı (`MilestoneOverlay`) | Disk **96** (mevcut hata dairesi ölçüsü) · kart radius **32** + `clay.raised-lg` · üst banda `absolute`, scrim yok | K-048 |
| `MonthGrid` (E-24) | Satır = 7 eşit hücre (`flex: 1`, kart içi 326 → hücre 46) · hücre içi kutu **44** · kutu altı bugün noktası **8** · satır arası **8**. **CSS grid yok** | T-1 |
| `MonthNav` | `lib.ay_secici`nin pasif oklu sürümü; uçta ok **gizlenmez**, pasifleşir (§6) | K-049 |
| `PasswordField` sağ yuvası | `TextField`'ın varyantı: 44pt ikon düğmesi, alanın sağ iç boşluğu 16 → **8** | T-2 |
| `Slider` (E-25/E-26) | Oluk **12** (mevcut çubuk kalınlığı) · topuz **32** · satır **44** · dolgu topuzun **merkezinde** biter · üst sınırda topuz `warning-soft` (hata değil) | T-3 |
| `ShareBar` (pay çubuğu) | Tek oluk, 3 segment, aralar **4** — oluk aradan görünür. Segment renkleri: zorunlu `primary-deep` · sosyal `primary` · birikim `success` (K-059/4). **Metin taşımaz** | T-3 |
| `EquationRow` (E-26) | 3 çukur kutu + `÷` `=` işleç sütunları 16 · kutu iç boşluğu **8** (326'ya sığması için; 8 zaten §3 skalasında) · sonuç kutusu kabarık + `primary-soft` | T-3 |
| `ProgressBar` (Katman 2) | Oluk **8** + dolgu (`grad.action`, metinsiz) + yanında `n/8`. **8 segment çizilmez** | T-3 |
| `NeutralIconBox` | **48 × 48** · radius 16 · `primary-soft` + `primary-text`. Daire değil — "daire ikon + başlık" şablonundan kaçınmanın yapısal karşılığı | T-3 |
| `oneri-pul` (öneri etiketi) | İç boşluk 4/12 · radius 999 · `primary-soft` + `clay.sunken` · `label`/`primary-text`. Dokunulamaz; öneri kabul edilince **pul düşer** | K-059/5 |
| Arama alanı (E-11) | Mevcut `.giris` aynen: **56** · `well` · `clay.sunken`. Yeni giriş biçimi üretilmedi | K-050 |
| `son-kullanilanlar-cip` | Ad `max-width: 120`, tek satır, ellipsis; **tutar kırpılmaz** (kırpılan tutar yanlış tutardır) | K-050 |
| `gun-btn` (tutar kuyusu içinde) | Görsel 20-24pt → `hitSlop` ile 44'e tamamlanır. Vurgu `primary-text`/600, basılı `primary-press`. **Amber/kırmızı kullanılmaz** | K-049 |

---

## 8. HAREKET

| Token | Süre | Eğri |
|---|---|---|
| `motion.press` | **150ms** | ease-out |
| `motion.arc` | **250ms** | ease-out |
| `motion.count` | **250ms** | ease-out (yay ile eş zamanlı) |
| `motion.sheet` | **250ms** | ease-out |
| `motion.celebrate.hold` | **700ms** | — (bir animasyon değil, **bekleme**) |
| Reduce motion açık | **0ms** | — |

DESIGN.md §7: 150–250ms, stable easing. Üst sınır aşılmaz.

**Kutlama zaman çizelgesi (K-048 · seri durağı):** giriş 250 (`motion.arc`,
`opacity` 0→1 + `translateY` 8→0) + bekleme **700** + çıkış 250 =
**1.200ms** (K-048'in "≤1.2 sn" sınırı). Tek geçişin üst sınırı yine 250ms;
700 bir geçiş değil, kartın ekranda durduğu süredir. `scale`, spring ve
overshoot yasağı korunur. `reduceMotion` açıkken süreler 0ms, kart yine
1.200ms görünür kalır; dokunma anında kapatır.

**Yasak:** yanıp sönme, titreme, zıplama/spring overshoot, konfeti,
sürekli dönen dekoratif öğe, `scale` basma animasyonu, shimmer.

---

## 9. İKON

| Kural | Değer |
|---|---|
| Set | **Lucide** (`lucide-react-native`, ISC) — tek set. v4'te eklenen 5 glif: `eye` · `eye-off` · `log-out` · `wifi-off` · `mail-check` (K-057/2). Yeni set, yeni boyut, yeni kalınlık **yok** |
| Boyutlar | 24pt (varsayılan) · 20pt (liste/buton içi) · 28pt (FAB). Ara boyut yok. |
| Çizgi kalınlığı | **2.0** (clay'in yumuşak yüzeyine karşı net kontur) |
| Dolgulu ikon | Kullanılmaz |
| Renk | `text` / `text-2` / `primary-text` / `#FFFFFF` / `cat.*.solid` / `warning-ink` / `danger-ink` |
| Emoji | **Yasak** — ayırt edicilik gerekiyorsa ikon |

Kategori ↔ ikon eşleşmesi: §1.4 tablosu.

---

## 10. LOGO

| Token | Değer |
|---|---|
| Kelime markası | `Trinkow` · **Poppins SemiBold** · tracking −2.0% · tek satır |
| Minimum punto | 20pt · uygulama içi maksimum 26pt |
| Monogram | "T" + topuz (v2 geometrisi korunur: 100×100 ızgara, T cap-height 58, baseline y=79, kol x 18→72, kol üstü y=21; topuz çap 18, merkez (78, 26.5)) |
| Monogram rengi | Tek renk (`text` ya da `#FFFFFF`) **veya** iki renk (T `#FFFFFF` + topuz `#3B82F6`) |
| App icon | 1024×1024, saydamlık yok, zemin `grad.action`, T `#FFFFFF` (5.37:1), topuz `#FFFFFF` |
| Splash | Zemin `bg`, ortada wordmark 26pt `text`, "w" sağında topuz `primary`. Animasyon yok. |
| Logoda yasak | Gölge, outline, esnetme, döndürme, `₺` ile harf değiştirme, Montserrat ile dizme, `warning`/`danger` rengi |

---

## 11. FAZ 2 — KARANLIK MOD

**Faz 1'de yoktur.** `useColorScheme()` kullanılmaz, tema değiştirme kodu
yazılmaz, karanlık token üretilmez. Clay'in inset/outset dengesi karanlıkta
**ters çevirmeyle çalışmaz** (beyaz parlama yerine daha açık yüzey tonu
gerekir) — Faz 2'de ayrıca çizilir.

---

## 12. HIZLI DENETİM LİSTESİ (`design-reviewer`)

Tarama **yalnız `<main class="content">` bloğu içinde** yapılır; cihaz
çerçevesi kapsam dışıdır (`agency/reference/open-design-entegrasyon.md`).

### 12.0 Kapsam istisnaları (yalnız bu ikisi — başkası eklenemez)

| İstisna | Kapsam | Gerekçe | Dayanak |
|---|---|---|---|
| **İşletim sistemi çizimleri** | Sistem klavyesi, durum çubuğu, home indicator | Bu yüzeyleri **işletim sistemi çizer**; paletimizi ve ölçeğimizi onlara uygulamak yalan olurdu. Palet/ölçek dışı değerleri (ör. `#D1D4DA` `#1C1C1E` `#ADB3BE` `#3A3A3C` · radius 5 · gap 6) prototipte yalnız bu bölgede geçer | **K-061/6** |
| **Üçüncü taraf marka varlıkları** | Apple/Google oturum açma düğmeleri (`.btn-apple`, `.btn-google`, `.g-*`) ve logoları | Dolgu, logo ve etiket sahibinin kılavuzundan gelir; değiştirmek marka kuralını çiğner. Madde 1 (`#000000`) ve madde 27 (palet dışı hue) bu blokta geçmez | **K-057/2** |

**İstisnanın yeri yapıdadır, kodda değil:** `denetim.py` bu blokları
`/* @denetim-disi: … */` … `/* @denetim-disi-son */` işaretiyle eler ve
**blok sayısını da doğrular** (biri sessizce eklenirse/silinirse bulgu
verir). İstisna ham değerleri `<main>` içine yazılmaz; `stil.css`'te sınıf
olarak durur. Bunların dışında hiçbir yüzey palet/ölçek dışına çıkamaz.

| # | Aranan | Beklenen |
|---|---|---|
| 1 | `#000000` / `rgba(0,0,0` | `<main>` içinde bulunmamalı |
| 2 | `JetBrains`, `monospace`, `font-mono` | Bulunmamalı (`₺` glifi yok) |
| 3 | `Poppins` + rakam aynı elemanda | Bulunmamalı (`tnum` yok) |
| 4 | `Figtree`, `Space Grotesk`, `Inter` | Bulunmamalı (v2 arşiv) |
| 5 | `#FFFFFF` metin + `#3B82F6` zemin | Bulunmamalı → `primary-deep` (§1.6) |
| 5b | Metin taşıyan yüzeyde `grad.action` / `background-image` | Bulunmamalı → düz `primary-deep` (§1.6 · §1.8 · **K-062**) |
| 5c | 2pt `inset` halka ile "seçili" anlatımı | Bulunmamalı → §5.4 seçim dili (K-061/2) |
| 6 | `box-shadow` / `boxShadow` katman sayısı | Kabarık 4 · basılı 3 · çukur 2 (§5.1) |
| 7 | Gölge rengi | Yalnız `rgba(28,57,142,α)` veya `rgba(47,104,197,α)` |
| 8 | `inset` gölge | Her clay yüzeyde **bulunmalı** (yoksa clay uygulanmamış demektir) |
| 9 | `border-radius` değerleri | Yalnız 16, 24, 32, 999, 0 (+ odak 20/28/36) |
| 9b | Dört piksellik yarıçap | İzinli küme dışıdır ve denetim aracından da çıkarıldı — bkz. karar defteri, düzeltme turu hükmü beş. *(Bu satıra rakam yazılmaz: `denetim.py` izinli radius kümesini madde dokuzun satırından okur.)* |
| 10 | `font-size` değerleri | Yalnız 12, 13, 16, 17, 19, 26, 32, 56 |
| 11 | Boşluk değerleri | Yalnız 4, 8, 12, 16, 24, 32 · her biri §3.1'deki tek işinde |
| 11b | İlan edilmemiş boşluk | Bulunmamalı. Kabuk 48/64 yalnız bölge [A]'da (§3.2); negatif marj yalnız −4/−8 oluk telafisi (§3.3) |
| 11c | Kaydırma alanının altında dilimlenen satır/nesne | Bulunmamalı; kesme yalnız bir boşluk bandına düşebilir |
| 12 | `:hover` | Bulunmamalı |
| 13 | `grid`, `::before`, `::after`, `sticky`, `float`, `calc(`, `vh`, `vw` | `<main>` içinde bulunmamalı |
| 14 | Emoji karakteri | Bulunmamalı |
| 15 | `!` (arayüz metninde) | Bulunmamalı |
| 16 | `#DC2626` kullanımı | Yalnız §1.3'teki dört bağlam. Limit aşımı ekranında ve tek harcama silmede bulunmamalı. |
| 17 | Limit aşımı rengi | `#D97706` / `#8A4B04` ailesi olmalı |
| 18 | Kategori rengi `color:` olarak metinde | Bulunmamalı (soft zemin üstüne `text`) |
| 19 | Ekranda birden fazla 56pt | Bulunmamalı |
| 20 | `textTransform: uppercase` | Bulunmamalı |
| 21 | Dokunma hedefi < 44pt | `hitSlop` ile tamamlanmalı |
| 22 | `opacity` ile pasiflik | Bulunmamalı |
| 23 | `useColorScheme` / karanlık mod | Faz 1'de bulunmamalı |
| 24 | Depolama/mimari anlatan arayüz metni | Bulunmamalı |
| 25 | `TRINKOW` / `trinkow` | Yalnız `Trinkow` |
| 26 | `elevation:` (eski Android API) | Bulunmamalı (§5.2) |
| 28 | `keyboardType` / sistem klavyesi çizimi | Tutar girişinde bulunmamalı (§7.11) |
| 29 | SVG `id` çakışması (`gArc`, `gOver`) | Tek sayfada birden çok gösterge varsa id benzersizleştirilir (prototipte hepsi aynı olduğu için görsel etki yok) |
| 27 | Palet dışı hue | Bulunmamalı; her değer §1.7 formülüyle türetilmiş olmalı. İstisna: §12.0 |
| 30 | `stil.css` hex + radius taraması | `denetim.py` ölçütü **bu dosyadır** (§1 palet + madde 9). §13 ARŞİV beyaz listeye girmez |

---

## 13. ARŞİV — **UYGULANMAZ**

### 13.1 v2.0 "Gün Işığı" (2026-09-11 · reddedildi, TUR C)
`bg #F6F4F1` · `surface #FFFCF8` · `surface-2 #EFEAE3` · `line #E6E1DA` ·
`text #17181C` · `text-2 #5A5B63` · `accent #D9661A` · `accent-deep #A8500C`
· `accent-soft #FDEBD8` · `ink #17181C` · `edge #6E3B6B` · `danger #9B2C1F`
· kategori: kahve/yemek/ulaşım/market/fatura/diğer 6 renk · fontlar
Space Grotesk Bold + Figtree Regular/SemiBold · ölçek 56/32/17/26/19/16/13/12
· radius 16/24/28/999 · gölge `elev.1`/`elev.2` tek katman, renk `#3A2A1C`,
inset **yasaktı** · spacing 4/8/12/16/20/24/32/48/64 · Lucide 1.75.

> **v2'nin teşhisi:** gölge tek katman + inset yasağı → yüzeyler "biraz
> yumuşak kart" oldu, hacim yok. v3 bunu §5 ile düzeltiyor.

### 13.2 v1.0 "Defter" (2026-09-11 · reddedildi)
`bg #F4F1EA` · `surface #FFFDF8` · `text #1B1A17` · `accent #14484C` ·
`edge #A24A2A` · `danger #8E2F20` · Source Serif 4 + Public Sans · radius
12/hap · gölge yok · kategori rengi yok.

### 13.3 Yön B "Ölçüm Aleti" (hiç seçilmedi)
`bg #0E1110` · `surface #171B1A` · `text #E8EDEB` · `accent #E8A33D` ·
IBM Plex Sans/Mono · radius 8/4 · Tabler 2.0.

---

## 14. TÜRETİLMİŞ DEĞERLER — **formüllerin tek kaynağı**

> Neden burada: bir sayının tanımı yazılı değilse **iki ekranda iki kez
> kodlanır ve ayrışır** (K-040'ın dersi). Para daima **kuruş cinsinden
> integer**; yuvarlama yalnız **gösterimde**. Dayanak: K-059/6 · K-060/4 ·
> K-053 · K-059/5.

### 14.1 `kalan_gun`

| Kural | Değer |
|---|---|
| Tanım | Maaş gününden kurulan dönemde **bugün dahil** kalan gün sayısı |
| Maaş günü o ayda yoksa (31 → Şubat) | **Ayın son günü** kullanılır |
| Maaş günü "Düzensiz" | Dönem **30 gün** kabul edilir |
| Kaç yerde tanımlı | **Bir** — plan (E-26), limit önerisi ve dönem göstergeleri aynı fonksiyonu çağırır |

### 14.2 Plan zinciri (E-25 → E-26)

| # | Büyüklük | Formül |
|---|---|---|
| 1 | `zorunlu_kurus` | Σ (kira_aidat + faturalar + ulasim_yakit + kredi_taksit) — **yalnız kullanıcı girdisi**; boş alan 0 sayılır |
| 2 | `birikim_kurus` | `gelir_kurus × birikim_yuzde / 100` |
| 3 | `sosyal_kurus` | `gelir_kurus − zorunlu_kurus − birikim_kurus` |
| 4 | `birikim_yuzde` üst sınırı | `100 − zorunlu_yuzde` (bu noktada `sosyal_kurus = 0`) |
| 5 | Yüzdeler | `pay_kurus × 100 / gelir_kurus`, **tam sayıya** yuvarlanır; üç yüzdenin toplamı **en büyük kalan** yöntemiyle 100'e tamamlanır |
| 6 | `gunluk_limit_kurus` | `sosyal_kurus // kalan_gun` → gösterimde **tam liraya AŞAĞI** (`// 100 × 100`). Yukarı yuvarlamak limiti her gün bir miktar aşındırır |
| 7 | `aliskanlik_aylik_kurus` | `siklik_gunluk × fiyat_kurus × 30`; haftalıkta `haftalik / 7`; "Ayda 1-2"de `siklik_aylik × fiyat_kurus`. **"Hiç" → kalem hiç üretilmez** (0 ₺ satırı yazılmaz) |
| 8 | `yatirim_payi_kurus` | `birikim_kurus × yatirim_yuzde / 100` — **yalnız etiket**, ayrı kova değil |
| 9 | Negatif kalan | `zorunlu_kurus > gelir_kurus` ise plan **kurulmaz**; ekranda `zorunlu − gelir` **"1.400 ₺ eksik"** biçiminde yazılır (negatif sayı gösterilmez) |

**Cevaplanmamış alan `null`'dır, 0 ile doldurulmaz.** 0 = "hiç harcamıyorum";
`null` = "cevaplamadım". Plan ekranı bu ikisini farklı gösterir.

### 14.3 `gunluk_limit_onerisi` (Katman 1 çıkışı · K-059/5 · K-060/2)

`floor(gelir_kurus × 0.30 / kalan_gun)` → tam liraya **aşağı**.
Varsayılan dağılım **%50 zorunlu / %30 sosyal ve keyfi / %20 birikim**
ekranda **yazılıdır**; kullanıcının cevabından çıkmadığı ayrıca söylenir.
Sabit giderler biliniyorsa onlar **olgu** olarak kullanılır, yüzde yalnız
bilinmeyen kısma uygulanır. **Onaylanana kadar limit yoktur:** depoya
`gunluk_limit` değil `gunluk_limit_onerisi` yazılır; E-10 limitsiz kipte
açılır ve seri kapalı kalır (K-048).

### 14.4 `biriken` — "Limit altı günlerde biriken" (K-056 · brandbook §2.4)

`biriken = Σ (o günün günlük limiti − o gün harcanan)`, yalnız **limit
altında kapanan** günler için.

| Kural | Değer |
|---|---|
| Hangi günler sayılır | Gün **kapanmış** ve harcanan ≤ o günün limiti |
| Limit dışı günler | **0 sayılır** — negatif değer toplama eklenmez (kayıp "geri ödenmez") |
| O gün limiti yoksa | Gün hesaba **girmez** (limitsiz günün artanı tanımsızdır) |
| Kayıt yazılmamış gün | Girmez; "harcamasız" işaretli gün de **girmez** (K-048 hile kapısıyla aynı gerekçe) |
| Pencere | Gösterildiği ekranın penceresi: E-24'te **görüntülenen ay**, E-16'da hafta |
| Ne DEĞİLDİR | Banka birikimi değil, gerçekleşmiş tasarruf iddiası değil. Arayüz **"biriken"** der; "tasarruf ettin", "kazandın" yazılmaz |

### 14.5 `seri` (streak · K-048)

Üst üste, **limit altında kapanmış** ve (**kayıt var** ya da **harcamasız
işaretli**) günler. Gün kapanışı E-19'daki **gün sınırı** ayarıdır. Hesap
**yereldir**, sunucu yoktur. **Limitsiz kipte seri çalışmaz** — bu yüzden
E-10'da seri çipi çizilmez ve E-21'e giriş kapalıdır.
