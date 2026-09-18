# open-design (Claude Design) Entegrasyon Kuralları

Kaynak: `github.com/nexu-io/open-design` — Apache-2.0, ücretsiz (K-009 uyumlu).
Yerel kopya: `agency/vendor/open-design/` (ağdan tekrar çekme, orası yeterli).

Mustafa: *"claude design'i kullan işte mobil tasarım için."*

```
agency/vendor/open-design/
├── mobile-app/
│   ├── SKILL.md                  ← iş akışı
│   ├── assets/template.html      ← iPhone 15 Pro çerçevesi + ekran ilkelleri
│   └── references/
│       ├── layouts.md            ← 6 ekran arketipi (Feed/Detail/Onboarding/Profile/Checkout/Focus)
│       └── checklist.md          ← P0/P1/P2 öz-denetim
├── _schema/{AGENTS.md,defaults.css}
└── LICENSE
```

---

## Neden kullanıyoruz

Önceki prototip "amatör" bulundu. Bu şablonun getirdiği ve bizde eksik olan şey
**sunum kalitesi**: gerçek iPhone çerçevesi, Dynamic Island, SVG durum çubuğu
ikonları, home indicator. Ekran aynı kalsa bile, çıplak 390×844 kutu yerine
gerçek bir telefonun içinde görünmesi profesyonellik algısını doğrudan değiştirir.

Ayrıca değerli: 6 ekran arketipi, dokunma hedefi/gerçek metin/emoji disiplini
içeren P0 kontrol listesi.

---

## ⚠️ ÇATIŞMA VE ÇÖZÜMÜ — en önemli bölüm

Şablon **web için** yazılmış. Bizim prototipimizin **React Native'e
çevrilebilir** kalması gerekiyor. Şablonda RN'de karşılığı olmayan CSS var:
`grid` (13 kez), `::before`/`::after` (7 kez), `z-index`, `backdrop-filter`,
`box-shadow`, `gradient`.

### ÇÖZÜM: Çerçeve ile ekran içeriğini AYIR

Bu ayrım bağlayıcıdır ve `design-reviewer` buna göre denetler.

**A) ÇERÇEVE / KABUK — CSS serbest**
Telefon gövdesi, Dynamic Island, durum çubuğu, home indicator, yan raylar,
sayfa arka planı, cihazın üstündeki başlık.
→ Bunlar **asla React Native'e kodlanmayacak.** Sadece sunum. `grid`,
`::before`, `backdrop-filter`, `z-index` — hepsi serbest. Şablonu olduğu
gibi kullan, yeniden yazma.

**B) EKRAN İÇERİĞİ (`<main class="content">` içi) — RN kuralları GEÇERLİ**
Gerçek ürün burası; birebir React Native'e kodlanacak.
→ `grid` YOK · `::before`/`::after` YOK · `position:sticky` YOK · `float` YOK ·
`calc()` YOK · `vh`/`vw` YOK · `z-index` oyunu YOK · `:hover` YOK (pressed var).
→ Sadece flexbox.
→ **Gölge ve gradyan artık SERBEST** (K-019) — ama RN'de nasıl karşılanacağı
yazılacak: gölge iOS `shadowColor/Offset/Opacity/Radius`, Android `elevation`;
gradyan `expo-linear-gradient` veya `react-native-svg`.

**Denetim kuralı:** `design-reviewer` yasak CSS taramasını **yalnızca
`<main class="content">` bloğu içinde** yapar. Çerçevede bulması ihlal değildir.

---

## Şablonun kurallarından SAPTIKLARIMIZ

Şablonun kendi kuralları var; bazıları bizim marka kararlarımızla çelişiyor.
Aşağıdakiler **bilinçli sapmadır**, denetimde ihlal sayılmaz.

| Şablon diyor | Biz ne yapıyoruz | Gerekçe |
|---|---|---|
| "Display başlıkları **serif** olsun, sans'a çevirme, yoksa stok şablon gibi durur" | Yeni brandbook ne diyorsa o (muhtemelen **geometrik sans**) | Uyarı *sistem* sans'ı (SF/Helvetica varsayılanı) içindir. Bilinçli seçilmiş karakterli bir sans başka şeydir. Karar brandbook'un. |
| "**Tek accent**, ekranda en fazla 2 kez" | 1 birincil accent (eylemler için, ≤2 kez) **+ işlevsel kategori tonları** | Kategori renkleri K-019'da serbest bırakıldı ve **bilgi taşıyor** (dekorasyon değil). Küçük pill'lerde kullanılır, "accent bütçesi"ne sayılmaz. |
| "Sayılar **mono** font" | Brandbook'un tabular rakam kararı | Mono zorunlu değil; tabular hizalama şartı yeterli. |
| "Tek ekran, tek iş — akış birleştirme" | **Uyulacak.** Her ekran ayrı dosya. | Zaten ekran envanterimiz böyle. |
| `<artifact>` etiketiyle çıktı ver | **Dosyaya yaz** (`projects/trinkow/docs/design/prototip/`) | Bizim akışımız dosya tabanlı, sohbet artifact'ı değil. |
| "Harici görsel yok, `.ph-img` kullan" | **Uyulacak.** | Zaten stok görsel yasağımız var. |

## Şablonun UYACAĞIMIZ kuralları (bizimkilerle örtüşüyor)

- Dokunma hedefi **≥44px** — bizde de zorunlu.
- **Gerçek, spesifik metin** ("1.250,50 ₺" > "X.XXX ₺") — bizim lorem yasağımız.
- **UI'da emoji yok, sadece SVG monoline ikon** — K-004 ile birebir aynı.
- Gövde metni **≥14px**.
- İçerik kayar, çerçeve kaymaz.
- Durum çubuğunda gerçek SVG ikonlar, saat `9:41`.
- **İlk ekranda birincil eylem katlamanın üstünde** olsun.

---

## Arketip eşleştirmesi (Trinkow ekranları)

`references/layouts.md`'deki 6 arketipten hangisi hangi ekranımıza:

| Trinkow ekranı | Arketip | Not |
|---|---|---|
| Bugün / pano | **F — Focus / hero card** | Dairesel kahraman gösterge tam buraya oturuyor |
| Harcama ekle | **E — Checkout / form** | Tab bar düşürülür |
| Onboarding (3 adım) | **C — Onboarding (1 of N)** | "Adım 1/3" göstergesi zaten var |
| Kayıtlar | **A — Feed** | Tab bar kalır |
| Özet | **F** veya **A** | Grafik ağırlıklıysa F |
| Ayarlar | **E** | Form/liste |
| Harcama detayı | **B — Detail** | Tab bar düşürülür |

---

## Kullanım sırası (ui-ux-designer için)

1. `agency/vendor/open-design/mobile-app/assets/template.html`'i **baştan sona oku**
   (`<style>` bloğu dahil). Çerçeveyi yeniden yazma.
2. `references/layouts.md`'yi oku — 6 arketipi tanı.
3. Yeni `projects/trinkow/docs/brand/tokens.md`'yi oku, şablonun `:root` değişkenlerini
   **bizim tokenlarımızla** değiştir.
4. Ekran başına: uygun arketipi seç, `<main class="content">` içine koy,
   **gerçek Türkçe metinle** (`projects/trinkow/docs/content/metinler.md`) doldur.
5. `references/checklist.md` P0'ı geç + bizim anti-pattern listemizi geç.
6. Ekran içeriğinde yasak CSS kullanmadığını kendin grep'le.
