# -*- coding: utf-8 -*-
"""E-11 — Harcama ekle (BottomSheet). Mood: hizli, klavye oncelikli.
Dokunus butcesi 3: [1] Harcama ekle · [2] kategori cipi · [3] Kaydet."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

KATS = ["Kafe", "Market", "Ulaşım", "Restoran", "Akaryakıt", "Fatura"]


def katchip(ad, secili=False, basili=False):
    renk = "#14484C" if secili else "#5C574C"
    cls = "chip chip-sel" if secili else ("chip chip-press" if basili else "chip")
    tr = "c-acc" if secili else "c-ink2"
    return div(cls + " shrink0",
               ic(CAT_ICON[ad], 20, renk) + wsp(8) + T("t-label", tr, ad),
               "margin-right:8px;margin-bottom:8px")


def tumu_chip(basili=False):
    cls = "chip chip-press" if basili else "chip"
    return div(cls + " shrink0",
               T("t-label", "c-ink2", "Tüm kategoriler") + wsp(8)
               + ic("chevron-down", 20, "#5C574C", 1.75, "Listeyi genişlet"),
               "margin-right:8px;margin-bottom:8px")


def amountbox(sayi, durum="focused", cls="t-display", renk="c-ink"):
    b = {"focused": "field field-focus", "default": "field",
         "error": "field field-err"}[durum]
    caret = div("caret") + wsp(8) if durum == "focused" else ""
    return div(b, div("row grow", "", "justify-content:flex-end")
               + caret
               + f'<span class="{cls} {renk} tab-num">{sayi}</span>'
               + wsp(8)
               + T("t-h1", "c-ink2", "₺"),
               "height:64px;justify-content:flex-end")


def odeme_satiri(nakit=False, taksit_link=True, tarih="Bugün"):
    seg = div("seg shrink0",
              div("seg-i" + (" seg-on" if nakit else ""),
                  ic("banknote", 20, "#14484C" if nakit else "#5C574C", 1.75, "Nakit")
                  + wsp(8) + T("t-label", "c-acc" if nakit else "c-ink2", "Nakit"))
              + div("seg-i" + ("" if nakit else " seg-on"),
                    ic("credit-card", 20, "#5C574C" if nakit else "#14484C", 1.75, "Kart")
                    + wsp(8) + T("t-label", "c-ink2" if nakit else "c-acc", "Kart")))
    sag = div("row shrink0",
              div("chip shrink0", T("t-label", "c-ink2", tarih), "margin-right:8px")
              + (T("t-label", "c-acc", "Taksitli") if taksit_link else ""))
    return div("row between px20", seg + wsp(12) + sag, "min-height:44px")


def uyari(metin, tur="edge"):
    strip = "toast-strip-edge" if tur == "edge" else "toast-strip"
    renk = "c-edge" if tur == "edge" else "c-acc"
    return div("row px20",
               div(strip, "", "height:40px;flex-shrink:0") + wsp(12)
               + f'<span class="t-caption {renk} grow">{metin}</span>',
               "min-height:48px")


def hata(metin):
    return div("col px20", sp(8) + T("t-caption", "c-dan", metin))


def klavye(basili=""):
    tuslar = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], [",", "0", "sil"]]
    out = ""
    for satir in tuslar:
        r = ""
        for t in satir:
            cls = "kbkey kbkey-press" if t == basili else "kbkey"
            if t == "sil":
                r += div(cls, T("t-h2", "c-ink2", "⌫"))
            else:
                r += div(cls, T("t-h1", "c-ink", t))
        out += div("kbrow", r)
    return div("keyboard", sp(8) + out + sp(8))


def pano_arka():
    return div("col",
               div("row between px20",
                   T("t-h1", "c-ink", "Bugün") + iconbtn("settings", "Ayarları aç"),
                   "min-height:44px")
               + sp(32)
               + div("col px20",
                     T("t-label", "c-ink2", "bugün kalan") + sp(4)
                     + T("t-display", "c-ink", "120 ₺") + sp(24)
                     + limitbar(180, 300)))


def sheet_frame(sheet_ic, kb=None, arka=None):
    icerik = (arka if arka else pano_arka())
    kutu = div("scroll", icerik + div("scrim", div("sheet", sheet_ic)),
               "position:relative")
    return ('<div class="frame">' + chrome_top() + kutu
            + (kb if kb else "") + chrome_bottom() + '</div>')


def sheet_bas(baslik="Harcama ekle", kapat_basili=False):
    return (sp(8) + div("row mid-y", div("sheet-grab"), "justify-content:center")
            + sp(8)
            + div("row between px20",
                  T("t-h2", "c-ink", baslik)
                  + iconbtn("x", "Kapat", kapat_basili), "min-height:44px"))


def alan(etiket, govde):
    return div("col px20", T("t-label", "c-ink2", etiket) + sp(8)) + div("col px20", govde)


def kat_alani(secili=None, basili=None, genis=False):
    liste = KATS if not genis else list(CAT_ICON.keys())
    c = ""
    for k in liste:
        c += katchip(k, secili == k, basili == k)
    if not genis:
        c += tumu_chip()
    return div("col px20",
               T("t-label", "c-ink2", "Kategori") + sp(8)
               + div("row wrap", c))


if __name__ == "__main__":
    bloklar = []

    # ------------------------------------------------------- 1. acilis (dokunus 1)
    bloklar.append(item(
        "E-11", "Harcama ekle · sheet açıldı (tutar boş)",
        "Dokunuş 1 tamamlandı. AmountField otomatik odaklı, klavye hazır — "
        "alana dokunmak gerekmez. Kaydet pasif (renkle, opaklıkla değil).",
        "", bg="#F4F1EA"))
    bloklar[-1] = div("g-item",
                      sheet_frame(sheet_bas() + sp(16)
                                  + alan("Tutar", amountbox("0", "focused", "t-display", "c-ink3"))
                                  + sp(16) + kat_alani()
                                  + sp(8) + odeme_satiri()
                                  + sp(16) + div("col px20", btn_p("Kaydet", "disabled"))
                                  + sp(12), klavye())
                      + div("g-cap", T("t-label", "c-acc", "E-11 · sheet açıldı (tutar boş)") + sp(4)
                            + T("t-caption", "c-ink2",
                                "Dokunuş 1 bitti. Alan otomatik odaklı, klavye hazır. "
                                "Kaydet pasif: zemin #E3DCCC, metin #5C574C — opaklık yok.")))


    def kutu(kod, ad, notu, sheet_ic, kb=None, arka=None):
        return div("g-item",
                   sheet_frame(sheet_ic, kb, arka)
                   + div("g-cap", T("t-label", "c-acc", kod + " · " + ad) + sp(4)
                         + T("t-caption", "c-ink2", notu)))


    # ------------------------------------------------------- 2. tutar yazildi
    bloklar.append(kutu(
        "E-11", "tutar yazılıyor · kategori seçilmedi",
        "Binlik ayracı yazarken canlı biçimlenir. Kategori önceden seçili "
        "GELMEZ — yanlış kategoriye sessiz kayıt riski yerine 1 dokunuş ödenir.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("1.250,50"))
        + sp(16) + kat_alani(basili="Kafe")
        + sp(8) + odeme_satiri()
        + sp(16) + div("col px20", btn_p("Kaydet", "disabled"))
        + sp(12), klavye("5")))

    # ------------------------------------------------------- 3. hazir (dokunus 2 bitti)
    bloklar.append(kutu(
        "E-11", "kategori seçildi · kaydetmeye hazır",
        "Dokunuş 2 bitti. Seçili çipte onay ikonu yok — zemin ve kenarlık "
        "yeterli (8.06:1). Kaydet klavyenin hemen üstünde.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("180"))
        + sp(16) + kat_alani(secili="Kafe")
        + sp(8) + odeme_satiri()
        + sp(16) + div("col px20", btn_p("Kaydet"))
        + sp(12), klavye()))

    # ------------------------------------------------------- 4. limit disi uyarisi
    bloklar.append(kutu(
        "E-11", "kaydetmeden önce limit dışı bilgisi",
        "Kayıt ENGELLENMEZ. Kırmızı değil Kiremit şerit; ünlem, uyarı ikonu ve "
        "modal yok. Kullanıcı durdurulmaz, bilgilendirilir.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("180"))
        + sp(16) + kat_alani(secili="Restoran")
        + sp(8) + odeme_satiri()
        + sp(8) + uyari("Bu harcama günlük limitin 60 ₺ üzerine çıkarır.")
        + sp(8) + div("col px20", btn_p("Kaydet", "pressed"))
        + sp(12), klavye()))

    # ------------------------------------------------------- 5. kaydediliyor
    bloklar.append(kutu(
        "E-11", "Kaydet · loading (dokunuş 3)",
        "Yazma işlemi her zaman buton loading'i kullanır. Genişlik sabit, "
        "metin 'Kaydediliyor', buton disabled. Scale animasyonu yok.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("180", "default"))
        + sp(16) + kat_alani(secili="Kafe")
        + sp(8) + odeme_satiri()
        + sp(16) + div("col px20", btn_p("Kaydet", "loading"))
        + sp(12), klavye()))

    # ------------------------------------------------------- 6. hatalar
    bloklar.append(kutu(
        "E-11", "doğrulama hataları",
        "'Hata:', 'Geçersiz', ünlem ve büyük harf uyarı yok. Kenarlık kalınlığı "
        "değişmez (1.5pt) — düzen kaymaz, yalnız renk döner.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("0", "error", "t-display", "c-ink3"))
        + hata("Tutar boş kalamaz.")
        + sp(16) + kat_alani()
        + hata("Bir kategori seç.")
        + sp(8) + div("row between px20",
                      div("seg shrink0",
                          div("seg-i", ic("banknote", 20, "#5C574C") + wsp(8)
                              + T("t-label", "c-ink2", "Nakit"))
                          + div("seg-i seg-on", ic("credit-card", 20, "#14484C") + wsp(8)
                                + T("t-label", "c-acc", "Kart")))
                      + div("chip", T("t-label", "c-dan", "11 Eylül")), "min-height:44px")
        + hata("Gelecek tarihe harcama yazılamaz.")
        + sp(12) + div("col px20", btn_p("Kaydet", "disabled"))
        + sp(12), klavye()))

    # ------------------------------------------------------- 7. uzun tutar
    bloklar.append(kutu(
        "E-11", "uzun tutar · 44pt → 28pt tek kademe",
        "1.250.000,50 ₺ taşmadan sığar. Punto tek kademe düşer (ara değer yok). "
        "Sınır 9.999.999,99 ₺; üstü kabul edilmez.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("1.250.000,50", "focused", "t-h1"))
        + sp(16) + kat_alani(secili="Kira ve ev") if False else
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("1.250.000,50", "focused", "t-h1"))
        + sp(16)
        + div("col px20",
              T("t-label", "c-ink2", "Kategori") + sp(8)
              + div("row wrap", katchip("Kafe") + katchip("Market")
                    + katchip("Kira ve ev", True) + katchip("Fatura") + tumu_chip()))
        + sp(8) + odeme_satiri()
        + sp(16) + div("col px20", btn_p("Kaydet"))
        + sp(12), klavye()))

    # ------------------------------------------------------- 8. tum kategoriler
    bloklar.append(kutu(
        "E-11", "Tüm kategoriler açık (expanded)",
        "13 sabit kategori. Renk YOK — ayrım yalnız ikon + isim. Çip 32pt, "
        "dokunma hedefi hitSlop ile 44pt'ye tamamlanır.",
        sheet_bas("Kategori seç") + sp(16)
        + kat_alani(secili="Alışkanlıklar", genis=True)
        + sp(16) + div("col px20", btn_s("Geri", "default"))
        + sp(12)))

    # ------------------------------------------------------- 9. taksit
    bloklar.append(kutu(
        "E-11", "Taksitli · InstallmentPicker",
        "Yalnız Kart seçiliyken görünür. Nakite dönülürse taksit sessizce "
        "sıfırlanır. +3 dokunuş: bilinçli olarak varsayılan akışın dışında.",
        sheet_bas("Kaç taksit") + sp(16)
        + div("col px20",
              div("row wrap", chip("2") + chip("3") + chip("6") + chip("9")
                  + chip("12", True)))
        + sp(8)
        + div("col px20",
              div("card", T("t-label", "c-ink2", "Önizleme") + sp(8)
                  + T("t-amount", "c-ink", "Ayda 1.041,67 ₺ · 12 ay") + sp(8)
                  + T("t-caption", "c-ink3",
                      "Taksitler girildiği güne değil, ait olduğu aya yazılır.")))
        + sp(16) + div("col px20", btn_p("Uygula"))
        + sp(12)))

    # ------------------------------------------------------- 10. not + nakit
    bloklar.append(kutu(
        "E-11", "not alanı · uzun metin · nakit",
        "Not isteğe bağlı, 60 karakter. Sayaç yalnız son 10 karakterde görünür. "
        "Nakit seçilince Taksitli bağlantısı görünmez.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("420,00", "default"))
        + sp(16) + kat_alani(secili="Restoran")
        + sp(8) + odeme_satiri(nakit=True, taksit_link=False, tarih="Dün")
        + sp(12)
        + div("col px20",
              div("row between", T("t-label", "c-ink2", "Not (isteğe bağlı)")
                  + T("t-micro", "c-ink3", "3"))
              + sp(8)
              + div("field field-focus",
                    '<span class="t-body c-ink clip1 grow">Akşam yemeği, iki kişi,'
                    ' arkadaşımla ödeme sonradan bölündü</span>'))
        + sp(16) + div("col px20", btn_p("Kaydet"))
        + sp(12)))

    # ------------------------------------------------------- 11. yazma hatasi
    bloklar.append(kutu(
        "E-11", "yazma hatası",
        "Sheet kapanmaz, girilen veri korunur. Hata satırı Toast değil sheet "
        "içinde — kullanıcı düzeltmeyi burada yapar.",
        sheet_bas() + sp(16)
        + alan("Tutar", amountbox("180", "default"))
        + sp(16) + kat_alani(secili="Kafe")
        + sp(8) + odeme_satiri()
        + sp(8) + uyari("Kayıt yazılamadı. Yeniden dene.", "info")
        + sp(8) + div("col px20", btn_p("Kaydet"))
        + sp(12), klavye()))

    bloklar.append(note("E-11 dokunuş bütçesi ve bilinçli kararlar", [
        "3 dokunuş: [1] Pano'da 'Harcama ekle' · [2] kategori çipi · [3] Kaydet. Rakam tuşları veri girişidir, sayılmaz.",
        "Otomatik odak 1 dokunuş kazandırır: alana dokunmaya gerek yok, klavye sheet ile birlikte gelir.",
        "Ekran değil sheet: Pano'nun üst şeridi görünür kalır, kaydedince çubuğun hareketi aynı karede görülür.",
        "Varsayılanlar 0 dokunuş: tarih Bugün · ödeme Kart · taksit yok · not boş.",
        "Kaydet klavyenin üstünde sabit (KeyboardAvoidingView) — kaydırma yok.",
        "Klavye OS yüzeyidir; ⌫ sistem tuşudur, uygulama ikonu değildir (Lucide kilidi dışında).",
        "Gölge istisnası yalnız burada: sheet üst kenarında iOS shadow / Android elevation 8 + scrim.",
    ]))

    page("E-11 · Harcama ekle",
         "En çok kullanılan yüzey. 11 durum: boş · yazılıyor · hazır · limit dışı "
         "bilgisi · loading · hatalar · uzun tutar · tüm kategoriler · taksit · not · yazma hatası.",
         bloklar, "02-harcama-ekle.html")
