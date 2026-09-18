---
name: ajan-yonlendirme-kisiti
description: Çalışan alt-ajana müdahale edilemez (SendMessage kapalı) — brief ilk seferde eksiksiz olmalı
metadata:
  type: project
---

Bu oturumda `SendMessage` aracı **kapalı**: başlatılmış bir alt-ajana ek girdi
gönderilemez, durdurulamaz. Yeni bir `Agent` çağrısı ise **soğuk** başlar; "devam
eden görevine ekle" demek işe yaramaz, ikinci bir ajan aynı dosyalara yazmaya başlar.

**Why:** 2026-09-17'de tasarımcı çalışırken Mustafa referans görseller verdi. Ek
girdiyi çalışan ajana iletmek isterken yeni bir ajan başlatıldı → aynı
`docs/design/prototip-v4/` üzerinde iki ajan, çakışma riski. Onaylı `prototip-v3`
tar yedeği alınarak zarar sınırlandı.

**How to apply:**
1. Brief'i **başlatmadan önce** tamamla; referans/varlık dosyalarını önce repoya
   kopyala, sonra ajanı başlat.
2. Oturum ortasında yeni istek gelirse çalışan ajanı bitmeye bırak; ek işi
   **sonraki tura** ver. Aynı dosya kümesine ikinci ajan gönderme.
3. Aynı dosyaya (ör. prototip `_uret/lib.py`) yazacak işleri paralel başlatma;
   paralellik ancak dosya sahipliği ayrıksa güvenli.
4. Kritik/onaylı artefaktı riske atacak iş öncesi `tar czf /tmp/...` yedeği al —
   `projects/` git'te izlenmiyor, geri dönüş yolu yok.
