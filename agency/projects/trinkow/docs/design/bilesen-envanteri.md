# Trinkow — Bileşen Envanteri (P-7) · **v4.1 · Claymorphism (REV2 senkronu)**

> **Amaç:** Tasarım ve kodun **aynı ismi** kullanması. Buradaki isimler
> `src/components/<İsim>.tsx` dosya adı olarak birebir kullanılır.
> Ölçü/renk değerleri burada **tekrarlanmaz** — kaynak `projects/trinkow/docs/brand/tokens.md`
> **v3.1**. Bu dosya "hangi bileşen + hangi durumlar" sorusunun cevabıdır.
>
> **v3.1 güncellemesi (2026-09-12, Tur E):** dosya v1.0 değerleriyle
> (`accent`, `edge`, hairline, tek katman gölge, 12 radius) kalmıştı.
> Tamamı v3.1 claymorphism'e çekildi: renk adları, **clay gölge katmanları**,
> **§3.1 ritim seti**, `pressed` tanımı. Yeni yüzeylerle (E-15 · E-17 · E-18 ·
> E-19 · E-20) gelen bileşenler eklendi, ölen bileşenler işaretlendi.
>
> **v4.0 güncellemesi (2026-09-18, v4 birleştirmesi · T-1…T-5):** seri,
> gün/ay ızgarası, oturum açma, profilleme, plan ve ürün arama yüzeyleriyle
> gelen bileşenler eklendi (§1'den §5'e dağıtıldı, sayım §6'da). §0'a
> `selected` durumunun tek dili yazıldı (K-061/2). §6'nın kapsam-dışı
> listesi K-054/3'e göre düzeltildi.
>
> **v4.1 senkronu (2026-09-25, hijyen turu):** yeni tasarım kararı
> **üretilmedi**; dosya Rev ve REV2 turlarında kodlanan gerçekle hizalandı.
> Geçersiz kalan maddeler: çubuktaki `Fab` · `OptionCard`'ın "2pt iç çizgi"
> seçili hâli · `ClayKeypad` · `LegalConsentText` · `AccountSection`'ın
> "hesap hiçbir özelliği kilitlemez" cümlesi (K-080). REV2 bileşenleri
> §1-§5'e dağıtıldı, sayım §6'da güncellendi. Otorite:
> `projects/trinkow/docs/design/rev2-onboarding-kayit.md` §10 +
> `projects/trinkow/docs/design/rev2-tasarruf-profil.md` §5.
>
> Kapsam: **Faz 1** · React Native (Expo, New Architecture) · tek tema: açık.
> Çizili karşılığı: `projects/trinkow/docs/design/prototip-v4/`
> (**18 sayfa · 122 yüzey**; `_uret/denetim.py` → 0 bulgu) ve REV2'nin iki
> yüzey seti: `prototip-rev2/onboarding-kayit.html` ·
> `prototip-rev2/tasarruf-profil.html`.
> v3 karşılığı `prototip-v3/` arşiv olarak durur.

---

## 0. Ortak durum sözlüğü (bağlayıcı — kodda da bu anahtarlar)

| Durum anahtarı | Ne zaman | Not |
|---|---|---|
| `default` | Normal | Kabarık yüzey: `clay.raised` + `grad.clay-face` |
| `pressed` | Parmak elemanın üstündeyken | **RN'de hover YOK.** Tek geri bildirim budur. Görünüm: gölge `clay.pressed` + zemin `groove`, birincil butonda `clay.action-pressed` + `primary-press`. **`scale` animasyonu yok** — yüzey çöker, küçülmez. Atlanan bileşen kabul edilmez. |
| `focused` | Klavye/erişilebilirlik odağı | 2pt `primary-text` dış halka, elemandan 2pt boşlukla, halka yarıçapı = eleman yarıçapı + 4. Kaldırılmaz. |
| `disabled` | Eylem şu an mümkün değil | Zemin `disabled-bg`, metin `text-2`, gölge `clay.sunken`. **Opaklık kullanılmaz** |
| `loading` | İşlem sürüyor | Aşağıdaki 150ms kuralına bak |
| `error` | Doğrulama/okuma hatası | 2pt `danger` kenarlık + altında `caption`/`danger-ink`. Metin `metinler.md`'den |
| `empty` | Veri yok | "Henüz veri yok" yazılmaz |
| `selected` | Seçili (çip, segment, sekme, seçim kartı) | Seçili = **çukur** (`clay.sunken`) + `primary-soft`; ikon kabı varsa **tersine kabarır**. Onay ikonu yok, **halka yok** (tokens §5.4 · K-061/2). RN: `accessibilityState={{selected:true}}` |
| `filled` | **Verinin durumu** (seçim değil): dolu gün kutusu, geçilmiş durak | Düz `primary-deep` + kabartma, beyaz sayı (5.37 ✅ · K-062). Gradyan **kullanılmaz** — tokens §1.6/§5.4 |
| `overflow` | **Limit dışı** | `warning` ailesi. Kırmızı, ünlem, suçlayıcı ikon yok |
| `skeleton` | İlk okuma iskeleti | Bloklar `well` + `clay.sunken`. Parıldama (shimmer) **yok** |

### Clay üç derinlik kuralı (v3'ün omurgası)

| Derinlik | Anlamı | Nerede |
|---|---|---|
| **Kabarık** (`clay.raised` / `-lg`) | "Bu bir nesne" | Kart, liste satırı, çip, tuş, anahtar topuzu |
| **Çukur** (`clay.sunken`) | "Buraya değer girer / bu seçili" | Kuyu, oluk, segment track, kategori kabı, seçili çip |
| **Basılı** (`clay.pressed`) | "Parmağın üstünde" | Her etkileşimli yüzeyin `pressed` hâli |

Gölge dekorasyon değildir; **katman bilgisini renk değil gölge taşır**
(`surface` ↔ `bg` kontrastı kasıtlı olarak 1.16:1'dir, tokens §1.1).

### `loading` için 150ms kuralı (bağlayıcı)
- **< 150ms:** hiçbir yükleme göstergesi çizilmez (yanıp sönme üretir).
- **≥ 150ms:** `Skeleton` gösterilir.
- **Yazma işlemleri** (Kaydet/Sil) her zaman butonun `loading` durumunu
  kullanır — kullanıcı dokunduğu için geri bildirim bekler.

### Dikey ritim (tokens §3.1 — bileşen yazarken bağlayıcı)

| Değer | Tek işi |
|---|---|
| **4** | Aynı nesnenin iki satırı (tutar ↔ "limit dışı") |
| **8** | Başlık ↔ gövde · etiket ↔ girdi · aynı grubun tekrarlayan öğeleri (liste satırları, çipler, tuşlar) |
| **12** | Kartın **içinde** iki bağımsız blok |
| **16** | **İç boşluk** (padding) — dikey ritim değil |
| **24** | Ekran düzeyinde iki bağımsız blok · içerik alt boşluğu |

Bileşen kendi dışına marj koymaz; aralığı **ekran** verir.

### Her etkileşimli bileşenin taşıması zorunlu 4 şey
1. `pressed` görünümü · 2. minimum **44×44pt** dokunma hedefi (`hitSlop`) ·
3. Türkçe ve fiille yazılmış `accessibilityLabel` · 4. `disabled` ise
`accessibilityState={{ disabled: true }}`.

---

## 1. Etkileşim bileşenleri

### `Button`
tokens.md §7.1. Varyantlar: `primary` (**56**) · `secondary` (**52**) ·
`ghost` (**44**). Dördüncü varyant üretilmez. Ekranda **aynı anda tek
`primary`**. Radius 999 (hap).

| Durum | Davranış |
|---|---|
| `default` | primary: `grad.action` + `clay.action` · secondary: `surface` + `clay.raised` · ghost: şeffaf |
| `pressed` | primary: `primary-press` + `clay.action-pressed` · secondary/ghost: `well` + `clay.pressed`. 150ms, **scale yok** |
| `disabled` | `disabled-bg` + `text-2` + `clay.sunken`. Opaklık yok |
| `loading` | Metin "Kaydediliyor", sağında 20pt spinner, **genişlik sabit**, disabled |
| `focused` | 2pt `primary-text` dış halka (koyu zeminde `#FFFFFF`) |
| Uzun metin | Buton büyümez; `numberOfLines={1}` + `ellipsizeMode="tail"` |

> **Beyaz metin `#3B82F6` üzerine yazılmaz** (3.68:1). Buton zemini daima
> `primary-deep`, gradyan dikey ve koyu uçludur (tokens §1.6).

### `IconButton`
Görsel kutu **44×44**, radius 16, zemin `surface` + `clay.raised`, ikon 22pt.
`pressed`: `groove` + `clay.pressed`. Sağ üstte kullanılır; **sol üstte
yalnız `PushHeader`'ın geri oku bulunur** (kritik/yıkıcı hedef sol üste
konmaz — iOS geri kaydırmasıyla çakışır).

### `Chip`
tokens.md §7.6. Yükseklik 40 (hitSlop ile 44), radius 999.
`default` kabarık · `selected` **çukur** (`primary-soft` / `cat.*.soft`,
solda 8pt nokta, **onay ikonu yok**) · `pressed` · `disabled`.
`flexWrap` ile sarar (grid yok), aralarında 8.
**Taşma (tokens §7.6 · bağlayıcı):** çip tek satırdır, `flexShrink: 0`,
maks. genişlik 240. Ad `numberOfLines={1}` + `ellipsizeMode="tail"`, maks.
120 genişlik; **tutar hiç kırpılmaz — `₺` kaybolursa çip işlevini yitirir.**
`accessibilityLabel` tam adı taşır. Uzun ad test dizesi:
`Marlboro Touch Blue 20'lik`.

### `SegmentedControl`
Track `well` + `clay.sunken`, iç boşluk 4, radius 999. Seçili segment
**kabarık** (`surface` + `clay.raised`) — seçim renkle değil **yükseklikle**
okunur. Kullanım: Nakit/Kart (F-6) · gün sınırı 00.00/03.00/06.00 (E-19).
İkiden fazla segment yalnız gün sınırında (3) kullanılır; dördüncü eklenmez.

### `ClaySwitch` (eski `Switch`)
**RN'in platform `Switch`'i kullanılmaz** — iOS/Android farklı çizer ve clay
dili uygulanamaz. `Pressable` + iki `View`: track 56×32 (`well` + sunken;
açıkken `grad.action` + `clay.action`), topuz 24pt daire (`surface` +
`clay.raised`), hizalama `justifyContent` ile (flex, animasyon 150ms).
Durumlar: `on` / `off` / `pressed` / `disabled`.
**Dokunma hedefi satırın tamamıdır** (`SettingRow`, ≥68pt).

### `Checkbox` (yeni — REV2 · hesap oluştur)
Yasal onayın tek dili. Kutu **32×32** · radius 16 · satır min **44**
(dokunma hedefi **satırın tamamı**, `hitSlop` dikey 8) · kutu ↔ metin 12 ·
20pt `check` glifi. Etiket `caption`/`text` ve **bağlantı taşımaz** —
belgeler grubun altındaki iki `ghost` satırından açılır.
Durumlar: `unchecked` (`well` + `clay.sunken`, glif yok) / `checked` (düz
`primary-deep` + `clay.raised` + beyaz glif; gradyan yok · K-062) /
`pressed` (iki hâl) / `focused` (2pt `primary-text` halka) / `error`
(2pt `danger`; hata **iki kutuya birlikte** uygulanır, ilk dokunuşta kalkar) /
`disabled` (`disabled-bg`, opaklık yok).
Küçük kontrolde §5.4 "seçili = çukur" dilinden bilinçli sapmanın gerekçesi:
`rev2-onboarding-kayit.md` §7.1.

---

### `SocialAuthButton` (yeni — E-22 · E-23)
Apple ve Google varyantı. Durumlar: `default` / `pressed` / `busy`.
**Kap bizim, içerik sağlayıcının** (tokens §7.1 `button.social`): dolgu,
logo ve etiket palet dışıdır ve değiştirilemez. **iOS'ta Apple varyantı
bizim bileşenimiz değildir** — `expo-apple-authentication`'ın
`AppleAuthenticationButton`'ı (style `BLACK`, type `CONTINUE`, radius 28).
Sağlayıcı kümesi platforma göre kurulur: iOS Apple + Google, Android
yalnız Google (K-058).

### `Slider` (yeni — E-25 · E-26) — *yeni tip*
Oluk 12 · topuz 32 · satır 44; dolgu topuzun **merkezinde** biter.
Durumlar: `default` / `pressed` (topuz çöker) / `max` (topuz durur, zemin
`warning-soft` — üst sınır bir **hata değil**) / kullanılamıyorsa **hiç
çizilmez** (gelir yoksa pasif kaydırıcı bırakılmaz).
RN: platform bileşeni değil, `PanResponder` + üç `View`;
`accessibilityRole="adjustable"` + `increment`/`decrement` (adım %1).

### `FrequencyChips` (yeni — E-25)
Sarmalı çip satırı; **serbest sayı seçeneği en sonda**. `selected` (çukur)
/ `pressed` / "Hiç" (fiyat alanını kapatır, planda 0 ₺ satırı üretmez).

---

## 2. Girdi bileşenleri

### `TextField`
tokens.md §7.4. Yükseklik 56, radius 16, zemin `well`, gölge `clay.sunken`,
**kenarlık yok** — çukurluk gölgeyle anlatılır. Etiket üstte (`label`/`text-2`,
arası 8), placeholder'a gömülmez.
Durumlar: `default` / `focused` (2pt `primary-text`) / `error` (2pt `danger`
+ altında hata metni, 8 boşlukla) / `disabled` / `filled`.

### `AmountWell` + `ClayKeypad` (eski `AmountField`)
tokens.md §7.4 + §7.11. **Sistem klavyesi açılmaz.**

| Parça | Kural |
|---|---|
| `AmountWell` | `well` + `clay.sunken` kuyu; sayı `hero` (56pt) tabular, `₺` `display` (32pt) `text-2`, imleç 3pt `primary` |
| `ClayKeypad` | 4×3: `1 2 3 / 4 5 6 / 7 8 9 / , 0 ⌫`. Tuş 56 yüksek, radius 16, kabarık; `pressed` → `groove` + `clay.pressed`. Tuşlar arası 8 (negatif oluk telafisi −4) |
| Nokta tuşu | **Yok** — binlik ayracı otomatik eklenir |
| "Kaydet" | Tuş takımının **altında sabit**; `KeyboardAvoidingView` gerekmez |
| Taşma | 7 karakteri aşan tutarda rol bir basamak iner: `hero` → `display`. Kuyu yüksekliği sabit, düzen kaymaz |
| Nerede | E-11 · E-02 · E-17 |

Durumlar: `empty` (0, `text-3`) / `typing` / `error` / `overflow-preview`.

> **Rev/REV2: `ClayKeypad` kullanımdan düştü.** Para girişi RN'in kendi
> `TextInput`'uyla yapılır (`decimal-pad`, virgül/nokta, yapıştırma, veri
> integer kuruş); kil tuş takımı hiçbir ekranda çağrılmıyor. `AmountWell`
> native girdinin çukur kabuğu olarak yaşar; "Kaydet" tuş takımının değil
> `KeyboardAvoidingView`'in üstünde sabit durur. Yukarıdaki tuş takımı
> satırları **tarihsel kayıttır**, ölçü kaynağı değildir.

### `MoneyField` (yeni — REV2 · kurulum 2/4 · sheet'ler)
Tam genişlik para alanı: `TextField` ölçüsü (56 · radius 16 · `well` +
`clay.sunken`) + native `decimal-pad`, tabular rakam, sağda sabit birim.
Durumlar: `empty` / `focused` / `filled` / `error` / `disabled`.
Ayrıntı: `rev2-onboarding-kayit.md` §4.2.

### `MoneyRow` (yeni varyant — REV2)
`ValueWellRow`un **düzenlenebilir** ikizi: çukur satırın içinde etiket +
native girdi. `birim` parametresi **zorunlu** (`"₺"` | `""`);
`fontScale > 1.3`'te dikey düzene döner. Durumlar: `dolu` / `bos` /
`focused` / `error`. Ayrıntı: `rev2-onboarding-kayit.md` §4.3.

### `PasswordField` (yeni — E-22 · E-23)
`TextField`'ın **sağ yuvalı (trailing slot)** varyantı; yeni bileşen değil,
alanın varyantıdır. Yuva 44pt ikon düğmesi alır, alanın sağ iç boşluğu
16 → 8. Durumlar: `default` / `focused` / `error` / `visible` / `hidden`.
Göz düğmesi yalnız `secureTextEntry`'yi çevirir — odak ve imleç korunur.

### `PasswordRuleLine` (yeni — E-23)
`unmet` (caption) / `met` (20pt `check` + caption). **Renkli güç çubuğu
yok**: ölçtüğü şey kullanıcının anladığı şey değil (K-050 sahte skor).

### `SearchField` (`arama-alani`, yeni — E-11)
Mevcut `.giris` ölçüsü (56 · `well` · `clay.sunken`) — yeni giriş biçimi
icat edilmedi. Durumlar: `empty` (placeholder) / `focused` / `typing`
(+ temizle) / `loading` (iskelet) / `selected` (ürün seçili + kaldır).
**Boşken akışa karışmaz:** odaklanmaz, doğrulama hatası üretmez, Kaydet'i
engellemez.

### `ValueWellRow` (`kuyu_deger`, yeni — E-25)
Çukur satır: etiket + değer + chevron, iç boşluk 12/16. `dolu` / `bos`
("Girilmedi" / "Fiyatını yaz" — **placeholder rengi değil**, geçerli
durum) / `pressed` / `focused`.

### `ValueWell`
Dokunulabilir **çukur değer satırı**: solda etiket, sağda değer + `chevron`
ya da `pencil`. Kartın içinde "bu değer değiştirilebilir" demenin tek yolu.
Nerede: E-17 limit satırları · E-19 bildirim saati, kip.
Durumlar: `default` / `pressed` / `focused` / `error` (2pt `danger`).

### `SettingRow`
**Kabarık** tek karar satırı: solda başlık + `caption` açıklama, sağda
kontrol (`ClaySwitch` ya da değer). İç boşluk 12/16, minimum 68.
Durumlar: `default` / `pressed` / `disabled` (açıklama metni değişir,
opaklık değişmez).

### `CategoryPicker`
Frekansa göre sıralı çip listesi; ilk 6 görünür, altında `ghost` "Tüm
kategoriler" → 3 sütunlu kutu ızgarası (`flexWrap`, grid yok).
Durumlar: `default` / `selected` / `expanded` / `empty` (ilk gün sabit sıra).
**REV2: harcama ekleme ekranında kullanılmaz** — kategori route param'ından
ya da seçilen üründen gelir ve orada **salt okunur göstergedir**. Bileşen
`RoutineSheet` (yatay çip şeridi), limitler, favoriler ve harcama detayında
yaşamaya devam eder.

### `InstallmentPicker`
Taksit sayısı (F-7). Yalnız **Kart** seçiliyken görünür. **+2 dokunuş**
(K-023): "Taksitli" çipi → sayı çipi; ayrı "Uygula" adımı yoktur.
Durumlar: `default` / `selected` / `hidden`. Nakite dönülürse taksit
**sessizce sıfırlanır**.

### `DateField`
Varsayılan **bugün**. "Bugün" / "Dün" / tarih. Dokununca sistem tarih seçici.
Durumlar: `default` / `pressed` / `error` (gelecek tarih kabul edilmez).

### `NoteField`
İsteğe bağlı tek satır not (60 karakter). Durumlar: `default` / `focused` /
`filled`. Sayaç yalnız son 10 karakterde görünür.

---

## 3. Veri gösterim bileşenleri

### `LimitGauge` — **hero bileşen** (F-3) — *eski adı `LimitBar`*
tokens.md §7.5. v3'te çubuk değil **270° dairesel kil yay**: 224pt kabarık
disk, oluk `well` + iki kenar yayı, dolgu `grad.arc` 16pt yuvarlak uçlu,
**topuz zorunlu**.

| Durum | Görünüm |
|---|---|
| `default` | Oluk + `grad.arc` dolgu + topuz. **Doluluğa göre renk değişmez** |
| `full` (%100) | Yay tam dolu, renk dönmez, eşik işareti yoktur |
| `overflow` | Ana yay %100 kalır + **dışında** 8pt `grad.arc-over` taşma yayı + `hero` sayı `warning-ink` + altında "limit dışı" |
| `empty` | 176pt çukur disk, dolgu ve topuz yok; ortadaki sayı limitin tamamı |
| `no-limit` | **Yay hiç çizilmez → `HeroPlain`** (aşağıda). `EmptyState` ve "Limit belirle" çağrısı **kullanılmaz**: limitsiz kalmak geçerli bir seçimdir |
| `skeleton` | Disk ve oluk çizilir, dolgu çizilmez |
| Animasyon | 250ms ease-out, sayı eş zamanlı sayar; reduce-motion 0ms |
| a11y | `role="progressbar"` + `accessibilityValue={{min,max,now}}` |

### `MiniGauge`
`LimitGauge`'ın 56pt türevi: kalınlık 8, topuz yok, dolgu `cat.*.solid`.
Ekranda en fazla **3 tane**.

### `CategoryLimitBar`
Yükseklik **12**, radius 999, oluk `groove` + `clay.sunken`, dolgu
`cat.*.solid`, taşma `warning`. Taşmada oluk **toplamı** temsil eder
(dolu kısım orantılı daralır). Nerede: E-10 kartı · E-15 özet kartı.

### `MonthLoadRow` (yeni — E-18)
Ay adı (56pt sabit sütun) · `LoadBar` (esner) · tutar (88pt sabit sütun,
tabular, sağa hizalı). Çubuklar **aynı ölçeği** paylaşır: en yüklü ay %100.
Durumlar: `current` (ay adı `text`, SemiBold) / `future` (`text-2`) /
`skeleton`.

### `SeriesRow` (yeni — E-18)
Kategori kabı · "{kategori} · {mevcut}/{toplam}" · bitiş tarihi ·
sağda aylık tutar + "her ay". `last` durumunda alt satır
"Son taksit bu ay" (`warning-ink`).

### `HeroAmount`
`hero` (56pt) tabular sayı + altında `label`. İçerik **kipe** göre değişir.
Durumlar: `default` / `overflow` (sayı `warning-ink`, "limit dışı"; eksi
işareti yok) / `long` (6+ karakter → `display`'e iner) / `skeleton`.

### `HeroPlain` (yeni — E-10 · limitsiz)
**Yaysız** kahraman düzeni. Nerede: günlük limit tanımlı **değilken** E-10.
Yapı: kip çipi ↔ sağda "Limit yok" değeri → **24** → `HeroAmount`
("bugün harcanan") → **24** → `body` gün özeti tek satır. Kart
`primary-soft` + `clay.raised-lg`, radius 32 — yay varyantıyla aynı kap,
yay varyantından **kısa**; boşluk doldurulmaz.

`EmptyGauge` neden değil: `EmptyGauge` *veri* beklenen yerde durur; burada
veri var, **eşik** yok. Boş bir oluk çizmek "bir şey eksik" yalanıdır.

Yasaklar (bağlayıcı): "Limit belirle" birincil çağrısı · `warning` renk ·
uyarı ikonu · yayın gri/kesikli hâli. Bu bir **bilgi** ekranıdır, hata
değil. Durumlar: `default` / `long` (6+ karakter → `display`) / `skeleton`.

### `AmountText`
`1.250,50 ₺`, tabular, `₺` bölünmez boşlukla, simge sonda.
Varyantlar: `hero` / `row` / `inline`. Negatif yok → `overflow` varyantı
"60 ₺ limit dışı" üretir.

### `SpendRow` (`FlatList` satırı)
tokens.md §7.3. **Her satır ayrı kabarık yüzeydir** (radius 16,
`clay.raised`), aralarında 8 — v1/v2'deki hairline ayraç kaldırıldı.

| Durum | Görünüm |
|---|---|
| `default` | `surface` + `clay.raised`, sol 44×44 çukur kategori kabı |
| `pressed` | `groove` + `clay.pressed` |
| `overflow` | Zemin `warning-soft`, tutarın altında `caption`/`warning-ink` "limit dışı" |
| `swipe` | Sağa kaydır → **Sil** · sola kaydır → **Tekrarla**. Tek harcamada onay yok, 6 sn geri al (K-029); taksitli kayıtta `Dialog` |
| `installment` | İkincil satırda "3/12 taksit" · ikon değişmez |
| Uzun metin | Birincil satır 1 satır kırpılır; **tutar asla kırpılmaz** |

### `RoutineRow` (yeni varyant — REV2 · kurulum 3/4 · Rutinler)
`SpendRow` ölçüleri (kabarık satır, radius 16, sol 44 kategori kabı) +
sağda `pencil`: eklenmiş bir rutini gösterir ve düzenlemeye açar. İkincil
satır "Her gün {adet} × {fiyat}". Durumlar: `default` / `pressed` /
`empty` (satır çizilmez, bölüm "Eklediğin rutinler burada sıralanır." der).
Ayrıntı: `rev2-onboarding-kayit.md` §5.1.

### `DayBox` (E-15 · v4'te E-21 / E-24 / E-03)
44×44 kutu: gün sayısı (`label`) + ay kısaltması (`micro`).
`SpendRow`'un sol sütununda kategori kabının **yerine** geçer — kategori
sabitken aynı ikonu tekrarlamak bilgi taşımaz.

**v4 varyantları:** `sayı-only` (28/31 günlük pencerede ay tekrarı bilgi
taşımaz) ve dört durum — `altinda` (düz `primary-deep` + beyaz sayı,
5.37 ✅) · `disinda` (`warning-soft` + `warning-ink`, 5.86 ✅) · `yok`
(`well` çukur + `text-2`, 5.13 ✅) · `pasif` (`disabled-bg` + `clay.sunken`
+ `text-3`; gölge **kaldırılmaz**, gizlenmez).
Üç veri durumu renge **ek olarak** derinlikle ve `accessibilityLabel` ile
ayrışır (WCAG 1.4.1). **"Seçili" durumu yoktur** (E-24): açık gün ay
başlığının altında **yazıyla** söylenir; tek görsel işaret "bugün"
noktasıdır (tokens §5.4). E-03 maaş günü seçiminde kullanılan `secili`
ayrı sınıftır — seçim ile veri aynı görünümü paylaşmaz.

### `StreakDayGrid` (yeni — E-21)
28 gün (4 tam hafta), 7 sütun `flexWrap` (**CSS grid yok**); kelimeli
lejant (`LegendSwatch` 24×24). Pencere **bugünü içermez** — bugün
kapanmadığı için dördüncü bir kutu durumu üretilmedi; başlık tarih
aralığını yazar. `dolu` / `empty` ("Günleri yazdıkça buraya dolacak.").

### `MonthGrid` (yeni — E-24)
7 eşit hücreli flex satırlar (`flex: 1`), hücre içi kutu 44. Hücre:
`altinda` / `disinda` / `yok` / `pasif` / `pressed`. Ay başı/sonu boş
hücreleri **yer tutar** (ızgara kaymaz), gerçek `View`'dir.

### `MilestoneRail` (yeni — E-21)
8 durak (3·7·14·30·60·100·180·365) + aralarında **oranlı** yol; yatay
`ScrollView`. Durak: `gecildi` / `sirada` / `ileri`. Yarım görünen durak
keşfedilebilirliği sağlar.

### `StreakSummaryWell` (yeni — E-21)
`ValueWell`'in **dokunulmaz** varyantı ("En uzun seri"). `default` /
`empty` ("Henüz yok").

### `StreakPill` (yeni — E-10 başlığı)
`Chip`'in metin varyantı ("Seri 12 gün") → E-21. `default` / `pressed` /
`skeleton`. **Seri yoksa ya da limitsiz kipteyse render edilmez** — pasif
çip ölü arayüzdür. Başarım ikonu değil **değer** taşır; alev/şimşek yok.

### `ShareBar` + `ShareRow` (yeni — E-26)
Tek oluk + 3 segment (aralar 4, oluk aradan görünür): zorunlu
`primary-deep` · sosyal `primary` · birikim `success` (K-059/4). Metin
taşımaz. `3 pay` / `2 pay` (birikim girilmedi) / `loading`.
`ShareRow`: 8pt nokta + ad + açıklama + sağda ₺ / % · `dolu` /
`Girilmedi` (**%0 yazılmaz**).

### `EquationRow` (yeni — E-26)
Üç çukur kutu + `÷` `=` + **kabarık** sonuç kutusu (`primary-soft`):
hiyerarşi gölgeyle kuruldu. `dolu` / `loading`.

### `MirrorWell` (yeni — E-25)
Çukur "Ayda X ₺" + altında formül satırı. Soru cevaplanmadıysa **hiç
çizilmez**.

### `CategoryGroupRow` (yeni — E-10)
Kategori grubu satırı: ikon + ad + **aylık toplam / aylık limit** +
çubuk + `+`. İkincil satırda "bugün {tutar}" ve "kalan {tutar}" /
"{tutar} limit dışı". Durumlar: `default` / `bugün kayıt yok` /
`limit dışı` / `+ pressed`. Halka yerine **çubuk** kullanılır: halka bu
ekranda kahraman göstergenin dilidir.

### `CategoryShareRow` (yeni bileşim — REV2 · Tasarruf)
Ayın kategori dağılımı satırı: 44 kategori kabı · ad + tutar · 12pt kategori
çubuğu · altında pay ve rutin farkı satırı. `CategoryLimitBar` +
`MonthLoadRow` geometrisinden kuruldu, **yeni ölçü açmaz**. Çubuk
dokunulamaz (bilgi), payı ayrıca yazıyla okunur.
Durumlar: `default` / `rutin farkı var` / `skeleton`.

### `SavingsMovementRow` (yeni varyant — REV2 · Tasarruf · /birikimler)
`SpendRow`'un birikim hareketi hâli: sol sütun **`DayBox`** (`.gun-kutu`
deseni — ikon kabı değil), birincil satırda yön metni, sağ altta "çekildi",
sola kaydır → Sil. Not yoksa ikincil satır **çizilmez**.
Durumlar: `default` / `pressed` / `çekildi` / `swipe` / `skeleton`.

### `IdentityPanel` (yeni — REV2 · Profil)
Profil'in kahraman paneli: radius 32 · `primary-soft` · `clay.raised-lg` ·
iç boşluk 16 · 48pt çukur ikon kutusu + iki satır + `chevron-right`.
`signed-in` hâlinde içine `FactStrip` girer (panel 156pt).
Durumlar: `signed-in` / `signed-out` / `error` / `skeleton` — dördü de
**aynı paneldir**: durum değişince aksan kaybolmaz.

### `SearchResultRow` (`sonuc-satiri`, yeni — E-11)
`default` / `pressed` / `"… olarak ekle"` (nötr kap). **Sağda tutar
sütunu yoktur** — olmayan bir fiyat otoritesi ima edilmez; kullanıcının
kendi tutarı ikinci satırda "geçen sefer" sözcüğüyle, `caption`
ağırlığında durur.

### `RecentChip` (`son-kullanilanlar-cip`, yeni — E-11)
`default` / `pressed` / uzun ad (ad kırpılır, **tutar kırpılmaz**).
Tutar 0 iken görünür, ilk rakamda kapanır. Girilen değerin üzerine
**sessizce yazmaz**.

### `SuggestionTag` (`oneri-pul`, yeni — Katman 1 çıkışı)
Dokunulamaz çukur etiket: sayının **onaylanmamış** olduğunu söyler.
Kabul edilince **pul düşer** (K-059/5).

### `SectionHeader`
Kartsız tek satır: solda `h2` ya da `body-strong`, sağda `label`/`text-2`
toplam. **Yapışkan (sticky) değildir** — `sticky` RN'de yoktur.
`overflow` durumunda sağ taraf `warning-ink` olur ve yanına birebir
"limit dışı" yazılır.

### `SummaryRow`
Etiket (solda, `body`) + tabular sayı (sağda, `amount`).
Durumlar: `default` / `overflow` / `zero` ("0 ₺" gösterilir, satır
gizlenmez — dürüstlük).

### `WeekStrip`
7 günlük sütun şeridi (F-5). Sütun oluğu `well` + `clay.sunken`, dolgu
`primary`, limit çizgisi kesikli `text-2`, eşiği aşan üst parça `warning`.
Durumlar: `default` / `partial` (gelecek günler yalnız oluk) / `empty`.
**Yasak:** ızgara çizgisi, hue değiştiren degrade, üç boyut.

### `Card`
tokens.md §7.2. Radius 24 (kahraman/sheet 32), zemin `surface` +
`grad.clay-face`, gölge `clay.raised`, **kenarlık yok**, iç boşluk
**16 istisnasız**. `pressed` varsa `groove` + `clay.pressed`.
**Yasak:** daire ikon + başlık + tek cümle üçlü kart düzeni.

### `Divider` — **kaldırıldı**
1px `line` ayraç v3'te liste ayracı **değildir**: satırları gölge ayırır.
`line` yalnız kart içi mantıksal ayraç ve sheet tutamacı olarak kalır.

---

## 4. Yapı / navigasyon

### `ScreenHeader`
Sekme ekranlarının başlığı: solda (isteğe bağlı tarih `caption` +) `h1`,
sağda tek `IconButton`. Alt çizgi yok. Kaydırınca başlık küçülmez.
Üst/alt boşluk 8/16.

### `PushHeader` (yeni)
İtilen ekranlar (E-15 · E-17 · E-18 · E-19): solda geri `IconButton`,
ortada `h1` (tek satır, kırpılır), sağda isteğe bağlı eylem ya da 44pt boş
denge kutusu. Geri oku iOS kenar kaydırmasının görünür karşılığıdır.

### `SetupShell` (yeni — REV2 · kurulum 1/4…4/4)
Kurulumun kendi kabuğu; bu akışta `RevScreen` **kullanılmaz**. Üstte
**sabit** bölge (44 geri oku + `StepIndicator`, kaydırma alanının dışında),
ortada `ScrollView`, altta sabit birincil düğme bloğu. "Kurulum · 1/4"
kocaman başlığı **yoktur** — adım numarası ekranın en büyük tipografik
öğesi değildir. Durumlar: `adim=1..4` / `geri yok` (ilk adım) /
`klavye açık` / `busy` (düğme `loading`). Ayrıntı:
`rev2-onboarding-kayit.md` §2.

### `TabBar` + `TabItem`
tokens.md §7.7. **Yüzen** çubuk: yükseklik 68, radius 999, `clay.raised-lg`,
alttan `insets.bottom + 8`, yanlardan 16. Faz 1: **3 sekme** —
**Günlük · Tasarruf · Profil** (REV2), `space-around` ile eşit dağılır.
`TabItem`: `active` (ikon arkasında 40pt çukur `primary-soft` daire +
`primary-text` + SemiBold) / `inactive` / `pressed`. Etiketsiz ikon yok,
rozet yok.
**`Fab` kaldırıldı (REV2).** Çubukta büyük `+` yoktur; harcama ekleme girişi
Günlük'teki kategori satırının `+` düğmesidir. Taşan FAB'ın yer açtığı
`.sekme-alan` (84) yerine düz `.sekme-cubugu` (68) kullanılır
(`rev2-tasarruf-profil.md` §1.1).
**İtilen ekranlarda ve sheet açıkken çubuk düşer.**

### `DayPager` (yeni — E-10)
Kahraman göstergeyi saran gün geçişi: iki 44pt `IconButton` + yatay
sayfalanan liste. `default` / `pressed` / `disabled` (sağ uç = bugün,
sol uç = ilk kayıt günü). **Nokta dizisi göstergesi yok** — oklar yönü
söyler, sınırı `disabled` gösterir. Sayfa yönü: **sol = geçmiş** (K-055);
jest yönü yalnız yazıyla söylenir.

### `MonthNav` (yeni — E-24)
`ay_secici`nin pasif oklu sürümü: `default` / `pressed` / `disabled`.
Pasif ok **gizlenmez** — gizlenen ok düzeni kaydırır.

### `ProgressBar` (yeni — E-25)
Tek oluk + dolgu + `n/8` metni. **8 segment çizilmez**: 390px'te 38px'lik
parçalara bölünür ve ilerleme okunmaz olur.

### `OrDivider` (yeni — E-22 · E-23)
Tek durum. **Çizgi yok**, ortalanmış tek sözcük ("ya da"): `line`/`bg`
kontrastı 1.08 — sayfa zemininde hairline görünmez (tokens §1.9).

### `BottomSheet`
Üst köşeler **32**, zemin `bg`, gölge `clay.raised-lg`, scrim
`rgba(28,57,142,0.38)`, 250ms. Üstte 44×4 tutamak (`line`).
Ekranın tamamını kaplamaz — arkadaki yüzey görünür kalır.
Durumlar: `open` / `closing` / `keyboard-open`.
**REV2:** "`keyboard-open` yoktur" hükmü düştü — tutar girişi artık native
`TextInput` olduğu için sistem klavyesi açılır ve sheet klavyeye göre
yükselir (`trinkow-rev.md` "Native para girişi").

### `RoutineSheet` (yeni — REV2 · kurulum 3/4 · Rutinler)
`BottomSheet`'in **üç bölgeli** varyantı: tutamak · kayan form (ad ·
kategori çip şeridi · günlük adet · birim fiyat · `MirrorWell` ayna kuyusu) ·
sabit alt blok (birincil düğme). Durumlar: `open` / `keyboard-open` /
`filled` / `error` / `edit` (başlık değişir + `ghost` "Rutini kaldır") /
`closing`. Ölçüler: `rev2-onboarding-kayit.md` §5.2.

### `SavingsSheet` (yeni — REV2 · Tasarruf)
Birikim hareketi girişi: `SegmentedControl` (ekle/çek) + native
`AmountWell` + `DateField` + `NoteField` + birincil düğme. İki kip:
`mode="create"` / `mode="edit"`; `edit` kipinde başlık değişir ve `ghost`
"Sil" eklenir. Form **sayfada değil sheet'tedir**
(`rev2-tasarruf-profil.md` §3.7).

### `Dialog`
**Yalnız yüksek etkili, geri alınamaz işlem için** (K-029): taksit serisi
silme · tüm verileri silme. Tek harcama silme **dialog açmaz**.
Yapı: çukur `danger-soft` ikon kabı → `h2` başlık → tek satır sonuç → ne
silineceğinin özeti → dikey butonlar: üstte "Sil" (`danger`), altında
"Vazgeç" (`ghost`). Limit aşımı **asla** dialog ile bildirilmez.

### `AppFooter` (yeni — REV2 · Profil)
Kaydırmanın sonunu kapatan alt bilgi: sürüm satırı (`micro`/`text-2`) +
iki yasal bağlantı (44pt `ghost` satırları). Kart değildir, gölge taşımaz.
Durumlar: `default` / `pressed` (bağlantı satırı).

### `StepIndicator`
Sayaç metni (`micro`) + oluklar; tamamlanan oluk `grad.action` dolgulu.
Oluk `well` + `clay.sunken`, yükseklik 8, radius 999. Yüzde yazılmaz.
**REV2 deltası:** kurulumda `toplam=4` · sayaç metni **bileşenin dışında**
yaşar · dolum animasyonlu · **dolu oluğun renkli gölgesi kaldırıldı** ·
bileşen `SetupShell`'in **sabit** bölgesinde durur
(`rev2-onboarding-kayit.md` §2.1).

---

## 5. Geri bildirim ve durum ekranları

### `Toast`
tokens.md §7.9. Zemin `surface`, radius 24, `clay.raised-lg`, üstte
`insets.top + 8`. Sol **8pt daire** gösterge: `primary` (bilgi) ·
`warning` (limit dışı) · `danger` (yıkıcı sonuç).

| Varyant | Süre | Not |
|---|---|---|
| `info` | 4 sn | Kaydedildi, güncellendi |
| `warning` | 4 sn | "{tutar} kaydedildi · {fark} limit dışı" |
| `undo` | **6 sn** | "Geri al" eylemli: tek harcama silme, limit kaldırma, "Tekrarla". **Geri alma penceresi = toast'ın ömrü** (K-029); düğme kaybolduğu an işlem kalıcıdır |

Eylem/kapatma hedefi 44×44. Limit aşımı modal ile bildirilmez.

### `EmptyState`
tokens.md §7.8. `EmptyGauge` → `h2` → `body` tek satır → (varsa) birincil
buton. Aralar 12/8/12. Her yüzeyde **farklı metin** (`metinler.md` §13);
aynı cümle tekrar edilmez. Buton yalnız kullanıcının **buradan**
yapabileceği bir iş varsa konur (E-15 ve E-18'de yoktur).

### `ErrorState`
`h2` başlık + `body` açıklama + buton "Yeniden dene". İllüstrasyon 96pt
çukur daire (boş durumdan **farklı**). Teknik hata kodu, "Ayrıntıyı gör"
kapısı ve depolama/mimari açıklaması **yoktur**.

### `Skeleton`
Gerçek düzenin kabarık kutuları yerinde durur, **içleri** `well` +
`clay.sunken` çukur bloklara döner. Blok genişlikleri gerçek içeriğin
genişliğine yakın tutulur. **Shimmer yok**, tam ekran spinner yok;
spinner yalnız buton içinde. Yalnız ≥150ms okuma için.

### `ProfilingSheet` (F-12 — eski `ProfilingPrompt`)
Pano içinde kart değil, **bottom sheet** (E-20): `micro` gün sayacı +
kapatma → `h1` tek soru → `caption` karşılığı → 2-4 `OptionCard` →
"Şimdi değil" (`ghost`, tam genişlik).
Kuralları: günde **en fazla 1**, toplam **3** soru, reddedilen soru
**14 gün** geri gelmez, üçü de cevaplanınca bileşen kaybolur.
Cevaptan sonra **panoda ne değiştiği gösterilir** (bilgi şeridi + yeni kart).
Durumlar: `default` / `pressed` / `dismissed` / `hidden`.

### `OptionCard`
Tam genişlik seçim kartı (kurulum + profilleme): `secim-kart`.
`default` kabarık · `selected` **çukur yüzey** (`clay.sunken` +
`primary-soft`; ikon kabı varsa tersine kabarır) · `pressed`.
**İç çizgi/halka yoktur** — v4.0'daki "2pt `primary-text` iç çizgi" cümlesi
K-061/2 öncesine aitti ve düzeltildi (tokens §5.4 · REV2 ·
`rev2-onboarding-kayit.md` §3.1). Kurulum 1/4'te **varsayılan seçim yoktur**:
üç kart da `default` ile açılır.
Seçenekler **eşit ağırlıktadır** — "Söylemek istemiyorum"
küçültülmez, griye çekilmez, en alta sürülmez.

### `InfoStrip`
Çukur bilgi şeridi: ikon + 1-2 satır `caption`. Varyantlar: `info`
(`primary-soft`) · `warning` (`warning-soft`) · `danger` (`danger-soft`,
yalnız `Dialog` içinde). Yargı içermez, sonucu söyler.

### `FactStrip` (yeni varyant — REV2 · Profil)
`InfoStrip`'in **nötr ve dokunulamaz** kipi: zemin `well` (`primary-soft`
değil), 20pt ikon + `label` olgu + `caption` bağlam. Yeni ölçü/renk/ikon
açmaz; tek kullanıcısı `IdentityPanel`'in `signed-in` hâlidir
(`rev2-tasarruf-profil.md` §4.2.1). Ayrı odak almaz.
Durumlar: `default` / `skeleton`.

### `MilestoneOverlay` (yeni — E-10 · seri durağı)
Üst banda `absolute` tek kart (96pt disk + radius 32 + `clay.raised-lg`).
`visible` / `pressed (atla)`. **Scrim yok, modal değil**, sekme çubuğunu
engellemez. Zaman çizelgesi 250 + 700 + 250 = 1.200ms (tokens §8).
Milestone başına **bir kez**. Konfeti, rozet, puan **yok** (K-048).

### `NoSpendDayCard` (yeni — E-10)
Harcamasız gün işaretleme: ikincil buton → işaretlendikten sonra yerini
`InfoStrip`'e bırakır ("Harcamasız gün. Seriye sayıldı.").

### `ResetSentCard` (yeni — E-22)
`default`. İçinde `button.secondary` `disabled` + gerekçe satırı
("60 saniye sonra yeniden gönderebilirsin.").

### `AccountSection` (yeni — E-19)
`signed-in` (e-posta çukuru + sağlayıcı satırı + Çıkış yap + Hesabı sil)
/ `signed-out` (tek nötr satır).
**K-080 düzeltmesi:** v4.0'daki "hesap hiçbir özelliği kilitlemez" (K-052)
cümlesi **geçersiz** — hesap zorunludur, "hesapsız devam et" kaldırıldı ve
uygulama giriş ekranıyla açılır. Bölüm artık bir davet değil, var olan
hesabın yönetim yüzeyidir; Profil'de karşılığı `IdentityPanel`'dir.

### `LegalConsentText` — **kullanımdan düştü (REV2)**
Yasal onay artık **iki `Checkbox`**'tır; onay cümlesi bağlantı taşımayan düz
`caption`, belgeler grubun altındaki iki 44pt `ghost` satırından açılır.
İç içe `Text onPress` çözümü RN'de 44pt dokunma hedefi üretemediği için
inşa edilemezdi (`rev2-onboarding-kayit.md` §7.0). Dosya
(`LegalConsentText.tsx`) repoda duruyor ama **hiçbir ekranda çağrılmıyor**;
silinip silinmeyeceği PM kararıdır (`rev2-onboarding-kayit.md` §12/6).
Yaşayan bileşen sayımına **girmez**.

### `NeutralIconBox` (yeni — E-25 · E-26)
48×48 · radius 16 · `primary-soft` + `primary-text`. **Kare, daire
değil** ve satırın solunda: "daire ikon + başlık + tek cümle" şablonundan
kaçınmanın yapısal karşılığı.

### `EmptyGauge` (eski `TallyGraphic`)
Markanın çizim primitifi v3'te **kil yayın kendisidir**: 176pt çukur disk +
oluk, dolgu ve topuz yok, ortasında 32pt ikon. Boş durumlarda ikon değişir
(kayıt yok → `notebook-text`, kategori → kategori ikonu, taksit →
`calendar-clock`). Stok illüstrasyon, maskot, avatar **yasak**.
v1/v2'nin hairline "çentik" primitifi **kullanılmaz**.

---

## 6. Bileşen sayımı ve kapsam dışı

**Sayım yöntemi (v4'te sabitlendi):** bu dosyadaki `###` bileşen
başlıklarının sayısı. Mekanik olarak doğrulanabilir; iki yerde farklı
sayı tutulmaz (K-040).

| Sürüm | Yaşayan bileşen başlığı |
|---|---|
| v1.0 | 27 |
| v3.1 (Tur E) | 41 (metinde "34" yazıyordu — sayım yöntemi yazılı değildi) |
| v4.0 | 70 (+30 yeni · `Divider` kaldırıldığı için sayılmaz) |
| **v4.1 (REV2 senkronu)** | **81** (+12 yeni başlık · `LegalConsentText` kullanımdan düştüğü için sayılmaz; `Divider` de sayılmaz) |

v4.1'de eklenenler (12): `Checkbox` · `SetupShell` · `MoneyField` ·
`MoneyRow` · `RoutineSheet` · `SavingsSheet` · `RoutineRow` ·
`SavingsMovementRow` · `CategoryShareRow` · `IdentityPanel` · `FactStrip` ·
`AppFooter`. Hepsi kodda mevcuttur (`../mobile/src/components/`).
`ClayKeypad` ve `LegalConsentText` **çağrılmıyor**; dosyaları silinene kadar
repoda durur, sayıma girmez (`Fab` ise çubuktan kaldırıldı).

v4'te eklenenler (30): `SocialAuthButton` · `Slider` · `FrequencyChips` ·
`PasswordField` · `PasswordRuleLine` · `SearchField` · `ValueWellRow` ·
`StreakDayGrid` · `MonthGrid` · `MilestoneRail` · `StreakSummaryWell` ·
`StreakPill` · `ShareBar` · `ShareRow` · `EquationRow` · `MirrorWell` ·
`CategoryGroupRow` · `SearchResultRow` · `RecentChip` · `SuggestionTag` ·
`DayPager` · `MonthNav` · `ProgressBar` · `OrDivider` ·
`MilestoneOverlay` · `NoSpendDayCard` · `ResetSentCard` ·
`AccountSection` · `LegalConsentText` · `NeutralIconBox`.

Kendi başlığı olmayan **varyantlar** (yeni bileşen değil, kayıt için):
`TextField` sağ yuvası · `DayBox` sayı-only + `pasif` · `Chip` metin
varyantı · `CategoryPicker`'ın değer satırı hâli · `Skeleton`'ın arama
iskeleti · `BottomSheet`'in limit önerisi yüzeyi · `SectionHeader`'ın
arama grup başlığı · tutar kuyusu içindeki `gun-btn` ·
**REV2:** `LimitGauge`'ın `mod="birikim"` kipi · `MonthPager` (`DayPager`ın
ay karşılığı, kendi dosyası yok) · `SettingRow`'un gezinme kipi (sol nötr
ikon kabı + `chevron-right` + değer satırı) · `RevScreen`'in
`header?` / `contentGap?: 0 | 24` prop'ları (`contentGap: 0` **yalnız**
Tasarruf ve Profil'de).

**Ekran parçası bileşim dosyaları** (`src/components/tasarruf/`, REV2 ·
kendi başlıkları yok çünkü yeni primitif değil, yukarıdaki bileşenlerin
ekran düzeyinde birleşimi): `SavingsHeroCard` · `BudgetCard` ·
`RealSavingsCard` · `MovementsSection` · `CategoryDistributionCard` ·
`RoutineSavingsCard` · `SavingsSkeleton`.

Faz 1'de **üretilmeyecekler** (istenirse PM'e sorulur): grafik kütüphanesi
tabanlı pasta/çizgi grafik, filtre paneli, avatar, **rozet/başarım/puan/
seviye/lig**, karanlık mod anahtarı, 4. sekme, karusel, `Accordion`,
`Tooltip`, şifre gücü çubuğu, paylaşım yüzeyi.

> **K-054/3 düzeltmesi (v4):** bu liste v3.1'de "takvim ızgarası" ve
> "arama çubuğu" da diyordu. İkisi de **MVP'ye alındı** ve üretildi:
> gün/seri ızgarası (`StreakDayGrid`, `MonthGrid` · K-048/K-050) ve ürün
> arama (`SearchField` · K-050). **Rozet / başarım / puan hâlâ kapsam
> dışıdır** (K-048): seri bir **sayaçtır**, ödül ekonomisi değildir.

---

## 7. Denetim listesi (`design-reviewer` bu dosyaya karşı bakar)

| # | Kontrol | Beklenen |
|---|---|---|
| 1 | Her etkileşimli bileşende `pressed` | Var (gölge çöker, `scale` yok) |
| 2 | Her clay yüzeyde `inset` gölge | Var — yoksa clay uygulanmamıştır |
| 3 | Gölge katman sayısı | Kabarık 4 · basılı 3 · çukur 2 |
| 4 | Dokunma hedefi | ≥ 44×44 (hitSlop dahil) |
| 5 | `disabled` opaklıkla mı verilmiş? | Hayır, renk + `clay.sunken` |
| 6 | `LimitGauge` renk değişimi | Yalnız taşma yayı (`warning`), doluluğa göre asla |
| 7 | Kategoride renk tek başına | Hayır: renk + ikon + metin |
| 8 | Skeleton parıldaması / tam ekran spinner | Yok |
| 9 | Ekranda birincil buton sayısı | ≤ 1 |
| 10 | Ekranda 56pt sayı | ≤ 1 |
| 11 | `Dialog` nerede açılıyor? | Yalnız taksit serisi + tüm veri silme |
| 12 | `undo` toast süresi | 6 sn, pencere = toast ömrü |
| 13 | Emoji / ünlem | Yok |
| 14 | Tasarımdaki isim = kod dosyası adı | Birebir |
| 15 | "Seçili" anlatımı | Derinlik + zemin (+ ikon kabarması). **Halka yok** (tokens §5.4) |
| 16 | Metin taşıyan mavi yüzeyde gradyan | Yok → düz `primary-deep` (K-062) |
| 17 | Rozet / puan / seviye / konfeti | Yok (K-048) |
| 18 | Katalog/öneri sayısında uydurma fiyat | Yok — fiyatı yalnız kullanıcı yazar (K-050) |
| 19 | Üçüncü taraf düğme (Apple/Google) | Kap bizim, dolgu/logo/etiket sağlayıcının; yeniden renklendirilmemiş (K-057/2) |
