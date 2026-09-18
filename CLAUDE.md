# ai-ajans — Proje Talimatları

Bu repo, "PM ajanı + aşamalara göre devreye giren uzman alt-ajanlar"
sistemiyle proje dökümantasyonundan profesyonel, markalı bir ürün üreten
bir pilot sistemdir.

## Aşama modeli
Ajanlar rastgele/hepsi-birden değil, `projects/trinkow/status/STAGE.md`'de tanımlı sırayla
devreye girer: Keşif → Marka → UI/UX Tasarım → Geliştirme → Kalite →
DevOps/Yayın; Büyüme/Sosyal Medya aşaması Marka onayından sonra diğerleriyle
paralel ilerleyebilir. Detaylar ve her aşamanın çıkış kriteri
`projects/trinkow/status/STAGE.md`'de.

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
- Hiçbir UI/UX çalışması, önce `projects/trinkow/docs/brand/brandbook.md` onaylanmadan
  başlamaz (bkz. Aşama 1 → 2 geçiş kuralı).
- Her tasarım `agency/reference/jenerik-ai-ui-anti-pattern-listesi.md`'ye göre
  `design-reviewer` tarafından denetlenir.
- Tasarım/frontend ajanları `agency/reference/referans-repolar.md`'deki
  sabitlenmiş kaynakları kullanır. **Kritik nüans:** o repolardan
  *sistematik* (token mimarisi, erişilebilirlik, state/edge case) alınır;
  *görsel stil* alınmaz — hazır design system temalarını kopyalamak,
  kaçındığımız jenerik görünümün birebir kaynağıdır.

## Token ekonomisi (kalite kadar önemli)
Bu bir çok-ajanlı sistem: her alt-ajan **soğuk başlar** ve bağlamı yeniden
keşfetmesi pahalıdır. Kalite düşürmeden maliyeti düşürmek için:

1. **Brief'te bağlam ver.** PM alt-ajana görev verirken okunacak dosyaların
   TAM YOLLARINI ve önceki kararların 2-3 satırlık özetini verir.
   "Repoya bak, anlarsın" en pahalı cümledir.
2. **Arama değil, adres.** Açık uçlu `WebSearch` yerine
   `agency/reference/referans-repolar.md`'deki bilinen URL'ye gidilir. Repo
   sayfası yerine ham dosya (`raw.githubusercontent.com`) çekilir.
3. **Hedefli okuma.** Önce `grep`/`glob`, sonra gerekiyorsa `Read`. Büyük
   dosyaları baştan sona okumak yerine ilgili bölüm okunur.
4. **Doğrulama için geri okuma yok.** Dosya düzenlendikten sonra tekrar
   okunmaz; düzenleme başarısızsa araç zaten hata verir.
5. **Çıktı sözleşmesi.** Her ajanın PM'e raporu satır sınırlıdır ve kod/
   dosya içeriği rapora kopyalanmaz — dosya zaten diskte.
6. **Tek ajan, tek net görev.** Kapsamı geniş görev, ajanın gereksiz
   keşif yapmasına ve tekrar denemelere yol açar.
7. **Delta denetim.** `design-reviewer` ikinci turda baştan denetlemez,
   sadece kapanan/yeni maddelere bakar.
8. **Model kademelendirmesi.** Yargı gerektiren roller (PM, marka, tasarım,
   tasarım denetimi) `opus`; uygulama/analiz rolleri (geliştirme, QA,
   DevOps, sosyal medya) `sonnet`. Bir role model atarken "bu işin bedeli
   yanlış yargı mı, yavaşlık mı?" diye sorulur.

## Repo yapısı — AJANS ve PROJELER ayrıdır

Bu repo iki ayrı şeyi barındırır. **Karıştırma.**

```
ai-ajans/
├── CLAUDE.md          ← bu dosya (ajans talimatları)
├── .claude/agents/    ← alt-ajan tanımları
│
├── agency/            ← 🏢 OTOMASYON SİSTEMİ (tüm projelerde ortak)
│   ├── templates/     ← proje-kurulum-checklist.md, brandbook-template.md
│   ├── reference/     ← anti-pattern listesi, referans-repolar.md,
│   │                     rn-tasarim-kisitlari.md, open-design-entegrasyon.md
│   └── vendor/        ← open-design skill, design-systems kütüphanesi (138 sistem)
│
└── projects/          ← 📦 ÜRÜNLER (her proje kendi içinde kapalı)
    └── trinkow/
        ├── docs/      ← CONTEXT.md, brand/, design/, content/, social/
        ├── status/    ← STATUS · STAGE · BACKLOG · DECISIONS · HANDOFF
        └── app/       ← Expo (React Native) uygulaması
```

### AKTİF PROJE: `projects/trinkow/`
PM oturuma başlarken **aktif projenin** `status/` dosyalarını okur:
`projects/trinkow/status/STAGE.md` → `STATUS.md` → `BACKLOG.md` → `DECISIONS.md`.
Yeni bir proje başlarsa `projects/<ad>/` altında aynı iskeletle kurulur ve
bu satır güncellenir.

### Ayrımın kuralı
- **`agency/`** — birden çok projede tekrar kullanılan her şey. Bir dosya
  yalnız Trinkow için anlamlıysa oraya KOYULMAZ.
- **`projects/<ad>/`** — yalnız o ürüne ait her şey. Proje silinse `agency/`
  bozulmamalı; `agency/` değişse proje çalışmaya devam etmeli.
- Şüphedeysen sor: *"ikinci bir proje başlasa bu dosyayı kopyalar mıydım?"*
  Evet → `agency/`. Hayır → `projects/`.

## Alt-ajan preprompt standardı
`.claude/agents/*.md` dosyaları ortak bir iskelet izler. Yeni ajan
eklenirken bu yapı korunur:
`Rol → Girdiler (tam dosya yolları) → Süreç → Kalite kuralları →
Çıktı sözleşmesi (satır sınırlı) → Token disiplini → Sınırlar →
Definition of Done`

Her ajanın preprompt'unda **ne YAPMAYACAĞI** açıkça yazılıdır; kapsam
kayması bu sistemdeki en yaygın kalite ve maliyet sorunudur.

## Onay gerektiren işlemler
Aşağıdakiler İÇİN HER ZAMAN önce `projects/trinkow/status/DECISIONS.md`'ye yazılıp
Mustafa'nın onayı beklenir, otomatik yapılmaz:
- Brandbook'un nihai onayı (Aşama 1 → 2 geçişi)
- UI/UX tasarımının son onayı (Aşama 2 → 3 geçişi)
- Yeni bir ücretli servis/API/kütüphane bağımlılığı eklemek
- Var olan bir dosyayı/veriyi geri dönüşü olmayacak şekilde silmek
- Bir şeyi "canlıya" (prod/deploy) almak, domain/DNS değişikliği
- projects/trinkow/docs/ içindeki dökümanla çelişen veya belirsiz bir gereksinim bulmak

Bunların dışındaki teknik kararları alt-ajanlar ve PM kendi başına verip
ilerler.
