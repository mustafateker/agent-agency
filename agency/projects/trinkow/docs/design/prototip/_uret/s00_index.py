# -*- coding: utf-8 -*-
"""Prototip giris sayfasi. page() her sayfaya 'Tum yuzeylere don' baglantisi
koyuyor; hedefi burasi. Yeni tasarim uretmez, yalniz gezinme + temel ozeti."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

SAYFALAR = [
    ("01-bugun.html", "E-10", "Bugün (Pano)",
     "Ürünün kalbi. Kahraman sayı + tek LimitBar. 11 durum + odak hâlleri şeridi.",
     "Mood: sakin ve tek odaklı"),
    ("02-harcama-ekle.html", "E-11 · E-12", "Harcama ekle · Kayıt detayı",
     "Tutar tuş takımı, kategori çipleri, taksit ve tekrar seçenekleri. 11 durum.",
     "Mood: hızlı ve tek elle"),
    ("03-onboarding.html", "E-01 – E-09", "Açılış ve ilk kurulum",
     "Karşılama, günlük limit, kategori seçimi, izinler. 10 kare.",
     "Mood: kısa ve söz veren"),
    ("04-kayitlar.html", "E-14 · E-12 · E-13", "Kayıtlar · detay · silme",
     "Gün gün defter ritmi, kaydırma eylemleri, silme onayı. 11 kare.",
     "Mood: defter"),
    ("05-ozet.html", "E-16 · E-15 · E-18", "Özet · kategori · taksitler",
     "Haftalık cetvel, kategori dağılımı, taksit yükü. 12 kare.",
     "Mood: ölçüm sayfası"),
    ("06-ayarlar.html", "E-17 · E-19 · E-20", "Limitler · ayarlar · veri",
     "Limit düzenleme, bildirim tercihi, dışa aktarma ve veri silme. 6 kare.",
     "Mood: ayar masası"),
    ("07-sosyal.html", "Sosyal", "Kart şablonu ve profil görseli",
     "Instagram 4:5 tipografik carousel, monogram, kelime markası.",
     "Mood: afiş"),
]

TEMEL = [
    ("Spacing", "4pt tabanlı: 4 · 8 · 12 · 16 · 20 · 24 · 32 · 48. Ekran yan boşluğu her yerde 20pt. Ara değer üretilmez."),
    ("Tip ölçeği", "9 rol: display 44 · h1 28 · h2 20 · amount 17 · body 16 · body-strong 16 · label 13 · caption 13 · micro 12. Uppercase ve italik yok."),
    ("Köşe yarıçapı", "Tek kural: kutu 12pt (buton, kart, girdi, sayfa, dialog). Yalnız iki istisna: hap biçimli çip/çubuk uçları ve tam daire. 16/24 karışımı yok."),
    ("Gölge", "Yalnız iki yüzeyde: BottomSheet ve Dialog. İkisi de içeriğin üstünde durduğunu anlatır. Kartlarda, butonlarda, listede gölge yok."),
    ("Renk", "Petrol #14484C tek accent. Kiremit #A24A2A yalnız limit dışı. Kırmızı #8E2F20 yalnız silme onayı ve form hatası. Doluluk arttıkça renk değişmez."),
    ("Durumlar", "Hover YOK. Her etkileşimli eleman için pressed zorunlu; ayrıca disabled, loading, focused, hata, boş ve uzun içerik taşması çizildi."),
]

satirlar = ""
for i, (dosya, kod, ad, ozet, mood) in enumerate(SAYFALAR):
    satirlar += (f'<a class="g-row" href="{dosya}">'
                 + div("col grow",
                       T("t-label", "c-acc", kod) + sp(4)
                       + T("t-h2", "c-ink", ad) + sp(4)
                       + T("t-caption", "c-ink2", ozet) + sp(4)
                       + T("t-caption", "c-ink3", mood))
                 + wsp(16)
                 + div("shrink0", ic("chevron-right", 24, "#14484C"))
                 + '</a>')
    if i < len(SAYFALAR) - 1:
        satirlar += div("divider")

temel = T("t-h2", "c-ink", "Tasarım temeli") + sp(16)
for i, (baslik, metin) in enumerate(TEMEL):
    temel += (T("t-label", "c-acc", baslik) + sp(4)
              + T("t-body", "c-ink2", metin) + sp(20 if i < len(TEMEL) - 1 else 0))

html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trinkow — Tüm yüzeyler</title>
<link rel="stylesheet" href="stil.css">
</head>
<body>
<div class="g-page">
  <div class="col">
    <span class="t-h1 c-ink">Trinkow — tüm yüzeyler</span>
    <div class="h8"></div>
    <span class="t-body c-ink2">Aşama 2 prototipi. 7 sayfa, 61 cihaz karesi + 11 sosyal panel, 390×844 viewport.
    Her kare React Native&#8217;e çevrilebilir: yalnız flexbox, hover yok, grid yok.</span>
    <div class="h8"></div>
    <span class="t-caption c-ink3">Kaynak: projects/trinkow/docs/brand/tokens.md · projects/trinkow/docs/design/ekran-envanteri.md ·
    projects/trinkow/docs/design/bilesen-envanteri.md · projects/trinkow/docs/content/metinler.md</span>
    <div class="h32"></div>
  </div>
  <div class="g-strip">
    <div class="g-item"><div class="g-list">{satirlar}</div></div>
    <div class="g-item"><div class="g-note">{temel}</div></div>
  </div>
</div>
</body>
</html>
'''
yol = os.path.join(OUT, "index.html")
with open(yol, "w", encoding="utf-8") as f:
    f.write(html)
print("yazildi:", yol, len(html), "bayt")
