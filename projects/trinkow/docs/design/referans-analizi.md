# Referans Tasarım Analizi — Mustafa'nın verdiği video

Kaynak: Dribbble video (kalori takip uygulaması), 19 sn, 2880×2160.
Kareler: `projects/trinkow/docs/design/referans-gorseller/` — `hd_anaekran.jpg`,
`hd_pano.jpg`, `hd_detay.jpg` (yüksek çözünürlük) + `kare_*.jpg`.

**PM videoyu kare kare izledi.** Aşağıdakiler tahmin değil, gözlem.
Ajanlar bu dosyayı okumakla yetinmesin — `referans-gorseller/` altındaki
görselleri **açıp baksın** (Read aracı görsel okur).

> Mustafa'nın kararı: *"Tasarımlar fazla amatör geldi… ruhsuz bir UI/UX
> istemiyorum… bu videodaki gibi bir UI/UX istiyorum… tasarımların
> tamamını değiştirsin."*

---

## Referansın tasarım dili (gözlemlenen)

### 1. Kahraman: dairesel ilerleme halkası
- Kalın çizgili **daire/yay**, koyu (neredeyse siyah) dolgu + açık gri iz.
- Ucunda **yuvarlak kap + küçük topuz (knob)** — ilerlemeye fiziksellik katıyor.
- Ortada **çok büyük sayı** (`460/1600`), altında küçük gri etiket
  (`Calories`). Sayı kahraman, etiket fısıltı.
- Aynı dil küçük ölçekte tekrar ediyor: her metrik kartında **mini dairesel
  gösterge** (34g Protein left, 25g Carbs left, 14g Fat over).

### 2. Kartlar
- **Çok yumuşak köşe** (~20-28px), saf beyaz zemin.
- Kenarlık yok; ayrım **yumuşak gölge/yükseklik** ile yapılıyor.
- Kartlar zeminden "kalkık" duruyor — katmanlı kompozisyon.

### 3. Renk cömertçe ama yumuşak kullanılıyor
- Her metriğin **kendi pastel tonu**: şeftali, lavanta, nane.
- Pill/hap biçiminde etiketler, içinde küçük renkli ikon.
- Üst başlıkta **mor gradyan** bant; arka planda ortam gradyanı.
- Grafiklerde **gradyanlı alan dolgusu**, zirvede yüzen rozet (`84%`).
- BMI ölçeği: uçtan uca **çok renkli gradyan şerit**.

### 4. Tipografi
- **Geometrik/nötr sans**, serif yok.
- Sayılar kalın ve büyük; açıklamalar küçük, gri, sessiz.
- Hiyerarşi boyut kontrastıyla kuruluyor (12px etiket ↔ 40px sayı).

### 5. Butonlar
- **Tam yuvarlak (pill), koyu/siyah** birincil buton ("Update my goal",
  "Done") — yüksek kontrast, net çağrı.
- İkincil buton açık zeminli, aynı pill geometrisi.

### 6. Navigasyon
- Alt sekme çubuğu **yüzen**, yuvarlatılmış.
- **Ortada vurgulu eylem** dairesi (kamera/ekle) — merkezde bir odak var.

### 7. Üst bölge
- Kişisel karşılama ("Welcome Back / Stay On Track Today") + avatar.
- **Yatay tarih şeridi**: günler pill olarak, seçili gün dolu mor daire.

### 8. Fotoğraf
- Yemek fotoğrafları **tam genişlik, büyük**. Ürünün içeriğini görselleştiriyor.

---

## Ruhu veren şey ne? (asıl ders)

Referans "süslü" olduğu için değil, şu dört sebeple canlı hissettiriyor:

1. **Tek bir kahraman öğe var.** Ekranı dairesel halka yönetiyor; gözün
   nereye gideceği belli. Bizim tasarımda her şey eşit ağırlıkta.
2. **Derinlik var.** Kartlar zeminden kalkıyor, katman hissi oluşuyor.
3. **Renk bilgi taşıyor.** Her kategori kendi tonunu taşıyor → ekran hem
   renkli hem okunabilir.
4. **Geometri dostane.** Yüksek köşe yarıçapı + daire + pill = yumuşak,
   yaklaşılabilir. Keskin/dik geometri "resmi belge" hissi verir.

---

## ⚠️ ÇATIŞMA — bu referans mevcut brandbook'un ZIDDI

Bu bir uygulama hatası değil; **onaylı marka yönünün doğal sonucu.**
Ekranları yeniden çizmek, brandbook aynı kalırsa aynı hissi üretir.

| Referans | Onaylı brandbook (Yön A "Defter") |
|---|---|
| Dairesel halka + topuz | **Düz çubuk** |
| Her metrik kendi pastel renginde | **Kategoriler renk taşımaz** (§3.4) |
| Yumuşak gölge, kalkık kartlar | **Gölge KULLANILMIYOR** (§6.4) |
| Gradyan başlık, gradyan grafik dolgusu | **Gradyan yasak** (anti-pattern) |
| Geometrik sans | **Source Serif 4** (serif) |
| Siyah pill buton, çok yuvarlak | Petrol accent, tek radius kuralı |
| Tam genişlik fotoğraf | **"Fotoğraf yok, illüstrasyon yok"** (§6.2) |
| Çok sayıda yumuşak vurgu rengi | **"Ekrandaki TEK vurgu rengi"** |
| Mor/lavanta ortam gradyanı | Anti-pattern listesi **1. maddesi**: "Mor-mavi varsayılan gradyan arka planlar" |

**Sonuç:** Referansı benimsemek = brandbook'u değiştirmek (Aşama 1 işi).
Yalnızca ekranları yeniden çizmek yetmez.

### Anti-pattern listesiyle ilgili dürüst not
Referansın kullandığı bazı öğeler bizim yasak listemizde:
mor-lavanta gradyan arka plan, her karta uygulanmış yumuşak gölge,
3'lü eşit kart dizilimi. Mustafa emoji maddesinde yaptığı gibi bu maddeleri
de gevşetebilir — ama **bilerek** yapılmalı, sessizce ihlal edilmemeli.

Ayrıca dikkat: referanstaki mor/lavanta bir **Dribbble sunum estetiği**.
Trinkow'un kendi rengi olmak zorunda değil. Alınması gereken şey **renk
seçimi değil, tasarım dili**: dairesel kahraman gösterge, derinlik,
kategori başına renk, yumuşak geometri, büyük sayı + sessiz etiket.
Rengi kopyalarsak "bir başka mor SaaS" oluruz — kaçındığımız şey buydu.

---

## İkinci karar: UI'da teknik açıklama YASAK

> Mustafa: *"kullanıcı verinin nereye kaydedildiği hakkında niye bir bilgi
> edinmek istesin, UI'da açıklama koymak için hiçbir teknik açıklama
> girilmesin."*

`projects/trinkow/docs/content/metinler.md`'de temizlenecek satırlar:
- `:312` `ayar.veri_aciklama` → "Kayıtların yalnızca bu cihazda. Hesap yok,
  sunucu yok."
- `:329` `prof.aciklama` → "Cevabın cihazda kalır."
- `:361` `hata.okuma.govde` → "Veriler bu cihazda tutuluyor ve şu an
  okunamadı."
- `:363` `hata.okuma.ayrinti` → "Teknik detay bunun altında saklanır"

**Kural:** Kullanıcıya depolama/mimari anlatılmaz. Hata mesajı ne olduğunu
değil **ne yapacağını** söyler ("Tekrar dene"). Uygulamanın nasıl çalıştığı
kullanıcının sorunu değildir.
