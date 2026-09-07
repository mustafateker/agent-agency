# ai-ajans — Proje Talimatları

Bu repo, "PM ajanı + aşamalara göre devreye giren uzman alt-ajanlar"
sistemiyle proje dökümantasyonundan profesyonel, markalı bir ürün üreten
bir pilot sistemdir.

## Aşama modeli
Ajanlar rastgele/hepsi-birden değil, `status/STAGE.md`'de tanımlı sırayla
devreye girer: Keşif → Marka → UI/UX Tasarım → Geliştirme → Kalite →
DevOps/Yayın; Büyüme/Sosyal Medya aşaması Marka onayından sonra diğerleriyle
paralel ilerleyebilir. Detaylar ve her aşamanın çıkış kriteri
`status/STAGE.md`'de.

## Diller / Standartlar
- Backend / iş mantığı / otomasyon kodu: **Python**.
- Frontend/UI kodu: onaylanmış tasarıma sadık kalmak kaydıyla uygun web
  teknolojisi (HTML/CSS/JS; gerekirse bir framework) — saf Python'a
  zorlanmaz, çünkü modern/profesyonel UI genelde bunu gerektirir.
- Kod okunabilir, tip belirteçli (Python: type hints) ve test edilebilir
  olmalı. Her yeni backend özelliği için pytest testi eklenmeli.

## Tasarım kalite standardı
Bu sistemin en önemli kuralı: UI/UX çıktıları "bir yapay zekanın yaptığı
belli olan" jenerik görünümde OLMAYACAK. Bunun için:
- Hiçbir UI/UX çalışması, önce `docs/brand/brandbook.md` onaylanmadan
  başlamaz (bkz. Aşama 1 → 2 geçiş kuralı).
- Her tasarım `docs/design/jenerik-ai-ui-anti-pattern-listesi.md`'ye göre
  `design-reviewer` tarafından denetlenir.

## Klasörler
- `docs/`         — İnsan (Mustafa) tarafından yazılan proje dökümanları.
- `docs/brand/`   — Brandbook ve marka çalışmaları.
- `docs/design/`  — UI/UX tasarımları/prototipler + anti-pattern listesi.
- `docs/social/`  — Sosyal medya içerik takvimi ve analiz raporları.
- `status/STATUS.md`   — Güncel ilerleme ve kaldığı yer.
- `status/STAGE.md`    — Aşama tanımları ve mevcut aşama.
- `status/BACKLOG.md`  — Görev kırılımı ve durumları.
- `status/DECISIONS.md`— Onay bekleyen/verilmiş kararlar.
- `src/`   — Üretilen kod (backend Python, frontend ilgili alt klasörde).
- `.claude/agents/` — Alt-ajan tanımları.

## Onay gerektiren işlemler
Aşağıdakiler İÇİN HER ZAMAN önce `status/DECISIONS.md`'ye yazılıp
Mustafa'nın onayı beklenir, otomatik yapılmaz:
- Brandbook'un nihai onayı (Aşama 1 → 2 geçişi)
- UI/UX tasarımının son onayı (Aşama 2 → 3 geçişi)
- Yeni bir ücretli servis/API/kütüphane bağımlılığı eklemek
- Var olan bir dosyayı/veriyi geri dönüşü olmayacak şekilde silmek
- Bir şeyi "canlıya" (prod/deploy) almak, domain/DNS değişikliği
- docs/ içindeki dökümanla çelişen veya belirsiz bir gereksinim bulmak

Bunların dışındaki teknik kararları alt-ajanlar ve PM kendi başına verip
ilerler.
