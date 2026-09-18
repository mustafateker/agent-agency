# React Native Tasarım Kısıtları

`ui-ux-designer`, `design-reviewer` ve `frontend-developer` için **bağlayıcı**
liste. Amaç tek: tasarımcının web alışkanlığıyla **React Native'de inşa
edilemeyecek** bir şey üretmesini engellemek.

Bu dosya bir revizyon turunu önlemek için var. Bir revizyon turu (tasarla →
denetle → REVİZE → yeniden tasarla) bu listeyi okumaktan kat kat pahalıdır.

---

## Prototip nasıl üretilecek?

Tasarım prototipi yine **HTML/CSS** olarak üretilir — hızlı açılır,
`design-reviewer` `grep` ile denetleyebilir. **AMA** aşağıdaki kısıtlara
uyularak yazılır, yani "RN'e çevrilebilir HTML" olur.

Prototip kuralları:
- Viewport **390 × 844** (iPhone 14/15 referansı). Masaüstü genişliğinde
  tasarım yapma.
- Sadece bu listeye uyan CSS özelliklerini kullan.
- Her ekranı ayrı bir bölüm/dosya olarak ver.

---

## ❌ KULLANILAMAZ (RN'de karşılığı yok)

| Web'de yaptığın | RN'de durum | Bunun yerine |
|---|---|---|
| **`:hover`** | **YOK** — dokunmatik ekranda hover diye bir şey yok | `pressed` (basılı) durumu tasarla |
| CSS Grid | Yok | Flexbox |
| `float`, `position: sticky` | Yok | Flexbox / `position: absolute` |
| `::before`, `::after` | Yok | Gerçek bir element ekle |
| CSS kalıtımı (cascade) | Yok — her element kendi stilini alır | Stilleri açıkça ver; metin stilleri sınırlı kalıtır |
| Global CSS / class'lar | Yok | `StyleSheet` nesneleri, tema dosyası |
| `gap` (eski RN'lerde) | Kısmi | Aralarına boşluk elemanı veya margin |
| `vh` / `vw` / `%` (her yerde) | Kısıtlı | `Dimensions` / flex oranları |
| CDN'den webfont | Yok | Font dosyası uygulamaya **gömülür** |
| `calc()` | Yok | JS ile hesapla |
| SVG doğrudan | Yok | `react-native-svg` bileşenleri |
| `overflow: scroll` | Yok | `ScrollView` / `FlatList` |
| `z-index` oyunları | Güvenilmez | Eleman **sırası** belirleyici |
| `transition` (CSS) | Yok | `Animated` / `Reanimated` |
| `box-shadow` (tek kural) | Platforma göre değişir | ↓ aşağıya bak |

## ⚠️ PLATFORMA GÖRE DEĞİŞİR

- **Gölge:** iOS `shadowColor/shadowOffset/shadowOpacity/shadowRadius`,
  Android `elevation`. Aynı görsel sonucu vermezler. Tasarımda gölgeye
  **kritik bir anlam yükleme**; katman ayrımını kenarlık/arka plan tonuyla
  da destekle.
- **Yazı tipi ölçümü** iOS/Android'de birkaç piksel oynar. Metni piksele
  kilitli kutulara sıkıştırma, esneme payı bırak.
- **Klavye** açılınca ekranı iter. Form ekranlarında klavye açıkken hâlâ
  görünmesi gereken elemanı (ör. "Kaydet" butonu) belirt.
- **Geri hareketi:** iOS'ta soldan kaydırma. Sol üst köşeye kritik bir
  dokunmatik hedef koyma.

## ✅ ZORUNLU

- **Safe area:** Üstte çentik/Dynamic Island, altta home indicator var.
  İçerik bunların altında kalmamalı. Tasarımda güvenli alanı işaretle.
- **Dokunma hedefi minimum 44×44 pt** (iOS HIG) / 48 dp (Android).
  Küçük ikon butonları görsel olarak küçük olabilir ama dokunma alanı
  büyük olmalı.
- **Her etkileşimli eleman için `pressed` durumu.** Hover olmadığı için
  kullanıcının tek geri bildirimi budur. Tasarlanmazsa uygulama "ölü" hisseder.
- **Uzun listeler `FlatList`** ile — harcama listesi büyüyecek, hepsini
  birden render etme.
- **Erişilebilirlik:** ARIA yok. Karşılığı `accessibilityLabel`,
  `accessibilityRole`, `accessibilityState`. Tasarımda her ikon-butonun
  sesli okunacak etiketini yaz.
- **Fontlar gömülür:** Seçilen font ailesinin dosyaları projeye eklenir.
  Bu yüzden **ağırlık sayısını sınırlı tut** (2-3), her ağırlık uygulama
  boyutunu büyütür.
- **Karanlık mod** yapılacaksa ayrıca tasarlanır (renkleri ters çevirme).

---

## Bu ürüne özel notlar

- **İlerleme çubuğu ("kalori çubuğu")** ürünün kalbi. `react-native-svg`
  ile çizilecek. Tasarımda kesin geometri ver: kalınlık, uç yuvarlaklığı,
  dolum yönü, %100'ü aşınca ne oluyor (renk değişimi? taşma göstergesi?).
- **Harcama girişi ekranı** en çok kullanılan ekran. Klavye açıkken tam
  akış çalışmalı: sayısal klavye, kategori seçimi, kaydet — **kaç dokunuşta
  bitiyor?** Bu sayıyı tasarımda açıkça yaz, hedef mümkün olan en az.
- **Para gösterimi:** TL, binlik ayracı, kuruş. Uzun tutarların (ör.
  1.250.000,50 ₺) taşmadığını tasarımda göster.
- **Boş durumlar** kritik: ilk gün hiç harcama yok. "Henüz veri yok" demek
  yetmez; kullanıcıyı ilk girişe yönlendiren bir ekran tasarla.
- **Limit aşımı** durumu suçlayıcı olmamalı (marka tonu: farkındalık veren,
  utandıran değil). Kırmızı + ünlem refleksine kapılma.
