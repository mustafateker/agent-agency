# ai-ajans — Proje Talimatları

Bu repo, bir "PM ajanı + uzman alt-ajanlar" sistemiyle proje dökümantasyonundan
çalışan yazılım üreten küçük bir pilot sistemdir.

## Diller / Standartlar
- Üretilecek uygulama kodu **Python** ile yazılır (aksi belirtilmedikçe).
- Kod okunabilir, tip belirteçli (type hints) ve test edilebilir olmalı.
- Her yeni özellik için basit bir test eklenmeli (pytest).

## Klasörler
- `docs/`  — İnsan (Mustafa) tarafından yazılan proje dökümanları buraya konur.
  PM ajanı her oturumun başında burayı kontrol eder.
- `status/STATUS.md`     — Güncel ilerleme ve kaldığı yer.
- `status/BACKLOG.md`    — Görev kırılımı ve durumları.
- `status/DECISIONS.md`  — Onay/karar bekleyen veya verilmiş kararlar.
- `src/`    — Üretilen Python kodu.
- `.claude/agents/` — Alt-ajan tanımları.

## Onay gerektiren işlemler
Aşağıdakiler İÇİN HER ZAMAN önce `status/DECISIONS.md`'ye yazılıp Mustafa'nın
onayı beklenir, otomatik yapılmaz:
- Yeni bir ücretli servis/API/kütüphane bağımlılığı eklemek
- Var olan bir dosyayı/veriyi geri dönüşü olmayacak şekilde silmek
- Bir şeyi "canlıya" (prod/deploy) almak
- docs/ içindeki dökümanla çelişen veya belirsiz bir gereksinim bulmak

Bunların dışındaki teknik kararları alt-ajanlar ve PM kendi başına verip ilerler.
