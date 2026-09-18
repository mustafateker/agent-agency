"""Trinkow prototip v4 — ortak üretim kitaplığı (claymorphism).

ÖNEMLİ: Bu dosya yalnız HTML üretir. Üretilen HTML iki bölgeye ayrılır:
  [A] cihaz çerçevesi  -> RN'e kodlanmaz, CSS serbest
  [B] <main class="content"> içi -> RN'e kodlanır, yalnız flexbox
"""
from __future__ import annotations
import math

# ---------------------------------------------------------------- ikonlar
# Lucide (ISC) — stroke-width 2, monoline. Emoji kullanılmaz.
IC = {
    # kategori
    "coffee": '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M6 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "shopping-basket": '<path d="m15 11-1 9"/><path d="m19 11-4-7"/><path d="M2 11h20"/><path d="m3.5 11 1.6 7.4a2 2 0 0 0 2 1.6h9.8a2 2 0 0 0 2-1.6l1.7-7.4"/><path d="M4.5 15.5h15"/><path d="m5 11 4-7"/><path d="m9 11 1 9"/>',
    "bus": '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
    "fuel": '<path d="M3 22h12"/><path d="M4 9h10"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 4 0V9.8a2 2 0 0 0-.6-1.4L18 5"/>',
    "receipt-text": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>',
    "house": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .7-1.5l7-6a2 2 0 0 1 2.6 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "pill": '<path d="m10.5 20.5 10-10a5 5 0 1 0-7-7l-10 10a5 5 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
    "shirt": '<path d="M20.4 3.5 16 2a4 4 0 0 1-8 0L3.6 3.5a2 2 0 0 0-1.3 2.2l.6 3.5a1 1 0 0 0 1 .8H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.1a1 1 0 0 0 1-.8l.6-3.5a2 2 0 0 0-1.3-2.2z"/>',
    "ticket": '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 11v2"/><path d="M13 17v2"/>',
    "footprints": '<path d="M4 16v-2.4C4 11.5 3 10.5 3 8c0-2.7 1.5-6 4.5-6C9.4 2 10 3.8 10 5.5c0 3.1-2 5.7-2 8.7V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.4c0-2.1 1-3.1 1-5.6 0-2.7-1.5-6-4.5-6C14.6 6 14 7.8 14 9.5c0 3.1 2 5.7 2 8.7V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
    "circle-dashed": '<path d="M10.1 2.2a10 10 0 0 1 3.8 0"/><path d="M17.6 3.7a10 10 0 0 1 2.7 2.7"/><path d="M21.8 10.1a10 10 0 0 1 0 3.8"/><path d="M20.3 17.6a10 10 0 0 1-2.7 2.7"/><path d="M13.9 21.8a10 10 0 0 1-3.8 0"/><path d="M6.4 20.3a10 10 0 0 1-2.7-2.7"/><path d="M2.2 13.9a10 10 0 0 1 0-3.8"/><path d="M3.7 6.4a10 10 0 0 1 2.7-2.7"/>',
    "eye": '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
    "eye-off": '<path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.5 13.5 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/><path d="m2 2 20 20"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
    "wifi-off": '<path d="M12 20h.01"/><path d="M8.5 16.42a5 5 0 0 1 7 0"/><path d="M5 12.86a10 10 0 0 1 5.2-2.7"/><path d="M19 12.86a10 10 0 0 0-3.6-2.4"/><path d="M2 8.82a16 16 0 0 1 4.6-2.9"/><path d="M22 8.82a16 16 0 0 0-10.7-4.1"/><path d="m2 2 20 20"/>',
    "mail-check": '<path d="M22 13V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h8"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/><path d="m16 19 2 2 4-4"/>',
    # arayüz
    "gauge": '<path d="m12 14 4-4"/><path d="M3.3 19a10 10 0 1 1 17.3 0"/>',
    "notebook-text": '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9.5 8h5"/><path d="M9.5 12H16"/><path d="M9.5 16H14"/>',
    "chart-no-axes-column": '<path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "sliders": '<path d="M21 4h-7"/><path d="M10 4H3"/><path d="M21 12h-9"/><path d="M8 12H3"/><path d="M21 20h-5"/><path d="M12 20H3"/><path d="M14 2v4"/><path d="M8 10v4"/><path d="M16 18v4"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.8 9.8 0 0 1 6.7 2.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.8 9.8 0 0 1-6.7-2.7L3 16"/><path d="M3 21v-5h5"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "delete": '<path d="M21 5H9l-7 7 7 7h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Z"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "credit-card": '<rect width="20" height="14" x="2" y="5" rx="3"/><path d="M2 10h20"/>',
    "banknote": '<rect width="20" height="12" x="2" y="6" rx="3"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "landmark": '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M12 2 21 7H3Z"/>',
    "trending-down": '<path d="M22 17 13.5 8.5 8.5 13.5 2 7"/><path d="M16 17h6v-6"/>',
    "trash-2": '<path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M10 11v6"/><path d="M14 11v6"/>',
    "pencil": '<path d="M21.2 4.8a2.7 2.7 0 0 0-3.9 0L4 18v3h3L20.3 8.7a2.7 2.7 0 0 0 .9-3.9Z"/><path d="m15 5 4 4"/>',
    "calendar-days": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/>',
    "list-x": '<path d="M11 5h10"/><path d="M11 12h10"/><path d="M11 19h4"/><path d="m3 5 4 4"/><path d="m7 5-4 4"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "bell": '<path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/><path d="M4 17h16a2 2 0 0 1-2-2V9a6 6 0 1 0-12 0v6a2 2 0 0 1-2 2Z"/>',
    "chart-no-axes-column": '<path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>',
    "circle-slash": '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "calendar-clock": '<path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h5"/><path d="M21 10V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6"/><circle cx="17.5" cy="17.5" r="4.5"/><path d="M17.5 15.5v2.2l1.5 1"/>',
}


def icon(name: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[name]}</svg>')


# ------------------------------------------------------- cihaz çerçevesi [A]
STATUSBAR = '''        <div class="statusbar">
          <span class="saat">9:41</span>
          <span class="right">
            <svg viewBox="0 0 17 11" aria-hidden="true"><rect x="0" y="7" width="3" height="4" rx="0.6"/><rect x="4" y="5" width="3" height="6" rx="0.6"/><rect x="8" y="3" width="3" height="8" rx="0.6"/><rect x="12" y="0" width="3" height="11" rx="0.6"/></svg>
            <svg viewBox="0 0 17 11" aria-hidden="true"><path d="M8.5 1.5C5.5 1.5 2.7 2.6 0.5 4.6L2 6.1C3.8 4.5 6.1 3.6 8.5 3.6c2.4 0 4.7 0.9 6.5 2.5l1.5-1.5c-2.2-2-5-3.1-8-3.1zM3.5 7.6L5 9.1c1-0.9 2.2-1.4 3.5-1.4 1.3 0 2.5 0.5 3.5 1.4l1.5-1.5c-1.4-1.3-3.1-2-5-2-1.9 0-3.6 0.7-5 2zM6.5 10.6l2 2 2-2c-0.5-0.5-1.2-0.8-2-0.8s-1.5 0.3-2 0.8z"/></svg>
            <svg class="battery" viewBox="0 0 25 11" aria-hidden="true"><rect x="0.5" y="0.5" width="21" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-opacity="0.45"/><rect x="22" y="3.5" width="1.5" height="4" rx="0.4" fill="currentColor" fill-opacity="0.45"/><rect x="2" y="2" width="18" height="7" rx="1.4"/></svg>
          </span>
        </div>
'''


# Sistem klavyesi — **bölge [A]**, `<main>`'in DIŞINDA çizilir.
# Sebep: bu klavyeyi iOS/Android çizer, biz çizmeyiz; RN'e kodlanmaz ve
# denetim.py taramasına girmez. Yalnız "metin girerken ekranın ne kadarı
# kalıyor" sorusunu dürüst göstermek için prototipte yer alır.
KLAVYE_SATIR = [
    list("qwertyuıopğü"),
    list("asdfghjklşi"),
    ["shift"] + list("zxcvbnmöç") + ["sil"],
]


def sistem_klavye() -> str:
    rows = []
    for i, r in enumerate(KLAVYE_SATIR):
        keys = []
        for t in r:
            if t in ("shift", "sil"):
                g = "\u21E7" if t == "shift" else "\u232B"
                keys.append(f'<span class="ktus koyu genis">{g}</span>')
            else:
                keys.append(f'<span class="ktus">{t}</span>')
        kenar = ' style="padding:0 18px"' if i == 1 else ""
        rows.append(f'<span class="ksatir"{kenar}>{"".join(keys)}</span>')
    rows.append('<span class="ksatir">'
                '<span class="ktus koyu genis2">123</span>'
                '<span class="ktus bosluk">boşluk</span>'
                '<span class="ktus koyu genis2">ara</span>'
                '</span>')
    return f'<div class="sistem-klavye" aria-hidden="true">{"".join(rows)}</div>\n'


def device(caption_bold: str, caption_rest: str, content: str, note: str = "",
           sabit_alt: str = "", klavye: bool = False) -> str:
    """content -> kayan bölge (RN: ScrollView) · sabit_alt -> ekrana sabit alt blok.
    klavye=True -> sistem klavyesi (bölge [A], main'in dışında)."""
    note_html = f'\n      <div class="not-kutu">{note}</div>' if note else ""
    klavye_html = sistem_klavye() if klavye else ""
    return f'''    <div class="sahne-birim">
      <div class="baslik-etiket">{caption_bold} <span>· {caption_rest}</span></div>
      <div class="device" data-od-id="device">
        <span class="btn-rail left-1" aria-hidden="true"></span>
        <span class="btn-rail left-2" aria-hidden="true"></span>
        <span class="btn-rail left-3" aria-hidden="true"></span>
        <span class="btn-rail right-1" aria-hidden="true"></span>
        <span class="island" aria-hidden="true"></span>
        <div class="screen">
{STATUSBAR}        <main class="content" data-od-id="content">
          <div class="kaydir" data-od-id="scroll">
{content}
          </div>
{sabit_alt}        </main>
{klavye_html}        <div class="home-indicator" aria-hidden="true"></div>
        </div>
      </div>{note_html}
    </div>
'''


def page(title: str, h1: str, intro: str, units: str) -> str:
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<link rel="stylesheet" href="stil.css" />
</head>
<body>
  <div class="sayfa-basligi">
    <h1>{h1}</h1>
    <p>{intro} · <a href="index.html">Prototip dizinine dön</a></p>
  </div>
  <div class="sahne">
{units}  </div>
</body>
</html>
'''


# ---------------------------------------------- kahraman gösterge (clay yay)
# Geometri (tokens.md §7.5). Ölçüler pt = px (390 viewport).
# İki ölçü vardır (tokens.md §7.5):
#   224 -> dolu/limit dışı gösterge (v3.1: 296'dan indirildi, ekranı yutuyordu)
#   176 -> boş durum göstergesi (§7.8) — taşma yayı ve topuz yoktur
GEO = {
    224: dict(c=112.0, kal=16.0, r=86.0, r_over=102.0, rim=6.5, knob=13.0),
    176: dict(c=88.0,  kal=12.0, r=70.0, r_over=None,  rim=5.0, knob=10.0),
}
SPAN = 270.0      # yay açıklığı, boşluk altta
START = 135.0     # saat 7 yönü (SVG açısı: 0=doğu, 90=güney, saat yönü artı)
SIZE = 224.0
IC_ALAN = 2 * (GEO[224]["r"] - GEO[224]["kal"] / 2)   # ortadaki boş çap = 156px


def _pt(r: float, deg: float, c: float) -> tuple[float, float]:
    a = math.radians(deg)
    return c + r * math.cos(a), c + r * math.sin(a)


def _arc(r: float, a0: float, a1: float, c: float) -> str:
    x0, y0 = _pt(r, a0, c)
    x1, y1 = _pt(r, a1, c)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"


def hero_gauge(oran: float, over_oran: float = 0.0, bos: bool = False,
               cap: int = 224) -> str:
    """oran: 0..1 limit içi doluluk · over_oran: limitin üzerine taşan oran."""
    g = GEO[cap]
    C, KAL, R, R_OVER = g["c"], g["kal"], g["r"], g["r_over"]
    KN = g["knob"]
    arc_len = 2 * math.pi * R * (SPAN / 360.0)
    oran = max(0.0, min(1.0, oran))
    dolu = oran * arc_len
    kx, ky = _pt(R, START + SPAN * oran, C)
    track = _arc(R, START, START + SPAN - 0.01, C)
    rim_dis = _arc(R + g["rim"], START, START + SPAN - 0.01, C)   # oluğun dış kenarı (koyu)
    rim_ic = _arc(R - g["rim"], START, START + SPAN - 0.01, C)    # oluğun iç kenarı (açık)

    over = ""
    if over_oran > 0 and R_OVER:
        deg = min(SPAN, SPAN * over_oran)
        over = (f'<path d="{_arc(R_OVER, 270, 270 + deg, C)}" stroke="url(#gOver)" stroke-width="8" '
                f'stroke-linecap="round" fill="none"/>'
                f'<path d="{_arc(R_OVER, 270, 270 + deg, C)}" stroke="rgba(255,255,255,0.32)" stroke-width="3" '
                f'stroke-linecap="round" fill="none"/>')

    fill = knob = ""
    if not bos:
        fill = (f'<path d="{track}" stroke="url(#gArc)" stroke-width="{KAL:.0f}" stroke-linecap="round" fill="none" '
                f'stroke-dasharray="{dolu:.2f} {arc_len + 60:.2f}"/>'
                f'<path d="{track}" stroke="rgba(255,255,255,0.30)" stroke-width="5" stroke-linecap="round" fill="none" '
                f'stroke-dasharray="{max(0.0, dolu - 14):.2f} {arc_len + 60:.2f}" stroke-dashoffset="-7"/>')
        knob = (f'<circle cx="{kx:.2f}" cy="{ky + 2:.2f}" r="{KN + 0.5:.1f}" fill="rgba(28,57,142,0.18)"/>'
                f'<circle cx="{kx:.2f}" cy="{ky:.2f}" r="{KN:.1f}" fill="#FFFFFF"/>'
                f'<circle cx="{kx:.2f}" cy="{ky:.2f}" r="{KN - 2:.1f}" fill="none" stroke="#2F68C5" stroke-width="4"/>'
                f'<circle cx="{kx:.2f}" cy="{ky - 2:.2f}" r="{KN - 5:.1f}" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>')

    return f'''<svg class="yay" width="{cap}" height="{cap}" viewBox="0 0 {cap} {cap}" role="img" aria-label="Günlük limit kullanımı">
              <defs>
                <linearGradient id="gArc" x1="0" y1="1" x2="1" y2="0">
                  <stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2F68C5"/>
                </linearGradient>
                <linearGradient id="gOver" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#D97706"/><stop offset="100%" stop-color="#B45309"/>
                </linearGradient>
              </defs>
              <path d="{track}" stroke="#E6EFFE" stroke-width="{KAL:.0f}" stroke-linecap="round" fill="none"/>
              <path d="{rim_dis}" stroke="rgba(28,57,142,0.13)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="{rim_ic}" stroke="rgba(255,255,255,0.95)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              {fill}
              {over}
              {knob}
            </svg>'''


# ------------------------------------------------------------- parça üretici
CATS = {
    "Market": ("shopping-basket", "kat-yesil"),
    "Sağlık": ("pill", "kat-yesil"),
    "Kafe": ("coffee", "kat-amber"),
    "Restoran": ("utensils", "kat-amber"),
    "Ulaşım": ("bus", "kat-mavi"),
    "Akaryakıt": ("fuel", "kat-mavi"),
    "Fatura": ("receipt-text", "kat-lacivert"),
    "Kira ve ev": ("house", "kat-lacivert"),
    "Abonelik": ("repeat", "kat-lacivert"),
    "Eğlence": ("ticket", "kat-kiremit"),
    "Giyim": ("shirt", "kat-kiremit"),
    "Alışkanlıklar": ("footprints", "kat-duman"),
    "Diğer": ("circle-dashed", "kat-duman"),
}


def kat_kab(ad: str) -> str:
    ikon, renk = CATS[ad]
    return f'<div class="kat-kab {renk}">{icon(ikon)}</div>'


def satir(ad: str, alt: str, tutar: str, limit_disi: bool = False, basili: bool = False) -> str:
    cls = "satir-kart"
    if limit_disi:
        cls += " limit-disi"
    if basili:
        cls += " basili"
    ek = ('<div class="h4"></div><div class="t-cap c-warn">limit dışı</div>'
          if limit_disi else "")
    return f'''<div class="{cls}">
              {kat_kab(ad)}
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-body">{ad}</div>
                <div class="t-cap tek-satir">{alt}</div>
              </div>
              <div class="w12"></div>
              <div class="kolon" style="align-items:flex-end;flex:0 0 auto;white-space:nowrap">
                <div class="t-amount">{tutar}</div>
                {ek}
              </div>
            </div>'''


def sekme_cubugu(aktif: str = "gunluk", fab_basili: bool = False, fab: bool = True) -> str:
    """Yüzen sekme çubuğu + merkez-sağ FAB.

    RN karşılığı: yükseklik 82 olan bir View; bar ve FAB `position:absolute`
    ile yerleşir (RN'de absolute desteklenir, overflow:visible desteklenmez).

    v4: en sol sekme "Bugün" -> **"Günlük"** (K-049). Ekran artık yalnız
    bugünü değil herhangi bir günü gösterdiği için etiket gün adı değil
    **yüzey adı** taşır. Sekme sayısı 3'te kalır. Eski `"bugun"` anahtarı,
    diğer üreteç dosyaları bozulmasın diye takma ad olarak kabul edilir.
    """
    if aktif == "bugun":
        aktif = "gunluk"

    def s(key, ikon, ad):
        a = " aktif" if key == aktif else ""
        return (f'<button class="sekme{a}" aria-label="{ad} sekmesi">'
                f'<div class="sekme-ikon-kab">{icon(ikon)}</div>'
                f'<div class="ad">{ad}</div></button>')
    fb = " basili" if fab_basili else ""
    fab_html = (f'<button class="fab{fb}" aria-label="Harcama ekle">{icon("plus")}</button>'
                if fab else '')
    bosluk = '<div class="sekme-bosluk"></div>' if fab else ''
    return f'''<div class="pad" style="padding-bottom:8px">
            <div class="sekme-alan">
              <div class="sekme-cubugu">
                {s("gunluk","gauge","Günlük")}
                {s("kayitlar","notebook-text","Kayıtlar")}
                {s("ozet","chart-no-axes-column","Özet")}
                {bosluk}
              </div>
              {fab_html}
            </div>
          </div>'''


def para_hero(sayi: str, renk_cls: str = "") -> str:
    """Kahraman sayı. `₺` 56pt yerine 32pt dizilir (tokens.md §2.3).

    Yayın iç alanı 156px (v3.1). Ölçülen genişlikler: `1.250 ₺` = 137px ✅,
    `12.500 ₺` = 163px ❌. Bu yüzden 6+ karakterli tutarda rol **bir basamak**
    iner: hero 56 -> display 32, `₺` 32 -> amount 17 (tokens.md §7.5).
    Keyfi ara punto üretilmez.
    """
    if len(sayi) >= 6:
        return (f'<div class="para-hero"><div class="t-display{renk_cls}">{sayi}</div>'
                f'<div class="w4"></div><div class="t-amount{renk_cls}">₺</div></div>')
    return (f'<div class="para-hero"><div class="t-hero{renk_cls}">{sayi}</div>'
            f'<div class="w4"></div><div class="t-hero-simge{renk_cls}">₺</div></div>')


def tus_takimi(basili_tus=""):
    rows = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], [",", "0", "sil"]]
    out = []
    for r in rows:
        hucre = []
        for t in r:
            b = " basili" if t == basili_tus else ""
            ic = icon("delete") if t == "sil" else t
            lbl = ' aria-label="Son rakamı sil"' if t == "sil" else ""
            hucre.append(f'<button class="tus{b}"{lbl}>{ic}</button>')
        out.append(f'<div class="tus-satir">{"".join(hucre)}</div><div class="h8"></div>')
    out[-1] = out[-1].replace('<div class="h8"></div>', '')   # son satırdan sonra boşluk yok
    return f'''              <div class="pad kolon">
                {''.join(out)}
              </div>'''


def kaydet(durum="aktif"):
    if durum == "pasif":
        return '<button class="btn-primary pasif" disabled aria-disabled="true">Kaydet</button>'
    if durum == "loading":
        return ('<button class="btn-primary basili" disabled aria-disabled="true">Kaydediliyor'
                '<div class="w8"></div><div class="spinner"></div></button>')
    return '<button class="btn-primary">Kaydet</button>'


# ------------------------------------------------- ortak parçalar (s04/s05/s06)
def isk(w: str, h: str, r: str = "999px") -> str:
    """Yükleniyor iskeleti bloğu (tokens.md §7.10) — çukur, animasyonsuz."""
    return f'<div class="iskelet" style="width:{w};height:{h};border-radius:{r}"></div>'


def ay_secici(ay: str, alt: str, sol_basili: bool = False,
              onceki: str = "Önceki ay", sonraki: str = "Sonraki ay") -> str:
    """E-14 ay / E-16 hafta değiştirici. Çukur oluk + iki kabarık topuz."""
    b = " basili" if sol_basili else ""
    return f'''          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="aralik">
                <button class="ikon-btn{b}" aria-label="{onceki}">{icon("chevron-left")}</button>
                <div class="kolon orta">
                  <div class="t-strong">{ay}</div>
                  <div class="h4"></div>
                  <div class="t-cap">{alt}</div>
                </div>
                <button class="ikon-btn" aria-label="{sonraki}">{icon("chevron-right")}</button>
              </div>
            </div>
          </div>'''


def gun_basligi(gun: str, toplam: str, limit_disi: str = "") -> str:
    """Defter ritmi: gün başlığı kart değildir, listeyi bölen tek satırdır.
    RN: FlatList içinde normal öğe — yapışkan (sticky) DEĞİL."""
    sag = (f'<div class="t-label c-warn">{limit_disi}</div>' if limit_disi
           else f'<div class="t-label c-2">{toplam}</div>')
    return f'''          <div class="pad aralik">
            <div class="t-strong">{gun}</div>
            {sag}
          </div>'''


def push_basi(baslik: str, sag: str = "", geri_basili: bool = False,
              sol_ek: str = "") -> str:
    """İtilen (push) ekranların başlığı: geri oku + h1 (+ isteğe bağlı sağ eylem).

    Geri oku SOL ÜSTTEDİR ve bu bilinçlidir: iOS'ta kenardan kaydırma zaten
    geri götürür, buton onun görünür karşılığıdır. Kritik/yıkıcı hiçbir hedef
    sol üste konmaz (rn-tasarim-kisitlari.md).
    """
    b = " basili" if geri_basili else ""
    sag_html = sag or '<div style="width:44px;height:44px"></div>'
    return f'''          <div class="ekran-basi">
            <button class="ikon-btn{b}" aria-label="Geri">{icon("chevron-left")}</button>
            <div class="esnek satir" style="justify-content:center">{sol_ek}<div class="t-h1 tek-satir">{baslik}</div></div>
            {sag_html}
          </div>'''


def anahtar(acik: bool = False, basili: bool = False, etiket: str = "") -> str:
    """Kil anahtar (switch). RN'de platform `Switch` KULLANILMAZ — iOS/Android
    farklı çizer ve clay dili uygulanamaz; `Pressable` + iki View ile kurulur.
    Dokunma hedefi anahtarın kendisi değil, **satırın tamamıdır** (≥68pt).
    """
    c = " acik" if acik else ""
    b = " basili" if basili else ""
    durum = "açık" if acik else "kapalı"
    # Dış kap <button> DEĞİL: dokunma hedefi satırın kendisidir ve iç içe
    # buton geçersiz HTML üretir. RN'de zaten tek `Pressable` (satır) vardır.
    return (f'<div class="anahtar{c}{b}" role="switch" aria-checked="{str(acik).lower()}" '
            f'aria-label="{etiket}, {durum}"><div class="topuz"></div></div>')


# ==========================================================================
# v4 · T-2 — GİRİŞ / KAYIT ortak parçaları (E-22 · E-23)
# --------------------------------------------------------------------------
# K-052: hesap yalnız KİMLİK içindir; harcama verisi cihazda kalır. Bu
# yüzden bu ekranlar bir DUVAR değil KAPIDIR — "Hesapsız devam et" her iki
# ekranda görünür bir çıkıştır (F-2/F-9 sürtünme kuralı).
#
# ÜÇÜNCÜ TARAF MARKA VARLIKLARI (tek istisna):
#   Apple ve Google düğmelerinin **dolgusu, logosu ve etiket metni** kendi
#   marka kılavuzlarına aittir; bizim paletimizden ve buton sözlüğümüzden
#   gelmez. Uzlaşma kuralı: **kap bizim, içerik onların.**
#     kap      -> yükseklik 56, radius 999, `clay.raised` / `clay.pressed`,
#                 8pt ikon↔metin boşluğu, tam genişlik (tokens §7.1 ölçüleri)
#     içerik   -> Apple: siyah zemin + beyaz elma + "Apple ile Devam Et"
#                 Google: beyaz zemin + 4 renkli G + "Google ile devam et"
#   Palet dışı değerler `stil.css`'in "ÜÇÜNCÜ TARAF" bloğunda toplanmıştır
#   (sınıf adı üzerinden), `<main>` içinde ham renk kodu geçmez.
#   RN'de iOS tarafında düğme BİZ ÇİZMEYİZ: `expo-apple-authentication`'ın
#   `AppleAuthenticationButton`'ı yerel düğmeyi çizer (doğru glif, doğru
#   yerelleştirme, doğru dokunma davranışı garanti). Aşağıdaki çizim onun
#   **yer ölçüsüdür**; Google düğmesi kendi logo varlığıyla çizilir.
# ==========================================================================

# Apple mark — tek renk glif (viewBox 17×20, beyaz dolgu sınıfla verilir)
APPLE_ISARET = (
    '<svg viewBox="0 0 17 20" aria-hidden="true">'
    '<path class="apple-govde" d="M13.62 10.62c.01 2.9 2.53 3.86 2.56 3.87-.02.06-.4 1.37-1.33 '
    '2.72-.8 1.17-1.63 2.33-2.94 2.35-1.29.03-1.7-.76-3.17-.76-1.47 0-1.93.74-3.15.79-1.26.05-2.22-1.26-3.03-2.42C.9 '
    '15.3-.4 10.98 1.3 8.05c.84-1.45 2.35-2.37 3.98-2.4 1.24-.02 2.41.83 3.17.83.75 0 '
    '2.18-1.03 3.67-.88.62.03 2.37.23 3.5 1.71-.09.06-2.08 1.22-2.06 3.63M11.15 3.38c.67-.81 '
    '1.12-1.94.99-3.06-.96.04-2.13.64-2.82 1.45-.62.71-1.16 1.86-1.01 2.96 1.07.08 2.17-.54 2.84-1.35"/>'
    '</svg>')

# Google "G" — dört renkli resmî glif (viewBox 48×48, renkler sınıfla)
GOOGLE_ISARET = (
    '<svg viewBox="0 0 48 48" aria-hidden="true">'
    '<path class="g-mavi" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 '
    '5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"/>'
    '<path class="g-yesil" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 '
    '2.1-7.45 2.1-5.73 0-10.58-3.87-12.3-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z"/>'
    '<path class="g-sari" d="M11.7 28.18c-.44-1.32-.68-2.72-.68-4.18s.25-2.86.68-4.18v-5.7H4.34C2.85 '
    '17.09 2 20.45 2 24s.85 6.91 2.34 9.88l7.36-5.7z"/>'
    '<path class="g-kirmizi" d="M24 9.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 3.18 29.93 1 '
    '24 1 15.4 1 7.96 5.93 4.34 13.12l7.36 5.7c1.72-5.2 6.57-9.07 12.3-9.07z"/>'
    '</svg>')


def sosyal_btn(saglayici: str, basili: bool = False, mesgul: bool = False) -> str:
    """Apple / Google ile devam et. Etiket metni sağlayıcının kılavuzundan
    gelir ve ÇEVİRİLMEZ/KISALTILMAZ (bizim 1-3 kelime buton kuralı burada
    geçerli değildir — marka kilidi kuralı yenir)."""
    if saglayici == "apple":
        isaret, ad = APPLE_ISARET, "Apple ile Devam Et"
        cls, a11y = "btn-apple", "Apple ile devam et"
    else:
        isaret, ad = GOOGLE_ISARET, "Google ile devam et"
        cls, a11y = "btn-google", "Google ile devam et"
    b = " basili" if basili else ""
    if mesgul:
        sag = '<div class="w8"></div><div class="spinner spinner-koyu"></div>'
    else:
        sag = ""
    return (f'<button class="btn-sosyal {cls}{b}" aria-label="{a11y}">'
            f'<span class="marka-isaret">{isaret}</span>'
            f'<div class="w8"></div><div class="ad">{ad}</div>{sag}</button>')


def sosyal_kume(apple_basili: bool = False, google_basili: bool = False,
                google_mesgul: bool = False, platform: str = "ios") -> str:
    """Sağlayıcı kümesi **platforma göre değişir** (Mustafa kararı, 2026-09-17):

      iOS      -> **Apple + Google**. Apple üstte: App Store kuralı 4.8
                  üçüncü taraf girişi sunan uygulamada Apple girişini
                  zorunlu kılar ve platform beklentisi de budur.
      Android  -> **yalnız Google** + e-posta/şifre. Apple düğmesi
                  Android'de **hiç çizilmez**: kural yalnız iOS'u bağlar ve
                  Android'de Apple akışı web köprüsü ister (ek iş, ek hata
                  yüzeyi). Yarım çalışan bir düğme koymak, hiç koymamaktan
                  kötüdür.

    **Apple ile açılmış hesap Android'de nasıl açılır:** Apple'ın verdiği
    (gerekirse gizlenmiş) e-posta adresi hesabın kimliğidir → kullanıcı
    E-22'deki **"Şifremi unuttum"** ile o adrese bağlantı ister, şifre
    belirler ve e-posta/şifre ile girer. Yeni ekran gerekmedi; var olan
    kurtarma yolu bu boşluğu zaten kapatıyor.
    """
    g = sosyal_btn("google", google_basili, google_mesgul)
    if platform == "android":
        return f'''          <div class="pad kolon">
            {g}
          </div>'''
    return f'''          <div class="pad kolon">
            {sosyal_btn("apple", apple_basili)}
            <div class="h8"></div>
            {g}
          </div>'''


def ayirac(metin: str = "ya da") -> str:
    """İki yolu ayıran tek sözcük. **Hairline çizgi yok:** `line #DCE6F9`
    sayfa zemini `bg #E6EFFE` üzerinde 1.08:1 — görünmez bir çizgi çizmek
    yerine boşluk ayırıyor (clay dilinde ayraç oluktur, saç teli değil)."""
    return f'''          <div class="pad kolon orta">
            <div class="t-cap">{metin}</div>
          </div>'''


def metin_alani(etiket: str, deger: str = "", placeholder: str = "",
                odakli: bool = False, hata: str = "", imlec: bool = False,
                sag_html: str = "", alt_html: str = "", a11y: str = "",
                pasif: bool = False) -> str:
    """`TextField` (tokens §7.4). Etiket girişin ÜSTÜNDE, placeholder'a
    gömülmez. Hata: 2pt `danger` kenarlık + altında `caption`/`danger-ink`
    (8 boşlukla) — kırmızının izinli dört bağlamından biri."""
    cls = "giris"
    if hata:
        cls += " hatali"
    elif odakli:
        cls += " odakli"
    if deger:
        ic = f'<div class="esnek t-body tek-satir">{deger}</div>'
    else:
        ic = f'<div class="esnek t-body c-3 tek-satir">{placeholder}</div>'
    if imlec:
        ic += '<div class="imlec"></div>'
    ek = ""
    if sag_html:
        ic += f'<div class="w8"></div>{sag_html}'
        ek = ' style="padding-right:8px"'
    hata_html = (f'\n              <div class="h8"></div>'
                 f'\n              <div class="t-cap c-danger">{hata}</div>' if hata else "")
    etiket_a11y = a11y or etiket
    return f'''          <div class="pad kolon">
            <div class="t-label c-2">{etiket}</div>
            <div class="h8"></div>
            <div class="{cls}"{ek} aria-label="{etiket_a11y}">
              {ic}
            </div>{hata_html}{alt_html}
          </div>'''


def goz_btn(gorunur: bool = False, basili: bool = False) -> str:
    """Şifre görünürlük anahtarı. İki durum, iki ikon, iki etiket — ikon
    tek başına durumu anlatmaz, `accessibilityLabel` eylemi söyler."""
    b = " basili" if basili else ""
    ad = "Şifreyi gizle" if gorunur else "Şifreyi göster"
    return (f'<button class="ikon-btn{b}" aria-label="{ad}">'
            f'{icon("eye-off" if gorunur else "eye")}</button>')


# ==========================================================================
# v4 · T-3 — PROFİLLEME (E-25) + PLANIN HAZIR (E-26) ortak parçaları
# --------------------------------------------------------------------------
# K-053: Katman 1 üç soruda kapanır, Katman 2 ("Seni tanıyalım") ATLANABİLİR.
# K-050: hiçbir fiyat varsayılmaz — sıklık ve fiyat kullanıcıdan gelir.
# Yatırım tavsiyesi YOK: enstrüman adı, getiri, risk skoru hiçbir yüzeyde
# geçmez; yalnız "yatırım payı" etiketi vardır.
# ==========================================================================

IC_GEN = 358.0    # ekran iç genişliği (390 - 2*16) — kaydırıcı/çubuk hesapları


def tl(lira: int, kurus: int | None = None) -> str:
    """Para biçimi (metinler.md §18): binlik nokta, kuruş yalnız istenirse."""
    g = f"{lira:,}".replace(",", ".")
    return f"{g},{kurus:02d} ₺" if kurus is not None else f"{g} ₺"


def yuzde(n: int) -> str:
    """Yüzde biçimi: `%26` — işaret önce, boşluk yok (TDK)."""
    return f"%{n}"


def kaydirici(oran: float, etiket: str, deger_html: str, alt: str = "",
              basili: bool = False, sinirda: bool = False,
              sol: str = "", sag: str = "", a11y: str = "",
              genislik: float = IC_GEN) -> str:
    """Kaydırıcı (Slider) — **yeni bileşen**.

    Geometri: oluk 12 · topuz 32 · satır 44 (dokunma hedefi).
    Topuz konumu `left = (genislik - 32) * oran`; RN'de `onLayout` ile
    ölçülen genişlikten aynı formülle hesaplanır, sabit sayı gömülmez.

    `sinirda=True`: değer üst sınıra dayandı. Topuz **durur**, zemini uyarı
    yumuşağına döner ve altındaki satır sınırın sebebini yazar. Kırmızı
    kullanılmaz — bu bir hata değil, bir sınır.
    """
    x = (genislik - 32.0) * max(0.0, min(1.0, oran))
    b = " basili" if basili else ""
    s = " sinirda" if sinirda else ""
    dolgu = max(0.0, (genislik - 32.0) * max(0.0, min(1.0, oran)) + 16.0)
    uc_sol = f'<div class="kaydirici-uc"><div class="t-micro">{sol}</div></div>' if sol else ""
    uc_sag = f'<div class="kaydirici-uc"><div class="t-micro">{sag}</div></div>' if sag else ""
    alt_html = f'<div class="h8"></div><div class="t-cap">{alt}</div>' if alt else ""
    return f'''              <div class="aralik">
                <div class="t-label c-2">{etiket}</div>
                {deger_html}
              </div>
              <div class="h8"></div>
              <div class="kaydirici" role="slider" aria-label="{a11y or etiket}">
                {uc_sol}
                <div class="kaydirici-oluk">
                  <div class="kaydirici-dolgu" style="width:{dolgu:.0f}px"></div>
                </div>
                {uc_sag}
                <div class="kaydirici-yer" style="left:{x:.0f}px">
                  <div class="kaydirici-topuz{b}{s}"></div>
                </div>
              </div>
              {alt_html}'''


def pay_oluk(paylar: list[tuple[str, int]], genislik: float = IC_GEN) -> str:
    """Üç payın tek oluktaki dizilişi. `paylar`: [(sinif, yuzde), ...].
    Segmentler arasına 4pt boşluk girer; oluk aradan görünür."""
    ara = 4.0 * (len(paylar) - 1)
    kullanilir = genislik - ara
    parca = []
    for i, (sinif, y) in enumerate(paylar):
        w = kullanilir * y / 100.0
        if i:
            parca.append('<div class="pay-ara"></div>')
        parca.append(f'<div class="pay-dolgu {sinif}" style="width:{w:.0f}px"></div>')
    return f'<div class="pay-oluk">{"".join(parca)}</div>'


def pay_satiri(sinif: str, ad: str, tutar: str, oran: str, alt: str = "") -> str:
    """Pay açıklama satırı: nokta + ad + ₺ + %.
    Renk tek başına bilgi taşımaz (WCAG 1.4.1) — nokta yanında daima ad var."""
    alt_html = (f'<div class="h4"></div><div class="t-cap">{alt}</div>') if alt else ""
    return f'''              <div class="satir-ust">
                <div class="kolon" style="padding-top:8px">
                  <div class="nokta {sinif}"></div>
                </div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-strong">{ad}</div>
                  {alt_html}
                </div>
                <div class="w12"></div>
                <div class="kolon" style="align-items:flex-end">
                  <div class="t-amount">{tutar}</div>
                  <div class="h4"></div>
                  <div class="t-cap">{oran}</div>
                </div>
              </div>'''


def denklem(sol: tuple[str, str], orta: tuple[str, str], sonuc: tuple[str, str],
            op1: str = "÷", op2: str = "=") -> str:
    """Günlük limitin türetildiği işlem — ekranda görünür (K-053: kara kutu yok)."""
    def kutu(v, cls=""):
        return (f'<div class="denklem-kutu{cls}">'
                f'<div class="t-amount">{v[0]}</div>'
                f'<div class="h4"></div>'
                f'<div class="t-micro">{v[1]}</div></div>')
    return f'''              <div class="denklem">
                {kutu(sol)}
                <div class="denklem-op"><div class="t-body c-2">{op1}</div></div>
                {kutu(orta)}
                <div class="denklem-op"><div class="t-body c-2">{op2}</div></div>
                {kutu(sonuc, " sonuc")}
              </div>'''


def ilerleme(n: int, toplam: int, genislik: float = IC_GEN - 44.0) -> str:
    """Katman 2 ilerlemesi: tek oluk + dolgu + "3/8". 8 segment çizilmez."""
    w = genislik * n / toplam
    return f'''            <div class="pad satir" aria-label="{toplam} kartın {n}. kartı">
              <div class="ilerleme-oluk">
                <div class="ilerleme-dolgu" style="width:{w:.0f}px"></div>
              </div>
              <div class="w12"></div>
              <div class="t-micro">{n}/{toplam}</div>
            </div>'''


def kuyu_deger(ad: str, deger: str, basili: bool = False, bos: str = "",
               ikon: str = "chevron-right", a11y: str = "") -> str:
    """Çukur değer satırı: etiket solda, değer sağda, dokunulunca tuş takımı.
    Değer yoksa **placeholder değil**, geçerli bir durum yazılır ("Girilmedi")."""
    b = " basili" if basili else ""
    sag = (f'<div class="t-amount">{deger}</div>' if deger
           else f'<div class="t-cap c-2">{bos or "Girilmedi"}</div>')
    return f'''              <button class="kuyu-btn{b}" style="padding:12px 16px" aria-label="{a11y or ad}">
                <div class="esnek t-strong">{ad}</div>
                <div class="w12"></div>
                {sag}
                <div class="w12"></div>
                {icon(ikon)}
              </button>'''


def sik_cipleri(secenekler: list[str], secili: str = "", basili: str = "") -> str:
    """Sıklık seçimi: **ayrık seçenekler** önce, serbest sayı en sonda.
    Serbest sayı ilk seçenek olsaydı her kullanıcı klavye açmak zorunda
    kalırdı; sürtünme kuralı (F-2) bunu yasaklar."""
    o = []
    for s in secenekler:
        c = " secili" if s == secili else (" basili" if s == basili else "")
        o.append(f'<div class="cip-ag-oge"><button class="cip{c}">{s}</button></div>')
    return f'<div class="cip-ag">{"".join(o)}</div>'


def ikon_kab(ikon_ad: str) -> str:
    """Nötr ikon kabı (48×48, radius 16). Kategori kabının (`kat-kab`)
    yerine kullanılır: **kategori renkleri yalnız kategori bilgisi taşır**
    (tokens §1.4), profilleme kartları kategori değildir. Zemin
    `primary-soft`, ikon `primary-text` — onboarding seçim kartının
    ikon kabıyla aynı bileşen."""
    return f'<div class="secim-ikon">{icon(ikon_ad)}</div>'
