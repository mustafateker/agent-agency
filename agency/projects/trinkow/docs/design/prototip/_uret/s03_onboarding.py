# -*- coding: utf-8 -*-
"""E-00…E-03 — Onboarding. Mood: kisa nefes. Ekran basina tek soru, cok bosluk,
tek birincil buton. 4. ekrana cikarilamaz."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *


def ob(adim, baslik, aciklama, govde, buton, geri=True, alt=""):
    ust = div("row px20",
              (iconbtn("chevron-left", "Geri dön") if geri else div("", "", "width:44px;height:44px")),
              "min-height:44px")
    return div("scroll",
               ust + sp(16)
               + div("col px20", stepind(adim)) + sp(24)
               + div("col px20",
                     f'<span class="t-h1 c-ink">{baslik}</span>'
                     + (sp(8) + f'<span class="t-body c-ink2">{aciklama}</span>'
                        if aciklama else ""))
               + sp(32) + govde) \
        + div("col px20", buton + (sp(8) + alt if alt else ""),
              "padding-top:12px;padding-bottom:24px")


def secim_karti(ikon, baslik, alt, secili=False, basili=False):
    stil = "background:#FFFDF8;border:1px solid #DCD5C6"
    if secili:
        stil = "background:#FFFDF8;border:1.5px solid #14484C"
    if basili:
        stil = "background:#F4F1EA;border:1px solid #DCD5C6"
    renk = "#14484C" if secili else "#5C574C"
    sag = ic("check", 24, "#14484C", 1.75, "Seçili") if secili else ""
    return div("row",
               div("shrink0", ic(ikon, 24, renk)) + wsp(16)
               + div("col grow",
                     f'<span class="t-bodys {"c-acc" if secili else "c-ink"}">{baslik}</span>'
                     + f'<span class="t-caption c-ink2">{alt}</span>')
               + (wsp(12) + sag if sag else ""),
               "border-radius:12px;padding:16px;margin-bottom:12px;min-height:64px;" + stil)


def limitkutu(sayi, durum="focused", renk="c-ink"):
    b = {"focused": "field field-focus", "default": "field", "error": "field field-err"}[durum]
    caret = div("caret") + wsp(8) if durum == "focused" else ""
    return div(b, div("row grow", "", "justify-content:flex-end") + caret
               + f'<span class="t-display {renk} tab-num">{sayi}</span>' + wsp(8)
               + T("t-h1", "c-ink2", "₺"),
               "height:64px;justify-content:flex-end")


bloklar = []

# ---------------------------------------------------------------- E-00 splash
bloklar.append(item(
    "E-00", "Açılış (Splash)",
    "Zemin Kağıt, ortada kelime markası 32pt Petrol. Animasyon yok, slogan "
    "yok, sürüm yok, yükleme çubuğu yok.",
    div("scroll mid-x mid-y", T("t-splash", "c-acc", "Trinkow"))))

# ---------------------------------------------------------------- E-01
bloklar.append(item(
    "E-01", "Adım 1/3 · Niyet (seçim yok)",
    "Seçim yapılmadan Devam pasif. Kartlar dikey — 'daire ikon + başlık + "
    "tek cümle' üçlü kart düzeni kurulmadı.",
    ob(1, "Neden buradasın", "Sonra değiştirebilirsin.",
       div("col px20",
           secim_karti("notebook-text", "Param nereye gidiyor",
                       "Günlük harcamanı görmek istiyorsun.")
           + secim_karti("gauge", "Bütçe yaratmak",
                         "Her ay bir miktar ayırmak istiyorsun.")
           + secim_karti("layers", "Borç kapatmak",
                         "Kalan borcu eritmek istiyorsun.")),
       btn_p("Devam", "disabled"), geri=False)))

bloklar.append(item(
    "E-01", "Adım 1/3 · seçili + basılı hâller",
    "Seçili kart: 1.5pt Petrol kenarlık + check ikonu, başlık Petrol. "
    "Ortadaki kart 'pressed' (zemin Kağıt) — hover yok, geri bildirim bu.",
    ob(1, "Neden buradasın", "Sonra değiştirebilirsin.",
       div("col px20",
           secim_karti("notebook-text", "Param nereye gidiyor",
                       "Günlük harcamanı görmek istiyorsun.", secili=True)
           + secim_karti("gauge", "Bütçe yaratmak",
                         "Her ay bir miktar ayırmak istiyorsun.", basili=True)
           + secim_karti("layers", "Borç kapatmak",
                         "Kalan borcu eritmek istiyorsun.")),
       btn_p("Devam"), geri=False)))

# ---------------------------------------------------------------- E-02
bloklar.append(item(
    "E-02", "Adım 2/3 · günlük limit (boş)",
    "Alan otomatik odaklı, klavye açık gelir. Tutar boşken Devam pasif. "
    "Öneri çipleri tek dokunuşla doldurur.",
    ob(2, "Günde ne kadar harcamak istiyorsun",
       "Kesin olması gerekmiyor. Sonra düzeltiriz.",
       div("col px20",
           T("t-label", "c-ink2", "Günlük limit") + sp(8)
           + limitkutu("0", "focused", "c-ink3") + sp(16)
           + T("t-label", "c-ink2", "Sık kullanılan") + sp(8)
           + div("row wrap", chip("200 ₺") + chip("350 ₺") + chip("500 ₺"))),
       btn_p("Devam", "disabled"), geri=True)))

bloklar.append(item(
    "E-02", "Adım 2/3 · dolu · hata · basılı çip",
    "Üstte 350 ₺ girilmiş hâl, altta hata satırı. Hata metninde 'Hata:', "
    "'Geçersiz' ve ünlem yok.",
    ob(2, "Günde ne kadar harcamak istiyorsun",
       "Kesin olması gerekmiyor. Sonra düzeltiriz.",
       div("col px20",
           T("t-label", "c-ink2", "Günlük limit") + sp(8)
           + limitkutu("350") + sp(8)
           + T("t-caption", "c-ink2", "Ayda yaklaşık 10.500 ₺. Tahmini.")
           + sp(16)
           + T("t-label", "c-ink2", "Sık kullanılan") + sp(8)
           + div("row wrap", chip("200 ₺") + chip("350 ₺", secili=True)
                 + chip("500 ₺", basili=True))
           + sp(24) + div("divider") + sp(24)
           + T("t-label", "c-ink2", "Hatalı hâl (aynı alan)") + sp(8)
           + limitkutu("0", "error", "c-ink3") + sp(8)
           + T("t-caption", "c-dan", "Tutar boş kalamaz.")),
       btn_p("Devam"), geri=True)))

# ---------------------------------------------------------------- E-03 üç kip
bloklar.append(item(
    "E-03", "Adım 3/3 · Takip kipi",
    "Seçilen niyete göre TEK soru. En fazla üç kategori seçilir; seçili "
    "çiplerde onay ikonu yok. 'Şimdi değil' ile atlanabilir.",
    ob(3, "En çok neyi merak ediyorsun", "En fazla üç kategori seç.",
       div("col px20",
           div("row wrap",
               chip("Market") + chip("Kafe", secili=True) + chip("Restoran")
               + chip("Ulaşım", secili=True) + chip("Akaryakıt") + chip("Fatura")
               + chip("Kira ve ev") + chip("Abonelik") + chip("Sağlık")
               + chip("Giyim") + chip("Eğlence", secili=True)
               + chip("Alışkanlıklar") + chip("Diğer"))),
       btn_p("Başla"),
       alt=btn_g("Şimdi değil", "default", "c-ink2",
                 "align-self:center;padding-left:20px;padding-right:20px"))))

bloklar.append(item(
    "E-03", "Adım 3/3 · Tasarruf kipi",
    "Aynı iskelet, farklı tek soru. Kip değişince pano kahraman etiketi de "
    "değişir (aşağıdaki iki kareye bak).",
    ob(3, "Ayda ne kadar biriktirmek istiyorsun", "",
       div("col px20",
           T("t-label", "c-ink2", "Aylık hedef") + sp(8)
           + limitkutu("3.000") + sp(8)
           + T("t-caption", "c-ink2", "Günde yaklaşık 100 ₺. Tahmini.")),
       btn_p("Başla"),
       alt=btn_g("Şimdi değil", "default", "c-ink2",
                 "align-self:center;padding-left:20px;padding-right:20px"))))

bloklar.append(item(
    "E-03", "Adım 3/3 · Borç kipi · basılı buton",
    "Birincil buton 'pressed': zemin #0E3A3E. Ölçek (scale) animasyonu yok, "
    "yalnız renk döner (120ms).",
    ob(3, "Kalan borcun ne kadar", "Yaklaşık yazman yeterli.",
       div("col px20",
           T("t-label", "c-ink2", "Toplam kalan borç") + sp(8)
           + limitkutu("48.500") + sp(8)
           + T("t-caption", "c-ink2", "Ayda 4.041 ₺ ödersen 12 ayda biter. Tahmini.")),
       btn_p("Başla", "pressed"),
       alt=btn_g("Şimdi değil", "pressed", "c-ink2",
                 "align-self:center;padding-left:20px;padding-right:20px"))))

# ---------------------------------------------------------------- kisisellesen pano
def pano_kip(etiket, sayi, alt, bar, kip):
    return div("scroll",
               div("row between px20",
                   T("t-h1", "c-ink", "Bugün") + iconbtn("settings", "Ayarları aç"),
                   "min-height:44px")
               + sp(32)
               + div("col px20",
                     div("row between",
                         T("t-label", "c-ink2", etiket)
                         + div("chip chip-sel shrink0", T("t-label", "c-acc", kip)))
                     + sp(4) + T("t-display", "c-ink", sayi) + sp(24) + bar
                     + sp(12) + T("t-caption", "c-ink2", alt))
               + sp(48)
               + div("col px20 mid-x",
                     tally() + sp(24) + T("t-h2", "c-ink", "Bugün boş") + sp(8)
                     + '<span class="t-body c-ink2 mid">Bugün henüz bir şey yazmadın.'
                       ' İlk kahve iyi bir başlangıç.</span>')) \
        + div("col px20",
              div("btn-p", ic("plus", 24, "#FFFDF8") + wsp(8)
                  + T("t-bodys", "c-page", "Harcama ekle"), "align-self:stretch"),
              "padding-top:12px;padding-bottom:12px") \
        + tabbar("bugun")


bloklar.append(item(
    "E-10", "Onboarding sonrası pano · Tasarruf kipi",
    "Niyet seçimi panoyu anında kişiselleştirir: kahraman etiketi "
    "'bu ay biriken' olur, çubuk aylık hedefe göre dolar.",
    pano_kip("bu ay biriken", "1.150 ₺", "Hedefin 3.000 ₺. Ayın 10. günü.",
             limitbar(1150, 3000), "Tasarruf")))

bloklar.append(item(
    "E-10", "Onboarding sonrası pano · Borç kipi",
    "Aynı iskelet, üçüncü kip: 'kalan borç'. Ekran klonlanmadı, tek "
    "değişken kahraman etiketi ve çubuğun ölçeği.",
    pano_kip("kalan borç", "48.500 ₺", "Bu ay 4.041 ₺ ödendi.",
             limitbar(4041, 52541), "Borç")))

bloklar.append(note("Onboarding kararları", [
    "Üç adım, dördüncü yok. StepIndicator yüzde/dolan çubuk değil, üç hairline çentik.",
    "E-01'de intent ikonları kilitli Lucide setinden yeniden kullanıldı (notebook-text / gauge / layers) — sete yeni ikon eklenmedi.",
    "Seçili kart onay için 'check' ikonu kullanır; çiplerde onay ikonu YOKTUR (tokens.md 7.6) — iki farklı bileşen, iki farklı kural.",
    "E-03 atlanabilir; atlanırsa aynı soru E-20 ile 2. günde bir kez döner, ikinci reddedişte bir daha sorulmaz.",
    "Geri dönüş her adımda var; sol üstteki geri ikonu 44pt hedef, iOS kaydırmasıyla birlikte çalışır.",
    "Onboarding'de logo yalnız splash'ta geçer; pano başlığında marka adı gösterilmez (brandbook 5.1).",
]))

page("E-00…E-03 · Onboarding",
     "Kısa nefes. 10 kare: splash · niyet (boş/seçili/basılı) · limit (boş/dolu/hata) "
     "· üç kip sorusu · kipe göre kişiselleşen pano.",
     bloklar, "03-onboarding.html")
