# ai-ajans (pilot)

Bu, "PM ajanı + uzman alt-ajanlar" ile çalışan küçük bir yapay zeka ajansı
pilotudur. Şu an tamamen yerel (local) çalışıyor; VS Code + Claude Code ile
kullanılmak üzere kuruldu.

## Nasıl çalıştırılır
1. Bu klasörü VS Code'da aç.
2. Terminalde bu klasörün içindeyken `claude` komutunu çalıştır
   (Claude Code CLI kurulu olmalı). `.claude/settings.json` sayesinde oturum
   otomatik olarak `pm-orchestrator` ajanıyla başlayacak.
3. Bir proje dökümanını `docs/` klasörüne ekle (markdown veya metin olarak).
4. PM ajanına şunu söyle: "docs/ klasöründeki dökümanı oku ve BACKLOG.md'yi
   oluştur, sonra ilk göreve başla."
5. İlerlemeyi `status/STATUS.md` üzerinden takip edebilirsin.

## Klasörler
- `docs/`   — proje dökümanları (SEN eklersin)
- `status/` — PM ajanının ilerleme/karar takibi (ajan günceller)
- `src/`    — üretilen Python kodu
- `tests/`  — pytest testleri
- `.claude/agents/` — pm-orchestrator, python-developer, qa-engineer tanımları

## Notlar
- Şu an her şey Python ile yazılıyor.
- Ücretli servis/yeni bağımlılık/silme/deploy gibi kararlar otomatik
  yapılmaz — PM bunları `status/DECISIONS.md`'ye yazıp senin onayını bekler.
