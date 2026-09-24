# ai-ajans

"PM ajanı + aşamalara göre devreye giren uzman alt-ajanlar" ile çalışan bir
yapay zeka ajansı. Yerel çalışır (VS Code + Claude Code CLI).

```
ai-ajans/
├── CLAUDE.md      ← ajans talimatları · aşama modeli · onay kuralları
├── .claude/       ← alt-ajan tanımları (10 ajan)
├── agency/        ← 🏢 OTOMASYON — tüm projelerde ortak
│   ├── templates/   proje kurulum checklist'i, brandbook şablonu
│   ├── reference/   anti-pattern listesi, referans repolar, RN kısıtları
│   └── vendor/      open-design skill'i, 138 design system kütüphanesi
└── projects/      ← 📦 ÜRÜNLER — her proje kendi içinde kapalı
    └── trinkow/     docs/ · status/ · app/
```

**Ayrımın kuralı:** *"İkinci bir proje başlasa bu dosyayı kopyalar mıydım?"*
Evet → `agency/` · Hayır → `projects/<ad>/`

## Nasıl çalıştırılır
1. Bu klasörü aç, terminalde `claude` çalıştır.
2. `.claude/settings.json` oturumu otomatik `pm-orchestrator` ile açar.
3. PM, `CLAUDE.md`'deki **aktif projenin** `status/` dosyalarını okuyup
   kaldığı yerden devam eder.

## Aşamalar
| Aşama | Ajan(lar) | Model |
|---|---|---|
| 0 Keşif | pm-orchestrator | opus |
| 1 Marka | brand-strategist | opus |
| 2 UI/UX | ui-ux-designer, design-reviewer | opus |
| 3 Geliştirme | frontend-developer, python-developer | sonnet |
| 4 Kalite | qa-engineer | sonnet |
| 5 DevOps/Yayın | devops-engineer | sonnet |
| 6 Büyüme | social-media-strategist, social-media-analyst | sonnet |

Aşama 6, marka onayından sonra diğerleriyle paralel yürür.
Çıkış kriterleri ve onay kuralları: `CLAUDE.md` + aktif projenin `status/STAGE.md`.

## Aktif proje
**Trinkow** — harcamaları "kalori sayar gibi" takip ettiren davranışsal finans
uygulaması. React Native (Expo), Türkçe; Python/FastAPI + MongoDB backend.
Veri sunucuda; yerel geliştirme ve geçici test girişi için
`cd projects/trinkow/app && npm run dev`. Ayrıntı: `projects/trinkow/app/README.md`.
→ `projects/trinkow/docs/CONTEXT.md`

## İlkeler
- **Tasarım jenerik olmayacak** — her çıktı anti-pattern listesine karşı
  `design-reviewer` tarafından denetlenir; REVİZE bloklayıcıdır.
- **Ücretli bağımlılık yok** — font OFL, ikon MIT/ISC; ücretli servisler ayrıca onaylanır.
- **Uygulama yalan söylemez** — eksik veri uydurulmaz, tahmin "güncel" diye
  sunulmaz.
- **Onay kapıları PM tarafından varsayılamaz** (marka, tasarım, deploy,
  ücretli servis, silme).
