---
name: calisma-tarzi
description: Mustafa gives short, broad directives and expects end-to-end execution with judgment calls made inline — don't stop to ask for clarification on scope
metadata:
  type: feedback
---

Mustafa verir gibi kısa ve geniş direktifler verir ("sistemi optimal ve en
kaliteli hale getirelim", "repoları da ekleyelim yapılacaklar listesine") ve
işin uçtan uca bitirilmesini bekler. Yorum gerektiren noktalarda durup soru
sormak yerine, makul yorumu yapıp uygula ve yorumunu raporda açıkça belirt.

**Why:** İki oturum üst üste geniş direktif verdi; her ikisinde de yaptığım
yorumu (ör. "token tasarrufu için repolar" → küratörlü referans kayıt defteri +
bağlam paketi varlıkları) itirazsız kabul edip üzerine inşa etti. Netleştirme
sorusu sormak akışı yavaşlatıyor; o kararı bana devretmiş durumda.

**How to apply:**
- Kapsam belirsizse en savunulabilir yorumu seç, uygula, raporda "şöyle
  yorumladım" diye tek cümleyle belirt.
- Durup sorma kuralı SADECE `CLAUDE.md` → "Onay gerektiren işlemler" ve
  aşama geçiş onayları için geçerli (brandbook onayı, tasarım onayı, ücretli
  bağımlılık, silme, deploy). Bunlar gerçek kapılar, kapsam yorumu değil.
- Tekrarlanacak bir iş üretiyorsan tek seferlik değil **şablon** olarak kur
  (bkz. `templates/proje-kurulum-checklist.md`) — sistemin çok proje
  üreteceğini varsayıyor.
- Dış kaynak (repo/link) verirken **doğrula**; uydurma link tolere edilmez.
  `curl -o /dev/null -w "%{http_code}"` ile toplu kontrol ucuz ve yeterli.
- Commit etme; istemedikçe değişiklikleri çalışma alanında bırak.

İlgili: [[user-role]]
