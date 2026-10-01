# projects/ — Ürünler

Her proje kendi içinde kapalıdır. Ortak varlıklar bir üstteki
`templates/`, `reference/` ve `vendor/` alanlarındadır; çalışan kod ise
repo kökündeki `../mobile/` ve `../backend/` klasörlerindedir.

```
projects/<proje-adı>/
├── docs/
│   ├── CONTEXT.md   ← P-1: tek sayfalık bağlam paketi (TÜM ajanlar bunu okur)
│   ├── brand/       ← brandbook.md + tokens.md (makine okunur)
│   ├── design/      ← prototipler, ekran/bileşen envanteri, varlık kilidi
│   ├── content/     ← metinler.md (arayüzdeki tüm gerçek metin)
│   └── social/      ← analiz raporu + içerik takvimi
├── status/
│   ├── STAGE.md     ← mevcut aşama + çıkış kriterleri
│   ├── STATUS.md    ← nerede kalındı
│   ├── BACKLOG.md   ← görev kırılımı
│   ├── DECISIONS.md ← onay bekleyen/verilmiş kararlar (K-xxx)
│   └── HANDOFF.md   ← aşama başına 3-5 satır devir-teslim
```

## Aktif proje: `trinkow/`
**Trinkow** — harcamaları "kalori sayar gibi" takip ettiren davranışsal
finans uygulaması. React Native (Expo), Türkçe; FastAPI + MongoDB, veri sunucuda.
Ayrıntı: `trinkow/docs/CONTEXT.md`

Durum: Aşama 3 (Geliştirme). Tasarım tamamlandı ve onaylandı
(13 dosya, 62 yüzey, claymorphism).

## Yeni proje başlarken
1. `projects/<ad>/` altında yukarıdaki iskeleti kur.
2. `templates/proje-kurulum-checklist.md`'deki **P-1…P-8**'i
   `status/BACKLOG.md`'ye kopyala.
3. `CLAUDE.md`'deki "AKTİF PROJE" satırını güncelle.
4. Proje-özel kural geçersiz kılmaları `docs/CONTEXT.md`'ye yazılır;
   ortak ajans kuralları değiştirilmez.
