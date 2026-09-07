# Jenerik "AI Yapmış" UI/UX Anti-Pattern Listesi

Bu dosya `ui-ux-designer` ve `design-reviewer` ajanları tarafından HER tasarımda
kontrol listesi olarak kullanılır. Amaç: "bir yapay zeka yapmış gibi duran",
markasız, birbirinin kopyası SaaS şablonlarından kaçınmak.

## Kaçınılacaklar
- Mor-mavi (indigo/violet) varsayılan gradyan arka planlar ve butonlar.
- Her elementte aynı "glassmorphism" (bulanık cam) efekti.
- Amaçsız, her karta otomatik uygulanmış yumuşak drop-shadow.
- Tutarsız / aşırı yuvarlatılmış köşeler (rastgele 12px, 16px, 24px karışık).
- Başlıklarda/ikonlarda emoji kullanımı (🚀 ✨ 💡).
- Varsayılan font seçimi: Inter / Poppins / Montserrat — markaya özgü bir
  gerekçe olmadan "AI'ın en sevdiği fontlar" kullanılmaz.
- "Üstte daire içinde ikon + başlık + 1 cümle" formatında 3 sütunlu özellik
  kartı şablonu (her AI-üretimi sitede aynı düzen).
- Stok illüstrasyon paketlerinden (undraw.co tarzı) markaya özgü olmayan
  rastgele illüstrasyonlar.
- Belirsiz, kimliksiz "SaaS başlangıç şablonu" hissi veren aşırı beyaz boşluk.
- Jenerik pazarlama dili ("Elevate your workflow", "Empower your team",
  "Supercharge your business") — marka sesi/kişiliği yansıtmayan metinler.
- Düşük kontrastlı açık gri metinler (erişilebilirlik göz ardı edilmiş).
- Tutarlı bir grid/spacing sistemi olmadan rastgele boşluk değerleri.
- Dark mode'un sadece renkleri ters çevirerek "otomatik" üretilmesi.

## Yapılması gerekenler
- Brandbook'taki renk paletini VE SADECE onu kullan; oradan sapma.
- Bilinçli seçilmiş bir tipografi çifti kullan (başlık/gövde) ve seçim
  gerekçesini kısaca yaz (marka kişiliğiyle ilişkisi ne?).
- Gerçek bir spacing/type scale sistemi tanımla (örn. 4px/8px grid) ve
  TÜM ekranlarda tutarlı uygula.
- Her ekran/bölüm için brandbook'taki marka kişiliğine bağlı belirgin bir
  "mood" tanımla; her ekran birbirinin klonu olmasın.
- İlham/rakip analizini gerçek, iyi tasarlanmış markalardan yap (Dribbble,
  Behance, gerçek marka siteleri) — jenerik AI şablonlarından değil.
- Placeholder yerine gerçek/gerçekçi içerik kullan (lorem ipsum kullanma).
- Kontrast oranlarını WCAG AA seviyesinde tut.

`design-reviewer` bu listedeki her maddeyi tek tek kontrol eder ve ihlal
varsa somut, satır/element bazlı düzeltme isteğiyle `ui-ux-designer`'a geri
gönderir.
