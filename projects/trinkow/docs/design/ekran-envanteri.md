# Trinkow — Ekran Envanteri ve Akış Haritası

> Faz 1 (MVP) kapsamındaki **tüm** yüzeyler. Tur 2'de yalnızca buradaki
> ekranlar çizilir; listede olmayan ekran tasarlanmaz.
> Bileşen adları: `projects/trinkow/docs/design/bilesen-envanteri.md` · Metinler:
> `projects/trinkow/docs/content/metinler.md` · Ölçüler: `projects/trinkow/docs/brand/tokens.md`.
> Tarih: 2026-09-10 · **v4 birleştirmesi: 2026-09-18**
>
> **v4'te değişen:** sekme 1'in adı **"Günlük"** (K-049, sekme sayısı 3
> kaldı) · E-02/E-03 yeniden tanımlandı (K-053: gelir + maaş günü) ·
> altı yeni ekran **E-21…E-26** · E-20'nin gelir sorusu **emekliye
> ayrıldı** (K-061/3) · §7'nin "Faz 1'de olmayan ekranlar" listesi
> gerçeğe göre düzeltildi.

---

## 1. Navigasyon yapısı

```
Uygulama
├── Onboarding yığını (yalnızca ilk açılışta)   E-00 → E-01 → E-02 → E-03
└── Ana yığın
    ├── Alt sekme çubuğu (3 sekme — tokens.md §7.7)
    │   ├── [1] Günlük     E-10   (açılış sekmesi · K-049)
    │   ├── [2] Kayıtlar   E-14
    │   └── [3] Özet       E-16
    ├── İtilen (push) ekranlar:  E-15 · E-17 · E-18 · E-19 · E-21 · E-24
    │                            E-22 · E-23 · E-25 · E-26
    └── Örtüşen (modal) yüzeyler: E-11 · E-12 · E-13 · E-20
```

**Sekme sayısı 3'tür ve artmaz** (K-049). Referans uygulamanın dört
sekmesi (Tarifler / Profil / Pro) alınmadı; Seri, Gün seçici, Hesap ve
Plan **itilen** ekranlardır — günde bir kez bile açılmayan yüzey,
günde beş kez basılan çubukta yer kaplamaz.

**Kararlar:**
- **Ayarlar sekme DEĞİL.** Günde bir kez bile açılmayacak bir yüzey,
  günde 5 kez basılacak çubukta yer kaplamaz. Ayarlara Pano'nun sağ
  üstündeki `settings` ikonundan girilir. (Sağ üst — sol üste kritik hedef
  konmaz, iOS geri kaydırması ile çakışır: `rn-tasarim-kisitlari.md`.)
- **Harcama ekleme modal (bottom sheet), ekran değil.** Sebep: kullanıcı
  Pano'yu gözünün ucuyla görmeye devam eder, kaydettiği anda çubuğun
  hareket ettiğini görür. Bu ürünün davranışsal döngüsünün tamamı budur.
- Sekme sayısı 3'te kalır; 4. sekme (Taksitler) reddedildi → E-18'e
  Özet ekranından girilir.

---

## 2. Ekran listesi

| ID | Ekran | Tek cümlelik işi | Tip |
|---|---|---|---|
| E-00 | Açılış (Splash) | Marka adını gösterir, veritabanını açar. | Sistem |
| E-01 | Niyet — Adım 1/3 | Kullanıcının neden geldiğini sorar (Takip/Bütçe/Borç). | Onboarding |
| E-02 | Aylık net gelir — Adım 2/3 | Aylık net geliri sorar; **atlanabilir** (K-053). | Onboarding |
| E-03 | Maaş günü — Adım 3/3 | Maaşın hangi gün yattığını sorar; dönem buradan kurulur. | Onboarding |
| E-10 | **Günlük (Pano)** | Görüntülenen günün durumunu gösterir, harcama eklettirir; günler arasında sayfalanır. | Sekme 1 |
| E-11 | **Harcama ekle** | Yeni harcamayı en az dokunuşla kaydeder. | Sheet |
| E-12 | Harcama detayı | Tek harcamayı düzenletir veya sildirir. | Sheet |
| E-13 | **Taksit serisi silme onayı** | Aylara yayılmış taksit serisinin tamamen silineceğini onaylatır. | Dialog |
| E-14 | Kayıtlar | Geçmiş harcamaları gün gün gösterir. | Sekme 2 |
| E-15 | Kategori detayı | Bir kategorinin harcamalarını ve limitini gösterir. | Push |
| E-16 | Özet | Günlük/haftalık toplamı ve kategori dağılımını gösterir. | Sekme 3 |
| E-17 | Limitler | Günlük ve kategori limitlerini değiştirtir. | Push |
| E-18 | Taksitler | Önümüzdeki aylara yayılmış taksit yükünü gösterir. | Push |
| E-19 | Ayarlar | Bildirim, gün sınırı, varsayılan ödeme, veri. | Push |
| E-20 | Profilleme sorusu | 2-4. günde tek soruyla profili derinleştirir. | Sheet |
| E-21 | **Seri** | Kaç gündür limit altında kapatıldığını, durakları ve son 4 haftayı gösterir. | Push |
| E-22 | **Oturum aç** | Var olan hesapla oturum açtırır; şifre sıfırlatır. | Push |
| E-23 | **Hesap oluştur** | Yeni hesap açtırır (e-posta/şifre ya da sağlayıcı). | Push |
| E-24 | **Gün seçici** | Ay ızgarasında gün durumlarını gösterir, seçilen güne götürür. | Push |
| E-25 | **Seni tanıyalım** | Katman 2: 8 kartla sabit gider, alışkanlık ve birikim profilini toplar. | Push (akış) |
| E-26 | **Planın hazır** | Payları, günlük limiti ve hesabın nasıl yapıldığını gösterir. | Push (akış) |

**Toplam 21 yüzey.** (5 ana ekran + 10 alt/akış ekranı + 4 modal +
onboarding 3 adım + splash.)

### 2.1 v4'te eklenen ekranların giriş / çıkış / boş / hata tablosu

| Kod | Giriş | Çıkış | Boş | Hata |
|---|---|---|---|---|
| E-21 | E-10 başlığındaki seri çipi | geri → E-10 | "Seri henüz başlamadı" · "Seri kapalı" (limitsiz kip) | okuma hatası E-10 ile aynı desende |
| E-22 | E-19 Hesap satırı · E-23'ten "Oturum aç" | başarılı → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (biçim · kimlik) + ağ şeridi |
| E-23 | E-19 Hesap satırı · E-22'den "Hesap oluştur" | başarılı → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (kayıtlı e-posta · kural) + ağ şeridi |
| E-24 | E-10 başlığındaki takvim düğmesi | gün dokunuşu → E-10 o güne gider | "Bu ayda kayıt yok" + Bugüne dön | okuma hatası E-10 ile aynı desende |
| E-25 | E-10'daki nötr "Limit belirle" kapısı · Ayarlar > Plan ve profil | "Planı gör" → E-26 · her an bırakılır ("Kaldığın yerden") | kart boş / "Hiç" cevabı | — (yerel, ağ yok) |
| E-26 | Katman 2'nin sonu · "Kaldığın yerden" · Ayarlar > Plan ve profil | "Planı kur" → limit E-10'a yazılır · "Şimdi değil" → geri | gelir yok ("Limitini yazalım") · yarım veri | negatif kalan → "Plan bu ay kurulamadı" + üç çıkış yolu |

**Hesap hiçbir akışın önkoşulu değildir** (K-052): onboarding, E-10 ve
E-11 hesapsız tam çalışır; oturum durumu hiçbir özelliği kilitlemez.
Uygulamada hesap için **tek davet** vardır: E-19'daki tek satır.

---

## 3. Akışlar

### A. İlk açılış (bir kez) — **Katman 1** (K-053)
`E-00` → `E-01` (niyet) → `E-02` (aylık net gelir · **atlanabilir**) →
`E-03` (maaş günü) → *(gelir girildiyse)* **günlük limit önerisi yüzeyi** →
`E-10`.
- Her adımda `StepIndicator` ("Adım 1/3") ve geri dönüş vardır.
- Katman 1 **3 soruda kalır** (CONTEXT: en fazla 3 soru). 8 kartlık
  **Katman 2 ayrı bir ekrandır** (E-25) ve onboarding'in parçası değildir.
- **Katman 1 sonunda günlük limit YOKTUR.** Gelir girildiyse tek dokunuşla
  onaylanacak bir **öneri** gösterilir (K-059/5); onaylanmazsa ya da gelir
  atlandıysa uygulama **limitsiz kipte** açılır ve bu dürüstçe yazılır
  ("Günlük limit — Henüz yok"). Limitsiz kipte seri çalışmaz (K-048).

### B. Günlük döngü — **en sık kullanılan akış**
`E-10` → `E-11` → kaydet → `E-10` (çubuk 280ms'de yeni değere gider + `Toast`).
E-11'de ürün arama **isteğe bağlı bir kısayoldur**: aranmazsa varsayılan
3 dokunuşluk yol (tutar → kategori → Kaydet) değişmez (K-050).

### C. Hızlı tekrar (Latte Faktörü akışı)
`E-10` listesinde bir satırı **sola kaydır** → "Tekrarla" → aynı tutar,
kategori ve ödeme tipiyle **bugüne** yeni kayıt + "Geri al" içeren `Toast`.

### D. Düzeltme ve silme — **K-029: etkiye göre iki yol**
`E-10`/`E-14` → satıra dokun → `E-12` → "Kaydet" **veya** silme:

| | Tek harcama | Taksit serisi |
|---|---|---|
| Eylem | "Sil" | "Taksit serisini sil" |
| Onay | **Yok** — kayıt anında gider | **E-13 diyaloğu** |
| Koruma | 6 sn'lik `Toast` + "Geri al" (toast.md §15) | Onaydan sonra geri alınamaz |
| Neden | Sık ve düşük etkili; her seferinde onay istemek onayı anlamsızlaştırır | Aylara yayılmış birden çok kayıt siliniyor |

Alternatif: satırı **sağa kaydır** → "Sil" (aynı iki yol geçerlidir).
`danger #DC2626` yalnız E-13'te ve silme toast'ının göstergesinde görünür.

### E. Anlama akışı (haftada 1-2)
`E-16` → kategori satırına dokun → `E-15` → "Limiti değiştir" → `E-17`.

### F. Limit düzeltme (markanın imza akışı)
Aynı ayda 5+ limit aşımı olduğunda `E-10`'da `Toast` değil, `Card` belirir:
"Bu ay 6. limit aşımı. Limit gerçekçi mi?" → "Limiti gözden geçir" → `E-17`.
Suç kullanıcıya değil **kuruluma** atılır (brandbook §2.3).

### G. Aşamalı profilleme (F-12)
2. gün: **yatırım** · 3. gün: taksit alışkanlığı · 4. gün: akşam bildirimi.
Her biri `E-20` sheet'i, günde **en fazla 1**, reddedilen soru 14 gün geri
gelmez.

> **K-061/3:** 2. günün sorusu eskiden "aylık gelir aralığı"ydı;
> **emekliye ayrıldı.** Gelir Katman 1'de tam tutar olarak alınıyor ve
> plan formülleri (tokens §14.2) tam tutar istiyor — aynı olguyu bir
> yerde aralık, bir yerde tutar sormak iki ayrı doğru üretirdi. Yerine
> E-25'in cevaplanmamış kartlarından **Yatırım** geldi: tek soru, tek
> dokunuş, klavye açılmaz. Eksik gelir **Ayarlar > Plan ve profil**'den
> tamamlanır.

### H. Gün gezinme (v4 · K-049 · K-055)
`E-10` → yana kaydırma **ya da** başlıktaki oklar → önceki gün sayfası.
**Geçmiş günler solda**, bugün en sağdaki sayfadır; gelecek sayfa
üretilmez. Uzağa gitmek için: `E-10` → başlıktaki takvim düğmesi →
`E-24` → gün dokunuşu → `E-10` (o gün). **"Seç" butonu yoktur** —
dokunuş hem seçer hem kapatır.
Geçmiş bir gün açıkken FAB aynı FAB'dır; `E-11`'i **o günün tarihiyle
ön dolu** açar.

### I. Seri (v4 · K-048)
`E-10` başlığındaki seri çipi → `E-21`. Çip yalnız **limitli kipte** ve
seri varken çizilir; limitsiz kipte ne çip ne de E-21 girişi vardır
(pasif çip ölü arayüzdür). Durak geçildiğinde `E-10`'da 1.2 saniyelik
kutlama kartı görünür — modal değildir, dokununca kapanır. Rozet, puan,
seviye üretilmez.

### J. Plan kurma (v4 · K-053)
`E-10`'daki nötr "Limit belirle" kapısı **ya da** Ayarlar > Plan ve
profil → `E-25` (8 kart, hepsi atlanabilir) → "Planı gör" → `E-26` →
"Planı kur" → günlük limit `E-10`'a yazılır. Akış her an bırakılabilir;
dönüşte "Kaldığın yerden" yüzeyi karşılar.
Kısa yol: kullanıcı planı hiç kurmadan `E-17`'den limiti **elle** yazabilir.

### K. Hesap (v4 · K-052 · K-058)
Ayarlar > Hesap satırı → `E-22` ⇄ `E-23`. Şifre sıfırlama E-22'nin bir
**durumudur**, ayrı ekran değildir. Sağlayıcı kümesi platforma göre
değişir: iOS'ta Apple + Google, Android'de yalnız Google.
Çıkış yapmak ve hesabı silmek **kayıtlara dokunmaz**; veri silme ayrı
kapıdır (Ayarlar > Veri).

---

## 4. E-11 — Harcama ekleme: **dokunuş bütçesi**

> Hedef (brandbook §7.4): **3 dokunuş.** Ölçüm kuralı: rakam tuşlarına
> basışlar sayılmaz (bunlar veri girişidir, kaçınılmazdır); **gezinme ve
> seçim** dokunuşları sayılır.

| # | Dokunuş | Neden kaçınılmaz |
|---|---|---|
| 1 | Pano'da "Harcama ekle" | Akışı başlatan tek dokunuş |
| — | Tutarı yaz | Sheet açılınca `AmountField` **otomatik odaklanır**, klavye hazır gelir. Alana dokunmak gerekmez → **1 dokunuş kazanıldı** |
| 2 | Kategori çipine dokun | Frekansa göre sıralı ilk 6 çip görünür; tahmin edilen kategori en solda |
| 3 | "Kaydet" | Klavyenin hemen üstünde sabit (`KeyboardAvoidingView`) |

**Sonuç: 3 dokunuş.** Sheet varsayılanları bu sayıyı korumak için seçildi:

| Alan | Varsayılan | Ek dokunuş |
|---|---|---|
| Tarih | **Bugün** | 0 |
| Ödeme tipi (F-6) | Ayarlardaki varsayılan (kurulumda "Kart") | 0 |
| Taksit (F-7) | Yok | 0 |
| Not | Boş | 0 |

**Kısa yollar ve maliyetli yollar:**
- "Tekrarla" (akış C): **2 dokunuş** (kaydırma + eylem). Aynı kahveyi her
  gün giren kullanıcı için en hızlı yol.
- Ödeme tipini değiştirme: **+1** · Tarihi düne alma: **+2** ·
  Taksitli yapma: **+2** (K-023: "Taksitli" çipi → taksit sayısı. Ayrı bir "Uygula" adımı yoktur, sayıya dokunmak seçimi bitirir). Bunlar seyrek
  yollardır ve bilinçli olarak varsayılan akışın dışına konmuştur.
- **Kategori önceden seçili gelmez.** Gelseydi 2 dokunuşa inerdi ama
  yanlış kategoriye sessizce kayıt riski doğardı; marka *Dürüst*
  (brandbook §2.1). Bu, bilinçli olarak ödenen 1 dokunuştur.

---

## 5. Ekran başına durum matrisi

Her ekran için Tur 2'de **çizilmesi zorunlu** durumlar:

| ID | boş | dolu | hata | yükleniyor | özel durum |
|---|---|---|---|---|---|
| E-01 | — | var | seçim yapılmadan devam → buton `disabled` | — | — |
| E-02 | var (**atlanabilir** — "Atla" her zaman açık) | var | — (gelir doğrulaması yok, yaklaşık yeter) | — | Gelir atlanırsa özet "Henüz yok" der |
| E-03 | — | var | — | — | "Düzensiz geliyor" → dönem 30 gün · maaş günü ayda yoksa ayın son günü |
| E-10 | var **ilk gün** · var **limitsiz** | var | veri okunamadı → `ErrorState` | ≥150ms `Skeleton` | **`overflow` (limit dışı)** · uzun liste · `ProfilingSheet` görünür varyant · **geçmiş gün sayfası** (kapanmış gün) · **harcamasız gün** · **kutlama kartı** |
| E-11 | var (tutar 0) | var | boş tutar · 0 ₺ · gelecek tarih | Kaydet `loading` | Taksit açık · uzun tutar (`1.250.000,50 ₺`) · uzun not |
| E-12 | — | var | kayıt bulunamadı | Kaydet `loading` | Taksitli kayıt (seri uyarısı) · **silme sonrası geri al toast'ı** |
| E-13 | — | var (**yalnız taksit serisi**) | — | Sil `loading` | Tek harcama silme bu diyaloğu **açmaz** → E-12'de geri al toast'ı (K-029) |
| E-14 | var (hiç kayıt yok) | var | okuma hatası | var | Ay değiştirici · limit dışı satırlar · 200+ kayıt (`FlatList`) |
| E-15 | var (bu kategoride kayıt yok) | var | — | var | Kategori limiti yok · kategori limiti aşıldı |
| E-16 | var (hafta boş) | var | — | var | Hafta ortası (eksik günler) · tüm hafta limit dışı |
| E-17 | var (kategori limiti hiç yok) | var | limit < 0 · limit toplamı günlük limitle çelişiyor → bilgi notu | Kaydet `loading` | — |
| E-18 | var (taksit yok) | var | — | var | 12 aya yayılan seri · biten seri |
| E-19 | — | var | bildirim izni reddedilmiş → satır açıklaması değişir + saat satırı düşer | — | Gün sınırı seçimi (F-15) · **tüm verileri sil onayı** (`Dialog`, yüksek etki) |
| E-20 | — | var | — | — | "Şimdi değil" ile kapatma |
| E-21 | var (seri başlamadı) · var (**seri kapalı** — limitsiz kip) | var | okuma hatası E-10 deseni | var | Seri kırıldı · durak sırada · 28 günlük pencere boş |
| E-22 | — (form) | var | alan düzeyinde: biçim · kimlik · ağ şeridi | Oturum açılıyor | Şifre bağlantısı gönderildi + "Yeniden gönder" `disabled` · Android (yalnız Google) |
| E-23 | — (form) | var | kayıtlı e-posta · kural karşılanmadı · ağ şeridi | Hesap oluşturuluyor | Şifre görünür · yasal bağlantı `pressed` · Android (yalnız Google) |
| E-24 | var ("Bu ayda kayıt yok") | var | okuma hatası E-10 deseni | var | Başlangıç ayından öncesi **pasif** · bugünün ayında sağ ok `disabled` |
| E-25 | var (kart cevaplanmadı) | var | — (yerel) | — | "Hiç" cevabı · yarıda bırakma → "Kaldığın yerden" · birikim üst sınırı |
| E-26 | var (gelir yok → "Limitini yazalım") | var | **negatif kalan** → "Plan bu ay kurulamadı" + üç çıkış | iskelet (pay çubuğu + denklem) | Yarım veri ("Plan yarım hazır") · alışkanlık kartları boş |

**"Her şey yolunda" ekranı tek başına teslim edilmez** — yukarıdaki her satırdaki durumlar Tur 2 kapsamındadır.

---

## 6. Ekran başına "mood" (birbirinin klonu olmasın diye)

Palet, tipografi ve düzen sistemi **aynı**; değişen şey içerik yoğunluğu
ve dikey ritim.

| Ekran | Mood | Nasıl elde edilir |
|---|---|---|
| E-10 Bugün | **Sakin ve tek odaklı** | Ekranın üst yarısı neredeyse boş: tek büyük sayı + tek çubuk. Liste alt yarıda başlar |
| E-11 Harcama ekle | **Hızlı, klavye öncelikli** | Sayı ekranın en üstünde ve devasa; her şey klavyenin üstüne sığar, kaydırma yok |
| E-14 Kayıtlar | **Defter** | Sık dikey ritim, 1px ayraçlar, yapışkan gün başlıkları; hiç kart yok |
| E-16 Özet | **Ölçüm sayfası** | Hairline `WeekStrip` + tabular sayı sütunu; grafik değil çizelge hissi |
| E-17 Limitler | **Ayar masası** | Form ağırlıklı, her satır tek karar; değer satırları çukur, kararlar kabarık. Kaydet vardır |
| E-15 Kategori detayı | **Karne** | Tek konunun sayfası: kategori kimliği tek yerde, listenin sol sütunu gün kutusu (ikon tekrarlanmaz), ölçü nesnesi kategori çubuğu |
| E-18 Taksitler | **Yük haritası** | Ürünün tek ileri bakan yüzeyi: üstte ay şeridi, altta seriler. Yorum yok, süre ve sayı var |
| E-19 Ayarlar | **Arka oda** | E-17'nin kardeşi ama **Kaydet yok** — her anahtar dokunulduğu an geçerli; ekranda birincil buton bulunmaz |
| E-20 Profilleme | **Kısa nefes (davetsiz)** | Onboarding'le aynı aile, farkı: kullanıcı gelmedi, soru gününe düştü → iki çıkış kapısı + cevabın karşılığı gösterilir |
| E-01…E-03 | **Kısa nefes** | Ekran başına tek soru, çok boşluk, tek birincil buton |
| E-21 Seri | **Çetele** | Tek büyük sayı + yatay durak rayı + 28 kutuluk sessiz ızgara. Kutlama hariç hareket yok; övgü değil **tespit** |
| E-22 · E-23 | **Eşik** | Duvar değil kapı: iki sağlayıcı düğmesi, kısa form, altta tam genişlikte "Hesapsız devam et". Ekranın vaadi tek cümlede ("Harcamaların sende kalır.") |
| E-24 Gün seçici | **Alet paneli** | Bilgi yoğun ay ızgarası + kelimeli lejant + üç satırlık özet. Boşlukla değil, ritimle ferahlar |
| E-25 Seni tanıyalım | **Sohbet temposu** | Kart başına tek soru, her kartta görünür "Bu kartı atla"; ilerleme tek oluk + `n/8`. Sigara/alkol kartları diğerlerinin birebir kopyası — yargı yok |
| E-26 Planın hazır | **Döküm** | Başarı ekranı değil hesap özeti: pay çubuğu, denklem satırı, "Nasıl hesaplandı". Konfeti, rozet, skor yok |

---

## 7. Faz 1'de OLMAYAN ekranlar (bilinçli)

Filtre paneli · pasta/çizgi grafik · profil ekranı · bildirim merkezi ·
veri dışa aktarma · yedekleme/senkron · karanlık mod anahtarı ·
**başarım/rozet/puan** · paylaşım ("Başarını paylaş") · arkadaşlar ·
Pro/paywall · fiş fotoğrafı · banka bağlama.

Bunlar çizilmez; talep gelirse PM'e sorulur.

> **v4 düzeltmesi (K-050 · K-048 · K-052):** bu liste "arama", "takvim
> ızgarası" ve "hesap/giriş"i de sayıyordu. Üçü de sonradan **MVP'ye
> alındı** ve üretildi: ürün arama (E-11 içinde), gün seçici (E-24) ve
> oturum açma / hesap oluşturma (E-22 · E-23). Liste gerçekle
> hizalandı; **rozet/puan/paylaşım hâlâ kapsam dışıdır** — seri bir
> sayaçtır, ödül ekonomisi değil.
