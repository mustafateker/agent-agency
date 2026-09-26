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
>
> **REV2 senkronu (2026-09-25 · hijyen turu, yeni ekran tasarlanmadı):**
> sekmeler **Günlük · Tasarruf · Profil** ve **FAB kaldırıldı** · sekme 2/3
> (Kayıtlar · Özet) itilen ekrana indi · üç yüzey eklendi (**E-27 · E-28 ·
> E-29**) · kurulum **4 adım** oldu, ayrı "maaş günü" adımı kalmadı ·
> hesap **zorunlu** (K-080, K-052'nin "önkoşul değil" hükmü düştü) ·
> harcama ekleme ekranından **kategori seçimi** kaldırıldı.
> Otorite: `design/rev2-onboarding-kayit.md` ve
> `design/rev2-tasarruf-profil.md`.

---

## 1. Navigasyon yapısı

```
Uygulama
├── Giriş duvarı (K-080 · hesap zorunlu)        E-22 ⇄ E-23
├── Kurulum yığını (hesap açıldıktan sonra bir kez)
│                                               E-00 → 1/4 → 2/4 → 3/4 → 4/4
└── Ana yığın
    ├── Alt sekme çubuğu (3 sekme · FAB YOK — REV2 · tokens.md §7.7)
    │   ├── [1] Günlük     E-10   (açılış sekmesi · K-049)
    │   ├── [2] Tasarruf   E-27   (REV2 · eski [2] Kayıtlar E-14'ün yerine)
    │   └── [3] Profil     E-28   (REV2 · eski [3] Özet E-16'nın yerine)
    ├── İtilen (push) ekranlar:  E-14 · E-15 · E-16 · E-17 · E-18 · E-19
    │                            E-21 · E-24 · E-25 · E-26 · E-29
    └── Örtüşen (modal) yüzeyler: E-11 · E-12 · E-13 · E-20
```

**REV2: `Fab` kaldırıldı.** Harcama ekleme girişi Günlük'teki kategori
satırının `+` düğmesidir; sekme çubuğunda büyük `+` yoktur
(`rev2-tasarruf-profil.md` §1.1). Eski `/kayitlar` rotası `/tasarruflar`a
yönlenir; **E-14 ve E-16 silinmedi**, itilen ekran olarak yaşar (E-16'ya
Profil > Takip > Aylık özet satırından girilir).

> **ID çakışması — PM doğrulaması gerekiyor.** `rev2-*.md` belgeleri giriş
> ekranına **E-15**, hesap oluşturmaya **E-16** diyor; bu envanterde bu
> ID'ler **Kategori detayı** ve **Özet**'e ait. Eşleme: rev2'nin "E-15
> Giriş" = **E-22**, rev2'nin "E-16 Hesap oluştur" = **E-23**. Tek bir
> numaralandırmaya geçmek (hangi tarafın yeniden numaralanacağı) PM kararıdır;
> bu turda hiçbir ID değiştirilmedi.

**Sekme sayısı 3'tür ve artmaz** (K-049). Referans uygulamanın dört
sekmesi (Tarifler / Profil / Pro) alınmadı; Seri, Gün seçici, Hesap ve
Plan **itilen** ekranlardır — günde bir kez bile açılmayan yüzey,
günde beş kez basılan çubukta yer kaplamaz.

**Kararlar:**
- **Ayarlar sekme DEĞİL.** Günde bir kez bile açılmayacak bir yüzey,
  günde 5 kez basılacak çubukta yer kaplamaz. **REV2:** ayarlara artık
  Profil sekmesinden girilir (başlıktaki ikon düğmesi **ve** "Tüm ayarlar"
  satırı — iki yol, biri yedek); Günlük'ün sağ üstündeki `settings` ikonu
  tek kapı değildir. (Sağ üst — sol üste kritik hedef konmaz, iOS geri
  kaydırması ile çakışır: `rn-tasarim-kisitlari.md`.)
- **Harcama ekleme modal sunumda açılır, sekme değildir.** Sebep: kullanıcı
  Günlük'ü gözünün ucuyla görmeye devam eder, kaydettiği anda sayının
  değiştiğini görür. Bu ürünün davranışsal döngüsünün tamamı budur.
  **REV2:** giriş noktası FAB değil, ilgili kategori satırının `+`'sıdır ve
  ekran kategoriyi `?kategori=` param'ıyla **hazır** alır.
- Sekme sayısı 3'te kalır; 4. sekme (Taksitler) reddedildi → E-18'e
  **REV2'de Profil > Kayıt kolaylıkları > Taksitler** satırından girilir.

---

## 2. Ekran listesi

| ID | Ekran | Tek cümlelik işi | Tip |
|---|---|---|---|
| E-00 | Açılış (Splash) | Marka adını gösterir, veritabanını açar, oturumu doğrular. **REV2: ağ hatasında `ErrorState` değil giriş ekranı (E-22) gelir.** | Sistem |
| E-01 | Niyet — **Adım 1/4** | Kullanıcının neden geldiğini sorar (takip / tasarruf / borç). **Varsayılan seçim yok** (REV2). | Kurulum |
| E-02 | **Gelir ve gider — Adım 2/4** | Geliri, sabit giderleri ve hedefi alır; hedef etiketi **niyete göre değişir** (REV2). Gelir zorunlu, diğerleri değil. | Kurulum |
| E-03 | **Rutinler — Adım 3/4** | Günlük tekrar eden harcamaları `RoutineSheet` ile toplar; "Rutin harcamam yok" ile atlanır. **REV2: eski "maaş günü" adımı kaldırıldı**, "maaş" sözcüğü kurulum ekranlarından çıktı; dönem düzensiz sayılır ve maaş günü Profil > Maaş ve bütçe'den girilir. | Kurulum |
| E-03b | **Plan özeti — Adım 4/4** | Günlük limiti ve nasıl hesaplandığını gösterip akışı kapatır (REV2'de eklenen dördüncü adım; kalıcı ID **PM doğrulaması gerekiyor**). | Kurulum |
| E-10 | **Günlük (Pano)** | Görüntülenen günün durumunu gösterir, harcama eklettirir; günler arasında sayfalanır. | Sekme 1 |
| E-11 | **Harcama ekle** | Yeni harcamayı en az dokunuşla kaydeder. | Sheet |
| E-12 | Harcama detayı | Tek harcamayı düzenletir veya sildirir. | Sheet |
| E-13 | **Taksit serisi silme onayı** | Aylara yayılmış taksit serisinin tamamen silineceğini onaylatır. | Dialog |
| E-14 | Kayıtlar | Geçmiş harcamaları gün gün gösterir. **REV2: sekme değil** — `/kayitlar` rotası `/tasarruflar`a yönlenir, ekran itilen yüzey olarak yaşar. | Push |
| E-15 | Kategori detayı | Bir kategorinin harcamalarını ve limitini gösterir. | Push |
| E-16 | Özet | Günlük/haftalık toplamı ve kategori dağılımını gösterir. **REV2: sekme değil** — Profil > Takip > "Aylık özet" satırından açılır. | Push |
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
| E-27 | **Tasarruf** (REV2) | Ayın birikimini tek kahraman göstergeyle, denklemiyle ve hareketleriyle gösterir. | Sekme 2 |
| E-28 | **Profil** (REV2) | Kimliği gösterir ve planı/kayıt kolaylıklarını/takibi/uygulamayı 4 grupta 9 satırla dağıtır. | Sekme 3 |
| E-29 | **Tüm birikim hareketleri** (REV2 · `/birikimler`) | Ayın 5 satırlık özetinin tamamını **salt okunur** listeler. ID bu turda verildi — **PM doğrulaması gerekiyor**. | Push |

**Toplam 25 yüzey** (REV2 sonrası): 3 sekme + 12 itilen/akış ekranı +
4 modal + kurulum 4 adım + splash. *(v4'te 21 yazıyordu; sekmelerin
itilene inmesi yüzey sayısını azaltmadı.)*

### 2.1 v4'te eklenen ekranların giriş / çıkış / boş / hata tablosu

| Kod | Giriş | Çıkış | Boş | Hata |
|---|---|---|---|---|
| E-21 | E-10 başlığındaki seri çipi | geri → E-10 | "Seri henüz başlamadı" · "Seri kapalı" (limitsiz kip) | okuma hatası E-10 ile aynı desende |
| E-22 | E-19 Hesap satırı · E-23'ten "Oturum aç" | başarılı → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (biçim · kimlik) + ağ şeridi |
| E-23 | E-19 Hesap satırı · E-22'den "Hesap oluştur" | başarılı → gelinen ekran · "Hesapsız devam et" → geri | — (form) | alan düzeyinde (kayıtlı e-posta · kural) + ağ şeridi |
| E-24 | E-10 başlığındaki takvim düğmesi | gün dokunuşu → E-10 o güne gider | "Bu ayda kayıt yok" + Bugüne dön | okuma hatası E-10 ile aynı desende |
| E-25 | E-10'daki nötr "Limit belirle" kapısı · Ayarlar > Plan ve profil | "Planı gör" → E-26 · her an bırakılır ("Kaldığın yerden") | kart boş / "Hiç" cevabı | — (yerel, ağ yok) |
| E-26 | Katman 2'nin sonu · "Kaldığın yerden" · Ayarlar > Plan ve profil | "Planı kur" → limit E-10'a yazılır · "Şimdi değil" → geri | gelir yok ("Limitini yazalım") · yarım veri | negatif kalan → "Plan bu ay kurulamadı" + üç çıkış yolu |

**K-080 düzeltmesi (REV2 · K-052'nin bu hükmü düştü): hesap ZORUNLUDUR.**
Uygulama giriş duvarıyla açılır (E-22 ⇄ E-23), "Hesapsız devam et" yoktur
ve kurulum ancak hesap açıldıktan sonra başlar. E-19'daki "tek davet"
cümlesi geçersiz; hesap yönetimi Profil'deki kimlik panelinden ve
Ayarlar > Hesap'tan yapılır.

---

## 3. Akışlar

### A. İlk açılış (bir kez) — **Katman 1** (K-053 · REV2'de yeniden yazıldı)
`E-00` → `E-22` giriş **ya da** `E-23` hesap oluştur (K-080: zorunlu) →
kurulum `1/4` niyet → `2/4` gelir ve gider → `3/4` rutinler → `4/4` plan
özeti → "Trinkow'u kullanmaya başla" → `E-10`.
- Akış kendi kabuğundadır (`SetupShell`): geri oku + `StepIndicator`
  kaydırma alanının **dışında sabit**; "Kurulum · 1/4" kocaman başlığı
  **yoktur**. Her adımda geri dönüş vardır ve geri dönmek girdiyi silmez.
- `StepIndicator` **`toplam=4`** ile çalışır; eski "Adım 1/3" metni geçersiz.
- **Ayrı "maaş günü" adımı yok** (REV2): dönem düzensiz sayılır, maaş günü
  Profil > Maaş ve bütçe'den girilir. Adım 2 tek ekranda gelir + sabit
  giderler + hedefi alır; hedef etiketi adım 1'deki niyete göre değişir.
- 8 kartlık **Katman 2 ayrı bir ekrandır** (E-25), kurulumun parçası değildir.
- **Kurulum sonunda günlük limit adım 4/4'te gösterilir**; gelir yoksa
  limit "Henüz yok" der ve uygulama **limitsiz kipte** açılır (K-059/5).
  Limitsiz kipte seri çalışmaz (K-048).

### B. Günlük döngü — **en sık kullanılan akış**
`E-10` → ilgili **kategori satırının `+`**'sı → `E-11` (kategori hazır) →
kaydet → `E-10` (gösterge yeni değere gider + `Toast`).
**REV2:** E-11'de kategori **seçilmez** — `?kategori=` param'ından ya da
seçilen üründen gelir ve ekranda salt okunur göstergedir; "önceden bütçeden
ayrılan sabit ödeme" bölümü de kaldırıldı. Varsayılan yol böylece
**2 dokunuşa** iner (§4). Ürün arama/favori yine **isteğe bağlı
kısayoldur** (K-050).

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
Geçmiş bir gün açıkken **kategori satırının `+`'sı** aynı düğmedir (REV2:
FAB yok); `E-11`'i **o günün tarihiyle ve o kategoriyle** ön dolu açar.

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

### K. Hesap (v4 · **K-080** · K-058 · K-086)
Uygulama **giriş duvarıyla açılır**: `E-22` ⇄ `E-23` (K-080; "Hesapsız
devam et" yok). Ayarlar > Hesap ve Profil'deki kimlik paneli aynı ekranların
ikinci kapısıdır. Sağlayıcı kümesi platforma göre değişir: iOS'ta
Apple + Google, Android'de yalnız Google.
**REV2/Rev düzeltmeleri:** (1) şifre sıfırlama E-22'nin bir durumu değil,
**iki ayrı rotadır** (`/sifremi-unuttum` → `/sifre-sifirla`) ve bu envanterde
ID'leri yok — **PM doğrulaması gerekiyor**; (2) "hesabı silmek kayıtlara
dokunmaz" cümlesi **geçersiz**: hesap silme kullanıcının **tüm verisini**
siler (K-086) ve kendi ekranında (`/hesap-sil`) sonucu birebir yazar.
Çıkış yapmak veriye dokunmaz.

---

## 4. E-11 — Harcama ekleme: **dokunuş bütçesi**

> Hedef (brandbook §7.4): **3 dokunuş** — REV2 sonrası gerçekleşen: **2**.
> Ölçüm kuralı: rakam tuşlarına
> basışlar sayılmaz (bunlar veri girişidir, kaçınılmazdır); **gezinme ve
> seçim** dokunuşları sayılır.

> **REV2 güncellemesi:** kategori seçimi ekrandan kalktığı için bütçe
> **3 → 2 dokunuşa** indi. Kategori bilgisi girişin kendisinden gelir.

| # | Dokunuş | Neden kaçınılmaz |
|---|---|---|
| 1 | Günlük'te ilgili **kategori satırının `+`**'sı | Akışı başlatan tek dokunuş; kategoriyi de bu dokunuş belirler |
| — | Tutarı yaz | Ekran açılınca tutar alanı **otomatik odaklanır**, native `decimal-pad` hazır gelir. Alana dokunmak gerekmez → **1 dokunuş kazanıldı** |
| 2 | "Kaydet" | Sabit alt blokta, `KeyboardAvoidingView` ile klavyenin üstünde görünür kalır |

**Sonuç: 2 dokunuş** (REV2; v4'te 3'tü). Varsayılanlar bu sayıyı korumak
için seçildi:

| Alan | Varsayılan | Ek dokunuş |
|---|---|---|
| Kategori | **Girilen yoldan gelir** (kategori satırı / ürün / favori) — ekranda salt okunur | 0 |
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
- ~~**Kategori önceden seçili gelmez.**~~ **REV2'de bu karar tersine
  döndü:** kategori artık girilen yoldan (kategori satırının `+`'sı, ürün,
  favori, rutin) gelir ve ekranda **salt okunur göstergedir**. Dürüstlük
  kaybolmadı, yer değiştirdi: kullanıcı kategoriyi **girmeden önce**
  seçiyor ve seçtiğini kaydetme ekranında okuyor; "sessizce yanlış
  kategori" riski kategorisiz yolun **kapatılmasıyla** çözüldü (kategorisiz
  ulaşan bilinen bir yol kalmadı). Kazanılan: 1 dokunuş.

---

## 5. Ekran başına durum matrisi

Her ekran için Tur 2'de **çizilmesi zorunlu** durumlar:

| ID | boş | dolu | hata | yükleniyor | özel durum |
|---|---|---|---|---|---|
| E-01 (1/4) | — | var | seçim yapılmadan devam → buton `disabled` | — | **Varsayılan seçim yok** — üç kart da `default` açılır (REV2) |
| E-02 (2/4) | var (gelir boş → birincil `disabled`) | var | gelir 0/boş · sabit gider satırı hatalı | Plan kuruluyor (`busy`) | Hedef etiketi **niyete göre** değişir · `fontScale > 1.3`'te `MoneyRow` dikeye döner |
| E-03 (3/4) | var ("Eklediğin rutinler burada sıralanır.") | var | sheet alan hatası (ad/fiyat) | — | "Rutin harcamam yok" ile atlama · `RoutineSheet` `edit` kipi |
| E-03b (4/4) | var (gelir yoksa limit "Henüz yok") | var | — | iskelet (limit satırı) | Sessiz kutlama: konfeti/rozet/puan yok (K-048) |
| E-10 | var **ilk gün** · var **limitsiz** | var | veri okunamadı → `ErrorState` | ≥150ms `Skeleton` | **`overflow` (limit dışı)** · uzun liste · `ProfilingSheet` görünür varyant · **geçmiş gün sayfası** (kapanmış gün) · **harcamasız gün** · **kutlama kartı** |
| E-11 | var (tutar 0) | var | boş tutar · 0 ₺ · gelecek tarih | Kaydet `loading` | Taksit açık · uzun tutar (`1.250.000,50 ₺`) · uzun not · **kategori salt okunur gösterge** (REV2: seçim arayüzü ve sabit ödeme bölümü yok) |
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
| E-27 | var (**ay yeni başladı** → 176 disk + `0 ₺`, denklem 0'larla dürüst) · var (**bütçe yok** → `HeroPlain` + tek birincil düğme) | var | `ErrorState` kartı; **ay okları kendi satırında kalır** (başka aya geçilebilsin) | "Hesaplanıyor" + çukur bloklar | **`overflow` (bütçe dışı)** → ana yay çizilmez, yalnız taşma yayı · kapanmış ay ("· ay kapandı") · hareket listesi 5 satır + "Tüm hareketler" · `SavingsSheet` `create`/`edit` |
| E-28 | var (`signed-out` kimlik paneli) | var | `IdentityPanel` `error` hâli — satırlar erişilebilir kalır | `skeleton` (panel + satırlar, düzen zıplamaz) | `FactStrip` olgu şeridi (`signed-in`) · 9 satırın tamamı `pressed` · hiçbir satır `disabled` değil |
| E-29 | var (hiç hareket yok) | var | okuma hatası E-27 deseni | var | Salt okunur: bu ekranda ekleme/düzenleme yok · uzun liste (`FlatList`) |

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
| E-01…E-03b (kurulum 1/4…4/4) | **Kısa nefes — ama dört ayrı ton** (REV2) | 1/4 ferah tek karar (üç kart, sayı yok) · 2/4 berrak hesap masası (çukur kuyular, tabular rakam) · 3/4 tezgah (liste + tek ikincil eylem, giriş sheet'te) · 4/4 sessiz kutlama (tek 56pt sayı + mavi kil panel). Ortak kabuk: `SetupShell`'in sabit adım göstergesi |
| E-21 Seri | **Çetele** | Tek büyük sayı + yatay durak rayı + 28 kutuluk sessiz ızgara. Kutlama hariç hareket yok; övgü değil **tespit** |
| E-22 · E-23 | **Eşik** | Duvar değil kapı: iki sağlayıcı düğmesi, kısa form, altta tam genişlikte "Hesapsız devam et". Ekranın vaadi tek cümlede ("Harcamaların sende kalır.") |
| E-24 Gün seçici | **Alet paneli** | Bilgi yoğun ay ızgarası + kelimeli lejant + üç satırlık özet. Boşlukla değil, ritimle ferahlar |
| E-25 Seni tanıyalım | **Sohbet temposu** | Kart başına tek soru, her kartta görünür "Bu kartı atla"; ilerleme tek oluk + `n/8`. Sigara/alkol kartları diğerlerinin birebir kopyası — yargı yok |
| E-26 Planın hazır | **Döküm** | Başarı ekranı değil hesap özeti: pay çubuğu, denklem satırı, "Nasıl hesaplandı". Konfeti, rozet, skor yok |
| E-27 Tasarruf (REV2) | **Kanıtlı hesap** | Tek kahraman gösterge → tek cümlelik anlam şeridi → denklem kartı (harcanabilir − harcanan = kalan) → hareketlerin kanıtı. Üç kavram (hesaplanan tasarruf · gerçek birikim · rutin tasarrufu) üç ayrı yüzeyde; hiçbir yerde toplanmaz |
| E-28 Profil (REV2) | **Kimlik + dizin** | Üstte tek kahraman kimlik paneli (içinde nötr olgu şeridi), altında 4 grupta 9 gezinme satırı; her satırın ikincil satırı **gerçek değeri** söyler, asla "…" göstermez. Ekranda birincil buton yok |
| E-29 Tüm hareketler (REV2) | **Dökümün arkası** | Tek işi olan sessiz liste: başlık + gün kutulu satırlar. Özet, grafik ve ekleme çağrısı yok — ekleme kendi sheet'inde kalır |

---

## 7. Faz 1'de OLMAYAN ekranlar (bilinçli)

Filtre paneli · pasta/çizgi grafik · bildirim merkezi ·
veri dışa aktarma · yedekleme/senkron · karanlık mod anahtarı ·
**başarım/rozet/puan** · paylaşım ("Başarını paylaş") · arkadaşlar ·
Pro/paywall · fiş fotoğrafı · banka bağlama.

> **REV2 düzeltmesi:** bu liste "profil ekranı"nı da sayıyordu; **E-28
> Profil artık bir sekmedir** ve üretildi. Kalanlar hâlâ kapsam dışıdır.

Bunlar çizilmez; talep gelirse PM'e sorulur.

> **v4 düzeltmesi (K-050 · K-048 · K-052):** bu liste "arama", "takvim
> ızgarası" ve "hesap/giriş"i de sayıyordu. Üçü de sonradan **MVP'ye
> alındı** ve üretildi: ürün arama (E-11 içinde), gün seçici (E-24) ve
> oturum açma / hesap oluşturma (E-22 · E-23). Liste gerçekle
> hizalandı; **rozet/puan/paylaşım hâlâ kapsam dışıdır** — seri bir
> sayaçtır, ödül ekonomisi değil.
