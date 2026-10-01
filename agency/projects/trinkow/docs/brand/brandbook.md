# Brandbook — Trinkow · **TASLAK (v2.0)**

> **Durum: TASLAK — ONAY BEKLİYOR.** v1.0 (Yön A "Defter") Mustafa
> tarafından **reddedildi** (2026-09-11): *"Tasarımlar fazla amatör
> geldi… ruhsuz bir UI/UX istemiyorum"*, *"bizim renk çok katı, farklı
> bir renk seçelim, piyasaya uygun olsun."*
>
> Bu doküman bir rötuş değil, **yön değişikliğidir.** Hiçbir maddesi
> Mustafa onaylamadan bağlayıcı değildir. Onay `projects/trinkow/status/DECISIONS.md`
> üzerinden verilir (CLAUDE.md → onay gerektiren işlemler).
>
> **Önerilen yön: Yön C — "Gün Işığı".** Alternatif: Yön D — "Gece
> Sayacı" (§3.D, §4.D). Reddedilen v1.0 yönleri (A "Defter",
> B "Ölçüm Aleti") **Bölüm 9'da ARŞİV** olarak duruyor, silinmedi.
>
> Kaynaklar: `projects/trinkow/docs/CONTEXT.md` · `projects/trinkow/docs/design/referans-analizi.md` +
> `projects/trinkow/docs/design/referans-gorseller/` (görseller açılıp incelendi) ·
> `reference/rn-tasarim-kisitlari.md` ·
> `reference/jenerik-ai-ui-anti-pattern-listesi.md`
> Tarih: 2026-09-11 · **Revizyon: 2026-09-17** (K-048 · K-052 · K-057 —
> bkz. dosya sonu "Revizyon notu") · Hazırlayan: `brand-strategist`

---

## 0. Bu dokümanın nasıl okunacağı

| Etiket | Anlamı | Uygulanır mı? |
|---|---|---|
| (etiketsiz gövde) | **Yön C — "Gün Işığı"**, Faz 1 | Onaylanırsa **bağlayıcı** |
| **ALTERNATİF — Yön D** (§3.D, §4.D) | İkinci palet/tipografi yönü | Mustafa D'yi seçerse gövde D'ye göre yeniden yazılır |
| **FAZ 2** (§3.8) | Karanlık mod hazırlığı | Faz 1'de **hayır** |
| **ARŞİV** (Bölüm 9) | Reddedilen v1.0 Yön A ve Yön B | **Hayır.** Yalnızca kayıt. |

**Makine okunur özet:** `projects/trinkow/docs/brand/tokens.md` (Yön C değerleriyle
güncellendi). Çelişirse **bu dosya esastır**, `tokens.md` düzeltilir.

**v1.0'dan v2.0'a ne değişti — tek bakışta:**

| Konu | v1.0 (reddedildi) | v2.0 (bu doküman) |
|---|---|---|
| Kahraman öğe | Düz yatay çubuk | **Dairesel yay + topuz + çok büyük sayı** |
| Palet | Petrol `#14484C` + kağıt `#F4F1EA` | **Mandalina `#D9661A`** + ışık `#F6F4F1` + mürekkep `#17181C` |
| Kategori | Renk taşımaz | **Her kategori kendi rengini taşır** (6 renk + pastel tint) |
| Gölge | Yasak | **İki seviyeli, amaçlı** (iOS + Android ayrı tarif) |
| Gradyan | Yasak | **3 yerde serbest** (yay, grafik dolgusu, hero ambiyansı) |
| Radius | 12 / hap | **16 / 24 / 28 / hap / daire** |
| Tipografi | Source Serif 4 + Public Sans (serif) | **Space Grotesk + Figtree** (geometrik sans) |
| Birincil buton | Petrol dikdörtgen-yuvarlak | **Mürekkep hap (pill)** |
| Fotoğraf/illüstrasyon | Yasak | **Markaya özel geometrik illüstrasyon serbest** |
| Emoji · utandırmayan ton · WCAG AA | Yasak / zorunlu | **Aynen korunuyor** |

---

# BÖLÜM 1 — KONUMLANDIRMA

## 1.1 Marka ne yapıyor, kim için, neden farklı?

**Trinkow**, insanın **günlük parasının nereye gittiğini fark etmesini**
sağlayan bir mobil takip aracıdır. Kullanıcı günlük bir harcama limiti
koyar, her harcamayı elle girer, kalan limiti **tek bir dairesel
göstergede** anlık görür. Amaç muhasebe değil **davranış**: dijital
ödemenin köreltmesi "ödeme acısı"nı, harcamayı elle yazma anında geri
getirmek.

v1.0'da marka "sakin bir defter" olarak konumlandı. Bu konumlandırma
mantıklıydı ama **bir ürün kişiliği değil, bir kâğıt parçası** üretti:
ölçülü, doğru, cansız. v2.0'ın konumlandırması aynı işi yapan farklı
bir nesne üzerinden kurulur:

> **Trinkow bir defter değil, günlük bir gösterge.**
> Sabah bakılır, gün içinde iki kere kontrol edilir, akşam kapanır.
> Kalori uygulamasının yaptığı işi para için yapar.

Bu, ürünün kendi tanımıyla (`projects/trinkow/docs/CONTEXT.md`: "harcamaları kalori sayar
gibi takip ettiren") birebir örtüşür ve markanın enerjisini nereden
alacağını söyler: **canlı bir sayı, dolan bir yay, günün ritmi.**

Markanın tek cümlelik gerilimi değişmedi:

> **Ciddi ama ezici değil. Basit ama çocukça değil. Farkındalık veren
> ama suçlamayan.**

Değişen şey, bu gerilimin **hangi uçtan** çözüldüğü. v1.0 "ezici değil"i
sessizlikle çözdü ve cansızlaştı. v2.0 aynı dengeyi **sıcaklıkla**
çözer: renk, derinlik ve büyük sayı ile canlı; ton ve metinle yargısız.

**Marka vaadi (iç kullanım, slogan değil):**
"Yargılamadan sayar. Kararı sen verirsin."

## 1.2 Hedef kitle (davranışsal tanım — değişmedi)

| Kim | Gözlenen davranış | Markadan beklentisi |
|---|---|---|
| **Farkında ama kör** | Kira/faturayı bilir; günlük 200-400 ₺'nin nereye gittiğini bilmez. Temassız ödemeye tam geçmiş. | "Bana kızmadan göster." |
| **Denemiş, bırakmış** | Bütçe uygulaması kurmuş, kategori tablolarında boğulup 3 günde bırakmış. | "Bu sefer 10 saniyede bitsin." |
| **Suçluluk hassasiyeti yüksek** | Para konusunda kendini kötü hissetmeye programlı; kırmızı uyarı görünce uygulamayı açmayı bırakır. | "Beni kötü hissettirme, yoksa silerim." |

Üçüncü satır markanın en sert kısıtıdır: **kullanıcı kaybı kötü
tasarımdan değil, kötü tondan gelir.** Bu yüzden §3.4'te limit aşımı
rengi kırmızı **değildir** ve §2.3'teki cümle kütüphanesi bağlayıcıdır.

Dördüncü, v2.0'da eklenen gözlem: bu kitle günde 8-10 uygulama açıyor ve
hepsi 2020 sonrası mobil estetiğe göre çizilmiş. **Görsel olarak
"eski/amatör" duran bir araç, tonu ne kadar doğru olursa olsun ikinci
haftaya kalmıyor.** Estetik burada süs değil, **elde tutma (retention)
koşuludur.** v1.0'ın reddedilme sebebi tam olarak budur.

**Üç niyet kipi** (üründen gelir): Sadece Takip · Tasarruf/Yatırım ·
Borç Kapatma. Marka kuralı §2.4.

## 1.3 Rakip haritası — ne yapıyorlar, görsel olarak neredeler, biz neredeyiz

| Marka | Ne yapıyor | Görsel konumu | Biz |
|---|---|---|---|
| **YNAB** | Zarf usulü katı bütçe metodolojisi (~$99/yıl) | Mavi-mor ("blurple") ana renk, illüstratif, neşeli; ama öğretmen pozisyonunda — sana bir *yöntem* öğretiyor. | Yöntem öğretmiyoruz. Ekranda tek bir sayı var, o da senin. Mavi-mor bizde yok. |
| **Copilot Money** | ABD'de banka bağlantılı otomatik takip | Yüksek zanaat, iOS-yerli his, **renkli kategori sistemi** güçlü; ama pasif — güzel bir rapor gösterir, davranışı değiştirmez. | Kategori renk sistemini **alıyoruz** (§3.3), pasifliği almıyoruz: kahraman öğe rapor değil, harcamadan önce bakılan gösterge. |
| **Monarch Money** | Aile/çift bütçesi, varlık takibi | Koyu yeşil + krem, olgun, "finansal kontrol paneli". Kurulum ağır, ritim haftalık/aylık. | Ritmimiz **günlük ve saniyelik**. Kontrol paneli değil, hızlı kayıt aracı. |
| **Monzo / Revolut** | Neo-banka | Monzo: sıcak mercan, cesur, insani. Revolut: siyah + mor-mavi degrade, "premium finans". | Monzo, **sıcak rengin finansta çalıştığının kanıtı** — biz de sıcak bir çekirdek renk alıyoruz. Revolut'un premium-kurumsal mesafesini almıyoruz. |
| **Headspace** (finans dışı, en yakın ruh eşi) | Günlük alışkanlık + yargısız ton | Sıcak turuncu, yumuşak geometri, büyük sayı/sayaç, karakterli ama çocuksu değil. | En yakın referansımız bir finans markası değil, bir **alışkanlık markası**. "Kalori sayar gibi" metaforu bizi oraya koyuyor. |
| **Türkiye bankaları/fintech'leri** (Papara, Tosla, ininal, Enpara, Garanti BBVA, İş Bankası, Akbank, QNB, Getir Finans) | Ödeme/banka/yatırım | Yüksek doygunluklu kurumsal renkler, kampanya dili, sık bildirim, "bir kurumla konuşuyorsun" hissi. | **Kurum gibi görünmüyoruz.** Harcama kaydı kullanıcının telefonunda durur, bizim panelimizde değil; hesap yalnız **kimlik** içindir ve **zorunlu değildir** (K-052). Görsel dil kurumsal değil **kişisel**: bu senin göstergen, bizim müşteri panelimiz değil. |

## 1.4 Rakip **renk** haritası (Mustafa'nın istediği ayrışma analizi)

> HEX değerleri **gözlemsel/yaklaşıktır** — rakiplerin resmi marka
> kılavuzlarından değil, kamuya açık arayüzlerinden okunmuştur. Amaç
> pikselde doğruluk değil, **hangi renk ailesinin dolu olduğunu**
> görmek.

| Aile | Kim kullanıyor | Yaklaşık ton | Doluluk |
|---|---|---|---|
| **Lacivert / kurumsal mavi** | İş Bankası, Yapı Kredi, Halkbank, Garanti BBVA, YNAB | `#0A2C6B` – `#1464A5` | **Tıka basa dolu.** "Banka" demenin varsayılan yolu. |
| **Mor / menekşe** | Papara, QNB, Getir Finans, Cleo, Emma, YNAB aksanı | `#5B2BD9` – `#7B2C8F` | **Dolu ve hızla doluyor.** Ayrıca "jenerik AI/SaaS" imzası (anti-pattern §1). |
| **Kırmızı** | Akbank, Ziraat, Vakıfbank | `#E3001B` – `#B0121A` | Dolu **ve bizim için yasaklı bölge**: kırmızı bizde yalnızca silme onayı (§3.4). |
| **Turkuaz / camgöbeği** | Enpara, N26, Garanti aksanı | `#00B7BD` – `#36A18B` | Dolu. **v1.0'ın petrolü de buraya düşüyordu** — Mustafa'nın "çok katı" dediği ton. |
| **Koyu yeşil** | Monarch, Rocket Money | `#0B3B36` – `#12513F` | ABD bütçe uygulamalarının varsayılanı. Ayrıca "yeşil = kâr/başarı" kodlaması riski. |
| **Magenta / fuşya** | Tosla | `#E6007E` civarı | Kısmen dolu, TR'de tanınır. |
| **Siyah + neon** | Revolut, Copilot, borsa/trading uygulamaları | `#000` + canlı aksan | Dolu; ayrıca "yatırım/trading" çağrışımı yapıyor — biz yatırım ürünü değiliz. |
| **Sıcak amber / mandalina / mercan** | TR'de neredeyse **boş** (yalnız ininal turuncusu — ön ödemeli kart kategorisi, düşük görünürlük, dönemsel olarak eski). Küreselde yalnız Monzo mercanı. | `#D9661A` – `#FF4F40` | **BOŞ ALAN.** |

**Ayrışma tezi:** Kişisel finansta sıcak amber/mandalina ailesi hem
Türkiye'de hem küreselde neredeyse sahipsiz. Üstelik bu aile markanın
işine üç yönden yarıyor:

1. **"Kurum değil" der.** Sıcak turuncu bir banka rengi değildir; ilk
   bakışta "bu bir uygulama, bir kurum değil" kodlar (§1.3).
2. **Günün rengidir.** Ürün günlük bir ritim aracı; ışık/gün metaforu
   sıcak amberde doğal, lacivertte zorlama olur.
3. **Yargısız kalabilir.** Bu markada uyarı rengi olarak sarı-turuncu
   **kullanılmayacağı** için (trafik ışığı reddedildi, §3.7), amber
   "dikkat" anlamına düşmez; her doluluk oranında aynı renktir,
   dolayısıyla hiçbir zaman "kötü haber" kodlamaz.

**Neden referanstaki mor/lavantayı kopyalamıyoruz:** o bir Dribbble
sunum estetiği (ambiyans gradyanı + cam efekti), ürün kararı değil.
Kopyalarsak (a) Papara/QNB/Cleo ile aynı aileye düşeriz, (b) anti-pattern
listesinin 1. maddesine (mor-mavi varsayılan) çarparız, (c) "bir başka
mor SaaS" oluruz. Referanstan aldığımız şey **renk değil, tasarım
dilidir**: dairesel kahraman gösterge, derinlik, kategori başına renk,
yumuşak geometri, büyük sayı + sessiz etiket.

---

# BÖLÜM 2 — MARKA KİŞİLİĞİ

## 2.1 Kişilik sıfatları (4 sıfat — her biri somut bir kurala bağlanır)

| Sıfat | Ne demek | Bağlandığı somut kural |
|---|---|---|
| **Sıcak** | Yüzey insani; ekran soğuk bir tablo değil. Bu, v1.0'ın kaybettiği sıfattır. | Nötrler sıcak (`#F6F4F1`, saf beyaz/gri değil) · çekirdek renk Mandalina (§3.2) · radius 24 · hap butonlar · gölge rengi **sıcak mürekkep**, siyah değil (§6.2) |
| **Odaklı** | Ekranda gözün gideceği **tek** yer vardır. | Ekran başına **bir** kahraman gösterge (§7.5) · ekran başına **bir** birincil buton · kahraman sayı 56pt, yanındaki etiket 13pt (§4.2) |
| **Net** | Sayıyı olduğu gibi verir; yumuşatmaz, süslemez, açıklamaya boğmaz. | Önce rakam, sonra (varsa) cümle (§2.2) · tabular rakam (§4.4) · arayüz cümlesi ≤ 12 kelime · **UI'da teknik açıklama yasak** (§2.8) |
| **Yargısız** | Ne suçlar ne över. Övgü de bir yargıdır; tersi suçlamadır. | Limit dışı rengi **Mürdüm**, kırmızı değil (§3.4) · trafik ışığı yok (§3.7) · ünlem yasak · övgü yasak (§2.2) |

**Marka insan olsaydı:** para konusunu abartmadan konuşan, sen
anlatırken yüzünü buruşturmayan, "peki, ne kadar oldu?" diye sorup
cevabı duyduğunda tepki vermeyen biri — ama **sıkıcı değil**: bugünün
sayısını söylerken gözünü kırpmadan da olsa canlı bir sesi var.

**Marka ASLA olmayacağı şeyler:** neşeli maskot, motivasyon konuşmacısı,
kampanya duyurucusu, öğretmen, arkadaş canlısı chatbot, borsa terminali.

> **"Sakin" ile "cansız" farkı (bu markanın en kritik ayrımı):**
> Sakin = aciliyet üretmez, kovalamaz, bağırmaz. Cansız = renk yok,
> derinlik yok, hiyerarşi yok, ekranda hiçbir şey öne çıkmıyor.
> v1.0 ikisini karıştırdı. **v2.0'da sakinlik tondan, canlılık
> renk-derinlik-ölçekten gelir.** Bu iki kaynak birbirine karıştırılamaz:
> ton asla yükselmez, görsel asla sönmez.

## 2.2 Ton of voice — bağlayıcı yazım kuralları

1. **Hitap: "sen".** Kişisel günlük araç; "siz" kurumsal mesafe yaratır.
   Laubali değil: argo, şaka, "hadi bakalım" yok.
2. **Önce sayı, sonra (gerekiyorsa) cümle.** Sayı zaten mesajdır.
3. **Ünlem işareti (!) kullanılmaz.** Hiçbir yüzeyde — aciliyet ve azar
   tonunun tek kaynağı odur. (Sıcaklık ünlemle değil, kelime seçimiyle
   verilir.)
4. **EMOJİ KULLANILMAZ** (§2.6 — kesin kural).
5. **Fiil nötr olur.** "aştın", "harcadın", "yazdın" serbest;
   "abarttın", "kaçırdın", "batırdın" yasak.
6. **Övgü yok.** "Harikasın", "Süpersin", "Bravo" yasak — övgü
   şartlanma yaratır, övgünün olmadığı gün kullanıcı cezalandırılmış
   hisseder. Yerine **nötr tespit**.
7. **Buton etiketi: 1-3 kelime, fiil önce.** "Harcama ekle", "Kaydet",
   "Limiti değiştir". "Hadi başlayalım", "Devam et ve keşfet" yasak.
8. **Pazarlama dili yasak.** "Finansal özgürlüğüne kavuş", "Paranı
   yönetmenin en akıllı yolu" bu markada kullanılmaz.
9. **Belirsizlik itiraf edilir.** "Tahmini" olan yerde "tahmini" yazar.
10. **Arayüz cümlesi en fazla 12 kelime.** Uzunsa ikiye böl veya sil.
11. **Teknik açıklama yasak** (§2.8 — v2.0'da eklendi). **Tek istisna
    §2.8.1:** mahremiyet, *kullanıcı faydası dili* ile ve yalnızca orada
    sayılan yüzeylerde söylenebilir; mimari sözcükleri her yerde yasak.

## 2.3 "Şöyle deriz / şöyle demeyiz" — gerçek cümleler

Bunlar örnek değil **kütüphanedir**; `ui-ux-designer` ve `social-media`
ajanı metni buradan üretir.

### Limit aşımı (markanın en kritik anı)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Günlük limitin doldu. Bugün 412 ₺." | "Dikkat! Limitini aştın!" |
| "Limitin 60 ₺ üzerindesin." | "Yine fazla harcadın." |
| "Bugün limit dışı 3 harcama var." | "Bütçen tehlikede!" |
| "Bu ay 6. limit aşımı. Limit gerçekçi mi?" | "Kendini tutamıyorsun." |

Son satır markanın imzasıdır: suçu kullanıcıya değil **kuruluma** atar.
Limit ısrarla aşılıyorsa hatalı olan kullanıcı değil, limittir.

### Limit altında kalma (övgü tuzağı)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Bugün 180 ₺. Limitinin 120 ₺ altında." | "Harikasın! Bugün çok tasarruflusun" |
| "Bu hafta 4 gün limit altında." | "Muhteşem gidiyorsun, böyle devam" |

### Gün başı / gün sonu (v2.0'da eklendi — sıcaklık buradan gelir)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Günaydın. Bugünün limiti 340 ₺." | "Günaydın şampiyon" |
| "Gün kapandı. Bugün 6 kayıt, 290 ₺." | "Harika bir gün geçirdin" |
| "Bugün henüz kayıt yok." | "Neredesin, seni özledik" |

> Sıcaklık **selamlamadan** gelir, sıfattan değil. "Günaydın" sıcaktır;
> "şampiyon" yargıdır.

### Boş durum (ilk gün, hiç veri yok)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Bugün henüz bir şey yazmadın. İlk kahve iyi bir başlangıç." | "Henüz veri yok" |
| "Kayıt yok. Aşağıdaki butonla ilkini ekle." | "Buralar çok boş görünüyor" |

### Onboarding (en fazla 3 soru, adım göstergeli)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Adım 1/3 — Neden buradasın?" | "Hadi seni tanıyalım" |
| "Param nereye gidiyor" / "Bütçe yaratmak" / "Borç kapatmak" | "🚀 Yatırım İçin Bütçe Yaratmak" (rapordaki emoji'li örnek **geçersiz**) |
| "Sonra değiştirebilirsin." | "Merak etme, çok kısa sürecek" |

### Bildirim (günde en fazla 1, akşam)
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Bugün 3 harcama, 210 ₺. Kalan 130 ₺." | "Bugün harcamalarını girmeyi unuttun" |
| "Dün hiç kayıt yok. 20 saniyede tamamlayabilirsin." | "Seni özledik" |

### Hata ve onay
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Tutar boş kalamaz." | "Hata! Geçersiz giriş" |
| "Şu an açılamadı. Tekrar dene." | "Veriler bu cihazda tutuluyor ve şu an okunamadı" (§2.8) |
| "Bu harcama silinecek. Geri alınamaz." · Butonlar: "Sil" / "Vazgeç" | "Emin misin? Bu işlem geri alınamaz!" |

### Borç kapatma kipi
| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "Kalan borç 12.400 ₺. Bu ay 900 ₺ azaldı." | "Borç canavarını yeniyorsun" |
| "Bu hızla tahmini bitiş: Mart 2027." | "Özgürlüğüne 14 ay kaldı" |

### Seri (streak) ve milestone — **MVP'DE** (K-048, 2026-09-17)

> v2.0'da bu blok "FAZ 2 — Faz 1'de üretilmez" etiketliydi. **K-048 ile
> seri + milestone MVP kapsamına alındı**; etiket geçersizdir. Önden
> kilitlenen iki ton satırı aynen geçerli, aşağıda MVP'nin gerçekten
> ihtiyaç duyduğu yüzeylerle genişletildi.

| ✅ Deriz | ❌ Demeyiz |
|---|---|
| "12 gündür kayıt giriyorsun." | "12 günlük serin var, kaybetme!" |
| "Seri dün kırıldı. Bugün yeniden başlıyor." | "Serini kaybettin" |
| "En uzun serin 21 gün." | "Rekorunu kırmaya çalış" |
| "Bugün limit altında kapandı. Seri 13 gün." | "Bir gün daha kazandın" |
| "3 gün." · "7 gün. En uzun serin bu." (milestone) | "Tebrikler! 7 günlük seriye ulaştın" |
| "Harcamasız gün olarak işaretlendi." | "Bugünü boş geçirdin" |
| "Seri için günlük limit gerekir." · "Limit belirle" | "Seri kazanmak istemez misin?" |

**Seri dilinin dört kuralı (bağlayıcı):**

1. **Çerçeve "farkındalık"tır, "disiplin/ceza" değil.** Seri bir ödül
   ekonomisi değil, kayıt alışkanlığının görünür hâlidir. Yasak fiiller:
   "kazandın", "hak ettin", "kaybettin", "ıskaladın", "cezası".
   Seri bir **sayaçtır**, bir puan değildir.
2. **Kutlama abartısız.** Milestone metni **en fazla iki kısa cümle**,
   ilki sayı (§2.2/2). Ünlem yok (§2.2/3), emoji yok (§2.6), konfeti ve
   zıplama yok (§6.6). Kutlama ≤1.2 sn ve dokunmayla atlanabilir
   (K-048) → metin de tek okumada bitmek zorundadır.
3. **Kırılma suçlamaz, dramatize etmez, ikna etmez.** Seri kırılınca
   ekranda yalnızca olgu + yeniden başlangıç durur. "Yazık", "ne oldu",
   "yeniden denesek mi" yasak. Kırılma **ayrı bir uyarı yüzeyi**
   (modal, alarm, tam ekran) üretmez — en fazla mevcut seri yüzeyinde
   satır değişir. "En uzun seri" her zaman görünür kalır; kırılmanın
   yıkıcı okunmamasının tek sebebi budur.
4. **Seri kullanıcıyı kovalamaz.** "Günde en fazla 1 bildirim, akşam"
   kuralı seriyi de kapsar; "serin bugün bitiyor" tipi aciliyet
   bildirimi gönderilmez. Seri bir son tarih değildir.

**Puan · seviye · rozet · lig neden kalıcı olarak kapsam dışı (K-048):**
Bu markanın tek motivasyon kaynağı kullanıcının **kendi parasıdır**;
harcamayı elle yazmanın ürettiği farkındalık zaten gerçek bir geri
bildirimdir. Araya bir puan ekonomisi girdiği anda ölçü değişir:
kullanıcı ne harcadığını değil kaç puan topladığını takip etmeye başlar
ve para davranışı hiç iyileşmeden "iyi gidiyorum" hissi üretilir — yani
**sahte motivasyon**. Üstelik puan/seviye/rozet dili kaçınılmaz olarak
övgü üretir, övgü de bir yargıdır (§2.2/6): rozetin gelmediği gün
kullanıcı cezalandırılmış hisseder ve bu kitle uygulamayı tam o noktada
siler (§1.2, 3. satır). Seri ve milestone bu riski taşımaz, çünkü ikisi
de **icat edilmiş bir birim değil, gerçek gün sayısıdır** — kullanıcının
kendi davranışını sayarlar, onun yerine bir skor uydurmazlar. Bu yüzden
sayaç kalır, ekonomi gelmez.

## 2.4 Üç niyet kipini marka nasıl taşır? (bağlayıcı)

Kip değişince **palet, tipografi ve düzen DEĞİŞMEZ.** Üç ayrı tema
yapılmaz.

Kipe göre değişen **yalnızca üç şey**:
1. **Kahraman sayı** (dairesel göstergenin ortasındaki 56pt rakam):
   Sadece Takip → *bugün kalan limit* · Tasarruf → *bu ay biriken tutar*
   · Borç → *kalan borç*
2. **Göstergenin altındaki tek satırlık ikincil metin** (§2.3'ten).
3. **Kip etiketi**: başlık yanında küçük bir pill (metin, ikon değil):
   "Takip" · "Tasarruf" · "Borç".

Kip adı arayüzde **"Borç Avcısı Modu" gibi dramatik biçimde geçmez**;
kullanıcıya görünen etiket sadedir ("Borç"). Gerekçe: §2.1 *Yargısız* —
avcı/savaş metaforu suçlayıcı çerçeve üretir.

## 2.5 Para ve sayı yazım kuralları (tüm yüzeyler)

- Biçim: `1.250,50 ₺` — binlik nokta, kuruş virgül, simge **sonda**,
  araya tek boşluk.
- Kuruş: liste ve kahraman sayıda **gösterilmez** (`1.250 ₺`); yalnızca
  giriş ekranında ve detay görünümünde gösterilir. Gerekçe: kahraman
  sayının okunma hızı.
- Negatif/aşım: eksi işareti değil **"limit dışı"** etiketi.
  `-60 ₺` yerine `60 ₺ limit dışı`.
- "TL" yazılmaz, `₺` kullanılır. Tutar ile simge arasında satır sonu
  olmaz.
- Rakamlar **daima tabular** (§4.4).

## 2.6 EMOJİ YASAĞI (kesin kural — Mustafa, değişmedi)

**Uygulamanın hiçbir yerinde emoji kullanılmaz.** Buton etiketi, başlık,
onboarding seçeneği, boş durum, bildirim, hata mesajı, kategori adı,
App Store açıklaması, sosyal medya gönderisi — hiçbiri.

Gerekçe: emoji her işletim sisteminde farklı render edilir; markanın
çizgi kalınlığını ve rengini taşımaz; "neşeli uygulama" kodlaması yapar.
Ayırt edicilik gereken yerde **tek ikon seti** kullanılır (§6.5).
v2.0'da kategoriler artık **renk de** taşıyor (§3.3) — ayırt edicilik
ihtiyacı emoji olmadan fazlasıyla karşılanıyor.

## 2.7 Marka adının yazımı — **Trinkow** (değişmedi)

> ### `Trinkow`
> Büyük **T**, kalan altı harf küçük. Başka varyant geçerli değildir.

| ✅ Doğru | ❌ Yanlış | Neden |
|---|---|---|
| Trinkow | TRINKOW / TRİNKOW | Büyük harf bağırma tonu taşır; Türkçe `I/İ` dönüşümü platformlar arası bozulur. |
| Trinkow | trinkow | Özel ad olduğu belirsizleşir. |
| Trinkow | TrinKow / Trin Kow | Tek kelime, tek büyük harf. |
| Trinkow | Trinkow App / Trinkow Uygulaması | Ad kendi başına yeter. |
| Trinkow | Trinkow™ / Trinkow® | Tescil yok; kurumsal ton üretir. |

**Okunuşu:** "trin-kov", vurgu ilk hecede. **Çekim ekleri daima kesme
işaretiyle:** Trinkow'u · Trinkow'a · Trinkow'da · Trinkow'dan ·
Trinkow'un. Çoğul kullanılmaz. İngilizce'de de `Trinkow`, iyelik
`Trinkow's`.

Ad, gövde metni içinde geçtiğinde **o metnin fontu ve ağırlığıyla**
yazılır; cümle ortasında wordmark kullanılmaz. Ada renk verilmez.

## 2.8 UI'DA TEKNİK AÇIKLAMA YASAĞI (v2.0'da eklendi — Mustafa kararı)

> *"kullanıcı verinin nereye kaydedildiği hakkında niye bir bilgi
> edinmek istesin, UI'da açıklama koymak için hiçbir teknik açıklama
> girilmesin."*

**Kural:** Kullanıcıya depolama, mimari, senkronizasyon, veri tabanı,
sunucu, şifreleme veya "nasıl çalıştığı" anlatılmaz. Uygulamanın iç
işleyişi kullanıcının sorunu değildir.

| ❌ Yasak (metinlerden temizlenecek) | ✅ Yerine |
|---|---|
| "Kayıtların yalnızca bu cihazda. Hesap yok, sunucu yok." | "Harcamaların telefonunda kalır." (§2.8.1 — "hesap yok" **artık yanlış**, K-052) |
| "Cevabın cihazda kalır." | (satır tamamen kaldırılır — burada mahremiyet bir fayda değil, dolgu) |
| "Veriler bu cihazda tutuluyor ve şu an okunamadı." | "Şu an açılamadı. Tekrar dene." |
| "Teknik detay bunun altında saklanır" | (kaldırılır) |

**Hata mesajı ne olduğunu değil, ne yapacağını söyler.** Tek istisna:
App Store gizlilik beyanı ve ayarlar içindeki yasal metin — bunlar
arayüz metni değil, zorunlu yasal yüzeydir.

### 2.8.1 İSTİSNA — mahremiyet, kullanıcı faydası dili ile söylenebilir

> **Karar dayanağı: K-057/1 (2026-09-17).** K-052 ile Google/Apple
> oturumu geldi. Kullanıcı artık hesap açıp açmama kararını verirken
> "harcamalarım nereye gidiyor?" sorusunu **haklı olarak** soruyor.
> Bu soruya cevap vermemek §2.8'in amacı değildi: yasak, kullanıcıyı
> ilgilendirmeyen **mimariyi** anlatmaya karşıydı.

**Kural iki parçalıdır ve ikisi birlikte uygulanır:**

- ✅ **İZİNLİ — kullanıcı faydası dili.** Kullanıcının kendi verisiyle
  ne olduğunu, *onun* cümleleriyle söylemek. Ölçüt: cümle, kullanıcının
  bir kararını (hesap açayım mı?) doğrudan bilgilendiriyor mu?
- ❌ **YASAK — mimari sözcükleri.** Şu sözcükler hiçbir arayüz
  yüzeyinde geçmez: **SQLite · veri tabanı · sunucu · backend ·
  senkron/senkronizasyon · şifreleme · token · API · uç nokta ·
  bulut · Supabase · JWT · yerel depolama · önbellek.**

| ✅ İzinli (kullanıcı faydası) | ❌ Yasak (mimari) |
|---|---|
| "Harcamaların telefonunda kalır." | "Harcamalar yerel SQLite veri tabanında tutulur." |
| "Hesap açmak zorunlu değil." | "Auth katmanı opsiyoneldir." |
| "Oturum açsan da harcamaların gönderilmez." | "Harcama tablosu sunucuya senkronlanmaz." |
| "Hesap, seni tanımak için." | "Hesap yalnız kimlik token'ı üretir." |
| "Telefon değiştirirsen kayıtlar şimdilik taşınmaz." | "Bulut yedekleme Faz 3'te gelecek." |
| "Google ya da Apple hesabınla oturum açabilirsin." | "OAuth sağlayıcı ile kimlik doğrulanır." |

**Üç ek sınır:**

1. **Doğrulanamaz iddia yasak.** "Askeri düzeyde şifreleme", "verini
   asla göremeyiz", "%100 gizli", "hiç kimse erişemez", "banka
   düzeyinde güvenlik" — bu markada kullanılmaz. Yazdığımız her cümle
   teknik olarak **doğrulanabilir** olmak zorundadır. Mahremiyet bir
   övünme değil, bir **olgu bildirimidir** (§2.1 *Net*).
2. **Abartı yok, korku yok.** Rakibin veriyi nereye gönderdiği,
   "verilerin satılıyor olabilir" gibi ima, tehdit dili yasak. Kendi
   olgumuzu söyleriz, karşılaştırma yapmayız (K-010/5).
3. **Yer sınırı.** Bu istisna yalnız şu yüzeylerde geçerlidir:
   oturum aç / hesap oluştur ekranı · "Hesapsız devam et" açıklaması ·
   Ayarlar → Hesap ve Veri bölümü · SSS/yardım · mağaza açıklaması ·
   pazarlama yüzeyleri. **Pano, harcama girişi, liste, hata mesajı,
   boş durum, bildirim** bu istisnanın dışındadır — orada §2.8 aynen
   geçerli.

**Sözcük kullanımı (K-057/6):** kimlik doğrulama için **"Oturum aç"**
denir; "giriş" sözcüğü yalnız veri girme anlamında kullanılır (harcama
girişi). Aynı sözcüğün iki anlamı bu ayrımla çözülür.

## 2.9 Mahremiyet cümlesi — üç sürüm (tek kaynak)

> Aynı olguyu her yüzeyde aynı uzunlukta söylemek zorunda değiliz; ama
> **üçünün de aynı şeyi** söylemesi zorunludur. Yeni bir sürüm
> türetilmez — ihtiyaç varsa buraya eklenir.
>
> **Vaadin özü (bir cümlede, iç kullanım):** *Harcama verisi cihazda
> kalır; hesap yalnız kimlik içindir ve hesap açmak zorunlu değildir.*

### Kısa — pazarlama, sosyal, mağaza alt başlığı, splash altı

> **"Harcamaların telefonunda kalır. Hesap açmak zorunlu değil."**

İki cümle, 8 kelime, §2.2/10 sınırının içinde. Tek cümle gerekiyorsa:
**"Harcamaların telefonunda kalır."** Bu, uygulamanın en kısa
mahremiyet ifadesidir ve kısaltılamaz — "telefonunda kalır" kısmı
düşerse iddia kalmaz, "harcamaların" düşerse iddia yanlış olur (çünkü
*kimlik* telefonda kalmıyor).

### Orta — mağaza açıklaması, oturum aç ekranı, ayarlar başlığı

> **"Harcama kayıtların telefonunda kalır. İstersen Google ya da Apple
> hesabınla oturum açabilirsin; bu yalnız seni tanımak için — harcamaların
> gönderilmez. Hesap açmadan da uygulamanın tamamını kullanırsın."**

Üç cümle, üç işi yapar: (1) olgu, (2) hesabın kapsamı, (3) hesabın
zorunlu olmadığı. **Sıra değiştirilemez** — kullanıcı önce neyin
paylaşılmadığını, sonra neyin paylaşıldığını öğrenir; tersi kaygı
üretir.

### Uzun — SSS / yardım (soru-cevap, her cevap ≤ 2 cümle)

| Soru | Cevap |
|---|---|
| "Harcamalarımı kimse görüyor mu?" | "Harcama kayıtların telefonunda kalır. Oturum açsan da açmasan da bu böyle." |
| "Oturum açmak zorunlu mu?" | "Hayır. 'Hesapsız devam et' ile uygulamanın tamamını kullanırsın." |
| "Oturum açarsam ne paylaşılıyor?" | "Yalnız kimliğin: Google ya da Apple'ın bize verdiği ad ve e-posta. Harcamaların gönderilmez." |
| "Neden hesap var o zaman?" | "Seni tanımak için. Kayıtlarını başka cihaza taşımak sonraki sürümlerde gelecek." |
| "Telefonumu değiştirsem kayıtlarım gelir mi?" | "Şimdilik gelmez. Yedekleme henüz yok." |
| "Hesabımı silebilir miyim?" | "Evet. Ayarlar → Hesap bölümünden silinir." |
| "Harcamalarımı silmek istersem?" | "Ayarlar → Veri bölümünden tüm kayıtlar silinir. Geri alınamaz." |

**Bu tablo için üç uyarı:**
- Cevaplar **mimari sözcüğü içermez** (§2.8.1). "Sunucuya gitmez" bile
  yazılmaz; "gönderilmez" yeterlidir ve daha anlaşılırdır.
- **"Yedekleme henüz yok"** dürüst ve gereklidir; "yakında" denmez
  (§2.2/9 belirsizlik itiraf edilir). Yedekleme Faz 3 (K-052).
- Bu tablo **gizlilik politikasının yerine geçmez.** Hukuki metin ayrı
  bir iş kalemidir (K-057/7) ve orada Supabase'in kimlik verisi
  işlediğini yazmak **zorunludur** — yasal yüzey §2.8'in istisnasıdır,
  orada teknik adlar geçebilir.

---

# BÖLÜM 3 — RENK PALETİ

## 3.0 İki yön, tek öneri

| | **Yön C — "Gün Işığı"** (ÖNERİLEN) | **Yön D — "Gece Sayacı"** (alternatif, §3.D) |
|---|---|---|
| Kavram | Gün ışığı alan sıcak bir yüzey; ekran bir *gösterge panosu* değil, *günün kendisi*. | Karanlık öncelikli tek tema; sayılar karanlıkta parlayan bir sayaç gibi. |
| Zemin | Işık `#F6F4F1` (sıcak, kirli beyaz) | Grafit `#0E1214` |
| Çekirdek renk | **Mandalina `#D9661A`** | **Nane `#4ADEA8`** |
| Kişilik | Sıcak · günlük · yaklaşılabilir | Odaklı · premium · araç gibi |
| Tipografi | Space Grotesk + Figtree | Manrope (tek aile) |
| **Artı** | Rakip renk haritasındaki **boş alanı** alır (§1.4) · referansın havadar/derinlikli dilini birebir taşır · pastel kategori sistemi açık zeminde doğal çalışır · gündüz dışarıda hızlı giriş için en okunur seçenek · Faz 2'de karanlık mod eklenebilir | TR pazarında hiçbir kişisel finans rakibi koyu değil → anında ayrışma · tek tema, Faz 2'de karanlık mod işi yok · büyük sayılar koyu zeminde daha "premium" · gece kullanımında göz yormaz |
| **Eksi** | Turuncu ailesi bazı gözlerde "uyarı" çağrışımı yapabilir (§3.2'de nötrleniyor) · açık zeminde amber metin olarak kullanılamaz, ayrı koyu varyant gerekir · Faz 2 karanlık modu ayrıca tasarlanmalı | Referansın açık/havadar ruhuyla çelişir — Mustafa'nın gösterdiği yön bu değil · koyu + finans = "borsa/trading" çağrışımı (biz yatırım ürünü değiliz) · pastel kategori tonları koyuda yeniden ayarlanmalı · güneş altında okunurluk düşer, ürün **gün içinde, dışarıda** kullanılıyor · fotoğraf/illüstrasyon koyuda zorlaşır |

**Öneri: Yön C.** Gerekçe tek cümlede: referans dili açık, havadar ve
derinlikli; rakip renk haritasında boş olan tek aile sıcak amber; ve
ürün **gün içinde, çoğunlukla dışarıda, hızlıca** açılıyor.

Aşağıdaki §3.1-3.8 **Yön C**'yi tam detayla tanımlar. Yön D'nin paleti
§3.D'dedir.

## 3.1 Nötr merdiven — Yön C

Nötrler **sıcak** ama v1.0'ın bej "kağıt" tonundan belirgin biçimde
**daha açık ve daha temiz**; amaç sayfa hissi değil **ışık** hissi.

| Token | HEX | Ad | Kullanım |
|---|---|---|---|
| `bg` | `#F6F4F1` | **Işık** | Tüm ekranların zemini. Tek zemin rengi. |
| `surface` | `#FFFCF8` | **Yüzey** | Kart, sheet, girdi zemini, sekme çubuğu. |
| `surface-2` | `#EFEAE3` | **Kum** | İkincil buton zemini, gösterge oluğu, pasif pill. |
| `line` | `#E6E1DA` | **Çizgi** | Hairline ayraç. **Dekoratiftir** — anlam taşımaz (§6.2). |
| `line-strong` | `#CFC9C0` | **Kenar** | Girdi kenarlığı (odaksız). |
| `text` | `#17181C` | **Mürekkep** | Başlık, tutar, birincil metin, birincil buton zemini. |
| `text-2` | `#5A5B63` | **Mürekkep 60** | İkincil metin, etiket, tarih, pasif ikon. |
| `text-3` | `#6B6C75` | **Mürekkep 45** | Placeholder, pasif metin. **Açıklık alt sınırı** — daha açık gri metin yasak. |
| `disabled-bg` | `#E7E1D8` | — | Pasif buton zemini. |
| `pressed-neutral` | `#E5DFD6` | — | İkincil/sessiz buton `pressed`. |
| `scrim` | `rgba(23, 24, 28, 0.45)` | — | Modal/sheet arkası. |

**Saf beyaz `#FFFFFF` ve saf siyah `#000000` kullanılmaz.** Gerekçe:
saf beyaz kart + saf gri zemin kombinasyonu, anti-pattern listesindeki
"kimliksiz SaaS şablonu" hissinin tam kaynağıdır; markanın sıcaklığı
nötrlerde başlar, aksan renginde değil.

## 3.2 Marka ve vurgu renkleri — Yön C

| Token | HEX | Ad | Kullanım kuralı |
|---|---|---|---|
| `accent` | `#D9661A` | **Mandalina** | Marka çekirdeği. Kahraman yay dolgusu, merkez eylem dairesi (FAB), aktif sekme, seçili durum, grafik dolgusu, ilerleme dolgusu. |
| `accent-deep` | `#A8500C` | **Mandalina Koyu** | Amber'in **metin/ikon varyantı** (bağlantı, tint üzerindeki tutar), yay gradyanının koyu ucu, `pressed`. |
| `accent-soft` | `#FDEBD8` | **Mandalina Tint** | Seçili pill, bilgi kutusu, hero kart ambiyansının sıcak ucu. Üzerine `text` ya da `accent-deep` yazılır. |
| `ink` | `#17181C` | **Mürekkep** | **Birincil buton zemini** ve en yüksek kontrastlı metin. (`text` ile aynı değer; rolü ayrı yazıldı.) |
| `ink-pressed` | `#2C2E34` | — | Birincil buton `pressed`, Android ripple. |

**Neden birincil buton amber değil mürekkep?** Amber üzerine beyaz metin
3.43:1 verir — AA'yı geçmez. Amber'i buton zemini yapmak ya metni
mürekkebe çevirmeyi (okunur ama zayıf çağrı) ya da kontrastı feda etmeyi
gerektirir. Referansın çözümü de aynı: **birincil eylem siyah hap,
marka rengi veriye ayrılmış.** Böylece amber hiçbir zaman "tıkla"
demez, hep "bu senin durumun" der — ve ekranda tek başına ayırt
edicidir.

**Amber neden "uyarı" olarak okunmaz?** Çünkü bu markada sarı-turuncu
bir uyarı seviyesi **yoktur** (§3.7: trafik ışığı reddedildi). Gösterge
%5 doluyken de %95 doluyken de aynı amber. Bir renk her durumda
görünüyorsa durum kodlayamaz.

## 3.3 Kategori renkleri — **v1.0'ın "renk taşımaz" kararı İPTAL**

Referansın canlılığının üç kaynağından biri: **her kategori kendi
yumuşak tonunu taşıyor.** v2.0'da bunu alıyoruz, ama denetimli:

**Faz 1 kategori paleti — 6 renk, sabit.**

| Kategori | `solid` (nokta, yay, grafik) | `soft` (pill/satır zemini) | `solid` kontrastı (`bg` üzerinde) |
|---|---|---|---|
| Kahve & atıştırma | `#7A5233` **Kahve** | `#F1E7DC` | **6.21:1** |
| Yemek | `#C2405A` **Nar** | `#FBE3E7` | **4.58:1** |
| Ulaşım | `#1F7A8C` **Deniz** | `#DDEEF1` | **4.53:1** |
| Market | `#4C7A34` **Zeytin** | `#E4EFDC` | **4.62:1** |
| Fatura & abonelik | `#2F4A8C` **Lacivert** | `#E2E7F5` | **7.72:1** |
| Diğer | `#5A5B63` **Kurşun** | `#EAEAED` | **6.15:1** |

**Bağlayıcı kurallar:**

1. **Renk asla tek başına bilgi taşımaz** (WCAG 1.4.1). Her kategori
   daima **renk + ikon + metin** üçlüsüyle görünür. Renk, tanımayı
   hızlandırır; anlamı yazı taşır.
2. **Kategori rengi metin rengi olarak kullanılmaz.** Tint zeminlerin
   üzerine daima `text #17181C` yazılır (en düşük oran **14.8:1**).
   Böylece 6 ayrı metin kontrastı doğrulamak gerekmez ve renk körlüğünde
   okunurluk garanti kalır.
3. **`solid` yalnızca**: 8pt nokta, kategori ikonu, kategori limit
   yayı/çubuğu dolgusu, grafik serisi. Hepsi ≥ 4.5:1 — metin dışı 3:1
   eşiğini rahatça geçer.
4. **7. renk üretilmez.** Yeni kategori gelirse rengi **bu tabloya
   kontrast oranıyla eklenir**, tasarımcı yerinde renk uydurmaz.
   (Anti-pattern: "her karta rastgele renk".)
5. Kategori renkleri **marka rengi değildir**: amber ailesi ve mürdüm
   ailesi kategori paletinde **yoktur** — o iki aile markaya ve duruma
   ayrılmıştır. Çakışma olmaz.

## 3.4 Durum renkleri

| Token | HEX | Ad | Kullanım |
|---|---|---|---|
| `edge` | `#6E3B6B` | **Mürdüm** | **Yalnızca limit dışı**: taşma yayı, limit dışı tutar, limit dışı satır vurgusu. Başka hiçbir yerde. |
| `edge-soft` | `#F0E4EF` | — | Limit dışı liste satırının zemini. Üzerine `text` veya `edge` (6.82:1). |
| `danger` | `#9B2C1F` | **Karar Kırmızısı** | **Yalnızca geri alınamaz yıkıcı işlem** (silme onayı, form hatası). Limit aşımında **kesinlikle kullanılmaz.** |
| `danger-on` | `#FFFCF8` | — | `danger` zemin üzerindeki metin (**7.40:1**). |

**Limit aşımı neden mor/mürdüm?** Bu, markanın en bilinçli renk
kararıdır. Kırmızı "hata" der, turuncu "dikkat" der, ikisi de
kullanıcıyı suçlar (§1.2, 3. satır: bu kitle kırmızı görünce uygulamayı
siliyor). Mürdüm **hiçbir yerleşik uyarı koduna ait değildir** — sakin,
koyu, ciddi ama alarm değil. Kullanıcının okuyacağı şey renkten değil
etiketten gelir: **"limit dışı"**. Renk sadece "burası çizginin öbür
tarafı" der.

Ayrıca mürdüm, amberin tam karşı sıcaklığındadır: ekranda ikisi
yan yana **anında ayrışır**, renk körlüğünde bile (protanopi/döteranopide
turuncu ↔ mor açıklık farkıyla ayrılır: 3.26 vs 7.65).

## 3.5 Kontrast — WCAG AA doğrulaması (hesaplanmış)

| Ön plan | Arka plan | Oran | Sonuç |
|---|---|---|---|
| `text #17181C` | `bg #F6F4F1` | **16.15:1** | AAA ✅ |
| `text #17181C` | `surface #FFFCF8` | **17.34:1** | AAA ✅ |
| `text-2 #5A5B63` | `bg #F6F4F1` | **6.15:1** | AA ✅ (AAA large) |
| `text-2 #5A5B63` | `surface #FFFCF8` | **6.60:1** | AA ✅ |
| `text-3 #6B6C75` | `bg #F6F4F1` | **4.75:1** | AA ✅ (alt sınır) |
| `text-2 #5A5B63` | `disabled-bg #E7E1D8` | **5.20:1** | AA ✅ (pasif buton bile okunur) |
| `surface #FFFCF8` | `ink #17181C` | **17.34:1** | AAA ✅ (birincil buton) |
| `surface #FFFCF8` | `ink-pressed #2C2E34` | **13.28:1** | AAA ✅ |
| `accent #D9661A` | `bg #F6F4F1` | **3.26:1** | Metin dışı AA ✅ (yay, nokta, dolgu) · normal metin ✗ |
| `accent #D9661A` | `surface #FFFCF8` | **3.50:1** | Metin dışı AA ✅ |
| `text #17181C` | `accent #D9661A` | **4.96:1** | AA ✅ (FAB ikonu, amber zeminde metin) |
| `accent-deep #A8500C` | `bg #F6F4F1` | **5.01:1** | AA ✅ (amber'in metin varyantı) |
| `accent-deep #A8500C` | `surface #FFFCF8` | **5.38:1** | AA ✅ |
| `accent-deep #A8500C` | `accent-soft #FDEBD8` | **4.73:1** | AA ✅ |
| `text #17181C` | `accent-soft #FDEBD8` | **15.25:1** | AAA ✅ |
| `edge #6E3B6B` | `bg #F6F4F1` | **7.65:1** | AAA ✅ |
| `edge #6E3B6B` | `surface #FFFCF8` | **8.21:1** | AAA ✅ |
| `edge #6E3B6B` | `edge-soft #F0E4EF` | **6.82:1** | AA ✅ |
| `danger #9B2C1F` | `bg #F6F4F1` | **6.90:1** | AAA ✅ |
| `danger-on #FFFCF8` | `danger #9B2C1F` | **7.40:1** | AAA ✅ |
| `text #17181C` | en koyu kategori tinti `#DDEEF1` | **14.84:1** | AAA ✅ (en kötü durum) |
| Kategori `solid` renkleri | `bg #F6F4F1` | **4.53 – 7.72:1** | Hepsi metin dışı 3:1'i ve hatta 4.5'i geçiyor ✅ |

**Kasıtlı olarak zayıf tek çift:** `surface #FFFCF8` ↔ `bg #F6F4F1`
= **1.07:1**. Bu bir hata değil: kart ile zemin arasındaki ayrım renkle
değil **gölge + radius + boşlukla** kurulur (§6.2). Bir sınır anlam
taşıyorsa (ör. seçilebilir kart) yalnız yüzey tonuna güvenilmez.

**Kural:** Yeni bir renk çifti gerekirse **önce buraya oranıyla eklenir,
sonra kullanılır.** Hesaplanmamış çift kullanılamaz.

## 3.6 Gradyan kuralı (v1.0'da yasaktı — v2.0'da denetimli serbest)

Gradyan **üç yerde** kullanılabilir, dördüncüsü üretilmez:

| # | Nerede | Nasıl |
|---|---|---|
| 1 | **Kahraman yay dolgusu** | `#D9661A` → `#A8500C`, yay boyunca (açık uçtan topuza doğru koyulaşır). İki uç da ≥3:1. |
| 2 | **Grafik alan dolgusu** | `accent` %18 alfa → %0 alfa, dikey. Yalnızca çizgi grafiğin altında. |
| 3 | **Hero kart ambiyansı** | `surface #FFFCF8` → `accent-soft #FDEBD8`, dikey, yalnızca kahraman göstergenin bulunduğu kartta. Kontrast farkı ≤1.2:1 → üzerindeki metin her iki uçta da ≥14:1. |

**Yasak:** tam ekran arka plan gradyanı · **mor-mavi/indigo-violet
gradyan (anti-pattern §1)** · buton gradyanı · metin gradyanı · üç ve
daha fazla duraklı gradyan · farklı hue aileleri arası gradyan (amber →
mor gibi) · gradyanlı kenarlık · "glassmorphism" bulanık cam katmanı.

**Kural:** Gradyan **tek hue içinde iki durak**tır. Renk değiştiren
gradyan bu markada yoktur. RN'de `expo-linear-gradient` (Expo SDK'nın
parçası, ücretsiz) kullanılır.

## 3.7 Kahraman gösterge — renk davranışı (ürünün kalbi, bağlayıcı)

| Durum | Görünüm |
|---|---|
| %0-99 doluluk | Yay dolgusu **Mandalina gradyanı** (§3.6/1), oluk `surface-2 #EFEAE3`. Renk doluluk arttıkça **değişmez**. |
| %100 | Yay tam tur (270°) amber. Yayın bitiş noktasında **eşik işareti**: 2pt, `text-2`, yayın dışına 6pt taşar. |
| %100+ (limit dışı) | Ana yay amber kalır. Taşan miktar, ana yayın **6pt dışında, 6pt kalınlığında ayrı bir yay** olarak **Mürdüm `#6E3B6B`** ile çizilir; saat 12 hizasından başlar. |

**Neden dışarıda ayrı bir yay?** Çünkü ürünün dili bu: aşım "hata" değil
**"limit dışı"**. Taşan miktar kelimenin tam anlamıyla çizginin
dışında durur. Ana yay rengini değiştirmez, yanıp sönmez, titremez,
ikon değiştirmez.

**Neden yeşil→sarı→kırmızı geçişi yok?** Trafik ışığı metaforu her
harcamayı bir "risk" olarak kodlar ve §2.1 *Yargısız* ilkesini yıkar.
Bilgi taşıyıcısı **doluluk oranıdır**, renk değil.

## 3.8 Karanlık mod — **FAZ 2 · Faz 1 kapsamı dışı**

> Faz 1'de karanlık mod **yoktur**; `useColorScheme()` kullanılmaz.
> Aşağıdaki tablo, Faz 2'de aceleyle `invert` yapılmasın diye kavramı
> şimdiden kilitler. Karanlık mod **ters çevirmeyle üretilemez**
> (anti-pattern).

Gece hali "ışık"ın karşıtı değil, **akşam**: sıcaklık korunur (nötrler
nötr-gri değil, sıcak kahverengi-siyah), amber koyu zeminde okunacak
şekilde **açılır**.

| Token | Açık (Faz 1) | Karanlık (Faz 2) | Kontrast (ön hesap) |
|---|---|---|---|
| `bg` | `#F6F4F1` | `#151311` | saf siyah değil |
| `surface` | `#FFFCF8` | `#1F1C19` | katman farkı + gölge yerine ince `line` |
| `line` | `#E6E1DA` | `#33302B` | — |
| `text` | `#17181C` | `#F2EDE6` | **15.91:1** ✅ |
| `text-2` | `#5A5B63` | `#B0A79B` | **7.81:1** ✅ |
| `accent` | `#D9661A` | `#F0913F` | **7.79:1** ✅ (buton zemini olursa metin `#151311`) |
| `edge` | `#6E3B6B` | `#C48FC0` | Faz 2'de hesaplanacak |
| `danger` | `#9B2C1F` | `#E38273` | Faz 2'de hesaplanacak |
| Kategori `solid` | tablo §3.3 | **açılmış varyantları ayrıca çizilir** | Faz 2'de hesaplanacak |

Karanlık modda gölge **azaltılır** (koyu zeminde gölge görünmez):
katman ayrımı yüzey tonu + 1px `line` ile yapılır.

---

## 3.D ALTERNATİF — Yön D "Gece Sayacı" paleti

> **Bu palet şu an uygulanmaz.** Mustafa Yön D'yi seçerse §3.1-3.8
> bu değerlerle yeniden yazılır ve `tokens.md` buna göre üretilir.

**Kavram:** Uygulama gündüz-gece fark etmeyen, karanlık öncelikli tek
temalı bir **sayaç**. Ekran kararır, sayı parlar. Enerji renkten değil,
**karanlık ile canlı aksan arasındaki kontrasttan** gelir.

| Token | HEX | Kullanım |
|---|---|---|
| `bg` | `#0E1214` | Ana zemin |
| `surface` | `#171C1F` | Kart |
| `surface-2` | `#1F2529` | Yükseltilmiş katman, oluk |
| `line` | `#2A3135` | Hairline |
| `text` | `#EDF1F2` | ~15:1 ✅ |
| `text-2` | `#9FAAAD` | ~7:1 ✅ |
| `accent` — **Nane** | `#4ADEA8` | Yay dolgusu, aktif durum, FAB. Koyu zeminde ~11:1 ✅; buton zemini olduğunda metin `#0E1214` |
| `edge` — **Şeftali** | `#FFB07C` | Yalnızca limit dışı (sıcak ama alarm değil) |
| `danger` | `#F2705C` | Yalnızca yıkıcı işlem |
| Kategori | Aynı 6 kategori, **koyuda okunacak biçimde açılmış** varyantlar (ör. Deniz `#5EC7D8`, Nar `#FF8095`) | Tintler yerine %12 alfa dolgular |

**Artı:** TR kişisel finansta hiçbir rakip koyu değil → anında ayrışma ·
tek tema (Faz 2 karanlık mod işi ortadan kalkar) · büyük rakamlar koyu
zeminde daha güçlü.
**Eksi:** Mustafa'nın gösterdiği referans açık ve havadar — bu yön onun
ruhuna ters · koyu + finans, "borsa/trading" çağrışımı yapıyor · ürün
**gün içinde dışarıda** kullanılıyor, güneşte okunurluk düşer ·
kategori pastel sistemi koyuda yeniden ayarlanmalı · illüstrasyon ve
sosyal medya görselleri koyuda daha zor yönetilir.

---

# BÖLÜM 4 — TİPOGRAFİ

## 4.0 Kısıt: RN'de font gömülür

Fontlar CDN'den çekilmez, **uygulamaya gömülür**. Her ağırlık dosyası
uygulama boyutunu büyütür.

> **Bütçe: en fazla 3 font dosyası.** Variable font kullanılmaz (RN'de
> ağırlık ekseni desteği platformlar arası güvenilmez); statik `.ttf`
> gömülür. İtalik kullanılmaz. Vurgu = ağırlık + boyut + renk.

Seçilen fontların ikisi de **OFL** (ücretsiz, ticari kullanıma açık,
`@expo-google-fonts/*` ile kurulur). **Ücretli font önerilmemiştir.**

## 4.1 Yön C — Font çifti

### Sayılar: **Space Grotesk** · Bold 700 (tek ağırlık)

Kullanım alanı **yalnızca rakamlardır**: kahraman sayı, kart içi büyük
sayı, liste tutarları. Metin dizmez.

**Gerekçe (marka bağı):**
- Space Grotesk, sabit genişlikli **Space Mono**'nun oransal
  varyantıdır. Rakamları bu mirastan gelir: dik, eşit ağırlıklı,
  **sayaç gibi**. Ürünün çekirdek metaforu ("kalori sayar gibi") tam
  olarak budur — sayı bir *bakiye* değil, bir *ölçüm* gibi durur.
- **Tabular figür desteği var** (fontun OpenType özellikleri arasında
  tabular figures bulunuyor) — kahraman sayı her harcamada değişecek;
  rakamlar farklı genişlikte olursa sayı "titrer". Para uygulamasında
  bu pazarlık edilemez.
- 56pt'de karakterlidir ama gösterişçi değildir: `1`, `4`, `7`
  terminalleri kesiktir, `0` dar ve diktir — ekranda **tanınır bir
  imza** bırakır. Marka tanınırlığının büyük kısmını bu üstlenir.
- Latin Extended-A kapsar → Türkçe tam (§4.3 testi yine de zorunlu).

### Arayüz ve başlık: **Figtree** · Regular 400 + SemiBold 600

**Gerekçe:**
- Geometrik-hümanist bir arayüz sansı; **dostane geometri** hedefinin
  (yüksek radius, daire, pill) tipografik karşılığı. Referansın
  "yumuşak ama profesyonel" hissini serife düşmeden verir.
- Ürün arayüzleri için çizilmiş: 13pt etiketlerde ve dar mobil sütunda
  okunur, x-height yüksek, sayaç fontunun yanında geri planda kalır
  (başlığın önüne geçmez) = §2.1 *Odaklı*.
- OFL, 280+ Latin dili, Türkçe dahil; tabular figür özelliği de var
  (yedek olarak).
- Poppins'in geometrik neşesine yakın bir sıcaklığı var ama Poppins
  değil — yani **anti-pattern'e düşmeden** aynı yaklaşılabilirlik
  elde ediliyor.

**Neden Inter / Poppins / Montserrat değil:** Üçü de anti-pattern
listesinde ve bu kategoride varsayılan hâline geldiler — font seçimi
olmaktan çıkıp "seçim yapılmadığının işareti" oldular. Inter nötr-teknik
soğukluğuyla §2.1 *Sıcak*'a ters; Montserrat'ın geniş geometrik formları
küçük puntoda TL tutarlarını şişirir; Poppins'in dairesel formları
finansal içerikte çocuksu kaçar.

**Toplam: 3 dosya** — `SpaceGrotesk-Bold.ttf`, `Figtree-Regular.ttf`,
`Figtree-SemiBold.ttf`. Bütçe içinde (v1.0'da 4 dosyaydı).

## 4.2 Tip ölçeği (9 rol — ara değer üretilemez)

| Rol | Font / Ağırlık | Boyut | Satır y. | Harf ar. | Kullanım |
|---|---|---|---|---|---|
| `hero` | Space Grotesk Bold | **56** | 60 | −1.5 | **Yalnızca** kahraman gösterge ortasındaki sayı. Ekranda bir tane. Tabular. |
| `display` | Space Grotesk Bold | **32** | 38 | −0.8 | Kart içi büyük sayı, tutar girişi. Tabular. |
| `amount` | Space Grotesk Bold | **17** | 24 | 0 | Liste içi tutar. Tabular, sağa hizalı. |
| `h1` | Figtree SemiBold | **26** | 32 | −0.3 | Ekran başlığı |
| `h2` | Figtree SemiBold | **19** | 25 | −0.1 | Kart/bölüm başlığı |
| `body` | Figtree Regular | **16** | 24 | 0 | Gövde, liste birincil satır |
| `body-strong` | Figtree SemiBold | **16** | 24 | 0 | Buton etiketi, vurgulu gövde |
| `label` | Figtree SemiBold | **13** | 18 | +0.3 | Etiket, pill, sekme adı, gösterge altı etiket |
| `caption` | Figtree Regular | **13** | 18 | 0 | Tarih, ikincil satır, hata metni |
| `micro` | Figtree Regular | **12** | 16 | +0.2 | Yasal metin. **Mutlak alt sınır — 12'nin altına inilmez.** |

İzinli punto listesi: **12 · 13 · 16 · 17 · 19 · 26 · 32 · 56**
(+ splash wordmark 32). Bu listenin dışına çıkılamaz.

**Hiyerarşi kuralı (referanstan alınan ders):** Kahraman sayı ile onun
etiketi arasındaki oran **en az 4×** olmalıdır (56 ↔ 13). Bu oran
düşerse ekran "her şey eşit ağırlıkta" hâline gelir — v1.0'ın
cansızlığının teknik sebebi tam olarak buydu.

**BÜYÜK HARF (uppercase) kullanılmaz.** Türkçe `i/İ` ve `ı/I` dönüşümü
platformlar arası hata üretir; ayrıca bağırma tonu taşır.

## 4.3 Türkçe kontrol listesi (zorunlu)

Font gömülmeden önce şu karakterler render edilip **gözle** kontrol
edilir: `ğ Ğ ı I i İ ş Ş ç Ç ö Ö ü Ü â î û`
En kritik ikili: **ı (noktasız i)** ve **İ (noktalı büyük i)**.
Eksikse font reddedilir, yeni aday brandbook'a gerekçesiyle eklenir.
Ek olarak `₺` glifi kontrol edilir; fontta yoksa sistem yedeğine
düşeceği için tutar hizası bozulur — bu durumda `₺` ayrı `Text` olarak
`Figtree` ile dizilir.

## 4.4 Rakam kuralı (bağlayıcı)

Tüm para tutarları `fontVariant: ['tabular-nums']` ile render edilir.
Bir platformda uygulanmazsa **geri düşüş kuralı:** tutar kabı sabit
genişlikte olur ve sağa hizalanır. Hiçbir koşulda değişen sayı yatayda
oynamaz. Kahraman sayı için ek kural: kap genişliği **en uzun olası
tutara göre** ölçülür, sayı büyüdükçe kart yeniden düzenlenmez.

## 4.D ALTERNATİF — Yön D tipografisi

> Uygulanmaz. Yön D seçilirse geçerli olur.

**Manrope** · Regular 400 + ExtraBold 800 — **tek aile, 2 dosya.**
Gerekçe: yarı-daraltılmış geometrik formu koyu zeminde büyük rakamları
sıkı ve parlak gösterir; tek aile, "araç" kişiliğine uygun tek sesli
bir tipografi kurar; OFL, Türkçe destekli. Ölçek Yön C ile aynı
puntolardadır; `hero` mono-benzeri değil daha sıkı olduğu için **60**'a
çıkabilir.
**Riski:** tek aile, hiyerarşiyi yalnız ağırlık/boyutla kurar; yanlış
uygulanırsa monoton görünür.

---

# BÖLÜM 5 — LOGO: **Trinkow**

Ad kesin (Mustafa kararı). Yazım kuralı §2.7; burada **görsel** kullanım
tanımlanır. v2.0'da logo **yeni tipografiye ve yeni kahraman öğeye
göre** yeniden çizilir.

## 5.1 Logo sistemi — üç varyant, fazlası üretilmez

Logo bir **kelime markasıdır (wordmark)**. Maskot, soyut sembol veya
"amblem + isim" kilidi üretilmez: iyi bir wordmark, tanınırlık bütçesi
olmayan bir üründe soyut sembolden her zaman daha iyi çalışır (sembol
öğrenilmek ister, kelime doğrudan okunur) ve tek kişilik ekipte bakımı
garanti edilebilecek tek sistem budur.

| # | Varyant | Ne zaman |
|---|---|---|
| 1 | **Kelime markası** — "Trinkow" | Ana varyant: splash, onboarding ilk ekran, ayarlar altbilgisi, App Store başlığı, sosyal kapak. |
| 2 | **Monogram** — "T" + topuz | Yalnızca kare/dar alan: uygulama ikonu, bildirim ikonu, favicon. |
| 3 | **Tek renk** | Baskı, tek renkli yüzey, üçüncü taraf listeleme. %100 mürekkep veya %100 ışık. |

**Uygulama içinde logo nerede geçer?** Geçer: splash, onboarding ilk
ekran, ayarlar altbilgisi. **Geçmez:** ekran başlıkları, pano üstü,
bildirim, boş durum. Bu, kullanıcının göstergesi — bizim müşteri
panelimiz değil.

## 5.2 Kelime markası — dizim spesifikasyonu

| Özellik | Değer |
|---|---|
| Font | **Space Grotesk Bold 700** (§4.1 ile aynı aile — ek dosya yok) |
| Büyük/küçük | `Trinkow` (§2.7) |
| Harf aralığı | **−2.0%** (32pt'de ≈ −0.64pt). Ölçek büyüdükçe yüzde sabit kalır. |
| Kerning | Fontun kendi tablosu; elle çift düzeltmesi yapılmaz. |
| Satır | **Her zaman tek satır.** Kavise dizilmez. |
| Dönüştürme | Yok. Uppercase/smallcaps yasak. |

Neden Space Grotesk (gövde fontu Figtree değil): wordmark'ın markanın
**sayı sesiyle** aynı olmasını istiyoruz — kullanıcı uygulamada en çok
o formu görecek. Wordmark ile kahraman sayı aynı aileden gelince marka
tek bir imza bırakır.

Kelime markası **canlı metin olarak** dizilebilir
(`fontFamily: SpaceGrotesk-Bold`, `letterSpacing: fontSize × −0.02`).

## 5.3 Monogram — "T ve topuz"

Sembol zorlanmadı: monogram, kelime markasının **ilk harfidir**; sağ
üst ucuna ürünün çekirdeğinden gelen **tek bir topuz** eklenir.

**Fikrin bağı:** cüzdan, kumbara, madeni para, yükselen ok, `₺` simgesi
— hepsi fintech'in tükenmiş dağarcığı ve §5.6 gereği yasak. Bizim
işaretimiz **kahraman göstergeden** türer: `T`'nin yatay kolu bir yay
parçası gibi okunur, ucundaki **dolu daire** göstergenin topuzudur
(§7.5). Yani logo, ürünün tek kahraman öğesinin en küçük hâlidir.

**Geometri (100 × 100 ızgara, ölçeklenebilir):**

| Eleman | Değer |
|---|---|
| Izgara | 100 × 100 kare |
| "T" | Space Grotesk Bold, cap-height **58**, taban çizgisi **y = 79**, kolun üstü **y = 21** |
| "T" yatay konum | Kolun sol ucu **x = 18**, sağ ucu **x = 72** |
| Topuz | Dolu daire, çap **18**, merkez **(x = 78, y = 26.5)** — kolun dikey ekseninde |
| Topuz ↔ kol | Topuz kola **değer** (1 birim örtüşür), boşluk bırakılmaz |
| Topuz sayısı | **Tam olarak 1.** Çoğaltılmaz, sayaç gibi kullanılmaz. |
| Optik merkez | Bileşke şeklin görsel merkezi ızgara merkezine oturur. |

**Renk:** Monogram **tek renk** ya da **iki renk** olabilir:
- Tek renk (varsayılan): tamamı `text` veya tamamı `bg`.
- İki renk (yalnızca uygulama ikonu ve büyük kullanımlar): "T" =
  `bg #F6F4F1`, topuz = `accent #D9661A`, zemin = `ink #17181C`
  (kontrast: T/zemin **16.1:1**, topuz/zemin **4.96:1**) ✅
- Üç renk yoktur. Gradyanlı monogram yoktur.

## 5.4 Koruma alanı, minimum boyut

- **Koruma alanı:** dört yanda en az **1 × cap-height** (monogramda
  ızgaranın %25'i). Bu alana metin, ikon, kenar girmez.
- **Minimum — ekran:** kelime markası **20pt**; monogram **16 × 16pt**.
  Daha dar alan varsa logo **konmaz** (küçültülmez).
- **Minimum — baskı:** kelime markası **18 mm**.
- Uygulama içinde kelime markası **28pt**'i geçmez (splash hariç: 32pt).

## 5.5 Uygulama ikonu ve splash

| Kural | Değer |
|---|---|
| Ana dosya | **1024 × 1024 px**, PNG, saydamlık yok |
| Zemin | Tam taşma **`ink #17181C`** |
| İşaret | İki renkli monogram: "T" `#F6F4F1`, topuz `#D9661A` |
| Monogram kutusu | **620 × 620 px**, optik merkez, dikeyde **20 px yukarı** |
| Köşe yuvarlaklığı | **Çizilmez** — iOS/Android maskeyi kendi uygular. Kare gönderilir. |
| Güvenli alan | Monogram, 1024'lük karenin merkezindeki **737 px çaplı daireye** taşmaz |
| Android adaptive | `background` düz `#17181C` + `foreground` monogram (66dp güvenli alan). Paralaks/gölge kapalı. |
| Android bildirim ikonu | 96 × 96, saydam zemin, **beyaz silüet**, 24 px iç boşluk. Sistem tek renge çevirir; topuz silüette de ayrı durmalı. |
| İçinde olmayacaklar | Metin, slogan, `₺`, gradyan, gölge, dış çizgi, çerçeve, parlama, ekran görüntüsü, emoji |
| **Splash** | Zemin `bg #F6F4F1`, ortada kelime markası 32pt `ink`, "w"nin sağında topuz noktası `accent`. Sürüm/slogan/spinner/animasyon **yok**. |

**Küçük boyut testi (zorunlu):** ikon 40 px'e küçültülüp bakılır. Topuz
hâlâ ayrı bir eleman olarak görülüyorsa geçer; "T"ye yapışıp tek leke
oluyorsa topuz çapı 18 → 20'ye çıkarılır. Bu, topuzun büyütülebileceği
**tek** durumdur.

## 5.6 Yasaklı kullanımlar

- Gradyan dolgu, gölge, dış çizgi (outline), 3D/kabartma, parlama.
- Esnetme, döndürme, eğme, kavise dizme.
- Palet dışı renk; logoda `edge` (mürdüm) veya `danger` kullanımı — bu
  renklerin anlamı markanın adına bulaştırılamaz.
- Yoğun fotoğraf/desen üzerine yerleştirme.
- Yanına emoji, ünlem veya slogan bitiştirme.
- **"o" harfini madeni para, daire, hedef tahtası veya `₺` ile
  değiştirmek** — fintech'in en yıpranmış klişesi.
- Harflerin üstüne ilerleme yayı/grafik/ok yerleştirmek.
- Kelime markasını farklı bir fontla (Figtree dahil) yeniden dizmek.
- Topuzu çoğaltmak, animasyonlamak, doluluk göstergesine çevirmek.
- Adı §2.7 dışında bir biçimde dizmek.

---

# BÖLÜM 6 — GÖRSEL DİL

## 6.1 Temel ilke — **tek kahraman**

Referansın canlı hissettirmesinin birinci sebebi süs değil,
**hiyerarşi**: ekranı tek bir öğe yönetiyor, göz nereye gideceğini
biliyor.

> **Her ekranda tam olarak bir kahraman öğe vardır.** Panoda dairesel
> gösterge, giriş ekranında tutar alanı, detayda büyük sayı. Kahraman
> öğe ekranın üst yarısındadır ve genişliğinin en az %55'ini kaplar.
> İkinci bir öğe onunla boyut/ağırlık yarışına giremez.

Dikkat çekme sırası: (1) **boyut**, (2) **ağırlık**, (3) **renk**,
(4) **derinlik/gölge**, (5) boşluk. v1.0 yalnız 5'i kullanıyordu; bu
yüzden ekranlar düz ve cansız çıktı.

## 6.2 Derinlik ve gölge (v1.0'da yasaktı — v2.0'da amaçlı serbest)

**İlke:** Gölge dekorasyon değil, **yükseklik bilgisidir.** Bir öğe
gölge alıyorsa "diğerlerinin üstünde/önünde" diyordur. Her karta
refleksle gölge uygulamak anti-pattern'dir ve yasaktır.

**İki seviye vardır, üçüncüsü üretilmez:**

| Seviye | Nerede | iOS | Android | Ek zorunluluk |
|---|---|---|---|---|
| `elev.1` | Kart, kategori kutusu, liste grubu | `shadowColor '#3A2A1C'` · `shadowOpacity 0.06` · `shadowRadius 12` · `shadowOffset {0, 4}` | `elevation: 2` | Yüzey `surface`, radius 24 |
| `elev.2` | Kahraman kart, yüzen sekme çubuğu, bottom sheet, FAB | `shadowColor '#3A2A1C'` · `shadowOpacity 0.10` · `shadowRadius 24` · `shadowOffset {0, 8}` | `elevation: 8` | Sheet'te ek olarak `scrim` |

**Platform kuralı (RN kısıtı — zorunlu):** iOS `shadow*` ile Android
`elevation` aynı sonucu vermez. Bu yüzden **gölge tek başına anlam
taşıyamaz**: gölgeli her yüzey aynı anda (a) `surface` tonunda,
(b) radius ≥ 24 olmak zorundadır. Android'de gölge zayıf kalsa bile
katman, ton ve form ile okunur.

**Gölge rengi siyah değil, sıcak mürekkeptir (`#3A2A1C`).** Saf siyah
gölge sıcak zeminde griye çalar ve yüzeyi kirletir; sıcak gölge
"gün ışığı" kavramını korur.

**Yasak:** her karta otomatik gölge · liste satırı, çip, buton, girdi
alanına gölge · iç gölge (RN'de yok) · renkli parlama (glow) · çift
gölge · `shadowOpacity > 0.12`.

## 6.3 Köşe yuvarlaklığı — **tip bazlı sabit tablo**

Yüksek radius **dostane geometri**nin (§2.1 *Sıcak*) taşıyıcısıdır, ama
"rastgele 12/16/24 karışımı" anti-pattern'dir. Bu yüzden değer,
tasarımcının kararı değil **eleman tipinin** sonucudur:

| Eleman | Radius |
|---|---|
| Kahraman kart, bottom sheet üst köşeleri | **28** |
| Kart, kategori kutusu, toast, modal | **24** |
| Küçük kutu, ikon kabı, grafik kabı, girdi alanı | **16** |
| Buton, çip, pill, sekme göstergesi, ilerleme çubuğu | **hap** → `borderRadius: 999` |
| Avatar, FAB, gösterge topuzu, kategori noktası | **daire** |
| İlerleme yayı uçları | `strokeLinecap: 'round'` |

İzinli değerler: **16 · 24 · 28 · 999 · 0**. Başka radius hesaplanmaz.
(Odak halkası: elemanın radius'u + 4.)

## 6.4 Fotoğraf ve illüstrasyon (v1.0'da yasaktı — v2.0'da koşullu serbest)

- **Fotoğraf uygulama içinde kullanılmaz.** Ürünün içeriği fotoğraf
  değil, sayıdır. (Faz 3 fiş fotoğrafı işlevseldir, dekorasyon değil ve
  kapsam dışıdır.) Pazarlama görsellerinde yalnızca **gerçek ürün ekran
  görüntüsü** kullanılır.
- **Stok illüstrasyon kesinlikle yasak** (undraw.co ve benzerleri).
  Maskot, karakter, avatar yok.
- **Markaya özel illüstrasyon serbest** ve şu dille sınırlıdır:
  > Boş durum ve onboarding görselleri yalnızca **markanın kendi
  > formlarından** kurulur: açık yay, dolu daire (topuz), pill, ince
  > çizgi. Palet marka paletidir (amber + bir nötr + en fazla bir
  > kategori rengi). Perspektif yok, insan figürü yok, gölge yok,
  > kontur kalınlığı ikonlarla aynı (2.0).
- Bu kural sayesinde illüstrasyonlar "stok" değil, **kahraman
  göstergenin akrabası** olur; her ekran aynı görsel aileden gelir.

## 6.5 İkon seti (tek set, kilitli)

- Set: **Lucide** (`lucide-react-native`, ISC — ücretsiz). Tek set
  kullanılır; başka setten tek bir ikon bile karıştırılmaz.
- **Boyut:** 24pt (varsayılan) · 20pt (liste içi) · 28pt (sekme).
  Ara boyut yok.
- **Çizgi kalınlığı: 2.0** (v1.0'da 1.75'ti). Gerekçe: geometrik sans
  ve yüksek radius yanında 1.75 cılız kalıyor; 2.0, Figtree SemiBold'un
  görsel ağırlığıyla eşleşir. Aktif sekme ikonu da 2.0 — ayrım renkle
  yapılır.
- **Dolgulu (filled) ikon kullanılmaz.** Tek istisna: kategori noktası
  (o bir ikon değil, renk göstergesidir).
- Her ikon-butonun `accessibilityLabel`'ı Türkçe ve fiil ile yazılır.

## 6.6 Hareket

- Amaç dekorasyon değil **durum değişimi**. "Ne oldu / nereden geldi"
  sorusuna cevap vermeyen animasyon silinir.
- Süreler: `pressed` **120ms** · gösterge dolumu **420ms ease-out**
  (yay uzun yol katediyor, 280ms'de sıçrar gibi görünüyor) · sheet
  **320ms ease-out** · sayı sayacı **420ms**, gösterge ile eş zamanlı.
- **Sayı animasyonu serbest ama kurallı:** kahraman sayı değişirken
  eski değerden yenisine sayar (tabular olduğu için genişlik oynamaz).
  Kuruş basamağı animasyonlanmaz.
- **Yasak:** yanıp sönme, titreme (shake), zıplama (bounce/spring
  overshoot), konfeti, sürekli dönen dekoratif öğe, `scale` basma
  animasyonu, splash animasyonu.
- `AccessibilityInfo.isReduceMotionEnabled` açıksa tüm süreler **0ms**.

---

# BÖLÜM 7 — UI COMPONENT İLKELERİ

> `ui-ux-designer` bu bölümü **birebir** uygular. Sayılar öneri değil,
> spesifikasyondur. Makine okunur karşılığı: `projects/trinkow/docs/brand/tokens.md`.

## 7.0 Spacing sistemi

**Taban birim 4pt.** İzin verilen değerler:
`4 · 8 · 12 · 16 · 20 · 24 · 32 · 48 · 64`

| Uygulama | Değer |
|---|---|
| Ekran yatay iç boşluğu | **20** (tüm ekranlarda sabit) |
| Bölümler arası dikey boşluk | 24 |
| Kart içi iç boşluk | **20** (radius 24 ile dengeli; 16 dar kalıyor) |
| Kartlar arası dikey boşluk | 12 |
| Liste satırları arası | 0 (ayrım 1px `line`) |
| Kahraman kart iç boşluğu (dikey) | 32 |
| Safe area | üst `insets.top` · alt `insets.bottom + 8` |
| Yüzen sekme çubuğu ↔ ekran kenarı | 16 (yanlar), `insets.bottom + 8` (alt) |

## 7.1 Buton (üç varyant, dördüncüsü üretilmez)

| Varyant | Yükseklik | Radius | Zemin | Metin | Kenarlık | Pressed |
|---|---|---|---|---|---|---|
| **Birincil** | **54** | 999 (hap) | `ink #17181C` | `#FFFCF8` / `body-strong` (**17.34:1**) | yok | zemin → `#2C2E34` |
| **İkincil** | **50** | 999 | `surface-2 #EFEAE3` | `text #17181C` / `body-strong` | yok | zemin → `#E5DFD6` |
| **Sessiz** | **44** | 999 | şeffaf | `text-2 #5A5B63` / `body-strong` | yok | zemin → `#E5DFD6` |

| Ortak kural | Değer |
|---|---|
| Yatay iç boşluk | **24** (hap formu daha fazla nefes ister) |
| Metin | Tek satır, kırpılmaz; sığmazsa metin kısaltılır, buton büyümez |
| Ekran başına birincil buton | **En fazla 1** |
| İkon | Solda, 20pt, metinle arası 8 |
| Gölge | **Yok** (butonlar yükselmez) |
| Android ripple | `android_ripple={{ color: '#2C2E34', borderless: false }}` |
| `disabled` | Zemin `#E7E1D8`, metin `text-2` (**5.20:1**). **Opaklık kullanılmaz.** |
| `loading` | Metin yerinde, sağında 20pt `ActivityIndicator`, genişlik sabit, `disabled`. Metin: "Kaydediliyor". |
| `scale` animasyonu | Yok. Geri bildirim yalnız zemin değişimi (120ms). |
| **Odak (focus)** | 2pt `ink #17181C` dış çizgi, elemandan **2pt boşlukla**, radius = eleman radius + 4. Koyu zeminli elemanda halka `#FFFCF8`. **Hiçbir zaman kaldırılmaz.** |

RN'de **hover yoktur**; `pressed` tek geri bildirimdir ve her
etkileşimli eleman için tanımlanması zorunludur.

## 7.2 Kart

| Özellik | Değer |
|---|---|
| Zemin | `surface #FFFCF8` |
| Radius | **24** (kahraman kart 28) |
| Gölge | `elev.1` (kahraman kart ve sheet: `elev.2`) — §6.2 |
| Kenarlık | **Yok.** Ayrım gölge + radius + boşlukla. (Android'de gölge zayıfsa 1px `line` eklenebilir; bu yalnız Android yedeğidir.) |
| İç boşluk | 20 |
| Kartlar arası | 12 |
| `pressed` (tıklanabilirse) | Zemin → `#F6F4F1`, gölge `elev.1` → düz (kart "basılıp yüzeye iner"). Ölçek animasyonu yok. |
| **Yasak** | "Daire içinde ikon + başlık + tek cümle" formatında 3'lü özellik kartı düzeni (anti-pattern) |

## 7.3 Liste satırı (harcama listesi — `FlatList`)

| Özellik | Değer |
|---|---|
| Minimum yükseklik | **68** |
| Dikey iç boşluk | 12 · yatay 20 |
| Sol | **Kategori kabı**: 40 × 40, radius 16, zemin kategori `soft`, içinde 20pt kategori ikonu `solid` renginde |
| Orta | Birincil satır `body` / `text` · ikincil satır `caption` / `text-2` |
| Sağ | Tutar `amount`, sağa hizalı, tabular, `text` |
| Ayraç | 1px `line`, sol kenardan **72pt** içeriden başlar (kategori kabı hizası) |
| Gölge | Yok — liste kart içindedir, satır ayrıca yükselmez |
| **Limit dışı satır** | Zemin `edge-soft #F0E4EF`, tutarın altında `caption` boyutunda `edge` renginde "limit dışı" etiketi. **Ünlem ikonu, kalın kırmızı çizgi, üstü çizili metin yok.** |
| Kaydırarak silme | Sağa kaydırma → `danger` zeminli "Sil"; **her zaman** onay diyaloğu |

## 7.4 Form / metin girişi (en kritik ekran: harcama girişi)

| Özellik | Değer |
|---|---|
| Yükseklik | **54** · radius **16** · zemin `surface` |
| Kenarlık (normal) | 1.5pt `line-strong #CFC9C0` |
| Kenarlık (odaklı) | 1.5pt `accent-deep #A8500C` — kalınlık değişmez, düzen kaymaz |
| Kenarlık (hatalı) | 1.5pt `danger #9B2C1F` + altında `caption` / `danger` hata metni, 8 boşlukla |
| Etiket | Girişin **üstünde**, `label`, `text-2`, arası 8. Placeholder'a gömülmez. |
| Placeholder | `text-3 #6B6C75` (4.75:1) |
| **Tutar alanı** | `keyboardType="decimal-pad"`, otomatik odak, **`display` (32pt Space Grotesk)** boyutunda, ondalık ayracı **virgül**, `₺` sağda `text-2` |
| Kategori seçimi | Yatay pill listesi (§7.6), seçili pill kategori `soft` zemin + `solid` nokta |
| Klavye açıkken görünür kalacak | **"Kaydet" butonu** (`KeyboardAvoidingView` ile klavyenin üstüne sabitlenir) |
| Hedef | **Harcama girişi en fazla 3 dokunuşta biter** (tutar → kategori → Kaydet). Aşan tasarım reddedilir. |

## 7.5 Kahraman gösterge — dairesel yay (ürünün kalbi)

| Özellik | Değer |
|---|---|
| Çizim | `react-native-svg` + `expo-linear-gradient` (yay dolgusu için `Defs`/`LinearGradient`) |
| Dış çap | **200pt** (390pt ekranda genişliğin %51'i) |
| Yay açıklığı | **270°**, boşluk **altta** (saat 7 → saat 5 yönü), başlangıç saat 7'de |
| Kalınlık | **18pt** · uç `strokeLinecap: 'round'` |
| Oluk | `surface-2 #EFEAE3` |
| Dolgu | Mandalina gradyanı `#D9661A` → `#A8500C` (§3.6/1), **doluluktan bağımsız** |
| **Topuz (knob)** | Yayın ucunda: 22pt `surface` daire + 4pt `accent-deep` halka + kendi `elev.1` gölgesi. Referansın "fizikselliğini" veren tek detay budur; **kaldırılamaz.** |
| Ortada | `hero` (56pt) kahraman sayı — §2.4'e göre kipe bağlı |
| Sayının altında | `label` (13pt) `text-2` tek satır etiket. **Oran ≥ 4× korunur** (§4.2). |
| Eşik işareti | %100 noktasında 2pt `text-2` çizgi, yayın dışına 6pt taşar |
| Taşma yayı | Ana yayın **6pt dışında**, 6pt kalınlıkta, `edge #6E3B6B`, saat 12'den başlar (§3.7) |
| Animasyon | 420ms ease-out; sayı eş zamanlı sayar. Reduce-motion açıksa 0ms. |
| Erişilebilirlik | `accessibilityRole="progressbar"` · `accessibilityValue={{min, max, now}}` · `accessibilityLabel="Günlük limit kullanımı"` · taşma varsa `accessibilityHint` yerine **görünür metin** kullanılır |
| %100+ davranışı | Renk dönmez, yanıp sönmez, titremez, ikon değişmez |

**Mini gösterge (kategori kartlarında):** aynı dil, küçültülmüş —
dış çap **56pt**, kalınlık 6pt, topuz **yok**, ortada `label` boyutunda
sayı, dolgu kategori `solid` rengi. Ekranda en fazla **3 mini gösterge**
yan yana (referanstaki gibi), dördüncüsü listeye döner.

**Kategori limit çubuğu (liste içinde, dairesel değil):** yükseklik 8pt,
radius 999, oluk `surface-2`, dolgu kategori `solid`, taşma `edge`.

## 7.6 Pill / çip (kategori ve kip seçimi)

| Özellik | Değer |
|---|---|
| Yükseklik | **36** → radius 999 |
| Pasif | Zemin `surface-2 #EFEAE3`, `label` / `text-2`, kenarlık yok |
| Seçili | Zemin kategori `soft` (kip pill'inde `accent-soft`), metin `text`, solda 8pt `solid` renkli nokta |
| `pressed` | Zemin → `#E5DFD6` |
| Yatay iç boşluk | 14 · nokta ↔ metin arası 8 |
| Dokunma hedefi | `hitSlop` ile **44** |
| Aralarında | 8 · yatay `ScrollView` |
| Onay ikonu | Eklenmez — zemin + nokta yeterli |

## 7.7 Yüzen sekme çubuğu + merkez eylem

| Özellik | Değer |
|---|---|
| Biçim | **Yüzen**: ekranın altından `insets.bottom + 8`, yanlardan 16 içeride |
| Yükseklik | **64** · radius 999 · zemin `surface` · gölge `elev.2` |
| Sekme sayısı | **En fazla 4** (Faz 1: 3) + merkez eylem |
| Sekme içerik kutusu | 48 × 48 (dokunma hedefi ≥ 44 ✅) |
| İkon | 28pt · altında `label` (13pt) — **etiketsiz ikon kullanılmaz** |
| Aktif | `accent-deep #A8500C` ikon + etiket SemiBold + ikonun arkasında 40pt `accent-soft` daire |
| Pasif | `text-2` + Regular |
| **Merkez eylem (FAB)** | **56 × 56 daire**, zemin `accent #D9661A`, içinde 24pt `ink` artı ikonu (**4.96:1** ✅), gölge `elev.2`. Sekme çubuğunun üst kenarından **12pt yukarı taşar.** |
| FAB `pressed` | Zemin → `accent-deep #A8500C` |
| FAB etiketi | `accessibilityLabel="Harcama ekle"` |
| Alt çizgi/nokta göstergesi | Yok |
| Odak halkası | 48 + 2pt boşluk + 2pt kenarlık = 56, bar İÇİNDE kalır |

Merkez eylem markanın en görünür renkli öğesidir: amber, ekranda tek
"buraya bas" noktasıdır ve her ekranda aynı yerdedir.

## 7.8 Boş durum

| Özellik | Değer |
|---|---|
| Sıra | Marka illüstrasyonu (§6.4) → `h2` başlık → `body` tek satır → birincil buton |
| İllüstrasyon | **Boş yay**: 120pt çaplı, 18pt kalınlıkta `surface-2` yay + ucunda topuz. Dolgu yok — "henüz bir şey yok" bunu zaten söyler. |
| Aralar | İllüstrasyon→başlık 24 · başlık→açıklama 8 · açıklama→buton 24 |
| Yasak metin | "Henüz veri yok" · teknik açıklama (§2.8) |

## 7.9 Toast / in-app banner

| Özellik | Değer |
|---|---|
| Zemin | `surface`, radius 24, iç boşluk 16, gölge `elev.2`, kenarlık yok |
| Sol gösterge | 8pt daire: `accent` (bilgi) · `edge` (limit dışı) · `danger` (yıkıcı sonuç) |
| Konum | Ekranın **üstünde**, `insets.top + 8` |
| Süre | 4 sn, otomatik kaybolur · kapatma 44 × 44 hit alanı |
| **Yasak** | Limit aşımını ekran ortasında modal ile bildirmek. Limit aşımı kullanıcıyı **durdurmaz**, bilgilendirir. |

## 7.10 Kategori kartı (panoda)

| Özellik | Değer |
|---|---|
| Düzen | Yan yana **3 kutu**, aralarında 12, her biri eşit genişlik |
| Kutu | Zemin `surface`, radius 16, iç boşluk 16, gölge yok (kart içindedirler) |
| İçerik sırası | Mini gösterge (56pt) → 4pt boşluk → `display`(32) yerine `h2`(19) sayı → `micro` etiket `text-2` |
| Renk | Her kutu kendi kategori `solid` rengini mini göstergede taşır |
| **Not** | Bu düzen, yasaklı "daire ikon + başlık + 1 cümle" 3'lü kart şablonu **değildir**: burada her kutu **gerçek veri** taşır (sayı + kategori), pazarlama metni değil. Ayrım budur ve `design-reviewer` bunu bu kritere göre denetler. |

---

# BÖLÜM 8 — KARARLAR

## 8.1 Kapanmış kararlar (değişmedi, yeniden açılmaz)

| # | Karar |
|---|---|
| 8.1.1 | **Ürün adı: Trinkow.** Yazım §2.7. |
| 8.1.2 | **Emoji yasak** — tüm yüzeyler (§2.6). |
| 8.1.3 | **Kullanıcıyı utandıran ton yasak** — limit aşımında suçlama yok (§2.3, §3.4). |
| 8.1.4 | **WCAG AA zorunlu** — hesaplanmamış renk çifti kullanılamaz (§3.5). |
| 8.1.5 | **Karanlık mod Faz 1'de yok** (§3.8). Yön D seçilirse bu karar konusuz kalır. |
| 8.1.6 | **Oyunlaştırma sınırı (K-048, 2026-09-17 — güncellendi):** **Seri (streak) ve milestone MVP'dedir**, dili §2.3'te kilitli. **Puan · seviye · XP · rozet · lig ise kalıcı olarak kapsam dışıdır** — "Faz 2'de yeniden açılır" ifadesi geçersizdir. Gerekçe §2.3 sonu: gerçek gün sayısı sayılabilir, icat edilmiş birim sayılamaz. |
| 8.1.7 | **Ücretli bağımlılık yok:** Space Grotesk + Figtree OFL, Lucide ISC, `expo-linear-gradient` ve `react-native-svg` Expo ekosisteminde ücretsiz. |
| 8.1.8 | **UI'da teknik açıklama yasak** (§2.8 — Mustafa kararı). **K-057/1 ile tek istisna tanımlandı:** mahremiyet, kullanıcı faydası dili ile söylenebilir (§2.8.1); mimari sözcük listesi ve yüzey sınırı bağlayıcıdır. Mahremiyet cümlesinin tek kaynağı §2.9. |
| 8.1.9 | **Hesap opsiyoneldir (K-052).** Google/Apple oturumu yalnız kimlik içindir; harcama verisi cihazda kalır. "Hesap yok / sunucu yok" ifadeleri **artık yanlıştır** ve hiçbir yüzeyde kullanılmaz. Sözcük: **"Oturum aç"** (K-057/6). |

## 8.2 AÇIK — Mustafa'nın karar vermesi gerekenler

| # | Soru | Ajanın önerisi |
|---|---|---|
| **S-1** | **Yön C ("Gün Işığı", sıcak amber + açık zemin)** mi, **Yön D ("Gece Sayacı", koyu + nane)** mi? | **Yön C.** Referans dili açık/havadar, rakip renk haritasında boş olan tek aile sıcak amber, ürün gün içinde dışarıda kullanılıyor. |
| **S-2** | Çekirdek renk tonu: **Mandalina `#D9661A`** onaylanıyor mu? Daha açık/parlak bir turuncu istenirse WCAG 3:1 eşiği nedeniyle yay dolgusu olarak kullanılamaz. | `#D9661A` (3.26:1) **alt sınırdır**; daha açık ton talep edilirse gösterge kalınlığı ve eşik işareti güçlendirilerek yeniden hesaplanmalı. |
| **S-3** | **Limit dışı rengi Mürdüm `#6E3B6B`** — kırmızı yerine mor bir ton kabul mü? | Evet. Kırmızı, hedef kitlenin en hassas noktası (§1.2). |
| **S-4** | **Birincil buton mürekkep (siyah hap)** mı olsun, marka rengi mi? | Mürekkep. Amber üzerine beyaz metin AA'yı geçmiyor (3.43:1); ayrıca marka rengi veriye ayrılınca daha güçlü çalışıyor. |
| **S-5** | **6 kategori rengi** yeterli mi? Ürün 8-10 kategoriyle çıkacaksa palet genişletilmeli. | 6 ile başla. Yeni kategori gelirse rengi brandbook'a **oranıyla** eklenir. |
| **S-6** | **Fotoğraf**: uygulama içinde hiç kullanılmaması kararı sürsün mü? (Referansta yemek fotoğrafı var; bizde harcamanın fotoğrafı yok.) | Sürsün. Faz 3 fiş fotoğrafı işlevseldir, ayrı ele alınır. |
| **S-7** | **Karanlık mod** hâlâ Faz 2 mi? | Evet (Yön C seçilirse). |
| **S-8** | Logo: monogramın **iki renkli** (T ışık + topuz amber) kullanımı onaylanıyor mu? v1.0'da logo tek renkti. | Onay öneriliyor — uygulama ikonunun 60pt'de ayrışması için renk ayrımı işe yarıyor. |

---

# BÖLÜM 9 — ARŞİV (reddedilen v1.0 yönleri)

> **Bu bölümdeki hiçbir değer uygulanmaz.** Mustafa 2026-09-11'de
> Yön A'yı reddetti (K-018/K-019). Blok, aynı tartışma yeniden
> açılmasın ve kararların izi kaybolmasın diye korunuyor.
> **v1.0'ın tam metni git geçmişindedir** (commit `6d0abcc` öncesi
> `projects/trinkow/docs/brand/brandbook.md`); burada tüm **sayısal değerler** ve
> gerekçe özetleri korunmuş, yalnızca uzun anlatım kısaltılmıştır.

## 9.1 ARŞİV — Yön A "Defter" (seçilmişti, sonra reddedildi)

**Kavram:** kağıt + mürekkep; ekran bir yüzey değil bir *sayfa*.

| Token | HEX |
|---|---|
| `bg` Kağıt | `#F4F1EA` |
| `surface` Sayfa | `#FFFDF8` |
| `line` | `#DCD5C6` · `line-strong` `#C9C0AC` |
| `text` Mürekkep | `#1B1A17` · `text-2` `#5C574C` · `text-3` `#6F6A5C` |
| `accent` **Petrol** | `#14484C` · `accent-pressed` `#0E3A3E` · `accent-soft` `#DCE7E5` |
| `edge` Kiremit | `#A24A2A` · `edge-soft` `#F3E3DB` |
| `danger` | `#8E2F20` |
| `disabled-bg` | `#E3DCCC` · `ghost-pressed` `#E9E4D8` |
| Faz 2 karanlık | `bg #191713` · `surface #221F19` · `line #33302A` · `text #EDE8DC` · `text-2 #A79F8D` · `accent #5FA79E` · `edge #D97B57` · `danger #E08472` |

**Tipografi:** Source Serif 4 (400/600) + Public Sans (400/600) — 4 dosya.
Ölçek: 44/28/20/17/16/13/13/12.
**Görsel dil:** gölge YOK · gradyan YOK · kategori rengi YOK · radius
tek kural (>32pt→12, ≤32pt→hap) · ikon Lucide 1.75 · fotoğraf ve
illüstrasyon YOK · düz yatay ilerleme çubuğu 14pt.
**Logo:** wordmark Source Serif 4 SemiBold, tracking −1.8%; monogram
"T + dikey çentik" (100×100: T cap-height 56, baseline y=78; çentik
x 66→72, y 42→78, keskin köşe); app icon zemin Petrol, monogram Kağıt.

**Neden reddedildi (2026-09-11, Mustafa):** *"Tasarımlar fazla amatör
geldi… ruhsuz bir UI/UX istemiyorum"*, *"bizim renk çok katı."*
Teknik teşhis (`projects/trinkow/docs/design/referans-analizi.md`): tek vurgu rengi +
gölgesiz düzlem + serif + düz çubuk birleşince ekranda hiyerarşi ve
derinlik oluşmadı; her öğe eşit ağırlıkta kaldı.

## 9.2 ARŞİV — Yön B "Ölçüm Aleti" (hiç seçilmedi)

**Kavram:** grafit zemin, tek yüksek görünürlüklü sinyal rengi,
karanlık öncelikli telemetri aleti.

| Token | HEX (karanlık) |
|---|---|
| `bg` Grafit | `#0E1110` · `surface` `#171B1A` · `line` `#262C2A` |
| `text` | `#E8EDEB` (16.0:1) · `text-2` `#9BA6A3` (7.6:1) |
| `accent` Sinyal Amber | `#E8A33D` (8.8:1) |
| `edge` Bakır | `#C4643C` · `danger` `#E06A55` |
| Açık mod karşılığı | `bg #F1F3F2` · `text #0E1110` · accent metin `#8A5A0B` (4.9:1) |

**Tipografi:** IBM Plex Sans (400/600) + IBM Plex Mono (500) — 3 dosya.
**Görsel dil farkı:** radius >32pt→8, ≤32pt→4 · çubuk uçları düz ·
ikon Tabler 2.0 · boş durum grafiği cetvel taksimatı.

**Not:** Yön B'nin sinyal amberi (`#E8A33D`), v2.0'ın Mandalina'sıyla
akraba bir fikirdir — ama Yön B onu **koyu zeminde** kullanıyordu ve
kişiliği "alet" idi. v2.0 aynı sıcaklığı **açık zeminde** ve "gün"
metaforuyla kullanır. Yön D bu fikrin güncellenmiş hâlidir.

---

## EK 1 — Anti-pattern uyum kontrolü

| Anti-pattern maddesi | v2.0'daki karşılığı |
|---|---|
| Mor-mavi varsayılan gradyan | Palet mor/indigo **marka rengi olarak içermiyor**; mürdüm yalnız limit dışı durumu (§3.4). Gradyan yalnız 3 yerde, **tek hue içinde** (§3.6); tam ekran gradyan ve mor-mavi gradyan açıkça yasak. |
| Her elemanda glassmorphism | Bulanık cam efekti hiçbir yerde tanımlı değil; §3.6'da açıkça yasak. |
| Amaçsız otomatik drop-shadow | Gölge **iki seviye**, yalnız yükseklik anlatan öğelerde; buton/çip/girdi/liste satırı gölge almaz (§6.2). |
| Tutarsız köşe yarıçapı | Radius eleman tipinden türer, tasarımcı seçmez: 16/24/28/999/0 (§6.3). |
| Inter/Poppins/Montserrat varsayılanı | Space Grotesk + Figtree; üçünün neden seçilmediği yazılı (§4.1). |
| 3 sütunlu "daire ikon + başlık + 1 cümle" kartı | §7.10'da ayrım kuralıyla birlikte yasak: 3'lü kutu **yalnızca gerçek veri** taşıyabilir, pazarlama metni taşıyamaz. |
| Stok illüstrasyon | §6.4'te yasak; illüstrasyon yalnız markanın kendi formlarından (yay/daire/pill). |
| Kimliksiz aşırı beyaz boşluk | Saf beyaz zemin yasak; `bg #F6F4F1` sıcak (§3.1). Ekranlarda tek kahraman öğe zorunlu (§6.1) — boşluk kimliksiz kalmıyor. |
| Jenerik pazarlama dili | §2.2/8 + §2.3 cümle kütüphanesi. |
| Düşük kontrastlı açık gri metin | Alt sınır `text-3 #6B6C75` = **4.75:1** (§3.5). |
| Rastgele boşluk değerleri | 4pt tabanlı kapalı liste (§7.0). |
| Dark mode'un ters çevirmeyle üretilmesi | Faz 1'de yok; Faz 2 için ayrı token tablosu, farklı sıcaklık, açılmış accent (§3.8). |
| Jenerik fintech sembolü | Monogram gösterge yayından türer; cüzdan/kumbara/ok/`₺` §5.6'da yasak. |
| Emoji ile ayırt edicilik | §2.6 mutlak yasak; ayrım kategori rengi + tek ikon setiyle. |

## EK 2 — Referans dili karşılama kontrolü

| Referanstaki dil (`referans-analizi.md`) | v2.0'daki karşılığı |
|---|---|
| Dairesel kahraman gösterge, kalın yay, uçta topuz | §7.5 — 200pt, 270°, 18pt, topuz zorunlu |
| Ortada çok büyük sayı, altında küçük sessiz etiket | §4.2 — `hero` 56 ↔ `label` 13, oran ≥ 4× zorunlu |
| Kartlar zeminden kalkık, yumuşak gölge | §6.2 — `elev.1` / `elev.2`, iOS + Android ayrı tarif |
| Her kategori kendi yumuşak tonunu taşıyor | §3.3 — 6 kategori, `solid` + `soft`, kontrastlar hesaplı |
| Pill etiketler, yüksek radius, daire | §6.3 radius tablosu · §7.6 pill |
| Geometrik/nötr sans, serif değil | §4.1 — Space Grotesk + Figtree |
| Yüksek kontrastlı birincil buton (siyah pill) | §7.1 — mürekkep hap, 17.34:1 |
| Yüzen alt sekme çubuğu, ortada vurgulu eylem | §7.7 — yüzen bar + 56pt amber FAB |
| Gradyanlı grafik dolgusu, ambiyans | §3.6 — 3 izinli gradyan |
| Tam genişlik fotoğraf | **Alınmadı** (§6.4, S-6): bizim içeriğimiz sayı, fotoğraf değil |
| Mor/lavanta ambiyans | **Alınmadı** — gerekçe §1.4 (Dribbble sunum estetiği + anti-pattern + rakip çakışması) |
| Emoji'li karşılama ("Welcome Back 👋") | **Alınmadı** — §2.6 emoji yasağı |

---

## Revizyon notu (2026-09-17)

> Bu revizyon **yeni bir marka yönü değildir.** v2.0'ın palet, tipografi,
> logo, görsel dil ve component kararlarına **dokunulmamıştır**; yalnızca
> 2026-09-17 tarihli ürün kararları (K-048 · K-052 · K-057) brandbook'un
> dil/metin katmanına işlenmiştir. Doküman **hâlâ TASLAK**.

| # | Ne değişti | Dayanak | Nerede |
|---|---|---|---|
| 1 | Seri (streak) ve milestone **FAZ 2'den MVP'ye** alındı; dili dört bağlayıcı kuralla ve izinli/yasak cümle tablosuyla kilitlendi. | **K-048** | §2.3 "Seri (streak) ve milestone" |
| 2 | **Puan · seviye · XP · rozet · lig** kalıcı olarak kapsam dışı ilan edildi; 8.1.6'daki "Faz 2'de yeniden açılır" ifadesi **geçersiz** kılındı. Gerekçe: gerçek gün sayısı sayılabilir, icat edilmiş birim övgü üretir (§2.2/6). | **K-048** | §2.3 sonu · §8.1.6 (bu revizyonda düzeltildi) |
| 3 | Hesap **opsiyonel** hâle geldi (Google/Apple oturumu, yalnız kimlik). "Hesap yok", "sunucu yok" ifadeleri **yanlış** ilan edildi; kullanılacak onaylı metin §2.9'a taşındı. §2.8'in yasak tablosundaki satır **öğretici karşılaştırma olarak** bilinçli bırakıldı. | **K-052** | §1.3 (TR fintech satırı) · §2.8 tablosu · §8.1.9 (bu revizyonda eklendi) |
| 4 | §2.8'e **tek istisna** eklendi: mahremiyet *kullanıcı faydası dili* ile söylenebilir ("Harcamaların telefonunda kalır."), **mimari sözcükleri** (SQLite · veri tabanı · sunucu · backend · senkron · şifreleme · token · API · bulut · JWT · önbellek) her yüzeyde yasak. İstisna yüzeyle sınırlı: pano, giriş, liste, hata, boş durum, bildirim **dışındadır**. | **K-057/1** | §2.8.1 · §2.2/11 (bu revizyonda çapraz referans verildi) · §8.1.8 |
| 5 | Mahremiyet ifadesi **tek kaynağa** bağlandı: kısa / orta / uzun (SSS) sürümler. Yeni sürüm türetilmez. Doğrulanamaz iddia ("askeri düzeyde şifreleme"), korku ve rakip karşılaştırması yasak. | **K-057/1** · K-010/5 | §2.9 |
| 6 | Sözcük kuralı: kimlik doğrulama için **"Oturum aç"**; "giriş" yalnız veri girme anlamında (harcama girişi). | **K-057/6** | §2.8.1 sonu · §2.9 |

**Bu revizyonda bilinçli olarak yapılmayanlar:**
- Renk, tipografi, logo, spacing, radius, token değerleri — **tek karakter değişmedi.**
- Gizlilik politikasının hukuki metni yazılmadı; ayrı iş kalemi (**K-057/7**). §2.9'daki SSS tablosu o metnin yerine geçmez.
- §6.6 (hareket) açılmadı: milestone kutlamasının süre sınırı (≤1.2 sn, dokunmayla atlanabilir) §2.3/2'de duruyor, §6.6'nın süre tablosuna **eklenmedi** — `ui-ux-designer` tasarım turunda bu iki yerin birleştirilmesi gerekebilir.
- §8.2'deki açık sorular (S-1…S-8) **aynen duruyor**; hâlâ Yön C/Yön D kararı bekliyor.

---

**Durum: TASLAK (v2.0) — Mustafa'nın onayı bekleniyor.**
Onay verilene kadar hiçbir UI/UX çalışması bu dokümana dayanarak
"kesinleşmiş" sayılamaz. Makine okunur karşılığı:
`projects/trinkow/docs/brand/tokens.md` (aynı gün Yön C değerleriyle güncellendi).
