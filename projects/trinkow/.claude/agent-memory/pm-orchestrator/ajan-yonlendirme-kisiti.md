---
name: ajan-yonlendirme-kisiti
description: Alt-ajan yürütme kısıtları — SendMessage kapalı, denetçi/QA dosyaya yazamaz, uzun görevler oturum limitinde kesilebilir
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
4. Kritik/onaylı artefaktı riske atacak iş öncesi `tar czf /tmp/...` yedeği al.
   **Düzeltme (2026-09-24):** `projects/` git'te İZLENİYOR (`git ls-files` ile
   doğrulandı), yani geri dönüş yolu var; yedek yine de commit'lenmemiş ara
   durumlar için ucuz sigorta.


## Ek kısıtlar (2026-09-26, REV2 turunda üç kez yaşandı)

**`design-reviewer` ve `qa-engineer` rapor dosyası YAZAMIYOR.** Brief'te
"`docs/design/...-denetim.md` dosyasına yaz" dense bile harness kısıtı nedeniyle
bulguları yalnız metin olarak döndürüyorlar (4 çağrının 4'ünde).
**How to apply:** Denetim/QA raporunun diske geçmesi gerekiyorsa bunu PM
üstlenir; ya da bir sonraki ajana bulguları **brief'in içinde** taşırım —
"önceki denetim raporunu oku" demek boşa çıkar, o dosya yoktur.

**Uzun görevler oturum limitiyle kesilebiliyor.** REV2'de bir tasarımcı ve bir
geliştirici görev ortasında öldü (biri diske yazmıştı, biri yazmamıştı).
**How to apply:** (1) Kesilen işi yeniden başlatırken brief'e "yarıda kesilmiş
bir işi TAMAMLIYORSUN, önce mevcut dosya durumunu oku, kapanmış maddeyi tekrar
kapatma" maddesini koy — aksi hâlde ajan işi baştan yapar. (2) Kesinti öncesi
`git status`/`git diff --stat` ile hasar tespiti yap: yazmaya başlamamış ajan
temiz baştan başlatılabilir. (3) Çok maddeli revizyonları gruplara böl; ajan
grup grup diske yazarsa kesinti daha az iş kaybettirir.
