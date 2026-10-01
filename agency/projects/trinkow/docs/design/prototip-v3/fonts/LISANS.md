# Font lisansları — prototip v3

| Dosya | Aile | Lisans | Kaynak |
|---|---|---|---|
| `Montserrat-Regular.ttf` | Montserrat 400 | SIL Open Font License 1.1 | Google Fonts (`ofl/montserrat`) |
| `Montserrat-SemiBold.ttf` | Montserrat 600 | SIL Open Font License 1.1 | Google Fonts (`ofl/montserrat`) |
| `Montserrat-Bold.ttf` | Montserrat 700 | SIL Open Font License 1.1 | Google Fonts (`ofl/montserrat`) |
| `Poppins-SemiBold.ttf` | Poppins 600 | SIL Open Font License 1.1 | Google Fonts (`ofl/poppins`) |

Montserrat statik kesitleri, Google Fonts'un variable dosyasından
(`Montserrat[wght].ttf`) `fontTools.varLib.instancer` ile wght=400/600/700
noktalarında üretildi. OFL türetmeye izin verir; aile adı korunmuştur.

Hepsi ücretsiz ve ticari kullanıma açıktır (K-009 uyumlu).

## Glif doğrulaması (fontTools, 2026-09-12)

| Font | `₺` U+20BA | Türkçe `ğĞıİşŞçÇöÖüÜâîû` | `tnum` |
|---|---|---|---|
| Montserrat 400/600/700 | ✅ var | ✅ tamamı var | ✅ var (+ `lnum`, `locl`) |
| Poppins SemiBold | ✅ var | ✅ tamamı var | ❌ yok |
| **JetBrains Mono** | **❌ YOK** | ✅ | ❌ |

→ **JetBrains Mono projeye alınmadı.** `₺` glifi olmadığı için para
rakamlarında kullanılamaz; mono'ya başka bir ihtiyaç da yok. Tüm rakamlar
Montserrat + `tabular-nums` ile dizilir.
→ Poppins `tnum` taşımadığı için **rakam taşıyan hiçbir metinde
kullanılmaz**; yalnız başlık (display) rolündedir.
