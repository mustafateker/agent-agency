---
name: mustafa-yonlendirme-tarzi
description: Mustafa direktifleri kısa ve dolaylı verir; onayı "yap" biçiminde gelir, "onaylıyorum" cümlesi beklenmemeli
metadata:
  type: feedback
---

Mustafa yönlendirmeyi **kısa, emir kipinde ve dolaylı** verir. Aşama geçiş
onayını "tasarımı onaylıyorum" diye değil, bir sonraki işi isteyerek kurar —
ör. "şimdilik frontend olarak sen bunu kodla, bir an önce ürüne ulaşalım"
cümlesi Aşama 2→3 geçiş onayı olarak işlendi (K-063).

**Why:** Tek kişilik ürün sahibi; hız önceliği açıkça belirtiyor ("bir an önce
ürüne ulaşalım"). Tören niteliğindeki onay cümlelerini kurmuyor, işin ilerlemesini
onay sayıyor.

**How to apply:**
- Bir sonraki adımı isteyen kısa bir cümle geldiğinde, bunu geçiş onayı olarak
  **yorumla ama yorumu DECISIONS.md'ye açıkça not et** ("Mustafa şu cümleyi kurdu,
  pratikte geçiş onayıdır ve öyle işlendi"). Sessizce varsayma.
- Bu yorum yalnız **ilerleme yönünde** geçerlidir. CLAUDE.md'deki onay listesi
  (ücretli bağımlılık, geri dönüşsüz silme, prod/deploy, döküman çelişkisi) için
  dolaylı cümle **yeterli değildir** — açık soru sorulur.
- İş sıralamasında kapsam bütünlüğü değil **ürüne ulaşma hızı** önceliklidir:
  değer üreten tur önce, kapı açan tur (auth gibi) sona.
- Rapor kısa olsun: ne yapıldı / ne bekliyor / senden ne lazım.
