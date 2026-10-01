# Prototip v4 — delta (Günlük / E-10 revizyonu + Seri / E-21)

Bu dosya **birleştirme listesidir.** Kaynak dosyalar (`tokens.md`,
`bilesen-envanteri.md`, `metinler.md`, `ekran-envanteri.md`) bu turda
**düzenlenmedi**; aşağıdaki maddeleri PM işler.

Üretilen: `prototip-v4/01-gunluk.html` (12 durum) ·
`prototip-v4/13-seri.html` (5 durum) · üreteçler
`_uret/s01_gunluk.py`, `_uret/s13_seri.py` · `_uret/lib.py` sekme etiketi ·
`stil.css` "v4 — GÜNLÜK + SERİ" bloğu · `index.html`.
Denetim: `python3 _uret/denetim.py` → **tüm sayfalar 0 bulgu**; bu turun
payı Günlük 12 + Seri 5 = **17 yüzey**.

---

## tokens.md eklentileri

| # | Bölüm | Eklenecek |
|---|---|---|
| 1 | §8 HAREKET | `motion.celebrate.hold` = **700ms** — bir *animasyon değil, bekleme*. Kutlama zaman çizelgesi: giriş 250 (`motion.arc`) + bekleme 700 + çıkış 250 = **1200ms** (K-048 "≤1.2 sn"). Üst sınır 250ms kuralı her geçişte korunur. |
| 2 | §2.2 `amount` rolü | Rolün kapsamı: "liste tutarı" + **gün sayısı değeri** ("21 gün", E-21). Tabular, sağa hizalı. Yeni punto üretilmedi. |
| 3 | §3.3 negatif oluk telafisi | 4. kap: `.gun-ag` (E-21 gün ızgarası) · çocuk gutter `margin-right/bottom: 8` · kap telafisi **−8**. İzinli küme (−4/−8) değişmedi. |
| 4 | §6 pasif eleman | `IconButton` pasif hâli: zemin `disabled-bg`, gölge `clay.sunken`, ikon `text-2` (4.73 ✅). **Opaklık kullanılmaz** kuralı korunur. |
| 5 | §7 bileşen ölçüleri | Yeni ölçü ailesi açılmadı: durak dairesi **44**, durak yolu **24×8** (radius 999), gün kutusu **44** (mevcut `DayBox`), lejant kare **24**, kutlama diski **96** (mevcut hata dairesi ölçüsü), kutlama kartı radius **32** + `clay.raised-lg`. |
| 6 | §1.9 kontrast (hesaplanmış) | `#FFFFFF` / `primary-deep` **5.37** AA — dolu gün kutusu ve geçilmiş durak sayısı · `warning-ink` / `warning-soft` **5.86** AA — limit dışı gün kutusu · `text-2` / `well` **5.13** AA — kayıt yok kutusu. Gün kutusunun üç durumu renge **ek olarak** derinlikle (kabarık ↔ çukur) ve `accessibilityLabel` ile ayrışır (WCAG 1.4.1). |
| 7 | §1.10 renk yasakları | Doğrulama: gün ızgarasında **yeşil/amber ikilisi kullanılmadı** — trafik ışığı semantiği yasak. Kutu dili göstergenin dilidir: mavi = limit altı, amber = limit dışı. |

## Yeni bileşenler

`bilesen-envanteri.md` sayımı: **34 → 42** (8 yeni). Rozet/puan/seviye/lig
üretilmedi (K-048 yasağı).

| Bileşen | Ekran | Durumlar |
|---|---|---|
| `DayPager` | E-10 | Kahraman göstergeyi saran gün geçişi: iki 44pt `IconButton` + yatay sayfalanan liste. `default` / `pressed` / `disabled` (sağ uç = bugün, sol uç = ilk kayıt günü). **Nokta dizisi göstergesi yok.** |
| `StreakPill` | E-10 başlık | `Chip`'in metin varyantı ("Seri 12 gün") → E-21. `default` / `pressed` / `skeleton`. Seri yok veya kapalıysa **render edilmez** (pasif çip = ölü arayüz). Başarım ikonu taşımaz, **değer** taşır. |
| `LimitChip` | E-10 kahraman kart | Bugün: dokunulur çip + `chevron-right` → E-17. Geçmiş gün: dokunulmaz `label`. v3'teki başlıktaki `sliders` `IconButton`'ının **yerine** geçer. |
| `MilestoneOverlay` | E-10 | Üst banda `absolute` tek kart. `visible` / `pressed(atla)`. Scrim yok, modal değil, sekme çubuğunu engellemez. |
| `MilestoneRail` | E-21 | 8 durak (3·7·14·30·60·100·180·365) + aralarında **oranlı** yol. Durak: `gecildi` / `sirada` / `ileri`. Yatay `ScrollView`. |
| `StreakDayGrid` | E-21 | 28 gün (4 tam hafta), 7 sütun `flex-wrap`. Kutu: `altinda` / `disinda` / `yok` + kelimeli lejant. |
| `StreakSummaryWell` | E-21 | "En uzun seri" çukur satırı — `ValueWell`'in **dokunulmaz** varyantı. `default` / `empty` ("Henüz yok"). |
| `NoSpendDayCard` | E-10 | Harcamasız gün işaretleme: ikincil buton → işaretlendikten sonra yerini `InfoStrip`'e bırakır. |

`DayBox` satırına eklenecek: v4'te üç seri durumu (`altinda` / `disinda` /
`yok`) ve **sayı-only** varyant (ay kısaltması yok — 28 günlük pencerede ay
tekrarı bilgi taşımaz).

## Yeni metinler

`metinler.md` §1'de `sekme.bugun` → **`sekme.gunluk` = "Günlük"** (K-049).

| Anahtar | Metin |
|---|---|
| `gunluk.baslik.bugun` / `.dun` | Bugün · Dün |
| `gunluk.baslik.tarih` | {gg}/{aa} {GünAdı} → "10/09 Perşembe" |
| `gunluk.ust.tarih` | {g} {Ay} {GünAdı} → "17 Eylül Perşembe" (yalnız Bugün/Dün sayfasında) |
| `gunluk.ust.uzaklik` | {n} gün önce (tarihli başlıklı sayfalarda) |
| `gunluk.onceki_gun` / `.sonraki_gun` | Önceki gün · Sonraki gün (a11y) |
| `gunluk.ipucu` | Yana kaydırarak önceki günlere geçebilirsin. |
| `gunluk.sinir.ilk_kayit` | İlk kaydın bu gün. Daha geriye kayıt yok. |
| `gunluk.hero.gecmis` | o gün harcanan |
| `gunluk.o_gun_limiti` | O gün limiti {tutar} |
| `gunluk.gun_kapandi` | Gün kapandı. {adet} kayıt, {tutar}. |
| `gunluk.gun_kapandi_disinda` | Gün kapandı. {tutar}, limitin {fark} üzerinde. |
| `gunluk.seriye_sayildi` | Bu gün seriye sayıldı. |
| `gunluk.seriye_sayilmadi` | Bu gün seriye sayılmadı. |
| `gunluk.liste_baslik.gecmis` | O günün kayıtları |
| `gunluk.harcamasiz.baslik` | Harcamasız gün |
| `gunluk.harcamasiz.govde` | O gün kayıt yok. Kayıtsız gün seriye sayılmaz. |
| `gunluk.harcamasiz.ipucu` | Harcamasız geçtiyse işaretle, seri korunur. |
| `gunluk.harcamasiz.eylem` | Harcamasız işaretle |
| `gunluk.harcamasiz.isaretli` | Harcamasız gün. Seriye sayıldı. |
| `gunluk.gun_bos.hero` | o gün harcanan (0 ₺ ile) |
| `gunluk.seri_baslar.baslik` / `.govde` | Seri bugün başlar · Günü limit altında kapatırsan seri 1 gün olur. |
| `seri.cip` | Seri {n} gün · a11y: "Seri {n} gün. Seri ekranını aç" |
| `seri.baslik` | Seri |
| `seri.hero.birim` | gün |
| `seri.aktif.govde` | {n} gündür limit altında kapatıyorsun. |
| `seri.kirildi` | Seri dün kırıldı. Bugün yeniden başlıyor. *(brandbook §2.3'ten birebir)* |
| `seri.bos.govde` | Seri henüz başlamadı. Bugünü limit altında kapat. |
| `seri.en_uzun` / `.en_uzun_bos` | En uzun seri · Henüz yok |
| `seri.duraklar` | Duraklar |
| `seri.durak.kalan` / `.sonraki` | {n} gün kaldı · Sıradaki durak {n} gün |
| `seri.durak.a11y` | {n} gün durağı geçildi / sırada / ileride |
| `seri.pencere` | Son 4 hafta · {ilk} – {son} |
| `seri.pencere.bos` | Günleri yazdıkça buraya dolacak. |
| `seri.lejant` | limit altında · limit dışı · kayıt yok |
| `seri.gun.a11y` | {g} {Ay}, limit altında / limit dışı / kayıt yok |
| `seri.kural.baslik` | Seri nasıl işler |
| `seri.kural.1` | Günü günlük limitin altında kapatırsan seri sürer. |
| `seri.kural.2` | Kayıt yazmadığın gün sayılmaz. Harcamasız geçtiyse işaretle. |
| `seri.kapali.baslik` / `.govde` / `.ipucu` | Seri kapalı · Seri için günlük limit gerekir. · Limit kurduğunda duraklar ve günler burada görünür. |
| `kutlama.baslik` / `.govde` / `.kapat` | {n} gün · Seri {n} güne ulaştı. Sıradaki durak {m} gün. · Dokununca kapanır (a11y: "Kutlamayı kapat") |

Övgü sözcüğü (tebrikler/harika/bravo), ünlem ve emoji **hiçbirinde yok**.
"Kalori/kcal/besin/porsiyon/barkod" hiçbir dizede geçmiyor.

## RN inşa notları

1. **Tarih sayfalama:** `FlatList` **horizontal + `pagingEnabled`**, sayfa
   genişliği `Dimensions.get('window').width`, `getItemLayout` ile sabit
   ölçü, `windowSize={3}`, `initialScrollIndex` = son (bugün),
   `inverted` **kullanılmaz**. Her sayfa kendi dikey `ScrollView`'ını taşır.
   Veri: ilk kayıt gününden bugüne gün listesi; liste **bugünde biter**
   (gelecek sayfa üretilmez, "geleceğe gidilmez" kuralı veri seviyesinde).
2. **Oklar:** `Pressable` 44×44, `accessibilityState={{ disabled: true }}`,
   uçlarda `scrollToIndex` çağrılmaz. Ok yönü = sayfa yönü: sol ok **soldaki
   (daha eski)** sayfaya götürür.
3. **Kutlama animasyonu:** `Reanimated` `withTiming` — `opacity` 0→1 ve
   `translateY` 8→0, **250ms `Easing.out(Easing.quad)`**; 700ms bekleme
   (`withDelay`); çıkış `opacity` 1→0, 250ms. **`scale` yok, spring yok,
   overshoot yok** (tokens §8 yasağı). `reduceMotion` açıkken süreler 0ms,
   kart 1200ms görünür kalır. Dokunma → anında kapanır. Milestone başına
   **bir kez**: gösterildi bayrağı yerel olarak saklanır (`3|7|14|...`).
4. **Gün ızgarası:** CSS Grid yok → `flexDirection:'row'`, `flexWrap:'wrap'`,
   kap `marginRight:-8`, çocuk `marginRight/Bottom:8`. 7 kutu × (44+8) = 364
   ≤ 358+8 → satır başına tam **7** kutu. Ölçüm: `390−32=358` iç genişlik.
5. **Duraklar şeridi:** `ScrollView horizontal`,
   `contentContainerStyle={{paddingHorizontal:16}}`, 8 durak + 7 yol = 520pt
   → kaydırılır; yarım görünen durak keşfedilebilirliği sağlar.
   Yol dolgusu genişliği yüzdeyle (`flex` değil) verilir.
6. **FAB geçmiş günde:** aynı FAB, E-11'i **görüntülenen günün tarihiyle ön
   dolu** açar (K-049 "geç kayıt"). `accessibilityLabel` değişmez.
7. **Seri hesabı yereldir** (sunucu yok): gün kapanışı = E-19'daki gün
   sınırı ayarı. Seri = üst üste, limit altında **ve** (kayıt var **veya**
   harcamasız işaretli) günler.
8. **Ölçüm (fontTools, 390pt):** en uzun başlık `03/09 Perşembe` = 218pt
   (Poppins 26) + 8 + `Seri 12 gün` çipi 104pt = **330 ≤ 358** ✅. Kahraman
   satır: 44 + 224 + 44 = **312 ≤ 326** (kart içi) ✅. Kahraman kart üst
   satırı: `Takip` çipi 85 + `Günlük limit 300 ₺` çipi 183 = **268 ≤ 326** ✅.
   Başlık `numberOfLines={1}` + `flexShrink` ile korunur.

## Bilinçli tasarım kararları (design-reviewer için)

1. **Sayfalama göstergesi nokta dizisi değil**, kahraman göstergeyi saran iki
   oktur: sıfır ek dikey yer harcar, yönü söyler, sınırı `disabled` ile
   gösterir. İkinci katman: ilk açılışlarda kapatılabilir tek satırlık ipucu.
2. **Kahraman sayının anlamı gün kapanınca değişir:** "bugün kalan" →
   "o gün harcanan". Kapanmış günde "kalan" diye bir şey yoktur.
   Öncülü var: v3 limitsiz varyantında "bugün harcanan" (`HeroPlain`).
3. **Kategori limitleri kartı yalnız Bugün sayfasında.** O kart *aylık* bir
   değerdir; geçmiş gün sayfasında o güne ait olmayan bir sayı gösterirdi.
4. **Limit dışı günde seri uyarısı yok.** "Serini kaybediyorsun" kaybetme
   korkusudur ve brandbook §2.3'te birebir yasaktır. Seri çipi gün kapanana
   kadar değişmez.
5. **Izgara 28 gün (4 tam hafta), 30 değil** ve **bugünü içermez**: bugün
   kapanmadığı için dördüncü bir kutu durumu (“sürüyor”) üretmek yerine
   pencere dünde bitirildi; başlık tarih aralığını yazar.
6. **Limitsiz modda E-21'e giriş yok** (çip çizilmez); kullanıcı seriyi
   yalnız kart içindeki nötr "Limit belirle" kapısından açar.

## 🔴 Çelişkiler

1. **K-049 kendi içinde tutarsız.** "Sola kaydır → bir önceki gün" ile
   "bugün **en sağdaki** sayfa" aynı yönü göstermiyor: bugün en sağdaysa
   önceki gün **soldadır** ve ona gitmek için içerik sağa kaydırılır.
   Yapısal cümleyi (bugün en sağda, geçmiş solda) **koruyup** jesti buna
   göre kurdum; oklar yönü kesinleştirdiği için kullanıcıda belirsizlik
   kalmıyor. **PM: K-049'un jest cümlesi düzeltilsin** ("önceki güne
   soldaki sayfaya geçerek gidilir").
2. **brandbook §2.3** başlığı hâlâ "FAZ 2 — seri/streak (Faz 1'de
   üretilmez)" diyor; K-048 seriyi MVP'ye aldı. Ton satırları aynen
   kullanıldı, yalnız **faz etiketi eski** → güncellenmeli.
3. **bilesen-envanteri §6**, Faz 1'de üretilmeyecekler arasında **"takvim
   ızgarası"** ve **"rozet/başarım"** sayıyor. `StreakDayGrid` takvim
   değildir (hafta başlığı, ay gezinmesi, gün seçimi yok — salt çetele) ama
   maddeye temas eder; PM direktifiyle üretildi, **onayın yazıya geçmesi**
   gerekir. Rozet/başarım üretilmedi.
4. **Buton kelime sınırı.** `metinler.md` §0: buton 1-3 kelime. Görevdeki
   "Harcamasız gün olarak işaretle" 4 kelime → butonda **"Harcamasız
   işaretle"**, tam cümle kart gövdesinde. PM onaylarsa tersi de yapılabilir.
5. **v3 kararından bilinçli sapma.** v3'te limitsiz varyantta "Limit
   belirle" çağrısı *yoktu* (limitsiz kalmak geçerli bir seçim). K-048 seriyi
   ürüne soktuğu için **tek** nötr kapı eklendi (E-10 limitsiz + E-21
   kapalı). Amber renk, ünlem ve "eksik kurulum" tonu yok.
6. **`stil.css` eşzamanlı yazılıyor.** Paralel bir ajan aynı dosyaya
   E-24/E-22/E-23 bloğunu ekliyor; bu turda benim bloğum bir kez üzerine
   yazıldı, geri kondu ve şu an iki blok çakışmasız duruyor. O blokta **iki
   token ihlali** var, birleştirmede düzeltilmeli:
   - `.imza-kare { border-radius: 4px }` → tokens §4 izinli değerler
     **16/24/32/999/0**; 4 yasak.
   - `.gun-kutu.pasif { box-shadow: none }` → tokens §6: pasif durum
     **renk + `clay.sunken`** ile verilir, gölge kaldırılmaz.
   - `.gun-kutu.secili` bir `inset 0 0 0 2px` halka kullanıyor; K-040 halkayı
     çip/kategori ızgarası için kaldırmıştı — gün seçici için **PM kararı**
     gerekir (aynı dilde iki farklı "seçili" anlatımı olmasın).

7. **`s01_gunluk.py` iki ajan tarafından yazıldı.** E-10 başlığına paralel
   ajan bir **takvim düğmesi** (→ E-24 Gün seçici) ekledi, seri çipinin
   görünen metnini genişlik için `Seri 12 gün` → **`Seri 12`** kısalttı
   (`accessibilityLabel` tam hâlini koruyor) ve kategori kartına satır
   başına hızlı **+** getirdi. Birleşmiş hâl tutarlı ve denetimden 0
   bulguyla geçiyor; **iki karar PM'e ait:**
   - Başlık sağ üstünde artık **iki** hedef var (çip + takvim). K-049 yalnız
     seri rozetini şart koşuyordu; takvim düğmesi kaydırmanın erişilebilir
     karşılığı olarak savunulabilir, ama üç dokunma hedefli bir başlık
     satırı v3 sadeliğinden sapmadır.
   - `Seri 12` görünen metni birimsiz kaldı. Ölçüm (fontTools): `Seri 12 gün`
     çipiyle bile en uzun başlıkta **338 ≤ 358** çıkıyor → birim geri
     konabilir.

---
---

# v4 · İKİNCİ BÖLÜM — Gün seçici (E-24) + Günlük'ün referans uyarlaması

> Bu bölüm aynı turun ikinci yarısıdır (PM'in ek brief'i: kalori takip
> uygulamasının 9 ekran görüntüsü referans alındı). Yukarıdaki bölüm
> E-10 sayfalama + E-21 Seri'yi anlatır; burada **E-24 Gün seçici** ekranı
> ve E-10'un **kategori grupları** mimarisi var.
>
> Üretilen: `prototip-v4/14-gun-secici.html` (5 durum) ·
> `_uret/s14_gun_secici.py` · `stil.css` "v4 — GÜN SEÇİCİ (E-24)" bloğu ·
> `01-gunluk.html` yeniden üretildi (başlıkta takvim düğmesi + kategori
> grupları) · `index.html` 14 ekran.
> Denetim: `python3 _uret/denetim.py` → **14 sayfa · 78 yüzey · 0 bulgu.**

## Referans uyarlama kararları

Referans görseller: `docs/design/referans-gorseller/kalori-app-referans/`.
Kural: **bilgi mimarisi ve mekanik alındı, görsel stil alınmadı.** Referans
Material/flat + emoji dilinde; Trinkow claymorphism ve emoji yasak (K-004).

| # | Referanstaki şey | Karar | Gerekçe |
|---|---|---|---|
| 1 | Tarih sol üstte ("13/09 Paz") | **ALINDI** | Mustafa'nın istediği birebir bu. Bizde Bugün / Dün / `10/09 Perşembe` (K-049). Üst satır başlığın taşımadığı bilgiyi taşır (tam tarih ya da "7 gün önce"). |
| 2 | Sağ üstte seri göstergesi + takvim ikonu | **ALINDI** | Seri çipi → E-21, takvim düğmesi → E-24. Çip **metin** taşır ("Seri 12"), alev/şimşek ikonu yok: emoji yasağı + oyunlaştırma klişesi. Çip "Seri 12 gün"den "Seri 12"ye kısaldı, üç hedef başlığa sığsın diye (ölçüm: çip 84 + takvim 44 + aralar 16 = 144; başlığa 214 kalır). |
| 3 | Elmas/puan sayacı (1030) | **ALINMADI** | K-048: puan/rozet/seviye yok. Bütçe uygulamasında puan ekonomisi sahte motivasyon üretir. |
| 4 | Kahraman: "Alınan / Kalan / Yakılan" | **KISMEN** | "Kalan" kahraman sayı olarak duruyor, "Alınan"ın karşılığı gün toplamıdır ve kartın alt satırında yazıyla geçer ("Bugün 180 ₺"). **"Yakılan" için karşılık İCAT EDİLMEDİ** — harcamada "yakılan kalori" diye bir şey yoktur; uydurulsa Mustafa'nın "saçma sapan kalori hesapları" dediği hata olurdu. Üçüncü yuva boş bırakıldı; günlük limit değeri zaten kartın sağ üstünde **dokunulur çip** olarak duruyor (→ E-17). |
| 5 | Makro çubukları (Karbonhidrat/Protein/Yağ) | **ALINDI, tek bileşende birleşti** | "En çok harcanan 3 kategori + limit çubuğu" ile "öğün grupları" ayrı ayrı çizilseydi aynı bilgi iki kez görünürdü. Tek **Kategoriler** kartı: satırlar bugünkü tutara göre azalan sıralı (= makro çubuklarının işi) + her satırda aylık limit çubuğu ve `+` (= öğün gruplarının işi). |
| 6 | Öğün grupları (Kahvaltı/Öğle/Akşam + halka + "+") | **ALINDI** | F-4 "zihinsel muhasebe" ile birebir örtüşüyor. Halka yerine **çubuk** kullanıldı: halka bu ekranda kahraman göstergenin dili, satırda tekrarlanınca hiyerarşi düzleşir. Son satır bilinçli olarak **"bugün kayıt yok"** — referansın "Öğle Yemeği 0 / 928" satırının karşılığı, boş yuva davet eder. |
| 7 | "795 / 928 kcal" (öğün hedefi) | **ALINMADI** | Trinkow'da kategori limiti **aylıktır** (E-17). Uydurma bir "günlük kategori limiti" üretmek referansı taklit etmek olurdu. Satırda iki zaman ölçeği var ve **yazıyla** ayrılıyor: "bugün 95 ₺" / "aylık 940 ₺ / 1.200 ₺". |
| 8 | Siyah pill "+" düğmesi | **BİÇİM ALINMADI** | Mekanik (kategoriden doğrudan ekleme) alındı; siyah dolgu yerine kil kabarık daire + `primary-soft` zemin. Siyah paletimizde yok. |
| 9 | Alt sekmeler (Günlük/Tarifler/Profil/Pro) | **ALINMADI** | Sekme 3'te kalır: Günlük · Kayıtlar · Özet (K-049). Tarifler/Profil/Pro karşılığı üretilmedi. |
| 10 | Streak ekranı: büyük sayı + "Günlük Seri" + 7 gün şeridi + "En uzun seri" | **ALINDI** | E-21'de (yukarıdaki bölüm). |
| 11 | Streak ekranı: emoji alev, konfeti, mor gradyan hero, "Seri Dondurma hakkı", "Kararlıyım" | **ALINMADI** | Emoji + mor gradyan: anti-pattern listesi ve K-004. Dondurma hakkı: Faz 1'de yok (K-048). "Kararlıyım": içi boş CTA — hiçbir şey yapmıyor. |
| 12 | Takvim ekranı: ay ızgarası, gün durumları, ay ileri/geri, altta üç istatistik | **ALINDI** → E-24 | Aşağıdaki bölüm. |
| 13 | Takvim: yeşil onay rozeti | **ALINMADI** | Rozet ızgarada 28-31 kez tekrarlanınca gürültü olur; durum **zemin + derinlik + etiket** ile kodlandı. Ayrıca yeşil/kırmızı trafik ışığı semantiği tokens §1.10'da yasak. |
| 14 | Takvim: "Kilo −5,0 kg" istatistiği | **ALINMADI** | Parasal karşılığı yok. Yerine dürüst üçüncü satır: **"Limit altı günlerde biriken"** (= Tasarruf kipinin tanımı, brandbook §2.4). |
| 15 | "Başarını Paylaş" | **ALINMADI** | Faz 1'de paylaşım/sosyal yüzey yok. |
| 16 | Profil / Pro (arkadaşlar, Health Connect, paywall) | **KAPSAM DIŞI** | Arkadaşlar sunucu gerektirir (F-13 "sunucu yok"); Pro/paywall için ürün kararı yok. Tasarlanmadı. |

## E-24 · Gün seçici — yeni ekran

`ekran-envanteri.md`'ye eklenecek satır:

| Kod | Ad | Giriş | Çıkış | Boş | Hata |
|---|---|---|---|---|---|
| E-24 | Gün seçici (ay ızgarası) | E-10 başlığındaki takvim düğmesi | gün seçilince E-10 o güne gider | "Bu ayda kayıt yok" + Bugüne dön | okuma hatası E-10 ile aynı desende |

Akış: E-10 → (takvim) → E-24 → gün dokunuşu → E-10 (o gün). **"Seç"
butonu yok**: dokunuş hem seçer hem kapatır, iki adım bire indi.

### tokens.md eklentileri (bu bölüm)

| # | Bölüm | Eklenecek |
|---|---|---|
| 8 | §7 bileşen ölçüleri | `MonthGrid`: satır = 7 eşit hücre (`flex: 1`), hücre içi kutu **44** (mevcut `DayBox`), kutu altı işaret **8**, satır arası **8**. Kart iç genişliği 326 → hücre 46, dokunma hedefi 44 korunur. **CSS grid yok.** |
| 9 | §7 lejant | `LegendSwatch` = 24×24, radius **16** (gün kutusunun küçük ölçeği; yeni radius üretilmedi). |
| 10 | §6 pasif eleman | `DayBox` pasif hâli: zemin `disabled-bg` + `clay.sunken` + sayı `text-3`. Gölge **kaldırılmaz** (ilk taslakta kaldırılmıştı, tokens §6'ya göre düzeltildi). |
| 11 | §1.9 kontrast | `text-3` / `disabled-bg` **3.4** — yalnız **pasif (disabled) ve dokunulmaz** gün sayısında kullanılır; WCAG 1.4.3 pasif bileşenleri kapsam dışı bırakır. Etkin hiçbir metin bu çiftle çizilmez. |

### Yeni bileşenler (bu bölüm) — sayım 42 → 45

| Bileşen | Ekran | Durumlar |
|---|---|---|
| `MonthGrid` | E-24 | 7 sütunlu flex satırlar. Hücre: `altinda` / `disinda` / `yok` / `pasif` / `pressed`. Ay başı/sonu boş hücreleri **yer tutar** (ızgara kaymaz). |
| `MonthNav` | E-24 | `lib.ay_secici`nin pasif oklu sürümü: `default` / `pressed` / `disabled` (iki uçta K-049 sınırı). Pasif ok **gizlenmez** — gizlenen ok düzeni kaydırır. |
| `CategoryGroupRow` | E-10 | Kategori grubu satırı: ikon + ad + bugünkü tutar + aylık limit çubuğu + `+`. Durumlar: `default` / `bugün kayıt yok` / `limit dışı` / `+ pressed`. |

`DayBox` satırına eklenecek: `pasif` durumu ve **"seçili" durumunun
olmadığı** notu (aşağıya bak).

### Yeni metinler (bu bölüm)

| Anahtar | Metin |
|---|---|
| `gunsec.baslik` | Gün seç |
| `gunsec.bugune_don` | Bugüne dön |
| `gunsec.alt.kayitli` | {n} gün kayıtlı |
| `gunsec.alt.kayit_yok` | kayıt yok |
| `gunsec.alt.acik_gun` | Açık gün {g} {Ay} |
| `gunsec.lejant.altinda` | limit altı |
| `gunsec.lejant.disinda` | limit dışı |
| `gunsec.lejant.kayit_yok` | kayıt yok |
| `gunsec.lejant.bugun` | Kutunun altındaki nokta bugünü gösterir. |
| `gunsec.sinir.baslangic` | Trinkow'a {g} {Ay}'ta başladın. Daha öncesi yok. |
| `gunsec.bos.baslik` | Bu ayda kayıt yok |
| `gunsec.bos.govde` | Kayıt yazdığın günler burada işaretlenir. Bugünden başlayabilirsin. |
| `gunsec.ozet.baslik` | {Ay} özeti |
| `gunsec.ozet.kayitli_gun` | Kayıt yazılan gün |
| `gunsec.ozet.limit_alti` | Limit altı gün |
| `gunsec.ozet.biriken` | Limit altı günlerde biriken |
| `gunsec.a11y.gun` | {g} {Ay} {GünAdı}, {durum}[, bugün] |
| `gunsec.a11y.onceki_ay` / `.sonraki_ay` | Önceki ay · Sonraki ay (sınırda: "… yok") |
| `gunluk.a11y.takvim` | Gün seç |
| `gunluk.grup.bugun` | bugün |
| `gunluk.grup.aylik` | aylık |
| `gunluk.grup.bugun_yok` | bugün kayıt yok |
| `gunluk.grup.baslik` | Kategoriler |
| `gunluk.grup.alt` | Bugünkü tutar · aylık limit |
| `gunluk.a11y.gruba_ekle` | {kategori} kategorisine harcama ekle |

Ay adları ve gün adları `metinler.md` §18'deki biçimlerden gelir; yeni
tarih biçimi üretilmedi.

### RN inşa notları (bu bölüm)

- `MonthGrid` **FlatList değil**: en fazla 6 satır × 7 hücre, sabit; `View`
  satırları yeterli. Ay değişince yeniden hesaplanır.
- Hücre `flex: 1` ile dağıtılır; sabit genişlik verilmez, çünkü cihaz
  genişliği 375-430 arasında değişir ve 44 hedefi korunmalıdır.
- Boş hücreler (ayın ilk haftası) **gerçek View**'dir, `::before` yok.
- Ay geçişi yatay `PagerView` **değil** — ok düğmeleri yeterli; gün seçici
  bir gezinme aracı, ikinci bir jest katmanı gerekmiyor.
- `disabled` hücrede `accessibilityState={{disabled:true}}`; etiket "seçilemez"
  kelimesini taşır, böylece ekran okuyucu sınırı söyler.
- E-10'daki `+` düğmesi harcama ekleme sayfasını **kategori ön dolu** açar;
  tutar alanı odaklı ve klavye açık gelir (F-2 sürtünme kuralı).

### Bilinçli kararlar (design-reviewer için · bu bölüm)

1. **Gün ızgarasında "seçili" durumu YOK.** K-040 halkayı kaldırmıştı,
   derinlik ise "kayıt var/yok" ayrımı için harcanmış durumda. Dördüncü bir
   görsel dil üretmek yerine açık gün, ay başlığının alt satırında
   **yazıyla** söylenir ("Açık gün 30 Ağustos"). Tek görsel işaret "bugün"
   noktasıdır.
2. **Üç istatistik referanstaki gibi yan yana değil, satır satır.** Yan yana
   ikon+etiket+değer üçlüsü, anti-pattern listesindeki "üç sütunlu daire
   ikon + başlık" şablonuna çok yakın duruyordu; ayrıca "Limit altı günlerde
   biriken" etiketi üç sütuna sığmıyor. Satır ritmi ürünün geri kalanıyla
   (E-17/E-19) aynı.
3. **Geçmiş gün sayfasında Kategoriler kartı yok.** Kart aylık limit taşır;
   kapanmış bir günün sayfasında bu ayın sayısını göstermek, o sayfada o güne
   ait olmayan bir değer göstermek olurdu.
4. **Ay ızgarası "kayıt yok" ve "seçilemez"i farklı çiziyor** (çukur boş kutu
   vs. `disabled-bg` çukur kutu) ama ikisi de renk-dışı bir kanalla da
   ayrışır: pasif kutunun sayısı `text-3`, etiketi "seçilemez" der.
5. **Ağustos sayfasında 1-27 silinmedi, pasifleştirildi.** Silinseydi ay
   sakat görünürdü; gri ama duran gün "burada veri yok" der ve ızgara
   takvim olarak okunmaya devam eder.

### Yukarıdaki "🔴 Çelişkiler" §6'nın kapanışı

E-24 bloğundaki üç bulgu **düzeltildi** (aynı turda, birleştirmeye iş
bırakmadan):
- `.imza-kare` radius 4 → **16** (ölçü 16 → 24).
- `.gun-kutu.pasif` `box-shadow:none` → **`clay.sunken`** (tokens §6).
- `.gun-kutu.secili` halkası **tamamen kaldırıldı** (K-040) — "seçili"
  durumu artık yok, bkz. bu bölüm "Bilinçli kararlar" 1.

## 🔴 Bu bölümün açık maddeleri (PM'e)

1. **E-22 Giriş / E-23 Kayıt tasarlanmadı.** K-047 bu iki ekranı istiyor ama
   bu turun brief'i E-10 + E-21 + E-24 ile sınırlıydı. Ayrı bir tur gerekir;
   `stil.css`'e onlar için jeton **eklenmedi** (kullanılmayan CSS bırakmamak
   için). Karar PM'de: aynı v4 içinde s15 olarak mı, ayrı turda mı?
2. **E-24 sekme çubuğu taşımıyor** (itilen ekran). E-10'dan açılır, geri
   dönüşü iOS'ta kenardan kaydırma + sol üstteki geri oku. Bu, E-15/E-17 ile
   aynı desen; onay gerekmiyor ama denetimde "sekme nerede" diye sorulmasın.
3. **"Limit altı günlerde biriken" sayısının kaynağı:** limit altı günlerde
   (limit − harcanan) toplamı. Bu tanım `tokens.md`/`metinler.md`'de yazılı
   değil; Tasarruf kipinin tanımıyla aynı olduğu için uydurma değil ama
   **yazıya geçmesi** gerekiyor (F-1/F-6 ile ilişkisi netleşsin).

## Anti-pattern öz-denetimi (E-24 + E-10 grupları · madde madde)

| Anti-pattern | Durum |
|---|---|
| Mor-mavi varsayılan gradyan | ✅ Referansın mor streak hero'su alınmadı; tek gradyan `grad-action` (brandbook birincil mavisi), yalnız eylem yüzeyinde. |
| Her elementte glassmorphism | ✅ Bulanıklık hiç yok; dil kil (kabarık/çukur). |
| Amaçsız drop-shadow | ✅ Gölge anlam taşıyor: kabarık = dokunulur/veri var, çukur = oluk/pasif, basılı = içe çöker. Gün kutusunda gölge **kayıt var/yok** ayrımının ikinci kanalı. |
| Karışık köşe yarıçapı | ✅ 16 (kutu/lejant) · 24 (kart) · 999 (nokta/çip/düğme). Radius 4 bulgusu düzeltildi. |
| Inter / Poppins / Montserrat "varsayılan" | ✅ Font seçimi v1'de gerekçelendirildi (Poppins başlık, Montserrat tabular rakam); yeni font eklenmedi, yeni ağırlık eklenmedi. |
| 3 sütunlu daire ikon + başlık + 1 cümle | ✅ Referanstaki yan yana üç istatistik **satıra** çevrildi; hiçbir ekranda bu şablon yok. |
| Stok illüstrasyon | ✅ Hiç illüstrasyon yok; boş durumlar tipografi + kil yüzeyle kuruldu. |
| Kimliksiz aşırı beyaz boşluk | ✅ Ritim 4/8/12/16/24/32; E-24 bilgi yoğun bir alet paneli, boşlukla doldurulmadı. |
| Jenerik pazarlama dili | ✅ Övgü yasağı uygulandı: "tebrikler/harika" yok; kutlama metni tespit + sıradaki durak. |
| Düşük kontrast gri metin | ✅ Etkin metinlerin hepsi AA; `text-3`/`disabled-bg` **yalnız** pasif gün sayısında (WCAG 1.4.3 kapsam dışı) ve delta'ya yazıldı. |
| Rastgele boşluk | ✅ `denetim.py` boşluk/punto/radius taraması 14 sayfada 0 bulgu. |
| Dark mode'un renk tersine çevrilmesi | ✅ Karanlık mod üretilmedi (Faz 2), jetonu da yok — yarım iş bırakılmadı. |
| Emoji | ✅ Referansın alev/konfeti/elmas emojileri alınmadı; `denetim.py` emoji taraması temiz. Tek ikon seti Lucide. |
| Hover | ✅ Hiç `:hover` yok; her etkileşimli eleman için `basili` çizildi (gün kutusu, oklar, `+`, çip, takvim düğmesi). |
| CSS grid / `::before` / `sticky` / `calc` / `vh` | ✅ Ay ızgarası flex satırlar; denetim yasak dize listesi 0 bulgu. |

> **RN uygulama notu (her iki bölüm için geçerli):** `Chip` görsel yüksekliği
> **40**'tır (v3'te onaylandı, jeton değişmedi). E-10 başlığındaki `Seri`
> çipi ve kahraman karttaki `Günlük limit` çipi artık **gezinme hedefi**
> olduğu için `hitSlop={{top:2,bottom:2}}` ile dokunma alanı 44'e
> tamamlanır. Görsel ölçü büyütülmedi: başlık satırında üç hedef var ve
> 44'lük çip başlığı taşırıyordu.

---
---

# T-2 — Giriş / Kayıt / Hesap (+ önceki turun 4 düzeltmesi)

> Tur kapsamı: **E-22 Giriş**, **E-23 Hesap oluştur**, **E-19'a Hesap
> bölümü** ve K-054/K-055'ten gelen dört düzeltme. Temel karar **K-052**:
> Google + Apple girişi onaylı · harcama verisi cihazda kalır, senkron yok ·
> hesap yalnız kimlik · **giriş duvarı yok.**
>
> Üretilen: `prototip-v4/15-giris.html` (7 durum) ·
> `16-kayit.html` (6 durum) · güncellenen `01-gunluk.html` (12),
> `11-ayarlar.html` (3 → **4**), `14-gun-secici.html` (dil), `index.html` ·
> üreteçler `_uret/s15_giris.py`, `_uret/s16_kayit.py`, `_uret/lib.py`
> (5 Lucide glifi + giriş/kayıt ortak parçaları), `stil.css`
> ("v4 · T-2" bloğu). Denetim: `python3 _uret/denetim.py` →
> **16 sayfa · 92 yüzey · 0 bulgu.**

## Ekran akışı (ekran-envanteri.md'ye eklenecek)

| Kod | Ad | Giriş | Çıkış | Boş | Hata |
|---|---|---|---|---|---|
| E-22 | Giriş yap | E-19 Ayarlar → Hesap satırı · E-23'ten "Giriş yap" | başarılı giriş → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (biçim · kimlik) + ağ şeridi |
| E-23 | Hesap oluştur | E-19 Ayarlar → Hesap satırı · E-22'den "Hesap oluştur" | başarılı kayıt → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (kayıtlı e-posta · kural) + ağ şeridi |

**Hesap hiçbir akışın önkoşulu değildir.** Onboarding (E-01…E-03), E-10 ve
E-11 hesapsız tam çalışır; oturum durumu hiçbir yerde özellik kilidi
açmaz/kapatmaz. Uygulamada hesap için **tek davet** vardır: E-19'daki tek
satır. Modal, banner, "hesabını koru" hatırlatıcısı üretilmedi.

## Önceki turun dört düzeltmesi (tamamlandı)

1. **K-055 · sayfalama yönü çevrildi.** Oklar zaten doğruydu (bugünde **sağ**
   ok pasif, ilk kayıt gününde **sol** ok pasif) — değiştirilmedi. Çevrilen
   şey **dil**: ipucu şeridi artık "Geçmiş günler solda. Sağa kaydır."
   **Kanal ayrımı bilinçli:** ok ve ikon daima **sayfanın** yönünü gösterir
   (sol = geçmiş), **jest** yönü yalnız yazıyla söylenir. İkisini aynı
   kanaldan anlatmak (sağa bakan ok + sola giden sayfa) çelişki üretirdi.
   G3 yüzeyinin adı "sola kaydırma sınırı" → **"sol uç · geriye sınır"**.
   E-24'ün dili hizalandı (sol = geçmiş; bugünün ayında sağ ok pasif).
2. **Seri çipinde birim geri: "Seri 12 gün"** (K-054/7). İskelet genişliği
   84 → **104px**. Ölçüm: çip 104 + takvim 44 + aralar 16 = 164; en uzun
   başlık `03/09 Perşembe` 218 → **338 ≤ 358** ✅. Başlıktaki üç hedef
   (tarih · seri · takvim) çakışmıyor, hepsi ≥44pt.
3. **Kategori satırında tek zaman ölçeği.** Birincil sağ değer artık
   **aylık toplam / aylık limit** (çubukla aynı ölçek); "bugün 95 ₺"
   ikincil satıra indi, yanında "kalan 260 ₺" ya da "140 ₺ limit dışı".
   Kart alt başlığı "Bugünkü tutar · aylık limit" → **"Bu ay · kategori
   limiti"** (tek satır). "Tümünü gör" düğmesi `flex:0 0 auto` + tek satıra
   kilitlendi — uzun alt başlıkla iki satıra sarıp kart başlığını bozuyordu.
   Uydurma **günlük kategori limiti** yine üretilmedi (K-050).
4. **"Limit altı günlerde biriken" tanımı yazıya geçti** → aşağıdaki
   "Yeni metinler" bölümü, `ozet.biriken.tanim`.

## tokens eklentileri

| # | Bölüm | Eklenecek |
|---|---|---|
| 12 | §3.1 dikey ritim | **12**'nin rol metni genişliyor: "kartın **ya da formun** içinde iki bağımsız blok". Kullanıldığı yerler: iki etiketli form alanı arası · "ya da" ayracının iki yanı. Yeni boşluk değeri üretilmedi. |
| 13 | §1.9 kontrast (hesaplandı) | `primary-text`/`bg` **5.12** AA (yasal bağlantı) · `danger-ink`/`bg` **4.97** AA (alan hatası metni) · `success-ink`/`bg` **4.24** — yalnız **grafik** (onay ikonu, eşik 3:1), metin olarak kullanılmadı · **BİLİNEN SINIR:** `success #16A34A`/`bg` **2.85** ❌ (ham yeşil bu zeminde kullanılmaz) · `line`/`bg` **1.08** → sayfa zemininde hairline ayraç **görünmez**, üretilmez. |
| 14 | §7.1 buton | 4. varyant **`button.social`**: yükseklik 56 · radius 999 · `clay.raised` → `clay.pressed` · logo 20pt + 8 boşluk · tam genişlik. **Dolgu, logo ve etiket palet dışıdır** (üçüncü taraf marka kilidi) — tek istisna ve `stil.css`'in "ÜÇÜNCÜ TARAF" bloğunda toplanmıştır: Apple zemin `#000000`, glif+etiket `#FFFFFF`, basılı `#1A1A1A` · Google zemin `#FFFFFF`, etiket `#1F1F1F`, 1px `#747775` kontur, G glifi `#4285F4`/`#34A853`/`#FBBC05`/`#EA4335`, basılı `#F2F2F2`. |
| 15 | §7.1 `button.secondary` | `disabled` hâli ilan edildi: zemin `disabled-bg`, metin `text-2`, gölge `clay.sunken`, **opaklık yok** (E-22 "Yeniden gönder"). |
| 16 | §9 ikon | Lucide setine 5 glif: `eye` · `eye-off` · `log-out` · `wifi-off` · `mail-check`. **Yeni set yok, yeni boyut yok** (20/22/24 mevcut). Hepsi 390px'te ayrı ayrı render edilip okunabilirlik doğrulandı. |
| 17 | §12 denetim listesi | Madde 1 (`#000000`) ve 27 (palet dışı hue) için **kapsam notu**: üçüncü taraf marka düğmeleri istisnadır; ham değerler `<main>` içinde değil, `stil.css`'te sınıf olarak durur (`.btn-apple`, `.btn-google`, `.g-*`). `denetim.py` **değiştirilmedi** — istisna koda gizlenmedi, yapıya yazıldı. |
| 18 | §2.3 metin kuralları | "Buton 1-3 kelime, fiil önce" kuralı **üçüncü taraf etiketlerinde geçmez**: "Apple ile Devam Et" (Apple'ın yerelleştirmesi, başlık düzeni onun) ve "Google ile devam et" kısaltılamaz, yeniden yazılamaz. |

## Yeni bileşenler

`bilesen-envanteri.md` sayımı: **45 → 52** (7 yeni).

| Bileşen | Ekran | Durumlar |
|---|---|---|
| `SocialAuthButton` | E-22 · E-23 | `default` / `pressed` / `busy`. Apple ve Google varyantı. **iOS'ta Apple varyantı bizim bileşenimiz değildir** (bkz. RN notu 1). |
| `PasswordField` | E-22 · E-23 | `TextField`'ın sağ yuvalı varyantı: `default` / `focused` / `error` / `visible` / `hidden`. Göz düğmesi 44pt, alanın sağ iç boşluğu 16 → 8. |
| `PasswordRuleLine` | E-23 | `unmet` (caption) / `met` (20pt `check` + caption). **Renkli güç çubuğu yok.** |
| `OrDivider` | E-22 · E-23 | Tek durum. Çizgi yok, ortalanmış tek sözcük. |
| `LegalConsentText` | E-23 | `default` / `pressed` (bağlantı rengi `primary-press`). RN: iç içe `Text` + `hitSlop`. |
| `AccountSection` | E-19 | `signed-in` (e-posta çukuru + sağlayıcı satırı + Çıkış yap + Hesabı sil) / `signed-out` (tek nötr satır). |
| `ResetSentCard` | E-22 | `default`. İçinde `button.secondary` `disabled` + gerekçe satırı. |

`TextField` satırına eklenecek: **sağ yuva (trailing slot)** — 44pt ikon
düğmesi alabilir; yeni bileşen değil, mevcut alanın varyantı.
`DestructiveConfirmDialog` yeni değil (E-13/E-19'dan) — E-19'da **ikinci
örneği** doğdu: hesabı sil.

## Yeni metinler

| Anahtar | Metin |
|---|---|
| `hesap.mahremiyet` | Harcamaların sende kalır. Hesap yalnız seni tanır. |
| `hesap.mahremiyet.ek` | Yedekleme sonraki sürümlerde. |
| `giris.baslik` | Giriş yap |
| `giris.eylem` / `.mesgul` | Giriş yap · Giriş yapılıyor |
| `giris.hesapsiz` | Hesapsız devam et |
| `giris.ayirac` | ya da |
| `giris.sosyal.apple` | Apple ile Devam Et *(Apple'ın yerelleştirmesi — değiştirilemez)* |
| `giris.sosyal.google` | Google ile devam et *(Google'ın yerelleştirmesi — değiştirilemez)* |
| `alan.eposta` / `.eposta_ph` | E-posta · ornek@eposta.com |
| `alan.sifre` / `.sifre_ph.giris` / `.sifre_ph.kayit` | Şifre · Şifreni yaz · Şifre belirle |
| `alan.sifre.gorunur` / `.gizli` | Şifreyi göster · Şifreyi gizle *(a11y)* |
| `giris.unuttum` | Şifremi unuttum |
| `giris.kayit_kapisi` | Hesap oluştur |
| `hata.eposta_bicim` | Geçerli bir e-posta yaz. |
| `hata.kimlik` | E-posta ya da şifre yanlış. Yeniden dene. |
| `hata.eposta_bos` | Önce e-postanı yaz. |
| `hata.baglanti.giris` | Giriş için bağlantı gerekir. Kayıtların bağlantısız çalışır. |
| `hata.baglanti.kayit` | Hesap açmak için bağlantı gerekir. Kayıtların bağlantısız çalışır. |
| `sifirla.baslik` / `.govde` / `.ipucu` | Bağlantıyı gönderdik · {eposta} adresine şifre bağlantısı gitti. · Gelmediyse istenmeyen klasörüne bak. |
| `sifirla.yeniden` / `.bekle` | Yeniden gönder · 60 saniye sonra yeniden gönderebilirsin. |
| `sifirla.geri` | Girişe dön |
| `kayit.baslik` | Hesap oluştur |
| `kayit.eylem` / `.mesgul` | Hesap oluştur · Hesap oluşturuluyor |
| `kayit.sifre_kural` / `.sifre_kural_tamam` | En az 8 karakter. · Uzunluk yeterli. |
| `kayit.yasal` | Hesap oluşturarak **Kullanım şartları** ve **Gizlilik politikasını** kabul ediyorsun. |
| `kayit.giris_kapisi` | Hesabın var mı · Giriş yap |
| `hata.eposta_kayitli` | Bu e-posta ile hesap var. Giriş yap. |
| `ayar.hesap.baslik` | Hesap |
| `ayar.hesap.aciklama` | Hesap yalnız girişte seni tanımak için. |
| `ayar.hesap.eposta` | E-posta |
| `ayar.hesap.saglayici` | Google ile bağlı. *(varyant: Apple ile bağlı. · Şifre ile bağlı.)* |
| `ayar.hesap.cikis` / `.cikis_not` | Çıkış yap · Çıkınca kayıtların sende kalır. |
| `ayar.hesap.sil` | Hesabı sil |
| `ayar.hesap.kapali` / `.kapali_kapi` | Hesap isteğe bağlı. Kayıtların sende kalır. · Giriş yap ya da hesap oluştur |
| `hesapsil.baslik` / `.govde` | Hesabın silinecek · Geri alınamaz. Bu e-posta ile bir daha giriş yapamazsın. |
| `hesapsil.veri` | {n} kayıt sende kalır. Silmek istersen Veri bölümünü kullan. |
| `hesapsil.eylem` | Hesabı sil |
| `gunluk.ipucu` **(değişti)** | Geçmiş günler solda. Sağa kaydır. |
| `gunluk.grup.alt` **(değişti)** | Bu ay · kategori limiti |
| `gunluk.grup.bugun` / `.kalan` / `.limit_disi` | bugün {tutar} · kalan {tutar} · {tutar} limit dışı |
| `seri.cip` **(değişti)** | Seri {n} gün *(birim geri kondu, K-054/7)* |

### `ozet.biriken.tanim` — "Limit altı günlerde biriken" (T-1'den devreden açık kalem)

**Formül:** `biriken = Σ (o günün günlük limiti − o gün harcanan)`, yalnız
**limit altında kapanan** günler için.

| Kural | Değer |
|---|---|
| Hangi günler sayılır | Gün kapanmış **ve** harcanan ≤ o günün limiti |
| Limit dışı günler | **0 sayılır** — negatif değer toplama eklenmez (kayıp "geri ödenmez") |
| O gün limiti yoksa | Gün hesaba **girmez** (limitsiz günün artanı tanımsızdır) |
| Kayıt yazılmamış gün | Girmez — "harcamasız" işaretli gün de girmez (K-048 hile kapısının aynı gerekçesi) |
| Pencere | Gösterildiği ekranın penceresi: E-24'te **görüntülenen ay**, E-16'da hafta |
| Ne DEĞİLDİR | Banka birikimi değil, gerçekleşmiş tasarruf iddiası değil. Arayüz metni **"biriken"** der; "tasarruf ettin", "kazandın" yazılmaz |
| UI açıklaması | `ozet.biriken.aciklama` = "Limit altında kapattığın günlerde artan tutarların toplamı." + "Limit dışı günler sıfır sayılır." |

Kaynak: brandbook §2.4 "Tasarruf kipi"nin tanımıyla aynıdır; bu tur onu
**formüle** çevirdi. PM `metinler.md` + `tokens.md` §7'ye işleyecek.

## RN inşa notları

1. **Apple düğmesini iOS'ta BİZ ÇİZMEYİZ.** `expo-apple-authentication`
   → `AppleAuthenticationButton` (style `BLACK`, type `CONTINUE`, cornerRadius
   28). Doğru glif, doğru yerelleştirme, doğru dokunma davranışı garanti.
   Prototipteki çizim onun **yer ölçüsüdür** (56pt yükseklik, tam genişlik).
2. **Google düğmesi bizim `Pressable`'ımızdır**; logo `react-native-svg` ile
   4 `Path`, renkler `src/theme/brand.ts`'ten gelir — **tema tokenlarından
   değil.** Bu ayrım kodda da korunur: marka varlığı tema değildir.
   SDK: `@react-native-google-signin/google-signin`.
3. **Klavye:** bu iki ekran kil tuş takımını kullanamaz (e-posta/şifre) →
   `KeyboardAvoidingView` (iOS `padding`, Android `height`) **zorunlu**;
   alt sabit blok klavyenin üstünde kalır. `ScrollView`
   `keyboardShouldPersistTaps="handled"` (göz düğmesi ilk dokunuşta çalışsın).
4. **`TextInput` özellikleri:** `autoCapitalize="none"` ·
   `keyboardType="email-address"` · `autoComplete="email" | "current-password"
   | "new-password"` · `textContentType` eşleniği · `secureTextEntry` ·
   `importantForAutofill="yes"`. Şifre yöneticileri çalışmalı; kendi
   "şifreyi yapıştırma" engelimiz **yok**.
5. **Göz düğmesi** yalnız `secureTextEntry`'yi çevirir; odak kaybolmaz
   (alan `blur` edilmez), imleç konumu korunur.
6. **Yasal bağlantılar:** iç içe `Text` + `onPress` + `accessibilityRole="link"`
   + `hitSlop={{top:12,bottom:12}}`. 12pt satırı 44pt kutuya çevirmek cümleyi
   parçalardı.
7. **Hata modeli alan düzeyindedir:** 400/biçim → e-posta alanı · 401 →
   şifre alanına **genel** mesaj · 409 → e-posta alanı · ağ/timeout →
   ekran üstü `warning` şeridi (hiçbir alana bağlanamaz).
8. **Hesap silme sunucu tarafı ister.** Supabase Auth'ta kullanıcıyı silmek
   `service_role` gerektirir → küçük bir **Edge Function** yazılacak
   (App Store 5.1.1(v) şartı). Maliyet ücretsiz katmanda; bkz. 🔴 4.
9. **Oturum** `expo-secure-store`'da (refresh token); **harcama verisi
   `expo-sqlite`'ta kalır ve çıkışta SİLİNMEZ.** Hesap silmek de yerel
   veriyi silmez — iki işlem iki ayrı kapıdır.
10. **Klavye açık yüzeyler prototipte "kaydırılmış" çizildi:** kaydırma alanı
    844 − 47 − 116 − 28 − 224 = **429px**; görünen içerik E-22'de 401,
    E-23'te 383 → alt kesme her ikisinde **24'lük boşluk bandına** düşer,
    hiçbir alan ortasından dilimlenmez (tokens §12/11c).

## Bilinçli tasarım kararları (design-reviewer için)

1. **"Kayıt ol" değil "Hesap oluştur".** `metinler.md` §0.1 "kayıt"ı
   **harcama kaydı** için kilitledi ("214 kayıt"). "Kayıt ol", ürünün en sık
   kullanılan sözcüğünü ikinci bir anlama bağlardı. Ekran kodu E-23 "Kayıt"
   olarak kalır; **arayüz metni** Hesap oluştur.
2. **Sosyal düğmeler formun üstünde, Apple üstte** (iOS). Geri dönen
   kullanıcı için en kısa yol; App Store 4.8 eşit görünürlük istiyor.
   Android derlemesinde sıra tersine döner — platform kuralı, tercih değil.
3. **Marka uzlaşması: "kap bizim, içerik onların".** Kap ölçüsü, geometrisi
   ve gölgesi tokens §7.1; dolgu/logo/etiket sağlayıcının. Apple'ın **siyah**
   stili seçildi: beyaz stil de **siyah** glif ve etiket isterdi (yani
   `#000000` yine ekranda olurdu), siyah stil ise 21:1 kontrast verir ve en
   tanınan hâldir. Kil dilinin sınırı burada **kabul edildi**: lacivert iç
   gölge siyah üzerinde görünmez, `pressed` geri bildirimini **zemin tonu**
   taşır.
4. **"ya da" ayracında çizgi yok.** `line` sayfa zemininde 1.08:1 —
   görünmeyen bir çizgi çizmek yerine boşluk ayırıyor. Clay dilinde ayraç
   oluktur, saç teli değil.
5. **Şifre gücü göstergesi üretilmedi.** Renkli zayıf/orta/güçlü çubuğu ve
   dört maddelik onay listesi klişedir; ölçtüğü şey (entropi) kullanıcının
   anladığı şey değildir ve K-050'nin yasakladığı **sahte skor** mantığının
   aynısıdır. Tek kural (8 karakter), tek satır, karşılanınca onay ikonu.
6. **İki hata mesajı bilerek farklı ayrıntıda.** E-22'de kimlik hatası
   **genel** ("E-posta ya da şifre yanlış") — hangi adreslerin kayıtlı
   olduğunu sızdırmamak için. E-23'te ise **açık** ("Bu e-posta ile hesap
   var"), çünkü adresi kullanıcının kendisi yazdı ve çözüm iki satır aşağıda.
7. **Çıkış yap için onay diyaloğu YOK, hesap silme için VAR.** Çıkmak geri
   alınabilir ve kayıtlara dokunmaz; sebebi düğmenin altında tek satır
   yazılı. Her eyleme diyalog koymak diyalogların anlamını tüketir.
8. **Hesap bölümü ekranın başında değil, Veri'nin üstünde.** Hesabı en üste
   koymak, K-052'nin "hesap zorunlu değil" kararının tersini söyleyen bir
   hiyerarşi kurardı. Kimlik ve veri komşu durur: kullanıcının sorusu
   ikisinde de aynı — "kayıtlarıma ne oluyor?"
9. **Şifre sıfırlama ayrı ekran değil**, E-22'nin bir durumu: adres zaten
   ekranda. Ayrı ekran, üçüncü bir başlık ve ikinci bir e-posta alanı
   üretirdi.
10. **`success-ink` ikon olarak kullanıldı, metin olarak kullanılmadı**
    (zemin `bg`: 4.24 grafik ✅, metin eşiğinin altında değil ama tokens
    §1.3 success-ink'i `surface`'e kilitliyor). Yeşil **işarettir**, cümle
    değildir: metin `text-2` kalır.
11. **Hesap silme diyaloğunun asıl işi bir soruyu cevaplamak:**
    "kayıtlarıma ne olacak?" Cevap ekranda ve ayrım net — hesap gider,
    **kayıtlar kalır**; veri silmek isteyene ayrı yol gösterilir.

## 🔴 Çelişkiler

1. **tokens §12/24 + brandbook §2.8 ("depolama/mimari anlatan arayüz metni
   YASAK") ↔ K-052 + bu turun brief'i ("dürüst mahremiyet ifadesi
   zorunlu").** Sessizce çözmedim: cümleyi **kullanıcı diline** yazdım ve
   mimari sözcüğü kullanmadım — "Harcamaların sende kalır. Hesap yalnız
   seni tanır." Bu, E-19'da **zaten onaylı** olan "Kayıtların sende kalır."
   satırının aynı dilidir; "cihaz / sunucu / senkron / yedek" geçmiyor.
   **PM'den istenen:** §2.8'in yasağı "teknik sözcükler" olarak
   daraltılsın; "sende kalır" biçimi **izinli** yazılsın. Aksi hâlde
   denetim bu iki ekranı kural ihlali sayar.
2. **Apple/Google logoları palet ve varlık kilidinin dışındadır.** Brief
   istisnayı verdi, ama `varliklar.md` (P-6) hâlâ "tek ikon seti + 4 font,
   kilitli" diyor. **`varliklar.md`'ye "üçüncü taraf marka varlıkları"
   bölümü eklenmeli** (kaynak, izinli stiller, değiştirilemezlik kuralı),
   yoksa sonraki denetim bunu ihlal olarak okur.
3. ~~**Apple girişi Android'de ne olacak?**~~ → **KAPANDI, Mustafa kararı
   (2026-09-17):** *"Android'de Google ile giriş olsun sadece, iOS'ta Apple
   ile giriş de olsun."* Uygulandı, bkz. aşağıdaki "Platform kuralı" bölümü.
   PM'in bunu `DECISIONS.md`'ye yeni bir K maddesi olarak işlemesi gerekiyor
   (tasarım tarafı bitti, kayıt eksik).
4. **Hesap silme sunucu tarafı kod gerektiriyor** (Supabase Edge Function,
   `service_role`). K-052 "kendi sunucumuzu yönetmiyoruz" diyor; bu tek
   fonksiyon o ifadeyi teknik olarak zorlar. Maliyet ücretsiz katmanda,
   ama **iş kalemi olarak kayda geçmeli** — App Store 5.1.1(v) şartı.
5. **Buton kelime sınırı ihlali (zorunlu).** `metinler.md` §0: buton 1-3
   kelime, fiil önce. "Apple ile Devam Et" 4 kelime ve fiil sonda; marka
   kilidi bizim kuralımızı yener. §0'a istisna satırı gerekiyor.
6. **`metinler.md` §0.1 "giriş" sözcüğünü yasaklıyor** ("kayıt | veri,
   giriş, entry") — ama oturum açma bağlamında "Giriş yap" kaçınılmaz.
   Ayrım yazıya geçsin: **"giriş" = oturum açma**; harcama kaydı için asla
   kullanılmaz. Şu an aynı sözlük iki şeyi yasaklamış görünüyor.
7. **Gizlilik politikası ve kullanım şartları metinleri yok** (K-052 bunları
   şart koşuyor). E-23'teki iki bağlantı **yer tutucudur**; metinler
   yazılmadan App Store'a çıkılamaz. Sahibi: PM / `brand-strategist`.
8. **Devralınan kesme:** `01-gunluk.html` A2 yüzeyinde kaydırma kesmesi bir
   liste satırının ortasına düşüyor (T-1'den gelir; bu turdaki değişikliğim
   kesme konumunu **değiştirmedi**, ipucu şeridi tek satırda tutuldu).
   Tokens §12/11c'ye tam uymak için A2'nin listesinden bir satır düşmek
   gerekir — içerik kararı olduğu için **PM'e bırakıldı**, sessizce
   kırpmadım.

## Anti-pattern öz-denetimi (E-22 · E-23 · Hesap · madde madde)

| Anti-pattern | Durum |
|---|---|
| Mor-mavi varsayılan gradyan | ✅ Tek gradyan `grad.action` (marka mavisi), yalnız birincil buton/FAB. Sosyal düğmelerde gradyan yok. |
| Her elementte glassmorphism | ✅ Bulanıklık yok; dil kil (kabarık form kabı, çukur alan kuyusu). |
| Amaçsız drop-shadow | ✅ Gölge anlam taşır: alan **çukur** (buraya değer girer), düğme **kabarık**, basılı **içe çöker**. Siyah Apple düğmesinde kil gölgenin sınırı delta'ya yazıldı. |
| Karışık köşe yarıçapı | ✅ 999 (buton/çip) · 16 (alan, e-posta kuyusu, şerit) · 24 (kart/diyalog). Yeni radius yok. |
| Inter/Poppins/Montserrat "varsayılan" | ✅ Font eklenmedi; Poppins yalnız h1/h2, Montserrat gövde/rakam. Sosyal düğme etiketi de Montserrat SemiBold (Roboto eklemek varlık kilidini kırardı — delta'da açık). |
| 3 sütunlu daire ikon + başlık + 1 cümle | ✅ Hiçbir yüzeyde yok. Hesap bölümü satır ritminde. |
| Stok illüstrasyon | ✅ Yok. "Bağlantıyı gönderdik" kartı 44pt kil kuyu + ikon, çizim değil. |
| Kimliksiz aşırı beyaz boşluk | ✅ Ritim 4/8/12/16/24; E-22 varsayılanı 751px yüksekliğinde dolu, ekran boş kalmıyor. |
| Jenerik pazarlama dili | ✅ "Hesabını koru", "Daha fazlasını keşfet", "Elevate" yok. Cümleler tespit + eylem. Övgü ve ünlem yok. |
| Düşük kontrast gri metin | ✅ Tüm etkin metin AA: `text-2`/`bg` 5.13 · `primary-text`/`bg` 5.12 · `danger-ink`/`bg` 4.97 · `text-3` yalnız placeholder. |
| Rastgele boşluk | ✅ `denetim.py` 16 sayfada 0 bulgu (boşluk/punto/radius taraması). |
| Dark mode renk tersleme | ✅ Karanlık mod üretilmedi (Faz 2), jetonu da yok. |
| Emoji | ✅ Yok; tarama temiz. Tek ikon seti Lucide (+ iki üçüncü taraf logosu, kılavuzlarına uygun). |
| Hover | ✅ Hiç `:hover` yok. `pressed` çizilenler: Apple düğmesi · Google düğmesi (CSS'te) · göz düğmesi · Şifremi unuttum · Giriş yap (ghost) · yasal bağlantı · Çıkış yap · Hesabı sil · Hesap kapısı satırı. |
| CSS grid / `::before` / `sticky` / `calc` / `vh` | ✅ Yalnız flexbox; tarama 0 bulgu. |
| Giriş duvarı (ürün anti-pattern'i) | ✅ "Hesapsız devam et" her iki ekranda, 44pt, tam genişlik — dipnot değil. Hesap hiçbir özelliği kilitlemiyor (K-052). |

## Platform kuralı — sağlayıcı kümesi (Mustafa kararı, 2026-09-17)

> *"Android'de Google ile giriş olsun sadece, iOS'ta Apple ile giriş de
> olsun."* → uygulandı; delta'nın 🔴 3. maddesi kapandı. PM bunu
> `DECISIONS.md`'ye bir K maddesi olarak işlemeli.

| Platform | Sağlayıcılar | Gerekçe |
|---|---|---|
| **iOS** | **Apple + Google** (Apple üstte) + e-posta/şifre | App Store kuralı 4.8: üçüncü taraf girişi sunan uygulama Apple girişini **zorunlu** sunar. Platform beklentisi de budur. |
| **Android** | **yalnız Google** + e-posta/şifre | Kural yalnız iOS'u bağlar. Android'de Apple akışı **web köprüsü** ister (ek iş, ek hata yüzeyi, tarayıcı sıçraması). Yarım çalışan bir düğme, hiç olmayan düğmeden kötüdür. |

**Apple ile açılmış hesap Android'de nasıl açılır** (yeni ekran
gerekmedi): Apple'ın verdiği — gerekirse gizlenmiş (`privaterelay`) —
e-posta adresi hesabın **kimliğidir**. Kullanıcı E-22'deki **"Şifremi
unuttum"** ile o adrese bağlantı ister, şifre belirler, e-posta/şifre ile
girer. Var olan kurtarma yolu bu boşluğu zaten kapatıyor; Android'de
"hesabım açılmıyor" çıkmaz sokağı oluşmuyor.

**Tasarım etkisi:** `lib.sosyal_kume(platform=...)` tek parametreyle iki
hâli üretir. Android'de küme 120 → **56pt**'ye iner; "ya da" ayracı, form
ve alt sabit blok yerinde kalır, ekran kısalır (E-23 Android'de **tek
ekrana sığar**, kaydırma gerekmez). Yeni yüzeyler: `15-giris.html`
**8. durum**, `16-kayit.html` **7. durum** ("Android derlemesi · yalnız
Google"). Toplam: **16 sayfa · 94 yüzey · 0 bulgu.**

**RN inşa notu (1. maddenin eki):** sağlayıcı listesi
`Platform.select({ios: ['apple','google'], android: ['google']})` ile
kurulur; Apple bileşeni Android paketine **hiç bağlanmaz**
(`expo-apple-authentication` yalnız iOS'ta `isAvailableAsync()` true).
Hesap e-postası aynı olduğu için Supabase tarafında **tek kullanıcı
kaydı** kalır — sağlayıcı bağlama (identity linking) Faz 1'de açılmaz;
kullanıcı Android'de şifre belirleyince aynı hesaba ikinci bir yöntem
eklenmiş olur.

---

# T-3 — Profilleme (Katman 1 + Katman 2) + "Planın hazır"

> Kaynak kararlar: **K-053** (iki katmanlı onboarding, plan ekranı,
> yasaklar) · **K-050** (fiyat uydurma yasağı) · **K-057/6** ("Oturum aç")
> · **K-057/8** (kaydırma kesmesi) · **K-040** (yazılı olmayan sayı iki kez
> kodlanır → bu bölümdeki **bütün formüller yazılı**).
>
> Üretilen/değişen dosyalar:
> `prototip-v4/03-onboarding.html` (yeniden yazıldı) ·
> `prototip-v4/17-tanisma.html` (**yeni**, E-25) ·
> `prototip-v4/18-plan.html` (**yeni**, E-26) ·
> `11-ayarlar.html` (+ "Plan ve profil" bölümü) ·
> `01-gunluk.html` (A2 kesme hizası) · `15-giris.html` · `16-kayit.html`
> (sözcük) · `stil.css` · `index.html`.
> **18 sayfa · 115 yüzey · denetim 0 bulgu.**

## Ekran akışı (ekran-envanteri.md'ye eklenecek)

```
E-01..E-03  Katman 1 (ZORUNLU, 3 soru)
            niyet -> aylık net gelir (ATLANABİLİR) -> maaş günü
                     |
                     v  "Başla"
E-10        Günlük — uygulama ÇALIŞIR. Günlük limit henüz YOK (limitsiz kip).
                     |
     +---------------+----------------------------------+
     |  E-10'daki nötr "Limit belirle" kapısı (K-054/5)  |
     |  Ayarlar > Plan ve profil                         |
     v                                                   v
E-25 Seni tanıyalım (KATMAN 2, 8 kart, hepsi atlanabilir)   E-17 Limitler
     her an bırakılır -> "Kaldığın yerden" yüzeyi           (limiti elle yaz)
                     |
                     v  "Planı gör"
E-26 Planın hazır -> "Planı kur" -> günlük limit E-10'a yazılır
```

E-25 ve E-26 **sekme çubuğu taşımaz** (arketip C/F+ akış ekranları).
E-26'ya üç giriş vardır: Katman 2'nin sonu · "Kaldığın yerden" yüzeyinin
"Planı şimdi gör" çıkışı · Ayarlar > Plan ve profil > "Planı gör".

## FORMÜLLER (bağlayıcı — kodda tek kaynak)

Para daima **kuruş cinsinden integer**; yuvarlama yalnız **gösterimde**.

| # | Büyüklük | Formül |
|---|---|---|
| 1 | `zorunlu_kurus` | Σ (kira_aidat + faturalar + ulasim_yakit + kredi_taksit) — **yalnız kullanıcı girdisi**, boş alan 0 sayılır |
| 2 | `birikim_kurus` | `gelir_kurus × birikim_yuzde / 100` |
| 3 | `sosyal_kurus` | `gelir_kurus − zorunlu_kurus − birikim_kurus` |
| 4 | `birikim_yuzde` üst sınırı | `100 − zorunlu_yuzde` (bu noktada `sosyal_kurus = 0`) |
| 5 | `zorunlu_yuzde` vb. | `pay_kurus × 100 / gelir_kurus`, **tam sayıya** yuvarlanır; üç yüzdenin toplamı **en büyük kalan** yöntemiyle 100'e tamamlanır |
| 6 | `kalan_gun` | maaş gününden kurulan dönemde **bugün dahil** kalan gün sayısı. Maaş günü ayda yoksa (31 → Şubat) **ayın son günü** kullanılır. Maaş günü "Düzensiz" ise dönem **30 gün** kabul edilir |
| 7 | `gunluk_limit_kurus` | `sosyal_kurus // kalan_gun` → **gösterimde tam liraya AŞAĞI** yuvarlanır (`// 100 × 100`). Yukarı yuvarlamak limiti her gün bir miktar aşındırır |
| 8 | `aliskanlik_aylik_kurus` | `siklik_gunluk × fiyat_kurus × 30`. Haftalık seçenekte `siklik_gunluk = haftalik / 7`; "Ayda 1-2" seçeneğinde doğrudan `siklik_aylik × fiyat_kurus`. "Hiç" → kalem **hiç üretilmez** (0 ₺ satırı yazılmaz) |
| 9 | `yatirim_payi_kurus` | `birikim_kurus × yatirim_yuzde / 100` — **yalnız etiket**, ayrı bir kova değil |
| 10 | Negatif kalan | `zorunlu_kurus > gelir_kurus` ise plan **kurulmaz**; ekranda `zorunlu − gelir` tutarı **"1.400 ₺ eksik"** biçiminde yazılır (negatif sayı gösterilmez, metinler §0) |

**Prototipteki örnek kullanıcı (tüm yüzeylerde aynı):** gelir 32.000 ₺ ·
sabit giderler 12.500 + 2.840 + 1.900 + 1.560 = **18.800 ₺** · birikim %15
= 4.800 ₺ (yatırım payı %40 = 1.920 ₺) · sosyal/keyfi **8.400 ₺** · maaş
günü ayın 15'i, 17 Eylül'de kalan gün **28** → günlük limit
**8.400 ÷ 28 = 300 ₺**. Bu sayı v4'ün tüm diğer ekranlarındaki
"Günlük limit 300 ₺" ile **kasten** birebir aynıdır; plan ekranı
prototipin geri kalanıyla çelişmiyor.

**Alışkanlık maliyeti:** kahve 2.700 · dışarıda yemek 1.629 · alkol 943 ·
abonelikler 520 → **5.792 ₺** (sosyal/keyfi payının %69'u). Sigara "Hiç"
seçildiği için **listede yok**.

## tokens eklentileri

| Ekleme | Değer | Gerekçe |
|---|---|---|
| `share.zorunlu` | `primary-deep #2F68C5` | Zorunlu pay = taahhüt edilmiş kısım, hue ailesinin koyu ucu |
| `share.sosyal` | `primary #3B82F6` | **Günlük limit bu paydan çıkar**; kahraman yayın rengiyle aynı → renk zinciri kuruyor. Metin taşımıyor, §1.6 ihlali değil |
| `share.birikim` | `success #16A34A` | 🔴 **PM onayı gerek:** tokens §1.3 `success`'i "onay ikonu dolgusu, limit altı mini gösterge" ile sınırlıyor; bu **yeni bir grafik bağlam**. Alternatifi kategori renklerini ödünç almaktı, o §1.4'ü ("aile rengi grup bilgisi taşır") kırardı |
| `slider.track` / `knob` / `row` | **12 / 32 / 44** | Oluk kalınlığı mevcut çubuklarla aynı (12), satır dokunma hedefi 44 |
| `slider.max-stop` | `warning-soft` zemin | Üst sınır bir **hata değil**; `danger` dört bağlamla sınırlı |
| Yüzde biçimi | `%59` (işaret önce, boşluk yok) | 🔴 metinler §18 ile çelişiyor, aşağıda |
| `.gun-kutu.secili` | `primary-deep` + `grad-action` + beyaz etiket | Seçili gün **dolgu + kabartma**, halka YOK (K-054/6). `.altinda` limit bilgisi taşır; aynı görünümü iki anlama bindirmemek için ayrı sınıf |
| `denklem-kutu` iç boşluğu | **8** (16 değil) | 326px'e üç kutu + iki 16'lık işleç sütunu sığacak. Ölçüldü: en uzun tutar "18.800 ₺" = 74.2px, kutu içi 82px. 8 zaten skalada (§3) |

## Yeni bileşenler (bilesen-envanteri.md'ye eklenecek)

| Bileşen | Ölçü / yapı | Durumlar |
|---|---|---|
| **`Slider`** (kaydırıcı) — *yeni tip* | oluk 12 · topuz 32 · satır 44 · dolgu topuzun **merkezinde** biter | `default` · `pressed` (topuz çöker, groove) · `max` (topuz durur, `warning-soft`) · `disabled` (gelir yoksa hiç çizilmez, pasif bırakılmaz) |
| **`ShareBar`** (pay çubuğu) | tek oluk · 3 segment · aralar **4pt**, oluk aradan görünür | 3 pay · 2 pay (birikim girilmedi) · `loading` (tek çukur blok) |
| **`ShareRow`** (pay satırı) | 8pt nokta + ad + açıklama + sağda ₺ / % | dolu · `Girilmedi` (yüzde **%0 yazılmaz**) |
| **`EquationRow`** (denklem) | 3 çukur kutu + `÷` `=` · sonuç kutusu **kabarık + `primary-soft`** | dolu · `loading` |
| **`ProgressBar`** (Katman 2) | oluk 8 + dolgu + `n/8` metni | 1/8 … 8/8 · 4/8 (dönüş) |
| **`ValueWellRow`** (`kuyu_deger`) | çukur satır · etiket + değer + chevron · padding 12/16 | dolu · boş (`Girilmedi` / `Fiyatını yaz` — **placeholder rengi değil**, geçerli durum) · `pressed` · `focused` (2pt `primary-text` + imleç) |
| **`FrequencyChips`** | sarmalı çip satırı · **serbest sayı en sonda** | seçili (çukur) · `pressed` · "Hiç" (fiyat alanını kapatır) |
| **`MirrorWell`** (ayna kuyusu) | çukur · "Ayda X ₺" + altında **formül satırı** | dolu · yok (soru cevaplanmadıysa hiç çizilmez) |
| **`NeutralIconBox`** (`ikon_kab`) | 48×48 · radius 16 · `primary-soft` + `primary-text` | tek durum |

`Slider` **RN'de platform bileşeniyle kurulmaz** (`@react-native-community/
slider` iOS/Android'de farklı çizer ve clay dili uygulanamaz) →
`PanResponder` + üç `View`. **Yeni kütüphane eklenmiyor.**

## Yeni metinler (metinler.md'ye eklenecek)

**Katman 1 (E-02 / E-03 yeniden yazıldı):**

| Anahtar | Metin |
|---|---|
| `ob.gelir.baslik` | Aylık net gelirin ne kadar |
| `ob.gelir.aciklama` | Planı buna göre kuruyoruz. İstemezsen atla. |
| `ob.gelir.etiket` | Aylık net gelir |
| `ob.gelir.net` | Eline geçen tutar. Kesintiden sonrası. |
| `ob.gelir.bos` | Kesin olması gerekmiyor. Yaklaşık yeter. |
| `ob.gelir.mahremiyet` | Gelirin telefonunda kalır. |
| `ob.gelir.atlarsan` | Atlarsan günlük limiti sen yazarsın. |
| `ob.gelir.atla` | Atla |
| `ob.maas.baslik` | Maaşın hangi gün yatıyor |
| `ob.maas.aciklama` | Günlük limit maaş dönemine bölünür. |
| `ob.maas.duzensiz` | Düzensiz geliyor |
| `ob.maas.donem` | Dönem ayın {gun}'inde başlar. Limit kalan güne bölünür. |
| `ob.maas.duzensiz.not` | Dönem 30 gün sayılır. Maaş günü değişirse ayarlardan düzeltebilirsin. |
| `ob.ozet.limit_yok` | Henüz yok |
| `ob.ozet.limit_not` | Günlük limiti plan kurunca ya da elle yazınca belirlersin. |

**Katman 2 (E-25):**

| Anahtar | Metin |
|---|---|
| `tan.baslik` | Seni tanıyalım |
| `tan.aciklama` | Sekiz kart. Her birini atlayabilirsin. |
| `tan.fiyat_vaadi` | Fiyatları biz tahmin etmiyoruz. |
| `tan.fiyat_vaadi.alt` | Ne kadar ödediğini sen yazıyorsun. |
| `tan.atla` | Bu kartı atla |
| `tan.sabit.baslik` | Sabit giderler |
| `tan.sabit.aciklama` | Her ay kesin çıkan tutarlar. Bilmediğini boş bırak. |
| `tan.sabit.kira` / `fatura` / `ulasim` / `kredi` | Kira ve aidat · Faturalar · Ulaşım ve yakıt · Kredi ve taksit |
| `tan.siklik.etiket` | Ne sıklıkla |
| `tan.siklik.*` | Günde 1 · Günde 2 · Haftada 2-3 · Haftada 1 · Ayda 1-2 · Hiç · Kendim yazayım |
| `tan.kahve.baslik` / `aciklama` | Kahve · Dışarıda aldığın kahve. Evde yaptığın sayılmaz. |
| `tan.kahve.fiyat` | Bir fincan kaç lira |
| `tan.sigara.baslik` / `aciklama` | Sigara · Sıklığı ve kendi ödediğin fiyatı yazıyorsun. |
| `tan.sigara.fiyat` | Bir paket kaç lira |
| `tan.hic.not` | Hiç dedin. Bu kart planda görünmez. |
| `tan.yemek.baslik` / `aciklama` | Dışarıda yemek · Öğle yemeği, akşam yemeği, paket sipariş. |
| `tan.yemek.fiyat` | Bir yemek kaç lira *(T-5: "Bir öğün kaç lira" idi — K-051)* |
| `tan.yemek.birim` | yemek *(serbest sayı girişinde "Günde kaç yemek")* |
| `tan.yatirim.baslik` / `aciklama` | Yatırım · Cevabın yalnız birikimini adlandırmak için. |
| `tan.yatirim.*` | Yapıyorum · Yapmayı düşünüyorum · İlgilenmiyorum |
| `tan.yatirim.sinir` | Yatırım tavsiyesi vermiyoruz. |
| `tan.yatirim.sinir.alt` | Birikimin bir kısmını yatırım payı diye etiketleriz. |
| `tan.birikim.baslik` / `aciklama` | Birikim hedefi · Sabit giderlerinden sonra kalanın içinden ayrılır. |
| `tan.birikim.etiket` | Gelirin yüzdesi |
| `tan.birikim.sinir` | Üst sınıra geldin. Kaydırıcı burada durur. |
| `tan.birikim.sinir.alt` | Sosyal ve keyfi payı 0 ₺ kalır. |
| `tan.donus.baslik` | Kaldığın yerden |
| `tan.donus.aciklama` | Dört kart cevapladın. Dördü bekliyor. |
| `tan.donus.cevaplanmadi` | Cevaplanmadı |
| `tan.donus.plan` | Planı şimdi gör |
| `tan.fiyat.bos` | Fiyatını yaz |

**Plan (E-26):**

| Anahtar | Metin |
|---|---|
| `plan.baslik` | Planın hazır |
| `plan.aciklama` | Cevaplarından çıkardık. Değiştirebilirsin. |
| `plan.pay.zorunlu` | Zorunlu |
| `plan.pay.zorunlu.alt` | Kira, fatura, ulaşım, kredi taksiti. |
| `plan.pay.sosyal` | Sosyal ve keyfi |
| `plan.pay.sosyal.alt` | Günlük limitin buradan çıkar. |
| `plan.pay.birikim` | Birikim |
| `plan.pay.yatirim` | Bunun {tutar}'si yatırım payı. |
| `plan.limit.baslik` | Günlük limit |
| `plan.limit.pano` | Panodaki büyük sayı bu olur. |
| `plan.limit.pano.alt` | Her maaş döneminde yeniden bölünür. |
| `plan.nasil` | Nasıl hesaplandı |
| `plan.nasil.1` | Sabit giderlerini topladık |
| `plan.nasil.2` | Birikim hedefini ayırdık |
| `plan.nasil.3` | Kalanı sosyal ve keyfi paya yazdık |
| `plan.nasil.4` | Dönemde kalan güne böldük |
| `plan.nasil.yuvarlama` | Hesap kuruş üzerinden yapılır. |
| `plan.nasil.yuvarlama.alt` | Günlük limit tam liraya aşağı yuvarlanır. Yüzdeler tam sayıya yuvarlanır, toplamı 100'e tamamlanır. |
| `plan.aliskanlik.baslik` | Alışkanlık maliyeti |
| `plan.aliskanlik.sag` | Kendi fiyatlarınla |
| `plan.aliskanlik.toplam_not` | Sosyal ve keyfi payının {tutar}'si. Yasak değil, görünür. |
| `plan.aliskanlik.bos` | Alışkanlık kartlarını cevaplamadın. |
| `plan.aliskanlik.bos.alt` | Sıklığı ve kendi fiyatını yazarsan aylık tutarı burada görürsün. |
| `plan.ayar.baslik` | Payları ayarla |
| `plan.ayar.not` | Zorunlu pay sabit kalır. O senin girdiğin sabit giderlerin toplamı. |
| `plan.ayar.degisim` | Sosyal ve keyfi pay {tutar} azaldı. Zorunlu pay değişmedi. |
| `plan.gelirsiz.baslik` | Limitini yazalım |
| `plan.gelirsiz.aciklama` | Gelirini paylaşmadın. Yüzde planı kurulmadı. |
| `plan.gelirsiz.eldeki` | Alışkanlık maliyeti gelirsiz de çalışır. |
| `plan.gelirsiz.sonra` | Gelirini sonra da ekleyebilirsin. |
| `plan.eksi.baslik` | Plan bu ay kurulamadı |
| `plan.eksi.aciklama` | Sabit giderlerin gelirinden fazla. |
| `plan.eksi.tutar` | Sabit giderlerin gelirini {tutar} aşıyor. |
| `plan.eksi.normalize` | Bu çok rastlanan bir durum. Ölçülebilir olması iyi haber. |
| `plan.eksi.kalan` | {tutar} eksik |
| `plan.eksi.yol1` | Giderleri gözden geçir |
| `plan.eksi.yol2` | Limiti elle yaz |
| `plan.eksi.yol3` | Limitsiz devam et |
| `plan.eksi.yol3.alt` | Takip etmek için plana ihtiyacın yok. Kayıt tutmak tek başına işe yarar. |
| `plan.yarim.baslik` | Plan yarım hazır |
| `plan.yarim.aciklama` | Dört kart boş. Eldekiyle böldük. |
| `plan.yarim.birikim` | Birikim hedefi girmedin. Şimdilik kalanın tamamı sosyal ve keyfi payında. |
| `plan.kur` | Planı kur |

**Ayarlar (E-19) yeni bölüm:** `ayar.plan.baslik` "Plan ve profil" ·
`ayar.plan.aciklama` "Plan cevaplarından çıkar. İstediğin an değiştir." ·
`ayar.plan.gelirsiz` "Gelirini girmedin. Plan onsuz kurulmuyor." ·
`ayar.plan.kalan` "{n} kart kaldı" · `ayar.plan.bekliyor` "8 kart bekliyor" ·
`ayar.plan.gor` "Planı gör".

**K-057/6 · sözcük değişimi uygulandı** (kimlik doğrulama = **"Oturum aç"**):
`15-giris.html` (başlık, birincil buton, meşgul metni "Oturum açılıyor",
ağ hatası şeridi, "Oturum açmaya dön"), `16-kayit.html` (ghost buton ve
"Bu e-posta ile hesap var. Oturum aç." hata metni), `11-ayarlar.html`
("Oturum aç ya da hesap oluştur", "Hesap yalnız seni tanımak için.",
"Bu e-posta ile bir daha oturum açamazsın."), `index.html`. Harcama
**girişi** anlamındaki "giriş" hiçbir yerde değiştirilmedi. Dosya adları
(`15-giris.html`) ve ekran kodu (E-22) değişmedi — bağlantı kırmamak için;
E-22'nin **adı** artık "Oturum aç".

## RN inşa notları

1. **`Slider` = `PanResponder` + 3 `View`.** Topuz konumu
   `left = (trackW − 32) × value`; `trackW` `onLayout` ile ölçülür, sabit
   sayı gömülmez (prototipte 326 = 390 − 32 ekran − 32 kart iç boşluğu).
   `accessibilityRole="adjustable"` + `accessibilityActions`
   `increment`/`decrement` (adım **%1**) — kaydırıcı ekran okuyucuyla
   sürüklenemez, artır/azalt eylemi zorunludur.
2. **%100 kilidi tek yerde.** `birikimYuzde` state'tir; `sosyal` ve
   `gunlukLimit` **türetilmiş** değerlerdir (`useMemo`), asla ayrı state
   tutulmaz. İki state tutmak iki ekranda iki farklı toplam üretir.
3. **`clamp(0, 100 − zorunluYuzde)`** kaydırıcının kendisinde uygulanır;
   sınıra dayanma `onPanResponderMove` içinde anlaşılır ve `maxReached`
   bayrağı topuzun `warning-soft` hâlini açar + `Haptics.selectionAsync()`
   bir kez tetiklenir (sürükleme boyunca tekrar etmez).
4. **Katman 2 kalıcılığı:** her kart cevabı **anında** yazılır
   (`profile` tablosuna upsert), "Devam" beklemez. Uygulama kapanırsa
   kaldığı kart `profile.lastCard` ile açılır. Cevaplanmamış alan
   `null`'dır; **0 ile doldurulmaz** (0, "hiç harcamıyorum" demektir ve
   "cevaplamadım" ile aynı şey değildir — plan ekranı bu ikisini farklı
   gösterir).
5. **Klavye:** sabit gider ve fiyat alanları kil tuş takımı kullanır,
   sistem klavyesi açılmaz → `KeyboardAvoidingView` gerekmez, düzen
   zıplamaz. "Devam" daima tuşların altında sabit.
6. **Plan ekranı `ScrollView`**, alt blok (`Planı kur` + `Şimdi değil`)
   kaydırmanın dışında sabittir; E-26 en uzun yüzeyde ~1.500px içerik.
7. **Gelir yoksa yüzde modeli hiç render edilmez** — `disabled` bir
   kaydırıcı ya da "—" dolu bir kart bırakılmaz. Ekranın başlığı da
   değişir ("Limitini yazalım").
8. **Kuruş aritmetiği:** tüm paylar `number` (kuruş, integer). Yüzdeden
   tutar hesabı `Math.round(gelir * y / 100)`; en büyük kalan yöntemi
   `%100` toplamı için tek bir yardımcı fonksiyonda
   (`dagitimYuzdeleri()`) — iki ekranda iki kez yazılmaz (K-040).
9. **E-25'in ilerleme çubuğu 8 segment değil**, tek oluk + `n/8`.
   Sekiz segment 390px'te 38px'lik parçalara bölünür ve ilerleme okunmaz
   olur.

## Bilinçli tasarım kararları (design-reviewer için)

1. **Tek kaydırıcı, tek serbestlik derecesi.** Zorunlu pay kullanıcının
   girdiği sabit giderlerin **toplamıdır**, bir tercih değil; kaydırılamaz.
   Üç kaydırıcıyı birbirine itmek her dokunuşta iki sayıyı birden
   kaybettirir. Değişen tek sayı var ve nereye gittiği yazılı:
   *"Fark sosyal ve keyfi paydan iner."*
2. **Katman 1 sonunda günlük limit YOK.** v3'te onboarding'in 2. sorusu
   günlük limiti soruyordu; K-053 onu gelirle değiştirdi. Elimizde sabit
   gider olmadığı için savunulabilir bir limit **türetilemez** → sayı
   uydurmak yerine uygulama **limitsiz kipte** açılıyor ve kurulum
   özetinde bu dürüstçe yazılıyor ("Günlük limit — Henüz yok"). Kayıt
   tutma, gün kapatma ve seri limitsiz kipte de çalışır.
3. **Alışkanlık maliyeti 30 gün, günlük limit kalan gün (28).** İki farklı
   zaman ölçeği ama **aynı satırda değil** (K-056'nın uyarısı): alışkanlık
   kartı "Ayda" der ve ayı sorar, limit kartı "dönemde kalan gün" der.
   Alışkanlık maliyetini 28'e bölmek "aylık kahve masrafı" sorusunun
   cevabı olmazdı.
4. **"Hiç" cevabı planda 0 ₺ satırı üretmez.** Sıfırlık satır kullanıcıya
   cevapladığı bir soruyu her açılışta tekrar gösterir ve toplamı
   kirletir. Kart yalnız *cevaplanmadı* durumunda "Girilmedi" der.
5. **Sigara ve alkol kartları diğerlerinin birebir kopyası.** Aynı punto,
   aynı çipler, aynı ikon kabı, aynı ton. Uyarı rengi, sağlık mesajı,
   "azaltmayı düşündün mü" yok. Ürün aynayı tutar, ders vermez.
6. **E-26'da kutlama yok.** "Planın hazır" bir başarı ekranı değil bir
   **döküm**. Rozet, konfeti, "tebrikler", puan, derece, "finansal sağlık
   skoru" üretilmedi (K-048 · K-050 · K-053).
7. **Yatırım = tek etiket.** "Yatırım payı" birikimin içinde bir yüzdedir;
   ayrı bir pay segmenti bile değil (4. renk üretmek gerekirdi). Enstrüman
   adı, getiri, risk sözcüğü hiçbir yüzeyde geçmiyor (SPK sınırı).
8. **Negatif kalan durumu `warning`, `danger` değil.** Sabit giderlerin
   geliri aşması bir kullanıcı hatası değil, bir gerçektir. Kırmızı dört
   bağlamla sınırlı (tokens §1.3) ve bu onlardan biri değil. Negatif sayı
   yazılmıyor: "1.400 ₺ eksik".
9. **Üç çıkış yolu tek kartta** (negatif kalan): giderleri gözden geçir ·
   limiti elle yaz · limitsiz devam et. Kullanıcıyı çıkışsız bir hata
   ekranında bırakmak, ürünü o gün silmenin en kısa yolu.
10. **`01-gunluk` A2 (K-057/8):** kesme hizası **pikselle değil içerikle**
    düzeltildi. Yüzey artık **tek kayıtlı bir gün**; içerik 659px'te
    bitiyor, kaydırma alanı 669px → hiçbir satır kesilmiyor ve dikey
    ritmin (tokens §3.1) tek bir değeri değişmedi. Yan fayda: eski hâlde
    liste başlığı "Günlük toplam 180 ₺" derken listede 137 ₺'lik iki satır
    vardı — **veri tutarsızlığı da kapandı.** Dikey kaydırma ipucu asıl
    yüzeyde (A) üç kayıt + kategori kartıyla zaten var; A2'nin işi
    **yatay** sayfalamayı öğretmek.
11. **Ayarlar'a "Plan ve profil" bölümü eklendi** ve yeri **Kip'in hemen
    altı**: Kip panodaki büyük sayının *hangi* sayı olduğunu, plan ise
    *kaç* olduğunu belirler. Katman 1'de atlanan gelir ve Katman 2'nin
    kalan kartları buradan tamamlanır (F-12).
12. **E-25'te iki ayrı çıkış** (geri oku + kapat) bilinçli: geri bir kart
    geri alır, kapat akıştan çıkar. Kritik/yıkıcı hiçbir hedef sol üste
    konmadı (iOS kenar jesti) — kapat **sağ üstte**.

## 🔴 Çelişkiler (PM'e — sessizce çözülmedi)

1. **metinler.md §18: "Yüzde — Faz 1'de kullanılmaz"** ↔ **K-053:
   "dağılım ₺ ve % olarak".** K-053 daha sonraki ve açık bir karar olduğu
   için yüzde kullandım; biçimi `%59` (işaret önce, boşluk yok).
   **PM §18'i güncellemeli**, yoksa sonraki denetim bunu ihlal okur.
2. **metinler.md §2 E-02/E-03 geçersiz.** "Günlük limit" sorusu (E-02) ve
   kipe bağlı soru (E-03) K-053 ile düştü; yerine gelir ve maaş günü
   geldi. Yeni anahtarlar yukarıda. §2 yeniden yazılmalı.
3. **Kaybolan tohumlama adımı:** v3'ün E-03'ü Takip kipinde "en çok neyi
   merak ediyorsun → en fazla üç kategori" diye sorup **kategori
   limitlerini tohumluyordu.** K-053'ün 8 kartında bu yok ve ben de
   eklemedim (kart sayısı bağlayıcı). Sonuç: kategori limitleri artık
   **yalnız E-17'den** kurulur. PM onaylasın ya da 9. kart olarak geri
   koymaya karar versin.
4. **`success` renginin yeni bağlamı.** Birikim segmenti `success #16A34A`
   kullanıyor; tokens §1.3 bu rengi iki bağlamla sınırlıyor. Paletin
   üçüncü ayırt edilebilir grafik rengi bu; alternatifi kategori
   renklerini ödünç almak (§1.4 ihlali) ya da iki mavi tonu üçe çıkarmak
   (komşu segment ayrımı 1.45:1, WCAG 1.4.11 sorunlu). **PM onayı gerek.**
5. **E-10'un varsayılanı.** Madde 2'nin sonucu: yeni kullanıcı artık
   **limitsiz kipte** açılıyor. `metinler.md` §3 ve `ekran-envanteri.md`
   E-10 anlatımı "Günlük limit 300 ₺" varsayımıyla yazılmış. Prototipte
   300 ₺ gösteren yüzeyler **planı kurmuş** kullanıcıyı anlatıyor; boş/
   limitsiz yüzeyler de mevcut. Dokümanlar bu ayrımı yazmalı.
6. **"Kalan gün" tanımı hiçbir belgede yoktu** (K-056/2 ile aynı tuzak).
   Formül 6 olarak yazdım: bugün **dahil**, maaş günü ayda yoksa ayın son
   günü, düzensiz gelirde dönem 30 gün. PM `metinler.md` §18'e ya da
   ayrı bir "türetilmiş değerler" bölümüne işlemeli.
7. **Gizlilik/kullanım şartları hâlâ yok** (K-057/7) — bu turda da yer
   tutucu bırakılmadı, çünkü bu ekranlarda yasal bağlantı gerekmiyor.
   Yayın bloklayıcısı olarak açık duruyor.

## Anti-pattern öz-denetimi (E-01…E-03 · E-25 · E-26 · madde madde)

| Madde | Durum |
|---|---|
| Mor-mavi varsayılan gradyan | ✅ Tek gradyan `grad-action` (`#3B82F6 → #2F68C5`), brandbook/DESIGN.md paletinden; mor yok |
| Her elemanda glassmorphism | ✅ Bulanıklık hiç yok; katman bilgisi clay üç derinlikten (raised/pressed/sunken) |
| Amaçsız drop-shadow | ✅ Her gölge bir **durum** anlatıyor: kabarık = dokunulabilir, çukur = değer/oluk, pressed = basılı. Denklemde girdiler **çukur**, sonuç **kabarık** — hiyerarşi gölgeyle kuruldu |
| Karışık köşe yarıçapı | ✅ Yalnız 16 (kutu/satır), 24/32 (kart/sheet), 999 (çip/oluk/topuz). Denetim `IZIN_RADIUS` ile tarıyor, 0 bulgu |
| Inter / Poppins / Montserrat "varsayılan" | ✅ Font seti değişmedi: Poppins başlık + Montserrat gövde/sayı (tokens §2, gömülü). Yeni font eklenmedi |
| 3 sütunlu "daire ikon + başlık + 1 cümle" | ✅ Hiçbir yüzeyde yok. E-25 kapısı **tek kartın içinde dikey satır**; ikon kabı 48×48 **kare (radius 16)**, daire değil ve satırın solunda |
| Stok illüstrasyon | ✅ Yok; boş/hata durumları tipografi + çukur yüzeyle anlatıldı |
| Kimliksiz aşırı beyaz boşluk | ✅ Boşluklar §3.1 ritim setinden (4/8/12/16/24); her değerin tek işi var |
| Jenerik pazarlama dili | ✅ "Planın hazır", "Kaldığın yerden", "Yasak değil, görünür", "Bu çok rastlanan bir durum" — ürünün kendi sesi. "Elevate/Empower" türü tek cümle yok |
| Düşük kontrastlı gri metin | ✅ Yeni yüzeylerde en düşük: `text-2 #4961A5` (4.56:1) ve `warning-ink` `surface` üstünde 6.80:1. `text-3` yalnız placeholder olarak `surface`/`well` içinde kullanıldı (E-02'nin "0"ı) |
| Sistemsiz rastgele boşluk | ✅ `denetim.py` satır içi boşlukları token setine karşı tarıyor: 0 bulgu |
| Dark mode'u ters çevirerek üretmek | ✅ Karanlık mod üretilmedi (Faz 2) |
| **Emoji** (K-004) | ✅ Yok; `denetim.py` emoji taraması 0 bulgu. Tüm ikonlar Lucide, **yeni ikon seti eklenmedi** (P-6) |
| **Ünlem** | ✅ Yok (denetim taraması) |
| **Sahte metrik / rozet** | ✅ "Finansal sağlık puanı", yüzde tamamlanma rozeti, seviye, derece yok. Katman 2 ilerlemesi **kaç kart kaldı** olarak yazıldı |
| **hover** | ✅ Yok; her etkileşimli elemanın `pressed` hâli çizildi (çip, kuyu satırı, kaydırıcı topuzu, atla butonu) |
| Boş / yükleniyor / hata / uzun metin | ✅ E-26: yükleniyor (iskelet) · gelir yok · negatif kalan · yarım veri. E-25: boş kart · "Hiç" · yarıda bırakma. Uzun tutar "18.800 ₺" denklem kutusunda ölçülerek doğrulandı (74.2 ≤ 82) |

---

# T-4 — Ürün arama + limit önerisi

- Tarih: 2026-09-18 · Kaynak kararlar: **K-050** (kalori-app uyarlaması + ürün
  arama), **K-049** (geçmiş güne kayıt), **K-059/5** (günlük limit önerisi),
  K-048 (seri limite bağlı), K-037 (fiyat uydurma yasağı).
- Dokunulan üretim dosyaları: `_uret/s02_harcama_ekle.py` (E-11 · 11 → **17
  yüzey**), `_uret/s03_onboarding.py` (E-01…E-03 · 5 → **6 yüzey**),
  `_uret/s00_index.py`, `stil.css` (iki yeni blok).
- Toplam prototip: **18 sayfa · 122 yüzey · `denetim.py` 0 bulgu.**

Bu turun tezi tek cümlede: **ürün arama bir fiyat girme kısayoludur, bir ürün
veritabanı değildir.** Katalog kullanıcının ne aldığını isimlendirir; ne kadar
ödediğini **yalnız kullanıcı** söyler. İkinci iş, K-059/5'in açtığı boşluğu
kapatmak: limitsiz kipte seri çalışmadığı için (K-048) Katman 2'yi atlayan
kullanıcı oyunlaştırmayı hiç görmüyordu; artık gelir girildiyse **onay bekleyen
bir limit önerisi** görüyor.

## Ekran akışı (değişen yerler)

```
E-11 Harcama ekle (FAB)
  ├─ varsayılan yol  : tutar yaz → kategori çipi → Kaydet            (3 dokunuş)
  ├─ son kullandığın : çip → (tutar + kategori dolar) → Kaydet       (3 dokunuş)
  ├─ arama · geçmiş  : ara → sonuç → (tutar + kategori dolar) → Kaydet (4)
  ├─ arama · katalog : ara → sonuç → (kategori dolar, TUTAR BOŞ) → yaz → Kaydet
  └─ eşleşme yok     : "… olarak ekle" → kategori çipi → Kaydet
       ↳ hiçbir dalda ürün seçmek zorunlu değildir; arama alanı boş bırakılırsa
         kayıt eksiksizdir ve doğrulama hatası üretmez.

E-01…E-03 Katman 1 (3 soru)
  adım 3/3 "Başla"
     ├─ gelir GİRİLDİ    → [yeni yüzey] Günlük limit önerisi (sheet)
     │      ├─ Limiti kabul et      → E-10 limitli kipte açılır, seri çalışır
     │      ├─ Başka bir sayı yaz   → E-17 Limitler (tuş takımı)
     │      └─ Limitsiz devam et    → E-10 limitsiz kipte açılır (K-048: seri yok)
     └─ gelir GİRİLMEDİ  → öneri yüzeyi HİÇ açılmaz, limitsiz kip aynen kalır
```

## tokens eklentileri

`tokens.md` düzenlenmedi; T-5 birleştirmesi için aday satırlar:

| Jeton / kural | Değer | Gerekçe |
|---|---|---|
| `cip-ad` kırpma sınırı | `max-width: 120px`, tek satır, ellipsis | "Son kullandıkların" çipinde **ad kırpılır, tutar kırpılmaz** — kırpılan bir tutar yanlış tutardır |
| `gun-btn` vurgu mürekkebi | `primary-text` + ağırlık 600 | Bugün değilse gün vurgulanır; **amber/kırmızı kullanılmaz**, §1.5'e göre amber yalnız "limit dışı" sinyalidir |
| `gun-btn` basılı mürekkebi | `primary-press` | RN'de hover yok; tek geri bildirim basılı hâl |
| `kat-kab.notr` | kap `primary-soft`, çizgi `primary-text` | "Kendi kalemini ekle" satırı bir kategori **değildir**; kategori renkleri yalnız kategori bilgisi taşır (§1.4) |
| `oneri-pul` | 4/12 iç boşluk · radius 999 · `primary-soft` zemin · `clay.sunken` · 12/16 · `primary-text` | Onaylanmamış sayının işareti. Kabul edilince **pul düşer** |
| Arama alanı | mevcut `.giris` (56 · `well` · `clay.sunken`) aynen | Yeni bir giriş biçimi icat edilmedi |

Yeni renk, yeni punto, yeni radius, yeni boşluk değeri **yok.** Palet dışına
çıkılmadı; `denetim.py` radius/punto/boşluk taramaları 0 bulgu.

## Yeni bileşenler

`bilesen-envanteri.md`'ye T-5'te eklenecek. Her biri için **basılı** durum
çizildi (RN'de hover yok).

| Bileşen | Durumlar | Not |
|---|---|---|
| `arama-alani` | boş (placeholder) · odaklı + imleç · yazılıyor + temizle · **yükleniyor (spinner)** · ürün seçili + kaldır | Boşken akışa karışmaz: odaklanmaz, hata üretmez, Kaydet'i engellemez |
| `sonuc-satiri` | normal · basılı · **"… olarak ekle"** (nötr kap) | Sağda **tutar sütunu yoktur.** Kullanıcının kendi tutarı ikinci satırda, "geçen sefer" sözcüğüyle ve `caption` ağırlığında |
| `son-kullanilanlar-cip` | normal · basılı · uzun ad (kırpılmış) | Tutar 0 iken görünür, ilk rakamda kapanır |
| `grup-basligi` | "Son kullandıkların" · "Ürünler" | İki kaynağı ayırır: kullanıcının kendi geçmişi ≠ katalog |
| `kategori-deger` (dropdown) | normal · basılı | Kategori **doldu**ğunda çip şeridinin yerine geçer |
| `kategori-seridi` | seçimsiz · seçili + nokta · hatalı | İlk 6 çip frekansa göre + "tüm kategoriler" kapısı |
| `gun-btn` | bugün · vurgulu (geçmiş gün) · basılı | Tutar kuyusunun **içinde** |
| `gecmis-gun-seridi` | tek durum | Vurgulu çipe ek olarak yazılı cümle (K-049) |
| `oneri-pul` | tek durum | Yalnız onay bekleyen sayının yanında |
| `limit-onerisi-sheet` | tek yüzey · kabul butonu basılı çizildi | Katman 1 çıkışı; ekran değil, **yüzey** |
| `arama-iskeleti` | 3 satır | Spinner değil, satır düzeni; içerik gelince zıplama olmaz |

## Yeni metinler

`metinler.md`'ye T-5'te eklenecek. Lorem yok, hepsi ürün sesi.

**E-11 · arama**

| Anahtar | Metin |
|---|---|
| `ekle.arama.placeholder` | Ne aldın? (isteğe bağlı) |
| `ekle.arama.grup.gecmis` | Son kullandıkların |
| `ekle.arama.grup.katalog` | Ürünler |
| `ekle.arama.satir.gecen` | {kategori} · geçen sefer {tutar} |
| `ekle.arama.yeni.baslik` | “{arama}” olarak ekle |
| `ekle.arama.yeni.alt` | Kategoriyi ve tutarı sen seç. |
| `ekle.tutar.oneri.cip` | Geçen sefer {tutar} |
| `ekle.tutar.alt.gecmisten` | Tutar geçen seferkinden geldi. Değiştirebilirsin. |
| `ekle.tutar.alt.katalogdan` | Tutarı sen yaz. Fiyat tahmini yapmıyoruz. |
| `ekle.tutar.alt.kategori` | Kategori üründen geldi. Değiştirebilirsin. |
| `ekle.tutar.alt.ikisi` | Tutar ve kategori son kaydından geldi. Değiştirebilirsin. |
| `ekle.gun.serit` | Bu kayıt {gün}'e yazılacak. |
| `ekle.hata.tutar` | Tutar sıfırdan büyük olmalı. |
| `ekle.hata.kategori` | Bir kategori seç. |
| `ekle.limit.onizleme` | Bu harcama günlük limitin {tutar} üzerine çıkarır. |
| `ekle.hata.yazilamadi` | Kayıt yazılamadı. Yeniden dene. |

**E-11 · a11y etiketleri** (ekranda görünmez, ekran okuyucuda okunur)

| Anahtar | Metin |
|---|---|
| `a11y.ekle.arama` | Ürün ara, isteğe bağlı |
| `a11y.ekle.aramaTemizle` | Aramayı temizle |
| `a11y.ekle.urunKaldir` | Ürünü kaldır |
| `a11y.ekle.gun` | Gün seç, şu an {gün} |
| `a11y.ekle.kategoriDeger` | Kategori {ad}, değiştirmek için dokun |
| `a11y.ekle.oneriCip` | Geçen sefer ödediğin {tutar} tutarını kullan |
| `a11y.ekle.sonKullanilan` | {ad}, geçen sefer {tutar} |

**Katman 1 · limit önerisi (K-059/5)**

| Anahtar | Metin |
|---|---|
| `oneri.baslik` | Günlük limit önerimiz |
| `oneri.pul` | Öneri |
| `oneri.alt` | Sen onaylamadan limit olmaz. |
| `oneri.nasil.baslik` | Nasıl hesaplandı |
| `oneri.nasil.1` | Aylık net gelirin {tutar}. |
| `oneri.nasil.2` | Yaygın bir varsayılan dağılım kullandık: %50 zorunlu, %30 sosyal ve keyfi, %20 birikim. |
| `oneri.nasil.3` | Sosyal ve keyfi pay {tutar} oldu, maaş döneminde kalan {n} güne bölündü. |
| `oneri.serit.1` | Bu sayı senin cevaplarından değil, varsayılan dağılımdan çıktı. |
| `oneri.serit.2` | Sekiz kartı doldurursan plan kendi giderlerinle kurulur. |
| `oneri.btn.kabul` | Limiti kabul et |
| `oneri.btn.degistir` | Başka bir sayı yaz |
| `oneri.btn.red` | Limitsiz devam et |
| `onboarding.ozet.limitSatiri` | Gelirini yazdığın için sana bir günlük limit önerebiliriz. Kabul etmek zorunda değilsin. |

## Ürün kataloğu (tam liste)

**Bağlayıcı kurallar**

1. **Fiyat alanı YOKTUR.** Katalogda `ad` ve `kategori` dışında alan yok
   (K-050 · K-037). Şema: `{ id, ad, kategori, arama_anahtarlari[] }`.
2. **Jenerik kalem, marka değil.** "Sigara paketi" katalogda; "Marlboro Touch
   Blue 20'lik" **kullanıcının kendi geçmişinden** gelir. Katalog marka adı
   taşımaz — marka listesi bakım yükü, reklam görüntüsü ve yanlış eşleşme
   üretir.
3. **Her kalem tam bir kategoriye bağlıdır** (13 kategori, `lib.CATS`). Bağ
   değiştirilemez değil: kullanıcı dropdown'dan değiştirir, **kullanıcının
   seçimi o kalem için kalıcı olarak öğrenilir** (yerel eşleme tablosu).
4. **Katalog uygulamayla gelir**, sunucu/servis yoktur; arama tamamen çevrimdışı.
5. **Liste kapalı değildir**: eşleşme yoksa kullanıcı kendi kalemini yazar ve o
   kalem kendi geçmişine girer. "fotokopi" bilerek katalogda **yoktur** —
   prototipin "eşleşme yok" yüzeyi (E) bu kalemle çalışır.

**80 kalem · 13 kategori**

| # | Kalem | Kategori |
|---|---|---|
| 1 | Filtre kahve | Kafe |
| 2 | Türk kahvesi | Kafe |
| 3 | Latte | Kafe |
| 4 | Sütlü kahve | Kafe |
| 5 | Soğuk kahve | Kafe |
| 6 | Çay | Kafe |
| 7 | Simit | Kafe |
| 8 | Poğaça | Kafe |
| 9 | Tatlı | Kafe |
| 10 | Döner | Restoran |
| 11 | Lahmacun | Restoran |
| 12 | Pide | Restoran |
| 13 | Kebap | Restoran |
| 14 | Tost | Restoran |
| 15 | Hamburger | Restoran |
| 16 | Pizza | Restoran |
| 17 | Öğle yemeği | Restoran |
| 18 | Kahvaltı tabağı | Restoran |
| 19 | Yemek siparişi | Restoran |
| 20 | Haftalık market | Market |
| 21 | Ekmek | Market |
| 22 | Süt | Market |
| 23 | Yumurta | Market |
| 24 | Peynir | Market |
| 25 | Meyve ve sebze | Market |
| 26 | Et ve tavuk | Market |
| 27 | Su damacanası | Market |
| 28 | Temizlik malzemesi | Market |
| 29 | Kişisel bakım | Market |
| 30 | Atıştırmalık | Market |
| 31 | Toplu taşıma yüklemesi | Ulaşım |
| 32 | Şehirlerarası otobüs bileti | Ulaşım |
| 33 | Taksi | Ulaşım |
| 34 | Otopark | Ulaşım |
| 35 | Köprü ve otoyol geçişi | Ulaşım |
| 36 | Uçak bileti | Ulaşım |
| 37 | Kargo | Ulaşım |
| 38 | Araç bakımı | Ulaşım |
| 39 | Benzin | Akaryakıt |
| 40 | Motorin | Akaryakıt |
| 41 | LPG | Akaryakıt |
| 42 | Elektrik faturası | Fatura |
| 43 | Su faturası | Fatura |
| 44 | Doğalgaz faturası | Fatura |
| 45 | İnternet faturası | Fatura |
| 46 | Telefon faturası | Fatura |
| 47 | Aidat | Fatura |
| 48 | Motorlu taşıtlar vergisi | Fatura |
| 49 | Kira | Kira ve ev |
| 50 | Ev eşyası | Kira ve ev |
| 51 | Mobilya | Kira ve ev |
| 52 | Tadilat ve usta | Kira ve ev |
| 53 | Ev tekstili | Kira ve ev |
| 54 | Müzik aboneliği | Abonelik |
| 55 | Dizi ve film aboneliği | Abonelik |
| 56 | Spor salonu üyeliği | Abonelik |
| 57 | Bulut depolama | Abonelik |
| 58 | Oyun aboneliği | Abonelik |
| 59 | Yazılım aboneliği | Abonelik |
| 60 | Sinema bileti | Eğlence |
| 61 | Konser bileti | Eğlence |
| 62 | Maç bileti | Eğlence |
| 63 | Oyun içi satın alma | Eğlence |
| 64 | Kitap | Eğlence |
| 65 | Müze ve sergi | Eğlence |
| 66 | Üst giyim | Giyim |
| 67 | Pantolon | Giyim |
| 68 | Ayakkabı | Giyim |
| 69 | Dış giyim | Giyim |
| 70 | Eczane | Sağlık |
| 71 | Doktor muayenesi | Sağlık |
| 72 | Diş hekimi | Sağlık |
| 73 | Gözlük ve lens | Sağlık |
| 74 | Tahlil ve görüntüleme | Sağlık |
| 75 | Vitamin ve takviye | Sağlık |
| 76 | Sigara paketi | Alışkanlıklar |
| 77 | Sarma tütün | Alışkanlıklar |
| 78 | Nargile | Alışkanlıklar |
| 79 | Bira | Alışkanlıklar |
| 80 | Şans oyunu | Alışkanlıklar |

**Katalog dışı bırakılanlar (bilinçli)**

- **Kredi kartı ödemesi / hesaplar arası transfer** — harcama değil, para
  taşıma. Kataloğa koymak çifte sayıma yol açar; kullanıcı yine de "Diğer"e
  elle yazabilir.
- **Kuaför, hediye, bağış, kuru temizleme, evcil hayvan maması** gibi
  "Diğer"e düşen kalemler — 13. kategori bir **kaçış kapısı**dır, katalog
  satırıyla doldurulmaz. Kullanıcı yazar, kendi geçmişine girer.
- **Marka adları** (kural 2) ve **ürün fotoğrafı/logo** — hiçbir yüzeyde yok.
- **Miktar/adet/birim alanı** — bu bir alışveriş listesi değil. "2 × kahve"
  ihtiyacı tutara yazılır; alan eklemek F-2 sürtünme kuralını bozar.

**Prototipte gösterilen alt küme (13 kalem):** Filtre kahve · Türk kahvesi ·
Soğuk kahve · Sütlü kahve · Kahvaltı tabağı · Sigara paketi · Sarma tütün ·
Nargile · Döner · Simit · Haftalık market. Bunların yanında **kullanıcının
kendi kayıtları** (katalog değil): Marlboro Touch Blue 20'lik · İstanbulkart —
kataloğun jenerik karşılıkları "Sigara paketi" ve "Toplu taşıma yüklemesi".

## Katlama tablosu (E-11 · 390×844)

Ölçüler px = pt. Kaydırılabilir alan:
`844 − 47 (durum çubuğu) − 28 (home indicator) − 324 (sabit alt blok: 8 + 248 tuş takımı + 12 + 56 Kaydet)` = **445 px.**

Sözleşme: **tutar kuyusu · kategori kontrolü · Kaydet** her yüzeyde katlamanın
üstünde ya da ekrana sabittir.

| Yüzey | Kategori kontrolünün alt kenarı | Pay | Durum |
|---|---|---|---|
| A · açılış (son kullandıkların açık) | 432 | 13 | ✅ en dar hâl; bu yüzden şerit tutar girilince kapanır |
| B · tutar girildi (şerit kapandı) | 342 | 103 | ✅ 3 dokunuşluk yol kaydırmasız |
| F · ürün geçmişten (alt not + değer satırı) | 376 | 69 | ✅ |
| L · geçmiş gün (ek şerit 42 + 8) | 392 | 53 | ✅ K-049 şeridi katlamayı bozmuyor |
| M · iki hata birden (hata satırı 26) | 368 | 77 | ✅ hata metinleri katlamanın üstünde |
| O · limit dışı önizleme (şerit 42 + 8) | 394 | 51 | ✅ |
| C · D · P · arama sonuçları açık | — | — | ⚠️ **bilinçli istisna** (aşağıda) |

**İstisna:** arama sonuç listesi açıkken kategori kontrolü ekranda yoktur,
yerini sonuçlara bırakır. Gerekçe: kategori bir sonraki dokunuşta **üründen**
gelecek; o an kullanıcıya iki kategori kaynağı göstermek çelişki üretir.
Kanıt: **E yüzeyi** (eşleşme yok) — ürün gelmeyeceği belli olduğu anda kategori
şeridi geri döner. Ödeme ve Not blokları katlamanın altına düşebilir: ikisinin
de varsayılanı vardır (Kart / boş).

## RN inşa notları

1. **Arama = yerel, senkron, çevrimdışı.** 80 kalem RAM'de; `FlatList`
   gerekmez, `ScrollView` yeter. `P` yüzeyindeki iskelet **yalnız kullanıcının
   kendi geçmişi SQLite'tan gelirken** görünür (tipik < 50 ms); katalog için
   iskelet gösterilmez.
2. **Türkçe eşleştirme.** `toLocaleLowerCase("tr")` + aksan/nokta normalizasyonu
   (`İ→i`, `I→ı`, `ş→s`, `ç→c`, `ğ→g`, `ü→u`, `ö→o`) **iki tarafa da** uygulanır.
   Sıralama: (1) kullanıcının kendi geçmişi, son kullanım tarihine göre;
   (2) katalog, önce **baştan eşleşenler**, sonra içinde geçenler.
   `localeCompare("tr")` kullanılır — aksi hâlde "Çay" listenin sonuna düşer.
3. **Girilen metnin üzerine yazma yasağı.** "Geçen sefer" çipi ve son
   kullanılan çipi, **tutar 0 değilse** tutarı değiştirmez; çip yalnız
   dokunulunca yazar. Sessizce üzerine yazan otomatik doldurma tuzaktır.
4. **Ürün kaydın ayrı alanıdır** (K-033 veri modeli): `harcama.urun_ad` boş
   olabilir. Ürün silinince kategori ve tutar **silinmez** — kullanıcı onları
   görmüş ve kabul etmiştir.
5. **Öğrenme tablosu** yerel: `(urun_id | serbest_ad) → kategori`. Kullanıcı
   dropdown'dan değiştirdiyse bir sonraki sefer o kategori gelir. Sunucuya
   hiçbir şey gitmez (K-052).
6. **`katman-ust` = RN'de `position:"absolute"` + `StyleSheet.absoluteFill`**
   kardeş View; sheet `justifyContent:"flex-end"` ile alta yaslanır. Scrim
   `rgba(28,57,142,0.38)` — `opacity` prop'u ile değil, **renk alfası** ile
   (opacity alt ağacın tamamını soldurur).
7. **Öneri limiti tek yerden hesaplanır.** `oneriLimit(gelir, kalanGun)` =
   `floor(gelir × 0.30 / kalanGun)`. Yuvarlama **aşağı** (T-3 kuralı; yukarı
   yuvarlamak limiti aşındırır). `kalanGun` T-3'teki "kalan gün" formülünün
   aynısıdır — ikinci bir tanım yazılmaz.
8. **Öneri kabul edilmeden limit yazılmaz.** Depoya yazılan alan
   `gunluk_limit` değil, kabul anına kadar `gunluk_limit_onerisi`'dir; E-10
   limitsiz kipte açılır, seri kapalı kalır (K-048).
9. **`cip-ad` kırpması** RN'de `numberOfLines={1}` + `flexShrink:1`; tutar
   `flexShrink:0`. Çip **sarmaz**, yatay `ScrollView` içinde kayar.
10. **Dokunma hedefleri.** `gun-btn` görsel yüksekliği 20–24 px; RN'de
    `hitSlop={{top:12,bottom:12,left:8,right:8}}` ile 44'e tamamlanır.

## Bilinçli tasarım kararları (design-reviewer için)

1. **Arama alanı tutarın ALTINDA ve odaksız.** Ürün arama eklemek varsayılan
   3 dokunuşluk yolu uzatmamalıydı. Aramayı isteyen ona uzanır; istemeyen
   görmezden gelir ve hiçbir doğrulama hatası yemez.
2. **Arama sonucunda tutar sütunu yok.** Sağda hizalı bir tutar sütunu, olmayan
   bir fiyat otoritesini ima ederdi. Kullanıcının kendi tutarı ikinci satırda,
   **"geçen sefer" sözcüğüyle** ve caption ağırlığında duruyor.
3. **Katalog jenerik, geçmiş markalı.** "Sigara paketi" ↔ "Marlboro Touch Blue
   20'lik" ayrımı ekranda **yan yana** gösterildi (D yüzeyi) ki kuralın
   kendisi tasarımdan okunabilsin.
4. **Kategori kontrolü tek kuraldan türüyor:** üründen doldu → **değer satırı +
   chevron**; kullanıcı seçiyor → **çip şeridi**. İki farklı görünüm keyfi
   değil, "seçilecek bir şey mi var, değiştirilecek bir değer mi" sorusunun
   cevabı.
5. **Otomatik dolan her şey tek cümlede söylenir** (tutar kuyusunun altında).
   Aynı bilgiyi hem kategori satırında hem tutarda tekrarlamak gürültüdür.
6. **Gün, tutar kuyusunun içinde.** Kaydın günü kaydın tutarıyla aynı yerde
   durur; geçmiş güne yazarken ayrıca yazılı şerit iner (K-049). Amber/kırmızı
   kullanılmadı: amber yalnız "limit dışı" demek.
7. **Öneri pulu kabul edilince düşer.** "Öneri" bir süsleme değil, sayının
   **hukuki durumu**: onaylanmamış. Kabul edilen sayı artık kullanıcınındır ve
   pul taşımaz.
8. **Üç çıkış, üç ağırlık.** Kabul (primary) · değiştir (secondary) · limitsiz
   devam (ghost, tam genişlik, 44 pt). Reddetme yolu küçültülmedi — K-053'ün
   "Atla" kuralının aynısı.
9. **Varsayılan dağılım ekranda yazılı.** %50/%30/%20 gizli bir katsayı değil;
   üç adımlık "Nasıl hesaplandı" bloğu sheet'in içinde, ayrı bir yüzeye
   saklanmadı. Kara kutu çıktı güven kaybettirir (K-053).
10. **Katman 1 özet satırı güncellendi** ("Günlük limiti plan kurunca ya da elle
    yazınca belirlersin." → "Gelirini yazdığın için sana bir günlük limit
    önerebiliriz. Kabul etmek zorunda değilsin."). Gerekçe: bir sonraki yüzeyde
    öneri gelirken özet satırının iki yol vaat etmesi çelişkiydi. Özetin
    "Günlük limit — **Henüz yok**" satırı **değişmedi**: öneri onaylanana kadar
    gerçekten limit yoktur.

## 🔴 Çelişkiler

1. **K-033/3 + K-037 gömülü tütün fiyat listesi ↔ K-050.** v2/v3 notlarında
   "yaygın sigara fiyatları gömülü gelir" maddesi vardı; K-050 kataloğa fiyat
   yazmayı **yasakladı**. Tasarım K-050'yi uyguladı, liste **kaldırıldı**.
   PM'in K-033/3'ü resmen kapatması gerekiyor — belge hâlâ ayakta duruyor.
2. **K-059/5 "%50/%30/%20" ↔ T-3'ün türetme zinciri.** T-3'te günlük limit
   *kullanıcının girdiği sabit giderlerden* çıkıyordu (zorunlu pay bir olgu).
   Öneride sabit gider **yok**, o yüzden zorunlu pay bir **varsayım**. İkisi
   aynı ekran dilini kullanıyor ama epistemik değerleri farklı; bu yüzden
   öneride "Öneri" pulu ve "senin cevaplarından değil" cümlesi var.
   **PM onayı gereken nokta:** varsayılan dağılım olarak %50/%30/%20'nin
   kabulü ve `metinler.md`'ye kaynak/atıf cümlesi yazılıp yazılmayacağı.
3. **Öneri kabul edilirse kategori limitleri ne olur?** K-059/3 kategori
   limitlerini **plan ekranından** tohumluyor; plan yoksa kategori limiti de
   yok. Yani öneriyi kabul eden kullanıcının günlük limiti var, kategori
   limiti yok — E-15/E-17 bu durumu zaten "limit yok" yüzeyiyle karşılıyor,
   ek tasarım gerekmedi. **Ürün kararı olarak doğrulanmalı.**
4. **"Kalan gün" tanımı hâlâ yalnız delta'da** (K-059/6). Öneri formülü aynı
   tanıma bağlandı; T-5'te `tokens.md`/`metinler.md`'ye taşınmazsa iki farklı
   uygulama çıkar.
5. **`metinler.md` §18 "yüzde Faz 1'de kullanılmaz"** maddesi öneri yüzeyinde
   de ihlal ediliyor (%50/%30/%20). K-059/1 bu maddeyi zaten geçersiz saydı;
   T-5 temizliğinde §18 güncellenmeli.

## Anti-pattern öz-denetimi (E-11 ürün arama + limit önerisi · madde madde)

| Madde | Durum |
|---|---|
| Mor-mavi varsayılan gradyan | ✅ Yeni gradyan yok; yalnız `grad-action` (`#3B82F6 → #2F68C5`) |
| Her elemanda glassmorphism | ✅ Bulanıklık yok; scrim düz renk alfası |
| Amaçsız drop-shadow | ✅ Arama alanı **çukur** (girdi), sonuç satırı **kabarık** (dokunulabilir), basılı hâl **pressed**. Öneri pulu çukur: dokunulamaz bir etikettir |
| Karışık köşe yarıçapı | ✅ 16 (giriş/kap/satır) · 24 (kart) · 32 (sheet) · 999 (çip/buton/pul). `denetim.py` 0 bulgu |
| Inter / Poppins / Montserrat "varsayılan" | ✅ Font seti değişmedi (P-6 kilitli): Poppins başlık + Montserrat gövde/sayı |
| 3 sütunlu "daire ikon + başlık + 1 cümle" | ✅ Yok. Arama sonuçları **dikey liste**; ikon kabı 44×44 **kare (radius 16)**, daire değil ve satırın solunda |
| Stok illüstrasyon | ✅ Yok. "Eşleşme yok" durumu **boş ekran çizmiyor**, doğrudan eyleme dönüşüyor: "… olarak ekle" |
| Kimliksiz aşırı beyaz boşluk | ✅ Boşluklar 4/8/12/16/24/32 setinden; katlama tablosuyla her yüzeyde ölçüldü |
| Jenerik pazarlama dili | ✅ "Ne aldın? (isteğe bağlı)", "Tutarı sen yaz. Fiyat tahmini yapmıyoruz.", "Sen onaylamadan limit olmaz." — ürünün kendi sesi |
| Düşük kontrastlı gri metin | ✅ En düşük `text-2 #4961A5` (4.56:1). Öneri pulu `primary-text` / `primary-soft` üstünde AA üstü; pul **metinle** okunur, renk tek başına bilgi taşımaz |
| Sistemsiz rastgele boşluk | ✅ `denetim.py` satır içi boşluk/punto/radius taraması: 122 yüzey, **0 bulgu** |
| Dark mode'u ters çevirerek üretmek | ✅ Karanlık mod üretilmedi (Faz 2) |
| **Emoji** (K-004) | ✅ Yok; tarama 0 bulgu. Tüm ikonlar Lucide, **yeni ikon eklenmedi** |
| **Ünlem** | ✅ Yok (tarama) |
| **Sahte metrik / uydurma sayı** | ✅ Katalogda fiyat yok, tahmin yok. Öneri limiti kullanıcının kendi gelirinden + **ekranda yazılı** bir dağılımdan çıkıyor ve **onaysız limit olmuyor** |
| **Kalori semantiği** (K-050) | ✅ kcal, porsiyon, makro, barkod, besin hiçbir yüzeyde yok. Alınan tek şey mekanik: "öğe ara → ekle". ⚠️ **T-5 düzeltmesi:** bu satır "'öğün' de hiçbir yüzeyde yok" diyordu, **doğru değildi** — E-25'in 5/8 kartında "Bir öğün kaç lira" duruyordu. T-5'te "Bir yemek kaç lira" oldu; sözcük artık yalnız `s01_gunluk.py`'nin **kod yorumunda**, referansın neyi olduğunu anlatan cümlede geçiyor (yüzey değil). |
| **hover** | ✅ Yok. Basılı hâl çizilen yeni bileşenler: sonuç satırı, kategori değer satırı, gün çipi, kabul butonu, çipler |
| Boş / yükleniyor / hata / uzun metin | ✅ Eşleşme yok (E) · arama yükleniyor (P) · iki doğrulama hatası (M) · kayıt yazılamadı (Q) · 1.250.000,50 ₺ + 40 karakterlik ürün adı + uzun not (N) |
| Zorunlu alan sürtünmesi | ✅ Ürün seçmek zorunlu değil; arama boş bırakılan yolda (A · B · L · M) kayıt eksiksiz |

---

# T-5 — Denetim düzeltmeleri

> Girdi: `denetim-raporu-v4.md` (**REVİZE — 3 bloklayıcı**) · PM hükümleri **K-061**.
> Bu bir düzeltme turudur: yeni ekran, yeni akış, yeni bileşen **yok**.
> `prototip-v3/` dokunulmadı, dosya silinmedi.
>
> **Turun dersi:** delta'nın tokens eklentisi #6 satırı dolu gün kutusunun
> kontrastını "`#FFFFFF`/`primary-deep` = 5.37" diye ilan etmişti; CSS o
> zemini üretmiyordu (üstüne `grad-action` biniyordu). **İlan ≠ uygulama.**
> Bu yüzden aşağıdaki her kontrast sayısı *hesaplanarak* ve
> **render edilen pikselden örneklenerek** doğrulandı, beyan edilmedi.

## B-1 · Kontrast — dolu gün kutusundaki beyaz sayı

`stil.css` · `.gun-kutu.altinda` · `.gun-kutu.secili` (+ aşağıdaki iki ek):
`background-image: var(--grad-action)` **kaldırıldı**, düz
`background-color: var(--primary-deep)` kaldı.

Ölçüm (WCAG 2.x göreli parlaklık, `#FFFFFF` ön plan):

| Zemin | Nerede | Oran | Sonuç |
|---|---|---|---|
| `grad-action` %34 → `#3779E5` | 44pt kutuda 13pt glifin **üst** kenarı | **4.18** | ❌ AA altı |
| `grad-action` %50 → `#3575DE` | kutunun ortası | **4.42** | ❌ AA altı |
| `primary-deep #2F68C5` (T-5) | kutunun her yeri | **5.37** | ✅ AA |

Piksel doğrulaması: 13-seri ve 14-gun-secici headless render edildi, dolu
kutunun içinden alınan örnek **rgb(47,104,197) = `#2F68C5`** — düz dolgu,
gradyan yok. Hacim gradyandan değil, `clay.raised` / `clay.action`
gölgesinden geliyor; kil dili bozulmadı.

Etkilenen yüzeyler yeniden üretildi: **E-21 gün ızgarası** (28 kutu),
**E-24 ay ızgarası** (31), **E-03 maaş günü** (31).

### Denetçinin listesinde olmayan iki ek (aynı kusur, aynı kaynak)

1. **`.durak.gecildi`** (E-21 durak rayı) — 44pt dairenin içinde **beyaz
   sayı**, zemin `grad-action`. `.gun-kutu.altinda` ile birebir aynı ihlal;
   rapor bu sınıfı anmamış. Gradyan kaldırıldı → **5.37 ✅**. Bir turda
   kapatılan kusurun ikizini ekranda bırakmak, kusuru kapatmamaktır.
2. **`.imza-kare.altinda`** (ızgara lejantı) — metin taşımıyor, yani
   kontrast ihlali **değil**; ama lejant "gerçek gün kutusunun küçük
   ölçeği" diye tanımlı. Kutu düzleşip lejant gradyanlı kalsaydı aynı şeyi
   iki ayrı yüzeyle anlatırdık. Düzleştirildi.

`.durak-bag-dolu`, `.adim-dolu`, `.yuk-dolgu`, `.ilerleme-dolgu`,
`.kaydirici-dolgu`, `.anahtar.acik`, `.fab` **dokunulmadı**: hiçbiri metin
taşımıyor, ikon konturu için gereken 3:1'in üstündeler (en kötü nokta 4.43).

## B-2 · Tek "seçili" dili

`.secim-kart.secili`'den `inset 0 0 0 2px var(--primary-text)` **halkası
kaldırıldı.** Artık `stil.css`'te tek bir 2pt halka kalmadı (`inset 0 0 0 2px`
taraması boş döner; Google düğmesindeki 1px kontur üçüncü taraf çizimidir).

Seçim üç işaretle veriliyor, üçü de kil dilinin kendi aracı:
zemin `primary-soft` · yüzeyin çukura inmesi (`clay.sunken`) · ikon kabının
**tersine kabarması** (`groove`+sunken → `surface`+raised).

**Kural (PM `tokens.md`'ye işleyecek):**

> **Seçimde derinlik, gün ızgarasında dolgu.** Bu üründe seçili durum
> halkayla anlatılmaz (K-040 → K-045 → K-054/6 → T-5). İki dil vardır ve
> ikisi iki ayrı iş yapar:
> · **Seçim dili** (çip, seçim kartı, kategori ızgarası): zemin
>   `primary-soft` + `clay.sunken`; varsa ikon kabı tersine kabarır.
>   *"Bunu ben seçtim, geri alabilirim."*
> · **Dolgu dili** (gün kutusu, durak): zemin `primary-deep` + kabartma.
>   *"Burada bir olgu var"* — kullanıcının seçimi değil, **verinin durumu**.
> Aynı görünümü iki anlama bindirmemek için `.gun-kutu.altinda` (veri) ve
> `.gun-kutu.secili` (seçim) ayrı sınıf olarak durmaya devam eder.

**Bilinçli risk (design-reviewer bilsin):** seçim kartı sayfa zemininde
(`bg #E6EFFE`) duruyor ve seçili zemini `primary-soft #E4EEFE` — ikisi
neredeyse aynı renk. Halka gidince seçimi **yalnızca derinlik + ikon
kabarması** taşıyor. Render edilip bakıldı: kart oyuk olarak okunuyor ve
beyaz kabaran ikon kutusu ikinci, renkten bağımsız ipucu (WCAG 1.4.1
karşılanıyor). RN'de üçüncü ipucu `accessibilityState={{selected:true}}`.
Halkayı geri koymak marka dilini bozar; alternatif gerekirse çözüm
"seçili kart zeminini `surface`'e çıkarmak" olur, halka değil.

## B-3 · Gelir bir kez sorulur

`_uret/s12_profilleme.py` · E-20'nin **"Aylık gelirin hangi aralıkta?"**
sorusu (4 aralık seçeneği) **emekliye ayrıldı.** Gerekçe dosyanın içine
yorum olarak yazıldı ki bir sonraki tur geri koymasın: gelir Katman 1'de
(E-02) **tam tutar** alınıyor, E-26'nın formülleri (`gelir_kurus`) tam tutar
istiyor; aynı olguyu bir yerde aralık bir yerde tutar olarak sormak iki ayrı
doğru üretir ve hangisinin kazanacağı tasarımda değil kodda belirlenir.
Eksik geliri tamamlama yolu zaten tek: **Ayarlar > Plan ve profil** (K-053/F-12).

Yerine **E-25'in cevaplanmamış kartlarından biri** geldi: **Yatırım (7/8)**.
Seçim gerekçesi — bekleyen dört karttan (Dışarıda yemek · Abonelikler ·
Yatırım · Birikim hedefi) tek soruluk sheet biçimine oturan tek kart odur;
diğer üçü **tutar** ister, tutar sormak klavye açar ve E-20'nin "tek dokunuş,
sheet kapanır" sözleşmesini bozar.

Başlık, üç seçenek ve bilgi şeridi `s17_tanisma.py`'deki 7/8 kartından
**kelimesi kelimesine** alındı — B-3'ün dersi tam olarak budur:

| | E-25 · kart 7/8 | E-20 · 2. gün sheet |
|---|---|---|
| Soru | "Yatırım" (kart başlığı) | "Yatırım yapıyor musun?" |
| Alt satır | Cevabın yalnız birikimini adlandırmak için. | *aynı* |
| Seçenekler | Yapıyorum · Yapmayı düşünüyorum · İlgilenmiyorum | *aynı, aynı sırada* |
| Sınır şeridi | Yatırım tavsiyesi vermiyoruz. / Birikimin bir kısmını yatırım payı diye etiketleriz. | *aynı* |
| Çıkış | Bu kartı atla | Şimdi değil + X |

K-053'ün yatırım sınırı korundu: enstrüman, getiri, risk, tavsiye sözcüğü yok.
`12-profilleme.html` yeniden üretildi; "gelir" sözcüğü bu ekranda kalmadı.

## ÖNEMLİ 4 · "öğün" sözcüğü

`_uret/s17_tanisma.py` · 5/8 kartı: **"Bir öğün kaç lira" → "Bir yemek kaç
lira"**; birim adı da `"öğün"` → `"yemek"` (serbest sayı girişinde
"Günde kaç yemek"). Gerekçe K-051: referans kalori uygulamasının bilgi
mimarisi "öğün grupları"ydı ve onu bilinçle kategoriye çevirdik — sözcük izi
yüzeyde kalmaz. Yeni metin anahtarları yukarıdaki T-3 metin tablosuna
işlendi (`tan.yemek.fiyat`, `tan.yemek.birim`).
T-4 öz-denetimindeki **yanlış satır düzeltildi** (yukarıda, işaretli).

## ÖNEMLİ 5 + 6 · Denetim aracı sıkılaştırıldı

**5.** `IZIN_RADIUS`'tan **"4" çıkarıldı.** Prototipte radius 4 hiç
kullanılmıyordu, yani izin bedelsizdi; açık kalsaydı K-054/6'da **elle**
yakalanan `.imza-kare{radius:4}` türü sapma bir daha yakalanmazdı.

**6.** `denetim.py` artık `stil.css`'i de tarıyor: **palet dışı hex** ve
**izinsiz radius**. İki tasarım kararı:

1. **Ölçüt betiğin kendisi değil, `tokens.md`.** İzinli hex kümesi
   `tokens.md`'den okunuyor (**§13 ARŞİV hariç** — orası reddedilmiş v2/v3
   paletlerini ve başka tasarım sistemlerinin renklerini anıyor, beyaz listeyi
   kirletirdi); izinli radius kümesi §12/9 satırından okunuyor. Böylece kural
   iki yerde tanımlı olmuyor — K-040'ın dersi.
   `#000000` beyaz listeden **çıkarılıyor**: tokens'ta yalnız "yasak"
   satırlarında geçiyor.
2. **İstisnalar `stil.css`'in içinde, gerekçesiyle.** `/* @denetim-disi: … */`
   … `/* @denetim-disi-son */` arası bloklar elenir. Üç blok var, betik
   **sayısını da doğruluyor** (biri sessizce eklenirse/silinirse bulgu verir):

   | Blok | Neden dışarıda |
   |---|---|
   | **[A] kabuk** | Telefon gövdesini/adayı/tuş rayını çizer, uygulamanın içini değil; RN'e hiç kodlanmaz (tokens §3.2 ayrı ölçek tanır) |
   | **Sistem klavyesi** (K-061/6) | Bu yüzeyi işletim sistemi çizer. Paletimizi uygulamak yalan olurdu. Palet dışı: `#D1D4DA` `#1C1C1E` `#ADB3BE` `#3A3A3C` · radius 5 · gap 6 |
   | **Üçüncü taraf düğmeler** (K-057/2) | Apple/Google marka varlıkları; dolgu, logo ve etiket rengi sahibinin kılavuzundan gelir. Kap bizim (56pt · radius 999 · clay.raised), içerik onların |

   Yorum **gövdeleri** taramadan düşürülüyor (satır numaraları korunarak):
   bir gerekçe cümlesinde geçen renk kodu ("gradyanın ortası `#3575DD` = 4.43")
   ihlal değil, kuralı anlatan cümledir.

Araç negatif testle doğrulandı: `.test { color:#7C3AED; border-radius:4px }`
+ `#FF00AA` + `radius:12px` eklendi → **4 bulgu** verdi (mor hue dahil),
satır geri alındı.

## ÖNEMLİ 8 · Üst veri

`04`…`11` yüzey dosyaları + `12`, `17` ve ilgili `_uret/*.py` üreteçleri:
`<title>` **"prototip v3" → "prototip v4"** (`lib.py` başlığı dahil).
Artık dizinde tek bir "v3" dizesi kalmadı.
⏸️ Yinelenen `fonts/fonts/` dizini **silinmedi** — geri dönüşsüz silme
Mustafa'nın onayına bağlı (K-061/7). Zararsız duruyor.

## Kapandı / kapanmadı

| # | Madde | Durum |
|---|---|---|
| B-1 | Gün kutusu kontrastı | ✅ 4.42 → **5.37** · +2 ek yüzey (`.durak.gecildi`, `.imza-kare.altinda`) |
| B-2 | Üç "seçili" dili | ✅ İkiye indi, kuralı yazıldı |
| B-3 | Gelir iki biçimde soruluyor | ✅ E-20'nin gelir sorusu emekliye ayrıldı |
| 4 | "öğün" | ✅ "yemek" · yanlış öz-denetim satırı düzeltildi |
| 5 | `IZIN_RADIUS` "4" | ✅ Çıkarıldı |
| 6 | `denetim.py` kapsamı | ✅ `stil.css` hex + radius taraması, ölçüt `tokens.md` |
| 7 | tokens §12 "işletim sistemi çizimleri" istisnası | ⏸️ **PM'de** — `tokens.md` bu ajan tarafından düzenlenmez. Gerekçe metni CSS'in içine ve bu bölüme yazıldı, PM işleyecek |
| 8 | `<title>` v3 → v4 | ✅ · `fonts/fonts/` ⏸️ Mustafa onayı |

## Açık kalan — PM'e

1. **`.btn-primary` metni de gradyanın açık yarısına denk geliyor.**
   56pt butonda 16pt metnin üst kenarı gradyanın ~%40'ında: `#3678E2` →
   **4.25:1**, alt kenarı %60'ta `#3472D9` → 4.61. Yani ortalaması AA'nın
   sınırında, üst kenarı altında. tokens §1.8 bu gradyanı *"metin gradyanın
   alt-koyu yarısına hizalanır"* diyerek onaylıyor — **ama CSS metni
   ortalıyor**, tokens'ın varsaydığı hizalama uygulanmıyor. B-1'in aynı
   fiziği. **Değiştirmedim:** denetçi bu bileşeni temiz saydı, tokens açıkça
   izin veriyor ve düzeltmesi uygulamanın en çok görünen düğmesinin
   görünümünü değiştirir — bu bir PM kararıdır, düzeltme turunun kapsamı
   değil. Karar verilirse iki seçenek var: (a) `grad-action`'ı buton için
   `#3B82F6`→`#295BAC` yapmak (metin bölgesi ≥4.8), (b) butonu da düz
   `primary-deep` yapmak (5.37, ama kil hacmi gölgeye kalır).
2. **§12 istisna satırı** (K-061/6) `tokens.md`'ye yazılmayı bekliyor.

---

# T-6 — Birleştirme (delta → kaynak dokümanlar)

> Tarih: 2026-09-18 · Kaynak kararlar: **K-062** (gradyan zeminde metin) ·
> K-045…K-061. Bu tur **yeni ekran/akış üretmedi**; iki iş yapıldı:
> (1) son kontrast bulgusu kapatıldı, (2) dört turun delta birikimi beş
> kaynak dokümana **işlendi**. Delta artık bir birikim listesi değil,
> bir **tur günlüğüdür**; bağlayıcı olan kaynak dokümanlardır.
>
> Denetim: `python3 prototip-v4/_uret/denetim.py` →
> **18 sayfa · 122 yüzey · stil.css · 0 bulgu.**

## İş 1 · K-062 — gradyan zeminde metin

`stil.css` tarandı: `grad-action` **13 yerde** kullanılıyor; bunların
**yalnız biri metin taşıyor** (`.btn-primary`). Değişen:

| Yüzey | Önce | Sonra | Beyaz metinle |
|---|---|---|---|
| `.btn-primary` | `grad-action` | düz `var(--primary-deep)` | 4.25 (üst kenar) ❌ → **5.37 ✅** |
| `.btn-primary.basili` | `grad-action-press` | düz `var(--primary-press)` | **6.59 ✅** |

`.btn-primary.pasif`'teki artık gereksiz `background-image: none`
temizlendi (dolgu zaten `background-color`).

**Ölçüm beyan değil, doğrulama** (T-5'in dersi): buton headless Brave ile
390px genişlikte render edildi ve **metin satırı bandındaki arka plan
pikselleri örneklendi** — varsayılan `rgb(47,104,197)` = `#2F68C5`
(5.37), basılı `rgb(41,91,172)` = `#295BAC` (6.59). Metin bandında kil
gölgesinin açık iç parlaması **yok** (parlama üst 4-8px'te kalıyor, metin
y≈74-85'te).

**Metin taşımadığı için dokunulmayanlar** (grafik eşiği 3:1, en kötü
nokta `#3B82F6` = 3.68 ✅): `.fab` (28pt beyaz ikon), `.anahtar.acik`,
`.adim-dolu`, `.yuk-dolgu`, `.kaydirici-dolgu`, `.ilerleme-dolgu`,
`.durak-bag-dolu`, `07-acilis.html`'deki app icon zemini.
`.gun-kutu.altinda`, `.gun-kutu.secili`, `.durak.gecildi`,
`.imza-kare.altinda` zaten T-5'te düzleştirilmişti — **artık kural
bunların hepsini tek cümleyle kapsıyor** (tokens §1.6/§1.8).

## İş 2 · Hangi madde nereye işlendi

| Delta maddesi | Gittiği yer | Dayanak |
|---|---|---|
| T-1/1 kutlama zaman çizelgesi | `tokens.md` §8 (`motion.celebrate.hold` 700ms) | K-048 |
| T-1/2 `amount` rolü + gün sayısı | `tokens.md` §2.2 | T-1 |
| T-1/3 `.gun-ag` oluk telafisi | `tokens.md` §3.3 | T-1 |
| T-1/4 · T-2/15 · E-24/10 pasif eleman hâlleri | `tokens.md` §6 | T-1 · T-2 |
| T-1/5 · E-24/8-9 · T-3 · T-4 bileşen ölçüleri | `tokens.md` **§7.13** (yeni) | T-1…T-4 |
| T-1/6 · T-2/13 · E-24/11 kontrast çiftleri | `tokens.md` §1.9 ("v4'te eklenen" + "v4 bilinen sınırlar") | ölçüldü |
| T-1/7 ızgarada trafik ışığı yasağı | `tokens.md` §1.10 | T-1 |
| T-2/12 `12`'nin rolü forma uzadı | `tokens.md` §3.1 | T-2 |
| T-2/14 `button.social` · T-2/18 etiket istisnası | `tokens.md` §7.1 + §2.3 · `metinler.md` §0 | K-057/2, K-057/5 |
| T-2/16 beş Lucide glifi | `tokens.md` §9 · `varliklar.md` **§1.2d** (yeni) | K-057/2 |
| T-2/17 + T-5/7 denetim istisnaları | `tokens.md` **§12.0** (yeni): işletim sistemi çizimleri + üçüncü taraf | **K-061/6** · K-057/2 |
| T-3 `success` birikim segmenti | `tokens.md` §1.3 | K-059/4 |
| T-3 · T-4 formüller (kalan gün, plan zinciri, öneri, biriken, seri) | `tokens.md` **§14** (yeni) | K-059/6 · K-060/4 |
| T-5/B-2 "tek seçili dili" kuralı | `tokens.md` **§5.4** (yeni) + `bilesen-envanteri.md` §0 | K-045 · K-054/6 · K-061/2 |
| **K-062** | `tokens.md` §1.6 (yeniden yazıldı) · §1.8 · §1.10 · §7.1 · §12/5b | K-062 |
| T-1…T-4 yeni bileşenler (30) | `bilesen-envanteri.md` §1-§5 + §6 sayımı | — |
| §6 "takvim ızgarası / arama Faz 1'de yok" | `bilesen-envanteri.md` §6 **düzeltildi**: ikisi de MVP'de; rozet/başarım/puan hâlâ kapsam dışı | **K-054/3** · K-048 |
| T-1…T-4 metin anahtarları (~190) | `metinler.md` **§23-§27** (yeni) | — |
| Sekme 1 "Günlük" | `metinler.md` §1 (`sekme.gunluk`) · `ekran-envanteri.md` §1 | K-049 |
| §2'deki geçersiz E-02/E-03 anahtarları | `metinler.md` §2 **yeniden yazıldı** (gelir + maaş günü); `ob.s3.takip.alt` geçersiz işaretlendi | **K-059/2** · K-053 |
| §18 "yüzde Faz 1'de kullanılmaz" | `metinler.md` §18'den **kaldırıldı**; biçim `%59` | **K-059/1** |
| E-20 gelir sorusu | `metinler.md` §12 + §22.5 · `ekran-envanteri.md` akış G: **emekliye ayrıldı**, yerine Yatırım | **K-061/3** |
| Üçüncü taraf marka varlıkları | `varliklar.md` **§7** (yeni) + §6 özeti | **K-057/2** · K-058 |
| E-21…E-26 · durum matrisi · mood · akışlar H-K | `ekran-envanteri.md` §2, §2.1, §3, §5, §6 | K-048…K-053 |
| §7 "Faz 1'de olmayan ekranlar" | `ekran-envanteri.md` §7 **düzeltildi** (arama/takvim/hesap artık var) | K-050 · K-052 |

## Birleştirme sırasında yapılan üç ek düzeltme (sessiz değil, burada)

1. **`denetim.py` beyaz listesi daraltıldı.** Betik izinli hex kümesini
   `tokens.md`'nin tamamından topluyordu. §12.0 ve §7.1'e üçüncü taraf ve
   sistem klavyesi renkleri yazılınca bu **denetimi zayıflatacaktı**
   (`#1F1F1F` bir jeton değil, Google'ın kuralıdır). Kaynak artık
   **yalnız §1 RENK** bölümü. Negatif testle doğrulandı: `#1F1F1F` +
   `radius:4px` eklendiğinde **2 bulgu** verdi, satır geri alındı.
2. **§1.6/§1.9'daki gradyan ara durakları `rgb()` olarak yazıldı**
   (`rgb(55,121,229)` vb.). Bunlar jeton değil **ölçüm sonucudur**; hex
   yazılsaydı beyaz listeye girer ve paletin dışındaki bir maviyi
   meşrulaştırırdı.
3. **§12/9 satırına rakam eklenmedi.** "4 izinli değildir (K-061/5)"
   diye yazmak, `denetim.py`'nin o satırdan okuduğu izinli radius
   kümesine **4, 61 ve 5'i geri sokuyordu** — yani K-061/5'i sessizce
   iptal ediyordu. Açıklama rakamsız bir **9b** satırına taşındı.
   *(Aynı tuzağın genel hâli: makine tarafından okunan satıra serbest
   metin yazılmaz.)*

## `varliklar.md`'de düzeltilen devralınan çelişki

§4 (logo/uygulama varlıkları) ve §6 (kilit özeti) hâlâ **v1.0 "Defter"**
yönünün değerlerini taşıyordu: `#14484C` zemin, Source Serif 4 + Public
Sans, `TallyGraphic`, çizgi kalınlığı 1.75. `tokens.md` §10/§2.1/§9 ile
hizalandı (K-040: tokens otoritedir). Yeni karar alınmadı, **var olan
onaylı değerler yazıya geçirildi**.

## Kapanmayanlar (PM'e / başka sahibe)

| # | Madde | Sahibi | Not |
|---|---|---|---|
| 1 | **brandbook §2.3** başlığı hâlâ "FAZ 2 — seri/streak (Faz 1'de üretilmez)" diyor | `brand-strategist` / PM | K-048 seriyi MVP'ye aldı; ton satırları aynen kullanıldı, **faz etiketi eski**. Brandbook onaylı marka dosyası olduğu için bu ajan düzenlemedi |
| 2 | **brandbook §2.8** "depolama/mimari anlatan metin yasak" istisnası yazılmadı | `brand-strategist` / PM | K-057/1 istisnayı verdi (kullanıcı faydası dili izinli, mimari sözcükleri yasak). `metinler.md` §0'a işlendi; brandbook tarafı açık |
| 3 | **Gizlilik politikası + kullanım şartları** metinleri yok | PM / Mustafa | K-057/7 · yayın bloklayıcısı. E-23'teki iki bağlantı yer tutucu |
| 4 | **Hesap silme Edge Function** | geliştirme | K-057/4 · App Store 5.1.1(v); iş kalemi olarak açık |
| 5 | `fonts/fonts/` yinelenen dizini | Mustafa | Geri dönüşsüz silme onayı bekliyor (K-061/7). Zararsız duruyor |
| 6 | `CONTEXT.md` "en fazla 3 soru" cümlesi | PM | Katman 1 hâlâ 3 soru, ama Katman 2 (8 kart) ürünün parçası. Çelişki değil ama **cümle güncellenirse** okuyan ajan tereddüt etmez |

**Yorumlanmayan / uydurulmayan:** delta ile `tokens.md` çeliştiğinde
tokens otorite kabul edildi (K-040); bir K-kararı tokens'ı açıkça
değiştirdiğinde karar kazandı ve dayanak numarası satırın yanına yazıldı.
Emin olunamayan hiçbir madde "tamamlanmış" gibi yazılmadı; yukarıdaki
altı kalem açık bırakıldı.

