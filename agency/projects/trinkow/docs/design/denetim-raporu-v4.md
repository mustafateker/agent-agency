# prototip-v4 · design-reviewer denetim raporu

> **NİHAİ DURUM: PASS** — bkz. dosyanın sonundaki "DELTA DENETİMİ (2. tur)".
> Aşağıdaki 1. tur raporu tarihsel kayıttır; tüm maddeleri kapandı.

**KARAR (1. tur): REVİZE GEREKİYOR — 3 bloklayıcı**
Tarih: 2026-09-18 · Kapsam: delta (v4'te yeni/değişen 10 ekran, 122 yüzey)
Not: rapor metni denetçinin çıktısıdır, PM tarafından dosyaya işlenmiştir.

## BLOKLAYICI

### B-1 · `stil.css:577-579` ve `:779-781` — gün kutusu sayısı WCAG AA altında
`.gun-kutu.altinda` ve `.gun-kutu.secili`, `background-image: var(--grad-action)`
(dikey `#3B82F6`→`#2F68C5`) üstüne ortalanmış **beyaz 13pt** metin koyuyor.
44px kutunun ortasında gradyan ≈ `#3575DD` → beyazla **4.43:1**, glifin üst
yarısında ~4.2 → **AA (4.5) altı**. `delta-v4.md` tokens eklentisi #6 bu yüzeyi
"`#FFFFFF`/`primary-deep` = 5.37" diye ilan ediyor ama CSS o değeri üretmiyor.
`tokens.md` §1.6 zaten "`#3B82F6` zeminli küçük beyaz metin yasak" diyor.
Etki: v4'ün en çok tekrarlanan elemanı — E-21 ızgarası (28 kutu), E-24 ay
ızgarası (31), E-03 maaş günü (31).
**Düzeltme:** iki sınıftan `background-image: var(--grad-action)` kaldırılsın,
düz `primary-deep` kalsın (5.37 ✅). Hacim `clay.raised`/`clay.action` gölgesinden
gelmeye devam eder. `.durak-bag-dolu` (571) metin taşımadığı için etkilenmez.

### B-2 · `stil.css:462` — aynı üründe ÜÇ farklı "seçili" dili
`.secim-kart.secili` hâlâ `inset 0 0 0 2px var(--primary-text)` **halka** kullanıyor.
Oysa: çip seçili = `primary-soft` + `clay.sunken`, halka yok (tokens §7.6, K-040);
gün kutusu seçili = dolgu + kabartma, halka yok (K-054/6). Bileşen v4'te
`03-onboarding` (yeniden yazıldı) ve `17-tanisma` (yeni) yüzeylerinde yeniden
kullanıldı; T-3 üçüncü bir dil ekledi.
**Düzeltme:** `.secim-kart.secili`'den halka kaldırılsın; seçim `primary-soft` +
`clay.sunken` + `secim-ikon` kabarması ile verilsin (462 ve 467 zaten bunu yapıyor).
Kalan iki dil tokens'a yazılsın: "seçimde derinlik, gün ızgarasında dolgu".

### B-3 · E-20 ↔ E-02 ↔ E-26 — aynı olgu iki uyumsuz biçimde soruluyor
`_uret/s12_profilleme.py:133` E-20 geliri **aralık** olarak soruyor (4 seçenek);
Katman 1 E-02 aynı bilgiyi **tam tutar** olarak alıyor; E-26'nın formülleri
(`gelir_kurus`) aralık cevabıyla **çalışmaz**. K-053/F-12 eksik profili tamamlama
yolunu artık "Ayarlar > Plan ve profil"e bağladı. Prototipte çelişen iki yüzey
birlikte duruyor.
**PM kararı (K-061/3):** E-20'nin gelir sorusu **emekliye ayrılır**; yerine E-25'in
cevaplanmamış kartlarından biri gösterilir. `s12_profilleme.py` yeniden üretilir.

## ÖNEMLİ (bloklamaz, bu turda düzeltilir)

4. `_uret/s17_tanisma.py:268-270` **"Bir öğün kaç lira"** → `delta-v4.md` T-4
   öz-denetimi "'öğün' hiçbir yüzeyde yok" diyor, doğru değil. K-050'nin yasak
   listesinde geçmiyor (teknik ihlal değil) ama referans kalori uygulamasının
   bilgi mimarisi tam olarak "öğün grupları"ydı ve K-051 onu bilinçle kategoriye
   çevirdi. → **"Bir yemek kaç lira"** yapılsın; `tan.yemek.fiyat` anahtarı
   delta'nın metin tablosuna eklensin.
5. `_uret/denetim.py:11` — `IZIN_RADIUS` kümesinde **"4"** var; tokens §4 4'ü
   yasaklıyor. Şu an hiçbir yerde radius 4 yok → kural bedelsiz sıkılaştırılabilir.
   Açık kalırsa K-054/6'da yakalanan `.imza-kare{radius:4}` türü ihlal bir daha
   yakalanmaz. → "4" çıkarılsın.
6. `denetim.py` kapsamı — yalnız HTML'in `<main>` bloğunu tarıyor; renk/radius/
   boşluk `stil.css` sınıflarında yaşıyor. "0 bulgu" iddiası paleti kapsamıyor.
   (Denetçi palet taramasını elle yaptı: sapma yok.) → `denetim.py`'ye `stil.css`
   hex/radius taraması eklensin.
7. `stil.css:602-616` sistem klavyesi bloğu palet dışı (`#D1D4DA`, `#1C1C1E`,
   `#ADB3BE`, `#3A3A3C`, radius 5, gap 6). Gerekçe geçerli (bu yüzeyi işletim
   sistemi çizer) ama yazılı istisnası yok — üçüncü taraf düğmeleri için K-057/2
   ile tokens §12'ye not açılmıştı, buraya açılmadı. → tokens §12'ye
   "işletim sistemi çizimleri (sistem klavyesi, durum çubuğu, home indicator)
   palet/ölçek dışıdır" satırı (T-5).
8. Devralınan üst veri kirliliği: 20 yüzey dosyasında `<title>` hâlâ "prototip v3"
   (`04`…`12` ve ilgili `_uret/*.py`). Ayrıca `fonts/fonts/` içinde dört TTF +
   LİSANS ikinci kez duruyor. → başlıklar v4'e çekilsin; yinelenen dizinin
   silinmesi **Mustafa onayına** bağlı (geri dönüşsüz silme kuralı).

## TEMİZ ÇIKANLAR (denetçi tasarımcının iddiasına güvenmeden doğruladı)

- **RN uygulanabilirliği:** `:hover`, `grid`, `::before/::after`, `sticky`, `float`,
  `calc()`, `vh/vw`, `z-index`, `transition` yalnız `stil.css`'in [A] kabuk
  bloğunda (97-194) — orada serbest. [B] bölgesi saf flexbox. `pressed` durumu
  yeni bileşenlerin hepsinde çizili. Viewport 390×844, safe area (47/28) hesapta.
- **Referans uyarlaması (K-051):** `kcal`, `porsiyon`, `besin`, `barkod`, `makro`
  hiçbir yüzeyde yok. Puan/elmas/rozet/seviye yok. Mor gradyan yok (tek gradyan
  `grad-action`). Alev/konfeti emojisi yok. Seri ekranının tezi "kupa vitrini
  değil, çetele". Kutlama övgüsüz: tespit + sıradaki durak, scrim yok, 1.2 sn,
  dokunuşla atlanır.
- **Katalog (K-050):** fiyat sütunu yok; tek tutar "geçen sefer 95 ₺" ve o
  kullanıcının kendi kaydı.
- **K-060/2:** "Öneri" pulu + "Nasıl hesaplandı" + üç çıkış (kabul / değiştir /
  limitsiz) mevcut.
- **K-053 yatırım sınırı:** yalnız "yatırım payı" etiketi; enstrüman/getiri/risk
  sözcüğü yok.
- **K-058:** Android yüzeylerinde Apple düğmesi yok.
- **Mahremiyet dili (brandbook §2.8 istisnası):** "Harcamaların sende kalır",
  "Gelirin telefonunda kalır" — mimari sözcük UI metinlerinde geçmiyor.
- **Seri kırılması dili:** "Seri dün kırıldı. Bugün yeniden başlıyor." — suçlama yok.
- **Durum bütünlüğü:** yeni ekranların hepsinde boş + yükleniyor (iskelet,
  shimmer/spinner yok) + hata + uzun metin yüzeyi var. Lorem/placeholder yok.

**Anti-pattern denetimi: 18/20 madde temiz.** İhlal eden iki madde (düşük kontrast
ve WCAG AA) tek kaynaktan: B-1.

## DELTA DENETİMİ (2. tur) — 2026-09-18

**KARAR: PASS** (teknik kapı açık; son görsel onay Mustafa'nın — CLAUDE.md)
Kapsam: yalnız kapanan maddeler + yan etkileri. **3/3 bloklayıcı, 5/5 önemli kapandı.**

| # | Madde | Durum | Denetçinin kendi doğrulaması |
|---|---|---|---|
| B-1 | Gün kutusu kontrastı | ✅ | `#FFFFFF`/`#2F68C5` **5.374:1** elle hesaplandı. `stil.css:595, 803, 575, 676` dördü de düz `primary-deep`. `.durak.gecildi` + `.imza-kare.altinda` ekleri yerinde |
| B-2 | Tek "seçili" dili | ✅ | `inset 0 0 0 2px` taraması **boş**. `.secim-kart.secili` artık `.cip.secili` ve `.kat-sec-kutu.secili` ile birebir aynı |
| B-3 | Gelir iki biçimde | ✅ | E-20 gelir sorusu emekli; `12-profilleme.html` gövdesinde "gelir" yok. `ekran-envanteri` akış G + `metinler` senkron. Ölü bağlantı yok |
| 4 | "öğün" | ✅ | Sözcük yalnız kod yorumu + gerekçede; hiçbir yüzeyde yok |
| 5 | `IZIN_RADIUS` "4" | ✅ | Küme `{0,16,20,24,28,32,36,999}` |
| 6 | `denetim.py` kapsamı | ✅ **araç güvenilir** | Beyaz liste gerçekten tokens §1 ile sınırlı; istisna 3 blok (~150/860 satır), sınırları açık. Blok dışı tüm hex ve radius değerleri bağımsız tarandı → "0 bulgu" gerçek |
| 7 | tokens §12.0 istisnası | ✅ | `tokens.md:849-860` |
| 8 | `<title>` v3→v4 | ✅ | `fonts/fonts/` ⏸️ Mustafa onayı |
| K-062 | Gradyan zeminde metin | ✅ | `grad-action`ın 11 kullanımının **hiçbiri metin taşımıyor**. `.btn-primary` düz `primary-deep`, basılı `primary-press` = 6.590. Grafik eşiği en kötü nokta 3.68 ≥ 3 ✅ |

**Yan etki taraması:** yeni jenerik-AI riski yok · yeni kontrast sorunu yok · durum
kaybı yok. RN kısıtları yeniden tarandı: `grid`/`::before`/`z-index`/`calc`/`vh`
yalnız [A] kabuk bloğunda; [B] bölgesi saf flexbox.

### B-2 bilinçli riski hakkında denetçi yargısı
**Kabul edildi, halka geri konmayacak.** (a) Seçili kartın zemin farkı zayıf
(`#E4EEFE`/`#E6EFFE` ≈ 1.01) ama bu `tokens.md` §1.1'de ilan edilmiş clay
tercihinin sonucu, bu turun yeni kusuru değil; (b) ayrım raised→sunken **biçim**
değişimi + ikonun ters kabarmasıyla iki kanaldan geliyor, renkle değil (WCAG 1.4.1 ✅);
(c) halka üçüncü bir dil açar ve K-040→K-045→K-054/6 çizgisini bozar;
(d) `tokens.md` §5.4 riski ve doğru çözümü (`surface` zemin, halka değil) yazılı bırakmış.
⚠️ Kalan risk: WCAG **1.4.11** (durum sınırı 3:1) bu yüzeyde sağlanmıyor (~1.3:1).
Clay dilinin sistemik bedeli; tek yüzeye yama yapılmaz.
**Mustafa'nın 1:1 ölçekte bakması gereken tek yüzey budur.**

### ÖNERİ (bloklamaz, T-7'ye alındı)
1. `tokens.md:849` §12.0 başlığı "yalnız bu ikisi" diyor ama `denetim.py` **3**
   `@denetim-disi` bloğu bekliyor ([A] kabuk üçüncüsü). Tam K-040 tipi ayrışma
   riski → §12.0'a üçüncü satır: "[A] kabuk — RN'e kodlanmaz (§3.2)".
2. `stil_tara()` yalnız hex + radius bakıyor; `font-size`, boşluk ve RN-yasak
   dizeleri hâlâ mekanik denetimsiz → tarama genişletilsin.
3. `07-acilis.html:66` `border-radius:11px` — platform ikon maskesi (≈%22.37),
   ihlal değil; `varliklar.md`'ye **oran** olarak yazılsın.

**Anti-pattern denetimi: 20/20 madde temiz.** Önceki turun iki ihlali (düşük
kontrast · WCAG AA) B-1 + K-062 ile tek kaynaktan kapandı.
