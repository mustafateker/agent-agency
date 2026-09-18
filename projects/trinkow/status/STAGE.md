# Aşama Takibi

Mevcut aşama: **2 — UI/UX Tasarım · ✅ design-reviewer PASS · 🔵 Mustafa'nın görsel onayı bekleniyor (K-063)**
Tasarım: `docs/design/prototip-v4/` — **18 ekran · 122 yüzey · 0 bulgu**, anti-pattern 20/20 temiz.
Kaynak dokümanlar senkron: `tokens.md` **v4.0** · bileşen envanteri · metinler · varlıklar · ekran envanteri.
Denetim raporu: `docs/design/denetim-raporu-v4.md` (2 tur: REVİZE → PASS).

⚠️ **Aşama 2 çıkış kriteri: PASS + Mustafa onayı.** PASS geldi, onay bekleniyor.
Onay gelince Aşama 3'e dönülür:
D-1 ✅ · D-2a ✅ · D-1b ✅ · D-2b ✅ · D-2c (onboarding/ayarlar — K-052 ile blok kalktı) ·
**D-2d 🆕 Günlük sekmesi · seri sistemi · gün seçici · oturum/hesap · profilleme+plan · ürün arama** ·
D-3 QA (Aşama 4).

Yayın öncesi bloklayıcılar (Mustafa'da): gizlilik politikası + kullanım şartları
metni (K-057/7) · hesap silme Edge Function (K-057/4).

Faz 1'de backend YOK, yalnız kimlik doğrulama var → `python-developer` hâlâ devrede değil (K-003).
Aşama 6 (Büyüme): içerik takvimi hazır, yayın zamanlaması Mustafa'da (K-010).
Aşama 1 ✅ (K-006/K-021, brandbook 2026-09-17'de K-052/K-048'e göre revize edildi).
Proje: Trinkow · Bağlam: `projects/trinkow/docs/CONTEXT.md` · Stack: RN (Expo) + TypeScript.

Kural: PM, mevcut aşamanın "çıkış kriteri" karşılanmadan ve gerekiyorsa
Mustafa'nın onayı `projects/trinkow/status/DECISIONS.md`'ye işlenmeden bir SONRAKİ aşamaya
GEÇMEZ. Bir aşamada listelenmeyen ajanı PM o aşamada çağırmaz.

Her aşamanın "Kurulum" satırı `agency/templates/proje-kurulum-checklist.md`'deki
P-serisine, "Girdi" satırı ise PM'in alt-ajana vereceği brief'te geçmesi
gereken dosya yollarıdır (bkz. CLAUDE.md → Token ekonomisi).

## Aşama 0 — Keşif
- Aktif ajan: pm-orchestrator (sadece okur/netleştirir, üretim yapmaz)
- Girdi: `projects/trinkow/docs/` altındaki proje dökümanı
- Kurulum: **P-1** (`projects/trinkow/docs/CONTEXT.md` tek sayfalık bağlam paketi), **P-8**
  (repo hijyeni) — bkz. `agency/templates/proje-kurulum-checklist.md`
- Çıkış kriteri: projects/trinkow/docs/ içindeki proje dökümanı okunmuş, BACKLOG.md'de net
  bir MVP tanımı var, P-1 üretilmiş.

## Aşama 1 — Marka
- Aktif ajan: brand-strategist
- Girdi: proje dökümanı, `agency/templates/brandbook-template.md`,
  `agency/reference/jenerik-ai-ui-anti-pattern-listesi.md`
- Çıktı: `projects/trinkow/docs/brand/brandbook.md`
- Kurulum (onaydan hemen sonra): **P-2** (marka token dosyası),
  **P-3** (`projects/trinkow/status/HANDOFF.md` başlat)
- Çıkış kriteri: Mustafa brandbook'u onayladı (DECISIONS.md'de kayıtlı).

## Aşama 2 — UI/UX Tasarım
- Aktif ajanlar: ui-ux-designer, design-reviewer
- Ön koşul: Aşama 1 tamamlanmış olmalı (brandbook onaylı).
- Girdi: `projects/trinkow/docs/brand/brandbook.md`,
  `agency/reference/jenerik-ai-ui-anti-pattern-listesi.md`,
  `agency/reference/referans-repolar.md`,
  **`agency/reference/rn-tasarim-kisitlari.md`** (RN'de inşa edilebilirlik — bağlayıcı)
- Kurulum (tasarım başlamadan ÖNCE): **P-4** gerçek metinler, **P-5**
  projeye özel referans seti, **P-6** varlık kilidi (tek ikon seti + fontlar),
  **P-7** bileşen envanteri + state listesi
- Çıktı: `projects/trinkow/docs/design/` altında tasarım/prototip
- Döngü: ui-ux-designer üretir → design-reviewer denetler → REVİZE ise
  somut maddelerle tasarımcıya geri döner. İkinci turdan itibaren denetim
  DELTA'dır (sadece açık maddeler + yeni sorunlar).
- Çıkış kriteri: design-reviewer PASS verdi VE Mustafa son görsel onayı
  verdi (DECISIONS.md). PASS tek başına yeterli değildir.

## Aşama 3 — Geliştirme
- Aktif ajanlar: frontend-developer (UI kodu), python-developer (backend/
  iş mantığı)
- Ön koşul: Aşama 2 tamamlanmış olmalı.
- Girdi: onaylı tasarım (`projects/trinkow/docs/design/`), `projects/trinkow/docs/brand/brandbook.md`
- Çıkış kriteri: Planlanan özellikler kodlanmış, BACKLOG.md'de işaretli.

## Aşama 4 — Kalite
- Aktif ajan: qa-engineer
- Girdi: `src/`, `tests/`
- Çıkış kriteri: Testler geçiyor, kritik/blocker hata yok.
- Not: BLOCKER bulgular `python-developer`/`frontend-developer`'a geri
  döner; QA düzeltme yapmaz.

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
- Girdi: `projects/trinkow/docs/brand/brandbook.md`, proje dökümanı,
  (varsa) `projects/trinkow/docs/social/analiz-raporu.md`
- Sıra: analyst önce veri üretir → strategist o veriyle takvimi kurar.

## Sonraki aşamalar (henüz kurulmadı, ihtiyaç oldukça agency-agents'tan
eklenecek): Satış, Müşteri Destek, Finans/Operasyon, Hukuk/Uyumluluk.
Bunlar için şu an ajan yok — iş bu noktaya geldiğinde PM'e/Mustafa'ya
haber verilip birlikte eklenecek.
