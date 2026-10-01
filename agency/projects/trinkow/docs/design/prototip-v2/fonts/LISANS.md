# Font lisansları — Trinkow prototip v2

Bu klasördeki üç dosya **gömülü uygulama fontudur** (CDN'den çekilmez).
Üçü de SIL Open Font License 1.1 (OFL) altındadır: ticari kullanım,
uygulamaya gömme ve dağıtım serbesttir. **Ücretli bileşen yoktur.**

| Dosya | Aile / kesim | Telif | Lisans |
|---|---|---|---|
| `SpaceGrotesk-Bold.ttf` | Space Grotesk Bold (700) | Copyright (c) 2018 Florian Karsten | SIL OFL 1.1 |
| `Figtree-Regular.ttf` | Figtree Regular (400) | Copyright (c) 2022 Erik Kennedy | SIL OFL 1.1 |
| `Figtree-SemiBold.ttf` | Figtree SemiBold (600) | Copyright (c) 2022 Erik Kennedy | SIL OFL 1.1 |

Kaynak: `@expo-google-fonts/space-grotesk` ve `@expo-google-fonts/figtree`
paketlerinin dağıttığı **statik** TTF'ler (Google Fonts deposu).
Lisans metinlerinin tamamı: <https://openfontlicense.org>

## Neden variable font yok

`projects/trinkow/docs/brand/tokens.md` §2.1 variable font kullanımını yasaklar. Gerekçe:
React Native'in variable font desteği platformlar arasında tutarsızdır —
uygulamada ara ağırlıklar yanlış ya da hepsi tek ağırlık olarak render
edilebilir. Ağırlık **dosya seçimiyle** gelir; `fontWeight` sayısıyla
ara ağırlık üretilmez. Prototip ile uygulama aynı görünmek zorunda.

## Glif denetimi (2026-09-11, fontTools ile ölçüldü)

Test dizisi: `ğ Ğ ı I i İ ş Ş ç Ç ö Ö ü Ü â î û` + `₺` + `0-9 . , -`

| Dosya | Türkçe karakterler | `₺` | Rakamlar |
|---|---|---|---|
| `SpaceGrotesk-Bold.ttf` | tam | **var** | tam, tabular |
| `Figtree-Regular.ttf` | tam | **yok** | tam |
| `Figtree-SemiBold.ttf` | tam | **yok** | tam |

**Sonuç: Figtree'de `₺` glifi yoktur.** tokens.md §2.3 bu durumu
öngörmüştür. Kural:

- Web prototipinde `--font-ui: 'Figtree', 'Space Grotesk', sans-serif`
  sıralaması `₺` karakterini kendiliğinden Space Grotesk'ten alır.
- **React Native'de font fallback yoktur.** `₺` içeren her metin ya
  Space Grotesk ile dizilir, ya da `₺` ayrı bir `<Text>` içinde
  Space Grotesk verilerek yazılır. Zaten tüm tutarlar Space Grotesk
  kullandığı için pratikte tek istisna, gövde cümlesi içinde geçen
  tutarlardır (ör. "Bugün 180 ₺ harcadın") — orada `₺` ve sayı ayrı
  `<Text>` olur.
- `TL` yazımı hiçbir yüzeyde kullanılmaz.

Dosya sayısı **3'tür ve artırılamaz** (tokens.md §2.1); yeni kesim
eklemek Mustafa onayı gerektirir.
