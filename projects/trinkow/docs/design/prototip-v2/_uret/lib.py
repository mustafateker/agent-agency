# -*- coding: utf-8 -*-
"""Trinkow prototip v2 ("Gun Isigi") — ortak uretici kutuphane.

Teslim edilen sey uretilen HTML'dir; bu klasor sadece uretim aracidir.
Gosterge geometrisi burada TEK yerde hesaplanir (tokens.md 7.5):
  dis cap 200, kalinlik 18, yay 270 derece, bosluk altta, ucunda 22pt topuz.
"""
from __future__ import annotations

import math
import os

from icons import ICONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# ikon
# --------------------------------------------------------------------------


def ico(name: str, size: int = 24, color: str = "currentColor", sw: float = 2.0) -> str:
    """Lucide ikonu (varliklar.md ile kilitli set). RN: lucide-react-native."""
    if name not in ICONS:
        raise KeyError("varliklar.md disinda ikon: " + name)
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


# --------------------------------------------------------------------------
# kategori aileleri — 6 renk ailesi, 13 kategori (varliklar.md 1.1)
# --------------------------------------------------------------------------
FAMILY = {
    "kahve":  ("#7A5233", "#F1E7DC"),
    "yemek":  ("#C2405A", "#FBE3E7"),
    "ulasim": ("#1F7A8C", "#DDEEF1"),
    "market": ("#4C7A34", "#E4EFDC"),
    "fatura": ("#2F4A8C", "#E2E7F5"),
    "diger":  ("#5A5B63", "#EAEAED"),
}
# kategori adi -> (aile, lucide ikonu)
CATEGORY = {
    "Kafe":          ("kahve",  "coffee"),
    "Alışkanlıklar": ("kahve",  "footprints"),
    "Restoran":      ("yemek",  "utensils"),
    "Eğlence":       ("yemek",  "ticket"),
    "Ulaşım":        ("ulasim", "bus"),
    "Akaryakıt":     ("ulasim", "fuel"),
    "Market":        ("market", "shopping-basket"),
    "Sağlık":        ("market", "pill"),
    "Fatura":        ("fatura", "receipt-text"),
    "Kira ve ev":    ("fatura", "house"),
    "Abonelik":      ("fatura", "repeat"),
    "Giyim":         ("diger",  "shirt"),
    "Diğer":         ("diger",  "circle-dashed"),
}


def cat_colors(name: str):
    fam, icon = CATEGORY[name]
    solid, soft = FAMILY[fam]
    return solid, soft, icon


def cat_box(name: str) -> str:
    """40x40 radius-16 kategori kabi + 20pt ikon. Renk + ikon + metin birlikte."""
    solid, soft, icon = cat_colors(name)
    return (
        f'<div class="rn-cat-box" style="background:{soft};color:{solid}">'
        f"{ico(icon, 20)}</div>"
    )


# --------------------------------------------------------------------------
# kahraman gosterge  (RN: react-native-svg + expo-linear-gradient)
# --------------------------------------------------------------------------
CX = 116.0          # 232x232 tuval; 200pt gosterge + 6pt tasma yayi sigsin diye
R_MAIN = 91.0       # (200 - 18) / 2
SW_MAIN = 18.0
R_OVER = 109.0      # ana yayin 6pt disinda
SW_OVER = 6.0
SWEEP = 270.0
START = 225.0       # saat 7-8 arasi; 270 derecelik yayin bosluğu tam altta kalir


def _pt(angle_deg: float, r: float):
    a = math.radians(angle_deg)
    return CX + r * math.sin(a), CX - r * math.cos(a)


def hero_gauge(ratio: float, gid: str, over_ratio: float = 0.0) -> str:
    """ratio 0..1 ana yay dolulugu. over_ratio > 0 ise murdum tasma yayi eklenir.

    Renk dolulukla DEGISMEZ (tokens 1.4): her oranda grad.arc.
    """
    c_main = 2 * math.pi * R_MAIN
    fill = max(0.0, min(1.0, ratio)) * SWEEP / 360.0 * c_main
    track = SWEEP / 360.0 * c_main
    kx, ky = _pt(START + max(0.0, min(1.0, ratio)) * SWEEP, R_MAIN)

    # %100 esik isareti (tokens 7.5). SADECE gerektiginde cizilir:
    # limit doldugunda ya da tasma yayi varken. Limit altindayken olugun
    # kendi ucu zaten "%100 burasi" diyor; ustune bir de cizgi koymak
    # yayin sag-alt ucunda artefakt gibi duruyordu (PM Tur A notu).
    mark = ""
    if over_ratio > 0 or ratio >= 0.999:
        mx1, my1 = _pt(START + SWEEP, R_MAIN + SW_MAIN / 2 + 2)
        mx2, my2 = _pt(START + SWEEP, R_MAIN + SW_MAIN / 2 + 8)
        mark = (f'<line x1="{mx1:.2f}" y1="{my1:.2f}" x2="{mx2:.2f}" y2="{my2:.2f}" '
                f'stroke="#5A5B63" stroke-width="2" stroke-linecap="round"/>')

    over = ""
    if over_ratio > 0:
        c_over = 2 * math.pi * R_OVER
        over_len = over_ratio * SWEEP / 360.0 * c_over
        over = (
            f'<circle cx="{CX}" cy="{CX}" r="{R_OVER}" fill="none" stroke="#6E3B6B" '
            f'stroke-width="{SW_OVER}" stroke-linecap="round" '
            f'stroke-dasharray="{over_len:.2f} {c_over:.2f}" '
            f'transform="rotate(-90 {CX} {CX})"/>'
        )

    return f"""<svg viewBox="0 0 232 232" aria-hidden="true">
  <defs>
    <linearGradient id="arc-{gid}" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#D9661A"/><stop offset="1" stop-color="#A8500C"/>
    </linearGradient>
  </defs>
  <circle cx="{CX}" cy="{CX}" r="{R_MAIN}" fill="none" stroke="#EFEAE3"
          stroke-width="{SW_MAIN}" stroke-linecap="round"
          stroke-dasharray="{track:.2f} {c_main:.2f}" transform="rotate(135 {CX} {CX})"/>
  {'' if fill <= 0.01 else f'<circle cx="{CX}" cy="{CX}" r="{R_MAIN}" fill="none" stroke="url(#arc-{gid})" stroke-width="{SW_MAIN}" stroke-linecap="round" stroke-dasharray="{fill:.2f} {c_main:.2f}" transform="rotate(135 {CX} {CX})"/>'}
  {mark}
  {over}
  <circle cx="{kx:.2f}" cy="{ky:.2f}" r="11" fill="#FFFCF8" stroke="#A8500C" stroke-width="4"/>
</svg>"""


def mini_gauge(ratio: float, color: str) -> str:
    """56pt mini gosterge — topuz yok, dolgu kategori rengi (tokens 7.5)."""
    r, sw, c = 25.0, 6.0, 2 * math.pi * 25.0
    track = SWEEP / 360.0 * c
    fill = max(0.0, min(1.0, ratio)) * SWEEP / 360.0 * c
    # ratio 0 iken dolgu HIC cizilmez: yuvarlak uc kapagi sifir uzunlukta bir
    # dashi nokta gibi gosterir ve olugun basinda artefakt birakir.
    dolgu = "" if fill <= 0.01 else (
        f'<circle cx="28" cy="28" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-dasharray="{fill:.2f} {c:.2f}" transform="rotate(135 28 28)"/>')
    return f"""<svg viewBox="0 0 56 56" aria-hidden="true">
  <circle cx="28" cy="28" r="{r}" fill="none" stroke="#EFEAE3" stroke-width="{sw}"
          stroke-linecap="round" stroke-dasharray="{track:.2f} {c:.2f}" transform="rotate(135 28 28)"/>
  {dolgu}
</svg>"""


def empty_arc() -> str:
    """Bos durum illustrasyonu: 120pt cap, 18pt kalinlik, dolgusuz yay + topuz."""
    r, sw, c = 51.0, 18.0, 2 * math.pi * 51.0
    track = SWEEP / 360.0 * c
    kx = 60 + 51 * math.sin(math.radians(225))
    ky = 60 - 51 * math.cos(math.radians(225))
    return f"""<svg viewBox="0 0 120 120" width="120" height="120" aria-hidden="true">
  <circle cx="60" cy="60" r="{r}" fill="none" stroke="#EFEAE3" stroke-width="{sw}"
          stroke-linecap="round" stroke-dasharray="{track:.2f} {c:.2f}" transform="rotate(135 60 60)"/>
  <circle cx="{kx:.2f}" cy="{ky:.2f}" r="11" fill="#FFFCF8" stroke="#EFEAE3" stroke-width="4"/>
</svg>"""


# --------------------------------------------------------------------------
# cerceve parcalari (BOLUM A — RN'e kodlanmaz)
# --------------------------------------------------------------------------
STATUSBAR = """<div class="statusbar">
  <span class="num">9:41</span>
  <span class="right">
    <svg viewBox="0 0 17 11" aria-hidden="true"><rect x="0" y="7" width="3" height="4" rx="0.6"/><rect x="4" y="5" width="3" height="6" rx="0.6"/><rect x="8" y="3" width="3" height="8" rx="0.6"/><rect x="12" y="0" width="3" height="11" rx="0.6"/></svg>
    <svg viewBox="0 0 17 11" aria-hidden="true"><path d="M8.5 1.5C5.5 1.5 2.7 2.6 0.5 4.6L2 6.1C3.8 4.5 6.1 3.6 8.5 3.6c2.4 0 4.7 0.9 6.5 2.5l1.5-1.5c-2.2-2-5-3.1-8-3.1zM3.5 7.6L5 9.1c1-0.9 2.2-1.4 3.5-1.4 1.3 0 2.5 0.5 3.5 1.4l1.5-1.5c-1.4-1.3-3.1-2-5-2-1.9 0-3.6 0.7-5 2zM6.5 10.6l2 2 2-2c-0.5-0.5-1.2-0.8-2-0.8s-1.5 0.3-2 0.8z"/></svg>
    <svg class="battery" viewBox="0 0 25 11" aria-hidden="true"><rect x="0.5" y="0.5" width="21" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-opacity="0.45"/><rect x="22" y="3.5" width="1.5" height="4" rx="0.4" fill="currentColor" fill-opacity="0.45"/><rect x="2" y="2" width="18" height="7" rx="1.4"/></svg>
  </span>
</div>"""

_KEY_BACKSPACE = (
    '<svg viewBox="0 0 24 24"><path d="M20 5a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9.4a2 2 0 0 1-1.4-.6l-4.4-4.4a2 2 0 0 1 0-2.8L8 6.6A2 2 0 0 1 9.4 6"/><path d="m12 9 4 4"/><path d="m16 9-4 4"/></svg>'
)


def keyboard() -> str:
    """iOS decimal-pad. Isletim sistemi cizer; bizim kodumuz degil.
    Burada duruyor cunku 'Kaydet klavye acikken gorunur kalir' kurali
    ancak klavye cizilirse denetlenebilir."""
    keys = "".join(f'<div class="key">{n}</div>' for n in "123456789")
    return f"""<div class="keyboard" aria-hidden="true">
  {keys}
  <div class="key">,</div>
  <div class="key">0</div>
  <div class="key fn">{_KEY_BACKSPACE}</div>
</div>"""


def device(content: str, caption: str, sub: str = "", warm: bool = False,
           tail: str = "", note: str = "", dark_indicator: bool = False) -> str:
    """Tek telefon cercevesi. `content` = <main class="content"> ICI (RN kismi).
    `tail` = icerigin altinda, kaymayan bolge (sekme cubugu / klavye)."""
    sub_html = f"<span>{sub}</span>" if sub else ""
    note_html = f'<div class="note">{note}</div>' if note else ""
    return f"""<div class="stage">
  <div class="caption"><strong>{caption}</strong>{sub_html}</div>
  <div class="device" data-od-id="device">
    <span class="btn-rail left-1" aria-hidden="true"></span>
    <span class="btn-rail left-2" aria-hidden="true"></span>
    <span class="btn-rail left-3" aria-hidden="true"></span>
    <span class="btn-rail right-1" aria-hidden="true"></span>
    <span class="island" aria-hidden="true"></span>
    <div class="screen{' warm' if warm else ''}">
      {STATUSBAR}
      <main class="content" data-od-id="content">
{content}
      </main>
{tail}
      <div class="home-indicator{' on-dark' if dark_indicator else ''}" aria-hidden="true"></div>
    </div>
  </div>
  {note_html}
</div>"""


def device_sheet(behind: str, sheet_html: str, caption: str, sub: str = "",
                 warm: bool = False, kb: bool = True, note: str = "") -> str:
    """Bottom sheet ekrani (E-11). `behind` = altta duran pano, `sheet_html` = sheet.

    RN karsiligi: <Modal transparent> icinde
      1) scrim  -> <Pressable style={StyleSheet.absoluteFill}> (kapatir)
      2) sheet  -> <KeyboardAvoidingView behavior="padding">
    Sira belirleyici; z-index kullanilmaz. Scrim durum cubugunun altindan
    baslar, iOS davranisiyla ayni.
    """
    sub_html = f"<span>{sub}</span>" if sub else ""
    note_html = f'<div class="note">{note}</div>' if note else ""
    return f"""<div class="stage">
  <div class="caption"><strong>{caption}</strong>{sub_html}</div>
  <div class="device" data-od-id="device">
    <span class="btn-rail left-1" aria-hidden="true"></span>
    <span class="btn-rail left-2" aria-hidden="true"></span>
    <span class="btn-rail left-3" aria-hidden="true"></span>
    <span class="btn-rail right-1" aria-hidden="true"></span>
    <span class="island" aria-hidden="true"></span>
    <div class="screen has-sheet{' warm' if warm else ''}">
      {STATUSBAR}
      <main class="content" data-od-id="content">
{behind}
      </main>
      <div class="rn-scrim" aria-hidden="true"></div>
      <div class="rn-sheetwrap" data-od-id="sheet">
{sheet_html}
      </div>
{keyboard() if kb else ''}
      <div class="home-indicator" aria-hidden="true"></div>
    </div>
  </div>
  {note_html}
</div>"""


def steps(now: int, total: int = 3) -> str:
    """Onboarding adim gostergesi. Metin + dolu segment birlikte: renk tek
    basina bilgi tasimaz (WCAG 1.4.1)."""
    segs = ""
    for i in range(1, total + 1):
        cls = "seg done" if i < now else ("seg now" if i == now else "seg")
        segs += f'<span class="{cls} rn-fill"></span>'
    return f"""          <div class="rn-row rn-between mt16">
            <div class="rn-steps rn-fill" role="progressbar" aria-label="Kurulum ilerlemesi"
                 aria-valuemin="1" aria-valuemax="{total}" aria-valuenow="{now}">{segs}</div>
            <p class="t-label c-2" style="margin-left:16px">Adım {now}/{total}</p>
          </div>"""


def tabbar(active: str = "bugun", fab_pressed: bool = False) -> str:
    """Yuzen sekme cubugu + merkez FAB. BU BOLUM RN'E KODLANIR (flexbox)."""
    def tab(key, name, label):
        on = " is-active" if active == key else ""
        return (
            f'<button class="rn-tab{on}" type="button" aria-label="{label} sekmesi">'
            f'<span class="icowrap">{ico(name, 28)}</span>'
            f'<span class="lbl">{label}</span></button>'
        )
    fab_cls = " is-pressed" if fab_pressed else ""
    return f"""<div class="rn-tabwrap" data-od-id="tabbar">
  <div class="rn-tabbar">
    {tab('bugun', 'gauge', 'Bugün')}
    {tab('kayitlar', 'notebook-text', 'Kayıtlar')}
    <button class="rn-fab{fab_cls}" type="button" aria-label="Harcama ekle">{ico('plus', 24)}</button>
    {tab('ozet', 'chart-no-axes-column', 'Özet')}
  </div>
</div>"""


# --------------------------------------------------------------------------
# sayfa
# --------------------------------------------------------------------------
def page(title: str, heading: str, intro: str, devices: str, out: str) -> None:
    html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<link rel="stylesheet" href="stil.css"/>
</head>
<body>
<div class="sheet-head">
  <h1>{heading}</h1>
  <p>{intro} · <a href="index.html">tüm ekranlar</a></p>
</div>
<div class="sheet">
{devices}
</div>
</body>
</html>
"""
    path = os.path.join(ROOT, out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("yazildi:", path, len(html), "bayt")
