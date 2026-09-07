# Aşama Takibi

Mevcut aşama: 0 — Keşif

Kural: PM, mevcut aşamanın "çıkış kriteri" karşılanmadan ve gerekiyorsa
Mustafa'nın onayı `status/DECISIONS.md`'ye işlenmeden bir SONRAKİ aşamaya
GEÇMEZ. Bir aşamada listelenmeyen ajanı PM o aşamada çağırmaz.

## Aşama 0 — Keşif
- Aktif ajan: pm-orchestrator (sadece okur/netleştirir, üretim yapmaz)
- Çıkış kriteri: docs/ içindeki proje dökümanı okunmuş, BACKLOG.md'de net
  bir MVP tanımı var.

## Aşama 1 — Marka
- Aktif ajan: brand-strategist
- Çıktı: docs/brand/brandbook.md
- Çıkış kriteri: Mustafa brandbook'u onayladı (DECISIONS.md'de kayıtlı).

## Aşama 2 — UI/UX Tasarım
- Aktif ajanlar: ui-ux-designer, design-reviewer
- Ön koşul: Aşama 1 tamamlanmış olmalı (brandbook onaylı).
- Çıktı: docs/design/ altında tasarım/prototip
- Çıkış kriteri: design-reviewer PASS verdi VE Mustafa son görsel onayı
  verdi (DECISIONS.md).

## Aşama 3 — Geliştirme
- Aktif ajanlar: frontend-developer (UI kodu), python-developer (backend/
  iş mantığı)
- Ön koşul: Aşama 2 tamamlanmış olmalı.
- Çıkış kriteri: Planlanan özellikler kodlanmış, BACKLOG.md'de işaretli.

## Aşama 4 — Kalite
- Aktif ajan: qa-engineer
- Çıkış kriteri: Testler geçiyor, kritik/blocker hata yok.

## Aşama 5 — DevOps / Yayın
- Aktif ajan: devops-engineer
- Ön koşul: Aşama 4 tamamlanmış olmalı.
- Çıkış kriteri: Yayın planı DECISIONS.md'de onaylı (prod/deploy/domain/
  ücretli servis kararları CLAUDE.md'deki onay kuralına tabidir).

## Aşama 6 — Büyüme / Sosyal Medya (PARALEL aşama)
- Aktif ajanlar: social-media-strategist, social-media-analyst
- Ön koşul: SADECE Aşama 1 (brandbook onayı) tamamlanmış olmalı — marka
  sesi olmadan içerik üretilmez. Bu aşama Aşama 2-5 ile PARALEL
  ilerleyebilir, sıralı beklemez.

## Sonraki aşamalar (henüz kurulmadı, ihtiyaç oldukça agency-agents'tan
eklenecek): Satış, Müşteri Destek, Finans/Operasyon, Hukuk/Uyumluluk.
Bunlar için şu an ajan yok — iş bu noktaya geldiğinde PM'e/Mustafa'ya
haber verilip birlikte eklenecek.
