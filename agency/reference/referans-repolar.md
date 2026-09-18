# Referans Repo Kayıt Defteri (Design & Frontend)

`ui-ux-designer`, `design-reviewer` ve `frontend-developer` ajanlarının
kullanacağı **sabitlenmiş** kaynak listesi.

Amacı iki tane:
1. **Kalite** — ajan, rastgele blog/AI şablonu yerine sektörün gerçekten
   olgun kaynaklarına bakar.
2. **Token tasarrufu** — açık uçlu `WebSearch` (her aramada devasa sonuç
   yığını) yerine, ajan doğrudan bilinen URL'ye gider. Arama yapmak yerine
   adrese gitmek, bir görevde binlerce token fark eder.

---

## ⚠️ EN ÖNEMLİ KURAL: Bunlar şablon değil, mühendislik referansı

Buradaki design system'lerin (shadcn/ui, MUI, Ant Design, Tailwind…)
**görsel stilini kopyalamak YASAKTIR.** Sebep şu: `jenerik-ai-ui-anti-pattern-listesi.md`'de
yasaklanan "AI yapmış gibi duran arayüz" görüntüsünün birebir kaynağı
bu kütüphanelerin **varsayılan temalarıdır**. shadcn defaultları + Inter
fontu + `rounded-lg` + slate paleti = tam olarak kaçındığımız şey.

Bu repolara şunun için bakılır:
- ✅ **Sistematik** — token mimarisi, spacing/type scale mantığı, state
  yönetimi (hover/focus/disabled/loading), component API'si, isimlendirme.
- ✅ **Erişilebilirlik** — klavye davranışı, ARIA, focus tuzağı, kontrast.
- ✅ **Edge case listesi** — olgun bir sistemin düşündüğü ama bizim
  atlayacağımız durumlar (boş durum, hata durumu, uzun metin taşması).

Şunun için BAKILMAZ:
- ❌ Renk paleti seçimi → o `projects/trinkow/docs/brand/brandbook.md`'den gelir, başka yerden değil.
- ❌ Font seçimi → brandbook'tan.
- ❌ Görsel "mood", layout kompozisyonu → brandbook + tasarımcının kararı.

**Özet:** Onlardan *nasıl düşünüleceğini* al, *nasıl göründüklerini* alma.

---

## Kullanım protokolü (token disiplini)

- Bir görevde **en fazla 3-4 fetch** yap. Daha fazlası gerekiyorsa
  muhtemelen yanlış soruyu soruyorsun.
- Repo ana sayfasını çekme — **doğrudan ilgili dosyayı** çek.
  `raw.githubusercontent.com/<repo>/<branch>/<dosya>` formatı, HTML
  gürültüsü olmadığı için repo sayfasından kat kat ucuzdur.
- Aynı oturumda aynı kaynağı iki kez çekme. Çektiğini 3-5 satır özetle,
  sonra ham içeriği bir daha referans alma.
- Buradaki listede cevabı olmayan bir ihtiyaç varsa, ancak o zaman
  `WebSearch` kullan — ve bulduğun kaynak kaliteliyse PM'e bildir,
  bu dosyaya eklensin (liste zamanla zenginleşsin).
- Link ölürse (404) uğraşma, PM'e bildir, listeden düşülsün.

> Aşağıdaki tüm repolar 2026-09-09'da erişilebilir olarak doğrulandı.

---

## 1. Design system mimarisi — "nasıl kurgulanır?"

Token yapısı, component API'si, varyant mantığı için.

| Repo | Ne için bakılır |
|---|---|
| `primer/design` | GitHub'ın tasarım sistemi. Yazılı **karar gerekçeleri** çok güçlü — "neden böyle" sorusunun cevabı var. |
| `carbon-design-system/carbon` | IBM. Token katmanlaması ve erişilebilirlik dokümantasyonu sektör standardı. |
| `shopify/polaris` | Ticari/ürün arayüzü kalıpları, içerik-yazımı (UX writing) rehberi çok iyi. |
| `adobe/react-spectrum` | Erişilebilirlik ve etkileşim davranışında referans kalite (özellikle `react-aria`). |
| `salesforce-ux/design-system` | Yoğun, veri ağırlıklı kurumsal arayüz kalıpları. |
| `alexpate/awesome-design-systems` | Yukarıdakiler yetmezse: sektörden design system dizini. |
| `mui/material-ui`, `ant-design/ant-design` | Sadece **component kapsamı/edge case** kontrolü için. Görsel dilleri güçlü ve tanınır → kopyalanırsa marka ölür. |

## 2. CSS token & temel altyapı

| Repo | Ne için bakılır |
|---|---|
| `argyleink/open-props` | CSS değişkeni olarak hazır scale'ler (spacing, size, easing, shadow). Değerleri körü körüne alma; **ölçek mantığını** al. |
| `necolas/normalize.css` | Tarayıcı farklarını sıfırlama. |
| `picocss/pico` | Minimal, class'sız semantik CSS — sade projelerde iskelet. |
| `tailwindlabs/tailwindcss` | Utility yaklaşımı ve scale mantığı. **Varsayılan paleti/fontu kullanma** (anti-pattern). |

## 3. CSS teknik & layout

| Repo | Ne için bakılır |
|---|---|
| `phuocng/csslayout` | Yaygın layout kalıplarının saf CSS çözümleri. |
| `AllThingsSmitty/css-protips` | Pratik CSS teknikleri. |
| `l-hammer/You-need-to-know-css` | Sık karşılaşılan CSS tuzakları. |
| `chokcoco/iCSS` | İleri seviye CSS efektleri — jenerik gradyana sapmadan karakter katmak için. |
| `mdn/content` | Herhangi bir CSS/HTML özelliğinin otoritesi. Spesifik sayfayı çek. |

## 4. Erişilebilirlik (WCAG AA zorunlu)

| Repo | Ne için bakılır |
|---|---|
| `w3c/wcag` | Kural metninin kaynağı. |
| `dequelabs/axe-core` | Otomatik denetim motoru; kural listesi "neyi kaçırdım" kontrol listesi olarak birebir. |
| `ffoodd/a11y.css` | Yaygın erişilebilirlik hatalarını görünür kılan CSS katmanı. |
| `thedaviddias/Front-End-Checklist` | Yayın öncesi genel kontrol listesi. |

## 5. Tipografi

| Repo | Ne için bakılır |
|---|---|
| `system-fonts/modern-font-stacks` | **Öncelikli kaynak.** Sıfır yükleme maliyetli, karakterli sistem font yığınları — Inter/Poppins tuzağından çıkışın en kolay yolu. |
| `google/fonts` | Lisansı net, geniş arşiv. Font seçimi brandbook'ta gerekçelendirilmiş olmalı. |
| `fontsource/font-files` | Fontu self-host etmek için (gizlilik + performans). |
| `IBM/plex`, `JetBrains/JetBrainsMono`, `githubnext/monaspace` | Karakterli, az yıpranmış alternatifler. |
| `rsms/inter` | Kalitesi yüksek ama **aşırı kullanılmış**. Anti-pattern listesinde: ancak brandbook'ta yazılı bir gerekçe varsa. |

## 6. İkonografi

| Repo | Ne için bakılır |
|---|---|
| `lucide-icons/lucide` | Dengeli, geniş, tutarlı. Genel amaçlı ilk tercih. |
| `tabler/tabler-icons` | Çok geniş set, ince çizgi. |
| `feathericons/feather` | Minimal; Lucide'ın atası. |
| `twbs/icons` | Dolgu + çizgi varyantları bir arada. |
| `tailwindlabs/heroicons` | Yaygın → tanınabilirlik riski var. |
| `simple-icons/simple-icons` | Marka/logo ikonları (sosyal medya vb.). |

**Kural:** Tek bir set seç ve sonuna kadar ona sadık kal. Setleri karıştırmak
amatörlüğün en görünür işaretidir — çizgi kalınlıkları tutmaz.

## 7. Hareket / animasyon

| Repo | Ne için bakılır |
|---|---|
| `motiondivision/motion` | (eski adı `framer/motion`) Modern animasyon; ikisi de canlı. |
| `animate-css/animate.css` | Hazır efektler. Dikkat: varsayılanları çok tanıdık, ölçülü kullan. |

**Kural:** Animasyon dekorasyon değil, **anlam** taşımalı (durum değişimi,
yön, hiyerarşi). `prefers-reduced-motion` desteği zorunlu.

## 8. Performans

| Repo | Ne için bakılır |
|---|---|
| `GoogleChrome/web-vitals` | LCP/CLS/INP ölçümü. |
| `uncss/uncss` | Kullanılmayan CSS tespiti. |

## 9. Genel dizinler (son çare)

| Repo | Ne için bakılır |
|---|---|
| `bradtraversy/design-resources-for-developers` | Geniş kaynak dizini. |
| `goabstract/Awesome-Design-Tools` | Tasarım aracı dizini. |
| `catppuccin/catppuccin`, `dracula/dracula-theme` | Sadece **çok-yüzeyli palete tutarlı uygulanışını** incelemek için. Paletlerini alma. |

## 10. Alan-bazlı (SADECE proje o alandaysa)

Bunlar global listeye dahil değil — `proje-kurulum-checklist.md` → **P-5**
adımında, proje o alana giriyorsa projeye özel referans setine eklenir.
Hepsini birden taşıma; projenin ihtiyacı olmayan kategori maliyettir.

**Veri görselleştirme / dashboard**

| Repo | Ne için bakılır |
|---|---|
| `observablehq/plot` | Grafik grameri; "hangi veri hangi grafik" kararı için en iyi başlangıç. |
| `d3/d3` | Tam kontrol gerektiğinde. Maliyeti yüksek, gerçekten gerekiyorsa. |
| `apache/echarts` | Hazır, geniş grafik seti; büyük veri setlerinde iyi. |
| `chartjs/Chart.js` | Basit ihtiyaçlar için hafif çözüm. |
| `plotly/plotly.js` | Bilimsel/analitik grafikler. |

**Veri tabloları**

| Repo | Ne için bakılır |
|---|---|
| `TanStack/table` | Sıralama/filtreleme/sayfalama/sanallaştırma mantığı. Headless — görsel stil dayatmaz, bizim için ideal. |

**Form ağırlıklı ürünler**

| Repo | Ne için bakılır |
|---|---|
| `react-hook-form/react-hook-form` | Doğrulama, hata durumu ve erişilebilir hata mesajı kalıpları. |

**İçerik / editör / metin**

| Repo | Ne için bakılır |
|---|---|
| `ueberdosis/tiptap` | Zengin metin editörü mimarisi. |
| `markdown-it/markdown-it` | Markdown işleme. |
| `tailwindlabs/tailwindcss-typography` | Uzun metin (makale/blog) tipografi ölçeği referansı. |
| `cure53/DOMPurify` | Kullanıcı içeriği gösteriliyorsa **zorunlu** (XSS). |

**Takvim / zaman**

| Repo | Ne için bakılır |
|---|---|
| `fullcalendar/fullcalendar` | Takvim/planlama arayüz kalıpları. |
| `date-fns/date-fns` | Tarih işlemleri ve yerelleştirme (TR formatları). |

**Harita**

| Repo | Ne için bakılır |
|---|---|
| `maplibre/maplibre-gl-js` | Açık kaynak harita; stil tamamen özelleştirilebilir (marka uyumu için önemli). |

**Diğer**

| Repo | Ne için bakılır |
|---|---|
| `nolimits4web/swiper` | Karusel/slider. Dikkat: karusel çoğu zaman yanlış çözümdür, önce gerekliliğini sorgula. |
| `Kozea/WeasyPrint` | HTML'den PDF (fatura, rapor çıktısı). |

---

---

## İlham kaynakları (repo değil, site)

Rakip/ilham analizi bu sitelerden yapılır — Dribbble'ın "trend" AI şablonları
veya jenerik template pazarlarından DEĞİL:

- `godly.website` — gerçekten iyi tasarlanmış canlı siteler
- `land-book.com` — landing page arşivi
- `siteinspire.com` — küratörlü, editoryal ağırlıklı
- `mobbin.com` — gerçek ürün akışları (ekran ekran)
- `fontsinuse.com` — tipografinin gerçek hayatta kullanımı
- `refactoringui.com` — pratik görsel karar rehberi (kitap)

**Kural:** İlhamı **gerçek markalardan** al, tek bir kaynağı taklit etme.
Bir tasarımın "neden iyi olduğunu" yaz, sonra o ilkeyi kendi markamıza uygula.
