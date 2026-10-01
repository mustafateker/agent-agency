# REV3 — E-18 Taksitler · kategori ve **ürün bazlı** kırılım

> **Delta spesifikasyonu.** Onaylı v4 tasarımını (`prototip-v4/10-taksitler.html`)
> yerinden oynatmaz; üzerine **bir düzey** ekler. Görsel otorite değişmedi:
> `docs/brand/tokens.md` v4 (claymorphism) + `docs/brand/brandbook.md` §2.
> Yeni renk · punto · radius · boşluk · gölge · ikon seti **üretilmedi**.
> Yeni veri alanı / API ucu **istenmedi**.
>
> Prototip: `prototip-rev2/taksitler.html` (**9 çerçeve**) ·
> üreteç: `prototip-rev2/_uret/uret_taksitler.py` ·
> mekanik denetim: `python3 _uret/denetim.py` → **0 bulgu**.
>
> **REV3-r1** (design-reviewer REVİZE turu): 4 bloklayıcı + 3 önemli madde
> kapatıldı. **REV3-r2** (ikinci tur): 1 bloklayıcı (tek kategorili bölüm
> başlığının yapısı) + 1 önemli (dip ≠ çubuk toplamı garantisi) + 2 rötuş.
> Değişenler ölçü, dizilim ve yazılı kuraldır; **hiçbir tutar değişmedi**
> — kapanan bulgular ve nerede karşılandıkları **§13**'te tablo hâlinde.
>
> Mustafa'nın direktifi (birebir): *"Taksitler kısmında kategori altında
> aldığım ürün bazlı da taksitleri göreyim. Direkt toplam taksit miktarı
> görünüyor; toplam da görünsün, aldığım ürün bazlı da takip edebileyim
> taksitleri."*

---

## 1. Bugünkü hâlin tespiti (koddan okundu, varsayım yok)

Kaynak: `../mobile/app/taksitler.tsx` · `../mobile/src/db/harcama.ts`.

| Soru | Bugünkü cevap | Kaynak |
|---|---|---|
| **Ekran ay bazlı mı?** | **Hayır.** Referans daima `ayAnahtari(new Date())`; ay gezinme kontrolü (`MonthNav`) yok, geçmiş aya bakılamaz. "Önümüzdeki aylar" kartı bugünden itibaren **6 ay** ileri bakar. | `taksitler.tsx` 63-73 |
| Toplam nereden geliyor | `taksitBuAyToplam(db, buAy)` → kahraman kart `display` 32pt | `taksitler.tsx` 127 |
| Ürün adı verisi var mı | **Var.** `Harcama.urunAdi` (`urun_adi`) her taksit satırında taşınıyor; `SurenSeri` türü onu **eşlemeye almıyor** sadece | `harcama.ts` 61, 490-524 |
| Seri konumu | `taksitNo` / `taksitToplam` — satırda hazır | `harcama.ts` 493-494 |
| Kalan tutar | Seri düzeyinde **türetilebilir**: `surenSeriler` zaten `tumSayfalariGetir({})` ile tüm kayıtları okuyor (`sonAy` için), aynı geçişte hesaplanır | `harcama.ts` 507-513 |
| Tamamlanmış seri | Bugün: listede **yok**; yalnız geçen ay biten **tek** seri bilgi şeridiyle anılıyor | `harcama.ts` 527-534 |
| Silme | Geri alınamaz, onay diyaloğu E-13 (K-029). E-18'de silme eylemi **yok** | `harcama.ts` 309 |

### 1.1 Ekranı ay bazlı YAPMAMA kararı (K-T0)

Ay seçici **eklenmiyor.** Gerekçe üç maddedir:

1. Ekranın işi **ileri bakmak**: "bu ay ne ödüyorum, sonraki aylarda ne
   ödeyeceğim". Geçmiş ay taksitleri zaten birer harcama kaydıdır ve
   E-14 Kayıtlar + E-16 Özet onları ay ay gösterir. Üçüncü bir ay gezinmesi
   aynı veriyi üçüncü kez sunardı.
2. Ay seçici gelirse "kalan" ve "3/12" **hangi aya göre** sorusu doğar;
   geçmiş bir ayda "kalan" göstermek kullanıcıyı yanıltır (o tarihteki
   kalan mı, bugünkü kalan mı?).
3. Mustafa'nın direktifi zaman ekseni değil **kırılım** istiyor.

→ **PM kararı gerekirse:** geçmiş aylara bakma ihtiyacı doğarsa bu, E-18'e
ay seçici eklemek yerine **E-16 Özet'e "taksit" süzgeci** olarak açılmalı.
Bu turda kapsam dışı bırakıldı.

---

## 2. Bilgi hiyerarşisi — üç düzey, tek ekran

```
Düzey 1   BU AY TOPLAMI          kahraman kart · display 32pt · "3.120 ₺"
Düzey 2   KATEGORİ               akordiyon başlığı · h2 + özet label
Düzey 3   ÜRÜN / SERİ            satır · body-strong ad + amount tutar
                                 + ilerleme çubuğu + caption "4/12 · kalan …"
Bağlam    ÖNÜMÜZDEKİ AYLAR       6 çubuk · v4'ten aynen
```

**Toplam kaybolmuyor** (direktifin ilk yarısı): kahraman kart hiç
değişmedi — aynı etiket, aynı 32pt sayı, aynı açıklama satırı.
**Toplam doğrulanabilir hâle geliyor**: ürün tutarlarının toplamı =
kategori özeti (1.041 + 520 + 259 = 1.820), kategori özetlerinin toplamı =
ay toplamı (1.820 + 780 + 520 = 3.120). Kullanıcı üç düzeyi kafasında
toplayabilir; bu, sayının "nereden çıktığı" sorusunu kapatır (Tasarruf
akordiyonunun A bölümüyle aynı mantık, `rev2-tasarruf-profil.md` §3.12.2).

> Bu eşitlik kendiliğinden gelmez, **kuralla** gelir: yuvarlama yalnız
> **yapraklarda** (ürün satırında) yapılır, üst düzeyler **ekranda yazan**
> değerleri toplar. Kuralın tam hâli ve gerekçesi **§5.1**'de; prototipin
> her sayısının kuruş modeli **§5.3**'te.

### 2.1 Ekran sırası DEĞİŞTİ — kırılım, ay haritasının ÜSTÜNE çıktı (K-T1)

| | v4 sırası | REV3 sırası |
|---|---|---|
| 1 | Bu ay toplamı | Bu ay toplamı |
| 2 | **Önümüzdeki aylar** (6 çubuk) | **Süren taksitler** (kategori → ürün) |
| 3 | Süren seriler (düz liste) | **Önümüzdeki aylar** (6 çubuk, içerik aynı) |
| 4 | Biten seri şeridi | Biten seri şeridi |

**İlk katın ölçüsü — tek kaynak:** E-18 bir **push** ekranıdır, sekme
çubuğu **yoktur** (§8, ve v4 HTML'inde de yok). `prototip-v4/stil.css`
162-186: `.screen` 844 → `.statusbar` **47** + `.home-indicator` **28** →
kaydırma alanı `.kaydir` = **844 − 47 − 28 = 769px**. Bu belgede geçen tek
ilk-kat değeri budur. (Sekmeli ekranların 693'ü bu ekrana **uymaz**.)

**Gerekçe (ölçüyle):** v4 sırası korunsaydı ilk akordiyon **568px**te
başlardı — kırılımın başlığı ve bir tam ürün satırı ilk katta görünürdü,
yani "hiç görünmezdi" demek yanlış olur. Sorun görünürlük değil **kesme
yeri**: v4 sırasında 68 (başlık) + 122 (kahraman) + 24 + **297** (ay kartı:
16 + 25 + 8 + 6×24 + 5×8 + 12 + 36 iki satır dip + 16) + 24 + 25 (bölüm
başlığı) + 8 = 568'de başlayan akordiyonun ilk satırı 640-726, **ikinci
satırı 738-824** olur; 769'daki kesme **ikinci ürün satırının tam
ortasından** geçer — K-057/8 ihlali. Yeni sırada kesme bir kabın alt iç
boşluğuna denk geliyor (§2.2).

İkinci ve üçüncü gerekçe (bu turda da geçerli) aşağıda: zaman mantığı ve
"olgu önce gelir".

**Zaman mantığı da tutarlı:** şimdi (bu ay toplamı) → şimdinin ayrıntısı
(neye ödüyorsun) → gelecek (önümüzdeki aylar). v4'te ortada duran gelecek,
şimdiyi ikiye bölüyordu.

**Kaybedilen:** ay haritası ilk kattan çıktı. Kabul edildi, çünkü (a)
içeriği ve ölçüsü hiç değişmedi, (b) kahraman kartın altındaki tek cümle
zaten "taksitler ait olduğu aya yazılır" diyerek zaman eksenini
hatırlatıyor, (c) ay haritası bir **tahmin**, kırılım bir **olgu**;
olgu önce gelir.

### 2.2 İlk kat hesabı (token yükseklikleriyle, T1 çerçevesi)

> Bu bir **hesap**, tarayıcı ölçümü değil: `tokens.md` §2.2 satır
> yükseklikleri + §3.1 ritim + §7.2/§7.3 iç boşlukları toplandı.

| Blok | Yükseklik | Nasıl | Bitiş |
|---|---|---|---|
| `PushHeader` (`.ekran-basi`) | 68 | 8 + 44 + 16 | 68 |
| Kahraman kart | 122 | 16 + (18 + 4 + 38 + 12 + 18) + 16 | 190 |
| ↕ bölümler arası | 24 | §3.1 | 214 |
| Bölüm başlığı satırı | 25 | `h2` satır yüksekliği | 239 |
| ↕ başlık ↔ gövde | 8 | §3.1 | 247 |
| **Diğer (açık, 3 satır)** | **370** | 16 + 44 + 12 + (86 + 12 + 86 + 12 + 86) + 16 | 617 |
| ↕ bölümler arası | 8 | akordiyon aralığı | 625 |
| **Giyim (kapalı)** | 76 | 16 + 44 + 16 | 701 |
| ↕ | 8 | | 709 |
| **Sağlık (kapalı)** | 76 | | 785 |

**İlk kat 769'da** (844 − 47 − 28), yani Sağlık bölümünün **alt iç
boşluğunda** kesiliyor: başlık bloğu 725-769 tam sığıyor (metin satırı
734,5-759,5), kesilen tek şey kabın 16pt alt boşluğudur. Hiçbir satır,
sayı ya da metin ortasından bölünmüyor (K-057/8) — E-10 ve E-27'nin
onaylanmış deseniyle aynı. Ay haritası 809'da başlar.

Ürün satırı yüksekliği **86**: 12 + (24 ad/tutar + 4 + 12 çubuk + 4 + 18
ikincil) + 12. `tokens.md` §7.3 minimum 68'in üstünde, yeni ölçü ailesi
açılmadı. Satırın iç genişliği: akordiyon içinde 326 − 32 (satır iç
boşluğu) − 12 − 20 (`chevron-right`) = **262**; akordiyon kurulmayan
düzende 358 − 32 − 32 = **294** (r1'de satırdan düşen `.kat-kab` 56pt yer
bıraktı, ok 32 aldı → ada **net 24pt kazanç**).

**Tek kategorili düzende** (T3/T4/T9) bölüm başlığı satırı 25 değil **44**
yükseliktir: akordiyonun başlık **yapısı** oraya taşındı — `.kat-kab` 44 +
12 + `h2` kategori adı + 12 + "{adet} ürün" (§4.2). Zincir: 214 → başlık
**214-258** → +8 → altı satır 266'dan başlar (her biri 86, araları 8) →
altıncı satır **736-822**. İlk kat bu satırın **içinden** geçer.

**769'da kesilen tam olarak nedir** (r2'de yazıldı: "yarım satır kaydırma
davetidir" savunması ancak kesilen parça adıyla yazılırsa savunmadır):

| Altıncı satırın parçası | Aralık | 769'da |
|---|---|---|
| üst iç boşluk | 736-748 | tam |
| **ürün adı + bu ayki tutar** (satır kutusu 24) | 748-772 | kutunun alt **3pt'si** kesilir, **metnin kendisi tam**: 16pt adın em kutusu 752-768, 17pt tutarın 751,5-768,5 — ikisi de kesmenin üstünde |
| ilerleme çubuğu (12) | 776-788 | **görünmez** |
| "{no}/{toplam} · kalan …" (18) | 792-810 | **görünmez** |
| alt iç boşluk | 810-822 | görünmez |

Yani kesilen katman **ikincil**: kullanıcı altıncı ürünün adını ve bu ayki
tutarını tam okur, çubuğunu ve kalanını görmek için kaydırır. Kesilen 3pt
ağırlıklı olarak satır **aralığıdır**. Tam dürüst ölçü şu (r3): yukarıdaki
752-768 / 751,5-768,5 aralıkları **em kutularıdır**; gerçek satır kutusunda
16pt bir adın alt çıkıntısı (T4'ün altıncı satırı "Elektrikli süpürge" → p,
g) em kutusunun ~1,7pt altına, yaklaşık **769,7**'ye iner. Yani kesmede
**glif gövdesi tam, alt çıkıntı kuyruğunun son ~1pt'si sıyrılabilir** —
harf tanınırlığını taşıyan hiçbir parça kaybolmuyor, "p" ile "o"yu
karıştırmak mümkün değil. K-057/8'in yasakladığı şey okunurluğu bozan
ortadan bölünmedir ve o oluşmuyor; istenirse altıncı satırı 3pt yukarı alan
bir düzeltme de bu 1pt'yi sıfırlar, ama ritmi (86 + 8) bozduğu için
yapılmadı. Bilinçli: liste kaydırılmak için vardır ve yarım görünen satır
kaydırma davetinin kendisidir. K-057/8 ölçülen **ana** çerçeveye (T1) tam
uygulanır.

---

## 3. Ürün satırı — neyin birincil olduğu kararı

```
┌──────────────────────────────────────────────────────┐  .satir-kart.kuyu
│ Telefon                          1.041 ₺             │  body-strong · amount
│ ▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ›   │  .cubuk-oluk 12pt
│ 4/12 · kalan 8.333 ₺                                 │  caption · text-2
└──────────────────────────────────────────────────────┘
                                                  20pt chevron-right (text-2)
```

| Bilgi | Düzey | Neden |
|---|---|---|
| **Ürün adı** | Birincil (sol üst, `body-strong` 16) | Direktifin öznesi. Kullanıcı "ne aldım" diye bakıyor |
| **Bu ayki tutar** | Birincil (sağ üst, `amount` 17, tabular) | Ekranın para birimi; kategori ve ay toplamlarıyla toplanabilir olmalı |
| İlerleme çubuğu | İkincil | "Bu borcun nesi bitti" sorusuna **okumadan** cevap |
| `{no}/{toplam}` | İkincil (`caption`) | Çubuğun metin karşılığı — renk/şekil tek başına bilgi taşımaz (WCAG 1.4.1) |
| Kalan tutar | İkincil (`caption`) | Görsel olarak türetilemeyen tek sayı |
| ~~Bitiş ayı~~ | **Satırdan çıkarıldı** | `{no}/{toplam}` + aylık ritim bitişi zaten söylüyor; serinin en geç bitişi ay kartının dip satırında duruyor. Dördüncü ikincil veri satırı bilgi çöplüğü olurdu |
| ~~"her ay"~~ | **Çıkarıldı** | Kartın etiketi "Bu ay", satırın tutarı zaten aylık. v4'teki ikinci satır yer israfıydı |
| **`chevron-right` 20pt** | Üçüncül (sağ kenar, `text-2`) | **r1'de eklendi.** Satır bir ilerleme çubuğu + iki sayı taşıyan **veri bloğu** gibi okunuyordu; dokunulabilir olduğunu söyleyen görsel işaret yoktu ve ilk turdaki "tutarı kırpar" gerekçesi geçersizdi: ok, tutarın **sağına** girer ve 12+20 = 32pt'yi `flex:1` olan **ad** sütunundan alır, `flex:0 0 auto` olan tutardan değil. Kategori ikon kabının satırdan düşmesiyle (§4.2) ada net 24pt **kaldı** |

**Son taksit hâli:** `no == toplam` ise "kalan 0 ₺" **yazılmaz** — sıfır
bir bilgi değil, gürültüdür. Yerine `label` / `primary-text` renginde
**"Son taksit bu ay"** durur ve çubuk %100 dolar.

> **v4 düzeltmesi:** v4 prototipi bu satırı `.c-warn` (= `warning-ink`,
> limit dışı sinyali) ile çiziyordu. `tokens.md` §1.3 `warning` ailesini
> **yalnız limit dışı** bağlamına kilitler; son taksit bir limit aşımı
> değil, bir olgudur (hatta iyi haberdir). REV3'te `primary-text`
> kullanılıyor. Bu, renk sisteminin kendi kuralına dönüş, yeni renk değil.

**Çubuk dolgusunun rengi kategorinin `solid` rengidir** (`cat.*.solid`),
`grad.action` değil. Gerekçe: `tokens.md` §1.4 `solid` için izinli yerler
arasında **"kategori çubuğu dolgusu"** yazılıdır ve satır kategorisinin
içinde yaşıyor; mavi dolgu `cat.mavi` kategorisinde kendisiyle çakışırdı.
Oluk `groove` + `clay.sunken` (`.cubuk-oluk` — E-10'un kategori limit
çubuğuyla **aynı bileşen**, yeni bileşen değil).

**Kategori düzeyinde ilerleme çubuğu ÇİZİLMEZ.** Bir kategori birbiriyle
ilgisiz serileri toplar; "Diğer %47 bitti" cümlesi hiçbir şey ifade etmez.
Kategori özeti yalnız **tutar + ürün sayısı** taşır.

---

## 4. Kategori bölümü — mevcut `Accordion` yeniden kullanıldı

Desen **yeniden icat edilmedi**: `stil-rev2.css` §9-§10 ve
`rev2-tasarruf-profil.md` §3.12'de kurulan akordiyon bileşeninin aynısı.
Tek delta: başlığa 44pt **kategori ikon kabı** (`.kat-kab`, mevcut bileşen)
eklendi.

| Konu | Karar | Dayanak |
|---|---|---|
| Kap | `surface` + `clay.raised` · radius 24 · iç boşluk 16 | §3.12.3 |
| Başlık bloğu | `.kat-kab` 44 + 12 + `h2` kategori adı (esner, tek satır) + 12 + özet `label`/`text-2` + 12 + 20pt `chevron-down` | §3.12.3 + `tokens.md` §7.3 |
| Başlık genişlik hesabı | 326 iç genişlik = 44 + 12 + ad (esner) + 12 + özet ≤ 120 + 12 + 20 → ada **en az 106** kalır; uzun kategori adı ("Kira ve ev" 11 karakter) sığar, sığmazsa tek satırda kırpılır | — |
| İçindeki satır | **Bir basamak iner**: `well` + `clay.sunken` (`.satir-kart.kuyu`) | `stil-rev2.css` §10 |
| Satırda kategori ikonu | **Hiçbir düzende yok** — kimliği daima bir **başlık** taşır, aynı ikonu her satırda tekrarlamak gürültüdür. Akordiyon varsa kategori akordiyonun başlığında, akordiyon yoksa **bölüm başlığında** (§4.2) | §1.4: renk + ikon + metin **bölüm düzeyinde** sağlanır |
| Satırda ok | 20pt `chevron-right`, `text-2` — her iki düzende **aynı** | §3 |
| Basılı | Kabın tamamı çöker (`groove` + `clay.pressed`); satır basılıyken `.kuyu.basili` | §3.12.3 |
| Ok | Tek glif, açıkken 180° döner (`chevron-up` kilitli sette yok) | `stil-rev2.css` §9 |
| Animasyon | Yükseklik 200ms ease-out; reduce motion → 0ms | §3.12.3 |
| Çoklu açık | Serbest; bir bölümü açmak diğerini kapatmaz | §3.12.3 |
| İç içe akordiyon | **Yok** | §3.12.3 |
| Hafıza | Ekranda kalındığı sürece korunur; ekrandan çıkıp dönünce varsayılana döner | §3.12.3 |

### 4.1 Hangi kategori açık gelir

**Bu ay toplamı en büyük olan kategori.** Gerekçe: kahraman sayının en
büyük parçası oradadır; kullanıcının "3.120 ₺ nereden çıktı" sorusu ilk
katta kapanır. Eşitlikte `kategoriler.ts` sırası belirler.

Reddedilen iki alternatif:
- **Hepsi kapalı:** ilk kat üç boş başlık olur, direktif görünmez.
- **Hepsi açık:** ekran satır duvarına döner, "toplam" okunurluğunu
  kaybeder — Mustafa'nın koruduğunu istediği şey tam olarak oydu.

### 4.2 Akordiyon NE ZAMAN kurulmaz (K-T2)

**Kategori sayısı 1 ise akordiyon çizilmez.** Tek çocuklu bir kap yalnız
bir dokunuş maliyeti ekler. O durumda kategori kimliği **bölüm başlığına**
taşınır, satıra değil:

- Bölüm başlığı, T1'in **akordiyon başlığıyla aynı yapıya** oturur:
  `.kat-kab` 44 (kategori rengi + glifi) + 12 + **`h2` kategori adı**
  ("Diğer") + 12 + sağda `label`/`text-2` **"{adet} ürün"** ("8 ürün").
  Başlık satırı bu düzende 25 değil **44** yüksekliktedir.
- **Jenerik "Süren taksitler" başlığı bu düzende DÜŞER.** K-T2 başlığın
  işini zaten kategoriye devrediyor; ikisi birlikte dururdu ise 358px'lik
  satırın **sol** ucunda kab, **sağ** ucunda kategori adı, ortada ilgisiz
  bir `h2` kalırdı — kabın en yakın metni "Süren taksitler" olurdu ve
  K-T2'nin kendi kuralı ("kategori kimliği **en yakın** başlıkta durur")
  ihlal edilirdi. Üstelik aynı bileşen (kab + `h2` + sağ özet) tek ekranda
  iki anlam taşırdı: T1'de kategoriye bağlı, burada bölüme.
- Kategori **tutarı** başlıkta yazılmaz (akordiyon özeti "1.820 ₺ · 3 ürün"
  derken burada yalnız "8 ürün"): tek kategoride kategori toplamı kahraman
  kartın sayısının kendisidir, 24pt yukarıda 32pt puntoyla duruyor.
- Başlıkta **`chevron-down` yok** — bu başlık açılıp kapanmaz ve
  dokunulabilir değil. Ama ayrımı taşıyan **ok değil, kartın yokluğudur**
  (r3; ok tek işaret sanılıyordu): bu dilde dokunulabilirliğin taşıyıcısı
  **kabarık kart**. Akordiyon **daima** `surface` + `clay.raised` +
  radius-24 bir karttır ve başlık satırı o kartın içindeki bir
  `<button>`'dur. Tek kategorili başlık ise **kartsızdır** — doğrudan `bg`
  üstünde duruyor, `<button>` değil, basılı durumu yok. Kullanıcı 44pt'lik
  bir kabı görüp "buraya basılır" demiyor; kabarık bir kart görmediği için
  demiyor. Ok, bu ayrımın yalnız **teyidi**.
- `.kat-kab`, tek kategorili düzende gerçekten **`bg` üstünde** duruyor —
  akordiyon bağlamında kalmıyor (r3: önceki hâlde bunun tersi yazılıydı,
  olgusal olarak yanlıştı). Görsel sonuç **kabul edildi**, çünkü v4'te
  örneği olmamasının nedeni tasarım yasağı değil, o düzenin henüz
  kurulmamasıydı: (1) `tokens.md`'de `clay.sunken` yalnız `inset` gölge
  tanımlar — çevresine dış gölge/halka atmadığı için altındaki yüzeyin
  kabarıklığına yaslanmaz, (2) kabın dolgusu `cat.*.soft` ve bu hue `bg`
  ile aynı değil, yani kap `bg` üstünde **kaybolmuyor** da, `bg`'yi
  oyuyormuş gibi de görünmüyor. Bu, v4'ün kapsamadığı bir komşuluğun
  bilinçli **genişletmesidir**; sapma değil.
- Satırlar **kabarık** kalır (`.satir-kart`, çünkü onları saran bir kap
  yok) ama ikon kabı **taşımaz**.

**Yükleme iskeletinin ayırdığı yükseklik (r3).** İskelet, kategori sayısını
**bilemez** — o yüzden tek bir düzen tahmin etmek zorunda. T7'nin iskeleti
bir açık + iki kapalı **akordiyon** çiziyor, yani **çok kategorili** düzeni
tahmin ediyor; o düzende bölüm başlığı 25'tir ve iskelet de **25** ayırır.
r2'de 44 ayrılıyordu: iskelet çizdiği düzenden farklı bir yükseklik
ayırdığı için **çok kategori çözüldüğünde** başlık 19px yukarı zıplıyordu —
gerekçe simetrik işliyor, bir düzeni kurtarmak diğerini bozuyordu.
Kabul edilen taraf: **tek kategori çıkarsa başlık 25 → 44 büyür ve altındaki
liste 19px aşağı oturur.** Üç nedenle bu taraf seçildi — (1) zıplama nadir
dalda (tek kategori) kalıyor, sık dalda hiç yok; (2) yön **aşağı**, yani
kullanıcının okuduğu başlık yerinde kalıyor, içerik altına açılıyor —
yukarı kayma okunan satırı kaçırtır; (3) alternatif, iskeletin tek
kategorili düzeni (kartsız başlık + 6 kabarık satır) çizmesiydi ve o zaman
çok kategori çözüldüğünde 19px değil **tüm gruplama yapısı** değişirdi.
`SectionHeader`'a evrensel `min-height:44` **verilmedi**: T1'in §2.2
zincirini +19 kaydırır ve 769'daki kesmeyi kapalı akordiyonun başlık
satırının içine sokardı.

**r2 düzeltmesi (K-T2):** ilk hâlde bu düzende hem kab hem "Süren
taksitler" `h2`'si hem "Diğer · 8 ürün" özeti aynı satırdaydı; kategori
glifi solda, kategori adı sağda, aralarında ilgisiz bir başlık. Yukarıdaki
yapı bunu tek noktada kapatıyor (üreteçte `bolum_basi`, T3/T4/T9).

**r1 düzeltmesi (K-T2):** ilk tur satıra `.kat-kab` koyuyordu ve bu §4'ün
kendi gerekçesiyle çelişiyordu — T4'te aynı `circle-dashed` glifi **altı
kez** tekrarlanıyordu. WCAG 1.4.1 gerekçesi de tutmuyordu: kategori adı
zaten bölüm başlığında **metin olarak** yazılı, yani renk tek kanal değil.
Kural artık **tek**: *kategori kimliği en yakın başlıkta durur, satırda
asla tekrarlanmaz.* Tek satır bile olsa (T3) bu kural aynı işler.

Tek kural, iki durumu kapatır: **tek seri** de **tek kategori** demektir
(prototip T3, T4 ve T9).

### 4.3 Sıralama ve liste sınırı

| Konu | Kural |
|---|---|
| Kategori sırası | Bu ay toplamı **azalan** · eşitlikte `kategoriler.ts` sırası |
| Kategori içi seri sırası | Bu ayki tutar **azalan** · eşitlikte `taksitNo` azalan (bitmeye yakın olan üstte) · sonra ürün adı (Türkçe sıralama) |
| Kategori içi satır sınırı | **6**; fazlası `button.ghost` "Tümünü göster" ile açılır |
| "Tümünü göster" | **Tek yönlü**: basılınca kalan satırlar eklenir, düğme düşer. Geri katlanma yok — kullanıcının okuduğu içerik altından çekilmez. İç içe akordiyon **değildir** |
| Ekran düzeyinde sınır | Yok. Kategori sayısı en çok 13'tür (sabit küme), hepsi kapalı 76pt'dir; `FlatList` ile render edilir |

---

## 5. Türetilmiş değerler — formüllerin tek yeri

> Hiçbiri yeni veri alanı / yeni uç istemez. Üçü de `surenSeriler`ın
> **zaten yaptığı** `tumSayfalariGetir({})` geçişinden hesaplanır.

| Değer | Formül | Not |
|---|---|---|
| `urunAdi` | Serinin bu ayki satırındaki `urun_adi` | `SurenSeri` türüne **eşleme** eklenir (alan zaten var) |
| `kalanKurus` | `Σ tutar_kurus` · aynı `taksit_id` · `gun > buAyınSonu` | **Bu ay hariç** — bu ayki tutar satırda ayrıca yazılı ve "Bu ay" toplamına dahil |
| `kategoriToplam(görünen)` | `Σ satır(görünen)` · kategorinin **tüm** serileri (gizli olanlar dahil) | Yuvarlanmış satır değerlerinin toplamı — bkz. §5.1 |
| `ayToplami(görünen)` | `Σ kategoriToplam(görünen)` | Kahraman karttaki sayı. `taksitBuAyToplam`ın kuruş değerinden **ayrı** hesaplanır; gerekçe §5.1 |
| Çubuk oranı | `taksitNo / taksitToplam` | Tutar oranı değil **taksit sayısı** oranı; kuruş dağıtımı oranı bozmasın diye |
| `urunAdi` boş | Yedek metin `taksit.urun_yok` = "{Kategori} taksidi" | Uydurma ad üretilmez |

### 5.1 Kuruş hassasiyeti — "eşit olmayan taksit" görünümü

Seri kuruş-hassas dağıtılır; kalan kuruşlar ilk taksitlere biner, yani
aynı serinin taksitleri **1 kuruş** farklı olabilir (12.500,00 ₺ / 12 →
ilk 8 taksit 1.041,67 ₺, kalan 4 taksit 1.041,66 ₺).

| Kural | Karar |
|---|---|
| Satır tutarı | **O ayın gerçek taksidi**, kuruşsuz yazılır (`1.041 ₺`). brandbook §2.5: liste ve kahraman sayıda kuruş gösterilmez → 1 kuruşluk fark listede **görünmez**. Kuruşlu değer yalnız E-12 detayında |
| `kalan` | Kalan satırların **kuruş toplamı**, sonra yuvarlanır. `aylık × kalan adet` **yasak** — o çarpım 1 kuruşluk sapmayı büyütür ve serinin sonunda tutmayan bir kalan üretir |
| Ay çubukları | Gerçek ay toplamının **kuruşu atılmış** hâli (`Σ kuruş // 100`). İki komşu ay 1 ₺ farklı görünebilir; **düzeltilmez, açıklanmaz** (brandbook §2.8). Ay çubuğu bir **ay**ın toplamıdır, ekrandaki üç düzeyin parçası değildir |

**Yuvarlama yönü (bağlayıcı, tek cümle):** gösterimde **kuruş atılır**, yani
aşağı yuvarlanır (`kuruş // 100`) — `tokens.md` §14.2/6'nın
`gunluk_limit_kurus` için verdiği yönle aynı; 1.041,67 ₺ ekranda **1.041 ₺**
olur, hiçbir yerde 1.042 olmaz.

### 5.1.1 Yuvarlama YAPRAKTA yapılır (K-T13) — r1'de düzeltildi

İlk tur "her satır kendi kuruşundan, toplam da kendi kuruşundan yuvarlanır;
ikisi daima eşittir" diyordu. **Bu matematiksel olarak yanlıştı:**
Σ(yuvarla(satır)) ≠ yuvarla(Σ satır). Üç satır da `x,90` ise ekrandaki
toplam 2 ₺ tutmazdı ve turun tek kazancı — kullanıcının üç düzeyi kafasında
toplayıp doğrulaması — rastgeleye dönerdi.

| Düzey | Nasıl hesaplanır |
|---|---|
| **Ürün satırı (yaprak)** | `tutar_kurus // 100` — **yuvarlama yalnız burada** |
| **Kategori toplamı** | `Σ satır(görünen)` — ekranda yazan tam lira değerlerinin toplamı |
| **Ay toplamı (kahraman)** | `Σ kategoriToplam(görünen)` |

→ "Önce yuvarlayıp sonra toplamak yasak" kuralı **bu ekran için tersine
çevrildi**: burada tam olarak öyle yapılır, aksi hâlde ekran kendini
yalanlar. Kural yalnız gösterime aittir; veritabanı ve E-12 detayı kuruş
cinsinden integer kalır (`tokens.md` §14 girişi).

**Bedeli, bilerek kabul edildi:** kahraman sayı, gerçek kuruş toplamının
yuvarlanmışından en çok *(seri sayısı) × 0,99 ₺* kadar aşağıda kalabilir.
Ekran içi tutarlılık, kuruşa sadakatten önce gelir — kullanıcı kuruşu
göremez, tutmayan toplamı görür.

**Gizli satırlar da toplama girer:** "Tümünü göster" arkasındaki ürünler
kategori toplamına **dahildir** (T4: görünen 6 satır 107.195 ₺, kahraman
sayı 107.390 ₺). Bu yüzden bölüm başlığındaki ürün **sayısı** zorunludur —
"8 ürün" olmadan altı satır kahraman sayıyı açıklamaz.

### 5.2 Gelecekte başlayan seri — bu durum **oluşamaz**

Bir seri ilk taksidini gelecek bir ayda alamaz: E-11 gelecek tarihe kayıt
yazmayı reddediyor (`hata.tarih_gelecek`). Dolayısıyla "ay haritasında var
ama ürün listesinde yok" tutarsızlığı için ayrı bir durum tasarlanmadı.
İleride gelecek tarihli kayıt açılırsa bu satır yeniden değerlendirilir.

### 5.3 Prototipin kuruş modeli — her sayının kaynağı (r1'de eklendi)

> Neden burada: ilk turda prototipteki dört sayı kendini yalanlıyordu
> (ay kartı Kasım/Ocak, iki kalan toplamı). Sebep tek: veri **yazılı**
> değildi, çerçeve çerçeve elle yazılmıştı. Aşağıdaki iki tablo artık
> ekrandaki her tutarın tek kaynağıdır; üreteç bu tablolardan yazıldı.
> Referans ay: **Eylül 2026** (T5'te Ekim 2026).

**A) T1 / T2 / T5 — üç kategori, altı seri**

| Seri | Kategori | Aylık | Eylül'deki no | Son taksit | Kalan (Eylül sonrası) |
|---|---|---|---|---|---|
| Telefon | Diğer | 1.041,72 (toplam 12.500,64) | 4/12 | **Mayıs 2027** | 8 × 1.041,72 = 8.333,76 → **8.333** |
| Buzdolabı | Diğer | 520,00 | 5/9 | Ocak 2027 | 4 × 520 = **2.080** |
| Elektrikli süpürge | Diğer | 259,00 | 6/6 | **Eylül 2026** | 0 |
| Mont | Giyim | 260,00 | — | Kasım 2026 | 2 × 260 = **520** |
| Ayakkabı | Giyim | 520,00 | — | Nisan 2027 | 7 × 520 = **3.640** |
| Gözlük | Sağlık | 520,00 | — | Mart 2027 | 6 × 520 = **3.120** |

- Eylül: Diğer 1.041 + 520 + 259 = **1.820** · Giyim 260 + 520 = **780** ·
  Sağlık **520** → kahraman **3.120** ✓ (§5.1.1 kuralıyla)
- Ay çubukları (kuruş toplamı, aşağı yuvarlanmış): Eylül 3.120,72 → 3.120 ·
  Ekim/Kasım 2.861,72 → 2.861 · Aralık/Ocak 2.601,72 → 2.601 ·
  Şubat/Mart 2.081,72 → 2.081 · Nisan 1.561,72 → 1.561 · Mayıs 1.041,72 → 1.041
- **T1 dip:** 8.333,76 + 2.080 + 0 + 520 + 3.640 + 3.120 = 17.693,76 →
  **17.693 ₺**, en geç bitiş Mayıs 2027 ✓
- **T5 dip (r1'de düzeltildi):** T5'in referans ayı **Ekim**'dir ve `kalan`
  daima **bu aydan sonrasını** sayar (K-T7). T1'in penceresi Ekim→Mayıs,
  T5'in penceresi Kasım→Mayıs; yani pencereden düşen ay **Ekim**'dir:
  17.693,76 − **2.861,72 (Ekim)** = 14.832,04 → **14.832 ₺**. İlk turdaki
  14.573, Ekim yerine **Eylül'ün 3.120**'sini düşürüyordu; bu yüzden kart
  kendi çubuklarıyla da çelişiyordu (Kasım→Mart çubuklarının toplamı
  12.225 ₺ iken iddia edilen kalan 14.573'tü ve arada yalnız Nisan-Mayıs
  vardı).
- T5 satırları: Telefon 5/12 kalan 7 × 1.041,72 = 7.292,04 → 7.292 ·
  Buzdolabı 6/9 kalan 3 × 520 = 1.560 · Diğer 1.041 + 520 = **1.561** ·
  kahraman 1.561 + 780 + 520 = **2.861** ✓

> **Telefon neden 1.041,72?** 12.500,00 / 12 modeli (1.041,67 / 1.041,66)
> kalan toplamları 17.693 **ve** 14.832 ile aynı anda tutturamıyor: 8
> taksitin kuruş kuyruğu .32, Ekim'in .67 → Ekim sonrası 14.831,69 çıkar.
> Aylık 1.041,72 (banka teklifinin tipik hâli: 12 × 1.041,72 = 12.500,64)
> hem 1.041 ₺ satırını, hem 8.333 ₺ kalanı, hem iki dip toplamını tutturan
> **tek** modeldir. §5.1'deki 12.500,00 örneği açıklayıcı kalır; prototip
> verisi bu tablodur.

> **Dip toplamı, ay çubuklarının toplamı DEĞİLDİR** — ve olmamalı.
> Dip (`taksit.kalan_toplam`) tek bir kuruş toplamından bir kez aşağı
> yuvarlanır; ay çubukları ise **her ay kendi kuruşundan** yuvarlanır
> (§5.1). T1'de Ekim→Mayıs çubuklarının toplamı 17.688, dip 17.693; fark
> 5 ₺ = 8 ayın attığı kuruşlar (8 × 0,72). Bu iki sayı ekranda **yan yana
> gelmiyor** (çubuklar 6 ay gösterir, dip tüm seriyi kapsar), o yüzden
> kullanıcı için çelişki üretmiyor. §5.1.1'in yaprak kuralı **ekranda üst
> üste duran üç düzey** içindir; zaman eksenine uygulanmaz.

#### 5.3.1 Ayrımın garantisi — kural, tesadüf değil (r2'de eklendi)

Yukarıdaki "yan yana gelmiyor" cümlesi dokuz çerçevede **doğrudur** ama
dayanağı veridir: çubuklar içinde bulunulan ayla başlar, `kalan` o ayı
saymaz ve her serinin kuyruğu 6 ayı aşar. Veri değişince dayanak düşer:
kalan ay sayısı **≤ 5 ise** (6 satırın ilki bu ay olduğu için eşik 5'tir)
çubuk kartı kalan **tüm** ayları gösterir ve
iki sayı doğrudan toplanabilir hâle gelir. Kuruş kuyruklu bir seride bu
çelişkidir — ör. 2 × 1.041,72 kalmışsa çubuklar 1.041 + 1.041 = **2.082**,
tek kuruş toplamından yuvarlanan dip **2.083** olur.

> **Bağlayıcı garanti (gösterim kuralı):** *kalan tüm aylar çubuk kartında
> görünüyorsa* `taksit.kalan_toplam` **= Σ(görünen aylar − içinde bulunulan
> ay)** — yani o durumda dip, kuruş toplamından bir kez yuvarlanmaz;
> **ekranda yazan** ay değerleri toplanır, ama **ilk satır toplamın dışında
> kalır.**

İlk satırın dışarıda kalması kuralın parçasıdır, ayrıntısı değil: çubuk
kartı **içinde bulunulan ayla** başlar, `kalan` ise tanımı gereği *bu aydan
sonrası*dır (§5.3, `:436-437`). İlk satır da toplanırsa dip, bu ayın tutarı
kadar şişer — 2 ay kalmışsa Σ(görünen) 3 × 1.041 = 3.123 çıkar, doğrusu
**2.082**'dir. Yani garanti, kapatmak için yazıldığı hatayı yeniden üretir.

Bu, §5.1.1'in yaprak kuralının zaman eksenindeki karşılığıdır ve aynı
gerekçeye dayanır: **ekranda birlikte görünen sayılar birbirini
doğrulamalı.** Kalan aylar çubuk kartına sığmıyorsa (5'ten fazla ay)
eski yol geçerlidir — tek kuruş toplamı, bir kez aşağı yuvarlanır; o
durumda iki sayı farklı pencereleri kapsar ve toplanamaz.

Uygulama notu: koşul `kalan ay sayısı ≤ çubuk kartının gösterdiği ay
sayısı − 1` — çubuk kartı bugün **6** satır gösteriyor, ilki bu ay olduğu
için eşik **5**'tir. `surenSeriler`ın zaten yaptığı geçişte bilinen bir
değer, yeni veri alanı istemez. Prototipin dokuz çerçevesinde koşul
**hiçbir yerde** sağlanmıyor (en kısa kuyruk T3'te 7 ay), bu yüzden
ekrandaki sayılar değişmedi.

**B) T4 / T9 — tek kategori (Diğer), sekiz seri**

| Seri | Aylık | Eylül'deki no | Son taksit | Kalan (Eylül sonrası) | Satırda |
|---|---|---|---|---|---|
| Mutfak yenileme | 104.167,00 (toplam 1.250.004) | 1/12 | **Ağustos 2027** | 11 × 104.167 = **1.145.837** | görünür |
| Telefon | 1.041,72 | 4/12 | Mayıs 2027 | 8.333,76 → **8.333** | görünür |
| Kanepe takımı | 833,00 (toplam 4.998) | 2/6 | Ocak 2027 | 4 × 833 = **3.332** | görünür |
| Buzdolabı | 520,00 | 5/9 | Ocak 2027 | **2.080** | görünür |
| Bisiklet | 375,00 | 8/12 | Ocak 2027 | 4 × 375 = **1.500** | görünür |
| Elektrikli süpürge | 259,00 | 6/6 | Eylül 2026 | 0 | görünür |
| Kulaklık | 120,00 | 2/6 | Ocak 2027 | 4 × 120 = **480** | *gizli* |
| Su arıtma filtresi | 75,00 | 2/6 | Ocak 2027 | 4 × 75 = **300** | *gizli* |

- Kahraman: görünen 6 satır 104.167 + 1.041 + 833 + 520 + 375 + 259 =
  107.195, gizli iki ürün 120 + 75 = 195 → **107.390 ₺** ✓
- Ay çubukları: Eylül 107.390,72 → **107.390** · Ekim…Ocak 107.131,72 →
  **107.131** (süpürge Eylül'de düştü; Bisiklet, Buzdolabı, Kanepe,
  Kulaklık ve Filtre **Ocak'ta** biter) · Şubat 107.131,72 − 1.923 =
  105.208,72 → **105.208**
  *(r1: ilk turda Kasım 106.756 ve Ocak 106.236 yazıyordu; ikisi de
  "Bisiklet 8/12" ve "Buzdolabı 5/9" satırlarıyla — yani serilerin Ocak'ta
  bittiğiyle — çelişiyordu.)*
- **T4 dip:** 1.145.837 + 8.333,76 + 3.332 + 2.080 + 1.500 + 0 + 480 + 300
  = 1.161.862,76 → **1.161.862 ₺**. Dip satırı sekiz serinin **tamamını**
  kapsar; ilk turdaki 1.161.078 yalnız görünen altı satırı topluyordu
  (gizli 780 ₺ dışarıda kalmıştı).
  → Denetim raporu bu değeri **1.161.858** olarak hesaplamıştı; o sayı
  Mutfak yenileme'nin kalanını 1.145.833 kabul ediyor. 1.145.833, satırda
  yazan 104.167 ₺ ile **bağdaşmaz**: aşağı yuvarlamada 104.167 görünmesi
  için aylık ≥ 104.167,00 olmalı, o hâlde 11 taksitin kalanı 1.145.837'dir
  (1.145.833 yalnız 1.250.000/12 = 104.166,67 modelinde çıkar, o da satırı
  **104.166** yapardı). Dört sayı arasındaki 4 ₺ fark buradan gelir ve
  bilinçlidir.
- Çubuk oranı = `round(ay / en büyük ay × 100)` → 100/100/100/100/100/98.
  Tek seri baskın olduğunda çubuklar **düzleşir**; bu bir hata değil,
  ölçeğin doğru sonucudur — ayrımı sağdaki sayı taşır. Ölçek sıfırdan
  değil **en büyük aydan** kurulur (T1/T5 ile aynı kural).

**C) T3 — tek seri:** Sağlık taksidi 520,00 · 3/10 · son taksit Nisan 2027
· kalan 7 × 520 = **3.640 ₺** · altı ay çubuğu da 520 ₺ (hepsi %100).

---

## 6. Silme akışı — yeni hiyerarşide nerede duruyor

**Ürün satırında silme YOK.** Ne düğme, ne kaydırma eylemi.

| Adım | Yüzey |
|---|---|
| 1 | Ürün satırına dokun → **E-12 harcama detayı** (o ayın taksit kaydı) |
| 2 | E-12'de `detay.taksit_bilgi` "{mevcut}/{toplam} taksit · her ay {tutar}" + `detay.sil_taksit` "Taksit serisini sil" |
| 3 | **E-13 onay diyaloğu**: "Bu taksit serisi silinecek" · "Kalan {adet} taksit de silinecek. Geri alınamaz." · Sil / Vazgeç |
| 4 | Toast: "Taksit serisi silindi." — **geri al yoktur** (K-029) |

**Gerekçe:** K-029'un ölçütü "yüksek etkili + geri alınamaz". Geri
alınamaz bir eylem, gezinme amaçlı bir ekranda **tek dokunuş** uzakta
olamaz. Kaydırarak silme de bu ekranda kullanılmaz: (a) satır bir kayıt
değil bir **seri**dir, (b) akordiyon içinde yatay kaydırma dikey kaydırma
ile yarışır, (c) `tokens.md` §7.3'ün kaydırma eylemi E-14 listesine aittir.
Böylece `danger` rengi bu ekranda **hiç görünmez** — mekanik denetim de
bunu doğruluyor (0 bulgu).

**Satırda `chevron-right` VARDIR** (20pt, `text-2`) — r1'de eklendi. İlk
turun gerekçesi ("sağ sütun tutarın ve tutar kırpılmaz") geçersizdi: ok
tutarın **sağına** girer ve 32pt'yi `flex:1` olan ad sütunundan alır, tutar
`flex:0 0 auto` olduğu için tek piksel kaybetmez. Asıl sorun
keşfedilebilirlikti: satır artık ilerleme çubuğu + iki sayı taşıyan bir
**veri bloğu** gibi okunuyor ve dokunulabilir olduğunu söyleyen tek işaret
basılı durumdu — yani kullanıcı ancak **denedikten sonra** öğreniyordu.
Uzun ürün adı zaten `tek-satir` ile kırpıldığı için 32pt kayıp kabul
edilebilir; kategori ikon kabının satırdan düşmesiyle (§4.2) ada net 24pt
**kazanç** kaldı.

---

## 7. Durum matrisi (tamamı prototipte çizili)

| Durum | Görünüm | Çerçeve |
|---|---|---|
| **Dolu · çok kategori** | Toplam + akordiyonlar (en büyüğü açık) + ay kartı | T1 |
| **Basılı · akordiyon dili** | Kapalı kabın tamamı çöker (`groove`+`clay.pressed`) · açık bölümdeki **kuyu** satır çöker | T2 |
| **Basılı · akordiyonsuz düzen** | **Kabarık** satır çöker (`.satir-kart.basili`) · **"Tümünü göster"** çöker (`.btn-ghost.basili` → `well`+`clay.pressed`) | **T9** |
| **Tek seri** | Akordiyon yok · kabarık satır (ikon kabı **yok**) · bölüm başlığı akordiyon başlığının yapısını alır: 44pt ikon kabı + `h2` **"Sağlık"** + sağda "1 ürün"; ok yok, "Süren taksitler" başlığı düşer (§4.2) | T3 |
| **Ürün adı yok** | "{Kategori} taksidi" | T3 |
| **Tek kategori · çok seri** | Akordiyon yok · başlık: kab + `h2` **"Diğer"** + "8 ürün" (tutar yazılmaz, kahraman sayının kendisi) · 6 satır + "Tümünü göster" | T4 · T9 |
| **Liste sınırı** | 6 satır, tek yönlü açma, başlıktaki sayı gerçeği söyler ("**8 ürün**"); gizli iki ürün kahraman sayıya ve dip toplamına **dahil** | T4 |
| **Uzun ürün adı** | Tek satırda kırpılır (`tek-satir`), tutar ve ok kırpılmaz | T4 · T9 |
| **Yedi haneli tutar** | "1.145.837 ₺" ikincil satırda tam yazılı, taşma yok | T4 · T9 |
| **Son taksit bu ay** | Çubuk %100 · "Son taksit bu ay" (`primary-text`) · kalan yazılmaz | T1 · T4 |
| **Bitmiş seri** | Listeden **düşer** (ekran süren yükü gösterir) | — |
| **Geçen ay bitmiş seri** | En altta `serit-info`: "{Ürün} taksidi {ay} ayında bitti. Aylık yük {tutar} düştü." | T5 |
| **Gelecek aylara sarkan seri** | Ay kartı 6 ay gösterir; serinin gerçek bitişi dip satırında ("Sonuncusu Mayıs 2027…") | T1 |
| **Boş (taksit yok)** | v4'ten aynen: 176pt çukur disk + `calendar-clock` + "Taksitli işlem yok". Kırılım için **ikinci** boş durum üretilmedi | T6 |
| **Yükleniyor** | İskelet gerçek düzeni tutar: 1 açık bölüm (2 satır) + 2 kapalı bölüm + 6 ay satırı. **Kategori adı da bloktur** (yüklenmeden bilinmiyor). Bölüm başlığı için **25pt** ayrılır (r3): iskelet akordiyonlu, yani **çok kategorili** düzeni tahmin ediyor ve çizdiği düzenin yüksekliğini ayırıyor. Tek kategori çözülürse başlık 44'e büyür ve liste **19px aşağı oturur** — kabul edilmiş (§4.2). ≥150ms sonra gösterilir | T7 |
| **Ağ hatası** | Tek okuma yolu → tek hata yüzeyi: 96pt `hata-daire` + "Taksitler açılamadı" + "Yeniden dene" | T8 |
| **Kısmi hata** | **Yok ve uydurulmadı.** Üç düzeyin tamamı aynı `Promise.all` okumasından gelir | — |
| **Pasif / kilitli bölüm** | Yok | — |

---

## 8. Erişilebilirlik

| Öğe | Karar |
|---|---|
| Akordiyon başlığı | `accessibilityRole="button"` + `accessibilityState={{ expanded }}` · etiket **"{Kategori}. {özet}"** ("Giyim. 780 ₺, 2 ürün") — özet açıkken görsel olarak gizlenir ama **etikette kalır** |
| Ürün satırı | `accessibilityRole="button"` · etiket "Telefon. Bu ay 1.041 ₺. 4. taksit, 12 taksitten. Kalan 8.333 ₺. Ayrıntıyı aç" · son taksitte "…Son taksit. Ayrıntıyı aç" |
| Satırın `chevron-right`'ı | Dekoratif: `aria-hidden` / RN'de `importantForAccessibility="no"`. "Ayrıntıyı aç" zaten etiketin sonunda — ok ikinci kez okunmaz |
| İlerleme çubuğu | `importantForAccessibility="no-hide-descendants"` — satır etiketinde "4. taksit, 12 taksitten" zaten geçiyor, ikinci kez okunması gürültü. `progressbar` rolü bu üründe **kahraman göstergeye** ayrılmıştır (`tokens.md` §6) |
| Kategori kimliği | Renk **tek başına** taşımıyor: `.kat-kab` içinde kategori ikonu + `h2` kategori adı + etiket metni |
| Dokunma hedefleri | Akordiyon başlığı 326 × ≥44 · ürün satırı 326 (ya da 358) × 86 · "Tümünü göster" tam genişlik × 44 · geri düğmesi 44 × 44 |
| Kapalı bölüm | İçerik **mount edilmez** → ekran okuyucu görmez, `expanded:false` ile tutarlı |
| Odak halkası | **Bu prototipte çizilmedi** — dürüst kayıt: HTML'de `:focus-visible` kuralı yok. RN'de `:focus-visible` karşılığı yoktur; klavye/harici anahtar erişimi tüm prototipleri ilgilendirdiği için **PM koordinasyonunda ayrı iş** olarak açıldı (r1 kapsamı dışı). Tasarım kararı değişmedi: geldiğinde 2pt `primary-text`, radius + 4 |
| Tabular rakam | Tutarlar, "4/12" ve özetler `.num` (`tabular-nums`) |
| Reduce motion | Akordiyon açılışı ve ok dönüşü 0ms |
| Safe area | Üstte `insets.top`, altta içerik boşluğu 24; ekran push olduğu için sekme çubuğu yok |

---

## 9. Metinler

Tam liste ve anahtar önerileri `docs/content/metinler.md` **§30**'a
eklendi (mevcut bölümler değiştirilmedi). Özet:

| Anahtar | Değer | Durum |
|---|---|---|
| `taksit.seriler_baslik` | **Süren taksitler** | Değişti · **PM onayladı**; `metinler.md` §22.3'teki eski satır da güncellendi (aynı dosyada iki değer kalmadı). **r2:** yalnız **çok kategorili** düzende çizilir (§4.2) |
| `taksit.ozet_kategorili` | **{kategori} kategori · {adet} ürün** | Yeni · r1'de düzeltildi |
| `taksit.ozet_tek_kategori` | **{adet} ürün** | Yeni · **r2'de düzeltildi**: kategori adı artık başlığın `h2`'si (§4.2), özet yalnız sayıyı taşır — aynı adı iki kez yazmaz |
| `taksit.kategori_ozet` | {tutar} · {adet} ürün | Yeni |
| `taksit.seri_kalan` | {mevcut}/{toplam} · kalan {tutar} | Yeni |
| `taksit.urun_yok` | {kategori} taksidi | Yeni |
| `taksit.tumunu_goster` | Tümünü göster | Yeni |
| `taksit.seri_bitti_urun` | {urun} taksidi {ay} ayında bitti. Aylık yük {tutar} düştü. | Yeni |
| `hata.okuma.taksit` | Taksitler açılamadı | Yeni |
| `taksit.son_taksit` | Son taksit bu ay | Mevcut, rengi düzeltildi |

**r1 düzeltmesi (Ö1) — "seri" sözcüğü arayüzden çıktı.** İlk turda bölüm
başlığı "6 seri · 3 kategori", 8px altındaki özetler "3 ürün / 2 ürün /
1 ürün" diyordu: **aynı nicelik iki farklı adla**, üstelik "seri" bir
geliştirici sözcüğü. Artık her iki yüzey de **ürün** sayar:

```
Süren taksitler            3 kategori · 6 ürün      ← bölüm başlığı
  Diğer                    1.820 ₺ · 3 ürün         ← kategori özeti
  Giyim                    780 ₺ · 2 ürün
  Sağlık                   520 ₺ · 1 ürün           3 + 2 + 1 = 6 ✓
```

Tek kategorili düzende (akordiyon kurulmaz, §4.2) başlığın kendisi
kategoriye dönüşür — jenerik başlık ve kategori tutarı düşer:

```
[kab] Diğer                             8 ürün      ← bölüm başlığı (44pt)
      Mutfak yenileme            104.167 ₺          ← satırlar, kab YOK
      …
```

"Seri" sözcüğü arayüzde yalnız **silme/detay** bağlamında kalır (E-12
`detay.sil_taksit` "Taksit serisini sil", E-13 onayı, `toast.taksit_silindi`)
— orada silinen şey gerçekten tek bir ay değil, serinin tamamıdır ve
sözcük bu farkı taşımak için gerekli.

Ton denetimi: ünlem yok · emoji yok · övgü yok · en uzun arayüz cümlesi
9 kelime · teknik sözcük yok · "seri bitti" cümlesi kutlama değil olgu.

---

## 10. Anti-pattern öz-denetimi (madde madde)

| Madde | Uyum |
|---|---|
| Mor-mavi varsayılan gradyan | Palet `tokens.md` §1'den; ekranda gradyan yalnız `grad.action` (ay çubuğu dolgusu) ve `grad.clay-face`. Denetim: palet dışı renk 0 |
| Her elemanda glassmorphism | Cam/blur yok; derinlik clay gölge katmanlarıyla |
| Amaçsız drop-shadow | Gölge **yükseklik anlatıyor**: kart `raised` → akordiyon `raised` → içindeki satır `sunken`. Üç basamak, üç anlam |
| Karışık köşe yarıçapı | Yalnız 16 (satır, ikon kabı) · 24 (kart, akordiyon) · 32 (kahraman kart) · 999 (çubuk, düğme). Denetim: radius dışı 0 |
| Inter / Poppins / Montserrat keyfî | Montserrat + Poppins `tokens.md` §2.1'de `₺` glifi ölçülerek kilitlendi; bu turda font kararına dokunulmadı |
| 3 sütunlu "daire ikon + başlık + 1 cümle" | Yok. Kategori ikonu **köşeli-yumuşak 44 kap** (daire değil) ve tek bir **başlıkta** durur (r1: satırlarda tekrarlanmıyor); sütun düzeni yok, tek kolon liste |
| Stok illüstrasyon | Yok; boş durum diski token geometrisi (176pt çukur yay) |
| Kimliksiz aşırı beyaz boşluk | Boşluklar §3.1 ritim setinden (4/8/12/16/24); ilk kat 769'un 785'i dolu |
| Jenerik pazarlama dili | "Süren taksitler", "Son taksit bu ay", "kalan 8.333 ₺" — olgu cümleleri. Övgü/motivasyon yok |
| Düşük kontrastlı gri metin | `text` 16.15:1 · `text-2` ≥4.56:1 · `primary-text` 5.92:1; `text-3` bu ekranda **hiç kullanılmadı** |
| Rastgele boşluk | Denetim `padding/margin` için izinli küme dışında 0 bulgu |
| Dark mode'un otomatik ters çevrilmesi | Karanlık mod Faz 2; bu turda üretilmedi (`tokens.md` §11) |
| **RN kısıtları** | `:hover` yok (basılı durum T2 **ve T9**'da çizili: dört ayrı hedef) · CSS grid yok · `::before/::after` yok · `calc/vh/vw/z-index` yok · gölge `boxShadow` dizeleriyle · uzun liste `FlatList` · dokunma hedefi ≥44. Denetim: yasak dize 0 |

---

## 11. Bileşen envanteri deltası

| Bileşen | Durum | Not |
|---|---|---|
| `InstallmentSeriesRow` | **Yeni varyant** (yeni bileşen değil) | `.satir-kart`ın iki hâli, r1'den sonra **tek** yapı: farkı yalnız yüzey basamağı — `kuyu` (akordiyon içinde) · kabarık (akordiyon kurulmadığında). İkisinde de ikon kabı **yok**, ikisinde de sağda 20pt `chevron-right` **var**. İçinde `.cubuk-oluk`/`.cubuk-dolgu` |
| `CategoryAccordion` | **Mevcut `Accordion`** | Tek delta: başlıkta `.kat-kab`. `stil-rev2.css` §9'a satır eklenmedi |
| `SectionHeader` | **Yeni varyant** | Tek kategorili düzende akordiyon başlığının yapısını alır: 44pt `.kat-kab` + `h2` **kategori adı** + "{adet} ürün", ok **yok** (§4.2) — mevcut `.pad.aralik` + `.kat-kab`, yeni sınıf yok. Çok kategoride `h2` "Süren taksitler" + "{n} kategori · {n} ürün" |
| `ListMoreRow` ("Tümünü göster") | `button.ghost` tam genişlik | `stil-rev2.css` §6 ile aynı hizalama deseni |
| `MonthLoadRow` | Değişmedi | Yalnız konumu bir blok aşağı indi |
| `InfoStrip` | Değişmedi | Metni ürün adı taşıyor |
| `ClaySurface` · `PushHeader` · `Skeleton` · `ErrorState` | Değişmedi | — |
| `_uret/lib.py` | **Yalnız ekleme**: `pill` (Sağlık ikonu) + `refresh` (hata durumu) — ikisi de kilitli Lucide setinden, v4 prototipinde zaten kullanılıyordu. Yeni glif çizilmedi |
| **`stil-rev2.css` §13** | **AÇILMADI** | r1'de de açılmadı: `chevron-right` mevcut `.ikon-kutu` ile, basılı hâller mevcut `.satir-kart.basili` / `.btn-ghost.basili` ile çizildi |

---

## 12. Kararlar tablosu

| # | Karar | Gerekçe | Nerede |
|---|---|---|---|
| **K-T0** | Ekran **ay bazlı yapılmadı** | Ekranın işi ileri bakmak; geçmiş ay E-14/E-16'nın işi; "kalan" geçmiş ayda anlamsızlaşır | §1.1 |
| **K-T1** | Kırılım, ay haritasının **üstüne** çıktı | v4 sırasında akordiyon 568'de başlar, 769'daki kesme **ikinci ürün satırının ortasından** geçerdi (738-824) → K-057/8 ihlali. Ayrıca zaman mantığı (şimdi → ayrıntı → gelecek) ve olgu-tahmin sırası | §2.1-2.2 |
| **K-T2** | Kategori sayısı 1 ise **akordiyon kurulmaz** | Tek çocuklu kap yalnız dokunuş maliyeti. Kategori kimliği **yalnız bölüm başlığına** taşınır (r1: satırdaki ikon kabı düşürüldü — aynı glif altı kez tekrarlanıyordu ve §4'ün kendi gerekçesiyle çelişiyordu). **r2:** bölüm başlığı akordiyon başlığının **yapısını** alır (kab + `h2` kategori adı + "{adet} ürün"); jenerik "Süren taksitler" başlığı bu düzende düşer, kab böylece kategori adının yanında ve akordiyon-başlığı bağlamında kalır | §4.2 |
| **K-T3** | Satırda birincil = **ürün adı + bu ayki tutar**; bitiş ayı ve "her ay" çıkarıldı | Dört ikincil veri satırı bilgi çöplüğü; bitiş `{no}/{toplam}` + dip satırından okunur | §3 |
| **K-T4** | İlerleme **seri düzeyinde**, kategori düzeyinde **yok** | İlgisiz serilerin ortalaması anlam taşımaz | §3 |
| **K-T5** | Çubuk dolgusu **kategori `solid` rengi** | `tokens.md` §1.4 "kategori çubuğu dolgusu" izinli; mavi dolgu `cat.mavi` ile çakışırdı | §3 |
| **K-T6** | "Son taksit bu ay" rengi `warning-ink` → **`primary-text`** | `warning` ailesi yalnız limit dışı (§1.3); son taksit limit aşımı değil | §3 |
| **K-T7** | `kalan` = **bu aydan sonrası**, kuruş toplamıyla | Bu ayki tutar satırda ve toplamda zaten var; `aylık × adet` çarpımı kuruş sapması üretir | §5 |
| **K-T8** | Bitmiş seriler **listelenmez**; geçen ay bitene bilgi şeridi | Ekran süren yükü gösterir. Arşiv ihtiyacı E-14'te karşılanır | §7 |
| **K-T9** | Silme **satırda değil**, E-12 → E-13 zincirinde | K-029: geri alınamaz eylem gezinme ekranından tek dokunuş uzakta olamaz | §6 |
| **K-T10** | Kategori içi sınır **6 satır** + tek yönlü "Tümünü göster" | İlk kat okunurluğu + `FlatList`; tek yönlü olması kaydırma konumunu korur | §4.3 |
| **K-T11** | `urunAdi` boşsa "{Kategori} taksidi" | Adsız satır ya da uydurma ad yerine doğrulanabilir yedek | §5 |
| **K-T12** | Kısmi hata durumu **üretilmedi** | Üç düzey tek okumadan gelir; olmayan bir hata hâli tasarlamak yanlış vaat | §7 |
| **K-T13** | Yuvarlama **yaprakta**: kategori = Σ satır(görünen), ay = Σ kategori(görünen); gösterimde **kuruş atılır** | Σ(yuvarlanmış) ≠ yuvarla(Σ); ekranın tek kazancı üç düzeyin toplanabilirliğiydi. Yön `tokens.md` §14.2/6 ile aynı | §5.1.1 |
| **K-T14** | Satıra 20pt **`chevron-right`** eklendi | Satır veri bloğu gibi okunuyordu, dokunulabilirliği yalnız basılı durum söylüyordu; ok 32pt'yi esneyen **ad** sütunundan alır, tutardan almaz | §3 · §6 |

### PM kararı gereken noktalar

1. ~~`taksit.seriler_baslik` metin değişikliği~~ — **PM onayladı** ("Süren
   taksitler"). `metinler.md` §22.3 ve §30.1 birlikte güncellendi; "seri"
   sözcüğü arayüzde yalnız silme/detay bağlamında kaldı (§9).
2. **Geçmiş aylara bakma** ihtiyacı: bu turda kapsam dışı (K-T0). Gerekirse
   E-18'e ay seçici değil, **E-16 Özet'e taksit süzgeci** olarak açılmalı.
3. **`SurenSeri` türüne `urunAdi` + `kalanKurus` eşlemesi** — yeni veri
   alanı değil, var olan `urun_adi` ve mevcut tam liste geçişinin
   kullanılması. `frontend-developer` bunu ek istek olmadan yapabilir;
   PM'in bilmesi yeterli.

---

## 13. Kapanan bulgular

### 13.0 REV3-r3 (üçüncü REVİZE turu: 1 bloklayıcı + 1 önemli + 3 cümle)

> Üçüncü tur r2'nin dört maddesinden ikisinin **kendi içinde hata ürettiğini**
> gösterdi. Ekrandaki hiçbir sayı ve hiçbir görsel karar değişmedi;
> `taksitler.html` yalnız T7 iskeletindeki yükseklik için yeniden üretildi.

| # | Bulgu | Ne yapıldı | Nerede |
|---|---|---|---|
| **B7** (bloklayıcı) | r2'nin §5.3.1 garantisi **bir ay fazla sayıyordu**: `Σ(görünen ay değerleri)` literal alındığında çubuk kartının **ilk satırı = içinde bulunulan ay** de toplama giriyor, ama `kalan` tanımı gereği o ayı saymaz (§5.3). 2 ay kalmışsa kural 3 × 1.041 = **3.123** üretir, doğrusu **2.082** — yani B6'nın kapattığı hata sınıfı kuralın içinden geri giriyordu. Koşul da iki yerde çelişikti (bir yerde ≤5, bir yerde "≤ gösterilen ay sayısı = 6") | Formül **`kalan_toplam = Σ(görünen aylar − içinde bulunulan ay)`**; koşul **`kalan ay sayısı ≤ gösterilen ay sayısı − 1`**, bugünkü 6 satırlı çubuk kartı için eşik **5**. İki geçiş (garanti bloğu + uygulama notu) tek ve tutarlı hâle getirildi, ilk satırın neden hariç olduğu kuralın gövdesine yazıldı. Koşul dokuz çerçevenin **hiçbirinde** sağlanmıyor (en kısa kuyruk T3'te 7 ay) → **ekrandaki sayılar değişmedi** | **§5.3.1** |
| **Ö5** (önemli) | r2'nin R1 rötuşu zıplamayı **taraf değiştirtti**: T7 iskeleti bölüm başlığına 44pt ayırıyor ama hemen altına üç **akordiyon** çiziyordu, yani çok kategorili düzeni tahmin ediyordu — o düzende gerçek başlık 25'tir ve yüklenince başlık **19px yukarı** zıplıyordu. Gerekçe simetrik: 44 ayırmak tek kategoriyi kurtarıp çok kategoriyi bozuyor | Seçenek **(b)** seçildi: iskelet çizdiği düzenin (çok kategori) yüksekliğini ayırır → `height:44px` kaldırıldı, başlık yine **25**. Tek kategori çözülürse 19px **aşağı oturma** olur ve §4.2'de *kabul edilmiş* olarak yazıldı; yön aşağı olduğu için okunan başlık yerinde kalıyor, ayrıca zıplama nadir dalda. `SectionHeader`'a evrensel `min-height:44` **verilmedi** (T1'in §2.2 zincirini +19 kaydırır, 769'daki kesmeyi kapalı akordiyon başlığının içine sokardı) | üreteç T7 · §4.2 · §7 |
| **C1** (cümle) | §2.2'nin "bölünen glif yok" iddiası **em kutusu** varsayımına dayanıyordu; gerçek satır kutusunda 16pt adın descender'ı (T4 6. satır "Elektrikli süpürge" → p, g) ~**769,7**'ye iniyor | Yumuşatıldı: *glif gövdesi tam, alt çıkıntı kuyruğunun son ~1pt'si sıyrılabilir*; harf tanınırlığı etkilenmiyor. 6. satırı 3pt yukarı alan alternatif yazıldı ama 86+8 ritmini bozduğu için **yapılmadı** | §2.2 |
| **C2** (cümle) | §4.2'deki *"kab akordiyon başlığı bağlamında kalır, `bg` üstüne çukur kap üretilmez"* cümlesi **olgusal olarak yanlıştı** — kab gerçekten `bg` üstünde | Cümle gerçeği anlatacak şekilde yazıldı: kab `bg` üstünde duruyor, görsel sonuç **kabul edildi** — `clay.sunken` yalnız `inset` gölge tanımlar (altındaki yüzeyin kabarıklığına yaslanmıyor) ve `cat.*.soft` dolgusu `bg` hue'suyla aynı değil. v4'ün kapsamadığı komşuluğun bilinçli **genişletmesi** olarak işaretlendi | §4.2 |
| **C3** (cümle) | Tek kategorili başlığın "dokunulabilir sanılması" endişesi reddedildi, gerekçe eksik yazılmıştı (ayrım yalnız `chevron` yokluğuna bağlanmıştı) | Gerekçeye **kartsızlık** eklendi: bu dilde dokunulabilirliğin taşıyıcısı **kabarık kart** — akordiyon daima `surface` + `clay.raised` + radius-24 kart ve içi `<button>`; yeni başlık kartsız, doğrudan `bg` üstünde ve `<button>` değil. Ok yalnız teyit | §4.2 |

### 13.0 REV3-r2 (ikinci REVİZE turu: 1 bloklayıcı + 1 önemli + 2 rötuş)

> İkinci tur r1'in sekiz maddesini **kapanmış** saydı ve sayıları bağımsız
> doğruladı; aşağıdaki dört kalem dışında hiçbir şeye dokunulmadı.

| # | Bulgu | Ne yapıldı | Nerede |
|---|---|---|---|
| **B5** (bloklayıcı) | Tek kategorili düzende kategori glifi 358px'lik satırın **sol** ucunda, kategori adı **sağ** ucunda, aralarında ilgisiz bir `h2` ("Süren taksitler") duruyordu → K-T2'nin kendi kuralı ("kimlik **en yakın** başlıkta") ihlal; aynı bileşen 8px arayla iki anlam; `clay-sunken` 44pt kap doğrudan `bg` üstünde (v4'te örneği yok, `tokens.md` §1.9/§5 kapsamıyor) | Bölüm başlığı T1'in **akordiyon başlığıyla aynı yapıya** oturtuldu: `.kat-kab` + `h2` **kategori adı** + sağda "{adet} ürün". Jenerik başlık **düştü** (K-T2 işi kategoriye devrediyor), kategori tutarı da yazılmıyor (kahraman sayının kendisi), ok yok (açılmıyor). Kab yine akordiyon-başlığı bağlamında yaşıyor → `bg` komşuluğu ortadan kalktı. Üreteçte tek nokta: `bolum_basi`; T3/T4/T9 yeniden üretildi | §4.2 · §7 · §9 · §11 · üreteç `bolum_basi` + T3/T4/T9 |
| **B6** (önemli) | "Dip ≠ çubuk toplamı" ayrımı dokuz çerçevede tutuyordu ama dayanağı **veri tesadüfü**ydü: kalan ay ≤5 **ve** kuruş kuyruklu bir seride iki sayı doğrudan karşılaştırılabilir hâle gelip çelişirdi (2 × 1.041,72 → çubuklar 2.082, dip 2.083) | Garanti **kural** olarak yazıldı: *kalan tüm aylar çubuk kartında görünüyorsa* `kalan_toplam` **= Σ(görünen ay değerleri)**. Koşul sağlanmıyorsa eski yol (tek kuruş toplamı, bir kez aşağı yuvarlama) geçerli. Prototipte koşul hiçbir çerçevede sağlanmıyor (en kısa kuyruk T3'te 7 ay) → **sayılar değişmedi** | **§5.3.1** |
| **R1** (rötuş) | T7 iskeleti bölüm başlığına 25pt ayırıyordu; tek kategori çıkarsa başlık 44'e büyür → 19px zıplama | İskelet satırı **44pt** ayırıyor (`.pad.aralik` + `height:44px`) — **r3'te geri alındı**, bkz. Ö5: bu düzeltme zıplamayı çok kategorili dala taşıyordu | üreteç T7 · §7 |
| **R2** (rötuş) | T4/T9'da 769'daki kesmenin **hangi parçaya** girdiği yazılı değildi | §2.2'ye parça tablosu eklendi: üst iç boşluk ve **ad + tutar metni tam** (em kutuları 752-768 / 751,5-768,5), kesilen 3pt satır **aralığı**; çubuk ve ikincil satır **görünmez**. Yani kesilen katman ikincildir, bölünen bir glif yok | §2.2 |

### 13.1 REV3-r1 — kapanan bulgular

> Denetim raporu: `design-reviewer` REVİZE turu (4 bloklayıcı + 3 önemli).
> Delta denetimi bu tabloyu izleyebilir.

| # | Bulgu | Ne yapıldı | Nerede |
|---|---|---|---|
| **B1a** | İlk kat 766 yazılıyordu; E-18 push ekranı, sekme çubuğu yok | Tüm geçişler **769** (= 844 − 47 durum çubuğu − 28 ana çubuk); türetme tek kaynak hâline getirildi, 693 değerinin bu ekrana uymadığı yazıldı | §2.1 (ölçü bloğu) · §2.2 · §10 · üreteç başlığı + T1 notu |
| **B1b** | K-T1'in "832px'te başlardı, hiç görünmezdi" gerekçesi uydurma | Gerekçe gerçek sayılarla yeniden yazıldı: v4 sırasında akordiyon **568**'de başlar, 769'daki kesme **ikinci ürün satırının** (738-824) ortasından geçerdi → K-057/8. Zaman mantığı ve olgu-tahmin gerekçeleri korundu | §2.1 · §12 (K-T1) |
| **B1c** | Mevcut sıralamada kesme bir nesnenin ortasından geçmiyor | Karar değişmedi, yalnız ölçü düzeltildi: 725-769 başlık bloğu tam, kesilen tek şey 16pt alt iç boşluk | §2.2 |
| **B2** | "Kategori toplamları = ay toplamı **daima** eşit" matematiksel olarak yanlıştı; kırpma/yuvarlama yönü ilan edilmemişti | Bağlayıcı kural: **yuvarlama yaprakta**, üst düzeyler **görünen** değerleri toplar. Yön tek cümleyle ilan edildi: **kuruş atılır** (`// 100`, `tokens.md` §14.2/6 ile aynı yön). "Önce yuvarlayıp sonra toplamak yasak" satırı bu ekran için tersine çevrildi; bedeli ve gizli satırların toplama dahil olduğu yazıldı | §5 tablo · **§5.1.1** · §2 · §12 (K-T13) |
| **B3.1** | T4 ay kartı: Kasım 106.756 · Ocak 106.236, üstteki satırlarla çelişiyordu | **Kasım 107.131 · Aralık 107.131 · Ocak 107.131 · Şubat 105.208**. Serilerin bitiş ayları (Bisiklet 8/12, Buzdolabı 5/9, Kanepe 2/6 ve iki gizli ürün → **Ocak 2027**) tabloya yazıldı | §5.3-B · üreteç `AYLAR_TEK` |
| **B3.2** | T4 dip yalnız görünen 6 satırı kapsıyordu (1.161.078) | Dip artık sekiz serinin tamamı: **1.161.862 ₺**. Denetim raporunun 1.161.858'inden 4 ₺ fark, Mutfak yenileme kalanının düzeltilmesinden gelir (1.145.833 → **1.145.837**): 104.167 ₺ satırı ile 1.145.833 aşağı yuvarlamada bağdaşmıyor, hesabı §5.3-B'de açık | §5.3-B · üreteç `DIP_TEK` |
| **B3.3** | T5 dip 14.573 ₺: `kalan` penceresinden Ekim yerine Eylül düşürülmüştü | **14.832 ₺** = 17.693,76 − **2.861,72 (Ekim)**; T5'in referans ayı Ekim, penceresi Kasım→Mayıs. Telefon serisi aylık **1.041,72**'ye oturtuldu — 1.041 ₺ satırını, 8.333 ₺ kalanı ve iki dip toplamını aynı anda tutturan tek model | §5.3-A · üreteç `DIP_DUSMUS` |
| **B4** | "Tümünü göster" basılı durumu hiçbir çerçevede çizilmemişti; not "üç hedef" diyip ikisini sayıyordu | **T9 eklendi** (9. çerçeve): kabarık satır basılı + "Tümünü göster" basılı. T2'nin notu "iki hedef"e çekildi ve T9'a yönlendirildi; durum matrisi iki ayrı satıra bölündü | §7 · T2/T9 notları |
| **Ö1** | Aynı nicelik iki adla ("6 seri" ↔ "3 ürün"), "seri" geliştirici sözcüğü | `taksit.ozet_kategorili` = **"{kategori} kategori · {adet} ürün"**, `taksit.ozet_tek_kategori` = **"{kategori} · {adet} ürün"** *(r2'de **"{adet} ürün"**'e indi: kategori adı başlığın `h2`'si oldu, §4.2)*. `taksit.seriler_baslik` = **"Süren taksitler"** (PM onaylı); `metinler.md` **§22.3 ve §30** birlikte güncellendi | §9 · `metinler.md` §22.3/§30 |
| **Ö2** | K-T2, §4'ün kendi gerekçesini çürütüyordu (aynı glif 6 kez); WCAG gerekçesi tutmuyordu | Kural tekleştirildi: **kategori kimliği en yakın başlıkta durur, satırda asla tekrarlanmaz.** Tek kategoride 44pt ikon kabı **bölüm başlığının soluna** taşındı; satırlar kabarık kaldı, ikon kabı düştü | §4 tablo · §4.2 · §12 (K-T2) |
| **Ö3** | Satır → E-12 geçişinin keşfedilebilirliği savunulamıyordu | **20pt `chevron-right` eklendi** (her iki satır varyantına). Eski gerekçe ("tutarı kırpar") yanlış olduğu yazılarak düzeltildi; ok 32pt'yi esneyen ad sütunundan alır, ikon kabının düşmesiyle ada net 24pt kaldı | §3 · §6 · §12 (K-T14) |
| **Ö4** | Odak halkası prototipte yok ama §8 "kaldırılmadı" diyordu | İddia **dürüstçe düzeltildi**; CSS'e dokunulmadı (tüm prototipleri ilgilendiren ayrı iş, PM takibinde) | §8 |

### Bilinçli olarak YAPILMAYANLAR (PM takibi)

| Konu | Neden bu turda değil |
|---|---|
| `:focus-visible` odak halkası | Dört prototipin tamamını ilgilendiriyor; tek ekranda çözülürse diller ayrışır. PM koordinasyonunda ayrı iş |
| "Önümüzdeki aylar" kartının **ilk satırı içinde bulunulan ay** | v4 mirası etiket çelişkisi (kart "önümüzdeki" diyor, ilk satır bu ay). Kart v4'ten birebir alındı; başlığı ya da kapsamı değiştirmek onaylı bir yüzeyi oynatmak olur → **not düşüldü**, düzeltilmedi |
| E-12'nin `detay.taksit_bilgi` "… her ay {tutar}" dizesi | Kuruş-hassas seride "her ay" yanlış bir söz (taksitler 1 kuruş farklı olabilir). E-12 turunda düzeltilecek |
| `.cubuk-oluk` / `well` komşuluğunun `tokens.md` §1.9'a eklenmesi | `tokens.md` bu turda **dokunulmaz** kapsamdaydı → PM'e not |
