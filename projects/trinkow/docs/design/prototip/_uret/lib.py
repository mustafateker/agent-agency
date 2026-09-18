# -*- coding: utf-8 -*-
"""Trinkow prototip uretici — ortak kutuphane.
Cikti: projects/trinkow/docs/design/prototip/*.html (statik, tek basina acilir).
Bu dosya sadece uretim araci; teslim edilen sey uretilen HTML'dir.
"""
from __future__ import annotations
import os
from typing import List

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --------------------------------------------------------------------------
# Lucide 1.43.0 ikon govdeleri (24x24 viewBox, stroke 1.75, dolgu yok)
# varliklar.md 1.1 + 1.2 disinda ikon YOK.
# --------------------------------------------------------------------------
ICONS = {
 'shopping-basket': '<path d="m15 11-1 9"/><path d="m19 11-4-7"/><path d="M2 11h20"/><path d="m3.5 11 1.6 7.4a2 2 0 0 0 2 1.6h9.8a2 2 0 0 0 2-1.6l1.7-7.4"/><path d="M4.5 15.5h15"/><path d="m5 11 4-7"/><path d="m9 11 1 9"/>',
 'coffee': '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>',
 'utensils': '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
 'bus': '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
 'fuel': '<path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 4 0v-6.998a2 2 0 0 0-.59-1.42L18 5"/><path d="M14 21V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v16"/><path d="M2 21h13"/><path d="M3 9h11"/>',
 'receipt-text': '<path d="M13 16H8"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M4 3a1 1 0 0 1 1-1 1.3 1.3 0 0 1 .7.2l.933.6a1.3 1.3 0 0 0 1.4 0l.934-.6a1.3 1.3 0 0 1 1.4 0l.933.6a1.3 1.3 0 0 0 1.4 0l.933-.6a1.3 1.3 0 0 1 1.4 0l.934.6a1.3 1.3 0 0 0 1.4 0l.933-.6A1.3 1.3 0 0 1 19 2a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1 1.3 1.3 0 0 1-.7-.2l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.934.6a1.3 1.3 0 0 1-1.4 0l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-1.4 0l-.934-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-.7.2 1 1 0 0 1-1-1z"/>',
 'house': '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 'repeat': '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
 'pill': '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
 'shirt': '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>',
 'ticket': '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/>',
 'footprints': '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
 'circle-dashed': '<path d="M10.1 2.182a10 10 0 0 1 3.8 0"/><path d="M13.9 21.818a10 10 0 0 1-3.8 0"/><path d="M17.609 3.721a10 10 0 0 1 2.69 2.7"/><path d="M2.182 13.9a10 10 0 0 1 0-3.8"/><path d="M20.279 17.609a10 10 0 0 1-2.7 2.69"/><path d="M21.818 10.1a10 10 0 0 1 0 3.8"/><path d="M3.721 6.391a10 10 0 0 1 2.7-2.69"/><path d="M6.391 20.279a10 10 0 0 1-2.69-2.7"/>',
 'gauge': '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
 'notebook-text': '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9.5 8h5"/><path d="M9.5 12H16"/><path d="M9.5 16H14"/>',
 'chart-no-axes-column': '<path d="M5 21v-6"/><path d="M12 21V3"/><path d="M19 21V9"/>',
 'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
 'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
 'chevron-left': '<path d="m15 18-6-6 6-6"/>',
 'chevron-right': '<path d="m9 18 6-6-6-6"/>',
 'chevron-down': '<path d="m6 9 6 6 6-6"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'trash': '<path d="M10 11v6"/><path d="M14 11v6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
 'pen-line': '<path d="M13 21h8"/><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>',
 'settings': '<path d="M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915"/><circle cx="12" cy="12" r="3"/>',
 'rotate-cw': '<path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>',
 'undo-2': '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"/>',
 'layers': '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"/><path d="M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12"/><path d="M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17"/>',
 'banknote': '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
 'credit-card': '<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
 'bell': '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>',
}

CAT_ICON = {
 "Market": "shopping-basket", "Kafe": "coffee", "Restoran": "utensils",
 "Ulaşım": "bus", "Akaryakıt": "fuel", "Fatura": "receipt-text",
 "Kira ve ev": "house", "Abonelik": "repeat", "Sağlık": "pill",
 "Giyim": "shirt", "Eğlence": "ticket", "Alışkanlıklar": "footprints",
 "Diğer": "circle-dashed",
}


def ic(name: str, size: int = 24, color: str = "#5C574C", sw: float = 1.75, label: str = "") -> str:
    """Lucide ikon. RN karsiligi: <Icon size color strokeWidth /> (lucide-react-native)."""
    body = ICONS[name]
    a = f' aria-label="{label}" role="img"' if label else ' aria-hidden="true"'
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round"{a}>{body}</svg>')


# --------------------------------------------------------------------------
# Metin ve bosluk
# --------------------------------------------------------------------------
def T(cls: str, color: str, text: str, extra: str = "") -> str:
    e = f' {extra}' if extra else ''
    return f'<span class="{cls} {color}"{e}>{text}</span>'


def sp(n: int) -> str:
    return f'<div class="h{n}"></div>'


def wsp(n: int) -> str:
    return f'<div class="w{n}"></div>'


def div(cls: str, inner: str = "", style: str = "") -> str:
    s = f' style="{style}"' if style else ''
    return f'<div class="{cls}"{s}>{inner}</div>'


# --------------------------------------------------------------------------
# Cihaz cercevesi
# --------------------------------------------------------------------------
def chrome_top(saat: str = "21.30") -> str:
    return div("chrome-top",
               T("t-label", "c-ink", saat, 'style="width:64px"')
               + div("chrome-island")
               + div("row", div("", "", "width:18px;height:8px;border-radius:4px;background:#C9C0AC")
                     + wsp(4)
                     + div("", "", "width:22px;height:11px;border-radius:4px;background:#1B1A17"),
                     "width:64px;justify-content:flex-end"))


def chrome_bottom() -> str:
    return div("chrome-bottom", div("chrome-bar"))


def frame(inner: str, saat: str = "21.30", bg: str = "#F4F1EA") -> str:
    return (f'<div class="frame" style="background:{bg}">'
            + chrome_top(saat) + inner + chrome_bottom() + '</div>')


# --------------------------------------------------------------------------
# Galeri iskelesi (PROTOTIP DISI)
# --------------------------------------------------------------------------
def item(kod: str, ad: str, not_: str, inner: str, saat: str = "21.30", bg: str = "#F4F1EA") -> str:
    return div("g-item",
               frame(inner, saat, bg)
               + div("g-cap",
                     T("t-label", "c-acc", kod + " · " + ad)
                     + sp(4)
                     + T("t-caption", "c-ink2", not_)))


def note(baslik: str, satirlar: List[str]) -> str:
    body = T("t-h2", "c-ink", baslik) + sp(8)
    for s in satirlar:
        body += T("t-caption", "c-ink2", s) + sp(8)
    return div("g-item", div("g-note", body))


def page(baslik: str, altbaslik: str, bloklar: List[str], dosya: str) -> None:
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trinkow — {baslik}</title>
<link rel="stylesheet" href="stil.css">
</head>
<body>
<div class="g-page">
  <div class="col">
    <span class="t-h1 c-ink">{baslik}</span>
    <div class="h8"></div>
    <span class="t-body c-ink2">{altbaslik}</span>
    <div class="h8"></div>
    <a class="g-link" href="index.html">Tüm yüzeylere dön</a>
    <div class="h32"></div>
  </div>
  <div class="g-strip">
    {"".join(bloklar)}
  </div>
</div>
</body>
</html>
'''
    yol = os.path.join(OUT, dosya)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(html)
    print("yazildi:", yol, len(html), "bayt")


# --------------------------------------------------------------------------
# Yeniden kullanilan bilesenler
# --------------------------------------------------------------------------
def limitbar(harcanan: int, limit: int, durum: str = "default") -> str:
    """tokens.md 7.5 — doluluga gore RENK DEGISMEZ. Tasma ayri segment."""
    if durum == "skeleton":
        return div("barwrap", div("bar-seg bar-l bar-r", "", "flex:1 1 0"))
    if durum == "empty" or harcanan <= 0:
        return div("barwrap",
                   div("bar-seg bar-l bar-r", "", "flex:1 1 0") + div("bar-thr"))
    if harcanan >= limit and harcanan > limit:
        tasma = harcanan - limit
        return div("barwrap",
                   div("bar-fill bar-l", "", f"flex:{limit} 1 0")
                   + div("bar-thr")
                   + div("bar-over bar-r", "", f"flex:{tasma} 1 0"))
    if harcanan == limit:
        return div("barwrap", div("bar-fill bar-l bar-r", "", "flex:1 1 0") + div("bar-thr"))
    kalan = limit - harcanan
    return div("barwrap",
               div("bar-fill bar-l", "", f"flex:{harcanan} 1 0")
               + div("bar-seg bar-r", "", f"flex:{kalan} 1 0")
               + div("bar-thr"))


def chip(metin: str, secili: bool = False, basili: bool = False, pasif: bool = False) -> str:
    cls, renk = "chip", "c-ink2"
    if secili:
        cls, renk = "chip chip-sel", "c-acc"
    if basili:
        cls, renk = "chip chip-press", "c-ink2"
    if pasif:
        cls, renk = "chip chip-dis", "c-ink3"
    return div(cls + " shrink0", T("t-label", renk, metin), "margin-right:8px;margin-bottom:8px")


def btn_p(metin: str, durum: str = "default", genislik: str = "align-self:stretch") -> str:
    cls, renk, ic_ = "btn-p", "c-page", T("t-bodys", "c-page", metin)
    if durum == "pressed":
        cls = "btn-p btn-p-press"
    elif durum == "disabled":
        cls, ic_ = "btn-p btn-p-dis", T("t-bodys", "c-ink2", metin)
    elif durum == "loading":
        cls = "btn-p"
        ic_ = T("t-bodys", "c-page", "Kaydediliyor") + wsp(8) + div("spin-acc")
    return div(cls, ic_, genislik)


def btn_s(metin: str, durum: str = "default", genislik: str = "align-self:stretch") -> str:
    cls = "btn-s btn-s-press" if durum == "pressed" else "btn-s"
    return div(cls, T("t-bodys", "c-acc", metin), genislik)


def btn_g(metin: str, durum: str = "default", renk: str = "c-ink2",
          style: str = "align-self:flex-start") -> str:
    cls = "btn-g btn-g-press" if durum == "pressed" else "btn-g"
    return div(cls, T("t-bodys", renk, metin), style)


def iconbtn(name: str, label: str, basili: bool = False, color: str = "#5C574C") -> str:
    cls = "iconbtn iconbtn-press" if basili else "iconbtn"
    return div(cls, ic(name, 24, color, 1.75, label))


def spendrow(kategori: str, alt: str, tutar: str, durum: str = "default",
             taksit: bool = False) -> str:
    cls = "srow"
    tutar_renk = "c-ink"
    if durum == "pressed":
        cls = "srow srow-press"
    elif durum == "overflow":
        cls, tutar_renk = "srow srow-edge", "c-edge"
    sol = div("shrink0", ic(CAT_ICON[kategori], 20, "#5C574C"), "width:20px")
    orta = div("col grow",
               T("t-body", "c-ink", kategori, 'class="t-body c-ink clip1"')
               + T("t-caption", "c-ink2", alt))
    # duzeltme: clip1 dogru uygulansin
    orta = div("col grow",
               f'<span class="t-body c-ink clip1">{kategori}</span>'
               + f'<span class="t-caption c-ink2 clip1">{alt}</span>')
    sag = div("col shrink0",
              f'<span class="t-amount {tutar_renk} right">{tutar}</span>',
              "align-items:flex-end;min-width:96px")
    tk = (wsp(8) + ic("layers", 20, "#5C574C")) if taksit else ""
    return div(cls, sol + wsp(16) + orta + wsp(12) + sag + tk)


def tabbar(aktif: str = "bugun", basili: str = "", odak: str = "") -> str:
    tabs = [("bugun", "gauge", "Bugün"), ("kayitlar", "notebook-text", "Kayıtlar"),
            ("ozet", "chart-no-axes-column", "Özet")]
    out = ""
    for key, icon_ad, ad in tabs:
        on = key == aktif
        renk = "#14484C" if on else "#5C574C"
        sw = 2.0 if on else 1.75
        cls = "tabitem tabitem-press" if key == basili else "tabitem"
        etiket = f'<span class="t-label {"c-acc" if on else "c-ink2"}">{ad}</span>' if on else \
                 f'<span class="t-caption c-ink2">{ad}</span>'
        # Ikon 28 (varliklar.md) + etiket satir kutusu 18 = 46 <= 48pt icerik kutusu.
        # Ayrica bosluk konmaz: ikonun ic payi + etiketin satir arasi optik 4pt verir.
        icerik = ic(icon_ad, 28, renk, sw, ad + " sekmesi") + etiket
        if key == odak:
            # Halka: 48 + 2pt bosluk + 2pt kenarlik = 56 = bar yuksekligi. Tasma yok.
            oge = div("focusring", div(cls, icerik, "flex:0 0 auto;align-self:stretch"),
                      "flex:1 1 0")
        else:
            oge = div(cls, icerik)
        out += oge
    return div("tabbar", out)


def toast(metin: str, tur: str = "info", eylem: str = "") -> str:
    strip = {"info": "toast-strip", "edge": "toast-strip-edge", "dan": "toast-strip-dan"}[tur]
    sag = ""
    if eylem:
        sag = wsp(12) + div("row shrink0", ic("undo-2", 20, "#14484C", 1.75, "İşlemi geri al")
                            + wsp(8) + T("t-label", "c-acc", eylem))
    govde = div("row grow",
                f'<span class="t-body c-ink clip1">{metin}</span>')
    return div("toast", div(strip) + wsp(12) + govde + sag,
               "align-self:stretch;padding-left:0")


def tally(n: int = 5, renk: str = "#C9C0AC") -> str:
    """TallyGraphic — markanin tek cizim primitifi (varliklar.md 3)."""
    marks = ""
    for i in range(4):
        marks += div("tallymark", "", f"background:{renk};margin-right:8px")
    marks += div("tallyslash", "", f"background:{renk};margin-left:-18px")
    return div("tally", marks)


def skeleton(w: str, h: int, mb: int = 12) -> str:
    return div("sk", "", f"width:{w};height:{h}px;margin-bottom:{mb}px")


def stepind(adim: int) -> str:
    cent = ""
    for i in range(1, 4):
        renk = "#14484C" if i <= adim else "#DCD5C6"
        cent += div("", "", f"width:20px;height:1.75px;background:{renk};margin-left:4px")
    return div("row", T("t-label", "c-ink2", f"Adım {adim}/3") + wsp(8) + div("row", cent))


def header(baslik: str, sag: str = "", geri: bool = False) -> str:
    sol = ""
    if geri:
        sol = iconbtn("chevron-left", "Geri dön") + wsp(4)
    return div("row between px20",
               div("row grow", sol + f'<span class="t-h1 c-ink clip1">{baslik}</span>')
               + (sag if sag else ""),
               "min-height:44px")


def monogram(boyut: int, zemin: str, murekkep: str) -> str:
    """brandbook 5.3 geometrisi, 100x100 izgara.
    Source Serif 4 SemiBold 'T': cap-height 664/1000 em -> punto = 56/0.664 = 84.34.
    Glif sol kenarligi 22/1000 em = 1.85 birim, bu yuzden origin x = 20 - 1.85 = 18.15.
    Taban cizgisi y = 78. Centik: x 66->72, y 42->78, kose keskin, tam 1 adet.
    RN karsiligi: react-native-svg <Svg><Rect/><SvgText/><Rect/></Svg>."""
    return (f'<svg width="{boyut}" height="{boyut}" viewBox="0 0 100 100" '
            f'role="img" aria-label="Trinkow monogramı">'
            f'<rect x="0" y="0" width="100" height="100" fill="{zemin}"/>'
            f'<text x="18.15" y="78" font-family="SerifSB" font-size="84.34" '
            f'fill="{murekkep}">T</text>'
            f'<rect x="66" y="42" width="6" height="36" fill="{murekkep}"/>'
            f'</svg>')
