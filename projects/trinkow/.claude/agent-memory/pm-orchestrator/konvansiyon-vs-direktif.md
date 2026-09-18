---
name: konvansiyon-vs-direktif
description: Mustafa'nın sözlü jest/yön tarifi platform konvansiyonuyla çakışırsa konvansiyon kazanır — sorulmaya değer ama varsayılan konvansiyondur
metadata:
  type: feedback
---

Mustafa'nın direktifleri hızlı yazıldığı için **jest/yön tarifleri gevşek** olabilir.
Böyle bir tarif yerleşik platform konvansiyonuyla çakıştığında **konvansiyonu
öner ve uygula**; direktifi birebir taklit etmek doğru okuma değil.

**Why:** 2026-09-17'de "kullanıcı sola kaydırdığında dün, tekrar sola kaydırdığında
2 gün önce" dedi. Birebir uyguladım (bugün en solda, geçmiş sağda). Takvim
konvansiyonunda geçmiş solda durur; bunu tek satırla sorduğumda cevabı **"çevir"**
oldu (K-055). Yani istediği şey "geçmişe gün gün gidebilmek"ti, jestin yönü değil.
Aynı örüntü: niyeti al, mekaniği konvansiyona göre kur.

**How to apply:** Direktifte yön/jest/sıralama geçtiğinde önce "asıl niyet ne?"
diye ayır. Konvansiyonla çakışma varsa alt-ajana konvansiyonu ver, Mustafa'ya da
**tek satırlık** "böyle yaptım, çevirmek bir satır" notu düş — uzun seçenek
listesi açma. Bkz. [[user-mustafa]].
