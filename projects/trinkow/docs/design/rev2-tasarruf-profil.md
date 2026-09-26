# Trinkow rev2 — **E-27 Tasarruf · E-28 Profil** tasarım deltası

> **Durum:** **REV3-r0** — Mustafa'nın 2026-09-26 direktifi üzerine E-27
> **akordiyon yapısına** çevrildi; tanım **§3.12**, kapanan maddeler
> **§13**. REV2 turlarının dökümü §11 (r1) ve §12 (r2) · `ui-ux-designer`
>
> **REV3 özeti (bu belgede değişen):** kahramanın altındaki altı kart
> **dört akordiyon bölümüne** indi · **ilk bölüm açık** gelir, diğerleri
> kapalı ve her biri kapalıyken **özet değer** taşır · "Gerçek birikim" ile
> "Birikim hareketleri" **tek bölümde** birleşti · motivasyon şeridi
> ekranın ortasından çıkıp eylemiyle aynı bölüme indi · **rutin tasarrufu
> bölümü kaldı** (tutarı başka hiçbir yerde toplanmıyor), kalkan şey günlük
> hızlı eylemdi → `rev3-gunluk-rutin.md`. §1-§2 ve §4 (Profil) **rev2'de
> onaylandığı gibi durur**; REV3 kutuları değişen yerleri işaretliyor.
>
> **Kapsam:** yalnız iki ekran (`app/app/tasarruflar.tsx`, `app/app/profil.tsx`)
> + uygulama geneli **canlılık reçetesi** (§8). Onboarding / Kayıt / Giriş /
> Harcama ekle bu belgenin dışındadır.
>
> **Otorite (değişmedi):** görsel → `projects/trinkow/docs/brand/tokens.md` v4
> (claymorphism) · ton/metin → `projects/trinkow/docs/brand/brandbook.md` §2 ·
> bileşen → `projects/trinkow/docs/design/bilesen-envanteri.md` v4 ·
> RN kısıtları → `agency/reference/rn-tasarim-kisitlari.md`.
>
> **Bu belgede üretilmeyenler:** yeni renk, yeni punto, yeni radius, yeni
> boşluk değeri, yeni font, yeni ikon seti, yeni kütüphane, yeni veri alanı.
> Tek istisna §7'de tek tek sayıldı ve gerekçelendi.
>
> **Prototip:** `projects/trinkow/docs/design/prototip-rev2/tasarruf-profil.html`
> (tarayıcıda aç · **15 durum** · 390×844) ·
> üretici: `prototip-rev2/_uret/uret.py` · delta stil: `prototip-rev2/stil-rev2.css` ·
> mekanik denetim: `prototip-rev2/_uret/denetim.py` (son koşu: **0 bulgu**)
>
> **Veri sözleşmesi:** `projects/trinkow/docs/design/trinkow-rev-api.md` →
> `GET /tasarruf/ay`, `GET /tasarruf/birikimler`. Ekranda **o yanıtta olmayan
> hiçbir alan yoktur.**

---

## 0. Bugün sorun ne? (tek paragraf)

`tasarruflar.tsx` yedi kartı alt alta diziyor ve her kartın içi düz metin
dökümü: `Txt role="h2"` başlık, üç `Txt role="body"` satır, iki `Txt
role="caption"` paragraf. Ekranda **kahraman sayı yok** (en büyük tipografi
26pt `h1`, o da Poppins — rakam için tasarlanmamış rol), **renk yok**
(kategoriler düz metin), **derinlik tek katmanlı** (her şey aynı `clay.raised`
kart), **eylem hiyerarşisi yok** (birbiriyle yarışan iki `primary` düğme) ve
form sayfanın içine gömülü. `profil.tsx` ise üç kart içinde yedi `secondary`
düğme — bir liste değil, düğme yığını. İkisinin ortak teşhisi: **tokens v4'ün
araçları kullanılmıyor**; ekranlar teknik olarak doğru, görsel olarak boş.

---

## 1. Akış ve bilgi mimarisi

### 1.1 Alt navigasyon (rev kararı)

`Günlük · Tasarruf · Profil` — **FAB yok**. Üç sekme `space-around` ile eşit
dağılır (`.sekme-cubugu`, yükseklik 68, radius 999, `clay.raised-lg`).
Harcama ekleme girişi Günlük ekranındaki kategori satırının `+` düğmesidir
(E-10, v4'te tasarlandı). Bu ekranlarda **harcama ekleme çağrısı yoktur** —
yanlış yerde ikinci bir birincil eylem üretmemek için.

### 1.2 E-27 Tasarruf — okuma sırası ve gerekçesi · **REV3**

| # | Blok | Akordiyon | Cevapladığı soru | Neden burada |
|---|---|---|---|---|
| 1 | Kahraman gösterge | **dışında** (daima açık) | "Bu ay ne kadar biriktim?" | Ekranın tek kahramanı; ay gezinmesi de burada (E-10'daki gün sayfalamasıyla **aynı dil**) |
| 2 | **A · Bu ayın bütçesi** | **AÇIK** gelir | "Bu sayı nereden çıktı?" | Denklem: harcanabilir − harcanan = kalan. Kahraman sayının açıklaması; açıklanmamış bir sayı ekranda tek başına duramaz |
| 3 | **B · Gerçek birikim** (+ hareketler + motivasyon şeridi) | kapalı · özet "9.500 ₺ · hedefin %95'i" | "Fiilen ne kadar ayırdım, ne zaman ayırdım?" | Değer ve kanıtı tek bölüm; hesaplanan tasarruftan **ayrı başlık** |
| 4 | **C · Kategori dağılımı** | kapalı · özet "Harcanan 15.240 ₺" | "Para nereye gitti?" | Tanı değil teşhis; kahramandan sonra |
| 5 | **D · Rutin tasarrufu** | kapalı · özet "1.240 ₺ · 3 rutin" | "Vazgeçmem ne kazandırdı?" | Üçüncü ve **en dar** kavram; en sonda, en dar hâliyle |

**Ayrım korunuyor:** *hesaplanan tasarruf* (1, A) · *gerçek birikim* (B) ·
*rutin tasarrufu* (D) üç ayrı bölümde, üç ayrı başlıkla durur. Hiçbir yerde
toplanmazlar; D'nin ilk satırında bunu birebir söyleyen tek cümle vardır.
Akordiyon bu ayrımı **güçlendirir**: üç kavram artık üç ayrı katlanır
kutudur, alt alta akan altı kart değil.

**Ne değişti ve neden (REV3):** rev2'de kahramanın altında altı bağımsız
kart vardı; ekran 2.100px'i aşıyordu ve ilk katta kahramandan sonra yarım
bir kart görünüyordu. Mustafa'nın *"şık bir şeye çevir"* direktifi süs
eklemek olarak değil **bilgi yoğunluğunu düşürmek** olarak yorumlandı:
altı kart dört bölüme indi, üçü katlandı, ilk katta tek net mesaj kaldı.
"Gerçek birikim" ve "Birikim hareketleri" birleşti çünkü ikisi aynı
kavramın **değeri ve kanıtıdır** — ayrı iki başlık kullanıcıya iki kavram
olduklarını söylüyordu.

### 1.3 E-28 Profil — gruplama

| Grup | Satırlar | Neden bu grup |
|---|---|---|
| (grupsuz) | Kimlik kartı | Ekranın kim olduğunu söyleyen tek yüzey, en üstte |
| **Planın** | Maaş ve bütçe · Limitler · Rutinler | Kullanıcının **kurduğu** şeyler; en sık değişen grup |
| **Kayıt kolaylıkları** | Favoriler · Taksitler | Harcama girişini hızlandıran şeyler |
| **Takip** | Aylık özet · Seri | Geriye bakış yüzeyleri |
| **Uygulama** | Tüm ayarlar · Yardım | Ürünün kendisi |

Sıralama ölçütü: **dokunma sıklığı × kullanıcının o şeyi burada araması**.
"Tüm ayarlar" en sonda, çünkü başlıktaki ikon düğmesi zaten oraya gider —
satır bir yedek, tek yol değil.

---

## 2. Ölçü temeli (bu iki ekranda uygulanışı)

Yeni bir sistem kurulmadı; tokens v4'ün **hangi değerinin nerede** kullanıldığı
aşağıdadır. Denetim bu tabloya karşı yapılabilir.

### 2.1 Dikey ritim (tokens §3.1 — tek iş, tek değer)

| Değer | Bu iki ekranda tek işi |
|---|---|
| **4** | Aynı nesnenin iki satırı: tutar ↔ "çekildi" · kategori çubuğu ↔ "payı %27" · satır başlığı ↔ alt satırı · hedef çubuğu ↔ "Hedef 10.000 ₺" |
| **8** | Başlık ↔ gövde · etiket ↔ alan · bölüm başlığı ↔ ilk satır · **liste satırları arası** (hareket satırları, ayar satırları) · **REV3: aynı grubun kartları arası** (akordiyon bölümleri) |
| **12** | Kartın/formun İÇİNDE iki bağımsız blok: kip şeridi ↔ gösterge · gösterge ↔ cümle · **kategori satırları arası** · rutin satırları arası · form alanları arası |
| **16** | Yalnız **iç boşluk**: `kart-ic` · ekran kenarı (yatay) · sheet iç boşluğu. Satır/liste aralığı olarak **kullanılmaz** — tokens §3.1 bağlayıcı tablosunda liste aralığı 8, iki satırlı nesnelerin aralığı 12 |
| **24** | Ekran düzeyinde **ilgisiz** iki blok (E-27'de ay okları ↔ hata kartı · Günlük'te rutin bölümü ↔ alt liste) · kaydırma sonu |

**32 kullanılmaz** (bu iki ekranda gerekmedi), **20/28/40 üretilmedi.**

> **REV3 · "8" neden akordiyon bölümleri arasında?** Dört bölüm **tek bir
> kontrol grubudur** (aynı akordiyon), ekranın dört bağımsız bloğu değil.
> Aynı ek Günlük'teki rutin bölümü için de geçerli
> (`rev3-gunluk-rutin.md` §2.2).
>
> **REV3-r1 · kahraman kart ↔ akordiyon grubu da 8 (eskiden 24).** Gerekçe
> ölçümdür, tercih değil: 24 ile açık bölümün kabı **704**'te bitiyordu ve
> kaydırma alanı **693** olduğu için kesme kartın alt kenarından geçiyordu
> (bkz. §3.12.1 · B1). 8 ile kap 688'de biter, kesme iki kartın arasındaki
> boşluğa düşer. Kahramanı gruptan ayıran şey **hava değil derinlik ve
> biçim**: kahraman radius 32 + `clay.raised-lg` + `primary-soft`, bölümler
> radius 24 + `clay.raised` + `surface`. r0'da bu satırda duran "ekran
> düzeyindeki tek 24 kahraman ↔ ilk bölüm arasındadır" cümlesi geçersizdir;
> bu ekranda 24'ün tek işi **kaydırma sonu** (ve F5'te ay okları ↔ hata
> kartı) oldu.

### 2.2 Tipografi rolleri

| Rol | Nerede (E-27) | Nerede (E-28) |
|---|---|---|
| `hero` 56 | Kahraman sayı — **yalnız 3 haneye kadar** (bkz. §3.2 taşma) | — |
| `display` 32 | 4+ haneli kahraman sayı · sheet tutar alanı | — |
| `amount` 17 | Denklem kutuları · liste tutarları · kategori tutarı · rutin toplamı · **`Gerçek birikim` tutarı** | — |
| `h1` 26 | "Tasarruf" | "Profil" |
| `h2` 19 | Kart ve bölüm başlıkları · sheet başlığı | Grup başlıkları |
| `body` 16 | Kahraman cümlesi · hareket satırının birincil satırı | — |
| `body-strong` 16 | Kategori adı · düğme etiketi | Ayar satırı başlığı · kimlik satırı |
| `label` 13 | Gösterge altı etiket · sağ üst değerler · form etiketleri | — |
| `caption` 13 | Açıklama satırları · tarih/not · hata metni | Ayar satırı değeri · sağlayıcı satırı |
| `micro` 12 | Denklem kutusu etiketi · gün sayacının değeri ("22/30 gün") | Sürüm ve yasal bağlantılar |

**Tek kahraman kuralı:** E-27'de `display`/`hero` rolünde **tek bir sayı** vardır
— göstergenin ortasındaki tutar. İkinci bir 32pt sayı üretilmez; `Gerçek birikim`
kartının ağırlığı 12pt hedef çubuğundan gelir.

**Kural:** Poppins (`h1`/`h2`) **rakam taşımaz** — bugünkü koddaki
`<Txt role="h1">{money(...)}</Txt>` kullanımları kaldırıldı. Para daima
Montserrat + `tabular-nums`.

### 2.3 Radius ve derinlik

| Eleman | Radius | Gölge |
|---|---|---|
| Kahraman kart · **Profil kimlik paneli** · sheet · boş durum kartı | 32 | `clay.raised-lg` |
| Kart · **REV3: akordiyon bölüm kabı** | 24 | `clay.raised` (basılı: `groove` + `clay.pressed`) |
| **REV3: akordiyon içindeki liste satırı** | 16 | `clay.sunken` (`well`) — kap `raised` olduğu için satır bir basamak **iner**; satırın içindeki 44pt gün kutusu bir basamak **çıkar** (`.segment` ile aynı üç katmanlı dil) |
| Boş durum diski (176) | daire | `clay.raised` — içinde durduğu kart `raised-lg` olduğu için disk bir basamak **iner**; aynı yükseklik iki kez söylenmez |
| Liste satırı · ayar satırı · ikon kabı · şerit · giriş | 16 | satır `clay.raised` · şerit/giriş `clay.sunken` |
| Düğme · çip · segment · çubuk · gösterge diski | 999 / daire | `clay.action` / `clay.raised` / `clay.sunken` |

**Üç derinlik kuralı:** her ekranda üçü de görünür — `raised-lg` (kahraman),
`raised` (kart/satır), `sunken` (oluk/kuyu/şerit/ikon kabı). Bugünkü ekranların
"soluk" görünmesinin en somut sebebi tek derinlik kullanmalarıdır (§8/7).

### 2.4 Durumlar (her etkileşimli eleman için zorunlu)

| Durum | Görünüm | Not |
|---|---|---|
| `pressed` | Zemin `groove`, gölge `clay.pressed` · birincil düğme `primary-press` + `clay.action-pressed` | **Hover yok** — tek geri bildirim budur. `scale` animasyonu yok |
| `disabled` | Zemin `disabled-bg`, metin/ikon `text-2`, gölge `clay.sunken` · **opaklık kullanılmaz** | Pasif ay oku **gizlenmez** (düzen kaymasın) |
| `loading` | ≥150ms ise iskelet; düğme içinde "Kaydediliyor" + 20pt spinner, genişlik sabit | Tam ekran spinner yok |
| `error` | Alan: 2pt `danger` kenarlık + altında `caption`/`danger-ink` · ekran: `ErrorState` kartı | Hata kodu, teknik açıklama yok |
| `empty` | `EmptyGauge` (176 kabarık disk + 32pt ikon) + başlık + tek cümle + (varsa) ikincil düğme | "Henüz veri yok" hiçbir yerde yazılmaz |
| `focused` | 2pt `primary-text` halka, elemandan 2pt boşlukla, radius+4 | Kaldırılmaz |

---

## 3. E-27 — Tasarruf ekranı

Prototip çerçeveleri: **1** (dolu) · **2** (bütçe dışı) · **3** (ilk ay) ·
**4** (iskelet) · **5** (hata) · **6-7** (sheet).

### 3.1 Başlık — `.ekran-basi`

```
padding 8 / 16 / 16   ·   yükseklik ~60
├ sol (esnek, kolon)
│   caption  "Eylül 2026 · ay devam ediyor"     ← kapanmış ayda "· ay kapandı"
│   h1       "Tasarruf"                          numberOfLines=1
└ sağ: yok
```

Ay adı **başlıkta**, ay gezinmesi **göstergede** durur: başlık "neredeyim",
gösterge "ne oldu" sorusunu cevaplar. Günlük ekranında da aynı bölünme var
(caption = tarih, h1 = "Bugün").

### 3.2 Kahraman kart — `.hero-kart` (radius 32 · `primary-soft` · `clay.raised-lg` · iç boşluk 16)

```
┌ hero-kart ─────────────────────────────────────────────┐
│ [çip "Tasarruf" seçili +8pt nokta]   [çip "Bütçe 24.000 ₺" ›] │
│                        ↕ 12                              │
│  (‹ 44)        ● 224pt kil gösterge ●         (› 44 pasif) │
│                        ↕ 12                              │
│  body, ortalanmış: "Kaydettiğin gelir ve harcamalara      │
│                     göre 22 gün hesaplandı."             │
└────────────────────────────────────────────────────────┘
```

| Parça | Değer |
|---|---|
| Kip çipi | `.cip.secili` — brandbook §2.4 kip etiketi. Metin "Tasarruf", solunda 8pt `primary` nokta. **Rotası var:** `→ /ayarlar` (Plan ve profil — kipin değiştirildiği tek yer, `metinler.md` §26.3). `accessibilityLabel="Kip: Tasarruf. Değiştirmek için ayarları aç"`. Rotasız olsaydı `View` olarak çizilirdi; tıklanabilir görünüp iş yapmayan kontrol bırakılmaz |
| Bütçe çipi | `.cip` + `chevron-right`, `→ /butce`. Ad kırpılır, **tutar kırpılmaz** (tokens §7.6). Çip yüksekliği 40 → dokunma hedefi `hitSlop={{top:2,bottom:2}}` ile **44**'e tamamlanır (tokens §6; çipin görsel yüksekliği büyütülmez, aynı satırdaki kip çipiyle hizası bozulmasın) |
| Ay okları | `.ikon-btn` 44×44, `chevron-left/right`. Gelecek ay → `disabled` (gizlenmez) |
| Gösterge | tokens §7.5 birebir: 224 disk, oluk r 86 / kalınlık 16 / `well`, 270°, saat 7'den, dolgu `grad.arc`. Topuz **dolgu > 0 iken zorunlu**, dolgu 0'da çizilmez (yoksa boş oluğun başında anlamsız bir işaret kalır) |
| **Dolgu oranı** (tek formül) | `dolgu = max(0, hesaplanan_tasarruf) / harcanabilir` — "bu ayın bütçesinin ne kadarı bana kaldı". Dolgu bu ekranda **biriken** demektir |
| **Taşma oranı** | `tasma = min(1, abs(min(0, hesaplanan_tasarruf)) / harcanabilir)` |
| **Bütçe dışı ayda** | `hesaplanan_tasarruf < 0` ⇒ `dolgu = 0` ⇒ **ana yay ve topuz çizilmez**, oluk boş kalır. Bu formül §5'teki `LimitGauge mod="birikim"` satırıyla **birebir aynıdır** ve prototip bunu çiziyor (F2) |
| Ortadaki sayı | Biçim `6.240 ₺` (kuruş yok). **Taşma:** `"{sayı} ₺"` 6 karakteri aşarsa rol bir basamak iner: `hero` 56 → `display` 32, `₺` 32 → `amount` 17 (tokens §7.5). Ölçüldü (`Montserrat-Bold.ttf`, `prototip-v4/fonts`) — **`tabular-nums` genişliğiyle**, çünkü tokens §2.3 parada tabular'ı zorunlu kılar (her rakam 700/1000 em): yayın iç alanı **156px** · `820 ₺` = 139px ✅ · `1.250 ₺` = 189px ❌ · `6.240 ₺` = 189px ❌ · `12.500 ₺` = 226px ❌. Aynı hane sayısındaki iki tutar tabularda **eşit genişliktedir**; `1.250` ile `6.240`'ı farklı ölçmek §2.3'le çelişirdi (H3). Yani 4+ haneli tutar **daima `display` 32** olur (tokens §7.5'in ölçüm satırı bu sayılarla düzeltildi) |
| Etiket | `label`/`text-2` — "bu ay biriken" (sayının altında 4) |
| Cümle | `body`, ortalanmış, en fazla 2 satır |
| a11y | Gösterge: `accessibilityRole="progressbar"` + `accessibilityValue={{min:0,max:harcanabilir,now:biriken}}` + `accessibilityLabel="Bu ayın biriken payı"` |

**Gösterge durumları**

| Durum | Koşul | Görünüm | Metin |
|---|---|---|---|
| `default` | `biriken > 0` | Dolgu `grad.arc`, doluluktan bağımsız renk | "bu ay biriken" |
| `overflow` | `hesaplanan_tasarruf < 0` | **Ana yay çizilmez** (dolgu 0), oluk boş kalır, topuz yok; yalnız diskin 8pt dışında `grad.arc-over` taşma yayı (r 102). Sayı ve etiket `warning-ink` | "bütçe dışı" · cümle: seçili ay içinde bulunulan ay ise "Bu ay harcaman bütçenin 2.150 ₺ üzerinde.", geçmiş ay ise "Ağustos'ta harcaman bütçenin 2.150 ₺ üzerinde." |
| `empty` | `tamamlanan_gun_sayisi = 0` | 176pt kabarık disk (`clay.raised`) + çukur oluk, dolgu ve topuz yok, ortada `0 ₺` | "bu ay biriken" · cümle: "Ay yeni başladı. İlk tamamlanan günle hesap başlar." |
| `no-budget` | `harcanabilir = null` | Yay hiç çizilmez → `HeroPlain`: 176 kabarık disk + ortada 32pt `landmark` ikonu, altında `h2` + `body` + **birincil düğme** | "Gelirini ekle" / "Aylık gelirini yazınca bu ayın payını hesaplarız." / "Bütçeyi düzenle" |
| `skeleton` | okuma ≥150ms | Oluk + iki kenar yayı çizilir; dolgu ve topuz çizilmez. Ortada **140×38** sayı bloğu, **4** boşluk, **88×18** etiket bloğu — yüklü durumun birebir ölçüleri (etiket satırının gerçek yüksekliği 18, aralık 4; iskelet yükleme bitince zıplamaz) | "Hesaplanıyor" (`caption`) |

**Neden ana yay çizilmiyor?** tokens §7.5'in "ana yay %100 dolu kalır" satırı
dolgunun **harcanan** olduğu Günlük göstergesi için yazıldı: orada %100 "bütçeyi
bitirdin" demektir. Burada dolgu **biriken**'dir; %100 mavi yay + "bütçe dışı"
etiketi "her şeyi biriktirdin ama bütçe dışısın" gibi okunur — birbirini
çürüten iki işaret. Boş oluk ise doğruyu söyler: **bu ay biriken yok.** tokens
§7.5'e bu kapsam cümlesi eklendi (tokens §13.4).

**Ay adı kuralı (metinler §28.1).** Kahraman kartın cümlesi, kartların başlıkları
ve boş durum metinleri seçili aya göre iki varyanttır: seçili ay **içinde
bulunulan ay** ise "bu ay …", **geçmiş ay** ise ay adıyla "Ağustos'ta …".
Prototipte F1 birinci varyantı, F2 ikinci varyantı çiziyor.

**Kırmızı hiçbir durumda kullanılmaz.** Bütçe dışı `warning` ailesidir; ünlem,
üstü çizili rakam, titreme, ikon değişimi yoktur.

### 3.3 Motivasyon şeridi — `InfoStrip` (`serit-info`, `clay.sunken`, radius 16, iç boşluk 12/16)

> **REV3 — YER DEĞİŞTİRDİ.** Şerit artık kahramanın altında değil,
> **B bölümünün içinde**, "Birikim hareketi ekle" düğmesinin hemen
> üstünde. Gerekçe: kahramanın kendi cümlesiyle sırt sırta duran ikinci
> bir cümle ilk katta iki mesaj üretiyordu; oysa şeridin önerdiği eylem
> ("bu tutarı ayırmayı düşünebilirsin") tam o düğmedir. Geometri, metin
> ve ikon **değişmedi**; yalnız `.pad` sarmalayıcısı düştü (`serit_ic`).

20pt `target` ikonu + 12 + tek satır `caption` (metin rengi `text`).

| `motivasyon.tur` | Metin |
|---|---|
| `birikim` | "Bu tutarı birikim hedefin için ayırmayı düşünebilirsin." |
| `borc` | "Bu tutar borcunun %18'ine denk geliyor." |

Kart değil şerit: kahramanın altında ikinci bir başlık/kart açılırsa ekranın
odağı ikiye bölünür. **Kaldırılan:** "Hedefine bir adım" başlığı ve "Bu bilgi
borç ödemesi veya yatırım işlemi yapıldığı anlamına gelmez." satırı (teknik
sorumluluk reddi; cümlenin kendisi zaten iddia içermiyor — brandbook §2.8).

### 3.4 Bütçe kartı (radius 24, iç boşluk 16)

> **REV3 — bu blok artık akordiyon bölümü A'nın İÇERİĞİDİR** ve ekranda
> **açık** gelir (§3.12). Başlık ve sağdaki değer kabuğa taşındı:
> `h2` başlık akordiyon başlığı, kapalı özet **"Kalan 8.760 ₺"**.
> Sağ üstteki **"1–30 Eylül" satırı KALDIRILDI** — ekran başlığı ayı
> ("Eylül 2026") ve gün sayacı gün sayısını ("22/30 gün") zaten söylüyor;
> üçüncü bir tarih ifadesi bilgi eklemiyordu. Aşağıdaki iç düzen (denklem,
> sabit ödeme satırı, gün sayacı, kümülatif satır) **aynen geçerli**.
> `bilinmeyen_gun_sayisi > 0` şeridi artık kartın üstünde değil, **A'nın
> içeriğinin ilk satırında**: etkilediği sayıyla aynı kutuda durur.

Başlık iki varyanttır: seçili ay içinde bulunulan ay ise **"Bu ayın bütçesi"**,
geçmiş ay ise **"Ayın bütçesi"** (sağ üstteki `1–31 Ağustos` zaten hangi ay
olduğunu söylüyor; "bu ay" geçmiş aya bakarken yanlış olur).

```
h2 "Bu ayın bütçesi" / "Ayın bütçesi"        label/text-2 "1–30 Eylül"
                     ↕ 8
┌ 98 ─────┐  16  ┌ 98 ─────┐  16  ┌ 98 ──────┐
│micro     │  −   │micro     │  =   │micro      │   ← denklem kutuları
│Harcanabilir│      │Harcanan  │      │Kalan     │      (çukur `well` + clay.sunken)
│amount    │      │amount    │      │amount    │      sonuç kutusu KABARIK
│24.000 ₺  │      │15.240 ₺  │      │8.760 ₺   │      + `primary-soft`
└──────────┘      └──────────┘      └──────────┘
                     ↕ 12
caption "Sabit ödemeler dahil toplam 18.400 ₺"
                     ↕ 12
caption "Tamamlanan gün"                          12       micro "22/30 gün"
                     ↕ 12
caption "Takip başından beri biriken 21.180 ₺"
```

- Kutu genişliği: `390 − 32 (ekran) − 32 (kart) = 326`; `(326 − 2×16) / 3 = 98`,
  iç boşluk 8 → içerik 82px. En uzun tutar `24.000 ₺` = 17pt'de 80px, sığar.
  Daha uzun tutarlarda kutu **büyümez**, tutar `numberOfLines={1}` ile tek satır
  kalır ve kuruş zaten gösterilmez.
- `overflow` durumunda üçüncü kutu `.denklem-kutu.disinda`: zemin
  `warning-soft`, etiket **"Bütçe dışı"**, tutar `warning-ink` (5.86:1 ✅).
- **Gün sayacı çubuk değil, tek satır metindir.** Sol tarafta `caption`
  "Tamamlanan gün", sağda `micro` "22/30 gün". Gerekçe: 8pt `grad.action`
  çubuk (geçen **zaman**) ile 200px aşağıdaki 12pt `grad.action` hedef çubuğu
  (**birikim**) aynı renkte iki farklı şey anlatıyordu ve aralarında 4px'lik
  bir kalınlık farkı vardı. Mavi ilerleme dili bu ekranda **tek**: hedef
  çubuğu. `ProgressBar` bileşeni burada kullanılmaz; sayı zaten "22/30 gün"
  yazısıyla okunuyor, ikinci bir görsel kanal bilgi eklemiyordu.
- `bilinmeyen_gun_sayisi > 0` ise kartın **üstüne** `serit-warn` iner:
  "3 günün geliri eksik. O günler hesaba katılmadı."

### 3.5 Gerçek birikim — kart

> **REV3 — bu blok akordiyon bölümü B'nin üst yarısıdır** ve §3.6 ile
> **aynı bölümde** birleşti. `h2` "Gerçek birikim" kabuğun başlığı olur;
> tutar başlık satırından çıkıp içeriğin ilk satırına iner (solda ay
> satırı `caption`, sağda `amount` 17 tutar). Kapalı özet:
> **"9.500 ₺ · hedefin %95'i"**. B4 kuralı sürüyor: tutar `amount` 17'dir,
> `display` 32 değil. Bölümün içerik sırası: tutar → hedef çubuğu →
> motivasyon şeridi → tek `secondary` eylem → son 5 hareket → ghost.

```
h2 "Gerçek birikim"                                 amount 17 "9.500 ₺"
              ↕ 8
caption "Bu ay 4.600 ₺ eklendi"      ← geçmiş ayda "Ağustos'ta kayıt yok"
              ↕ 12
[oluk 12pt `groove`+sunken · dolgu `grad.action`]
              ↕ 4
caption "Hedef 10.000 ₺"                          label/text-2 "%95"
              ↕ 12
[button.secondary 52 · "+ Birikim hareketi ekle"]
```

**Tutar `display` 32 değil `amount` 17.** Ekranın tipografik kahramanı
göstergenin ortasındaki tutardır; burada ikinci bir 32pt sayı olması —hele
değeri kahramandan büyükken (9.500 > 6.240)— gözü yanlış yere çekiyordu.
Kartın ağırlığını **12pt hedef çubuğu** taşır: ekranın tek ilerleme çubuğu bu,
ve tek başına "hedefe ne kadar kaldı" sorusunu cevaplıyor. Düzen `Rutin
tasarrufu` kartıyla aynı desendedir (başlık satırının sağında toplam, altında
tek satır `caption`) — aynı iş, aynı görünüm.

| Alan | Kaynak | Boş/uç durum |
|---|---|---|
| Tutar | `gercek_birikim_kurus` | `0 ₺` yazılır, satır gizlenmez |
| Başlık altı satırı | `ay_birikim_kurus` | Seçili ay içinde bulunulan ay: `> 0` → "Bu ay {tutar} eklendi" · `< 0` → "Bu ay {tutar} çekildi" · `= 0` → "Bu ay kayıt yok". Geçmiş ay: "Ağustos'ta {tutar} eklendi" / "Ağustos'ta kayıt yok" |
| Çubuk | `gercek_birikim / hedef_birikim`, %100'de durur | `hedef_birikim = 0/null` → çubuk **çizilmez**, yerine `caption` "Hedef koymadın" + `button.ghost` "Hedef koy" (`→ /butce`) |
| Yüzde | `%95` — işaret önce, boşluksuz | — |

Dolgu `grad.action`'dır (metin taşımayan yüzey, 3.18:1 ✅).

**Yeşil neden yok — iki ayrı jeton, iki ayrı gerekçe.** `success` bir **grafik**
rengi olarak kullanılamaz: `groove` üstünde 2.85 ile 3:1 grafik eşiğinin altında
kalıyor, yani çubuk dolgusu olamaz. `success-ink` ise bir **metin** rengidir ve
AA'yı geçer (4.90 ✅) — teknik engel yok, ama bu kartta kullanılmadı: hedefe
yaklaşmak bir "başarı bildirimi" değil bir ölçümdür ve renkle övmek "yeşil = iyi
/ kırmızı = kötü" kodlamasının kapısını açardı (tokens §1.10, brandbook §2.6).
İki ekranda da tek renkli sinyal `warning` ailesidir ve o da **durum** anlatıyor,
yargı değil.

### 3.6 Birikim hareketleri — bölüm + `SpendRow` ailesi

> **REV3 — ayrı bölüm değil, B'nin alt yarısı.** Kendi `h2` başlığı yerine
> `label`/`text-2` bir alt satır taşır ("Son hareketler" · sağda "7 kayıt"):
> bir bölümde tek başlık olur. Satırlar `clay.raised` yerine **`kuyu`**
> (well + `clay.sunken`) olur, içlerindeki gün kutusu `raised`'a çıkar
> (§2.3). **Boş durum illüstrasyonsuzdur:** 176pt kabarık disk (tokens §7.8)
> bir bölüm kabının içine girince aynı yüksekliği iki kez söyler ve açılan
> bölümü ikinci bir kahramana çevirir; yerine tek satır `caption` yazılır
> ("Ağustos'ta kenara ayırdığın para yok."). Liste sınırı (5), kaydırarak
> silme, 6 sn geri al ve sheet davranışı **değişmedi**.

```
pad aralik:  h2 "Birikim hareketleri"        label/text-2 "7 kayıt"
             ↕ 8
satır-kart (min 68 · radius 16 · surface · clay.raised · iç boşluk 12/16)
┌──────────────────────────────────────────────────────────┐
│ ┌ 44 gün kutusu ┐ 12  body    "Birikime eklendi"          │
│ │ label   22    │      caption "Kenara ayırdım"  amount    │
│ │ micro   Eyl   │                              "1.500 ₺"  │
│ └───────────────┘                                          │
└──────────────────────────────────────────────────────────┘
             ↕ 8   (satırlar arası · en çok 5 satır)
             ↕ 12
[button.ghost "Tüm hareketler" → /birikimler]
```

| Konu | Karar |
|---|---|
| Yön (ekleme/çekme) | **Metinle** taşınır: birincil satır "Birikime eklendi" / "Birikimden çekildi"; çekimde tutarın altında `caption` "çekildi". Eksi işareti yazılmaz (brandbook §2.5) |
| Sol sütun | **İkon değil `.gun-kutu`** (E-15'te tanımlı desen: kategori/tür sabitken sol sütun **günü** taşır). 44×44 `well` + `clay.sunken`, üstte `label` gün sayısı, altında `micro` ay kısaltması. Gerekçe: `banknote` glifi bu ekranda dört işi taşıyordu (sekme ikonu · hareket satırı · boş durum diski · Profil "Maaş ve bütçe" satırı) ve dördü de "para" diyordu, hiçbiri ayırt etmiyordu. Gün kutusu hem tekrarı bitirir hem tarihi ikincil satırdan öne çıkarır. **Yeni glif üretilmedi** |
| Liste uzunluğu | **En çok 5 satır** (en yeniden eskiye). Altında `button.ghost` "Tüm hareketler" `→ /birikimler`; bölüm başlığının sağındaki "7 kayıt" toplamı söyler. Gerekçe: ayda 40 hareket ekranı ikiye katlar, kategori ve rutin kartlarını kaydırma dibine gömerdi. Kategori kartındaki "Tümünü gör" ile **aynı desen** |
| Not yoksa | İkincil satır **çizilmez** (boş satır bırakılmaz), satır 68pt minimumunda kalır ve birincil satır dikeyde ortalanır. Prototip F1'de 19 Eylül satırı bu hâlde |
| Renk | Yön renk taşımaz (WCAG 1.4.1). Çekim bir hata değildir — `warning`/`danger` kullanılmaz |
| Satıra dokunma | Aynı sheet **düzenleme kipinde** açılır (`PUT` upsert aynı `id` ile). Kipin başlığı, düğme etiketleri ve silme yolu §3.7'de tanımlı; prototip çerçeve 8 |
| Silme | İki yol: (1) sheet'in düzenleme kipindeki `button.ghost` **"Sil"** — keşfedilebilir yol; (2) satırı **sağdan sola kaydır → Sil** — kısayol. Onay yok, 6 sn "Geri al" toast'ı (K-029 deseni). Bugünkü satır altı "Hareketi sil" ghost düğmesi kaldırıldı. **Yön:** trailing (sağdan sola); soldan sağa kaydırma iOS'ta sistem "geri" hareketidir, silme oraya bağlanmaz (tokens §7.3 bu kararla düzeltildi) |
| Boş durum | `EmptyState` (radius 32 kart): 176 disk (`clay.raised`) + `banknote` → h2 "Birikim kaydı yok" → body "Kenara para ayırdığında buraya yazarsın." **Düğme yok:** aynı eylem 200px yukarıda, `Gerçek birikim` kartının içinde duruyor; tokens §7.8 boş duruma düğmeyi ancak "yalnız oradan yapılabilecek bir iş varsa" koyar |
| Uzun not | `caption` tek satır, sonu kırpılır (`numberOfLines={1}`, `ellipsizeMode="tail"`); tutar **asla kırpılmaz** |

### 3.7 Birikim hareketi sheet'i (form artık sayfada değil)

`BottomSheet`: üst köşeler 32, zemin `bg`, `clay.raised-lg`, scrim
`rgba(28,57,142,0.38)`, 250ms. Ekranı kaplamaz — arkadaki kahraman kart görünür
kalır (prototip çerçeve 6).

```
[44×4 tutamak]
        ↕ 12
h2 "Birikim hareketi" / "Hareketi düzenle"              [44 ikon-btn ✕]
        ↕ 12
segment (44 · well + sunken):  [Ekledim ●seçili] [Çektim]
        ↕ 12
label "Tutar"  ↕8  [giris 56 · well+sunken · display 32 "1.500" + amount "₺" + imleç]
        ↕ 12
label "Tarih"  ↕8  [kuyu-btn 56 · body "23 Eylül 2026" + calendar 20]
        ↕ 12
label "Not"    ↕8  [giris 56 · placeholder text-2 "İsteğe bağlı"]
        ↕ 12
[button.primary 56 "Kaydet"]        ← ekranın tek birincil eylemi
        ↕ 8
[button.ghost 44 "Sil"]             ← YALNIZ düzenleme kipinde
        ↕ 8
```

**İki kip, tek sheet**

| Kip | Nereden açılır | Başlık | Düğmeler |
|---|---|---|---|
| **Ekleme** | `Gerçek birikim` kartındaki `secondary` "Birikim hareketi ekle" | "Birikim hareketi" | `primary` "Kaydet" |
| **Düzenleme** | Hareket satırına dokunmak | "Hareketi düzenle" | `primary` "Kaydet" + altında `button.ghost` "Sil" |

Düzenleme kipinde alanlar var olan kaydın değerleriyle dolu açılır ve segment
kaydın yönünde durur. "Sil" `ghost`tur çünkü yıkıcı eylem birincil olamaz;
`btn-danger` da kullanılmaz — tokens §1.3 kırmızıyı yalnız **geri alınamaz**
onaylara ayırıyor, burada 6 sn "Geri al" toast'ı var (K-029).

**Kuyu zemininde `text-3` kullanılmaz.** Pasif tutar ("0") ve "İsteğe bağlı"
placeholder'ı `text-2`dir: `text-3` (#7C8698) `well` (#E6EFFE) üstünde **4.50**
ile AA'nın altında kalıyor ve tokens §1.2 bu çifti birebir yasaklıyor. `text-2`
(#5A6378) aynı zeminde **5.13** ✅. Sonuç: bu iki ekranda `text-3` **hiç
kullanılmıyor**.

| Konu | Karar |
|---|---|
| Yön seçimi | İki yarışan düğme (`primary` + `secondary`) yerine **tek segment**. Bugünkü kodun en belirgin hiyerarşi hatası buydu |
| Tutar | Native `TextInput`, `keyboardType="decimal-pad"` (rev kararı). Özel tuş takımı yok |
| Tarih | Metin girişi değil (`YYYY-AA-GG` biçim dayatması kaldırıldı) → `DateField` çukur satırı, varsayılan bugün, gelecek gün seçilemez |
| Klavye | Klavye açılınca sheet yükselir; **Kaydet görünür kalır** (prototip çerçeve 7) |
| `loading` | "Kaydediliyor" + spinner, genişlik sabit, `disabled` |
| Kapanış | Kaydedince sheet kapanır + toast "1.500 ₺ birikime eklendi · Geri al" (6 sn) |

**Sheet hata durumları**

| Koşul | Alan | Metin |
|---|---|---|
| Tutar boş / 0 | Tutar kuyusu 2pt `danger` kenarlık | "Tutar boş kalamaz." |
| Çekim bakiyeyi eksiye düşürüyor | Tutar kuyusu | "Birikimin bu kadar düşmez. Tutarı azalt." |
| İleri tarih | Tarih satırı | "Tarih ileri bir gün olamaz." |
| Ağ/kayıt hatası | Alan değil, Kaydet'in üstünde `serit-warn` | "Kaydedilemedi. Yeniden dene." |

Hata varken Kaydet `disabled` (zemin `disabled-bg`, metin `text-2`,
`clay.sunken`; **opaklık yok**). Girilen değerler korunur.

### 3.8 Kategori dağılımı — bölüm + tek kart

> **REV3 — akordiyon bölümü C.** Bölüm başlığının sağındaki
> "Harcanan 15.240 ₺" kapalı **özet** olur; bölüm açıkken aynı değer
> içeriğin ilk satırında (`caption` "Harcanan" + `amount` tutar) durur,
> yani açılınca kaybolmaz. Satırların iç düzeni **değişmedi**.

```
pad aralik:  h2 "Kategori dağılımı"          label/text-2 "Harcanan 15.240 ₺"
             ↕ 8
kart (iç boşluk 16) · satırlar arası 12
┌──────────────────────────────────────────────────────────┐
│ [44 `cat.*.soft` kab + 20pt `cat.*.solid` ikon] 12        │
│     body-strong "Market"              amount "4.180 ₺"   │
│                        ↕ 8                                │
│     [oluk 12 `groove`+sunken · dolgu `cat.*.solid`]       │
│                        ↕ 4                                │
│     caption "payı %27"            label/text-2 "rutin 480 ₺" │
└──────────────────────────────────────────────────────────┘
             ↕ 12
[button.ghost "Tümünü gör" → /ozet]
```

- Çubuklar **ortak ölçeği** paylaşır: en yüklü kategori %100 (`MonthLoadRow`
  ilkesi). Yüzde ise **toplam harcamaya** göre yazılır — iki farklı bilgi,
  ikisi de etiketli.
- En çok **5 satır**; kalanı "Tümünü gör".
- "rutin {tutar}" satırı yalnız `rutin_tasarruf_kurus > 0` olan kategoride —
  `0 ₺` yazan etiket **üretilmez** (aynı ekran "Bu ay vazgeçtiğin rutin yok."
  derken "rutin 0 ₺" etiketi taşımak kendi kendini çürütüyordu).
- Etiketler rutin kartının toplamıyla **toplanır**: Kafe 760 (Kahve 620 +
  Enerji içeceği 140) + Market 480 (Sigara) = **1.240 ₺** — rutin kartının
  başlık tutarı ve Profil'deki "3 rutin · bu ay 1.240 ₺ tasarruf" satırıyla
  aynı sayı.
- Renk asla tek başına bilgi taşımaz: **renk + ikon + ad** üçlüsü (WCAG 1.4.1).
- Kategori rengi **metin olarak kullanılmaz** (tokens §1.4).
- Bölüm boşluğu (illüstrasyonsuz): body "Bu ay henüz harcama yazmadın." +
  caption "İlk kaydından sonra kategori payları burada görünür."

### 3.9 Rutin tasarrufu — kart

> **REV3 — bölüm KALIYOR (D), hızlı eylem KALKIYOR.** Mustafa'nın "buna
> gerek yok" dediği şey Tasarruf içinde ayrı bir *rutinlerim sayfası*
> kurmaktı; **tutarın kendisi bir finansal bilgidir** ve ürünün başka
> hiçbir yüzeyinde toplanmıyor (kategori satırlarında parça parça
> "rutin 480 ₺", Profil'de tek satır). Kaldırılsa sayı kaybolurdu.
> Karar: en dar hâliyle akordiyonda yaşar — **kapalıyken tek satır özet**
> ("1.240 ₺ · 3 rutin"), açıkken tutar + tek cümle + rutin başına tek
> satır + ghost "Rutinleri aç". Maliyeti kapalıyken **76pt**.
>
> İç düzen iki noktada değişti: (1) `h2` ve toplam kabuğa/ilk satıra
> taşındı, (2) satırlardaki 44pt **`repeat` ikon kabı düştü** — üç satırın
> üçü de rutin olduğu için aynı glif hiçbir şeyi ayırmıyordu (Ö8'in
> gerekçesi). Günlük hızlı eylem artık `rev3-gunluk-rutin.md`'de.

```
h2 "Rutin tasarrufu"                                 amount "1.240 ₺"
              ↕ 8
caption "Vazgeçtiğin rutinler. Bütçedeki kalana eklenmez."
              ↕ 12
[44 kab `notr` · repeat] 12 body "Kahve"              amount "620 ₺"
              ↕ 12  (rutin satırları arası)
...
              ↕ 12
[button.ghost "Rutinleri aç" → /rutinler]
```

| Durum | Metin |
|---|---|
| Bu ay vazgeçme yok, rutin var | caption "Bu ay vazgeçtiğin rutin yok." (satır listesi çizilmez) |
| Hiç rutin yok | caption "Rutin eklemedin. Vazgeçtiğin harcamalar burada toplanır." |

### 3.10 Ekran düzeyi durum matrisi (E-27)

| Durum | Başlık | Kahraman | Kartlar | Sekme çubuğu |
|---|---|---|---|---|
| `default` | gerçek | dolu gösterge | **A açık** + B/C/D kapalı, dördü de özet değerli | görünür |
| `overflow` | "· ay kapandı" | **ana yay yok** (dolgu 0) + taşma yayı + `warning-ink` | A açık: denklem sonucu `disinda`, başlık "Ayın bütçesi", eksik gelir şeridi içerikte; B/C/D özetleri ay adıyla | görünür |
| `empty` (ay yeni başladı) | gerçek | 176 disk + `0 ₺` | A açık, denklem 0'larla dürüst; B/C/D özetleri "0 ₺ · …" / "Harcama yok" | görünür |
| `no-budget` | gerçek | `HeroPlain` + tek birincil düğme | A açık ama **denklem yok**: `serit-info` + tek satır olgu. Özet "Gelir eksik" | görünür |
| `loading` | gerçek (ay adı dahil) | oluk + çukur bloklar + "Hesaplanıyor" | **başlıklar gerçek**, özetlerin yeri iskelet; A'nın içeriği iskelet | görünür |
| `error` (tüm ekran) | "Tasarruf verisi" | **ay okları kendi satırında kalır** (başka aya geçilebilsin) | akordiyon **çizilmez** — hiçbir bölümün özet değeri yok, kapalı başlıklar boş kalırdı | görünür |
| `error` (**kısmi**, REV3) | gerçek | dolu gösterge | yalnız ilgili bölüm: özet **"Açılamadı"**, açık içerikte `serit-warn` + `secondary` "Yeniden dene". Diğer bölümler normal | görünür |

`error` metni: h2 "Bilgiler yüklenemedi" + body "Bağlantını kontrol edip
yeniden dene." + `secondary` "Yeniden dene". 96pt çukur daire + `wifi-off`
ikonu — **boş durumun 176pt diskinden kasıtlı olarak farklı** (kullanıcı ikisini
karıştırmamalı).


### 3.11 Metin deltası — ne gitti, ne geldi (E-27)

| Bugün koddaki metin | Yeni | Gerekçe |
|---|---|---|
| "Kalan tutar, ayın henüz harcanmamış bütçesidir. Sabit giderler için ayrılan pay harcanabilir gelirden düşülür." | **silindi** | Denklem satırı aynı şeyi gösteriyor; 16 kelimelik cümle §2.2/10'u aşıyordu |
| "Sabit ödemeler dahil tüm harcamalar: 18.400 ₺" | "Sabit ödemeler dahil toplam 18.400 ₺" | 4 kelime |
| "Tamamlanan 22 günün gelir payı ve kayıtlı harcamalarından hesaplandı. Bugün henüz bu hesaba dahil değil." | "Kaydettiğin gelir ve harcamalara göre 22 gün hesaplandı." | 8 kelime, tek cümle |
| "Tüm dönemler: 21.180 ₺" | "Takip başından beri biriken 21.180 ₺" | "dönem" sözlükte yok |
| "Gelir bilgisi eksik günlerde tasarrufunu sıfır olarak kabul etmiyoruz." | "3 günün geliri eksik. O günler hesaba katılmadı." | Önce sayı, sonra cümle |
| "Gelirini tamamlayalım" | "Gelirini ekle" | Buton/başlık fiil önce, 2 kelime |
| "Yalnızca vazgeçtiğini belirttiğin harcamalar. Bütçedeki kalana veya gerçek birikime tekrar eklenmez." | "Vazgeçtiğin rutinler. Bütçedeki kalana eklenmez." | 6 kelime |
| "Rutinlerim / Bugün almadım" | "Rutinleri aç" | Buton 1-3 kelime, fiil önce |
| "Hedefine bir adım" + "Bu bilgi borç ödemesi veya yatırım işlemi yapıldığı anlamına gelmez." | başlık ve sorumluluk reddi **silindi**; mesaj tek satır şeritte | §2.8 |
| "Buraya yalnızca gerçekten kenara ayırdığın veya birikiminden çektiğin parayı kaydet." | **silindi** | Sheet başlığı + segment aynı şeyi söylüyor |
| "Birikime ekledim" / "Birikimden çektim" (iki düğme) | segment: "Ekledim" / "Çektim" | Tek karar, tek kontrol |
| "Birikim hareketini kaydet" | "Kaydet" | 1 kelime |
| "Tutar · ₺" · "Tarih · YYYY-AA-GG" · "Not (isteğe bağlı)" | "Tutar" · "Tarih" · "Not" + placeholder "İsteğe bağlı" | Etiket biçim dayatmaz |
| "İşlem kaydedilemedi. Tarihi ve birikim bakiyeni kontrol edip yeniden dene." | Alana özgü üç metin (§3.7) | Hata nerede olduğunu söyler |
| "Hareketi sil" (her satırda ghost düğme) | Düzenleme sheet'inde `ghost` "Sil" + trailing kaydırma kısayolu + 6 sn "Geri al" | Liste temizlenir, silme keşfedilebilir kalır |
| "Bu ay henüz harcama kaydın yok." | "Bu ay henüz harcama yazmadın." | Sözlük: "kayıt" isim, "yazmak" fiil |
| "Ay devam ediyor. Takip başlangıcı: 2026-09-23" | "Eylül 2026 · ay devam ediyor" + "Takip 23 Eylül'de başladı. Ayın 8 günü hesaplanacak." | ISO tarih kullanıcıya gösterilmez |
| "Yükleniyor…" | iskelet + "Hesaplanıyor" | Ölü ekran yerine düzen |

**REV3 ek satırları**

| rev2'de | REV3 | Gerekçe |
|---|---|---|
| "1–30 Eylül" (bütçe kartının sağ üstü) | **silindi** | Ekran başlığı ayı, gün sayacı gün sayısını söylüyor; üçüncü tarih ifadesi bilgi eklemiyordu |
| "Birikim hareketleri" (`h2` bölüm başlığı) | **"Son hareketler"** (`label`/`text-2`, B bölümünün içinde) | Bir bölümde tek başlık olur; liste artık değerin kanıtı |
| — | **"Kalan 8.760 ₺"** · **"9.500 ₺ · hedefin %95'i"** · **"Harcanan 15.240 ₺"** · **"1.240 ₺ · 3 rutin"** | Kapalı bölüm özetleri; kapalı hâl asla boş başlık değil (§3.12.4) |
| — | **"Gelir eksik"** · **"Harcama yok"** · **"Rutin eklemedin"** · **"Açılamadı"** | Veri yok / kısmi hata özetleri; "Henüz veri yok" hiçbir yerde yazılmaz |
| — | **"Gelirini yazınca harcanabilir, harcanan ve kalan burada görünür."** | Gelir yokken A'nın içeriği; uydurma "0 − 0 = 0" denklemi kurulmaz |
| — | **"Birikim kayıtları açılamadı."** | Kısmi hata şeridi; teknik açıklama yok (§2.8) |
| "Vazgeçtiğin rutinler. Bütçedeki kalana eklenmez." (tek cümle) | **"Vazgeçtiğin rutinler"** (sol etiket, sağında tutar) + **"Bütçedeki kalana eklenmez."** | Aynı iki olgu; biri tutarın etiketi, öteki kuralın kendisi |
| "Rutinleri aç" | değişmedi (D bölümünün ghost düğmesi) | Yönetimin kapısı burada kalıyor |

### 3.12 REV3 — **AKORDİYON YAPISI** (E-27'nin bağlayıcı tanımı)

Bu bölüm, §3.3-§3.9'daki blokların ekranda **nasıl paketlendiğini** tanımlar.
Çelişki olursa bu bölüm esastır.

#### 3.12.1 Ekran iskeleti ve **ilk kat ölçümü** (REV3-r1 · tek kaynak)

> **B1 kapandı.** r0'daki ölçüm yanlış viewport üzerine kuruluydu
> (`844 − 44 − 34 = 766`): **yüzen sekme çubuğu kaydırma alanının
> dışındadır** (tokens §3.1; prototipin kabuğu da öyle kurar — `uret.py`'da
> `sekme_cubugu()` `.kaydir`'in kardeşidir, içinde değil). Aşağıdaki formül
> ve tablo bu belgedeki **tek** ilk kat kaynağıdır; §13'teki satırlar buna
> gönderme yapar.

**Kaydırma alanının yüksekliği** (390×844, prototip kabuğu):

```
844  ekran
− 47  durum çubuğu            (.statusbar · flex 0 0 47)
− 28  ana çubuk alanı         (.home-indicator · flex 0 0 28)
− 76  YÜZEN SEKME ÇUBUĞU      (.sekme-cubugu 68 + sarmalayıcı alt boşluk 8)
= 693 .kaydir'ın görünür yüksekliği   ← ölçüldü, varsayılmadı
```

Gerçek cihazda alt güvenli alan 28 değil **34**'tür (iPhone 14/15 sınıfı),
yani kesme **687**'ye çıkar. Bu belge **687-693 bandını** kullanır: bir
nesnenin "ilk katta" sayılması için **687**'nin üstünde bitmesi gerekir.

```
.ekran-basi          caption "Eylül 2026 · ay devam ediyor" · h1 "Tasarruf"      74
                     (ayırıcı yok: 16pt alt iç boşluğu başlığın kendisinde)
hero-kart            kip çipi · bütçe çipi · ‹ 224pt gösterge › · tek cümle     368
  ↕ 8                                             ← REV3-r1: eskiden 24 (§2.1)
akordiyon A          "Bu ayın bütçesi"        AÇIK                              238
────────────────────────────────────────────────── 687-693 arası KESME (8pt boşluk)
  ↕ 8
akordiyon B          "Gerçek birikim"         kapalı · özet                      76
  ↕ 8
akordiyon C          "Kategori dağılımı"      kapalı · özet                      76
  ↕ 8
akordiyon D          "Rutin tasarrufu"        kapalı · özet                      76
  ↕ 24               kaydırma sonu
[yüzen sekme çubuğu — kaydırma alanının DIŞINDA]
```

| Blok | Üst | Alt | Nasıl |
|---|---|---|---|
| `.ekran-basi` | 0 | **74** | 8 + (caption 18 + h1 32) + 16 — ayrı bir ayırıcı **yok** |
| kahraman kart | 74 | **442** | **368** — ölçüldü: 16 + 40 çip satırı + 12 + 224 gösterge + 12 + 48 (iki satırlık cümle) + 16. *(r0'da 364 yazılıydı; 4px'lik fark cümlenin satır yüksekliğindeydi, düzeltildi.)* |
| ayırıcı | 442 | 450 | **8** — aynı grubun kartları arası (§2.1 · REV3-r1) |
| **A (açık)** | 450 | **688** | 16 + 44 başlık + 12 + 150 içerik (denklem 60 + 12 + 18 + 12 + 18 + 12 + 18) + 16 |
| **kesme** | — | **687-693** | **A'nın altındaki 8pt boşluğun içine düşer** |
| B kapalı | 696 | 772 | ilk katın **dışında** |

**İlk kata giren nesneler:** ekran başlığı · kahraman kart (tamamı) ·
**A bölümünün tamamı** — başlığı, denklemi, üç açıklama satırı ve alt iç
boşluğu dahil. Kesme hiçbir kartın, satırın, sayının veya gölgeli kenarın
üstünden geçmez. A **688**'de bitiyor, kesme bandı **687-693**: yani
A'nın alt kenarı kesmenin **en çok 5px üstünde** (693'lük cihazda),
687'lik cihazda ise son **1px**'i kesmenin **altında** kalır — kesilen
şey A'nın 16pt alt iç boşluğunun son pikselidir, içerik değil. Altındaki
boşluk A ile B'yi ayıran 8pt'nin kendisidir. K-057/8 sağlanır.

**B ilk katta görünmez — r0'ın iddiası geçersizdi.** 693'lük alanda
B'nin başlığının okunması için B'nin kabının 633'ten önce başlaması
gerekirdi; başlık (74) + kahraman (368) + A (238) toplamı **ayırıcılar
sıfır olsa bile 680**'dir. Yani B'nin başlığı *hiçbir* boşluk düzeniyle
ilk kata sokulamaz. r0'ın "B'nin başlığı ve özeti tam okunur, kaydırma
daveti buradan gelir" cümlesi ölçüyle desteklenmiyordu ve **silindi**.

**Kaydırma daveti nereden geliyor (dürüst cevap):** ilk katta yarım kart
yoktur; davet, A'nın altında kalan ve sekme çubuğunun arkasına doğru
devam eden **boşluktan** ve ekranın dört bölümlü olduğunu söyleyen
kapalı bölüm özetlerinden gelir — bunlar tek bir kaydırma hareketinden
sonra (B·C·D toplam 76+8+76+8+76 = 244pt) hepsi birlikte görünür.
Bedeli açık yazılıyor: **B·C·D ilk bakışta keşfedilmez.** Kazancı,
kahraman sayının açıklamasının (A) ilk katta **bütün** okunmasıdır ve bu
takas bilinçlidir — ölçüm ikisini birlikte vermiyor.

> **Motivasyon şeridini B'ye taşımanın ölçülebilir sonucu** (R4) budur:
> şerit (44 + 24 = 68pt) kahraman ile A'nın arasında kalsaydı A'nın kabı
> 518'de başlar, 756'da biterdi ve kesme A'nın **içindeki** satırlardan
> geçerdi — 693'te "Tamamlanan gün · 22/30 gün" satırı ortadan ikiye
> bölünürdü (692-710). Şeridin eylemiyle aynı bölüme inmesi, A'nın ilk
> katta bütün okunmasının koşuludur.

**Diğer çerçevelerde kesme nereye düşüyor** (hepsi ölçüldü, 693):

| Çerçeve | Kesme | Sonuç |
|---|---|---|
| **F1** dolu ay | A (450-688) ↔ B (696) arasındaki 8pt boşluk | ✅ hiçbir nesne kesilmiyor |
| **F2** bütçe dışı ay | A'nın içindeki 12pt boşluk (684-696) | ✅ kart **açıkça devam ediyor**, satır/tutar bölünmüyor |
| **F3** ilk ay (gelir yok) | A'nın alt iç boşluğu — kabın son **6px**'i (cihazda 12px) altta kalıyor | ⚠️ **ölçülmüş istisna**, aşağıda |
| **F4** iskelet | A (450-684) ↔ B arasındaki boşluk; 693'te B'nin üst kenarının 1px'i | ✅ metin/sayı kesilmiyor |
| **F12** B açık | B'nin içindeki motivasyon şeridinin üst iç boşluğu | ✅ şerit devam ediyor, metni kesilmiyor |
| **F13 · F14** | çerçeve zaten **kaydırılmış** çizildi (başlık ve kahraman yukarıda) | ✅ |
| **F5** hata | içerik 427'de bitiyor, kesme yok | ✅ |

> **F3 istisnası neden kapatılmadı?** O çerçevenin kahraman kartı 421pt'dir
> (boş durum diski 176 + "Gelirini ekle" + cümle + `primary` düğme), yani
> dolu aydan **53px** uzun. 74 + 421 + 8 + 196 = 699: kalan açığı kapatmak
> için ya boşluk skalasının dışına çıkmak (4pt'lik kart aralığı — iki kart
> neredeyse birbirine değer) ya da açıklama cümlesini **foldu kurtarmak
> için** kısaltmak gerekirdi. İkisi de reddedildi. Kesilen şey kabın alt iç
> boşluğu ve yuvarlatmasıdır; hiçbir metin, tutar ya da satır bölünmez ve
> bölüm kaydırmayla tamamlanır. Bu, F1'de bloklanan kusurun küçük bir
> kalıntısıdır ve bilerek görünür bırakıldı — ölçüm dürüstlüğü, ölçümün
> gizlenmesinden değerlidir.

#### 3.12.2 Hangi bölüm açık gelir ve neden

**A · "Bu ayın bütçesi" açık gelir.** Kahraman sayı (`6.240 ₺` — bu ay
biriken) ekranın mesajıdır ama **açıklanmamış bir sayıdır**; kullanıcının
ilk sorusu "bu nereden çıktı?" olur. A tam bunu cevaplar: harcanabilir −
harcanan = kalan. Böylece ilk katta **tek kavram** (hesaplanan tasarruf)
baştan sona tamamlanır, diğer iki kavram (gerçek birikim, rutin tasarrufu)
katlanmış hâlde bekler — akordiyon ürün sözlüğündeki üç ayrımı görsel
olarak da kurar.

Değerlendirilip **reddedilen** alternatif: *B · Gerçek birikim*'i açmak.
Orada gerçek para var ve daha "önemli" görünür; ama B kahramanla aynı
soruyu cevaplamaz, kahramanın yanına **ikinci bir tutar** koyar (9.500 ₺ >
6.240 ₺) ve ilk katta iki para sayısı yarışır. B4 bulgusunun kapattığı
sorunun aynısı geri gelirdi.

#### 3.12.3 Bölüm kabı — `Accordion`

| Konu | Karar |
|---|---|
| Kap | `surface` + `clay.raised`, radius **24**, iç boşluk **16** |
| Başlık | `h2` (sol, esnek, `numberOfLines={1}`) · özet (`label`/`text-2`, sağ) · 20pt `chevron-down` |
| Dokunma hedefi | Başlık bloğu 358 × **min 44** (kapalıyken kap = başlık) |
| Basılı | **Kabın tamamı** çöker: `groove` + `clay.pressed`. `scale` yok, opaklık yok |
| Ok | Tek glif; açıkken **180° döner**. `chevron-up` kilitli sette yok, **üretilmedi**. RN: `transform:[{rotate:'180deg'}]` |
| Animasyon | Yükseklik **200ms ease-out** (`LayoutAnimation`/Reanimated `Layout`); içerik mount/unmount (RN'de `display:none` yok). Reduce motion → **0ms**, içerik anında yerini alır |
| Çoklu açık | **Serbest.** Bir bölümü açmak diğerini kapatmaz: kapanma, kullanıcının o an okuduğu içeriği altından çeker ve kaydırma konumu zıplar |
| Hafıza | Açık/kapalı durumu **ay değiştirince korunur** (aylar arası karşılaştırma için şart). Ekrandan çıkıp dönünce varsayılana (**yalnız A açık**) döner: ekranın sözü "tek net mesaj"dır, dört bölümü açık hatırlamak o sözü bozar |
| İç içe akordiyon | **Yok.** Bir bölümün içinde ikinci bir katlanır kutu açılmaz |

#### 3.12.4 Kapalı hâl asla boş başlık değildir — özet tablosu

| Bölüm | Dolu ay | Bütçe dışı ay (geçmiş) | Veri yok | Yükleniyor | Kısmi hata |
|---|---|---|---|---|---|
| A · Bu ayın bütçesi | "Kalan 8.760 ₺" | "Bütçe dışı 2.150 ₺" | "Gelir eksik" | özetin yeri iskelet | "Açılamadı" |
| B · Gerçek birikim | "9.500 ₺ · hedefin %95'i" | "9.500 ₺ · {AyLokatif} kayıt yok" | "0 ₺ · hedef 10.000 ₺" · hedef yoksa "0 ₺ · hedef koymadın" | " | " | " |
| C · Kategori dağılımı | "Harcanan 15.240 ₺" | "Harcanan 24.150 ₺" | "Harcama yok" | " | " | " |
| D · Rutin tasarrufu | "1.240 ₺ · 3 rutin" | "0 ₺ · 3 rutin" | "Rutin eklemedin" | " | " | " |

**Kural:** özet ya **tutar** ya **sayı** ya da tek kelimelik **olgu** taşır;
asla boş kalmaz, asla "…" ya da "Henüz veri yok" yazmaz. Tutar taşıyan
özetler `tabular-nums`'tır.

**Açıkken özet çizilmez.** Gerekçe: her bölümün içeriği kendi özet değerini
zaten ilk satırında taşıyor (A: denklem sonuç kutusu · B: tutar satırı ·
C: "Harcanan" satırı · D: "Vazgeçtiğin rutinler" satırı). İki santim arayla
aynı sayıyı iki kez yazmak bilgi değil gürültüdür. Bunun **tek istisnası**
Günlük ekranındaki rutin bölümünün geçmiş gün hâlidir ve gerekçesi
güvenliktir (`rev3-gunluk-rutin.md` §6).

#### 3.12.5 Akordiyon durumları

| Durum | Görünüm |
|---|---|
| `kapalı` | Kap 76pt; başlık + özet + aşağı ok |
| `açık` | Kap = 16 + 44 + 12 + içerik + 16; özet gizli, ok 180° |
| `basılı` | Kap `groove` + `clay.pressed` (hem açık hem kapalı hâlde) |
| `açılış/kapanış` | 200ms yükseklik; ok eş zamanlı döner; reduce-motion 0ms |
| `yükleniyor` | Başlık **gerçek metin**, özetin yeri 104×18 çukur blok; açık bölümün içeriği iskelet |
| `hata (kısmi)` | Özet "Açılamadı"; bölüm açık gelir, içinde `serit-warn` + `secondary` "Yeniden dene" |
| `veri yok` | Bölüm **gizlenmez**; özet olguyu söyler, açık içerik illüstrasyonsuz bölüm boşluğudur (body + caption) |
| `disabled` | **Yok** — hiçbir bölüm kilitli değil |

**Hata hâli kapatılırsa ne olur — Ö4.** "Açıkken özet çizilmez" kuralının
istisnası **değildir**; kural olduğu gibi işler ve hatayı taşımaya yeter:

| Kullanıcı ne yaptı | Başlığın sağı | Bölümün içi |
|---|---|---|
| Hiçbir şey (varsayılan) | **boş** — bölüm açık geldi | `serit-warn` "…açılamadı." + `secondary` "Yeniden dene" |
| Hatalı bölümü **kapattı** | **"Açılamadı"** — özet bir tutar değil, bir olgu söyler | (katlandı) |
| Kapalı hatalı bölümü tekrar açtı | boş | Şerit ve "Yeniden dene" **geri gelir**; yeni bir istek atılmaz (kullanıcı basmadan denenmez) |

Yani hata **kaybolmaz**: açıkken şerit taşır, kapalıyken özet taşır, ikisi
birlikte asla görünmez. Erişilebilirlik etiketi her iki hâlde de değeri
söyler ("Gerçek birikim. Açılamadı"), çünkü etiket özetin çizilip
çizilmesinden bağımsızdır. Bu belgedeki **tek** özet istisnası geçmiş gün
kapsamıdır (E-10, `rev3-gunluk-rutin.md` §3); hata hâli istisna değil,
kuralın normal çıktısıdır.

#### 3.12.6 Tek kahraman kuralı akordiyonla bozuldu mu?

Hayır. `hero`/`display` rolündeki **tek sayı** hâlâ göstergenin ortasındaki
tutardır; akordiyonun içindeki en büyük tipografi `amount` 17'dir. Akordiyon
başlıkları `h2` 19'dur (Poppins, **rakam taşımaz** — §2.2 kuralı) ve özetler
`label` 13'tür. Bölüm açmak ekrana ikinci bir kahraman sokmaz.

#### 3.12.7 Erişilebilirlik

| Konu | Karar |
|---|---|
| Rol | Başlık `accessibilityRole="button"` + `accessibilityState={{expanded}}` |
| Etiket | "{başlık}. {özet}" — özet açıkken de **etikette kalır** (görsel olarak gizlenmiş olması ekran okuyucudan saklanması anlamına gelmez) |
| Odak | Bölüm açılınca odak başlıkta kalır; içerik açıldığı için otomatik odak taşınmaz (kullanıcı kendi ilerler) |
| İçerik | Kapalı bölümün içeriği **mount edilmediği** için ekran okuyucu onu hiç görmez — `expanded:false` ile tutarlı |
| Dokunma | Başlık 358×≥44; içerik kontrolleri kendi hedeflerini korur |
---

## 4. E-28 — Profil ekranı

Prototip çerçeveleri: **8** (oturum açık) · **9** (hesapsız) · **10** (hesap
hatası) · **11** (iskelet).

### 4.1 Başlık

```
caption "Hesabın ve planın"        ┐ sol, esnek
h1      "Profil"                   ┘
                                   [44 ikon-btn `ayarlar`]  aria: "Ayarları aç"
```

### 4.2 Kimlik paneli — **kahraman panel** (radius 32 · `primary-soft` · `clay.raised-lg` · iç boşluk 16)

Kart değil **panel**. Profil'in kahraman sayısı yoktur (§8/1: gezinme ekranı),
bu yüzden ekranın ilk nesnesi tek başına "bu ekran neyin ekranı" demek
zorundadır. Beyaz `surface` kart olarak çizildiğinde altındaki dokuz ayar
satırından ayırt edilemiyordu ve ekran uçtan uca beyaz kart listesine
dönüşüyordu. Panel E-27'nin kahraman kartıyla **aynı yüzey dilidir** —
`primary-soft` zemin, radius 32, `clay.raised-lg`; yeni token üretilmedi.

```
┌ hero-kart (primary-soft · r32 · raised-lg · pad 16) ────────┐
│ [48 çukur kutu `secim-ikon` + 24pt `user`] 12               │
│    body-strong "mustafa.teker.1988@uzunsirketalanadi.com.tr"│ ← tek satır, kırpılır
│    caption     "Google ile oturum açıldı"                   │
│                                        [20pt chevron-right] │
│                            ↕ 12                             │
│ ┌ olgu şeridi (well · r16 · clay.sunken · pad 12/16) ─────┐ │
│ │ [20 `trending-up` primary-text] 12                      │ │
│ │    label   "12 gündür kayıt giriyorsun"                 │ │
│ │    caption "En uzun 21 gün."                            │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                         panel: 358 × 156
```

**Üç derinlik burada tamamlanıyor:** panel `raised-lg` · içindeki 48pt ikon kabı
ve olgu şeridi `sunken` · altındaki ayar satırları `raised`. Ölçülen aksan
oranı §8/2'de.

#### 4.2.1 Olgu şeridi — Ö7 takviyesi (REV2-r2)

r1 denetimi paneli geçirdi ama aksan oranını düşük ölçtü: ilk katta görünen
şey "80pt mavi şerit + 5 beyaz satır"tı, panel kahraman gibi okunmuyordu. PM
kararıyla panel **tek bir `clay.sunken` olgu şeridiyle** takviye edildi.
Panel 80 → **156pt**, ilk kattaki aksan yüzey **%14,2 → %23,5** (doğru ilk
kat penceresine — 693 — karşı yeniden ölçüldü, B1; r0 bu iki sayıyı 766'lık
yanlış pencereyle %13,1 → %21,9 diye yazmıştı). Hesap §8/2'de.

| Kısıt | Nasıl tutuldu |
|---|---|
| Kahraman sayı üretilmedi | Roller `label` (olgu) + `caption` (bağlam). Ekranın hâlâ `hero`/`display` sayısı yok; Tasarruf'un tek kahramanı bozulmadı (§8/1) |
| Yeni veri alanı / API yok | Şeridin içeriği **Seri** ayar satırının değerinin aynısı (`profil.satir.seriDeger` — "12 gün · en uzun 21 gün"). Aynı kaynak, iki sunum |
| Yeni token / renk / ikon yok | `.serit` geometrisi (§3.3 `InfoStrip`: pad 12/16, r16, `clay.sunken`) + v4'ün `.clay-kuyu` zemini (`well`). İkon `trending-up` — Seri satırının glifi |
| Zemin neden `well`, neden `groove` değil | `groove` bu sistemde **basılı** yüzeyin zeminidir (tokens §5.4, `.ayar-satir.basili`); statik bir şeride verilirse "basılı" yalanını söyler. `serit-info`'nun `primary-soft` zemini de olmaz — panelin zeminiyle aynı olur, şerit kaybolur |
| Kontrast | `text`/`well` **8.96** · `text-2`/`well` **5.13** (B2'de onaylı) · `primary-text`/`well` **5.12** — üçü de AA |

**Metin varyantları** (`metinler.md` §28.2, "Kimlik panelinin olgu şeridi"):
şerit **asla boş çizilmez**, üç varyanttan biri daima doludur —
seri 0 → "Seri henüz başlamadı · İlk kaydınla ilk gün sayılır." ·
en uzun = mevcut → "{n} gündür kayıt giriyorsun · En uzun serin bu." ·
en uzun > mevcut → "{n} gündür kayıt giriyorsun · En uzun {n} gün."
Övgü, ünlem ve emoji yok; cümleler nötr tespit (§8/13).

**Şerit hangi durumda çizilir?**

| Profil durumu | Olgu şeridi | Panel yüksekliği | Neden |
|---|---|---|---|
| `signed-in` | **Var** (üç metin varyantından biri) | **156** | Panelin tek satırlık olduğu durum buydu; takviye tam buraya gerekiyordu |
| `signed-out` | **Yok** | 144 | Panelin işi uygulamanın **tek** hesap davetidir (K-052). Davetin altına ikinci bir mesaj koymak daveti ikiye böler. Şeridin yerini `button.secondary` "Oturum aç" alır |
| `error` | **Yok** | 144 | Panelin işi hata + "Yeniden dene". Şeridin yerini o blok alır. (Seri verisi yerel olduğu için teknik olarak gösterilebilirdi — gösterilmiyor, çünkü hata anında ekranın tek mesajı hata olmalı) |
| `skeleton` | **Yeri var, metni yok** | **156** | Şeridin yerinde tek parça çukur blok (326×64, r16). Şerit zaten çukur olduğu için **içine ikinci kat çukur çubuk konmadı**. Yükleme bitince düzen zıplamaz |
| `signed-in` + veri yok (seri 0) | **Var** | 156 | §4.3'ün "ikincil satır asla boş kalmaz" kuralı şeride de uygulanır: değer yoksa **tanım** yazılır ("İlk kaydınla ilk gün sayılır."). "…" ya da boş çukur gösterilmez |

Üç yüksekliğin 144 ↔ 156 aralığında kalması kasıtlıdır: durum değişince
(oturum açılınca, hata geçince) altındaki dokuz satır 12px'ten fazla kaymaz.

**Basma hedefi tek kaldı.** Şerit **dokunulamaz** (`clay.sunken` bu sistemde
dokunulmaz yüzeyin dili: oluk, kuyu, ikon kabı) ve kendi chevron'u yoktur;
panelin tek chevron'u kimlik satırındadır. Panelin tamamı hâlâ tek basma
hedefidir → Ayarlar ▸ Hesap. Ekran okuyucuda etiket birleşir, bu yüzden
`a11y.profil.kimlikSerit` şeridi de okuyor (bkz. §7/11).

| Durum | İçerik | Eylem |
|---|---|---|
| `signed-in` | E-posta + sağlayıcı satırı ("Google ile oturum açıldı" / "Apple ile oturum açıldı") **+ olgu şeridi** (§4.2.1) | Panelin tamamı basılabilir → Ayarlar ▸ Hesap. `pressed` = `groove` + `clay.pressed` |
| `signed-out` | body-strong "Hesapsız kullanıyorsun" + caption "Harcamaların telefonunda kalır." + `button.secondary` "Oturum aç" | Kart basılabilir **değil**; eylem düğmede. Uygulamadaki **tek hesap daveti** budur (K-052: hesap hiçbir özelliği kilitlemez) |
| `error` | 20pt `wifi-off` + body-strong "Hesap bilgisi açılamadı" + caption "Ayarların ve yasal metinler açık kalır." + `button.secondary` "Yeniden dene" | **Alttaki tüm ayar satırları etkin kalır** — veri gerektirmiyorlar |
| `skeleton` | Panel yüklenmiş hâliyle **aynı yüzeydir** (yükleme bitince düzen zıplamaz), içinde 48 çukur kutu + 208×16 ve 136×13 çukur blok + şeridin yerinde 326×64 çukur blok. `primary-soft` üstünde iskelet bloklarını **renk değil `clay.sunken` çukurluğu** ayırır — E-27'nin kahraman kart iskeletiyle aynı dil | — |

E-posta `numberOfLines={1}` + `ellipsizeMode="tail"`. Avatar fotoğrafı, baş
harf dairesi ve maskot **yok** (marka: stok illüstrasyon ve avatar yasak).

### 4.3 Ayar satırları — `SettingRow` (gezinme varyantı)

Her satır **kendi kabarık yüzeyi**: `surface` + `clay.raised`, radius 16,
iç boşluk 16, satırlar arası 8, minimum yükseklik 76 (44 ikon + 2×16).

```
[44 `kat-kab.notr` · 20pt ikon] 12 │ body-strong  Başlık          │ 12 [20 chevron]
                                   │ caption      Değer / özet    │
```

| Grup | İkon | Başlık | İkincil satır (gerçek değerden) | Rota |
|---|---|---|---|---|
| Planın | `banknote` | Maaş ve bütçe | "Aylık net gelir 24.000 ₺ · 5 sabit gider" | `/butce` |
| Planın | `limitler` | Limitler | "Günlük 300 ₺ · 4 kategori limiti" | `/limitler` |
| Planın | `repeat` | Rutinler | "3 rutin · bu ay 1.240 ₺ tasarruf" | `/rutinler` |
| Kayıt kolaylıkları | `notebook` | Favoriler | "14 ürün, son fiyatlarıyla" | `/favoriler` |
| Kayıt kolaylıkları | `calendar-clock` | Taksitler | "2 seri · bu ay 1.350 ₺" | `/taksitler` |
| Takip | `chart` | Aylık özet | "Kategori payları ve haftalık ritim" | `/ozet` |
| Takip | `trending-up` | Seri | "12 gün · en uzun 21 gün" | `/seri` |
| Uygulama | `ayarlar` | Tüm ayarlar | "Hesap, bildirim, gün sınırı, yasal" | `/ayarlar` |
| Uygulama | `info` | Yardım | "Sık sorulan sorular" | `/yardim` |

**İkincil satır kuralı:** değer varsa **değer** yazılır ("Günlük 300 ₺ ·
4 kategori limiti"); veri o an yoksa **tanım** yazılır ("Günlük ve kategori
limitlerini belirle"). İki metin de bu belgede tanımlıdır, satır asla boş
kalmaz ve asla "…" göstermez. Değer satırı `numberOfLines={1}`.

Grup başlığı: kartsız `h2` (`SectionHeader`), üstünde 24, altında 8.
Gruptan gruba 24.

| Durum | Görünüm |
|---|---|
| `pressed` | Zemin `groove` + `clay.pressed` (prototip çerçeve 8'de "Limitler" satırı bu durumda çizildi) |
| `disabled` | Bu ekranda yok — hiçbir satır kilitli değil |
| `skeleton` | 44 çukur kare + 120×16 + 176×13 blok, satır yüksekliği korunur (yükleme bitince düzen zıplamaz) |

### 4.4 Alt bilgi

```
micro/text-2, ortalanmış:  "Trinkow · sürüm 1.0.0"
                    ↕ 8
[Kullanım şartları]  ·  [Gizlilik]     ← micro/`primary-text`, her biri 44 yükseklikte ghost
```

Her iki bağlantı `button.ghost`tur: yükseklik 44, yatay iç boşluk **16**
(tokens §7.1 — ghost'un iç boşluğu istisnasız 16; 12 kullanılmaz).

Yasal bağlantılar **her durumda** erişilebilir (hata durumunda da) — rev
sözleşmesinin gereği. `pressed` → `primary-press` (12pt satıra kil kabartma
uygulanamaz, opaklık yasak).

### 4.5 Metin deltası (E-28)

| Bugün | Yeni | Gerekçe |
|---|---|---|
| "Hesap, güvenlik, çıkış ve hesap silme işlemlerini ayarlardan yönetebilirsin." | **silindi** | Kimlik kartının kendisi oraya götürüyor |
| "Hesap ve uygulama ayarları" (düğme) | Başlıktaki ikon düğmesi + "Tüm ayarlar" satırı | Düğme değil, gezinme |
| "Oturum bilgisi bulunamadı" | "Hesapsız kullanıyorsun" | Hata değil, geçerli bir durum |
| "Maaş ve bütçem" / "Rutinlerim" / "Favorilerim" | "Maaş ve bütçe" / "Rutinler" / "Favoriler" | İyelik eki gereksiz; başlıklar aynı biçimde |
| "Günlük ve kategori limitleri" | "Limitler" + değer satırı | Başlık kısa, ayrıntı ikinci satırda |
| "Aylık özeti aç" | "Aylık özet" | Satır bir başlık, buton değil |
| "Planın" / "Analiz" (kart başlıkları) | "Planın" / "Kayıt kolaylıkları" / "Takip" / "Uygulama" | Dört anlamlı grup |
| "Yükleniyor…" | iskelet | — |

---

## 5. Bileşen envanteri deltası

| Bileşen | Tip | Karar |
|---|---|---|
| `LimitGauge` | **varyant** | `mod="birikim"` — §3.2'deki formülün **birebir aynısı**: `dolgu = max(0, hesaplanan_tasarruf)/harcanabilir` · `tasma = min(1, abs(min(0, hesaplanan_tasarruf))/harcanabilir)`. `dolgu = 0` ise ana yay ve topuz **çizilmez** (varsayılan `mod="gunluk"`'te dolgu *harcanan* olduğu için taşmada ana yay %100 kalır — iki kipin tek farkı bu). Geometri, renk, animasyon aynı |
| `HeroPlain` | mevcut | `no-budget` durumunda kullanılır (E-10'daki limitsiz varyantla aynı) |
| `EmptyState` | mevcut | `banknote` ikonuyla birikim hareketleri boşluğu |
| `ErrorState` | mevcut | `wifi-off` ikonuyla E-27 |
| `EquationRow` | mevcut (E-26) | Yeni bağlam: harcanabilir − harcanan = kalan. Yeni durum: `disinda` sonuç kutusu |
| `ProgressBar` | mevcut (E-25) | Yeni bağlam: tamamlanan gün sayacı |
| `CategoryShareRow` | **yeni (bileşim)** | `CategoryLimitBar` + `MonthLoadRow` geometrisi: 44 kap · ad/tutar · 12pt kategori çubuğu · pay/rutin satırı. Yeni ölçü açmaz |
| `SavingsMovementRow` | **varyant** | `SpendRow`: sol sütun **`.gun-kutu`** (E-15 deseni; ikon kabı değil), birincil satır yön metni, sağ altta "çekildi", trailing kaydır→Sil. Not yoksa ikincil satır çizilmez |
| `SavingsSheet` | **yeni (ekran parçası)** | `BottomSheet` + `SegmentedControl` + `AmountWell`(native) + `DateField` + `NoteField` + `button.primary`. İki kip: `mode="create" \| "edit"`; `edit` kipinde başlık değişir ve `button.ghost` "Sil" eklenir (§3.7) |
| `MonthPager` | **varyant** | E-10'daki `DayPager`ın ay karşılığı: iki `IconButton` + arada gösterge. Hata durumunda göstergesiz satır olarak da çizilir |
| `SettingRow` | **varyant** | Gezinme kipi: sol 44 `notr` ikon kabı, sağda `chevron-right`, ikincil satırda değer. Mevcut anahtar (switch) kipi korunur |
| `IdentityPanel` | **yeni** | Kahraman panel (`primary-soft` · r32 · `clay.raised-lg`) + 48 çukur ikon kutusu + iki satır + chevron; `signed-in` / `signed-out` / `error` / `skeleton`. Dört durumun dördü de aynı paneldir — aksan durum değiştirince kaybolmaz. **REV2-r2:** `signed-in`'de içine `FactStrip` girer (§4.2.1), panel 156pt |
| `FactStrip` | **varyant** | `InfoStrip`'in (§3.3) nötr kipi: zemin `well` (`serit-info`'nun `primary-soft`'u yerine), 20pt ikon + `label` olgu + `caption` bağlam, **dokunulamaz**. Yeni ölçü/renk/ikon açmaz; şu an tek kullanıcısı `IdentityPanel` |
| `AppFooter` | **yeni** | Sürüm satırı + iki yasal bağlantı |
| `TabBar` | **değişiklik** | FAB kaldırıldı; üç sekme `space-around`. `.sekme-alan` (84) yerine düz `.sekme-cubugu` (68) |
| `Accordion` | **yeni (REV3)** | Başlık düğmesi (`h2` + özet + dönen `chevron-down`) + katlanır içerik. Kap `surface`/r24/`clay.raised`; basılıda **tüm kap** çöker. Durumlar: açık · kapalı · basılı · yükleniyor · kısmi hata · veri yok. **Günlük ekranındaki rutin bölümüyle aynı bileşen** (`rev3-gunluk-rutin.md` §3) — iki ekranda iki ayrı açılır kap dili kurulmadı |
| `SavingsMovementRow` | **değişiklik (REV3)** | Akordiyon kabının içinde durduğu için bir basamak iner: `kuyu` (well + `clay.sunken`); içindeki `.gun-kutu` `raised`'a çıkar. Kaydırarak silme, 6 sn geri al ve sheet davranışı aynı |
| `EmptyState` | **kapsam daralması (REV3)** | 176pt diskli boş durum E-27'de yalnız **kahraman** için kalır (`HeroPlain`). Akordiyon bölümünün içindeki boşluk illüstrasyonsuzdur (body + caption): disk bir bölüm kabının içine girince aynı yüksekliği iki kez söyler |

---

## 6. Erişilebilirlik

| Konu | Karar |
|---|---|
| Dokunma hedefi | Hepsi ≥44×44. Kategori çubuğu ve ilerleme çubuğu **dokunulmaz** (bilgi), bu yüzden hedef gerektirmez |
| **Akordiyon** (REV3) | Başlık `accessibilityRole="button"` + `accessibilityState={{expanded}}`, etiket "{başlık}. {özet}" — **özet açıkken de etikette kalır**. Kapalı bölümün içeriği mount edilmediği için ekran okuyucu onu görmez. Ayrıntı §3.12.7 |
| Gösterge | `accessibilityRole="progressbar"`, `accessibilityValue={{min:0,max:harcanabilir,now:biriken}}`, etiket "Bu ayın biriken payı"; `overflow`'da etiket "Bütçe dışı {tutar}" |
| Ay okları | "Önceki ay" / "Sonraki ay" + `accessibilityState={{disabled:true}}` sınırda |
| Hareket satırı | Etiket: "Birikime eklendi, 23 Eylül, 1.500 ₺, not: Kenara ayırdım". Kaydırma eylemi için `accessibilityActions=[{name:'delete',label:'Sil'}]` |
| Segment | `accessibilityRole="tab"` + `accessibilityState={{selected}}` |
| Ayar satırı | Etiket: "{başlık}. {değer satırı}" · `accessibilityRole="button"` |
| Kimlik paneli | Tek basma hedefi olduğu için etiket birleşir: "Hesabını aç. {e-posta}, {sağlayıcı}. {olgu}, {bağlam}" (`a11y.profil.kimlikSerit`). Olgu şeridi ayrı odak almaz — dokunulamaz bilgi. Aynı sayı **Seri** satırında da okunur; görünen olgunun iki kez duyulması kabul edildi, gizlemek yerine (§7/11) |
| Kategori | Renk + ikon + ad üçlüsü; çubuk ayrıca "payı %27" yazısıyla okunur |
| Hata | Alan hatası `accessibilityLiveRegion="polite"` ile duyurulur |
| Dinamik yazı | Kartlar büyür, tutar satırı sarabilir; hiçbir açıklama tek satıra kilitlenmemiştir. Tek satıra kilitli olanlar: e-posta, kategori adı, ayar değeri — hepsi kırpılır, taşmaz |
| Reduce motion | Tüm süreler 0ms; gösterge son değerine anında oturur |
| Kontrast | Kullanılan çiftlerin tamamı tokens §1.9'da onaylı. Yeni çift üretilmedi; `warning-ink`/`warning-soft` (5.86) tek yeni **bağlam** |

---

## 7. Bilinçli kararlar — `design-reviewer`'ın bilmesi gerekenler

> **REV3 kararları (bu turda eklenen) — §7.R**
>
> **R-a · Akordiyon dışında kalan iki şey.** Kahraman kart ve ay gezinmesi
> hiçbir zaman katlanmaz: ekranın kimliği ve gezinmesi bir dokunuşun ardına
> saklanamaz. Motivasyon şeridi ise akordiyonun *içine* girdi (B), çünkü
> önerdiği eylem oradadır.
>
> **R-b · Açıkken özet gizleniyor.** Başlık satırının içeriği duruma göre
> değişiyor; bu bilinçli. Alternatif ("özet her zaman görünür") denendi ve
> düşürüldü: A açıkken başlıkta "Kalan 8.760 ₺", 2 cm altında denklem
> kutusunda yine "Kalan 8.760 ₺" çıkıyordu. Ekran okuyucu etiketinde özet
> **korunuyor** (§3.12.7).
>
> **R-c · Çoklu açık serbest, hafıza ekrandan çıkışta sıfırlanıyor.** İkisi
> birbirini dengeliyor: kullanıcı istediği kadar bölüm açabilir, ama ekran
> her açılışta aynı sözü verir (tek net mesaj). Aylar arası geçişte hafıza
> **korunur** — ay karşılaştırırken aynı bölümü tekrar açmak zorunda kalmak
> kullanıcıyı cezalandırırdı.
>
> **R-d · Rutin tasarrufu bölümü ekranda kaldı.** Direktifin sözü "Tasarruf
> sayfasına ayrı bir rutinlerim kısmı yapmışsın, gerek yok"tu; kalkan şey
> **günlük hızlı eylem**. Tutar bir finansal bilgidir ve ürünün başka hiçbir
> yüzeyinde toplanmıyor → en dar hâliyle (kapalıyken 76pt tek satır özet)
> kaldı. Tamamen kaldırma istenirse tutarın nereye gideceği yazılı olarak
> çözülmeden uygulanmamalı (**PM kararı**, §13/R7).
>
> **R-e · Boş durum diski akordiyonun içine girmiyor.** 176pt kabarık disk
> §9/9'un canlılık reçetesinde var; bölüm kabının içinde kullanılması hem
> §9/3'ü (aynı yükseklik iki kez) hem tek kahraman kuralını zorlardı. Diskin
> E-27'deki tek kullanıcısı artık `HeroPlain` (F3).
>
> **R-f · Akordiyon başlığı hem başlık hem düğme.** Görsel olarak `h2`,
> semantik olarak `button` + `accessibilityState={{expanded}}`. RN'de
> disclosure rolü yoktur; en yakın doğru eşleme budur.
>
> **R-g · Bölüm sayısı 4'te sabitlendi.** Beşinci bir bölüm (ör. "Takip
> başından beri") açılmadı; o değer A'nın içinde tek satır olarak duruyor.
> Akordiyon bir menüye dönüşmemeli: dört katlanır kutu tarama sınırının
> içinde, yedi kutu yeni bir liste ekranıdır.


1. **"bütçe dışı" terimi.** Sözlükte "limit dışı" günlük limit için kilitli.
   Ay bütçesi farklı bir sınır olduğu için aynı kalıpla **"bütçe dışı"**
   türetildi (aynı `warning` ailesi, aynı görsel dil). Alternatif "-2.150 ₺"
   yazımı brandbook §2.5 ile yasak. → **PM onayladı (REV2-r2)**; terim
   `metinler.md` §0.1 sözlüğüne, *limit dışı* ile ayrımı açıkça yazılarak
   girdi: *limit dışı* **günlük limite**, *bütçe dışı* **ay bütçesine**
   bağlıdır; bir gün limit dışı olup ay bütçe içinde kalabilir.
2. **Kahraman sayı çoğu zaman 32pt olacak.** Tasarruf tutarları 4+ hanelidir,
   tokens §7.5'in taşma kuralı devreye girer ve `hero` 56 → `display` 32 iner.
   Sonuç: "kahraman sayı / etiket ≥4×" oranı (tokens §2.3) bu ekranda 2.46×'e
   düşer. Bu, tokens'ın kendi taşma kuralının kaçınılmaz sonucudur; kahramanlık
   ölçüden değil **224pt kil gösterge + `primary-soft` panel**den gelir.
   Alternatif (tutarı kısaltmak, göstergeyi büyütmek) iki ayrı kuralı ihlal
   ederdi.
3. **Yay dolgusu "biriken/harcanabilir" ve bütçe dışında ana yay yok.** Günlük
   ekranında yay *harcananı* doldurur, burada *bireni*. Bunun zorunlu sonucu:
   bütçe dışı ayda dolgu 0'dır ve **ana yay hiç çizilmez** — tokens §7.5'in
   "ana yay %100 kalır" satırı dolgunun *harcanan* olduğu kipe aittir. İki
   ekranda aynı grafik zıt yönde dolduğu için merkez etiketi zorunlu: "bu ay
   biriken". Kabul edilebilir bulunmazsa ikinci seçenek dolguyu
   "harcanan/harcanabilir" yapıp merkeze yine bireni yazmaktır (Günlük'le
   birebir aynı mantık, ama dolan yay "kötü haber" okunur).
4. **Birikim yön ikonu tek glif.** Ekleme/çekme aynı `banknote` ikonunu
   kullanır; yön yazıyla verilir. Gerekçe: yeni glif eklemek ikon setini
   genişletir (varlıklar kilitli) ve renkle kodlamak WCAG 1.4.1'e takılır.
5. **Yeşil kullanılmadı, ama iki ayrı gerekçeyle** (§3.5). `success` bir grafik
   rengi olarak **kullanılamaz** (2.85 < 3:1). `success-ink` bir metin rengi
   olarak **kullanılabilir** (4.90 ✅) — teknik engel yok; kullanılmadı, çünkü
   hedefe yaklaşmayı renkle övmek "yeşil = iyi / kırmızı = kötü" kodlamasını
   açar. PM isterse `success-ink` yalnız metin olarak açılabilir; hedef
   çubuğunun dolgusu her hâlde `grad.action` kalır.
6. **Hata ekranında ay okları duruyor.** Kahraman kart yokken pager kendi
   satırında çizilir — aynı iki `IconButton`, arada `label`. İkinci bir
   navigasyon deseni değil, aynı desenin kartsız hâli.
7. **`stil-rev2.css`** bu belgeye ait **üç** delta kuralı içerir: §1 hero
   sayısının `warning-ink` varyantı · §2 denklem sonuç kutusunun `disinda` hâli ·
   §8 boş durum diskinin `clay.raised`'a inmesi. Dosya rev2'deki diğer ekran
   çalışmasıyla ortaktır; **§3-§7 blokları o çalışmaya aittir ve bu turda
   ellenmedi.**
8. **Profil'in aksan oranı takviyeyle %23,5'e çıktı** (§8/2 · REV2-r2,
   REV3-r1'de yeniden ölçüldü). r1'de ölçülen **%14,2** hedefin (%18-22)
   altındaydı ve ✅ işaretlenmedi. r2'de
   PM kararıyla token-nötr takviye uygulandı: panelin içine **bir** `clay.sunken`
   olgu şeridi (§4.2.1) — panel 80 → 156pt, aksan **%14,2 → %23,5**. Üç kısıt
   tutuldu: kahraman sayı üretilmedi (roller `label`/`caption`), yeni veri alanı
   istenmedi (şerit Seri satırının değerini gösterir), yeni token/renk/ikon
   açılmadı. Reddedilen alternatif hâlâ reddedilmiştir: **ayar satırlarını
   renklendirmek** — kategori renk dilini çalar ve dokuz satırın hepsine
   "önemli" der.
9. **Kip çipinin rotası var.** `.cip.secili` bir seçim dilidir; tıklanabilir
   görünüp iş yapmayan kontrol bırakılmadı. Çip `→ /ayarlar` (Plan ve profil)
   rotasına bağlandı; kipin değiştirildiği tek yer orası. Rota PM tarafından
   reddedilirse çip `View` olarak çizilir ve `.cip.secili` yerine düz `.cip`
   kullanılır.
10. **`tokens.md`'de üç düzeltme yapıldı** (PM izniyle, §13.4'te gerekçeli):
   (a) §2.3'teki "yayın iç alanı 198px" → **156px** (198, v3.1'in 296pt
   diskinden kalmış); §7.5'in ölçüm satırı gerçek font ölçümleriyle düzeltildi.
   (b) §7.3'teki "sağa kaydırma → Sil" → **sağdan sola (trailing)**; soldan
   sağa iOS'un sistem geri hareketidir.
   (c) **r2 · H3:** §7.5'in ölçüm satırı bir kez daha düzeltildi, çünkü
   sayılar **oransal** rakam genişliğiyle alınmıştı; §2.3 parada `tabular-nums`
   zorunlu olduğu için aynı hane sayısındaki iki tutar eşit genişlikte olmak
   zorunda (`1.250 ₺` = `6.240 ₺` = **189px**). Yeni set 139 / 189 / 189 / 226
   ve §7.5'e ölçümün **formülü** yazıldı ki bir daha tahminle türetilmesin.
   Kuralın sonucu değişmedi: 4+ hane daima `display` 32.

11. **Olgu şeridi ekran okuyucuda panelin etiketine karışıyor.** Panel tek
   basma hedefi (`accessibilityRole="button"`), çocukları ayrı odak almıyor;
   bu yüzden şeridin metni `a11y.profil.kimlikSerit` ile etiketin sonuna
   eklendi. Sonuç: aynı olgu ekranda iki yerde duyuluyor (panel etiketi +
   **Seri** ayar satırı). Alternatifler tartıldı ve reddedildi:
   *(i)* şeridi `importantForAccessibility="no-hide-descendants"` ile gizlemek
   — görünen içeriği AT'den saklamak bu projede yapılmayan bir şey;
   *(ii)* paneli ikiye bölüp yalnız kimlik satırını basılabilir yapmak —
   `primary-soft` üstünde satır için yeni bir dinlenme/basılı yüzey çifti
   gerekirdi, yani yeni token. Tekrarı kabul etmek ikisinden de ucuz.
> **R-h · Aksan oranı NET alanla ölçülüyor (REV3-r1).** §8/2'nin %25-45
> bandı r0'da iki farklı yöntemle ölçülüyordu: kahraman ekranı brüt panel
> alanıyla, gezinme ekranı aksan yüzeylerinin toplamıyla. İlk kat 766'dan
> **693**'e düzeltilince (B1) kahramanın brütü %48,7'ye çıktı, yani bandın
> 3,7 puan üstüne. Karar: ölçü **net**tir — panelin ortasındaki 224pt beyaz
> disk ve iki beyaz çip aksan rengiyle boyanmış piksel değildir, panelin
> *üstünde duran ayrı nesnelerdir*. Net **%30,4**, bandın ortasına yakın.
> Bandın kendisi değişmedi; iki arkitip artık aynı soruyu aynı yöntemle
> cevaplıyor ("ilk katın ne kadarı gerçekten mavi?"). Brüt rakam şeffaflık
> için §8/2'de yazılı kalıyor.

8. **Kümülatif tasarruf** ("Takip başından beri biriken") bütçe kartının son
   satırında duruyor. Kendi kartını hak edecek kadar sık okunmuyor, ama
   silinecek kadar da değersiz değil.

---

## 8. CANLILIK REÇETESİ (uygulama geneli)

> Teşhis: ekranlar "sakin" değil **cansız** (brandbook §2.1'in ayrımı).
> Sebep tek tek somut ve hepsi token kullanımıyla ilgili — palet değişmiyor,
> **kullanım oranı** değişiyor. Her madde: *ne yapılacak · hangi token ·
> hangi ekran.*

| # | Sorun (bugün) | Reçete | Token | Ekran |
|---|---|---|---|---|
| 1 | **Ekranda hiç büyük sayı yok.** En büyük tipografi 26pt `h1` (Poppins, rakam için değil) | Her sekme ekranının **tam olarak bir** kahraman sayısı olacak: Günlük → bugün kalan, Tasarruf → bu ay biriken, Profil → **yok** (Profil bir gezinme ekranıdır, kahramanı kimlik kartıdır) | `hero` 56 / `display` 32 · `amount` 17 | E-10 ✔, **E-27 yeni**, E-28 |
| 2 | **Aksan rengi hiç görünmüyor** — bütün ekran beyaz kart + açık mavi zemin | Her sekme ekranının **ilk nesnesi** `primary-soft` + `clay.raised-lg` bir panel olacak. Oran ekran arkitipine göre ölçülür (aşağıdaki tablo) | `primary-soft` `#E4EEFE` + `clay.raised-lg` | E-27 kahraman kart · E-10 ✔ · **E-28 kimlik paneli (yeni)** |
| 3 | **Kategoriler renksiz metin** (`Txt role="label"` + iki satır) | Kategori geçen her yerde **44 kap (`cat.*.soft`) + 20pt ikon (`cat.*.solid`) + ad**; dağılım çubuğu kategori renginde | `cat.mavi/lacivert/yesil/amber/kiremit/duman` | E-27 kategori kartı · E-14 · E-15 · E-16 |
| 4 | **Tek derinlik**: her şey `clay.raised` kart | Her ekranda üç derinlik birden: `raised-lg` (kahraman/sheet/boş durum) · `raised` (kart, satır) · `sunken` (oluk, kuyu, şerit, ikon kabı). Bir ekranda `sunken` yoksa o ekran düzdür | `clay.raised-lg` · `clay.raised` · `clay.sunken` | tüm ekranlar |
| 5 | **Eylem hiyerarşisi yok**: 5-7 `secondary` düğme alt alta, yer yer iki `primary` | Ekran başına **en fazla 1** `primary`. Gezinme düğmeyle değil **satırla** yapılır (`SettingRow` + chevron) | `button.primary` · `.ayar-satir` | E-28 (7 düğme → 9 satır) · E-27 (2 primary → 1, o da sheet'te) |
| 6 | **Boşluk ritmi düz**: `RevScreen` tüm çocuklara `gap: 24` veriyor, kart içi `gap: 12` | Ritim üç kademeli olacak: **8** (aynı grubun satırları) · **12** (kart içi bloklar) · **24** (ekran düzeyi bloklar). `gap` yerine açık `View` ayırıcı. **Kapsam: yalnız E-27 ve E-28** — `content.gap` bu iki ekranda `0`'a iner ve ayırıcılar §3/§4'te çizili; v4'te PASS almış diğer ~16 ekran `gap: 24` ile kalır (bkz. §10) | tokens §3.1 | E-27 · E-28 |
| 7 | **Kart iç boşluğu 24** (kod) ↔ tokens 16 | `card.padding` **16**, istisnasız; kahraman kart da 16. **Kapsam: global** — tokens §3.1 zaten 16 diyor, 24 kodun sapmasıydı; düzeltme tüm ekranlara uygulanır | tokens §3.1 | `RevScreen.card` (global) |
| 8 | **Yükleme = "Yükleniyor…" tek satır** → ekran ölü | ≥150ms okumada **iskelet**: gerçek düzenin kutuları yerinde, içleri `well` + `clay.sunken`. Shimmer yok, tam ekran spinner yok. **Kapsam: iskeleti bu belgede çizilmiş ekran `Skeleton` kullanır** (E-27, E-28); iskeleti çizilmemiş ekran `LoadState`'te kalır — çizilmemiş iskelet, kendi düzenini bilmeyen iskelettir | `well` · `clay.sunken` | E-27 · E-28 |
| 9 | **Boş durum = düz cümle** | Boş durum = **176pt kabarık disk + 32pt ikon + başlık + tek cümle** (+ yalnız oradan yapılabilecek bir iş varsa düğme). Her yüzeyde **farklı** metin | `EmptyGauge` · `surface` + `clay.raised-lg` | E-27 (2 farklı boşluk) · E-14 · E-15 · E-16 · E-18 · **REV3 daraltması:** 176pt disk bir akordiyon bölümünün İÇİNDE kullanılmaz (aynı yükseklik iki kez + ikinci kahraman riski); bölüm içi boşluk illüstrasyonsuzdur (body + caption). E-27'de diskin tek kullanıcısı `HeroPlain` |
| 10 | **Basılı durum var ama nesne hissi yok** — düğme yığınında basılan şey "satır" değil | Her dokunulabilir yüzey kendi kabarık nesnesi olacak ve basınca **çöker** (`groove` + `clay.pressed`), küçülmez. 150ms | `clay.pressed` · `groove` | E-28 ayar satırları · E-27 hareket satırları |
| 11 | **Hareket yok** | İnşa edilebilir dört mikro-hareket: (a) gösterge yayı 250ms ease-out + sayı eş zamanlı sayar, (b) sheet 250ms yukarı, (c) toast 200ms giriş / 6 sn "Geri al", (d) milestone kartı 1.2 sn. `Animated`/`Reanimated`; reduce-motion → 0ms. **Konfeti, zıplama, parıltı yok** | tokens §8 | E-27 gösterge + sheet + toast |
| 12 | **Metin "sistem sesi" gibi**: açıklama paragrafları, sorumluluk reddi cümleleri | Önce sayı, sonra ≤12 kelime tespit. Sorumluluk reddi ve teknik açıklama silinir (§3.11'de 18 satır) | brandbook §2.2 | E-27 ✔ · E-28 ✔ |
| 13 | **Olumlu pekiştirme yok ama övgü de yasak** | Nötr tespit cümleleri (övgü değil, sayı + olgu): "Bu hafta 4 gün limit altında." · "Bu ay 1.500 ₺ ayırdın." · "12 gündür kayıt giriyorsun." · "Hedefine 500 ₺ kaldı." | `caption`/`label` | E-27 birikim kartı · E-10 · E-21 |
| 14 | **Tutar tipografisi gövde metniyle aynı** | Para **daima** `amount`/`display`/`hero` + `tabular-nums`; `h1`/`h2` (Poppins) rakam taşımaz | tokens §2.3 | her yer — bugün `tasarruflar.tsx` ve `profil.tsx` ihlal ediyor |

**§8/2'nin ölçülebilir hâli (REV3-r1'de yeniden ölçüldü).** İlk kat
**§3.12.1'in tek kaynağından** gelir: `.kaydir`'ın görünür yüksekliği
**693** (prototip kabuğu) / **687** (gerçek cihaz), yüzen sekme çubuğu
kaydırma alanının DIŞINDA. Profil de sekmeli bir ekrandır, yani onun da ilk
katı 693'tür — r0'ın buradaki `766` rakamı §3.12.1'de düzeltilen aynı yanlış
viewport'tan geliyordu ve **B1'in artığıydı.** İlk kat alanı:
390 × 693 = **270.270 px²** (%9,5 daha küçük pencere).

**Ölçüt net alanla ölçülür.** Aksan = ilk katta **gerçekten aksan rengiyle
boyanmış** piksel. Üstüne çizilen beyaz disk ve beyaz çipler aksan değildir;
onlar panelin üstünde duran ayrı nesnelerdir. Brüt rakam yalnız şeffaflık
için raporlanır. (r0 iki arkitipi iki farklı yöntemle ölçüyordu: kahramanı
brütle, gezinmeyi yüzey toplamıyla. Artık ikisi de net.)

| Arkitip | Ölçüt (net) | Ölçülen (693) | Nasıl |
|---|---|---|---|
| **Kahraman ekranı** (E-10, E-27) | `primary-soft` panel ilk katın **%25-45**'i | E-27: **%30,4** net · (%48,7 brüt) | Panel 358×368 = 131.744 (§3.12.1'de 364→368 düzeltildi). Düşülen: 224pt beyaz disk π·112² = 39.408 + iki çip 40pt × toplam 256pt = 10.240 → net 82.096 |
| **Gezinme ekranı** (E-28 Profil) | Kahraman sayı yok; aksan yüzey **≥%12** ve ekranın **ilk nesnesi** olmak zorunda | E-28: **%23,5** | Kimlik paneli 358×156 = 55.848 (%20,7) + ilk katta **tam** görünen 4 `kat-kab.notr` kabı 4×44×44 = 7.744 (%2,9) |

**Ölçüm nasıl yapıldı (E-28, 693'e karşı).** İlk kat yığını, üstten:
`.ekran-basi` 8+50+16 = **74** → panel **156** (→230) → 24 → `h2` 25 (→279)
→ 8 → üç ayar satırı 76 + iki 8 boşluk = 244 (→531) → 24 → `h2` 25 (→580)
→ 8 → 4'üncü satır 76 (→664) → 8 → 5'inci satır 76 (→**748**).
Kesme **687-693** bandı 5'inci satırın İÇİNE, üst iç boşluğuna düşer
(satırın 15-21 px'i görünür; ikon kabı 688'de başlar, yani 687'de hiç,
693'te 5 px'i görünür). Yani ilk katta **4 ayar satırı tam** görünür, 5'inci
bir şerit olarak belirir. Aksan = 55.848 + 7.744 = **63.592** / 270.270 =
**%23,5**. (5'inci kabın en çok 44×5 = 220 px'lik dilimi sayılmadı: %0,08,
yuvarlamayı değiştirmiyor.)

> **r1 ile karşılaştırma, aynı pencereye karşı (693).** Panel 358×80 = 28.640
> (%10,6); r1 yığınında satırlar 76 px yukarıda başladığı için 5 kap tam
> görünüyordu (5×1.936 = 9.680 · %3,6) ve 6'ncı satır 680-756'da, yani
> kesmenin 7-13 px altındaydı. Toplam 38.320 / 270.270 = **%14,2**.
> Panelin +76 px'i bir ayar satırını ilk katın dışına itti; aksan
> **%14,2 → %23,5**. (r0 bu iki sayıyı 766'lık pencereyle %13,1 → %21,9
> diye yazmıştı; yön aynı, büyüklükler yanlıştı.)

**Kesme neden burada sorun değil.** E-27'de kesmenin bir kartın değil bir
**boşluğun** içine düşmesi şart koşuldu (§3.12.1), çünkü orada ilk kat bir
kompozisyondur: kahraman sayı ve A bölümü birlikte okunur. E-28'in ilk katı
bir **listedir**; kesmenin 5'inci satırın üst iç boşluğuna düşmesi
kaydırılabilirliğin işaretidir — tam bitmiş bir liste "bu kadar" der.
Kesme hiçbir **sayının, etiketin veya panelin** üstünden geçmiyor.

**Kahraman brütü bandın üstünde, neti içinde.** %25-45 bandı yanlış pencereye
(766) yazılmıştı; doğru pencerede brüt %48,7'ye çıkıyor. Bandın cevapladığı
soru "ilk katın ne kadarı mavi?" olduğu için ölçünün **net** olması gerekir:
panelin ortasındaki 224pt beyaz disk mavi değildir. Net **%30,4** bandın
içinde ve bandın orta noktasına yakın. Bu, `design-reviewer`'ın bilmesi
gereken bilinçli bir karardır — ölçüt gevşetilmedi, **yöntemi tek hâle
getirildi** (bkz. §7.R-h).

Gezinme ekranının kahraman **ekranı** oranına (%25-45) çıkmasının tek yolu ayar
satırlarını renklendirmektir; o da kategori renk dilini çalar ve dokuz satırın
hepsine "önemli" der. Ölçüt bu yüzden arkitipe bağlandı, tek sayıya değil.
Arkitip eşiği (≥%12) r2'de **%23,5** ile fazlasıyla karşılanıyor — küçülen
pencere oranı düşürmedi, **yükseltti**; panel ilk katın beşte birinden
fazlasını tek başına tutuyor ve "mavi şerit" değil nesne gibi okunuyor.

**Türev token önerisi: yok.** 14 maddenin hiçbiri yeni değer gerektirmedi;
hepsi mevcut tokens v4 değerlerinin **doğru yerde ve doğru oranda**
kullanılmasıdır. Tek yeni *bağlam*: `warning-ink`/`warning-soft` çiftinin
"bütçe dışı" için kullanılması (oran zaten §1.9'da onaylı).

---

## 9. Anti-pattern öz-denetimi

| # | Madde | Durum |
|---|---|---|
| 1 | Mor-mavi varsayılan gradyan | ✅ Palet tokens v4 mavisi; izinli gradyan yalnız `grad.action`/`grad.arc`, indigo-violet yok |
| 2 | Her elemanda glassmorphism | ✅ `blur` katmanı yok; derinlik kil gölgesiyle |
| 3 | Amaçsız drop-shadow | ✅ Üç gölge seviyesi anlam taşır: `raised-lg` kahraman/sheet/kimlik paneli, `raised` nesne (kart, **akordiyon kabı**), `sunken` oluk/kuyu. Aynı yükseklik iç içe iki kez kullanılmaz — boş durum diski `raised-lg` kartın içinde `raised`'a iner; **REV3:** akordiyonun içindeki hareket satırı `raised`'dan `sunken`'a iner ve satırın içindeki gün kutusu `raised`'a çıkar. §2.3'te tablo |
| 4 | Karışık köşe yarıçapı | ✅ Yalnız 16 / 24 / 32 / 999; eleman tipinden türer (§2.3). Prototip taraması: inline radius tek değer, 16. Akordiyon kabı 24 (kart ailesi), içindeki satır ve eylem düğmesi 16 (satır ailesi) — **REV3'te yeni radius değeri açılmadı** |
| 5 | Varsayılan font (Inter/Poppins/Montserrat gerekçesiz) | ⚠️ Montserrat + Poppins kullanılıyor — **bu proje kararı** (tokens §2.1: `₺` glifi ve `tnum` doğrulaması yapılarak seçildi, JetBrains Mono bu yüzden düşürüldü). Bu belge font değiştirmez |
| 6 | 3 sütunlu "daire ikon + başlık + 1 cümle" kartı | ✅ Yok. İkon kapları **kare** (radius 16) ve satırın solunda; üçlü özellik ızgarası hiç kurulmadı |
| 7 | Stok illüstrasyon | ✅ Tek çizim primitifi kil diskin kendisi (`EmptyGauge`); maskot, avatar, undraw yok |
| 8 | Kimliksiz "SaaS şablonu" beyaz boşluk | ✅ Zemin `#E6EFFE`, saf beyaz yalnız yüzeylerde; kahraman panel `primary-soft` |
| 9 | Jenerik pazarlama dili | ✅ En uzun cümle 8 kelime; "finansal özgürlük" tipi ifade yok, övgü yok, ünlem yok |
| 10 | Düşük kontrastlı açık gri metin | ✅ Tüm çiftler tokens §1.9'dan. **`text-3` bu iki ekranda hiç kullanılmıyor** (kuyu zemininde 4.50 ile AA altı kalıyordu — tokens §1.2); placeholder ve pasif tutar dahil en düşük çift `text-2`/`well` = **5.13** |
| 11 | Rastgele boşluk | ✅ Yalnız 4/8/12/16/24; her değerin tek işi §2.1'de yazılı. Prototip taraması (12 yüzey): dikey ayırıcılar **yalnız** `h4` (73) · `h8` (91) · `h12` (74) · `h24` (55), yatay `w4` (8) · `w8` (27) · `w12` (143). 16 hiç ayırıcı olarak geçmiyor — yalnız iç boşluk. **REV3:** akordiyon bölümleri arası 8, kahraman ↔ akordiyon 24 — ikisinin gerekçesi §2.1'de yazılı |
| 12 | Dark mode'un renk ters çevirerek üretilmesi | ✅ Karanlık mod Faz 2; bu belgede üretilmedi |
| 13 | Emoji | ✅ Tarandı: 0 |
| 14 | Brandbook dışı renk | ✅ Palet dışı hex yok. `<main>` içindeki tek ham hex kümesi SVG yay duraklarıdır (`#3B82F6 #2F68C5 #D97706 #B45309 #E6EFFE #F2F7FE #FFFFFF`) — hepsi token değeri, v4 `01-gunluk.html` ile aynı zorunluluk (SVG `stop-color` değişken almaz) |
| 15 | Gerçek içerik | ✅ Tüm sayılar API sözleşmesinden türetilmiş tutarlı bir ay (24.000 / 15.240 / 8.760 / 6.240; kategori toplamı 15.240'a eşit; kategori "rutin" etiketleri 760 + 480 = rutin kartının 1.240'ı = Profil'deki rutin satırı). Lorem/"Feature 1" yok |
| 16 | `:hover` / grid / `::before` / `calc` / `z-index` | ✅ `<main>` taraması: 0 bulgu. Yalnız flexbox |
| 17 | Basılı durum | ✅ Her etkileşimli eleman için tanımlı; prototipte iki örnek **çizili** (hareket satırı F1, ayar satırı F8). Hover hiçbir yerde yok |
| 18 | Boş/yükleniyor/hata/uzun metin | ✅ **15** çerçevenin 7'si bu durumlar (bütçe dışı ay · ilk ay · iskelet ×2 · tüm ekran hatası · **kısmi hata + verisi olmayan açık bölüm** · alan hatası); uzun e-posta, 40 hareketlik liste ve 7 haneli tutar kuralı ayrıca yazılı. **Kapalı bölüm özetleri veri yokken bile dolu** (§3.12.4) |
| 19 | Ekran başına mood | ✅ Tasarruf = "ölçüm panosu" — REV3'te netleşti: **tek kahraman + açık tek cevap + katlanmış çekmeceler** · Profil = "düzenli çekmece" (kahramansız, ritmik satırlar) · Günlük = "günün kontrol listesi". Aynı aile, üç ayrı iş |
| 20 | Kontrast WCAG AA | ✅ Yeni çift üretilmedi; kullanılanların tamamı §1.9'da hesaplı |

---

## 10. Uygulama notu (frontend-developer'a)

Bu belge **kod değiştirmedi.** Uygulanırken beklenen dosyalar:
`app/app/tasarruflar.tsx` (yeniden yazım), `app/app/profil.tsx` (yeniden yazım),
`app/src/components/` altında §5'teki yeni/varyant bileşenler,
`app/src/components/TabBar.tsx` (FAB kaldırma — halihazırda `RevScreen`'den
düşürülmüş). Metinler `app/src/content/metinler.ts` üzerinden; bu belgedeki
tablolar `projects/trinkow/docs/content/metinler.md` **§28**'e girildi
(§28.1 E-27, §28.2 E-28 — §27 zaten E-11 ürün aramasına ayrılmıştı).

### 10.1 `RevScreen.tsx` — üç değişiklik, üç ayrı kapsam

Bu üç madde birbirinden **ayrı** uygulanır. v4'te PASS almış ~16 ekran
`RevScreen` üzerinden çiziliyor; hepsini birden değiştirmek tasarımı
denetlenmemiş ekranlarda regresyon üretir.

| Değişiklik | Kapsam | Gerekçe |
|---|---|---|
| `card.padding` **24 → 16** | **Global.** Tüm ekranlar. | tokens §3.1 zaten "kart iç boşluğu 16, istisnasız" diyor; koddaki 24 bir sapmaydı. Düzeltmek tasarımı tokens'a yaklaştırır, uzaklaştırmaz |
| `content.gap` **24 → 0** + açık `View` ayırıcılar | **Yalnız E-27 ve E-28.** Diğer ekranlar `gap: 24` ile kalır. | Üç kademeli ritim (8/12/24) yalnız ritmi bu belgede çizilmiş iki ekran için tanımlı. `gap: 0` global yapılırsa ayırıcısı yazılmamış her ekran tek bloğa çöker. Uygulama yolu: `RevScreen`'e `contentGap?: 0 \| 24` (varsayılan 24), bu iki ekran `0` geçer |
| `LoadState` → `Skeleton` | **Yalnız iskeleti çizilmiş ekranlar** (E-27, E-28; E-10 ve E-15 v4'te çizildi). Diğerleri `LoadState`'te kalır. | İskelet, o ekranın düzenini bilmek zorundadır. Çizilmemiş iskelet "kutuları rastgele yerleştiren" bir bileşen olur ve yükleme bitince düzen zıplar. `Skeleton` yeni bir bileşen olarak eklenir, `LoadState` **kaldırılmaz** |

Kalan ~16 ekranın ritim ve iskelet dönüşümü ayrı bir tur işidir; o ekranların
her biri için iskelet düzeni çizilmeden `Skeleton`'a geçilmez.

### 10.2 REV3 — beklenen dosyalar

| Dosya | İş |
|---|---|
| `app/src/components/Accordion.tsx` | **yeni.** Başlık düğmesi + özet + dönen chevron + katlanır içerik; `expanded` durumu dışarıdan verilir (ekran sahibi tutar). `LayoutAnimation.configureNext` + `AccessibilityInfo.isReduceMotionEnabled` |
| `app/app/tasarruflar.tsx` | Dört bölüme paketleme; açık/kapalı durumu `useState<Record<string, boolean>>`, varsayılan `{butce: true}`. Ay değişince **sıfırlanmaz** |
| `app/src/components/pano/RoutineQuickSection.tsx` | **yeni.** Günlük'ün rutin bölümü — aynı `Accordion`'u kullanır (`rev3-gunluk-rutin.md` §9) |
| `app/src/components/pano/GunlukSayfa.tsx` | Kategori kartından **8pt** sonra bölümü monte etmek; rutin yoksa hiç monte etmemek |
| `app/app/rutinler.tsx` | Yalnız **temizlik**: günlük eylem düğmeleri ("+ Harcama ekle", "Bugün almadım", adet alanı, "Bugünkü vazgeçişi geri al") kaldırılır; ekle/düzenle/kaldır kalır |
| `app/src/content/metinler.ts` | §28.3 (akordiyon özetleri) + §29 (rutin satırı) anahtarları |

**Akordiyon hafızası bileşende değil, ekran sahibinde.** `Accordion` kendi
`expanded` durumunu tutmaz — `open` + `onToggle` alır. Hafızanın ömrünü ekran
belirler, çünkü iki ekranın cevabı farklı:

| Ekran | Hafıza | Neden |
|---|---|---|
| **E-10 Günlük** | **Cihazda kalıcı** (`AsyncStorage`, tek anahtar) | Günlük günde birkaç kez açılır; kullanıcı bölümü kapattıysa "bugünkü rutinlerimi kapattım" demiştir, uygulamayı her açışında onu tekrar kapatmak zorunda kalmamalı |
| **E-27 Tasarruf** | **Ekran ömrü** — çıkışta `{butce: true}` varsayılanına döner | Tasarruf bir inceleme ekranıdır; her girişte aynı yerden başlamak (bütçe açık, diğerleri kapalı) ekranı öngörülebilir kılar. Ay değişince **sıfırlanmaz** (aynı oturumda ay gezerken bölüm kapanmaz) |

Bileşen bu farkı bilmez; ikisi de aynı `Accordion`'u kullanır.

**Kapsam uyarısı:** `Accordion` bu turda **yalnız iki ekranda** kullanılır
(E-27, E-10). v4'te PASS almış diğer ekranlar kart yapısında kalır; "her
uzun ekranı akordiyona çevirme" işi ayrı bir tur ve ayrı bir denetimdir.

---

## 11. REV2-r1 — kapanan bulgular

`design-reviewer` 1. tur: **REVİZE** · 6 bloklayıcı + 8 önemli + 6 küçük.
Aşağıdaki tablo her maddenin ne olduğunu ve nereye yazıldığını söyler;
prototip her satır için yeniden üretildi (`denetim.py`: **0 bulgu**).

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **B1** | Taşma yayının anlamı tek formüle bağlandı: `dolgu = max(0, hesaplanan_tasarruf)/harcanabilir` · `tasma = min(1, abs(min(0, hesaplanan_tasarruf))/harcanabilir)`. Bütçe dışı ayda dolgu 0 → **ana yay ve topuz çizilmez**, oluk boş kalır, yalnız `grad.arc-over` konuşur | §3.2 (dolgu/taşma satırları + `overflow` durumu + gerekçe paragrafı) · §5 `LimitGauge` · §7/3 · `lib.py: hero_yay()` · prototip **F2** |
| **B2** | `well` zemininde `text-3` (4.50) kaldırıldı: sheet'in "İsteğe bağlı" placeholder'ı ve hatalı durumdaki pasif tutar **`text-2`** (5.13). `text-3` bu iki ekranda artık hiç kullanılmıyor | §3.7 (kuyu paragrafı) · §9/10 · `uret.py: sheet()` · prototip **F6/F7/F7B** |
| **B3** | Kategori satırları arası **16 → 12**; §2.1'in 16 satırından "kategori satırları arası" ibaresi kaldırıldı ve 16 "yalnız iç boşluk"a indirildi | §2.1 · §3.8 · `uret.py: kategori_karti()` |
| **B4** | `Gerçek birikim` tutarı `display` 32 → **`amount` 17**; kartın ağırlığını 12pt hedef çubuğu taşıyor. Ekranda tek `display`/`hero` sayı kaldı (göstergenin ortası). Token değiştirilmedi | §2.2 (+ "tek kahraman kuralı") · §3.5 · `uret.py: birikim_karti()` |
| **B5** | Geçmiş ay seçiliyken metinler ay adıyla yazılıyor: başlık "Ayın bütçesi", "Ağustos'ta kayıt yok", "Ağustos'ta harcaman bütçenin 2.150 ₺ üzerinde.", "Ağustos'ta vazgeçtiğin rutin yok." İki varyant `metinler.md` §28.1'e girdi | §3.2 (ay adı kuralı) · §3.4 · §3.5 · §3.10 · `metinler.md` §28.1 · prototip **F2** yeniden çizildi |
| **B6** | §10 kapsam cümleleriyle yeniden yazıldı: `card.padding` 24→16 **global** · `content.gap` 24→0 **yalnız E-27/E-28** (`contentGap` prop'u) · `LoadState → Skeleton` **yalnız iskeleti çizilmiş ekranlar**, `LoadState` kaldırılmıyor. §8/6-7-8'e de kapsam yazıldı | §10.1 (yeni tablo) · §8/6 · §8/7 · §8/8 |
| **Ö7** | Profil kimlik kartı **kahraman panele** çevrildi: `primary-soft` · radius 32 · `clay.raised-lg` (dört durumun dördünde de). §8/2 arkitipe göre yeniden yazıldı ve ölçüldü: kahraman ekranı %43,6 brüt / %27 net · gezinme ekranı **%13,1** (hedef ≥%12). *(Bu üç rakam 766'lık yanlış ilk kat penceresiyle ölçülmüştü; REV3-r1'de 693'e karşı yeniden ölçüldü → %48,7 brüt / **%30,4 net** · **%14,2** — bkz. §14/B1.)* Hedefin altında kalan %18-22 rakamı ✅ diye işaretlenmedi, ölçümle değiştirildi | §4.2 · §8/2 (ölçüm tablosu) · §7/8 · `uret.py: kimlik_paneli()` · prototip **F8-F11** |
| **Ö8** | Hareket satırının sol kabı `banknote` ikonundan **`.gun-kutu`**'ya (E-15 deseni) çevrildi; `banknote` tekrarı dörtten ikiye indi, yeni glif eklenmedi | §3.6 ("Sol sütun" satırı) · §5 `SavingsMovementRow` · `uret.py: hareket_satiri()` |
| **Ö9** | Sheet'in **düzenleme kipi** tanımlandı (başlık "Hareketi düzenle", `primary` "Kaydet" + `button.ghost` "Sil"); kaydırma kısayol olarak kaldı. Prototipe 12. çerçeve eklendi | §3.6 (Silme) · §3.7 ("İki kip, tek sheet") · `uret.py: sheet(duzenleme=True)` · prototip **F7B** |
| **Ö10** | Birikim hareketleri listesi **en çok 5 satır** + `button.ghost` "Tüm hareketler"; bölüm başlığının sağı toplamı söylüyor ("7 kayıt") | §3.6 (Liste uzunluğu) · `uret.py: HAREKETLER` · prototip **F1** |
| **Ö11** | Tamamlanan gün **çubuktan metne** indi: `caption` "Tamamlanan gün" + `micro` "22/30 gün". Ekranın tek mavi ilerleme çubuğu hedef çubuğu | §2.2 (`micro`) · §3.4 · `uret.py: gun_sayaci()` |
| **Ö12** | Boş durum kartındaki ikinci "Birikim hareketi ekle" düğmesi kaldırıldı (aynı eylem 200px yukarıda) | §3.6 (Boş durum) · `uret.py: birikim_bos()` |
| **Ö13** | "rutin 0 ₺" etiketi kaldırıldı; kalan etiketler rutin kartıyla **toplanıyor** (Kafe 760 + Market 480 = 1.240 ₺) ve Profil'deki rutin satırıyla aynı sayıyı veriyor | §3.8 (iki madde) · `uret.py: KATEGORILER` · prototip **F1/F2** |
| **Ö14** | Kahraman iskeletinde sayı ↔ etiket arası `h8` → **`h4`**, etiket bloğu 16 → **88×18** (gerçek satır yüksekliği). Birikim kartı iskeleti de yüklü düzenin birebir aynası | `uret.py: F4` · prototip **F4** |
| **Ö15** | Kip çipine rota verildi: `→ /ayarlar` (Plan ve profil), `accessibilityLabel="Kip: Tasarruf. Değiştirmek için ayarları aç"`. Rotasız kalsaydı `View` olacaktı | §3.2 (Kip çipi) · §7/9 |
| **K1** | Boş durum diski `clay.raised-lg` → **`clay.raised`** (içinde durduğu kart `raised-lg`) | §2.3 · `stil-rev2.css` §8 |
| **K2** | Alt bilgi ghost düğmeleri `padding: 0 12px` → **16** (tokens §7.1) | §4.4 · `uret.py: ALT_BILGI` |
| **K3** | Bütçe çipinin 40pt yüksekliği `hitSlop` ile 44'e tamamlanıyor | §3.2 (Bütçe çipi) |
| **K4** | `tokens.md` §2.3 "yay iç alanı 198px" → **156px**; §7.5'in ölçüm satırı gerçek `Montserrat-Bold` ilerleme genişlikleriyle düzeltildi. *(Bu turun sayıları r2'de H3 ile bir daha düzeltildi — aşağı bkz.)* | `tokens.md` §2.3 · §7.5 · §13.4 · §3.2 (ölçüm satırı) |
| **K5** | Kaydırma yönü **sağdan sola (trailing)**; `tokens.md` §7.3'ün "sağa kaydırma → Sil" satırı düzeltildi (soldan sağa = iOS sistem geri hareketi) | `tokens.md` §7.3 · §3.6 (Silme) · §6 |
| **K6** | `success` / `success-ink` karışıklığı giderildi: `success` grafik eşiğinin altında (kullanılamaz), `success-ink` metin olarak AA geçiyor (kullanılabilir, kullanılmadı — gerekçesi yazılı) | §3.5 · §7/5 |

**Kapanmayan bulgu yok.**

---

## 12. REV2-r2 — HANDOFF şartları ve PM eklemeleri

`design-reviewer` 2. tur: **PASS** · 3 handoff şartı (H1/H2/H3) + 1 PM eklemesi
+ 1 PM kararı. Beşi de kod yazılmadan kapatıldı; prototip yeniden üretildi
(`denetim.py`: **0 bulgu**).

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **H1** | Türkçe **bulunma hâli eki** kalıpta sabitlenemez: `{Ay}'ta` / `{Ay}'de` 12 ayın 8'inde yanlış üretiyordu ("Eylül'ta", "Ağustos'de"). §28.1'in başına **12 satırlık ek tablosu** girdi (`Ocak'ta … Aralık'ta`, ünlü uyumu + ünsüz benzeşmesi) ve ek gereken 9 anahtar `{AyLokatif}` yer tutucusuna geçti. Ek çalışma zamanında hesaplanmaz, tablodan okunur. `{Ay}` (eksiz) yalnız ek almayan yerlerde kaldı ("Eylül 2026", "1–30 Eylül"). §24'teki aynı hata (`gunsec.sinir.baslangic`) da düzeltildi — tek satır, aynı kusur | `metinler.md` §28.1 (ek tablosu + 9 anahtar) · §24 |
| **H2** | Düzenleme sheet'indeki `button.ghost` **"Sil"** düğmesi `padding: 0 16px` override'ını almamış, sınıf varsayılanı 24'e düşüyordu. Üreteçte düzeltildi (elle yama yok) ve yorum yazıldı: ghost'un yatay iç boşluğu tokens §7.1 gereği **istisnasız 16**. HTML'deki 13 ghost düğmenin tamamı artık 16 | `uret.py: sheet()` · prototip **F7B** |
| **H3** | Ölçüm tablosu `tabular-nums` ile çelişikti: `1.250 ₺` 158 ↔ `6.240 ₺` 177 yazıyordu, ama §2.3 parada tabular'ı **zorunlu** kılıyor — tabular akışta her rakam 700/1000 em, yani aynı hane sayısındaki iki tutar **eşit genişlikte**. Sayılar oransal genişlikle (`1` = 392) ölçülmüştü. Yeni set: `820 ₺` **139 ✅** · `1.250 ₺` = `6.240 ₺` **189 ❌** · `12.500 ₺` **226 ❌**. §7.5'e ölçümün **formülü** eklendi (tek kaynak; bir hane = +37,2px) ki bir daha tahminle türetilmesin. Denetçinin ≈177/≈213 tahmini de `6.240` = 177'yi doğru sayıyordu; o da oransaldı — fark ve gerekçesi §13.4'e not olarak yazıldı. **Kuralın sonucu değişmedi:** 4+ hane daima `display` 32 | `tokens.md` §7.5 (+ yöntem satırı) · §2.3 · §13.4 (+ not) · bu belge §3.2 · `uret.py: gosterge_dolu()` docstring + F1 açıklaması |
| **PM/1** | **"bütçe dışı"** terimi `metinler.md` §0.1 sözlüğüne girdi (PM onayladı). Tanım *limit dışı*'ndan açıkça ayrıldı: *limit dışı* **günlük limite**, *bütçe dışı* **ay bütçesine** bağlıdır; bir gün limit dışı olup ay bütçe içinde kalabilir, tersi de olur. Görsel dil ikisinde de aynı (`warning-ink` / `warning-soft`), sözcük farklı | `metinler.md` §0.1 · bu belge §7/1 |
| **PM/2 · Ö7 takviyesi** | Profil kimlik paneli **bir adet `clay.sunken` olgu şeridiyle** takviye edildi (e-postanın altında): `label` "12 gündür kayıt giriyorsun" + `caption` "En uzun 21 gün." Panel **80 → 156pt**, ilk kattaki `primary-soft` yüzey **%13,1 → %21,9** (ölçüm yığını §8/2'de yazılı; REV3-r1'de doğru pencereye çekildi → **%14,2 → %23,5**). Üç kısıt tutuldu: kahraman sayı üretilmedi (roller `label`/`caption`, Tasarruf'un tek kahramanı bozulmadı), yeni veri alanı/API istenmedi (şerit **Seri** ayar satırının değerini gösterir), yeni token/renk/ikon açılmadı (`.serit` geometrisi + v4'ün `.clay-kuyu` zemini + `trending-up`). Şeridin dört durumdaki davranışı ve **veri yokken** ne yazacağı tabloya girdi; `signed-out` ve `error`'da şerit **çizilmez** (panelin tek mesajı bölünmez), `skeleton`'da yeri korunur, seri 0 iken **tanım** yazılır. Reddedilen alternatif (ayar satırlarını renklendirmek) hâlâ reddedilmiştir | §4.2 · **§4.2.1 (yeni)** · §5 (`FactStrip`) · §6 · §7/8 · §7/11 · §8/2 · `metinler.md` §28.2 · `uret.py: olgu_serit()` · prototip **F8 / F11** |

**Açık kalan tek şey:** Ö7 takviyesinin şerit metni ekran okuyucuda panel
etiketine karışıyor ve aynı olgu **Seri** satırında ikinci kez duyuluyor.
Bilinçli kabul edildi, gerekçe ve reddedilen iki alternatif §7/11'de yazılı.

---

## 13. REV3 — kapanan maddeler

Mustafa'nın 2026-09-26 direktifi iki işe bölündü: **(1)** günlük rutinlerin
Günlük ekranına taşınması → `rev3-gunluk-rutin.md` (kendi tablosu o belgenin
§13'ünde), **(2)** Tasarruf ekranının akordiyona çevrilmesi → aşağıdaki
tablo. Prototip iki dosya için de **üreteçten** yeniden üretildi (elle yama
yok); `denetim.py`: **0 bulgu**.

| Kod | Direktif / gereklilik | Ne yapıldı | Nerede |
|---|---|---|---|
| **R1** | "İlk soru ve cevabı direkt açık olsun" | **A · Bu ayın bütçesi** açık gelir; kahraman sayının "nereden çıktığı" ilk katta tamamlanır. Reddedilen alternatif (B'yi açmak) ve gerekçesi yazılı | §3.12.2 · prototip **F1** |
| **R2** | "Diğer sorular dropdown container'ı içinde" | B · C · D katlanmış; tek `Accordion` bileşeni, tek glif 180° dönüyor, 200ms yükseklik animasyonu (RN'de inşa edilebilir) | §3.12.3 · `stil-rev2.css` §9 |
| **R3** | Kapalı bölüm boş başlık olmayacak | Dört bölümün dördü kapalıyken **özet değer** taşıyor; özetler dolu/bütçe dışı/veri yok/yükleniyor/kısmi hata için tek tek yazılı | §3.12.4 |
| **R4** | "Şık" = bilgi yoğunluğunu düşürmek | Altı kart → **dört bölüm** (B ile hareketler birleşti) · "1–30 Eylül" satırı silindi · motivasyon şeridi ekranın ortasından B'ye indi · D'deki üç `repeat` ikon kabı düştü. İlk katın toplamı **688px** (B1'de yeniden ölçüldü), tek net mesaj | §1.2 · §3.4 · §3.9 · §3.12.1 |
| **R5** | Akordiyon durumları (açık · kapalı · animasyon · yükleniyor · hata · veri yok) | Durum tablosu + ekran düzeyi matrise **kısmi hata** satırı eklendi; üç yeni prototip çerçevesi | §3.12.5 · §3.10 · prototip **F12/F13/F14** |
| **R6** | Tek kahraman sayısı kuralı bozulmayacak | Akordiyonun içindeki en büyük tipografi `amount` 17; başlıklar `h2` (rakam taşımaz), özetler `label`. Ekranda tek `hero`/`display` sayı göstergededir | §3.12.6 · `denetim.py` "birden fazla 56pt" kuralı: 0 bulgu |
| **R7** | Rutin tasarrufu kaybolmayacak | **D bölümü kaldı** (kapalıyken 76pt, özet "1.240 ₺ · 3 rutin"); gerekçe ve kaybolma riski yazılı. Günlük hızlı eylemi buradan kalktı | §3.9 · §7/R-d · `rev3-gunluk-rutin.md` §1 |
| **R8** | Üç tasarruf kavramı karışmayacak | A (hesaplanan) · B (gerçek birikim) · D (rutin) üç ayrı katlanır kutu; hiçbir yerde toplanmıyor, D'nin ilk satırında "Bütçedeki kalana eklenmez." | §1.2 |
| **R9** | RN'de inşa edilebilirlik | `LayoutAnimation`/Reanimated `Layout`, mount/unmount, `transform rotate`, `accessibilityState={{expanded}}`; `display:none` · CSS transition · grid · `::before` kullanılmadı. Prototip taraması 0 bulgu | §3.12.3 · `agency/reference/rn-tasarim-kisitlari.md` |
| **R10** | Ölçülebilirlik | İlk kat yığını piksel piksel yazıldı (74+368+8+238 = **688**) ve kesmenin (687-693) A'nın altındaki **8pt boşluğa** düştüğü gösterildi: B ilk katta hiç görünmüyor, hiçbir nesne ortasından kesilmiyor. *(r0 bu satırda 708 ve "B'nin başlığı 733,5-758,5'te" yazıyordu — yanlış viewport, B1'de düzeltildi.)* | §3.12.1 |

**Kapanmayan madde yok.** PM kararı bekleyen tek nokta §7/R-d (rutin
tasarrufu bölümünün tamamen kaldırılması istenirse tutarın yeni yeri).

---

## 14. REV3-r1 — kapanan bulgular (`design-reviewer` 2. tur)

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **B1** (ana gövde) | İlk kat **ölçüldü, varsayılmadı**: yüzen sekme çubuğu kaydırma alanının dışında → `844 − 47 − 28 − 76` = **693** (gerçek cihazda **687**). Belge **687-693 bandını** kullanıyor. Kahraman kart 364 → **368** (cümlenin satır yüksekliği), A ile arası 24 → **8** → kesme **A'nın altındaki 8pt boşluğa** düşüyor; B ilk katta görünmüyor | §3.12.1 (tek kaynak) · prototip **F1/F4/F12/F13/F14** yeniden üretildi |
| **B1** (artık 1) | §8/2 hâlâ `766`/`298.740 px²` ile hesap yapıyordu. **Profil de sekmeli bir ekran**, ilk katı da 693'tür: tüm aritmetik yeniden yapıldı. Aksan **%21,9 → %23,5** (pencere küçüldü, panel aynı kaldı → oran **yükseldi**); ilk katta 5 değil **4 ayar satırı tam** görünüyor, kesme 5'incinin üst iç boşluğuna düşüyor. r1 karşılaştırması da aynı pencereye çekildi (%13,1 → **%14,2**) | §8/2 |
| **B1** (artık 2) | Ölçme **yöntemi tekleştirildi**: iki arkitip de **net** alanla ölçülüyor (r0 kahramanı brütle, gezinmeyi yüzey toplamıyla ölçüyordu). Kahraman: brüt %48,7 / **net %30,4** — band (%25-45) net ölçüde sağlanıyor, gevşetilmedi | §8/2 · §11 |
| **B1** (artık 3) | §13'ün R4 ve R10 satırları `708`/"B'nin başlığı 733,5-758,5'te" diyordu → **688** ve "kesme 8pt boşlukta" | §13/R4 · §13/R10 |
| **Ö4** | Hatalı bölüm kapatılırsa özetin "Açılamadı" olarak kaldığı yazıldı — üç hâlli tablo (varsayılan açık / kapalı / yeniden açılan). Hata hâli "açıkken özet çizilmez" kuralının **istisnası değil**, normal çıktısıdır; tek istisna geçmiş gün kapsamıdır. F14 not kutusu bununla aynı şeyi söylüyor | §3.12.5 · prototip **F14** |
| **öneri** | Akordiyon hafızasının **bileşende değil ekran sahibinde** olduğu yazıldı: Günlük cihazda kalıcı (`AsyncStorage`), Tasarruf çıkışta `{butce: true}` varsayılanına döner; `Accordion` bu farkı bilmez | §10.2 |
| **öneri** | Açık akordiyonun **basılı** hâli için çerçeve — zaten vardı ve korundu (F13'te "Kategori dağılımı" açık + başlığı basılı; kap çöker, ok dönmüş kalır) | prototip **F13** |

> **`:615`'e dokunulmadı.** Oradaki `766` tarihsel açıklamadır (r0'ın yanlış
> değerini anlatıyor) ve B1'in ne olduğunu okunur kılıyor.

---

## 14.1 REV3-r2 — PASS sonrası kapatılan iki metin artığı

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **Ö-A** (B1'in son artığı) | Prototipin **F8 not kutusu** hâlâ r0'ın 766'lık penceresiyle hesaplanmış **"%13,1 → %21,9"** diyordu. Bu kutu Mustafa'nın tarayıcıda okuduğu yüzeydir — yani yanlış sayıyı doğrudan o görüyordu. Belgenin doğru değerlerine çekildi: **%14,2 → %23,5** (§8/2 ve §14/B1 ile birebir). `tasarruf-profil.html` yeniden üretildi; prototipte artık hiçbir yerde `21,9` geçmiyor | `uret.py: E-28 F8 açıklaması` · prototip **F8** |
| **Ö-B** (tek kaynak kendiyle çelişiyordu) | §3.12.1 "A'nın alt kenarı kesmenin **en az 1px, en çok 7px** üstündedir" diyordu; aynı tablodaki ölçüler A'yı **688**'de bitirip bandı **687-693** veriyor. Doğrusu yazıldı: **en çok 5px üstünde** (693'lük cihaz), **687'lik cihazda son 1px kesmenin altında** — kesilen şey A'nın 16pt alt iç boşluğunun son pikseli, içerik değil. K-057/8 hâlâ sağlanıyor (ölçü değişmedi, cümle tabloya uyduruldu) | §3.12.1 |
