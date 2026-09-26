# rev2 · Kurulum (onboarding 1-4) + E-16 Hesap oluştur — tasarım delta spesifikasyonu

24 Eylül 2026 · `ui-ux-designer`. **Görsel otorite değişmedi:**
`projects/trinkow/docs/brand/tokens.md` **v4 (claymorphism)**. Bu belgede yeni renk,
yeni punto, yeni radius, yeni boşluk, yeni font, yeni ikon seti **üretilmedi**.
Yalnız **bir yeni bileşen** var (`Checkbox`) ve o da mevcut jetonlarla kuruldu.

| | |
|---|---|
| Kapsam | `app/onboarding.tsx` (4 adım) · `app/kayit.tsx` (E-16) |
| Kapsam dışı | Günlük · Tasarruf · Profil · Harcama ekle (paralel görev) |
| Çizili karşılık | `prototip-rev2/onboarding-kayit.html` — **20 yüzey**, 390×844 |
| Üreteç | `prototip-rev2/_uret/uret_onboarding_kayit.py` |
| Stil kaynağı | `prototip-v4/stil.css` + `prototip-rev2/stil-rev2.css` **§3-§7** (bu turda eklenen CSS: `.onay-*`, `.para-kuyu`, `.adim-dolu` gölge iptali, `.btn-ghost.belge`, `.sheet-bolgeli`) |
| Mekanik denetim | `prototip-v4/_uret/denetim.py` → **0 bulgu / 20 yüzey**; `stil-rev2.css` tokens §1 palet + §12/9 radius + RN yasak dizeleri → **0 bulgu** |
| Revizyon | **REV2-r1** · 24 Eylül 2026 — `design-reviewer`ın 5 bloklayıcı + 6 önemli bulgusu kapatıldı. Kalem kalem: **§13** |
| Bağlayıcı kısıt | `agency/reference/rn-tasarim-kisitlari.md` · `agency/reference/jenerik-ai-ui-anti-pattern-listesi.md` |

**Neden bu tur var:** kodda kurulum akışı `RevScreen title={"Kurulum · 1/4"}`
ile çiziliyordu; adım numarası ekranın en büyük tipografik öğesiydi ve
seçim/ilerleme kontrolleri üst üste dizilmiş sade `Button`'lardı. Onaylı v4
tasarımı (`prototip-v4/03-onboarding.html`) bunu hiç böyle söylemiyordu —
**kod tasarımdan saptı**. Bu belge sapmayı kapatır ve üstüne Mustafa'nın
istediği dört deltayı yazar: estetik adım göstergesi · seçenek kartları ·
motive edici metin · yasal onay kutuları + şifre tekrarı.

---

## 0. Akış ve ekran envanteri

```
E-15 Giriş ──"Hesap oluştur"──▶ E-16 Hesap oluştur ──başarılı kayıt──▶
   KURULUM 1/4 niyet ──▶ 2/4 gelir ve gider ──▶ 3/4 rutinler ──▶ 4/4 plan özeti
   ──"Trinkow'u kullanmaya başla"──▶ E-10 Günlük
```

| Ekran | İşi | Zorunlu mu | Geri yolu |
|---|---|---|---|
| E-16 | Hesap açmak (K-080: hesap zorunlu, "hesapsız devam" yok) | Evet | Başlıktaki geri oku → E-15 |
| 1/4 niyet | Tek karar: kullanıcı neyi hedefliyor (`'takip' \| 'tasarruf' \| 'borc'`) | Evet (varsayılan `tasarruf` **seçili gelmez**, kullanıcı seçer) | Yok (ilk adım) |
| 2/4 gelir ve gider | Bütçe verisi → `budgetPut` | Gelir zorunlu, diğerleri değil | Başlıktaki geri oku |
| 3/4 rutinler | Günlük tekrar eden harcamalar | Hayır ("Rutin harcamam yok") | Başlıktaki geri oku |
| 4/4 plan özeti | Sonucu göstermek + akışı kapatmak | Evet | Başlıktaki geri oku (girdi silinmez) |

**Ekran başına mood** (her adım birbirinin klonu değil, hepsi aynı aile):

| Adım | Mood | Nasıl kuruldu |
|---|---|---|
| 1/4 | **Ferah, tek karar** | Ekranda 3 nesne: başlık, üç kart, tek düğme. Sayı yok, kart yok, oluk yok |
| 2/4 | **Berrak hesap masası** | Kartsız bölüm başlıkları + kabarık kartların içinde çukur kuyular; tabular rakam ekranın dokusunu belirler |
| 3/4 | **Tezgah** | Liste + tek ikincil eylem; veri girişi sheet'e taşındı, ekran sakin kalır |
| 4/4 | **Sessiz kutlama** | Tek 56pt sayı, mavi kil panel (`primary-soft`), altında kullanıcının kendi yazdığı değerler. Konfeti/rozet/puan yok (K-048) |
| E-16 | **Kapı** | Dikey tek kolon, üçü bir arada karar: e-posta yolu · sosyal yol · iki onay |

---

## 1. Tasarım temeli (tokens.md'den — burada yeniden tanımlanmıyor, sabitleniyor)

| Eksen | Bu iki ekranda kullanılan **tam** küme |
|---|---|
| Boşluk | `4` (aynı nesnenin iki satırı) · `8` (etiket↔girdi, aynı grubun tekrarı) · `12` (kart içinde iki blok, "ya da"nın iki yanı) · `16` (iç boşluk / ekran kenarı) · `24` (ekran düzeyinde iki blok, içerik alt boşluğu) |
| Punto | `micro 12` (adım sayacı) · `caption 13` · `label 13` · `body 16` · `body-strong 16` · `amount 17` · `h2 19` · `h1 26` · `display 32` · `hero 56` (**yalnız 4/4'te, tek**) |
| Radius | `16` (kuyu, kutu, şerit, onay kutusu) · `24` (kart, seçim kartı) · `32` (kahraman panel) · `999` (düğme, adım oluğu) · odak halkası eleman + 4 |
| Gölge | `clay.raised` (nesne) · `clay.sunken` (kuyu / oluk / seçili) · `clay.pressed` (parmak altında) · `clay.action` / `clay.action-pressed` (yalnız birincil düğme) |
| Renk | `bg` zemin · `surface` kart · `well` kuyu · `groove` basılı · `primary-deep` birincil düğme ve işaretli onay kutusu · `primary-soft` seçili kart + kahraman panel · `primary-text` bağlantı/odak · `warning-*` düzeltilebilir hata · `danger` yalnız **form hatası kenarlığı ve metni** |
| Yükseklik | `44` (ikon düğmesi, onay satırı, kompakt kuyu) · `52` (ikincil düğme) · `56` (birincil düğme, metin/para kuyusu) · `68` (liste satırı) |

**Kontrast** (tokens §1.9'daki hesaplanmış çiftler): `text`/`surface` 10.37 ·
`text`/`bg` 8.96 · `text`/`surface` (onay cümlesi, 13pt) 10.37 ·
`text-2`/`surface` 5.94 · `text-2`/`bg` 5.13 · hata metni `danger-ink`/`bg`
4.97 · bağlantı `primary-text`/`bg` 5.12 · beyaz onay glifi `primary-deep`
üstünde 5.37 · beyaz düğme metni `primary-deep` 5.37 / `primary-press` 6.59.
**Bilinen sınır:** para kuyusundaki placeholder `0` `text-3`/`well` çiftidir
(tokens §1.2: `well` üstünde 4.50 — sınırda). Bu yüzden placeholder
**tek karakterdir ve bilgi taşımaz**; alanın anlamı üstteki `label`/`text-2`
etikettedir (5.13 ✅). Etkin hiçbir metin AA altında değildir.

**Hareket** (tokens §8): `motion.press` 150ms · `motion.arc` 250ms ·
reduce-motion → 0ms. Spring, overshoot, `scale`, shimmer, konfeti yok.

---

## 2. Kurulum kabuğu (`SetupShell`) — dört adımın ortak çerçevesi

`RevScreen` **kullanılmaz** (başlığı `h1` basıyor, "Geri"/"Ayarlar" ghost
düğmeleri koyuyor, kart iç boşluğunu 24 yapıyor — üçü de tokens'a aykırı).
Kurulumun kendi kabuğu var:

```
[safe area top]
╔═ EKRANA SABİT — ScrollView'ın DIŞI, kardeşi (B2) ══════════════════╗
║ ekran-basi          8 üst / 16 alt · 16 yan                        ║
║   sol   44×44 IconButton chevron-left  (1/4'te 44×44 denge kutusu) ║
║   orta  micro "n/4"   ← ekranın TEK adım göstergesi metni          ║
║   sağ   44×44 boş denge kutusu                                     ║
║ adım çubuğu         16 yan · 4 oluk · h 8 · aralar 8 (kap −8)      ║
╚════════════════════════════════════════════════════════════════════╝
[kaydırılan içerik — adıma özel]    ← ScrollView BURADA başlar
  24                  ← kayan içeriğin üst boşluğu (çubuk ↔ h1)
  … adımın kendi gövdesi …
  24                  ← içerik alt boşluğu
alt-sabit             8 üst · 16 yan          ← ScrollView'ın DIŞI
  (gerekiyorsa caption ipucu + 8) + birincil düğme 56
  (+ gerekiyorsa 8 + tam genişlik ghost)
[home indicator 28]
```

| Kural | Değer |
|---|---|
| `h1` "Kurulum" ya da "Kurulum · 1/4" | **Kaldırıldı.** Adım numarası içerik değil, konumdur → 12pt `micro`/`text-2` + oluk deseni |
| Her adımın `h1`'i | O adımın **kendi sorusu/başlığı** (26pt Poppins), içeriğin ilk satırı |
| Klavye açıkken | `KeyboardAvoidingView` (`padding`/`height`): odaklı alan **ve** alt-sabit blok görünür kalır; adım çubuğu kaydırma alanının dışında olduğu için yerinde durur |
| Geri | Yalnız başlıktaki 44pt ikon düğmesi. `Button variant="ghost" label="Geri"` **kullanılmaz** — ikincil eylem görsel olarak zayıf ama dokunma hedefi tam 44 |
| Ekran başına birincil düğme | **1** |
| **Sabit bölge ↔ kayan bölge** (B2) | `ekran-basi` ve adım çubuğu `ScrollView`ın **kardeşidir**, çocuğu değil: `<View>{başlık+çubuk}</View><ScrollView>{gövde}</ScrollView><View>{alt-sabit}</View>`. Gerekçe: iki satır kaydırma alanının içindeyken 2/4 formu aşağı kaydırıldığında **adım göstergesi ekrandan çıkıyordu** — ilerleme göstergesi kaydırmayla kaybolamaz (ve geri oku her an erişilebilir kalmalı) |

### 2.1 `StepIndicator` deltası

| | Bugün (kodda) | rev2 |
|---|---|---|
| `toplam` | varsayılan **3** | çağrı `toplam={4}`; varsayılan 3 kalır (profilleme sheet'i onu kullanıyor) |
| Metin | Ekran başlığında `t['ob.adim']` = "Adım 1/3" | `ob.sayac` = **"{adim}/4"** · rol `micro` · renk `text-2` · başlık çubuğunun **ortasında** |
| Oluk | `well` + `clay.sunken`, h 8, radius 999, aralar 8 | Aynı — değişmedi |
| Dolgu | `grad.action` (metin taşımaz → izinli) + **renkli gölge** | `grad.action` aynı; **gölge kaldırıldı**. v4'ten devralınan `0 2px 4px -1px rgba(47,104,197,0.45)` tokens §5.2'ye aykırıydı (renkli gölge yalnız `clay.action`; gölgeli yüzey zemini `surface`/`primary-deep` olmalı). Dolu oluk kabarık bir nesne değil, **oluğun içindeki dolgudur** — derinliği oluğun `clay.sunken` çukurluğu verir |
| Animasyon | yok | Dolan oluk `motion.arc` 250ms `ease-out` **genişlik** animasyonu; yalnız yeni dolan oluk animasyonlanır |
| a11y | `progressbar` + `accessibilityValue` | Aynı, `max: 4`; `accessibilityLabel` = `a11y.kurulum_ilerlemesi` ("Kurulum ilerlemesi") |
| Yasak | — | Yüzde yazmak · segment üstüne sayı basmak · nokta dizisi (dot indicator) |

### 2.2 Adımlar arası geçiş (RN'de inşa edilebilir)

Tek `Animated.Value` (`0→1`), yalnız `opacity` + `translateX` (ikisi de
`useNativeDriver: true`). Reanimated/yeni bağımlılık **gerekmez**.

| Yön | Çıkan adım | Giren adım |
|---|---|---|
| İleri | 150ms: `opacity 1→0`, `translateX 0→-8` | 250ms: `opacity 0→1`, `translateX 8→0` |
| Geri | 150ms: `opacity 1→0`, `translateX 0→8` | 250ms: `opacity 0→1`, `translateX -8→0` |

| Kural | Değer |
|---|---|
| Animasyonlanan alan | **Yalnız kaydırılan içerik.** Başlık çubuğu, adım çubuğu ve alt-sabit blok **yerinde durur** — birincil düğme parmağın altından kaçmaz |
| `scale` / spring / overshoot | Yok (tokens §8 yasak listesi) |
| `reduceMotion` | Süreler 0ms; içerik anında değişir |
| Kaydırma konumu | Yeni adım **en üstten** başlar (`scrollTo({y:0, animated:false})`) |

---

## 3. Adım 1/4 — niyet

```
[kabuk — sabit: başlık çubuğu + adım çubuğu]
24
h1        "Hadi başlayalım"                       26/32 Poppins · text
8
body      "Neyi hedefliyorsun? Günlük harcama     16/24 · text-2
           limitini buna göre kuruyoruz."
24
OptionCard  Birikim yapmak
8
OptionCard  Paramı kontrol altına almak
8
OptionCard  Borcumu bitirmek
24 (içerik alt boşluğu)
─ alt-sabit (8 üst / 16 yan) ────────────────────────────────
  caption  "Birini seçince devam edebilirsin."    ← YALNIZ seçim yokken
  8
  birincil "Devam"                                ← seçim yokken pasif
```

Bu adım 390×844'te **kaydırmaz** (içerik ≈ 474pt, ipucu satırıyla 500pt).

### 3.0 Adım 1/4'ün üç hâli — **ilk hâl varsayılan hâldir** (B3)

Varsayılan niyet kaldırıldığı için **her kullanıcının gördüğü ilk ekran**
"hiçbir kart seçili değil"dir. Prototipin ilk yüzeyi budur.

| Hâl | Kartlar | Birincil | İpucu satırı |
|---|---|---|---|
| **ilk (varsayılan)** | Üçü de `default` — kabarık, hiçbiri çukur değil | `disabled` | **Görünür** (`ob.niyet.ipucu`) |
| seçim yapıldı | Seçilen kart çukur + ikon kabı kabarık | etkin | Düşer (yer tutmaz, düğme yukarı kaymaz: satır 18 + 8 boşluk kadar alan serbest kalır ve alt-sabit blok aşağı oturur) |
| parmak altında | Dokunulan kart `groove` + `clay.pressed` | değişmez | değişmez |

| `ob.niyet.ipucu` kuralı | Değer |
|---|---|
| Konum | **Alt-sabit bloğun İÇİNDE**, birincil düğmenin **üstünde**, arası **8** |
| Neden orada | Cümle kartları değil **pasif düğmeyi** açıklıyor: "neden dokunamıyorum" sorusunun cevabı sorunun yanında durur. Kartların altına konsaydı 24'lük içerik boşluğunun içinde asılı kalırdı ve uzun yazı boyutunda düğmeden kopardı |
| Görünürlük | Yalnız `niyet === null` iken. Seçimden sonra **silinir** (ikinci bir "hazırsın" cümlesi yazılmaz) |
| Rol / renk | `caption` 13 / `text-2` (`bg` üstünde 5.13 ✅). Kırmızı değil — bu bir hata değil, bir yön |

**Başlık kararı (kapsam dışı, kayıt için):** `h1` "Hadi başlayalım"
Mustafa'nın birebir direktifidir ve **değişmedi**. Ekranın ayırt ediciliğini
başlık değil **alt satır** taşıyor: "Neyi hedefliyorsun? Günlük harcama
limitini buna göre kuruyoruz." — cümle 1. adımı 4. adımın çıktısına
(`ob.ozet.limit_etiket` = "Günlük harcama limitin") bağlar; jenerik bir
karşılama cümlesi değil, **sorunun sonucunu** söyler.

### 3.1 `OptionCard` — ölçüler ve durumlar (delta: netleştirme)

| Özellik | Değer |
|---|---|
| Genişlik / radius | Tam genişlik (ekran kenarı 16) · `radius.card` **24** |
| İç boşluk | **16** (istisnasız) · ikon kabı ↔ metin arası **16** |
| Yükseklik | İçerikten gelir: `body-strong` 24 + 8 + `caption` 18 = 50 → kart **82** (ikon kabı 48 < 50) |
| İkon kabı | **48×48**, radius 16, `groove` + `clay.sunken`, içinde **24pt** Lucide ikon `primary-text` |
| Başlık / destek satırı | `body-strong`/`text` · `caption`/`text-2`, arası **8** |
| Metin taşması | Başlık `numberOfLines={2}`, destek satırı `numberOfLines={2}`; kart büyür, kırpma son çare |

| Durum | Görünüm |
|---|---|
| `default` | `surface` + `grad.clay-face` + `clay.raised`; ikon kabı **çukur** |
| `selected` | Zemin `primary-soft`, gölge **`clay.sunken`** (kart çukura iner) + ikon kabı **tersine kabarır** (`surface` + `clay.raised` + parlama). **Halka yok, onay ikonu yok** (tokens §5.4 · K-061/2) |
| `pressed` | Zemin `groove` + `clay.pressed` (seçili kartta da aynı) — 150ms, `scale` yok |
| `focused` | 2pt `primary-text` dış halka, 2pt boşluk, radius 28 |
| `disabled` | **Yok** — üç niyetin hiçbiri pasifleşmez |
| Uzun metin | Yukarıdaki taşma kuralı; kart yüksekliği esner (RN'de yazı tipi ölçümü platforma göre oynar) |

> **Bileşen envanteri düzeltmesi:** `bilesen-envanteri.md` §5 `OptionCard`
> satırında hâlâ "`selected` çukur + **2pt `primary-text` iç çizgi**" yazıyor.
> Bu cümle K-061/2'den (halka kaldırıldı) **önceki** metindir; `stil.css`
> (`.secim-kart.secili`) ve `OptionCard.tsx` halkasız. Envanter satırı
> düzeltilmeli — bu belge halkasız dili uygular.

Seçim **tek kanal değildir**: derinlik + zemin + ikon kabının yön değiştirmesi
+ `accessibilityState={{ selected: true }}` (WCAG 1.4.1).

Varsayılan seçim **yoktur**: kodda `useState<Niyet>('tasarruf')` ile bir
seçenek baştan seçili geliyor ve kullanıcı hiç karar vermeden "Devam"a
basabiliyor. rev2'de `niyet: Niyet | null`, seçim yapılmadan birincil düğme
`disabled` (ipucu satırı: `ob.niyet.ipucu`).

---

## 4. Adım 2/4 — gelir ve gider

```
[kabuk]
24
h1      "Gelir ve gider"
8
body    "Gelirini ve giderlerini inceleyip sana en uygun planı kuruyoruz.
         Hedefine en kısa yoldan ulaşırsın."
24
SectionHeader  "Gelirin"                                   (kartsız, h2)
8
Card  ├ MoneyField "Aylık net gelir"                       (etiket 13 + 8 + kuyu 56)
      └ caption   "Eline geçen tutar, kesintiden sonrası."  (8 boşlukla)
24
SectionHeader  "Sabit giderlerin"        sağda toplam: label/text-2 "16.900 ₺"
8
Card  ├ MoneyRow "Kira ya da aidat"        56
      ├ 8  MoneyRow "Sabit faturalar"      56
      ├ 8  MoneyRow "Zorunlu ulaşım"       56
      └ 8  MoneyRow "Kredi ve taksitler"   56
24
SectionHeader  "Hedefin"
8
Card  ├ MoneyField "<niyete göre etiket>"  + caption
      └ 12  MoneyField "Kalan toplam borç" + caption
24
alt-sabit: birincil "Devam"
```

| Karar | Gerekçe |
|---|---|
| Bölüm başlıkları **kartın dışında** (`SectionHeader`) | Yedi para alanı tek kartta duvar gibi duruyordu; kartsız başlık üç anlamlı grup üretir ve kart iç boşluğu 16 tek değer olarak kalır |
| Sabit giderler **kompakt satır** (`MoneyRow`), gelir/hedef/borç **tam genişlik** (`MoneyField`) | Sabit gider etiketleri kısa ve aynı ailenin tekrarı; gelir ve hedef etiketleri uzun ("Aylık hedef borç kapatma") ve niyete göre değişiyor — 144'lük kuyunun yanında kırpılırdı |
| Sabit gider toplamı bölüm başlığının sağında | Kullanıcının kendi yazdığı sayıların aritmetiği; tahmin değil. `tabular-nums`, `label`/`text-2` |
| Kil tuş takımı **yok** | Rev kararı: `AmountWell` gerçek `TextInput`, `keyboardType="decimal-pad"`, iOS'ta `InputAccessoryView` → "Bitti" |
| Borç alanı her niyette görünür | `borc_kurus` niyet `'borc'` olmasa da anlamlı; gizlenirse veri kaybolur. Etiketin altında "Borcun yoksa boş bırakabilirsin." |

### 4.1 Niyete göre değişen etiket (bağlayıcı)

API alanı **değişmez**: `hedef_birikim_kurus`. Yalnız etiket değişir.

| `niyet` | `alan.hedef.*` etiketi |
|---|---|
| `tasarruf` | **Aylık hedef birikim** |
| `borc` | **Aylık hedef borç kapatma** |
| `takip` | **Aylık kenara ayırmak istediğin tutar** |

Aynı dil değişimi diğer alanlarda da geçerlidir: "maaş" sözcüğü **hiçbir
yerde kullanılmaz** → "gelir". (`alan.gelir` = "Aylık net gelir";
4/4 özetinde "Aylık gelirin".)

### 4.2 `MoneyField` (tam genişlik) — `TextField`/`AmountWell` deltası

| Özellik | Değer |
|---|---|
| Etiket | `label`/`text-2`, girdinin **üstünde**, arası 8. Placeholder'a gömülmez |
| Kuyu | Yükseklik **56**, radius **16**, `well` + `clay.sunken`, yatay iç boşluk 16, **kenarlık yok** |
| Değer | `amount` 17pt **tabular**, `text`, solda; sağ uçta `₺` `label`/`text-2` (bölünmez boşluk) |
| Placeholder | `0` · `text-3` |
| Klavye | `decimal-pad` · virgül/nokta ve yapıştırma kabul · iki kuruş hanesi · veri integer kuruş |
| Not satırı | Kuyunun altında 8 boşlukla `caption`/`text-2` |

| Durum | Görünüm |
|---|---|
| `empty` | Placeholder `0`; hata değildir |
| `focused` | `clay.sunken` + **2pt `primary-text`** halka; 3pt `primary` imleç |
| `filled` | Değer `amount`/`text`, binlik ayracı otomatik (`1.250.000`) |
| `error` | **2pt `danger`** kenarlık + altında 8 boşlukla `caption`/`danger-ink` |
| `disabled` | `disabled-bg` + `clay.sunken` + değer `text-2` (opaklık yok) — bu akışta kullanılmıyor |
| Uzun tutar | `1.250.000` 17pt'de kuyuya sığar (ölçü: 358 − 32 iç boşluk − `₺` 12 ≈ 300pt alan). Rol düşürme **gerekmez**; `hero`→`display` kuralı yalnız 56pt yüzeylerde |

### 4.3 `MoneyRow` (kompakt) — yeni **varyant**, yeni bileşen değil

`ValueWellRow`'un düzenlenebilir ikizi: solda etiket, sağda kuyu.

| Özellik | Değer |
|---|---|
| Satır | Yükseklik **56**, zemin yok (kartın/sheet'in içinde), etiket `body`/`text` |
| Kuyu | **144 × 44** (iki varyantta da aynı), radius 16, `well` + `clay.sunken`, iç boşluk 12; değer `amount` **sağa hizalı** |
| **`birim` parametresi** (B5) | Kuyunun son eki **parametredir**, gövdeye gömülü değil: `birim="₺"` → değer + **8** + `₺` (`label`/`text-2`) · `birim=""` → **son ek yok**. Kuyu genişliği iki durumda da **144** — aynı ailenin satırları hizada kalır |
| `birim="₺"` nerede | Sabit gider satırları (§4) · `RoutineSheet` "Birim fiyat" (§5.2) |
| `birim=""` nerede | `RoutineSheet` **"Günlük adet"** (§5.2) — integer alan. "2 ₺" yazılamaz; klavye `number-pad`, ondalık yok |
| Etiket ↔ kuyu | 12 |
| Satırlar arası | 8 |
| Dokunma hedefi | Satırın tamamı → kuyuya odaklanır (44'ün üstünde) |
| Durumlar | `empty` (`0` placeholder) · `focused` (2pt `primary-text`) · `filled` · `error` (2pt `danger`) |
| Hata metni | Hatalı satırın **hemen altında**, 8 boşlukla, `caption`/`danger-ink`. Kuyu 56 kalır, metin satırın **dışına** yazılır (satır yüksekliği bozulmaz, alttaki satırlar 26 kadar aşağı iner). Tek kural: kart içinde de, sheet içinde de aynı |
| **Uzun metin / büyük yazı** (Ö5) | `fontScale ≤ 1.3`: etiket tek satır kalır, sığmazsa `ellipsizeMode="tail"`. **`fontScale > 1.3`: `MoneyRow` dikey düzene döner** — etiket üstte tam genişlik (sarar, kırpılmaz), kuyu altında 8 boşlukla, satır yüksekliği 56 → 18+8+44 = **70**. Form etiketini kırpmak a11y hatasıdır; kuyu genişliği (144) iki düzende de sabittir |

### 4.4 Adım 2 durumları

| Durum | Ekran |
|---|---|
| `empty` (ilk giriş) | Tüm kuyular `0` placeholder; toplam satırı **"0 ₺"** yazar (satır gizlenmez — dürüstlük); birincil düğme `disabled` |
| Gelir boş + "Devam" | Gelir alanı `error`: "Planı kurmak için gelirini yazman gerekiyor." Odak gelir alanına gider |
| `loading` (kaydediliyor) | Birincil düğme: metin **"Plan kuruluyor"** + 20pt spinner, genişlik sabit, `disabled`; alanlar düzenlenemez ama görünür |
| `error` (yazma) | Formun **üstünde** `InfoStrip warning` + `wifi-off`: "Plan kaydedilemedi." / alt satır "Yazdıkların duruyor, yeniden deneyebilirsin." Birincil düğme etiketi "Yeniden dene" olur. Kırmızı **kullanılmaz** |
| Uzun metin / büyük yazı | `MoneyField` etiketi (kuyunun üstünde) daima sarar. `MoneyRow`: `fontScale ≤ 1.3`'te etiket tek satır (sığmazsa `tail` kırpma), **`fontScale > 1.3`'te satır dikey düzene döner** (etiket üstte tam genişlik + 8 + kuyu; yükseklik 70) — §4.3'teki **birebir aynı** kural. Kuyu genişliği 144 sabit |

---

## 5. Adım 3/4 — rutinler

```
[kabuk]
24
h1    "Günlük rutinlerin"
8
body  "Kahve, sigara, ulaşım gibi her gün tekrar edenler.
       Ekledikçe planın gerçeğe yaklaşır."
24
SectionHeader "Eklediklerin"          sağda "Günlük 240 ₺"
8
RoutineRow × n (68, aralar 8)
12
ikincil düğme "Rutin ekle"  (52, tam genişlik)
24
InfoStrip info "Rutinleri sonra Profil → Rutinlerim'den değiştirebilirsin."
24
alt-sabit: birincil "Plan özetine geç"  +8  ghost "Rutin harcamam yok"
```

| Karar | Gerekçe |
|---|---|
| Veri girişi **`BottomSheet`** içinde (`RoutineSheet`) | Ekranda iki birincil düğme olmaz; sheet klavyeyle birlikte yükselir (Rev kararı) ve adım sakin kalır. Adıma **ilk** girişte sheet kendiliğinden açılır (Rev: "doğrudan ekleme formunu açar"), kapatılınca liste/boş durum görünür |
| Kendiliğinden açılan sheet'in **çıkışı sheet'in içindedir** (B4/b) | Otomatik açılma korundu ama rutini olmayan kullanıcı artık scrim'e/`X`'e dokunmak zorunda değil: sheet'in en altında tam genişlik `ghost` **"Rutin harcamam yok"** durur ve ekrandaki aynı adlı çıkışın **birebir aynı işini** yapar (4/4'e geçer, rutin verisi yazılmaz). Aynı etiket = aynı eylem; kapatılmak zorunda olunan bir form bırakılmadı |
| 3/4'ün **gerçek ilk hâli** sheet'tir | Bu yüzden prototipte sheet dört yüzeyle çizildi (boş · klavye açık · dolu · düzenleme + hata); adımın kendi üç yüzeyi (liste · boş · yazma hatası) sheet kapatıldıktan sonrasıdır |
| Hazır rutin çipleri **yok** | Rev kararı + K-050: fiyatı ve adı kullanıcı yazar, uygulama fiyat uydurmaz |
| Satıra dokunmak = düzenle | "Rutini kaldır" sheet'in içinde `ghost` olarak durur; satırda yıkıcı hedef yok (yanlış dokunma maliyeti) |

### 5.1 `RoutineRow` (yeni **varyant** — `SpendRow` ölçüleri)

| Özellik | Değer |
|---|---|
| Satır | Min **68**, radius 16, `surface` + `clay.raised`, iç boşluk 12/16, satırlar arası 8 |
| Sol | 44×44 kategori kabı (`cat.*.soft` + `clay.sunken`, 20pt `cat.*.solid` ikon) |
| Orta | `body`/`text` ad (`numberOfLines={1}`) + `caption`/`text-2` "Her gün 2 × 45 ₺" |
| Sağ | `amount`/`text` günlük tutar (**asla kırpılmaz**) + 12 + 20pt `pencil` `text-2` |
| `pressed` | `groove` + `clay.pressed` |
| Uzun ad | `Marlboro Touch Blue 20'lik` → ad kırpılır, tutar korunur (tokens §7.6 kuralının satır karşılığı) |
| a11y | "Sabah kahvesi, her gün 2 × 45 ₺, günlük 90 ₺. Düzenle" |

### 5.2 `RoutineSheet` (`BottomSheet` varyantı) — **inşa edilebilir ölçüler** (B4)

Kap: üst köşeler **32** · zemin `bg` · `clay.raised-lg` · iç boşluk **16
(istisnasız)** · scrim `rgba(28,57,142,0.38)` · giriş/çıkış `motion.arc` 250ms
(yalnız `translateY`, `useNativeDriver`).

**Üç bölge** (klavyenin çözümü burada): sheet bir blok değil, üç bölgedir.

| Bölge | İçerik | Davranış |
|---|---|---|
| 1 · tutamak | 44 × 4, radius 999, `line` rengi, **yatayda ortalı**; sheet iç boşluğunun ilk satırı (üstten **16**), altında **12** | Sabit. Aşağı sürükleme kapatır |
| 2 · form | Aşağıdaki alanlar | **`ScrollView`** — klavye açıkken burası kayar |
| 3 · alt blok | 16 + birincil 56 (+ 8 + `ghost` 44) | Sabit. Birincil düğme **hiçbir durumda** klavyenin altında kalmaz |

**Form düzeni** (390 genişlikte iç alan = 390 − 32 = **358**):

```
tutamak 44×4                                  (üstten 16, altında 12)
h2      "Rutin ekle" / "Rutini düzenle"        19/25 Poppins
16
label   "Ne?"                                  13 · text-2
8
TextField  56 · radius 16 · well + sunken      ph "Sabah kahvesi"
16
label   "Kategori"                             13 · text-2
8
CategoryPicker  yatay şerit · çip 40 · aralar 8
   Kafe · Ulaşım · Market · Fatura · Abonelik · Alışkanlıklar · Tüm kategoriler
16
MoneyRow  "Günlük adet"   kuyu 144×44 · birim YOK · number-pad
8
MoneyRow  "Birim fiyat"   kuyu 144×44 · birim ₺   · decimal-pad
[hata]    8 + caption/danger-ink (hatalı satırın hemen altında)
[16 + MirrorWell]   ← yalnız iki alan da doluysa
────────────────────── (bölge 3, sabit)
16
birincil  "Rutini ekle" / "Değişikliği kaydet"  56
8
ghost     "Rutin harcamam yok" (ekleme) / "Rutini kaldır" (düzenleme)  44
```

| Parça | Ölçü / davranış |
|---|---|
| `CategoryPicker` çipi | tokens §7.6: yükseklik **40** · radius 999 · yatay iç boşluk **16** · aralar **8** · `label` 13. Pasif: `surface` + `clay.raised` + `text-2`. Seçili: `cat.*.soft` + `clay.sunken` + **solda 8pt `cat.*.solid` nokta** + metin `text`. Halka ve onay ikonu yok. Şerit **yatay kaydırır** (RN: `horizontal ScrollView`), çip `flexShrink: 0` — daralmaz, sarmaz |
| Son çip | "Tüm kategoriler" — 13 kategorinin tamamını açar (E-11'in kategori ızgarası). Hazır **rutin** önerisi değildir: ad ve fiyat kullanıcının (K-050) |
| `MirrorWell` | `well` + `clay.sunken` · radius **16** · iç boşluk **12/16** · tam genişlik (358 − 32 = 326). Üst satır: solda `body-strong` "Ayda", sağda `amount` tabular tutar. Altında **4** boşlukla `caption`/`text-2` **formül**: "Her gün 2 × 45 ₺ × 30 gün". v4 E-25'teki ayna kuyusuyla **aynı** bileşen — yeni geometri açılmadı |
| `MirrorWell` ne zaman | Yalnız **adet ve fiyat birlikte** doluyken. Boşken yer tutmaz (iskelet çizilmez), silinince kaybolur |
| Doğal yükseklik | **513pt** (aynasız) / **599pt** (aynalı). Klavye kapalıyken kullanılabilir alan 844 − 47 (durum çubuğu) − 28 (home) = **769pt** → kaydırmaz |
| Klavye açık | Gerçek cihazda iOS TR klavyesi + öneri çubuğu ≈ **291pt** → sheet'e kalan ≈ **475pt** < 513 → **bölge 2 kaydırır**, bölge 1 ve 3 yerinde durur. **Prototip notu:** HTML'deki sistem klavyesi bölge [A] temsilidir ve 224pt'dir (kalan 545pt) — o yüzden yüzey 7'de kaydırma görsel olarak tetiklenmez; yüzey **yapıyı** (üç bölge + görünür kalan birincil düğme) gösterir, ölçüyü cihaz verir |

| Durum | Görünüm |
|---|---|
| `open` (boş) | Ad boş (`text-3` placeholder), kategori seçilmemiş, iki kuyu `0`; birincil **pasif** (ad ve fiyat zorunlu) |
| `keyboard-open` | Odaklı alan 2pt `primary-text` + 3pt imleç; form kayar, birincil görünür |
| `filled` | `MirrorWell` görünür, birincil etkin |
| `error` | Eksik alanın kuyusu 2pt `danger` + **hemen altında** `caption`/`danger-ink` (`hata.rutin_fiyat_bos`). `MirrorWell` düşer — eksik veriyle hesap gösterilmez |
| `edit` (düzenleme kipi) | Başlık "Rutini düzenle", birincil "Değişikliği kaydet", alt çıkış **"Rutini kaldır"**. Yıkıcı hedef listede değil burada (yanlış dokunma maliyeti) |
| `closing` | 250ms `translateY`; scrim 250ms opaklıkla (opaklık **yalnız scrim'de**, bileşen durumlarında kullanılmaz) |

### 5.3 Adım 3 durumları

| Durum | Ekran |
|---|---|
| `empty` | `SectionHeader` yerine tek **çukur satır** (`well`, radius 16, iç boşluk 16): "Eklediğin rutinler burada sıralanır." `EmptyGauge` **çizilmez** — beklenen bir veri yok, rutini olmamak geçerli bir durumdur |
| `filled` | Liste + bölüm başlığının sağında "Günlük {toplam} ₺" |
| `loading` | Kaydetme sheet'in birincil düğmesinde ("Kaydediliyor"); listede iskelet **yok** (yerel veri) |
| `error` | Üstte `InfoStrip warning`: "Rutinler kaydedilemedi." / "Yazdıkların duruyor, yeniden deneyebilirsin."; birincil "Yeniden dene" |
| Atlama | `ghost` "Rutin harcamam yok" **iki yerde** aynı işi yapar: adımın alt-sabit bloğunda ve kendiliğinden açılan sheet'in içinde → 4/4'e geçer, rutin verisi yazılmaz |

---

## 6. Adım 4/4 — plan özeti

```
[kabuk — sabit]
24
h1    "Planın hazır"
8
body  niyete göre tek cümle
24
hero panel (primary-soft · radius 32 · clay.raised-lg · iç boşluk 16)
      label "Günlük harcama limitin"
      8
      hero 56 tabular sayı + 8 + ₺ (display 32, taban çizgisine hizalı,
                                    SAYIYLA AYNI RENK — tokens §2.3)
24
Card (iç boşluk 16 · satırlar arası 8)
      Amacın                → Birikim yapmak      ← body-strong (metin değer)
      Aylık gelirin         → 32.000 ₺            ← amount (tutar)
      Sabit giderlerin      → 16.900 ₺
      Aylık hedef birikim   → 4.000 ₺
      Günlük rutinlerin     → 240 ₺
8
caption "Gelirinden sabit giderlerini ve hedefini çıkarıp 30 güne bölüyoruz."
4
caption "Rutinlerin bu limitin içinden harcanır."
24
InfoStrip info "Limitini Profil → Bütçe ve rutinler'den her zaman değiştirebilirsin."
24
alt-sabit: birincil "Trinkow'u kullanmaya başla"
```

### 6.0 Günlük limit formülü — **tek satır, tek kaynak** (Ö1)

> `gunluk_limit = (gelir − sabit_giderler − aylık_hedef) ÷ 30`
> → gösterimde **tam liraya aşağı** (tokens §14.2/6 ile aynı yuvarlama).

| Kural | Değer |
|---|---|
| Bölen neden 30 | Kurulum maaş günü **sormaz** → dönem `kalan_gun` tanımının "Düzensiz" hâlidir: **30 gün** (tokens §14.1). Maaş günü sonradan Profil'den girilirse limit o fonksiyonla yeniden hesaplanır |
| **Rutinler düşülmez** | Rutin harcaması günlük limitin **içinden** yapılır (kullanıcı onu gün içinde kaydedecek). Limitten bir kez düşüp bir kez de harcanınca saymak limiti **çift aşındırır**. Özet satırındaki "Günlük rutinlerin 240 ₺" bu yüzden **bilgi satırıdır**, bir çıkarma kalemi değil |
| Bu ekranda yazılı mı | **Evet** — kartın altındaki iki `caption` satırı hesabı ve rutinlerin yerini söyler (K-050: gizli katsayı yok, kara kutu yok) |
| Boş alan | `null` 0 sayılır (tokens §14.2 notu: cevaplanmayan alan `null`'dır; bu formülde çıkarma yapılmaz) |
| Negatif sonuç | `sabit_giderler + hedef > gelir` → limit kurulmaz; 4/4 "eksik" dilini kullanır (tokens §14.2/9). Bu akışta gelir zorunlu olduğu için ekran hiç limitsiz kalmaz |

**Prototipteki iki yüzeyin aritmetiği (ikisi de bu formül):**
`32.000 − 16.900 − 4.000 = 11.100 ÷ 30 = **370**` ·
`1.250.000 − 16.900 − 4.000 = 1.229.100 ÷ 30 = **40.970**`

| Kural | Değer |
|---|---|
| Ekranda 56pt sayı | **1** (denetim maddesi 19) |
| Uzun limit | 6+ karakter → `hero` 56 **`display` 32'ye iner**, `₺` 32 → `amount` 17 (tokens §7.5). Prototipte gösterildi (`40.970 ₺`) |
| **`₺` rengi** (Ö2) | Kahraman panelde `₺` **sayıyla aynı renktedir** (`text`) — tokens §2.3 "`hero` rolünde `₺` … sayıyla aynı renk". `text-2` (`c-2`) **tutar girişi** ekranlarının ipucu dilidir (boş kuyuda simgeyi geri çeker); özet panelinde simgeyi soluklaştırmak tek bir sayıyı iki parçaya böler. `display`e inen hâlde de aynı: rol küçülür, renk değişmez |
| Özet satırları | `SummaryRow`: etiket `body`/`text` solda, değer sağda. Değer **yalnız** kullanıcının yazdığı ya da backend'in döndürdüğü sayıdır; yüzde, tahmini getiri, "%X tasarruf edeceksin" **yok** |
| **Değerin rolü** (Ö3) | Sayı değer → `amount` 17 tabular (tokens §2.2: `amount` = liste tutarı **ve gün sayısı**). **Metin değer → `body-strong` 16** ("Amacın → Birikim yapmak"). `amount` rolünü metne açmak jeton değişikliğidir ve yapılmadı; iki satır tipi sağ kolonda 17 ↔ 16 farkıyla zaten hizalı durur (ikisi de Montserrat 600) |
| Satır taşması | Etiket **iki satıra sarabilir** (`satir-ust` hizası, üstten hizalı), değer `flexShrink: 0` — **değer asla kırpılmaz**. Uzun niyet etiketi için ayrıca §6.1 |
| `loading` | Limit henüz yoksa sayının yerinde **çukur blok** (`well` + `clay.sunken`, 132×32) + yanında `body`/`text-2` "Hesaplanıyor"; birincil düğme `disabled`. Shimmer ve tam ekran spinner yok |
| `error` | Kurulum yazılamadıysa üstte `InfoStrip warning` "Kurulum tamamlanamadı." / "Yeniden deneyebilirsin."; birincil "Yeniden dene" |
| Kutlama | Metin + tek büyük sayı. Konfeti/rozet/puan/seviye **yok** (K-048) |

### 6.1 Özet satırının kısa etiketi (Ö6)

`takip` niyetinin form etiketi **36 karakter** ("Aylık kenara ayırmak
istediğin tutar"). Form alanında sorun değil — etiket kuyunun **üstünde**
tam genişlikte durur. Özet satırında ise değerin yanında ~244pt yer var.
Çözüm kırpmak değil, **kısa karşılık**:

| `niyet` | Form etiketi (§4.1) | **Özet satırı etiketi** |
|---|---|---|
| `tasarruf` | Aylık hedef birikim | Aylık hedef birikim |
| `borc` | Aylık hedef borç kapatma | Aylık hedef borç kapatma |
| `takip` | Aylık kenara ayırmak istediğin tutar | **Aylık kenara ayırdığın** |

İki etiket de aynı alanı (`hedef_birikim_kurus`) gösterir; kısa karşılık
**yalnız özet satırında** kullanılır. Ayrıca `SummaryRow` etiketi iki satıra
sarma iznine sahiptir (yukarıdaki "Satır taşması" kuralı) — büyük yazı
boyutunda kısa karşılık da sarabilir, hiçbir hâlde kırpılmaz.
`takip` varyantı prototipte **çizildi** (4/4 uzun tutar yüzeyi).

---

## 7. E-16 Hesap oluştur

```
PushHeader   44 geri ok · h1 "Hesap oluştur" · 44 denge kutusu      (8/16)
             ↑ KAYDIRMA ALANININ İÇİNDE — gerekçesi §7.0
24
[ağ hatası varsa] InfoStrip warning + wifi-off + 24
TextField      "E-posta"          (etiket 13 + 8 + kuyu 56)
12
PasswordField  "Şifre"            (+ göz düğmesi 44) 
   8  PasswordRuleLine  "En az 8 karakter." → karşılandıysa check + "Uzunluk yeterli."
12
PasswordField  "Şifre tekrar"     (+ göz düğmesi 44)
   [hata] 8 + caption/danger-ink "İki şifre aynı değil. Yeniden yaz."
24
Checkbox  "Kullanım şartlarını okudum, kabul ediyorum."   ← BAĞLANTISIZ düz metin
8
Checkbox  "Gizlilik politikasını okudum, kabul ediyorum."
8
caption   "İki onayı da işaretleyince hesabını oluşturabilirsin."  (onay eksikse)
   ya da  caption/danger-ink "Devam etmek için iki onay da gerekiyor."
                                                      (onaysız sosyal dokunuştan sonra)
12
ghost     "Kullanım şartları"     44 · tam genişlik · sola hizalı · belgeyi açar
8
ghost     "Gizlilik politikası"   44 · tam genişlik · sola hizalı · belgeyi açar
12
OrDivider "ya da"                                   (iki yanı 12 — tokens §3.1)
12
SocialAuthButton Apple (yalnız iOS)  +8  Google
24
satır: caption "Hesabın var mı"   ·   ghost "Oturum aç"
24
alt-sabit: birincil "Hesap oluştur" (56)
```

### 7.0 `PushHeader` sabit mi, kayan mı? — **kayar** (B2 sorusu)

E-16'nın `PushHeader`'ı **kaydırma alanının içindedir** ve içerikle birlikte
kayar. Gerekçe: taşıdığı şey bir **başlık**tır, kurulumun adım göstergesi
gibi kaydırma boyunca okunması gereken bir **durum** değil; v4'ün bütün
push ekranları (E-17 … E-24) da başlığı kayan bölgede tutuyor ve tek ekran
için ayrılmak tutarlılığı bozardı. Geri yolu kaybolmuyor: iOS'ta kenardan
kaydırma geri götürür, Android'de donanım geri düğmesi çalışır, üstelik
form kısa kaydırılıyor (tek ekran + ~200pt). Kurulumun dört adımı **tam
tersi** kuralı uygular ve bu bilinçli bir ayrımdır: orada gösterge sabit,
burada başlık kayar.

| Delta | Ne oldu |
|---|---|
| `hesap.mahremiyet` + `.ek` bilgi şeridi | **Kaldırıldı** (Mustafa kararı). Ekranda depolama/yedekleme anlatan cümle kalmadı — tokens §2.3 "teknik açıklama yasak" ile de uyumlu |
| `kayit.yasal` pasif cümle (`LegalConsentText`) | **Kaldırıldı** → yerine **iki ayrı `Checkbox`** (Mustafa direktifi). `LegalConsentText` bileşeni de **kullanımdan düştü** (Ö4): onay etiketi artık bağlantı taşımayan düz `caption`'dır, belgeler ayrı `ghost` satırlarında açılır. İç içe `<Text onPress>` çözümü RN'de **inşa edilemezdi** — `hitSlop` bir `Pressable` prop'udur, `Text`'in içindeki `Text` onu tanımaz ve bağlantının dokunma hedefi 18pt'de (44 altı) kalırdı. Bileşen dosyası silinsin mi, başka ekranda kullanılacak mı → §12/6 |
| **Yasal belgeler nasıl açılır** (Ö4) | Onay grubunun **altında**, 12 boşlukla, **iki adet 44pt `button.ghost` satırı**: "Kullanım şartları" · "Gizlilik politikası" (aralarında 8). Tam genişlik + sola hizalı → dokunma hedefi **358 × 44**. Ölçü/renk/punto tokens §7.1 `button.ghost`tan (`text-2` / `body-strong`, `bg` üstünde 5.13 ✅), yalnız hizalama sola çekildi; `pressed` = `well` + `clay.pressed`. **İkon yok:** kilitli sette (`varliklar.md` §1) "belge" ikonu bulunmuyor ve `notebook-text` **Kayıtlar sekmesinin** ikonudur — iki anlam taşımaz; yeni ikon eklemek onay gerektirir. Satırın eylem olduğunu 44pt yükseklik + sola hizalı `body-strong` + `pressed` hâli söyler (aynı dil: "Oturum aç" ghost'u da ikonsuz). Mustafa'nın "checkbox ile onay" direktifi korundu — değişen **yalnız belgenin nasıl açıldığı** |
| "Şifre tekrar" | **Eklendi**, şifrenin hemen altında (12 boşluk) |
| Sosyal düğmelerin yeri | Onay kutularının **altında**: onaylar hem e-posta hem sosyal yolu kapılar |
| **Sosyal düğmeler pasif mi?** (B1) | **Hayır — etkin kalırlar.** Pasifleştirme fikri kalktı: `button.social`ın dolgusu/logosu/etiketi sağlayıcının marka kılavuzundan gelir (tokens §7.1 istisnası) ve tokens §7.1'de `button.social` için **`disabled` durumu tanımlı değil** — uydurmak yeni bir jeton açmak olurdu; iOS'ta Apple düğmesini biz çizmiyoruz (`expo-apple-authentication`), pasif hâlini zorlayamayız. Yerine: **onaylar işaretsizken sosyal düğmeye dokunulursa** akış durur, **iki `Checkbox` `error` hâline geçer** (2pt `danger` halka) ve grubun altındaki ipucu satırı yerini `hata.onay_gerekli` cümlesine bırakır (`danger-ink` + `accessibilityLiveRegion="polite"`). Eksik olan şey **işaretlenir**, düğme suçlanmaz. **Birincil düğme** onaylar işaretlenmeden **pasif kalmaya devam eder** — iki yolun kapısı aynı, geri bildirimi farklı: biri baştan kapalı, diğeri dokununca eksiği gösterir. Çizili karşılık: yüzey 17 |
| Kod sırası hatası | Bugün `kayit.tsx`'te birincil düğme bloğu sosyal düğmelerden **önce** basılıyor ve `OrDivider` en altta boşta duruyor. Yukarıdaki sıra bağlayıcıdır |
| "Hesapsız devam et" | Yok (K-080) |

### 7.1 `Checkbox` — **yeni bileşen** (`src/components/Checkbox.tsx`)

Projede onay kutusu yoktu. Yeni ölçü ailesi açılmadı: 32 kutu · radius 16 ·
44 satır · 12 aralık · 20pt glif — hepsi mevcut kümelerden.

| Özellik | Değer |
|---|---|
| Satır | `flexDirection: row`, `alignItems: center`, min yükseklik **44**, tam genişlik, `hitSlop` dikey 8 |
| Kutu | **32 × 32**, `radius.tile` **16**, `flexShrink: 0` |
| Kutu ↔ metin | **12** |
| Etiket | `caption` 13/18 · renk **`text`** (13pt için `text-2` yerine `text`: `bg` üstünde 8.96) · bağlantı bölümü `primary-text` (5.12), altı çizili değil — renk + `accessibilityRole="link"` |
| Glif | 20pt Lucide `check`, `#FFFFFF`, `strokeWidth 2` |
| Dokunma | **Satırın tamamı** (358 × 44, `hitSlop` dikey 8) kutuyu çevirir — satırda **tek** dokunma hedefi var. İç içe bağlantı **yok** (Ö4): olay sızması, `hitSlop` eksikliği ve "hangi yarıya dokundum" belirsizliği birlikte kalktı. Belgeler grubun altındaki iki `ghost` satırından açılır |

| Durum | Görünüm | Not |
|---|---|---|
| `unchecked` | `well` + `clay.sunken`, glif **yok** | Boş kuyu: "buraya bir şey girecek" |
| `checked` | Düz **`primary-deep`** + `clay.raised` + beyaz `check` | Gradyan **yok** (K-062); beyaz glif 5.37 |
| `pressed` (unchecked) | `groove` + `clay.pressed` | 150ms |
| `pressed` (checked) | `primary-press` + `clay.action-pressed` | |
| `focused` | `clay.sunken` + **2pt `primary-text`** halka (radius 20 = 16+4) | Kaldırılmaz |
| `error` | `clay.sunken` + **2pt `danger`** halka + grup altında `caption`/`danger-ink` (`hata.onay_gerekli`) | **İki tetikleyici:** (1) onaylar işaretsizken **sosyal düğmeye dokunmak** (B1 — akışın normal bir parçası, yüzey 17); (2) sunucunun onay sürümünü reddetmesi. Hata **iki kutuya birlikte** uygulanır: eksik olan tek bir kutu değil, onayın kendisidir. İlk dokunuşta kalkar |
| `disabled` | `disabled-bg` + `clay.sunken`, glif `text-2` (4.73) | **Opaklık kullanılmaz** |
| a11y | `accessibilityRole="checkbox"` + `accessibilityState={{ checked }}` + tam cümle `accessibilityLabel` | |

> **Bilinçli sapma — `design-reviewer` için:** tokens §5.4 "seçim dili"
> seçili durumu `primary-soft` + `clay.sunken` ile anlatır. 32pt'lik bir
> kutuda bu dil **çalışmaz**: `well #E6EFFE` ile `primary-soft #E4EEFE`
> arasındaki fark 1.0x'tir ve iki durum da çukur olduğu için derinlik de
> ayırt etmez → işaretli/işaretsiz görsel olarak aynı görünür. §5.4'ün
> "bilinen sınır" satırı bu durumda çözümün **halka değil, yüzeyi
> kabartmak** olduğunu söylüyor; burada onu uyguladık: işaretsiz = çukur
> kuyu, işaretli = kabarık dolu yüzey + **glif** (renk tek kanal değil).
> Halka yine yok. Dördüncü bir "seçili" dili açılmadı: bu, `filled`
> (dolgu dili) durumunun küçük kontrol karşılığıdır.

### 7.2 `PasswordField` deltası — şifre tekrarı

| Özellik | Değer |
|---|---|
| Ölçü | `TextField` ile aynı (56 · radius 16 · `well` + `clay.sunken`), sağ iç boşluk 16 → **8**, yuvada 44pt göz düğmesi |
| Etiket | "Şifre tekrar" · placeholder "Şifreyi yeniden yaz" |
| Göz düğmesi | Bağımsız çalışır (ilk alanı etkilemez); `accessibilityLabel` "Şifreyi göster" / "Şifreyi gizle" |
| Doğrulama anı | **`onBlur`** ve gönderimde; her tuş vuruşunda hata gösterilmez |
| `error` | 2pt `danger` + 8 + `caption`/`danger-ink` "İki şifre aynı değil. Yeniden yaz." |
| `match` | **Ayrı bir "eşleşti" satırı çizilmez** — hata yokluğu yeterlidir; ikinci bir yeşil satır ekranı gürültüye çevirir |
| Yapıştırma | Açık (şifre yöneticileri için) · `textContentType="newPassword"` · `autoComplete="new-password"` |

### 7.3 E-16 durum tablosu

| Durum | Ekran |
|---|---|
| `empty` | Üç alan placeholder'lı, iki onay işaretsiz, ipucu satırı görünür, **birincil düğme `disabled`**; sosyal düğmeler **etkin** (B1) |
| `valid` | İki onay işaretli + e-posta biçimi geçerli + şifre ≥ 8 + tekrar eşleşiyor → birincil etkin, ipucu satırı **kaybolur** (belge satırları kalır — belge her an okunabilir olmalı) |
| **onaysız sosyal dokunuş** | İki `Checkbox` `error` (2pt `danger`), ipucu satırı yerine `hata.onay_gerekli` (`danger-ink`), odak birinci onay kutusuna gider, `accessibilityLiveRegion="polite"` cümleyi okur. Sosyal düğmenin görünümü **değişmez**; sağlayıcı akışı açılmaz. İlk onay dokunuşunda hata kalkar |
| `error` (alan) | E-posta biçimi: "Geçerli bir e-posta yaz." · kayıtlı e-posta (409): "Bu e-posta ile hesap var. Oturum aç." · tekrar eşleşmiyor: yukarıdaki metin. Hepsi **alanın altında** |
| `error` (ağ) | Formun **üstünde** `InfoStrip warning` + `wifi-off`: "Hesap açmak için bağlantı gerekir." / "Yazdıkların duruyor." Alan değerleri korunur |
| `loading` | Birincil düğme: "Hesap oluşturuluyor" + spinner, genişlik sabit, `disabled`. Sosyal düğmelerin **görünümü değişmez** (sağlayıcı kilidi), dokunuşları bu sürede **yok sayılır** — çakışan iki kayıt isteği önlenir |
| Klavye açık | `KeyboardAvoidingView`; odaklı alan ve alt-sabit birincil düğme görünür kalır; `keyboardShouldPersistTaps="handled"` (onay kutusuna ilk dokunuş çalışır) |
| Uzun metin | Onay cümleleri 2 satıra sarar (satır yüksekliği 18 × 2 = 36), kutu dikeyde **ortalanır**; 200%+ yazı boyutunda satır büyür, kutu 32 kalır |

---

## 8. Metinler — tam TR karşılıkları (`metinler.md`'ye işlenecek)

Ton: motive edici, suçlayıcı değil, sorgu değil. **Ünlem yok, emoji yok**,
cümle ≤ 12 kelime, "maaş" yerine **gelir**, teknik/depolama açıklaması yok.

### 8.1 Kurulum — ortak

| Anahtar | Metin |
|---|---|
| `ob.sayac` | {adim}/4 |
| `a11y.kurulum_ilerlemesi` | Kurulum ilerlemesi |
| `a11y.onceki_adim` | Önceki adıma dön |
| `ob.devam` | Devam |

### 8.2 Adım 1/4 — niyet

| Anahtar | Metin |
|---|---|
| `ob.niyet.baslik` | Hadi başlayalım |
| `ob.niyet.aciklama` | Neyi hedefliyorsun? Günlük harcama limitini buna göre kuruyoruz. |
| `ob.niyet.tasarruf` | Birikim yapmak |
| `ob.niyet.tasarruf.alt` | Her ay kenara bir pay ayıracaksın. |
| `ob.niyet.takip` | Paramı kontrol altına almak |
| `ob.niyet.takip.alt` | Günün nereye gittiğini net göreceksin. |
| `ob.niyet.borc` | Borcumu bitirmek |
| `ob.niyet.borc.alt` | Kalan borcu adım adım eriteceksin. |
| `ob.niyet.ipucu` | Birini seçince devam edebilirsin. |

*(Eski `ob.niyet.baslik` = "Neden buradasın" ve "Sonra değiştirebilirsin."
düşer: birincisi sorgu tonu, ikincisi kullanıcıya bir vaat değil bir uyarıydı.)*

*(`ob.niyet.aciklama` r1'de güçlendi: "Trinkow ile neyi hedefliyorsun?" cümlesi
soruyu soruyordu ama **karşılığını** söylemiyordu. Yeni cümle seçimin sonucunu
adıyla veriyor — 4/4'teki "Günlük harcama limitin" etiketiyle birebir aynı
sözcükler. Başlık "Hadi başlayalım" olarak **korundu** (Mustafa direktifi);
ekranın ayırt ediciliğini bu alt satır taşıyor.)*

### 8.3 Adım 2/4 — gelir ve gider

| Anahtar | Metin |
|---|---|
| `ob.butce.baslik` | Gelir ve gider |
| `ob.butce.aciklama` | Gelirini ve giderlerini inceleyip sana en uygun planı kuruyoruz. Hedefine en kısa yoldan ulaşırsın. |
| `ob.butce.gelir_bolum` | Gelirin |
| `ob.butce.gider_bolum` | Sabit giderlerin |
| `ob.butce.gider_toplam` | {tutar} *(bölüm başlığının sağı, yalnız tutar)* |
| `ob.butce.hedef_bolum` | Hedefin |
| `alan.gelir` | Aylık net gelir |
| `alan.gelir.not` | Eline geçen tutar, kesintiden sonrası. |
| `alan.kira` | Kira ya da aidat |
| `alan.fatura` | Sabit faturalar |
| `alan.ulasim` | Zorunlu ulaşım |
| `alan.kredi` | Kredi ve taksitler |
| `alan.hedef.tasarruf` | Aylık hedef birikim |
| `alan.hedef.borc` | Aylık hedef borç kapatma |
| `alan.hedef.takip` | Aylık kenara ayırmak istediğin tutar |
| `alan.hedef.not` | Zorunlu değil. Sonra Profil'den değiştirebilirsin. |
| `alan.borc` | Kalan toplam borç |
| `alan.borc.not` | Borcun yoksa boş bırakabilirsin. |
| `hata.gelir_bos` | Planı kurmak için gelirini yazman gerekiyor. |
| `ob.butce.mesgul` | Plan kuruluyor |
| `hata.butce_yazma` | Plan kaydedilemedi. |
| `hata.butce_yazma.ek` | Yazdıkların duruyor, yeniden deneyebilirsin. |
| `genel.yeniden_dene` | Yeniden dene |

### 8.4 Adım 3/4 — rutinler

| Anahtar | Metin |
|---|---|
| `ob.rutin.baslik` | Günlük rutinlerin |
| `ob.rutin.aciklama` | Kahve, sigara, ulaşım gibi her gün tekrar edenler. Ekledikçe planın gerçeğe yaklaşır. |
| `ob.rutin.bolum` | Eklediklerin |
| `ob.rutin.gunluk_toplam` | Günlük {tutar} |
| `ob.rutin.bos` | Eklediğin rutinler burada sıralanır. |
| `ob.rutin.ekle` | Rutin ekle |
| `ob.rutin.yok` | Rutin harcamam yok |
| `ob.rutin.devam` | Plan özetine geç |
| `ob.rutin.satir_alt` | Her gün {adet} × {fiyat} |
| `ob.rutin.sheet_baslik` | Rutin ekle |
| `ob.rutin.sheet_baslik.duzenle` | Rutini düzenle |
| `ob.rutin.ad` | Ne? |
| `ob.rutin.ad_ph` | Sabah kahvesi |
| `ob.rutin.kategori` | Kategori |
| `ob.rutin.tum_kategoriler` | Tüm kategoriler |
| `ob.rutin.adet` | Günlük adet |
| `ob.rutin.fiyat` | Birim fiyat |
| `ob.rutin.sheet_eylem` | Rutini ekle |
| `ob.rutin.sheet_eylem.duzenle` | Değişikliği kaydet |
| `ob.rutin.kaldir` | Rutini kaldır |
| `ob.rutin.ayna` | Ayda {tutar} |
| `ob.rutin.ayna_formul` | Her gün {adet} × {fiyat} × 30 gün |
| `hata.rutin_fiyat_bos` | Rutini kaydetmek için birim fiyat gerekiyor. |
| `ob.rutin.sonra` | Rutinleri sonra Profil → Rutinlerim'den değiştirebilirsin. |
| `hata.rutin_yazma` | Rutinler kaydedilemedi. |
| `hata.rutin_yazma.ek` | Yazdıkların duruyor, yeniden deneyebilirsin. |

### 8.5 Adım 4/4 — plan özeti

| Anahtar | Metin |
|---|---|
| `ob.ozet.baslik` | Planın hazır |
| `ob.ozet.aciklama.tasarruf` | Bu limitin altında kaldığın her gün birikimin büyür. |
| `ob.ozet.aciklama.borc` | Bu limitin altında kaldığın her gün borcun küçülür. |
| `ob.ozet.aciklama.takip` | Bu limitin altında kaldığın her gün planın tutar. |
| `ob.ozet.limit_etiket` | Günlük harcama limitin |
| `ob.ozet.hesaplaniyor` | Hesaplanıyor |
| `ob.ozet.amac` | Amacın |
| `ob.ozet.gelir` | Aylık gelirin |
| `ob.ozet.gider` | Sabit giderlerin |
| `ob.ozet.rutin` | Günlük rutinlerin |
| `ob.ozet.hedef.takip` | Aylık kenara ayırdığın *(özet satırının kısa karşılığı — §6.1)* |
| `ob.ozet.nasil` | Gelirinden sabit giderlerini ve hedefini çıkarıp 30 güne bölüyoruz. |
| `ob.ozet.rutin_not` | Rutinlerin bu limitin içinden harcanır. |
| `ob.ozet.degistir` | Limitini Profil → Bütçe ve rutinler'den her zaman değiştirebilirsin. |
| `ob.ozet.eylem` | Trinkow'u kullanmaya başla |
| `hata.kurulum` | Kurulum tamamlanamadı. |
| `hata.kurulum.ek` | Yeniden deneyebilirsin. |

### 8.6 E-16 Hesap oluştur

| Anahtar | Metin |
|---|---|
| `kayit.baslik` | Hesap oluştur *(değişmedi)* |
| `alan.eposta` / `.eposta_ph` | E-posta · ornek@eposta.com *(değişmedi)* |
| `alan.sifre` / `.sifre_ph.kayit` | Şifre · Şifre belirle *(değişmedi)* |
| `alan.sifre_tekrar` | Şifre tekrar |
| `alan.sifre_tekrar_ph` | Şifreyi yeniden yaz |
| `kayit.sifre_kural` / `.sifre_kural_tamam` | En az 8 karakter. · Uzunluk yeterli. *(değişmedi)* |
| `hata.sifre_eslesmiyor` | İki şifre aynı değil. Yeniden yaz. |
| `kayit.onay.kosullar` | Kullanım şartlarını okudum, kabul ediyorum. *(tek parça — bağlantı yok)* |
| `kayit.onay.gizlilik` | Gizlilik politikasını okudum, kabul ediyorum. *(tek parça)* |
| `kayit.belge.kosullar` | Kullanım şartları *(44pt ghost satır etiketi)* |
| `kayit.belge.gizlilik` | Gizlilik politikası *(44pt ghost satır etiketi)* |
| `kayit.onay.ipucu` | İki onayı da işaretleyince hesabını oluşturabilirsin. |
| `a11y.onay.kosullar` | Kullanım şartlarını kabul et |
| `a11y.onay.gizlilik` | Gizlilik politikasını kabul et |
| `a11y.belge.kosullar` | Kullanım şartları belgesini aç |
| `a11y.belge.gizlilik` | Gizlilik politikası belgesini aç |
| `hata.onay_gerekli` | Devam etmek için iki onay da gerekiyor. |
| `kayit.eylem` / `.mesgul` | Hesap oluştur · Hesap oluşturuluyor *(değişmedi)* |
| `kayit.giris_kapisi.soru` / `.aksiyon` | Hesabın var mı · Oturum aç *(değişmedi)* |
| `hata.baglanti.kayit` | Hesap açmak için bağlantı gerekir. |
| `hata.baglanti.kayit.ek` | Yazdıkların duruyor. |
| **Düşen anahtarlar** | `hesap.mahremiyet` · `hesap.mahremiyet.ek` · `kayit.yasal` — E-16'da **kullanılmaz** (başka ekranda da kullanılmıyor; silme kararı PM'in). r1'de ayrıca `kayit.onay.*.bag` / `kayit.onay.*.son` **parçalı anahtarları düştü**: cümle artık bölünmüyor (Ö4) |

**Terminoloji notu (bilinçli):** brief'te "Parola tekrar" yazıyordu; ürünün
bütün metni "Şifre" diyor (`alan.sifre`, `kayit.sifre_kural`,
`hata.kimlik`). Aynı ekranda iki sözcük kullanmak kalite hatasıdır →
**"Şifre tekrar"**. Sözlük değişecekse tüm anahtarlar birlikte değişir.

---

## 9. Erişilebilirlik özeti

| Konu | Karar |
|---|---|
| Dokunma hedefi | Her etkileşimli eleman ≥ **44×44**: onay satırı 358×44 (+`hitSlop` 8) · **yasal belge satırı 358×44** (`button.ghost`) · göz düğmesi 44 · geri oku 44 · `MoneyRow` satırın tamamı 56 · kategori çipi 40 + `hitSlop` 4 → 48. **Metin içine gömülü bağlantı yok** (Ö4): `hitSlop` `Pressable` prop'udur, iç içe `<Text onPress>` onu almaz — 44 altı hedef üretmemek için bağlantı satıra terfi etti |
| `pressed` | Hover yok → her yüzeyin basılı hâli tanımlı (yukarıdaki tablolarda). `scale` yok, gölge çöker |
| Odak | 2pt `primary-text`, eleman radius + 4; hiçbir yerde `outline: none` |
| Ekran okuyucu | Adım göstergesi `progressbar` (min 1, max 4, now n) · seçim kartları `accessibilityState.selected` · onay kutuları `role="checkbox"` + `checked` · pasif düğmeler `accessibilityState.disabled` |
| Hata bildirimi | Alan hatası alanın altında **metinle** (renk tek kanal değil) + `accessibilityLiveRegion="polite"`; ağ hatası formun üstünde şerit |
| Sol üst köşe | Yalnız **geri** oku bulunur (iOS kenar kaydırmasıyla çakışan yıkıcı hedef yok) |
| Reduce motion | Adım geçişleri ve oluk dolumu 0ms |
| Renk körlüğü | İşaretli onay kutusu **glifle** ayrışır; seçili kart derinlik + ikon kabıyla ayrışır |
| Dinamik yazı | Kartlar ve satırlar büyür; hiçbir açıklama tek satıra kilitlenmez (`numberOfLines` yalnız ad/etiket kırpmasında) |

---

## 10. Bileşen envanteri deltası (`bilesen-envanteri.md`'ye işlenecek)

| Bileşen | Durum |
|---|---|
| `Checkbox` | **Yeni** (§7.1). Durumlar: `unchecked` / `checked` / `pressed` (iki hâl) / `focused` / `error` / `disabled` |
| `SetupShell` | **Yeni** (§2) — kurulumun kabuğu; `RevScreen` bu akışta kullanılmaz |
| `RoutineSheet` | **Yeni** (§5.2) — `BottomSheet` varyantı, **üç bölge** (tutamak · kayan form · sabit alt blok). Durumlar: `open` / `keyboard-open` / `filled` / `error` / `edit` / `closing`. Dördü prototipte çizili (yüzey 6-9) |
| `MoneyField` | `TextField`/`AmountWell`ın Rev sonrası hâli (§4.2): native `decimal-pad`, kil tuş takımı yok |
| `MoneyRow` | **Varyant** (§4.3) — `ValueWellRow`un düzenlenebilir ikizi. **`birim` parametresi** zorunlu (`"₺"` \| `""`); `fontScale > 1.3`'te dikey düzene döner |
| `RoutineRow` | **Varyant** (§5.1) — `SpendRow` ölçüleri + `pencil` |
| `StepIndicator` | Delta (§2.1): `toplam=4`, sayaç metni bileşenin dışında, dolum animasyonu, **dolu oluğun renkli gölgesi kaldırıldı**. Kabuğun **sabit** bölgesinde yaşar (§2 · B2) |
| `OptionCard` | Delta (§3.1): ölçüler netleşti; envanterdeki "2pt iç çizgi" cümlesi **düzeltilecek** (halka yok). Varsayılan seçim yok → üçü de `default` ile açılır (§3.0) |
| `CategoryPicker` | `RoutineSheet` içinde **yatay çip şeridi** (§5.2): tokens §7.6 çipi, 6 kategori + "Tüm kategoriler". Yeni bileşen değil, çipin dizilişi |
| `MirrorWell` | v4 E-25'teki ayna kuyusunun **aynısı** (§5.2): `well` + `clay.sunken`, 12/16 iç boşluk, `body-strong` + `amount` + 4 + `caption` formül |
| `LegalConsentText` | **Kullanımdan düştü** (Ö4): onay etiketi bağlantısız düz `caption`, belgeler `button.ghost` satırıyla açılıyor. Bileşen hiçbir ekranda çağrılmıyor → silinsin mi, kararı PM'in (§12/6) |
| `PasswordField` | İki örnek yan yana çalışır (§7.2) |
| `Fab` | Kurulumda ve E-16'da **hiç görünmez**; sekme çubuğu bu akışta yoktur (Faz: sekmeler Günlük / Tasarruf / Profil) |

---

## 11. Anti-pattern öz-denetimi (madde madde)

| Madde | Durum |
|---|---|
| Mor-mavi/indigo gradyan zemin ve düğme | ✅ Tek gradyan `grad.action` ve yalnız **metinsiz** adım oluğunda; birincil düğme düz `primary-deep` |
| Her elemanda glassmorphism | ✅ `blur` yok; derinlik clay gölgesiyle |
| Amaçsız drop-shadow | ✅ Üç gölge = üç anlam: kabarık nesne · çukur kuyu/seçili · parmak altında. Karta "yumuşatmak için" gölge eklenmedi |
| Karışık köşe yarıçapı | ✅ Yalnız 16 (kuyu/kutu/onay kutusu) · 24 (kart) · 32 (kahraman panel) · 999 (düğme/oluk) |
| Varsayılan AI fontu (Inter/Poppins/Montserrat) | ⚠️ **Bilinçli:** Poppins + Montserrat onaylı v4 marka kararıdır (tokens §2.1, `₺` glifi ölçülerek seçildi). Bu turda font **eklenmedi/değiştirilmedi**; 4 dosya sınırı korundu |
| "Daire ikon + başlık + 1 cümle" 3'lü sütun kartı | ✅ Yok. Seçenekler **tam genişlik dikey kart**, ikon kabı **kare** (48, radius 16) ve **solda** |
| Stok illüstrasyon / maskot | ✅ Yok; tek çizim primitifi kil yay ve o da bu iki ekranda kullanılmadı |
| Kimliksiz aşırı beyaz boşluk | ✅ Zemin `bg #E6EFFE`, boşluk ritmi 4/8/12/16/24 ile ilan edildi; "SaaS başlangıç şablonu" havası yok |
| Jenerik pazarlama dili | ✅ Metinler somut ve ikinci tekil: "Gelirini ve giderlerini inceleyip sana en uygun planı kuruyoruz." Ünlem, "Supercharge", "Empower" yok |
| Düşük kontrastlı açık gri metin | ✅ En düşük çift `text-3` placeholder (tek karakter `0`) ve `danger-ink`/`bg` 4.97; gövde metinleri 5.13 – 10.37 |
| Rastgele boşluk | ✅ Yalnız 4/8/12/16/24 + ilan edilmiş −8 oluk telafisi; `denetim.py` boşluk taraması **20 yüzey · 0 bulgu** |
| Dark mode'u ters çevirerek üretmek | ✅ Karanlık mod Faz 2; bu turda karanlık jeton üretilmedi |
| Gerçek içerik | ✅ Lorem yok: `ayse.kaya@example.com`, `Marlboro Touch Blue 20'lik`, 32.000 ₺ / 16.900 ₺ / 370 ₺ gibi tutarlı aritmetik |
| Emoji | ✅ Yok (mekanik tarama) |
| Boş / yükleniyor / hata / uzun metin | ✅ 20 yüzeyin **9'u** bunlar: 1/4 seçimsiz ilk hâl · boş sheet · sheet alan hatası · boş rutin listesi · gelir alan hatası · rutin yazma hatası · meşgul düğme · limit iskeleti · uzun tutar + uzun ürün adı + onaysız dokunuş hatası |
| RN kısıtları | ✅ `grid`, `::before/::after`, `:hover`, `sticky`, `calc`, `vh/vw`, `z-index` yok (mekanik tarama). Yalnız flexbox; SVG'ler `react-native-svg` karşılığı olan tek yollu ikonlar |
| WCAG AA | ✅ Tüm çiftler tokens §1.9'da hesaplanmış kümeden |

**Mekanik denetim (r1):** `python3 prototip-v4/_uret/denetim.py ../prototip-rev2/onboarding-kayit.html`
→ **20 yüzey · 0 bulgu** (+ `stil.css` 0 bulgu). `stil-rev2.css` aynı ölçütlerle
(tokens §1 palet · §12/9 radius · RN yasak dizeleri) tarandı → **0 bulgu**.

---

## 12. Açık kalan / PM onayı gereken maddeler

1. **Kaydırma kesmesi ölçümü.** tokens §12/11c "kaydırma alanının altında
   dilimlenen satır olmasın" diyor. Adım 2 formu ve E-16 kaydırır; kesme
   noktaları **aritmetikle** boşluk bandına düşecek şekilde dizildi (bölüm
   başlıkları kart dışında, onay grubu + 12 + "ya da"), ancak bu turda
   **headless tarayıcıyla ölçülmedi** (ortamda yok). Uygulamada
   `frontend-developer` doğrulamalı.
2. **`trinkow-rev.md` ile iki çelişki.** O belge "ekran kenarı 24, kart içi
   24" ve "sosyal seçenekler altta" diyor. Bu spesifikasyon **kenar 16 /
   kart içi 16** (tokens §3.1 istisnasız kural) uygular; sosyal düğmeleri
   Rev'e uyarak altta bırakır ama **onay kutularının altına** alır (onay
   her iki yolu da kapılar). `trinkow-rev.md` §Ortak temel düzeltilmeli.
3. **Varsayılan niyet kaldırıldı** (`'tasarruf'` → `null`): kullanıcı karar
   vermeden ilerleyemez. Onboarding tamamlama oranını etkiler, ürün kararı.
4. **Sosyal yol onaya bağlı ama düğme pasif değil** (r1 · B1). Apple/Google
   düğmeleri **etkin** durur; onaysız dokunuşta akış durur ve iki onay kutusu
   `error` hâline geçer. Hukuki sonuç aynı (onaysız hesap açılmıyor),
   sağlayıcı marka kılavuzu ihlal edilmiyor ve tokens §7.1'e olmayan bir
   `social.disabled` durumu eklenmiyor. **Ürün kararı:** kullanıcı hatayı
   dokunduktan sonra öğrenir; alternatifi (pasif düğme) sağlayıcı kilidi
   yüzünden inşa edilemezdi.
5. `hesap.mahremiyet`, `hesap.mahremiyet.ek`, `kayit.yasal` anahtarları artık
   hiçbir ekranda kullanılmıyor → `metinler.md`'den silinsin mi, arşiv
   satırı olarak mı kalsın?
6. **`LegalConsentText` bileşeni artık çağrılmıyor** (Ö4). Dosya silinsin mi,
   ileride "yasal metin" gerektiren bir ekran için dursun mu? Silme kararı
   PM'in (geri dönüşsüz işlem).
7. **Yasal belge ekranları.** İki `ghost` satırı belgeyi **nerede** açacak:
   uygulama içi bir push ekranı (`WebView`) mı, sistem tarayıcısı mı? Tasarım
   ikisine de uyar; karar ürün/hukuk tarafında. Uygulama içi seçilirse ekran
   `PushHeader` + kayan metin olur ve **yeni jeton gerekmez**.
8. **`fontScale > 1.3` eşiği** (Ö5) `MoneyRow`un dikey düzene döndüğü nokta
   olarak seçildi. Eşik ürün genelinde tek olmalı; `frontend-developer`
   bunu tek bir yardımcıya bağlamalı (iki ekranda iki eşik = K-040).

---

## 13. REV2-r1 — kapanan bulgular (`design-reviewer`, 24 Eylül 2026)

**Yüzey numaraları** (prototipteki sıra): 1-2 · 1/4 niyet — 3-5 · 2/4 gelir ve gider — 6-9 · 3/4 `RoutineSheet` — 10-12 · 3/4 liste/boş/hata — 13-15 · 4/4 plan özeti — 16-20 · E-16 hesap oluştur.

| Kod | Bulgu | Ne yapıldı | Nerede |
|---|---|---|---|
| **B1** | Sosyal düğme pasifliği inşa edilemez (`button.social.disabled` yok) | Pasifleştirme kaldırıldı. Düğmeler etkin; onaysız dokunuşta **iki `Checkbox` `error`** + `hata.onay_gerekli` satırı. Birincil düğme pasif kalmaya devam ediyor. Spesifikasyon ve **beş** E-16 yüzeyi aynı şeyi söylüyor | §7 delta tablosu · §7.1 `error` · §7.3 (+ yeni "onaysız sosyal dokunuş" satırı) · **yüzey 17** |
| **B2** | Adım göstergesi kaydırma alanının içinde → 2/4'te ekrandan çıkıyor | `ekran-basi` + `progressbar` satırı **`ScrollView`ın kardeşi** oldu; **15 kurulum yüzeyinin** tamamında `.content`ın ilk iki çocuğu. Üreteçte `dev(..., sabit_ust=...)`. E-16'nın `PushHeader`'ı **kayar** — gerekçesi yazıldı | §2 düzen şeması + yeni kural satırı · **§7.0** · `uret_onboarding_kayit.py: dev()` |
| **B3** | Adım 1/4'ün gerçek ilk hâli (seçimsiz) çizilmemiş; ipucunun yeri belirsiz | Yeni **§3.0**: üç hâlin tablosu + `ob.niyet.ipucu` konumu (**alt-sabit bloğun içinde, düğmenin üstünde 8**). Başlık korundu, **alt satır güçlendirildi** | §3 düzen şeması · §3.0 · §8.2 · **yüzey 1** |
| **B4** | `RoutineSheet` çizilmemiş; kendiliğinden açılan formun çıkışı yok | (a) Sheet **dört yüzeyle** çizildi (boş · klavye açık · dolu + ayna · düzenleme + hata); çip/kuyu/ayna ölçüleri, alan boşlukları, tutamak konumu ve **üç bölge** (tutamak · kayan form · sabit alt) yazıldı. (b) Otomatik açılma korundu, sheet'in içine `ghost` **"Rutin harcamam yok"** çıkışı kondu | §5 karar tablosu · **§5.2** (yeniden yazıldı) · §5.3 · **yüzey 6-9** |
| **B5** | `MoneyRow` "Günlük adet" alanında `₺` yazıyor | `birim` **parametresi** tanımlandı (`"₺"` \| `""`), kuyu genişliği **144 sabit**; §5.2 hangi varyantı çağırdığını söylüyor. Prototipte "Günlük adet" son eksiz, "Birim fiyat" `₺` ile | §4.3 · §5.2 · §10 · **yüzey 8-9** |
| **Ö1** | 4/4 uzun tutar aritmetiği yanlış (`41.667`), rutinlerin durumu belirsiz | **§6.0**: `gunluk_limit = (gelir − sabit_giderler − hedef) ÷ 30`, tam liraya aşağı; **rutinler düşülmez** (limitin içinden harcanır) ve bu ekranda **iki `caption` satırıyla yazılı**. İki yüzey de formülle: **370** ve **40.970** | §6 düzen şeması · §6.0 · **yüzey 13 ve 15** |
| **Ö2** | `hero` rolünde `₺` yanlış renkte (`c-2`) | `c-2` iki satırdan da kaldırıldı; `₺` sayıyla aynı renkte (`display`e inen hâlde de) | §6 kural tablosu · `adim4()` · **yüzey 13, 15** |
| **Ö3** | `amount` rolü metin değere uygulanmış ("Birikim yapmak") | O satır **`body-strong` 16**; `amount` yalnız sayı değerlerde. Jeton genişletilmedi | §6 kural tablosu · `ozet_satir(sayi=False)` |
| **Ö4** | Yasal bağlantının dokunma hedefi RN'de 44 altı kalıyor | Onay cümlesi **bağlantısız düz metin**; iki belge **44pt `button.ghost` satırı** olarak grubun altında. `LegalConsentText` kullanımdan düştü | §7 düzen şeması + delta tablosu · §7.1 "Dokunma" · §9 · §10 · **tüm E-16 yüzeyleri** |
| **Ö5** | `MoneyRow` uzun metin kuralı çelişik (§4.3 ↔ §4.4) | Tek davranış: **`fontScale > 1.3` → `MoneyRow` dikey düzene döner** (etiket üstte, sarar; kuyu 144 sabit). Aynı cümle iki bölümde birebir yazılı; etiket kırpma kaldırıldı | §4.3 · §4.4 |
| **Ö6** | `takip` niyetinde özet satırı kırpılıyor; `takip` varyantı çizilmemiş | **§6.1**: özet satırı için kısa karşılık ("Aylık kenara ayırdığın") + `SummaryRow` etiketine **iki satır** izni (değer asla kırpılmaz). `takip` varyantı çizildi | §6 kural tablosu · §6.1 · §8.5 · **yüzey 15** |
| **Gölge** | `.adim-dolu` renkli gölgesi (`rgba(47,104,197,0.45)`) tokens §5.2'ye aykırı | Gölge **kaldırıldı** (`clay.action`a çekilmedi: dolu oluk kabarık bir nesne değil, oluğun içindeki dolgudur ve zemini `surface`/`primary-deep` değil). `stil-rev2.css` §5 | §2.1 "Dolgu" satırı · `stil-rev2.css` §5 |

**Jeton disiplini (r1):** tek jeton değişikliği `tokens.md §5.4`'e eklenen
"**32pt ve altı kontroller**" satırıdır (PM şartı — `Checkbox`ın dolgu dili
artık jetonda yazılı). Yeni renk, punto, radius, boşluk, gölge, font ya da
ikon **üretilmedi**; `stil-rev2.css`'e eklenen üç blok (gölge iptali · ghost
hizalaması · sheet bölgeleri) yalnız geometri ve hizalamadır.

**Kapsam dışı bırakılanlar (bilinçli):** font kararı (Poppins + Montserrat,
v4) · `text-3` placeholder kontrast sapması (v4 borcu, ayrı tur) ·
Tasarruf/Profil/Günlük/Harcama ekle yüzeyleri · `app/**` kodu ·
`prototip-v4/stil.css` (`.adim-dolu` v4 prototipinde hâlâ gölgeli; **jeton
ölçütü ve rev2 prototipi** doğru dili söylüyor, v4 HTML'i geçmiş bir turun
çıktısı olduğu için dokunulmadı).
