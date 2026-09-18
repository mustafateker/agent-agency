# Trinkow — Projeye Özel Referans Seti (P-5)

> Global liste (`agency/reference/referans-repolar.md`) budandı ve bu ürüne
> göre daraltıldı. **Bu dosyada 12 kalem vardır, artırılmaz.**
> Bir ajan bir görevde en fazla **3-4 fetch** yapar.
>
> **EN ÖNEMLİ KURAL — istisnasız:**
> Buradan **sistematik** alınır (davranış, durum listesi, erişilebilirlik,
> kenar durumları, isimlendirme). **Görsel stil alınmaz.**
> Renk, font, radius, boşluk **yalnızca** `projects/trinkow/docs/brand/tokens.md`'den gelir.
> Bir referansın ekran görüntüsüne bakıp düzen kopyalamak REVİZE sebebidir.
>
> Neden bu daraltma: Trinkow **form ağırlıklı giriş + basit veri
> gösterimi** olan bir üründür. Ağır dashboard, harita, takvim ızgarası,
> veri tablosu, zengin metin editörü **yoktur** → o kategorilerin tamamı
> (d3, echarts, TanStack/table, maplibre, fullcalendar, tiptap, swiper)
> bilinçli olarak **dışarıda bırakıldı.**
> Tarih: 2026-09-10

---

## A. Sistem ve davranış referansları (7)

| # | Kaynak | Neden bu projede | Ne ALINIR | Ne ALINMAZ |
|---|---|---|---|---|
| 1 | `primer/design` | Yazılı karar gerekçeleri güçlü; bileşen isimlendirme ve varyant mantığı için. | Bileşen adlandırma disiplini, "neden bu varyant var" sorgusu | GitHub'ın paleti, tipografisi, ikonografisi |
| 2 | `adobe/react-spectrum` (özellikle `react-aria`) | **Dokunmatik etkileşim modeli.** Hover'ı olmayan bir arayüzde `press` durumunun nasıl doğru kurulacağı burada en iyi belgelenmiş. | `usePress` davranışı: parmak dışarı kayınca durumun geri dönmesi, uzun basma, çift tetikleme koruması | Spectrum görsel dili, kendi tema sistemi |
| 3 | `shopify/polaris` | **UX writing rehberi.** Hata, boş durum ve onay metinlerinin yapısal kalıpları. | Metin *yapısı* (başlık + tek satır + eylem), buton etiketi disiplini | İngilizce ton, "friendly" ses — bizim tonumuz `brandbook.md` §2'dir |
| 4 | `carbon-design-system/carbon` | Durum listelerinin en olgun dökümantasyonu (boş / yükleniyor / hata / kısmi veri). | Hangi durumun tasarlanması gerektiği kontrol listesi, iskelet (skeleton) kullanım kuralları | IBM Plex, Carbon paleti, ızgara sistemi |
| 5 | `react-hook-form/react-hook-form` | Ürün form ağırlıklı: tutar, limit, taksit. | Doğrulama zamanlaması (blur mü submit mi), erişilebilir hata bağlama (`aria-describedby` → RN karşılığı `accessibilityHint`) | Web API'si birebir; RN'de `Formik`/RHF kullanımı ayrı karardır |
| 6 | `date-fns/date-fns` | **Gün sınırı ve saat dilimi** (F-15) bu üründe iş mantığıdır: gün 00.00'da mı 03.00'te mi biter. | Yerel gün başlangıcı, hafta başlangıcı (TR: Pazartesi), yaz saati kenar durumları, `tr` yerelleştirmesi | Biçimlendirme çıktısını körü körüne kullanma — biçim `metinler.md` §18'de sabit |
| 7 | `dequelabs/axe-core` | WCAG AA denetimi için "neyi kaçırdım" listesi. | Kural adları kontrol listesi olarak: kontrast, isimlendirilmemiş buton, odak sırası | Web DOM'una özgü kurallar (RN'de karşılığı yok) |

---

## B. İlham — gerçek ürünler (5)

> İlham **canlı ve iyi tasarlanmış gerçek ürünlerden** alınır; şablon
> pazarlarından, "AI dashboard" koleksiyonlarından değil.
> Her kalemde "neden iyi" yazılıdır — o ilke bizim markamıza uygulanır,
> ekranı taklit edilmez.

| # | Ürün | Neden iyi (alınacak ilke) | Bizde nasıl uygulanır | ALINMAZ |
|---|---|---|---|---|
| 8 | **MyFitnessPal** (myfitnesspal.com) | Ürünün doğrudan davranışsal analoğu: "kalan kalori" tek sayı + hızlı ekleme. Günde 3-5 kez tekrarlanan girişte sürtünmeyi sıfıra yaklaştırmış (son yenenler, tek dokunuşla tekrar). | "Tekrarla" akışı (E-11, 2 dokunuş) ve kahraman sayı hiyerarşisi | Reklam yoğunluğu, mavi/turuncu paleti, halka grafikler, oyunlaştırma |
| 9 | **Copilot Money** (copilot.money) | Finansal veriyi *sakin* sunmanın örneği: büyük tipografi, az renk, grafik yerine sayı. "Ciddi ama ezici değil" dengesi tam bizim boşluğumuz. | Sayı → boşluk → renk sıralaması (brandbook §6.1) | Koyu tema, degrade vurgular, kart gölgeleri, marka renkleri |
| 10 | **Monzo** (monzo.com) | Harcama listesi satırının bilgi yoğunluğu: ne, ne kadar, ne zaman — tek satırda, kategori rengine ihtiyaç duymadan okunur. | `SpendRow` sütun yapısı ve 56pt içerden başlayan ayraç | Mercan/turuncu marka rengi, yuvarlak avatar/logolar, kategori renkleri |
| 11 | **YNAB** (ynab.com) | Zihinsel muhasebenin en olgun ürün karşılığı; kategori limiti kavramını kullanıcıya *sistem* olarak anlatır. | Kategori limiti dili ve "limit gerçekçi mi" çerçevesi (E-17, `metinler.md` §9) | Katı/öğretici tonu, kural yükü, yoğun tablo düzeni, mor-mavi paleti |
| 12 | **Things 3** (culturedcode.com/things) | Hızlı giriş tasarımının ölçütü: klavye açılır açılmaz odak doğru alanda, tek birincil eylem, gereksiz alan sonradan açılır. | E-11'in 3 dokunuş bütçesi ve "isteğe bağlı alanlar gizli" kararı | Mavi vurgu rengi, iOS varsayılan tipografisi, kendi ikonografisi |

---

## C. Bilinçli olarak listede OLMAYANLAR

| Kaynak | Neden yok |
|---|---|
| `tailwindcss`, `shadcn/ui`, `mui`, `ant-design` | Varsayılan temaları tam olarak kaçındığımız "AI yapmış" görünümün kaynağı. Bileşen kapsamı kontrolü için bile gerek yok; kapsamımız `bilesen-envanteri.md`'de kapalı. |
| `d3`, `echarts`, `Chart.js`, `plotly` | Faz 1'de tek "grafik" hairline `WeekStrip`. Kütüphane hem ücretsiz-ama-ağır hem de görsel dili dayatır. |
| `TanStack/table` | Veri tablosu yok. |
| `fullcalendar` | Takvim ızgarası yok. |
| `maplibre` | Konum yok. |
| `framer/motion`, `animate.css` | Animasyon bütçesi 3 süreyle kapalı (tokens.md §8); kütüphane gereksiz. |
| `rsms/inter`, `modern-font-stacks` | Tipografi kilitli (Source Serif 4 + Public Sans). |
| Dribbble / template pazarları | Anti-pattern listesi gereği yasak. |

---

## D. Fetch protokolü (token disiplini)

- Repo ana sayfasını **çekme**; doğrudan ilgili dosyayı çek
  (`raw.githubusercontent.com/<repo>/<branch>/<yol>`).
- Aynı oturumda aynı kaynağı iki kez çekme; çektiğini 3-5 satırda özetle.
- Bu listede cevabı olmayan bir ihtiyaç çıkarsa: önce
  `projects/trinkow/docs/brand/tokens.md` ve `projects/trinkow/docs/design/bilesen-envanteri.md`'ye bak.
  Orada da yoksa PM'e sor — açık uçlu `WebSearch` son çaredir.
