# -*- coding: utf-8 -*-
"""E-17 Limitler · E-19 Ayarlar · E-20 Profilleme.
E-17 mood: AYAR MASASI — form agirlikli, her satir tek karar."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from s05_ozet import push
from s02_ekle import sheet_bas


def switch(acik=True, pasif=False):
    track = "#14484C" if acik else "#C9C0AC"
    if pasif:
        track = "#E3DCCC"
    knob = ("margin-left:24px" if acik else "margin-left:4px")
    return div("row shrink0",
               div("", "", f"width:24px;height:24px;border-radius:12px;"
                           f"background:#FFFDF8;{knob}"),
               f"width:52px;height:32px;border-radius:16px;background:{track}")


def ayar_satiri(baslik, aciklama="", sag="", basili=False, renk="c-ink"):
    return div("row between px20",
               div("col grow",
                   f'<span class="t-body {renk}">{baslik}</span>'
                   + (f'<span class="t-caption c-ink2">{aciklama}</span>'
                      if aciklama else ""))
               + (wsp(16) + sag if sag else ""),
               "min-height:64px;padding-top:12px;padding-bottom:12px;background:"
               + ("#F4F1EA" if basili else "#FFFDF8"))


def limit_satiri(kat, deger, durum="default"):
    kutu_cls = {"default": "field", "focused": "field field-focus",
                "error": "field field-err", "bos": "field"}[durum]
    renk = "c-ink3" if durum == "bos" else "c-ink"
    return div("row between px20",
               div("row grow",
                   div("shrink0", ic(CAT_ICON[kat], 20, "#5C574C"), "width:20px")
                   + wsp(16)
                   + f'<span class="t-body c-ink clip1">{kat}</span>')
               + wsp(16)
               + div(kutu_cls + " shrink0",
                     f'<span class="t-amount {renk} tab-num right grow">{deger}</span>'
                     + wsp(8) + T("t-body", "c-ink2", "₺"),
                     "width:136px;height:48px;justify-content:flex-end"),
               "min-height:64px;padding-top:8px;padding-bottom:8px;background:#FFFDF8")


bloklar = []

# ------------------------------------------------------------- E-17 dolu
bloklar.append(item(
    "E-17", "Limitler · dolu",
    "Her satır tek karar. Etiket girdinin üstünde/solunda, placeholder'a "
    "gömülmez. Açıklamalar caption; bilgi notu Petrol şeritli.",
    push("Limitler",
         div("col px20",
             T("t-label", "c-ink2", "Günlük limit") + sp(8)
             + div("field field-focus",
                   '<span class="t-h1 c-ink tab-num right grow">350</span>'
                   + wsp(8) + T("t-h1", "c-ink2", "₺"),
                   "height:64px;justify-content:flex-end")
             + sp(8)
             + T("t-caption", "c-ink2", "Her gün sıfırlanır. Aylık plan değildir."))
         + sp(24) + div("divider") + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Kategori limitleri") + sp(4)
               + T("t-caption", "c-ink2", "Aylık. Boş bırakırsan takip edilmez."))
         + sp(12) + div("divider")
         + limit_satiri("Market", "3.000") + div("divider-56")
         + limit_satiri("Kafe", "1.500") + div("divider-56")
         + limit_satiri("Restoran", "1.500", "focused") + div("divider-56")
         + limit_satiri("Ulaşım", "0", "bos") + div("divider")
         + sp(16)
         + div("row px20",
               div("toast-strip", "", "height:40px;flex-shrink:0") + wsp(12)
               + '<span class="t-caption c-acc grow">Kategori limitleri toplamı'
                 ' 6.000 ₺. Günlük limitinle karşılaştır.</span>',
               "min-height:48px"),
         div("col px20", btn_p("Kaydet"), "padding-top:12px;padding-bottom:12px"))))

# ------------------------------------------------------------- E-17 bos + hata
bloklar.append(item(
    "E-17", "Limitler · kategori limiti yok + hata + loading",
    "Boş hâlde 13 kategori 0 ₺ ile listelenir (gizlenmez). Hata satırı "
    "kenarlığı Vişne; kalınlık 1.5pt sabit, düzen kaymaz.",
    push("Limitler",
         div("col px20",
             T("t-label", "c-ink2", "Günlük limit") + sp(8)
             + div("field field-err",
                   '<span class="t-h1 c-ink tab-num right grow">-50</span>'
                   + wsp(8) + T("t-h1", "c-ink2", "₺"),
                   "height:64px;justify-content:flex-end")
             + sp(8) + T("t-caption", "c-dan", "Limit sıfırdan küçük olamaz."))
         + sp(24) + div("divider") + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Kategori limitleri") + sp(4)
               + T("t-caption", "c-ink2", "Aylık. Boş bırakırsan takip edilmez."))
         + sp(12) + div("divider")
         + limit_satiri("Market", "0", "bos") + div("divider-56")
         + limit_satiri("Kafe", "0", "bos") + div("divider-56")
         + limit_satiri("Restoran", "0", "bos") + div("divider-56")
         + limit_satiri("Kira ve ev", "0", "bos") + div("divider"),
         div("col px20", btn_p("Kaydet", "loading"),
             "padding-top:12px;padding-bottom:12px"))))

# ------------------------------------------------------------- E-19 ayarlar
bloklar.append(item(
    "E-19", "Ayarlar · varsayılan",
    "Sekme değil, panonun sağ üstünden girilir. Her satır tek ayar + tek "
    "açıklama. Marka adı yalnız altbilgide geçer.",
    push("Ayarlar",
         div("divider")
         + ayar_satiri("Akşam özeti", "Günde en fazla bir bildirim.", switch(True))
         + div("divider-56")
         + ayar_satiri("Bildirim saati", "", div("row",
                       T("t-amount", "c-ink", "21.00") + wsp(8)
                       + ic("chevron-right", 20, "#5C574C", 1.75, "Ayrıntıyı aç")))
         + div("divider")
         + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Gün sınırı") + sp(4)
               + T("t-caption", "c-ink2",
                   "Gün bu saatte başlar. Gece geç harcayanlar için.")
               + sp(12)
               + div("row wrap", chip("00.00") + chip("03.00", secili=True)
                     + chip("06.00")))
         + sp(16) + div("divider")
         + ayar_satiri("Varsayılan ödeme", "", div("seg shrink0",
                       div("seg-i", T("t-label", "c-ink2", "Nakit"))
                       + div("seg-i seg-on", T("t-label", "c-acc", "Kart"))))
         + div("divider-56")
         + ayar_satiri("Kip", "Panodaki büyük sayıyı belirler.",
                       div("row", T("t-body", "c-ink2", "Takip") + wsp(8)
                           + ic("chevron-right", 20, "#5C574C", 1.75, "Ayrıntıyı aç")))
         + div("divider")
         + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Veri") + sp(4)
               + T("t-caption", "c-ink2",
                   "Kayıtların yalnızca bu cihazda. Hesap yok, sunucu yok."))
         + sp(12) + div("divider")
         + div("row px20",
               ic("trash", 24, "#8E2F20", 1.75, "Tüm verileri sil") + wsp(8)
               + T("t-bodys", "c-dan", "Tüm verileri sil"),
               "min-height:64px;background:#FFFDF8")
         + div("divider")
         + sp(32)
         + div("col px20 mid-x",
               T("t-h2", "c-acc", "Trinkow") + sp(4)
               + T("t-micro", "c-ink3", "Sürüm 1.0.0"))
         + sp(24))))

bloklar.append(item(
    "E-19", "Ayarlar · bildirim izni kapalı + basılı satır",
    "İzin reddedilmişse anahtar pasif (renkle, opaklıkla değil) ve satır "
    "açıklaması değişir. Kullanıcı cihaz ayarına yönlendirilir.",
    push("Ayarlar",
         div("divider")
         + ayar_satiri("Akşam özeti",
                       "Bildirim izni kapalı. Cihaz ayarlarından açabilirsin.",
                       switch(False, pasif=True))
         + div("divider-56")
         + ayar_satiri("Bildirim saati", "", div("row",
                       T("t-amount", "c-ink3", "21.00") + wsp(8)
                       + ic("chevron-right", 20, "#6F6A5C", 1.75, "Ayrıntıyı aç")),
                       basili=False)
         + div("divider")
         + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Gün sınırı") + sp(4)
               + T("t-caption", "c-ink2",
                   "Gün bu saatte başlar. Gece geç harcayanlar için.")
               + sp(12)
               + div("row wrap", chip("00.00", basili=True) + chip("03.00", secili=True)
                     + chip("06.00")))
         + sp(16) + div("divider")
         + ayar_satiri("Varsayılan ödeme", "", div("seg shrink0",
                       div("seg-i seg-on", T("t-label", "c-acc", "Nakit"))
                       + div("seg-i", T("t-label", "c-ink2", "Kart"))))
         + div("divider-56")
         + ayar_satiri("Kip", "Panodaki büyük sayıyı belirler.",
                       div("row", T("t-body", "c-ink2", "Borç") + wsp(8)
                           + ic("chevron-right", 20, "#5C574C", 1.75, "Ayrıntıyı aç")),
                       basili=True)
         + div("divider")
         + sp(24)
         + div("col px20",
               T("t-label", "c-ink2", "Veri") + sp(4)
               + T("t-caption", "c-ink2",
                   "Kayıtların yalnızca bu cihazda. Hesap yok, sunucu yok."))
         + sp(12) + div("divider")
         + div("row px20 bg-ghostp",
               ic("trash", 24, "#8E2F20", 1.75, "Tüm verileri sil") + wsp(8)
               + T("t-bodys", "c-dan", "Tüm verileri sil"),
               "min-height:64px")
         + div("divider"))))


# ------------------------------------------------------------- E-20 profilleme
def sheet_frame_basit(ic_, arka):
    return ('<div class="frame">' + chrome_top()
            + div("scroll", arka + div("scrim", div("sheet", ic_)),
                  "position:relative")
            + chrome_bottom() + '</div>')


ARKA = div("col",
           div("row between px20",
               T("t-h1", "c-ink", "Bugün") + iconbtn("settings", "Ayarları aç"),
               "min-height:44px")
           + sp(32)
           + div("col px20",
                 T("t-label", "c-ink2", "bugün kalan") + sp(4)
                 + T("t-display", "c-ink", "120 ₺") + sp(24) + limitbar(180, 300)))

bloklar.append(div("g-item", sheet_frame_basit(
    sheet_bas("Tek soru") + sp(8)
    + div("col px20",
          T("t-h2", "c-ink", "Taksitli alışveriş yapar mısın") + sp(8)
          + T("t-caption", "c-ink3", "Cevabın cihazda kalır.")
          + sp(16)
          + div("row wrap", chip("Sık sık") + chip("Bazen", secili=True)
                + chip("Neredeyse hiç")))
    + sp(8)
    + div("row px20", btn_g("Şimdi değil", "default", "c-ink2",
                            "align-self:flex-start;padding-left:0;padding-right:0"))
    + sp(12), ARKA)
    + div("g-cap", T("t-label", "c-acc", "E-20 · profilleme sorusu (3. gün)")
          + sp(4) + T("t-caption", "c-ink2",
                      "Günde en fazla 1 soru, toplam 3. Reddedilen soru 14 gün "
                      "geri gelmez; üçü de cevaplanınca bileşen kaybolur."))))

bloklar.append(div("g-item", sheet_frame_basit(
    sheet_bas("Tek soru", kapat_basili=True) + sp(8)
    + div("col px20",
          T("t-h2", "c-ink", "Akşam kısa bir özet göndereyim mi") + sp(8)
          + T("t-caption", "c-ink3", "Cevabın cihazda kalır.")
          + sp(16)
          + div("row wrap", chip("Gönder") + chip("Gönderme", basili=True)))
    + sp(8)
    + div("row px20", btn_g("Şimdi değil", "pressed", "c-ink2",
                            "align-self:flex-start;padding-left:20px;padding-right:20px"))
    + sp(12), ARKA)
    + div("g-cap", T("t-label", "c-acc", "E-20 · basılı hâller")
          + sp(4) + T("t-caption", "c-ink2",
                      "Kapat ikon-butonu 44pt hedef, basılıyken 12 radius kare "
                      "zemin (daire değil). Çip ve ghost buton de basılı."))))

bloklar.append(note("E-17 / E-19 / E-20 kararları", [
    "Ayarlar sekme değil: günde bir kez bile açılmayan yüzey, günde 5 kez basılan çubukta yer kaplamaz.",
    "Kategori limit satırında girdi 136pt sabit genişlik — 13 satır boyunca rakamlar dikeyde hizalanır.",
    "'Kategori limitleri toplamı' çelişki notu engelleyici değil bilgilendirici; Kaydet'i kilitlemez.",
    "'Tüm verileri sil' tek başına Vişne metin; onayı E-13 ile aynı Dialog kalıbını kullanır.",
    "Switch RN'in kendi Switch'i; özel switch çizilmedi, pasif hâl renkle verildi.",
    "Ayarlar altbilgisi brandbook 5.1'e göre kelime markasının geçtiği üç yerden biri.",
]))

page("E-17 · Limitler + E-19 Ayarlar + E-20 profilleme",
     "Ayar masası. 6 kare: limitler (dolu / boş + hata + loading) · ayarlar "
     "(varsayılan / izin kapalı + basılı) · profilleme sheet (2 durum).",
     bloklar, "06-ayarlar.html")
