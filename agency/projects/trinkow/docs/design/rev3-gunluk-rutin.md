# Trinkow REV3 — **E-10 Günlük · rutin hızlı eylem satırı** tasarım deltası

> **Durum:** REV3-r0 — `design-reviewer` denetimi bekliyor · 2026-09-26 ·
> `ui-ux-designer`
>
> **Kapsam:** Günlük ekranına (`../mobile/src/components/pano/GunlukSayfa.tsx`)
> kategori kartının **altına** inen açılır rutin bölümü. Kategori kartının
> kendisi (`CategoryQuickAddCard`), kahraman gösterge, gün sayfalaması ve
> alt liste **bu belgenin dışındadır ve değişmedi.**
>
> **Bu belgede üretilmeyenler:** yeni renk, yeni punto, yeni radius, yeni
> boşluk değeri, yeni font, **yeni ikon glifi**, yeni kütüphane, yeni veri
> alanı, yeni API uç noktası.
>
> **Otorite:** görsel → `projects/trinkow/docs/brand/tokens.md` v4 (claymorphism) ·
> ton/metin → `projects/trinkow/docs/brand/brandbook.md` §2 ·
> ikon → `projects/trinkow/docs/design/varliklar.md` (kilitli set) ·
> bileşen → `projects/trinkow/docs/design/bilesen-envanteri.md` v4 ·
> RN kısıtları → `reference/rn-tasarim-kisitlari.md` ·
> veri → `projects/trinkow/docs/design/trinkow-rev-api.md`.
>
> **Prototip:** `projects/trinkow/docs/design/prototip-rev2/gunluk-rutin.html`
> (tarayıcıda aç · **7 durum** · 390×844) ·
> üretici: `prototip-rev2/_uret/uret_gunluk_rutin.py` ·
> delta stil: `prototip-rev2/stil-rev2.css` §11-§12 ·
> mekanik denetim: `prototip-rev2/_uret/denetim.py` (son koşu: **0 bulgu**)
>
> **Kardeş belge:** `rev2-tasarruf-profil.md` §3.12 (Tasarruf akordiyonu) —
> iki iş aynı turda yapıldı ve **aynı açılır bileşeni** paylaşıyor.

---

## 0. Direktif ve teşhis

Mustafa (2026-09-26):

> *"Tasarruf sayfasına ayrı bir sayfa yaparak rutinlerim kısmı yapmışsın.
> Buna gerek [yok]; kullanıcının eklediği günlük rutinler Günlük sayfasında
> dropdownlı şekilde kategorilerin altında yer alsın. Kullanıcı hızlı
> şekilde burdan rutin harcama girebilsin veya bugün bu rutin harcamayı
> yapmadığını işaretleyebilsin. Rutinin de tüm bilgileri görünmesine gerek
> yok: rutinin adı, mali değeri, bugün alındığını göstermek için 'artı
> iconu', alınmadığını belirtmek için başka bir icon olabilir."*

**Bugün sorun ne?** Günlük eylem (`bugün aldım / almadım`) yönetim
ekranının (`../mobile/app/rutinler.tsx`) içine gömülü. O ekranda her rutin bir
kart ve kartın içinde **beş düğme + bir metin alanı** var: "+ Harcama
ekle", "Bugün vazgeçtiğim adet" girişi, "Bugün almadım", "Bugünkü
vazgeçişi geri al", "Düzenle", "Rutini kaldır". Yani günde iki saniye
sürmesi gereken bir işaretleme, ayrı bir ekrana gidip yönetim
kontrollerinin arasından doğru düğmeyi bulmayı gerektiriyor. Günlük
ritimli bir ürün için bu, **işin yapılmayacağı** anlamına gelir.

**Bu deltanın tek cümlesi:** *günlük eylem Günlük'e taşınır, yönetim
`/rutinler`de kalır.*

---

## 1. Ne taşınıyor, ne taşınmıyor (kapsam çizgisi)

| İş | Nerede | Gerekçe |
|---|---|---|
| "Bugün aldım" (harcama yaz) | **Günlük · rutin satırı** (yeni) | Günde 1-3 kez, düşünmeden yapılan iş |
| "Bugün almadım" (vazgeçme işaretle) | **Günlük · rutin satırı** (yeni) | Aynı ritim, aynı satır |
| İşareti geri al | **Günlük · rutin satırı** + 6 sn toast | Yanlış dokunuş kaçınılmaz (§5/4) |
| Rutin ekle · düzenle · kaldır · adet/fiyat | `/rutinler` — **değişmedi** | Ayda bir yapılan kurulum işi. PM kararı: yönetim orada kalıyor |
| Rutin tasarrufu **toplamı** | `Tasarruf` → akordiyon bölümü D — **kaldı** | Rutin tasarrufu bir finansal bilgidir; tek toplandığı yer orasıdır (bkz. `rev2-tasarruf-profil.md` §3.12) |
| Rutin sayısı + aylık tasarruf | `Profil` → "Rutinler" satırı — değişmedi | Yönetimin kapısı |

**Üç tasarruf kavramı karışmıyor.** Bu satır *rutin tasarrufu* üretir;
*hesaplanan tasarruf* ve *gerçek birikim* ile hiçbir yerde toplanmaz.
Satırdaki tek cümle bunu söylüyor: "Vazgeçtin · rutin tasarrufu".
Bütçedeki kalana eklenmediği cümlesi Tasarruf ekranının D bölümünde
(tek kaynak) durur; Günlük'te 12 kelimelik bir uyarı cümlesi tekrarlanmaz.

---

## 2. Yerleşim

### 2.1 Günlük ekranının okuma sırası (REV3)

| # | Blok | Değişti mi? |
|---|---|---|
| 1 | Başlık (tarih + "Bugün" + seri çipi + takvim) | hayır |
| 2 | Kahraman gösterge (bugün kalan) + gün okları | hayır |
| 3 | (koşullu) ipucu / seri / limit gözden geçirme şeritleri | hayır |
| 4 | **Kategoriler** kartı — 10 kategori satırı, her birinde `+` | hayır |
| 5 | **Rutinler** — açılır bölüm | **YENİ** |
| 6 | Planlı ödemeler (bugün) / gün kayıtları (geçmiş gün) | hayır |

> Not: kategori listesi **10** satırdır, 13 değil — sabit ödeme olan üç
> kategori (`fatura`, `kiraev`, `abonelik`) hızlı ekleme listesinde yoktur
> (`GUNLUK_HARCAMA_KATEGORILERI`). Bu, bölümün gerçek cihazda **ilk katın
> dışında** kaldığı anlamına gelir; prototip çerçeveleri bu yüzden ekranı
> kaydırılmış gösterir (§11/6).

**Neden kategorilerin hemen altı?** Rutin satırı da bir harcama girişi
yüzeyidir; kategori satırıyla **aynı işi** yapar, tek farkı tutarın
önceden bilinmesidir. Üstüne konsa (kahramanla kategori arasına) her gün
açılan ekranın omurgasını böler; alt listenin altına konsa günün sonunda
kalır ve hiç görülmez.

### 2.2 Ölçü temeli (yeni değer üretilmedi)

| Değer | Bu bölümdeki tek işi |
|---|---|
| **4** | Rutin adı ↔ durum satırı · eylem ikonu ↔ eylem etiketi |
| **8** | Ad ↔ tutar (yatay) · **kategori kartı ↔ rutin bölümü** |
| **12** | Rutin satırları arası · başlık ↔ ilk satır · metin kolonu ↔ eylemler · iki eylem arası |
| **16** | Yalnız iç boşluk (bölüm kabı) |
| **24** | Rutin bölümü ↔ alt liste (ekran düzeyinde iki bağımsız blok) |

> **§2.1 (rev2) eki — "8"in tanımı genişledi:** *aynı grubun satırları*
> yanına *aynı grubun kartları* eklendi. Kategori kartı ile rutin bölümü
> 24 ile ayrılsaydı ikisi ilgisiz iki ekran bloğu gibi okunurdu; oysa
> rutin bölümü direktifin sözüyle **"kategorilerin altında"** duran aynı
> grubun devamıdır. Aynı ek Tasarruf akordiyonunun bölümleri arasında da
> geçerli (`rev2-tasarruf-profil.md` §3.12).

| Radius | Gölge |
|---|---|
| Bölüm kabı 24 | `clay.raised` (basılı: `groove` + `clay.pressed`) |
| Eylem düğmesi 16 | işaretsiz `clay.sunken` · işaretli `clay.raised` · basılı `clay.pressed` |

Üç derinlik bu bölümde de tamam: kap **raised** · eylem kuyusu
**sunken** · işaretli eylem **raised**. Ekranın `raised-lg` katmanı
kahraman karttır (değişmedi).

### 2.3 Tipografi rolleri

| Rol | Nerede |
|---|---|
| `h2` 19 | "Rutinler" (bölüm başlığı) |
| `label` 13 | Başlığın sağındaki özet / gün etiketi |
| `body-strong` 16 | Rutin adı |
| `amount` 17 | Rutinin mali değeri (Montserrat + `tabular-nums`) |
| `caption` 13 | Durum satırı ("Yazıldı · 08.20" / "Vazgeçtin · rutin tasarrufu") |
| `micro` 12 | Eylem etiketleri ("Aldım" / "Almadım") |

**Kahraman sayı üretilmedi.** Bu bölümdeki en büyük tipografi `amount`
17'dir; Günlük'ün tek kahraman sayısı göstergenin ortasındaki "bugün
kalan"dır ve bozulmadı (§8/1 tek kahraman kuralı).

---

## 3. Bölüm — açılır kap (`Accordion`)

Tasarruf akordiyonuyla **aynı bileşen** (`.akordiyon` + `.akordiyon-bas`);
iki ekranda iki ayrı açılır kap dili kurulmadı.

```
┌ akordiyon (r24 · surface · clay.raised · iç boşluk 16) ────────────┐
│ ┌ başlık düğmesi · 358×min44 · dokunma hedefi ────────────────────┐ │
│ │ h2 "Rutinler"              label "3 rutin · 1 işaretsiz"  [20 v] │ │
│ └──────────────────────────────────────────────────────────────────┘ │
│                        ↕ 12  (yalnız açıkken)                        │
│ [rutin satırı]  ↕12  [rutin satırı]  ↕12  [rutin satırı]             │
│                        ↕ 12                                          │
│ [button.ghost "Tüm rutinler"]      ← yalnız 5'ten fazla rutinde      │
└──────────────────────────────────────────────────────────────────────┘
kapalı: 16 + 44 + 16 = 76      açık (3 satır): 16 + 44 + 12 + 162 + 16 = 250
```

| Konu | Karar |
|---|---|
| Dokunma hedefi | Başlık satırı, 358 × **≥44**. Kapalıyken kabın tamamı zaten başlıktır |
| Basılı geri bildirim | **Kabın tamamı** çöker (`groove` + `clay.pressed`); `scale` yok (tokens §8) |
| Ok | Tek glif `chevron-down`; açıkken **180° döner**. `chevron-up` kilitli sette yok ve üretilmedi. RN: `transform:[{rotate}]`, reduce-motion'da anında |
| Animasyon | Yükseklik 200ms `ease-out` (`LayoutAnimation` / Reanimated `Layout`). İçerik **mount/unmount** edilir (`display:none` RN'de yoktur). Reduce motion → 0ms |
| Kapalı özet | **Asla boş başlık yok.** Sağda `label`/`text-2` özet durur (§3.1) |
| Açık özet | Çizilmez — içerik aynı bilgiyi satır satır veriyor. **Tek istisna geçmiş gün:** gün etiketi açıkken de durur (§6) |
| Varsayılan | İlk kurulumda **açık** (kullanıcı rutinini görmeden bildiğini varsayamayız). Sonrasında kullanıcının son bıraktığı hâl hatırlanır (cihaz ayarı, gün başına değil) |
| Hatırlama | Aynı ayar tüm günlerde geçerli; gün sayfaları arasında kaydırırken bölüm açık/kapalı durumu değişmez (sayfa başına ayrı hafıza kullanıcıyı şaşırtır) |

### 3.1 Kapalı hâlin özeti — metin tablosu

| Koşul | Özet |
|---|---|
| En az bir rutin işaretsiz | "{n} rutin · {n} işaretsiz" |
| Hepsi işaretli | "{n} rutin · hepsi işaretli" |
| Hiçbiri işaretli değil | "{n} rutin · işaretlenmedi" |
| Yükleniyor (bölüm **kapalı**) | Özetin **yeri** korunur (104×18 çukur blok), başlık gerçek metin |
| Yükleniyor (bölüm **açık**) | Özetin yeri **korunmaz** — yüklü açık bölüm de özet taşımaz; placeholder konsa yükleme bitince başlık satırı zıplardı. Başlık ve ok gerçek, içerik iskelet |
| Yazma/okuma hatası | "{n} rutin · işaret bekliyor" + bölüm içinde şerit (§5/7) |

Özet **sayaç** taşır, tutar taşımaz: bölümün işi bugünün kararlarını
kapatmaktır, para toplamı değil (o toplam Tasarruf'ta yaşar). "1
işaretsiz" kullanıcının **yapacak işi** olduğunu söyleyen tek bilgidir.

---

## 4. Rutin satırı

```
┌ satır (flat · 358−32 = 326 genişlik · yükseklik 46) ───────────────────┐
│ body-strong "Kahve"                  amount "31 ₺"  │12│[+ ]│12│[⃠ ]  │
│ caption "Yazıldı · 08.20"            (yalnız işaretliyken)             │
└────────────────────────────────────────────────────────────────────────┘
  metin kolonu 174 = 326 − 12 − 64 − 12 − 64
```

| Alan | Kaynak | Kural |
|---|---|---|
| Ad | `rutinler[].ad` | `numberOfLines={1}`, sonu kırpılır |
| Mali değer | `gunluk_adet × birim_fiyat_kurus` | **Günlük** değer (satırın kapsamı bir gündür). `amount` 17, kuruş yok, **asla kırpılmaz** |
| Durum satırı | işarete göre | Yalnız işaretli durumlarda çizilir; işaretsiz satır tek satırdır ve dikeyde ortalanır. Satır yüksekliği **değişmez** (düğmeler 44, metin kolonu 46) |
| Kategori · günlük adet · geçmiş | — | **GÖRÜNMEZ** (direktif). Bu bilgiler `/rutinler`de |
| Satır gövdesi | — | **Dokunulamaz.** Dokunulup hiçbir şey yapmayan yüzey bırakılmaz; satırın işi iki eylemdir |

**Günlük adedi 1'den büyük rutin nasıl okunuyor — Ö3.** `gunluk_adet = 2`
olan 31 ₺'lik bir kahve satırda **62 ₺** yazar; "×2" satırda **görünmez**.
Kural: **satır günün tamamını işaretler.** "Aldım" günün beklenen adedini
yazar (`adet = gunluk_adet`), "Almadım" da günün tamamı için vazgeçme
işaretler (`adet = beklenen`). Satırın bu hâlde okunuşu: *"Kahve · 62 ₺ ·
Yazıldı · 08.20"* — yani "bugünün kahvesi kapandı".

| Soru | Cevap |
|---|---|
| Kısmi işaret (iki kahveden birini aldım) | Bu satırdan **yapılamaz**; iki eylem de gün bazlıdır, ara değer girilecek alan yoktur |
| Kısmi işaret nereden yapılır | `/rutinler` → rutinin kendi ekranı (adet girişi orada yaşıyor). Alternatif: kategori satırından tek seferlik harcama yazmak |
| Kullanıcı 62 ₺'nin nereden geldiğini nereden doğrular | `/rutinler`: liste birim fiyatı ve günlük adedi yan yana gösterir ("31 ₺ × 2"). Günlük ekranı doğrulama yeri değil, **karar** yeridir |
| Bu bilgi saklamak mı | Hayır, **yer değiştirmek**. Satırda "31 ₺ × 2 = 62 ₺" yazmak üç sayıyı yan yana koyar ve satırı hesap makinesine çevirir; kullanıcı bugün o rutini alıp almadığına karar verecek, çarpımı denetlemeyecek |

Sonuç: `gunluk_adet` satırın **tutarına** girer, **metnine** girmez. Bu, §4
tablosundaki "Kategori · günlük adet · geçmiş GÖRÜNMEZ" satırının aritmetik
karşılığıdır. Prototipte çizili: G3'ün ilk satırı (`Kahve · 62 ₺ · Yazıldı`).

**Satırda ikon kabı yok.** Kategori satırının solunda 44pt renkli kategori
kabı vardır çünkü orada ayırt edilecek 10 kategori var. Rutin satırında
ayırt edilecek şey rutinin **adıdır**; üç satırın soluna aynı `repeat`
glifini koymak hiçbir şeyi ayırmaz, yalnız 56px çalar (Ö8'in gerekçesiyle
aynı). Ad, satırın sol hizasında ilk okunan şey olur.

### 4.1 İki eylem

| Eylem | Glif | Etiket | Yüzey (işaretsiz) | Ne yapar |
|---|---|---|---|---|
| Bugün aldım | **`plus`** | "Aldım" | `well` + `clay.sunken` | Rutinin günlük değeriyle harcama yazar (`rutin_id` + `adet`) |
| Bugün almadım | **`circle-slash`** | "Almadım" | `well` + `clay.sunken` | O gün için vazgeçme işaretler (`…/vazgecme`, `adet = beklenen`) |

**İkinci ikon neden `circle-slash`?** Kilitli sette zaten var
(`varliklar.md` §1.2c — "Limiti kaldır", E-17) ve uygulamada
`Icon.tsx`'te `limit-kaldir` adıyla **halihazırda gömülü**: yeni glif
eklenmedi. Anlamı iki bağlamda da aynı: *bu yok / bunu iptal ettim.*
Değerlendirilip **reddedilenler:** `x` (BottomSheet'in "Kapat" glifi —
aynı ekranda iki anlam), `check` ("Seçili" için ayrıldı ve "aldım"
ile karışır), `trash-2` (silme; vazgeçmek bir silme değil),
`triangle-alert` (marka uyarı ikonu kullanmaz, `varliklar.md` §1.3).

**Ayrım renkte değil.** İki düğme işaretsiz hâlde **aynı** yüzeydir; onları
ayıran şey **glif + görünür etiket**tir (WCAG 1.4.1). Renk yalnız
*işaretli/işaretsiz* durumunu güçlendirir, hangi eylem olduğunu söylemez.

**İşaretli hâl:** düz `primary-deep` zemin + beyaz glif ve etiket
(**5.37:1** ✅ — K-062), `clay.raised`. Gradyan yok. Bu, v4'ün aynı
soruya verdiği cevabın birebir tekrarı: `.durak.gecildi`,
`.gun-kutu.altinda`, `.onay-kutu.isaretli`.

**Kazara dokunma nasıl düşürüldü (dört katman):**
1. Her hedef **64×44**; aralarında **12pt** boşluk (yatayda yan yana iki
   hedef arasındaki en dar ölçü budur, `hitSlop` ile şişirilmez —
   şişirilse hedefler birbirine girerdi).
2. Etiket görünür: dokunmadan önce hangisi olduğu okunur.
3. Her iki eylem de **geri alınabilir** ve geri alma **6 sn** ekranda
   durur (K-029 deseni, `undoInfo` varyantı — silme kırmızısı yok).
4. Dokunuş **sessiz kalmaz**: satır anında durum satırı kazanır ve düğme
   işaretliye geçer. Yanlış dokunuş görünür, dolayısıyla düzeltilebilir.

---

## 5. Durum matrisi (zorunlu on durum)

| # | Durum | Görünüm | Metin |
|---|---|---|---|
| 1 | **Rutin yok** | **Bölüm hiç çizilmez** (başlık da yok). Günlük en çok açılan ekrandır; kurulmamış bir özelliğin boş kutusu burada yer tutmaz. İlk rutin eklendiği an bölüm görünür | — (boş durum metni üretilmedi) |
| 2 | **İşaretsiz** | İki düğme `well` + `sunken`; durum satırı yok, satır tek satır | — |
| 3 | **Aldım** | "Aldım" işaretli (`primary-deep`) · "Almadım" **pasif** (`disabled-bg` + `text-2` + `sunken`, **opaklık yok**) · durum satırı | "Yazıldı · {saat}" |
| 4 | **Almadım** | "Almadım" işaretli · "Aldım" **etkin kalır** (kullanıcı fikrini değiştirip alabilir) · durum satırı | "Vazgeçtin · rutin tasarrufu" |
| 5 | **Geri alma** | 6 sn toast: 8pt `primary` nokta + metin + `ghost` "Geri al". Süre sonrası yol: "Almadım" işaretine tekrar dokunmak vazgeçmeyi kaldırır (`adet: 0`); "Aldım"ın kaydı ise gün listesinden/kategori satırından silinir | "{ad} {tutar} yazıldı." · "{ad} almadın olarak işaretlendi." |
| 6 | **Yazılıyor** | Dokunulan düğme **iyimser** olarak işaretliye geçer, glifin yerini 20pt `spinner` alır; etiket ve genişlik sabit. Her iki düğme o an `disabled` | — |
| 7 | **Ağ hatası** | İyimser güncelleme geri alınır, satır eski hâline döner; hata **bölümün içinde** tek satır `serit-warn` (`wifi-off`) olur. Ekranın kalanı çalışır | "İşaret kaydedilemedi. Yeniden dene." |
| 8 | **Yükleniyor** | ≥150ms okumada iskelet: başlık ve ok **gerçek**, iki satır iskeleti (metin blokları + 64×44 çukur bloklar). Özetin yeri **yalnız kapalı bölümde** 104×18 blokla korunur (§3.1) — açık iskelette korunmaz, yoksa yükleme bitince başlık zıplar. Shimmer yok. Etiket: "Rutinler. Yükleniyor" | — |
| 9 | **Çok rutin** | Açık listede **en çok 5 satır**; hangi 5'in çizileceğini seçmek için sıralama: işaretsizler önce, sonra mali değeri büyük olan (§5 altındaki **sıralama kuralı** bağlayıcıdır). Altında `ghost` "Tüm rutinler" → `/rutinler`. Özet toplamı söyler ("6 rutin · 4 işaretsiz"), yani sınır bilgi kaybı değil | "Tüm rutinler" |
| 10 | **Uzun ad** | Ad tek satırda kırpılır (`ellipsizeMode="tail"`); **tutar asla kırpılmaz**, düğmeler küçülmez. Test dizesi prototipte çizili: "Öğle yemeği yerine evden getirdiğim kumanya" | — |

**Sıralama kuralı — B4 (bağlayıcı).** Sıralama **yalnız mount'ta** bir kez
çalışır ve **yalnız 5'ten fazla rutin varken** hangi 5 satırın çizileceğini
seçmek için vardır. Bir kez çizilen sıra o oturumda **donar**:

| Durum | Ne olur |
|---|---|
| Ekran açılır (≤5 rutin) | Sıralama **hiç çalışmaz**; rutinler `/rutinler`deki kullanıcı sırasıyla çizilir. Kullanıcının kendi kurduğu düzeni bozmanın faydası yok |
| Ekran açılır (>5 rutin) | Sıralama bir kez çalışır: işaretsizler önce, eşitlikte mali değeri büyük olan önce. İlk 5 çizilir, kalanı "Tüm rutinler"in arkasında |
| Kullanıcı bir satırı işaretler | **Satır yerinde kalır.** Yeniden sıralama YOK, listeden düşme YOK. Satır yalnız durum satırı kazanır, düğmesi işaretliye geçer |
| Kullanıcı "Geri al"a basar | Satır yine yerinde; sıra değişmez |
| Ekran yeniden açılır / gün değişir | Sıralama tekrar çalışır (yeni mount) |

Gerekçe: işaretlemeden sonra sıralamak **parmağın altındaki satırı listenin
sonuna zıplatır** — kullanıcı ikinci rutini işaretlemek için onu gözüyle
yeniden bulmak zorunda kalır, üçüncü dokunuş yanlış satıra gider. Bugünün
işini kapatma akışında liste **sabit bir hedef** olmalı. Bedeli şudur: ilk
5'in seçimi işaretleme sırasında güncellenmez, yani 6 rutinli kullanıcı
dördünü işaretlediğinde gizli 6'ncı rutin öne çıkmaz. Kabul edildi — o
kullanıcının yolu "Tüm rutinler" düğmesi ve özet ("6 rutin · 2 işaretsiz")
ona işinin bitmediğini zaten söylüyor. Prototipte G1 ve G3 bu kurala göre
çizildi: G1'in sırası 60 · 31 · 28 ve işaretli "Kahve" **ortada kalıyor**.

**Neden "Almadım" pasifleşiyor, "Aldım" pasifleşmiyor?** Veri
sözleşmesi bunu zorunlu kılıyor: vazgeçme adedi *beklenen adet − o güne
bağlı alımlar*'dan büyük olamaz, yani rutin alındıysa vazgeçme sıfırdır.
Tersi doğru değil: vazgeçmiş olsan da sonra alabilirsin. İki düğmenin
davranışı simetrik değildir **çünkü altındaki iki nesne simetrik
değildir**: harcama bir *kayıttır* (çok olabilir), vazgeçme bir gün
başına *işarettir*.

**Pasif durumda ne yapılacağı söyleniyor mu?** Evet, satırın durum
satırında: "Yazıldı · 08.20". Kullanıcı kaydı iptal etmek isterse kayıt
zaten gün listesinde duruyor ve oradan silinebilir; pasif düğmenin
yanına ikinci bir açıklama cümlesi konmaz (brandbook §2.2/10).

---

## 6. Geçmiş güne bakarken — net karar

**Karar: bölüm geçmiş günde de görünür ve eylemler çalışır.**

| Gün | Davranış |
|---|---|
| Bugün | Bölüm görünür, eylemler etkin, başlığın sağı özet taşır (açıkken boş) |
| **Geçmiş takipli gün** | Bölüm görünür, **eylemler etkin**; başlığın sağında **gün** durur ("16 Eylül") — bölüm **açıkken bile**. Etiketler gün-nötrdür: "Aldım" / "Almadım" ("Bugün aldım" yazılmaz) |
| Takip başlangıcından önce | Bölüm **çizilmez** (o günler takip edilmiyor) |
| Gelecek gün | Yok — Günlük ileri sayfalanamaz |

**Gerekçe:** veri sözleşmesi vazgeçmeyi "bugün ve geçmiş takipli günler"
için açıyor; kullanıcı dün akşam işaretlemeyi unuttuysa bunu düzeltmenin
yolu olmalı. Bilgiyi kaybetmemek bu üründe temel kural
(`brandbook` §2.2/9). Tek risk **yanlış güne yazmaktır**; iki önlem
alındı: (a) etiketler gün taşımadığı için "bugün" yanılgısı üretmez,
(b) geçmiş günde **gün adı başlıkta kalıcıdır**, çünkü eylemin anlamı
güne bağlıdır — bu, "açıkken özet çizilmez" kuralının tek istisnasıdır ve
gerekçesi güvenliktir.

> **Kategori kartı neden geçmiş günde yok da rutin bölümü var?** Kategori
> kartı **aylık** limit taşır; geçmiş bir günün sayfasında bu ayın sayısını
> göstermek o güne ait olmayan bir bilgi olur (K-056). Rutin satırı ise
> yalnız ad + günlük değer taşır: hiçbir aylık/kümülatif sayı yok.
> Kartı gizleyen sebep bu satır için geçerli değil.

---

## 7. Yazma sırası ve veri sözleşmesi (UI'nin verdiği kararlar)

Yeni uç nokta ve yeni alan **istenmedi**; kullanılanlar
`trinkow-rev-api.md`'de zaten var.

| Eylem | Çağrı | UI kararı |
|---|---|---|
| Aldım | Harcama `POST` — `kategori = rutin.kategori`, `ad = rutin.ad`, `tutar = birim_fiyat`, `adet = gunluk_adet`, `rutin_id` | Form **açılmaz**: rutinin fiyatı ve adedi tanımlı olduğu için doldurulacak alan yok. Fiyat/adet o gün farklıysa kullanıcı kaydı gün listesinden düzeltir |
| Almadım | `PUT /butce/rutinler/{id}/vazgecme` — `{gun, adet: beklenen}` | Tek dokunuş **tüm günün** rutinini işaretler |
| Geri al (almadım) | Aynı uç nokta, `adet: 0` | Sözleşme "sıfır, işareti kaldırır" diyor |
| Geri al (aldım) | Oluşan kaydın `DELETE`'i | 6 sn toast; sonrasında kayıt gün listesinden silinir |
| Aldım ⟵ almadım geçişi | Önce `adet: 0`, sonra harcama `POST` | **Aynı gün iki işaret birlikte durmaz.** Sunucu uzlaştırmasına güvenilmez; sıra UI'de sabittir |

**Kısmi adet (2 kahveden 1'i) bu satırda ele alınmaz.** Satırın kapsamı
"bugünün rutini"dir ve gösterdiği tutar günün tam değeridir. Kısmi durum
`/rutinler`deki adet alanıyla ya da kaydın kendisini düzenleyerek çözülür.
**PM kararı gerekebilir** (§11/3): günlük adedi 1'den büyük rutin
kullanımı yaygınsa bu satıra bir adet kontrolü değil, `/rutinler`e daha iyi
bir kısmi işaret akışı eklemek gerekir — satırın sadeliği direktifin
kendisidir, orayı kalabalıklaştırmak çözüm değil.

---

## 8. Erişilebilirlik

| Konu | Karar |
|---|---|
| Dokunma hedefi | Başlık 358×≥44 · her eylem 64×44. `hitSlop` kullanılmaz (hedefler yan yana) |
| Bölüm başlığı | `accessibilityRole="button"` + `accessibilityState={{expanded}}` · etiket "Rutinler. {özet}" |
| Eylem düğmesi | `accessibilityRole="button"` + `accessibilityState={{selected}}` · etiket "{ad} aldım olarak işaretle, {tutar}" / "{ad} almadım olarak işaretle, {tutar} rutin tasarrufu" |
| Geçmiş gün (**B3**) | Görünür etiketler gün-nötr kalır; günü **sesli katman taşır**: bölüm etiketi "Rutinler. {gün}. {özet}" (`a11y.gunlukRutin.bolumGecmis`), eylem etiketi "{ad}, {gün}. Aldım olarak işaretle, {tutar}" (`…aldimGecmis` / `…almadimGecmis`). **Karar: eylem etiketleri günü taşır** — ekran okuyucu kullanıcısı bölüm başlığını duymadan doğrudan bir düğmeye odaklanabildiği için kapsam düğmenin kendi etiketinde olmalı. Görsel etikete gün YAZILMAZ (64pt genişlik almaz, başlık zaten söylüyor) |
| Yükleniyor (**Ö5**) | Özet henüz yokken bölüm etiketi "Rutinler. " diye yarım kalmaz: **"Rutinler. Yükleniyor"** (`a11y.bolumYukleniyor` — E-27 akordiyonuyla paylaşılan anahtar). Görünür "Yükleniyor" yazısı yok; o yerde iskelet bloğu var |
| Pasif düğme | `accessibilityState={{disabled:true}}` — gizlenmez, düzen kaymaz |
| **Kilitli (yükleniyor) düğme** | RN'de `accessibilityState={{ selected, disabled }}` **birlikte** verilir. Görsel katmanda dokunulan düğme işaretli çizilir (B2); sesli katmanda da öyle duyulmalı — `disabled` tek başına verilirse iyimser işaret kaybolur ve ekran okuyucu kullanıcısı "dokunuşum işlendi mi?" sorusuyla kalır. *(Prototipte `aria-pressed`, `disabled` ile birlikte düşüyordu — HTML sınırı; RN'de düşmeyecek.)* |
| Durum değişimi | Toast `AccessibilityInfo.announceForAccessibility` ile duyurulur (mevcut `ToastHost` davranışı) |
| Hata şeridi | `accessibilityLiveRegion="polite"` |
| Renk | Hiçbir bilgi yalnız renkle taşınmaz: glif + etiket + durum satırı |
| Dinamik yazı | Ad kırpılır; eylem etiketi 12pt'den büyüdüğünde düğme **dikeyde** büyür, satır yüksekliği onunla artar (düğme genişliği sabit 64 kalır, iki hedef birbirine girmez) |
| Reduce motion | Açılış/kapanış 0ms; spinner dönmez, yerinde durur |

---

## 9. Bileşen envanteri deltası

| Bileşen | Tip | Karar |
|---|---|---|
| `Accordion` | **yeni** | Başlık düğmesi + özet + dönen `chevron-down` + katlanır içerik. Kap `surface`/r24/`clay.raised`, basılıda tüm kap çöker. **Tasarruf ekranıyla paylaşılır** (`rev2-tasarruf-profil.md` §3.12) |
| `RoutineQuickRow` | **yeni** | Ad + günlük değer + iki `RoutineActionButton`. Satır gövdesi dokunulamaz; durum satırı koşullu |
| `RoutineActionButton` | **yeni** | 64×44, r16, 20pt glif + 4 + 12pt etiket. Durumlar: idle / selected / pressed / selected+pressed / disabled / loading (spinner) |
| `InfoStrip` | mevcut | `warn` kipi bölüm içi hata şeridi olarak |
| `Skeleton` | mevcut | Bölüm iskeleti (E-27/E-28 ile aynı bileşen) |
| Toast (`undoInfo`) | mevcut | 6 sn "Geri al"; yeni varyant açılmadı |

---

## 10. Metin deltası (→ `metinler.md` §29)

| Bugün koddaki metin | Yeni | Gerekçe |
|---|---|---|
| "+ Harcama ekle" (rutin kartında) | **"Aldım"** | 1 kelime, fiil; satırda etiket olarak |
| "Bugün almadım" (düğme) | **"Almadım"** | Gün bilgisini başlık taşır; etiket gün-nötr olur (geçmiş günde de doğru) |
| "Bugün vazgeçtiğim adet" (metin alanı) | **kaldırıldı** | Satır bir günün tamamını işaretler; adet `/rutinler`de |
| "Bugünkü vazgeçişi geri al" (düğme) | **"Geri al"** (toast) + işarete tekrar dokunma | Ayrı bir düğme satırı üretmez |
| "Bugünkü vazgeçişin kaydedildi. Bu işlem birikim hesabına para eklemez." | **"{ad} almadın olarak işaretlendi."** | 4 kelime. Kavram ayrımı Tasarruf'taki tek cümlede söylenir, her toast'ta tekrarlanmaz |
| "Rutin değişiklikleri bugünden itibaren geçerlidir. Harcama girmemek otomatik tasarruf sayılmaz." | Günlük'te **yazılmaz** (yönetim ekranında kalır) | Günlük'te kural metni yok |
| — | **"Yazıldı · {saat}"** · **"Vazgeçtin · rutin tasarrufu"** | Durum satırı; övgü yok, ünlem yok |
| — | **"{n} rutin · {n} işaretsiz"** | Kapalı özet (§3.1) |
| — | **"İşaret kaydedilemedi. Yeniden dene."** | Ne olduğunu değil ne yapacağını söyler (§2.8) |

---

## 11. Bilinçli kararlar — `design-reviewer`'ın bilmesi gerekenler

1. **"Aldım" tek dokunuşla yazar, form açmaz.** Kategori satırının `+`'sı
   formu açar (tutar bilinmiyor), rutin satırının `+`'sı yazar (tutar
   biliniyor). Aynı glif iki farklı davranış: bu yüzden rutin eylemi
   **çıplak `+` dairesi değil, etiketli düğmedir** (`.ekle-btn` kullanılmadı).
   Ayrım görünür etiketle kurulur.
2. **Satır gövdesi dokunulamaz.** Kayda gitmek için ikinci bir yol
   (chevron) eklenmedi; kayıt zaten gün listesinde duruyor. Alternatif
   (satır → kayıt detayı) reddedildi: satırda üç dokunma hedefi olurdu.
3. **Kısmi adet ele alınmadı** (§7). PM kararı adayı.
4. **Rutin yoksa bölüm yok** — Günlük'te boş durum tasarlanmadı. Bu
   bilinçli bir "eksik": boş durum tasarlamamak genelde amatörlüktür, ama
   burada bölümün **yokluğu** doğru boş durumdur; kurulum yolu iki ayrı
   yerde (onboarding, Profil) duruyor ve Günlük'ün ilk katı korunuyor.
5. **Varsayılan açık.** İlk kullanımda kapalı gelse kullanıcı rutinlerinin
   Günlük'e taşındığını hiç öğrenmez. Sonraki açılışlarda son hâl
   hatırlanır — "her açılışta açık" bir kararı kullanıcının elinden alırdı.
6. **Prototip çerçeveleri kaydırılmış ekran gösteriyor.** Bölüm gerçek
   cihazda 10 kategori satırının altındadır; çerçeveyi tepeden çizmek
   bölümü hiç göstermezdi. Kesme **iki satır arasından** geçer, hiçbir
   nesne ortasından bölünmez (K-057/8). `.kirpik-ust` bölge [A]'dır,
   RN'e kodlanmaz.
7. **`circle-slash` iki anlama geldi** (limiti kaldır · almadım). Kilitli
   sete yeni glif eklemek yerine bu kabul edildi; iki bağlam birbirinden
   uzak ekranlarda ve iki anlam da "iptal/yok" ailesinde.
8. **Aynı bölümde iki farklı yükleme var** (bölüm verisi ≥150ms → iskelet;
   satır eylemi → düğme içi spinner). Bilinçli: biri ekranın düzenini,
   öteki tek bir dokunuşun sonucunu bekletir.

---

## 12. Anti-pattern öz-denetimi

| # | Madde | Durum |
|---|---|---|
| 1 | Mor-mavi varsayılan gradyan | ✅ Palet tokens v4; işaretli düğme **düz** `primary-deep`, gradyan yok |
| 2 | Her elemanda glassmorphism | ✅ Blur yok; derinlik kil gölgesinden |
| 3 | Amaçsız drop-shadow | ✅ Üç seviye anlam taşır: kap `raised` · eylem kuyusu `sunken` · işaretli eylem `raised`. Satır kabı içinde ikinci `raised` katman yok |
| 4 | Karışık köşe yarıçapı | ✅ Yalnız 24 (kap) ve 16 (eylem); ikisi de eleman tipinden türüyor. Prototip taraması: 0 bulgu |
| 5 | Varsayılan font | ⚠️ Montserrat + Poppins — **proje kararı** (tokens §2.1, `₺` glifi ve `tnum` doğrulamasıyla). Bu belge font değiştirmez |
| 6 | 3 sütunlu "daire ikon + başlık + 1 cümle" | ✅ Yok. Satırda ikon kabı bile yok; eylem düğmeleri **kare-yumuşak** (r16) ve bilgi değil eylem taşıyor |
| 7 | Stok illüstrasyon | ✅ Yok; bu bölümde çizim primitifi yok |
| 8 | Kimliksiz beyaz boşluk | ✅ Zemin `#E6EFFE`, kap `surface`, eylem kuyuları `well` |
| 9 | Jenerik pazarlama dili | ✅ En uzun cümle 4 kelime; övgü yok, ünlem yok ("vazgeçtin", "yazıldı" — nötr tespit) |
| 10 | Düşük kontrastlı açık gri metin | ✅ En düşük çift `text-2`/`well` = **5.13** ✅; pasif düğme `text-2`/`disabled-bg` = **4.73** ✅ (tokens §1.9'un hesaplanmış değeri; r0'daki 4.74 yuvarlama hatasıydı). `text-3` kullanılmadı |
| 11 | Rastgele boşluk | ✅ Yalnız 4/8/12/16/24; her değerin tek işi §2.2'de. Prototip taraması: 0 bulgu |
| 12 | Dark mode'un ters çevrilmesi | ✅ Karanlık mod Faz 2; üretilmedi |
| 13 | Emoji | ✅ Tarandı: 0 |
| 14 | Brandbook dışı renk | ✅ Palet dışı hex yok (`#FFFFFF` = `surface` jetonu, işaretli düğmenin metni) |
| 15 | Gerçek içerik | ✅ Rutin değerleri ürünün kendi sayılarıyla tutarlı: Kahve 31 ₺ × 20 gün = 620 ₺ · Sigara 60 × 8 = 480 ₺ · Enerji içeceği 28 × 5 = 140 ₺ → toplam **1.240 ₺**, yani Tasarruf D bölümünün ve Profil satırının aynı sayısı. Lorem yok |
| 16 | `:hover` / grid / `::before` / `calc` / `z-index` | ✅ `<main>` taraması 0 bulgu; yalnız flexbox |
| 17 | Basılı durum | ✅ Başlık, iki eylem ve işaretli eylem için ayrı ayrı tanımlı; prototipte **çizili** (G1). Hover yok |
| 18 | Boş/yükleniyor/hata/uzun metin | ✅ 7 çerçevenin 4'ü bu durumlar (rutin yok · iskelet · ağ hatası · uzun ad + liste sınırı) |
| 19 | Ekran başına mood | ✅ Günlük = "günün kontrol listesi": kahraman sayı + işaretlenecek satırlar. Bölüm bu moodun devamı, yeni bir dil değil |
| 20 | Kontrast WCAG AA | ✅ Yeni **değer** üretilmedi; kullanılan **dört** çiftin hepsi tokens §1.9'da: `#FFFFFF`/`primary-deep` **5.37** (işaretli düğmenin glifi + etiketi) · `text-2`/`well` **5.13** (işaretsiz düğmenin "Aldım/Almadım" etiketi) · `primary-text`/`well` **5.12** (işaretsiz düğmenin 20pt glifi — grafik eşiği 3:1, metin eşiğini de geçiyor) · `text-2`/`disabled-bg` **4.73** (pasif düğme). Dördüncü çift Ö1'de eksikti; **tokens §1.9'a eklendi**, uydurulmadı |

---

## 13. REV3 kapanan maddeler

| Kod | Direktif maddesi | Ne yapıldı | Nerede |
|---|---|---|---|
| **R1** | "Rutinler Günlük sayfasında kategorilerin altında yer alsın" | Kategori kartının altına, 8pt aralıkla açılır bölüm; okuma sırası §2.1 | §2 · prototip **G1** |
| **R2** | "dropdownlı şekilde" | `Accordion` bileşeni: kapalı 76pt, açık 250pt; tek glif 180° döner; 200ms yükseklik animasyonu (RN'de inşa edilebilir) | §3 · `stil-rev2.css` §9 |
| **R3** | "hızlı şekilde rutin harcama girebilsin" | "Aldım" tek dokunuşla harcama yazar (form açılmaz); 6 sn geri al | §4.1 · §7 |
| **R4** | "bugün bu rutin harcamayı yapmadığını işaretleyebilsin" | "Almadım" vazgeçmeyi işaretler; tekrar dokunmak kaldırır | §4.1 · §5/4-5 |
| **R5** | "rutinin adı, mali değeri" görünsün | Satırda yalnız ad (`body-strong`) + günlük değer (`amount` 17) | §4 |
| **R6** | "artı ikonu" | `plus`, "Aldım" etiketiyle | §4.1 |
| **R7** | "alınmadığını belirtmek için başka bir icon" | `circle-slash` — kilitli setten, yeni glif yok, gerekçe ve reddedilen dört alternatif yazılı | §4.1 · §11/7 |
| **R8** | "rutinin tüm bilgileri görünmesine gerek yok" | Kategori, günlük adet, geçmiş, yönetim düğmeleri satırdan çıktı; `/rutinler`de kaldı | §1 · §4 |
| **R9** | Zorunlu durumlar (10 kalem) | Durum matrisi §5; 7 prototip çerçevesi | §5 · prototip **G1-G7** |
| **R10** | Geçmiş gün davranışı | Net karar: görünür ve etkin; etiketler gün-nötr, gün başlıkta kalıcı | §6 · prototip **G7** |
| **R11** | Dokunma hedefi ≥44 + kazara dokunma | 64×44 hedefler, 12pt boşluk, görünür etiket, 6 sn geri al, sessiz olmayan geri bildirim | §4.1 |
| **R12** | Rutin yönetimi Günlük'e taşınmasın | Ekle/düzenle/kaldır/adet/fiyat `/rutinler`de; Günlük'te tek bir yönetim kontrolü yok | §1 |

---

## 14. REV3-r1 — kapanan bulgular (`design-reviewer` 2. tur)

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **B2** | `yukleniyor` hâlinde **iki düğme de** pasif: `rutin_eylem()` gerçek `<button>` üretiyor ve `kilitli = pasif or spinner` → `disabled` + `aria-disabled="true"`. Spinner taşıyan eleman artık `<div>` değil `<button disabled>`; rol ve pasif semantiği kaybolmuyor. Dokunulan düğme **işaretli** çizilir (kullanıcının gördüğü geri bildirim), dokunulmayan **pasif** | §5/6 · `uret_gunluk_rutin.py: eylem()/rutin_satiri()` · prototip **G4** |
| **B3** | Geçmiş günde gün bilgisi **sesli katmana** da girdi: bölüm etiketi "Rutinler. 16 Eylül. 3 rutin · 2 işaretsiz", eylem etiketi "Kahve, 16 Eylül. Aldım olarak işaretle, 31 ₺". Görsel etiketler gün-nötr kaldı. Kararın gerekçesi §8'e, anahtarlar (`bolumGecmis` · `aldimGecmis` · `almadimGecmis`) `metinler.md` §29'a yazıldı | §8 · `metinler.md` §29 · prototip **G7** |
| **B4** | Sıralama kuralı yazıldı: **yalnız mount'ta**, **yalnız >5 rutinde** ve **yalnız hangi 5 satırın çizileceğini seçmek için**. İşaretleme sonrası satırlar **yerinde kalır** (parmağın altındaki satır zıplamaz). Beş durumlu tablo + kabul edilen bedel. G1 (60 · 31 · 28, işaretli "Kahve" ortada) ve G3 buna göre çizili | §5 (sıralama kuralı) · §5/9 · prototip **G1/G3** |
| **Ö1** | `primary-text`/`well` çifti `tokens.md` §1.9'a eklendi: **5.12** AA (hesaplandı — `#2C62B8` üzerine `#E6EFFE`; `well` ve `bg` aynı hex olduğu için `primary-text`/`bg` ile aynı değer). §12/20 üç çiftten **dört çifte** çıktı. **Direktifteki 5.07 rakamı doğrulanamadı** — hesap 5.12 veriyor; 5.06 olan çift `primary-text`/`primary-soft`'tur | `tokens.md` §1.9 · §12/20 |
| **Ö2** | `text-2`/`disabled-bg` **4.74 → 4.73** (tokens §1.9'un hesaplanmış değeri; 4.74 yuvarlama hatasıydı). İki yer: §12/10 ve §12/20 | §12/10 · §12/20 |
| **Ö3** | `gunluk_adet > 1` olan rutinin satırda nasıl okunduğu yazıldı: satır **günün tamamını** işaretler, adet satırda görünmez, tutar çarpımı taşır (31 ₺ × 2 → **62 ₺**). Kısmi işaret ve doğrulama yolu `/rutinler`. Dört soruluk tablo. Prototipte çizili: G3'ün ilk satırı (`Kahve · 62 ₺ · Yazıldı · 08.20`) | §4 · prototip **G3** |
| **Ö5** | "Yükleniyor" a11y karşılığı `metinler.md` §29'a girdi: **`a11y.bolumYukleniyor` = "{başlık}. Yükleniyor"** (paylaşılan anahtar). İki yerde uygulandı — Günlük rutin bölümü (`iskelet_ozet` → "Rutinler. Yükleniyor") ve Tasarruf akordiyonunun **dört** bölümü (`ozet or "Yükleniyor"`). Görünür karşılığı yok: o yerde iskelet bloğu durur | §8 · `metinler.md` §29 · `uret_gunluk_rutin.py: rutin_bolum()` · `uret.py: akordiyon()` · prototip **G4** ve **F4** |
| **Ö6** | `stil-rev2.css` §12 yorumu: rutin bölümü "13 kategori satırının altındadır" → **10** (sabit ödeme üçlüsü `GUNLUK_HARCAMA_KATEGORILERI`'nde yok; `kategori_kirpik()` de 10 diyor) | `stil-rev2.css:160` |
| **ek** | Açık iskelet bölümünde özet placeholder'ı kaldırıldı: yüklü açık bölüm de özet taşımadığı için placeholder yükleme bitince başlık satırını **zıplatıyordu**. Artık 104×18 blok **yalnız kapalı** yüklenen bölümde çizilir (`uret.py: akordiyon()` ile aynı kural). §3.1 ve §5/8 buna göre ayrıldı | §3.1 · §5/8 · `rutin_bolum()` · prototip **G4** |
| **öneri** | "Hepsi işaretli" özet varyantı çerçevesi zaten vardı (**G2B**) ve korundu. "işaretlenmedi" varyantı **çizilmedi** — özet tablosunda (§3.1) yazılı, ayrı çerçeve aynı düzenin üçüncü kopyası olurdu | §3.1 · prototip **G2B** |

---

## 15. REV3-r2 — PASS sonrası kapatılan üç not

| Kod | Ne yapıldı | Nerede |
|---|---|---|
| **tokens tekrarı** | `primary-text`/`well` = **5.12** çifti §1.9'da **üç satırda** duruyordu (temel tablo "`well` = `bg`" · v4 "yasal bağlantı, E-23" · REV3 "E-10 düğme glifi"). `well` ve `bg` aynı hex (`#E6EFFE`) olduğu için üçü de aynı sayıydı. **Temel tablodaki satır** kaldı, kullanım yerleri onun notuna taşındı, tur bazlı iki tekrar silindi. **Değer değişmedi** (5.12 bağımsız olarak iki kez doğrulandı) | `tokens.md` §1.9 |
| **eksik komşuluk kaydı** | `.cubuk-oluk` (`groove #F2F7FE`) artık `well #E6EFFE` zeminli satır kuyusunun içinde yaşıyor; ölçüm §1.9'da kayıtlı değildi. Eklendi: dolgu/oluk **4.20 – 4.78** · dolgu/`well` **≥3** → yeni WCAG sorunu yok, ama komşuluk artık yazılı | `tokens.md` §1.9 |
| **üreteçte yanlış mantık varyantı** | `rutin_bolum()` içinde `acik = bool(icerik) or iskelet_ozet` idi: "kapalı + yükleniyor" çağrısında hem `aria-expanded="true"` hem 104×18 özet yer tutucusu üretirdi — §3.1 ("açık bölüm özet taşımaz") ile çelişir. Yedi çerçevede bu yola girilmiyordu (G4 içerik geçiriyor) ama **frontend bu mantığı kopyalayabilirdi**. `uret.py: akordiyon()`'un doğru hâline hizalandı: `acik = bool(icerik)` + gerekçe yorumu. Prototip yeniden üretildi, çıktı birebir aynı | `uret_gunluk_rutin.py: rutin_bolum()` |
| **a11y notu (kod için)** | Kilitli (yükleniyor) eylem düğmesinde RN'de `accessibilityState={{ selected, disabled }}` **birlikte** verilecek — iyimser işaret sesli katmanda kaybolmasın. Prototipte `aria-pressed` kilitli hâlde düşüyordu; bu HTML sınırıdır, RN'de taşınacak | §8 |
