# -*- coding: utf-8 -*-
"""Instagram tipografik kart sablonu (4:5) + profil gorseli (monogram).
Metinler projects/trinkow/docs/social/icerik-takvimi.md'den birebir alindi; uydurma metin yok.
Olcek: 1080x1350 -> 432x540 (0.4). Canva kullanilmadi; sablon tokens.md'den beslenir."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *


def kart(zemin, ic_, etiket, panel=""):
    alt = div("row between",
              f'<span class="t-label {etiket}">Trinkow</span>'
              + (f'<span class="t-micro {etiket} tab-num">{panel}</span>' if panel else ""))
    return div("igcard",
               div("col grow", ic_, "justify-content:center") + alt,
               f"background:{zemin};padding:32px")


def cizgi_motif(renk="#C9C0AC", adet=9):
    c = ""
    for i in range(adet):
        c += div("", "", f"width:1.75px;height:32px;background:{renk};margin-right:12px")
    return div("row", c)


def buyuk_bar(dolu, tasma=0, oluk=1):
    parcalar = div("", "", f"flex:{dolu} 1 0;height:24px;background:#14484C;"
                           "border-top-left-radius:12px;border-bottom-left-radius:12px")
    if tasma:
        parcalar += div("", "", "width:2px;height:36px;background:#5C574C;flex-shrink:0")
        parcalar += div("", "", f"flex:{tasma} 1 0;height:24px;background:#A24A2A;"
                                "border-top-right-radius:12px;border-bottom-right-radius:12px")
    else:
        parcalar += div("", "", f"flex:{oluk} 1 0;height:24px;background:#DCD5C6;"
                                "border-top-right-radius:12px;border-bottom-right-radius:12px")
        parcalar += div("", "", "width:2px;height:36px;background:#5C574C;flex-shrink:0")
    return div("row", parcalar, "height:36px;align-items:center")


def kutu(baslik, notu, kartlar):
    return div("g-item",
               div("row wrap", kartlar)
               + div("g-cap", T("t-label", "c-acc", baslik) + sp(4)
                     + T("t-caption", "c-ink2", notu), "width:auto;max-width:900px"))


bloklar = []

# ---------------------------------------------------- Varyant A: Kağıt (Hafta 1)
A = "".join([
    kart("#F4F1EA",
         cizgi_motif() + sp(32)
         + '<span class="ig-h2 c-ink">Günde 1 kahve,<br>1 taksi,<br>1 &#8220;küçük&#8221; alışveriş.</span>',
         "c-ink2", "1/3"),
    kart("#F4F1EA",
         '<span class="ig-h1 c-ink">Hiçbiri tek başına<br>önemli görünmüyor.</span>',
         "c-ink2", "2/3"),
    kart("#14484C",
         '<span class="ig-h1 c-paper">Ay sonunda<br>hepsi birden<br>görünüyor.</span>'
         + sp(24) + cizgi_motif("#F4F1EA", 9),
         "c-paper", "3/3"),
])
bloklar.append(kutu(
    "Varyant A — Kağıt · 3 panel (Hafta 1, Gözlem)",
    "Zemin Kağıt, metin Mürekkep, tek serif blok. Son panel Petrol'e dönerek "
    "carousel'in sonunu işaretler. Fotoğraf, illüstrasyon, ikon yok.", A))

# ------------------------------------------- Varyant B: Karşılaştırma (Hafta 2)
B = "".join([
    kart("#FFFDF8",
         T("ig-lbl", "c-acc", "deriz") + sp(24)
         + '<span class="ig-h1 c-ink">Limitin 60 ₺<br>üzerindesin.</span>'
         + sp(32) + buyuk_bar(300, 60),
         "c-ink2", "1/2"),
    kart("#FFFDF8",
         T("ig-lbl", "c-ink3", "demeyiz") + sp(24)
         + '<span class="ig-h1 c-ink3">Yine fazla<br>harcadın.</span>'
         + sp(32)
         + div("", "", "height:1.5px;background:#DCD5C6;width:200px"),
         "c-ink2", "2/2"),
])
bloklar.append(kutu(
    "Varyant B — Karşılaştırma · 2 panel (Hafta 2, Marka Sesi)",
    "İkinci panel Mürekkep 60 ile sessizleştirilir; kırmızı KULLANILMAZ "
    "(o renk yalnız limit dışı/yıkıcı işlem içindir). 'deriz / demeyiz' kütüphanesi.", B))

# --------------------------------------------- Varyant C: Diyagram (Hafta 3)
C = "".join([
    kart("#F4F1EA",
         '<span class="ig-h2 c-ink">Çoğu bütçe uygulaması<br>limiti aştığında'
         '<br>kırmızıya döner.</span>' + sp(32)
         + div("row", div("", "", "flex:1 1 0;height:24px;background:#DCD5C6;"
                                  "border-radius:12px"), "height:36px"),
         "c-ink2", "1/3"),
    kart("#F4F1EA",
         '<span class="ig-h2 c-ink">Trinkow&#8217;da çubuk<br>hep aynı renkte'
         '<br>kalıyor.</span>' + sp(32) + buyuk_bar(180, 0, 120),
         "c-ink2", "2/3"),
    kart("#F4F1EA",
         '<span class="ig-h2 c-ink">Taşan kısım ayrı bir<br>segment — kırmızı'
         '<br>değil, kiremit.</span>' + sp(32) + buyuk_bar(300, 60),
         "c-ink2", "3/3"),
])
bloklar.append(kutu(
    "Varyant C — Diyagram · 3 panel (Hafta 3, Yapım Sürecinde)",
    "Ürünün imza tasarım kararını anlatır. Diyagram uygulamadaki LimitBar'ın "
    "ta kendisi — sosyal medya için ayrı bir görsel dil üretilmedi.", C))

# ------------------------------------------- Varyant C2: ne yapar/ne yapmaz
D = "".join([
    kart("#F4F1EA",
         T("ig-lbl", "c-acc", "Trinkow ne yapar") + sp(24)
         + '<span class="ig-h2 c-ink">Günlük limit,<br>hızlı elle giriş,<br>'
           'kalan limiti tek<br>çubukta gösterir.</span>',
         "c-ink2", "1/3"),
    kart("#F4F1EA",
         T("ig-lbl", "c-ink2", "Trinkow şimdilik ne yapmaz") + sp(24)
         + '<span class="ig-h2 c-ink">Bankana bağlanmaz,<br>fişini okumaz.</span>',
         "c-ink2", "2/3"),
    kart("#14484C",
         '<span class="ig-h1 c-paper">Veri cihazında<br>kalır.</span>' + sp(16)
         + '<span class="ig-cap c-paper">Sunucu yok, hesap yok.</span>',
         "c-paper", "3/3"),
])
bloklar.append(kutu(
    "Varyant C2 — Aynı iskelet, dördüncü hafta içeriği (Bekleme Listesi)",
    "Şablon değişmedi, yalnız içerik ve son panelin zemini değişti. Üç varyant "
    "tek sistemden çıkar; her hafta yeni bir görsel dil icat edilmez.", D))

# ---------------------------------------------------------------- profil görseli
prof = div("row",
           div("col mid-x", monogram(160, "#14484C", "#F4F1EA") + sp(8)
               + T("t-micro", "c-ink2", "320×320 profil"), "margin-right:32px")
           + div("col mid-x", monogram(96, "#14484C", "#F4F1EA") + sp(8)
                 + T("t-micro", "c-ink2", "96×96"), "margin-right:32px")
           + div("col mid-x", monogram(40, "#14484C", "#F4F1EA") + sp(8)
                 + T("t-micro", "c-ink2", "40×40"), "margin-right:32px")
           + div("col mid-x", monogram(16, "#14484C", "#F4F1EA") + sp(8)
                 + T("t-micro", "c-ink2", "16×16 (alt sınır)"), "margin-right:32px")
           + div("col mid-x", monogram(96, "#F4F1EA", "#1B1A17") + sp(8)
                 + T("t-micro", "c-ink2", "tek renk"), "margin-right:32px"),
           "align-items:flex-end")

bloklar.append(div("g-item",
                   div("col", prof + sp(24)
                       + div("g-note",
                             T("t-h2", "c-ink", "Profil görseli — monogram") + sp(8)
                             + T("t-caption", "c-ink2",
                                 "brandbook 5.3 geometrisi birebir: 100×100 ızgara, "
                                 "T cap-height 56, taban çizgisi y=78, kolun üstü y=22, "
                                 "kolun sol ucu x=20; çentik x 66→72, y 42→78, köşesi "
                                 "keskin, tam olarak 1 adet.")
                             + sp(8)
                             + T("t-caption", "c-ink2",
                                 "Zemin Petrol #14484C, işaret Kağıt #F4F1EA (9.03:1). "
                                 "Köşe çizilmez — platform maskesi uygular. Degrade, "
                                 "gölge, outline, döndürme yok."),
                             "width:auto;max-width:640px"))))

bloklar.append(div("g-item",
                   div("col",
                       div("row",
                           div("col mid-x mid-y",
                               T("t-splash", "c-acc", "Trinkow"),
                               "width:390px;height:200px;background:#F4F1EA;"
                               "border:1px solid #C9C0AC;border-radius:12px;"
                               "margin-right:24px")
                           + div("col mid-x mid-y",
                                 monogram(200, "#14484C", "#F4F1EA"),
                                 "width:200px;height:200px"))
                       + sp(24)
                       + div("g-note",
                             T("t-h2", "c-ink", "Kelime markası ve uygulama ikonu")
                             + sp(8)
                             + T("t-caption", "c-ink2",
                                 "Kelime markası Source Serif 4 SemiBold, tracking "
                                 "−1.8% (32pt'de −0.58pt), tek satır, uppercase yok. "
                                 "Yalnız üç yerde geçer: açılış, onboarding ilk ekran, "
                                 "ayarlar altbilgisi.")
                             + sp(8)
                             + T("t-caption", "c-ink2",
                                 "Uygulama ikonu 1024×1024 üretilirken monogram kutusu "
                                 "620×620 ve dikeyde 20px yukarı konumlanır (tokens.md 10)."),
                             "width:auto;max-width:640px"))))

bloklar.append(note("Sosyal medya şablonu kararları", [
    "Tüm metinler projects/trinkow/docs/social/icerik-takvimi.md'den birebir alındı; hiçbir cümle uydurulmadı.",
    "Şablon tokens.md'den beslenir: aynı iki font, aynı beş renk, aynı hairline çizgi kalınlığı.",
    "Ünlem ve emoji yok; carousel panel sayacı '1/3' biçiminde, tabular rakam.",
    "Kart ölçüsü 1080×1350 (4:5); prototipte 0.4 ölçekle 432×540 çizildi, iç boşluk 80 → 32.",
    "Tipografi tokens.md §2.5 'sosyal dışa aktarım ölçeği'nden gelir (1080 ızgarası: 100/75/40/35); uygulama ölçeği 1080 tuvale zorlanmadı.",
    "Petrol zeminli panelde çetele çizgileri Kağıt #F4F1EA ile çizilir (9.03:1) — Faz 1 paleti dışında renk yok.",
    "Kırmızı hiçbir sosyal karta girmez; Kiremit yalnız 'taşma' anlatan panelde geçer.",
    "Canva kullanılmadı — kartlar bu HTML/CSS şablonundan ekran görüntüsü olarak dışa aktarılır (K-009: ücretsiz).",
]))

page("Sosyal medya kart şablonu + profil görseli",
     "Instagram tipografik carousel (4:5). 4 şablon varyantı / 11 panel + "
     "monogram profil görseli ve kelime markası.",
     bloklar, "07-sosyal.html")
