# ai-ajans (pilot)

"PM ajanı + aşamalara göre devreye giren uzman alt-ajanlar" ile çalışan bir
yapay zeka ajansı pilotu. Şu an tamamen yerel (VS Code + Claude Code CLI).

## Nasıl çalıştırılır
1. Bu klasörü VS Code'da aç, gerçek Terminal'de `claude` çalıştır
   (Claude Code CLI kurulu olmalı; kontrol: `claude --version`).
2. `.claude/settings.json` sayesinde oturum otomatik `pm-orchestrator` ile
   açılır.
3. `docs/` klasörüne proje dökümanını ekle.
4. PM'e "docs/ klasöründeki dökümanı oku ve BACKLOG.md'yi oluştur" de.
5. İlerlemeyi `status/STATUS.md` ve `status/STAGE.md` üzerinden izle.

## Aşamalar ve ajanlar
| Aşama | Ajan(lar) | Ne zaman devreye girer |
|---|---|---|
| 0. Keşif | pm-orchestrator | Her zaman ilk |
| 1. Marka | brand-strategist | docs/ dökümanı okunduktan sonra |
| 2. UI/UX | ui-ux-designer, design-reviewer | Brandbook ONAYLANDIKTAN sonra |
| 3. Geliştirme | frontend-developer, python-developer | Tasarım ONAYLANDIKTAN sonra |
| 4. Kalite | qa-engineer | Geliştirme bittikçe |
| 5. DevOps/Yayın | devops-engineer | QA'dan geçtikten sonra |
| 6. Büyüme/Sosyal Medya | social-media-strategist, social-media-analyst | Brandbook onaylanır onaylanmaz, PARALEL |

Detaylı çıkış kriterleri ve onay kuralları: `status/STAGE.md` ve `CLAUDE.md`.

İleride eklenecek (agency-agents'tan, ihtiyaç oldukça): Satış, Müşteri
Destek, Finans/Operasyon, Hukuk/Uyumluluk ajanları.

## Tasarım kalite güvencesi
UI/UX'in "AI yapmış gibi" jenerik durmaması için:
- Her ürün önce `docs/brand/brandbook.md` ile markalanır (2+ farklı yön
  sunulur, gerekçeli seçilir).
- Her tasarım `docs/design/jenerik-ai-ui-anti-pattern-listesi.md`'ye göre
  `design-reviewer` tarafından PASS/REVİZE olarak denetlenir.
- Son görsel onay her zaman Mustafa'dan alınır.

## Notlar
- Backend/otomasyon: Python. Frontend/UI: onaylı tasarıma sadık kalarak
  uygun web teknolojisi.
- Ücretli servis/yeni bağımlılık/silme/deploy/marka-tasarım onayı gibi
  kararlar otomatik yapılmaz — PM bunları `status/DECISIONS.md`'ye yazıp
  onayını bekler.
