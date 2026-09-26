# -*- coding: utf-8 -*-
"""Trinkow prototip rev2 — ortak üretim kitaplığı.

İki bölge (prototip-v4 ile aynı kural):
  [A] cihaz çerçevesi  -> RN'e kodlanmaz.
  [B] <main class="content"> içi -> RN'e kodlanır, yalnız flexbox.

Stil kaynağı: ../prototip-v4/stil.css (yeniden kullanılıyor, yeni sınıf
eklenmedi; rev2'ye özgü tek dosya stil-rev2.css'tir ve yalnız v4'te
karşılığı olmayan iki bileşen varyantını taşır).
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Lucide yol verileri — app/src/components/Icon.tsx'ten BİREBİR.
# Yeni ikon seti yok; yeni glif çizilmedi.
# ---------------------------------------------------------------------------
IKON: dict[str, str] = {
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    # REV3 — akordiyon oku. Açık bölümde AYNI glif 180° döner; `chevron-up`
    # kilitli sette (varliklar.md §1.2) yok ve üretilmedi.
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    # REV3 — "bugün almadım" eylemi. Kilitli setten (varliklar.md §1.2c
    # "Limiti kaldır"): uygulamada `limit-kaldir` adıyla zaten gömülü olan
    # glifin ta kendisi. Anlamı her iki bağlamda da olumsuzlama/iptal.
    "circle-slash": '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 22a8 8 0 0 1 16 0"/>',
    "notebook": '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/>'
                '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9.5 8h5"/>'
                '<path d="M9.5 12H16"/><path d="M9.5 16H14"/>',
    "chart": '<path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.3 19a10 10 0 1 1 17.3 0"/>',
    "banknote": '<rect x="2" y="6" width="20" height="12" rx="3"/><circle cx="12" cy="12" r="2"/>'
                '<path d="M6 12h.01M18 12h.01"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/>'
              '<path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "limitler": '<path d="M21 4h-7"/><path d="M10 4H3"/><path d="M21 12h-9"/><path d="M8 12H3"/>'
                '<path d="M21 20h-5"/><path d="M12 20H3"/><path d="M14 2v4"/><path d="M8 10v4"/>'
                '<path d="M16 18v4"/>',
    "calendar-clock": '<path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h5"/>'
                      '<path d="M21 10V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6"/>'
                      '<circle cx="17.5" cy="17.5" r="4.5"/><path d="M17.5 15.5v2.2l1.5 1"/>',
    "trending-up": '<path d="M22 17 13.5 8.5 8.5 13.5 2 7"/><path d="M16 17h6v-6"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
              '<circle cx="12" cy="12" r="2"/>',
    "landmark": '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/>'
                '<path d="M18 18v-7"/><path d="M12 2 21 7H3Z"/>',
    "ayarlar": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "wifi-off": '<path d="M12 20h.01"/><path d="M8.5 16.42a5 5 0 0 1 7 0"/>'
                '<path d="M5 12.86a10 10 0 0 1 5.2-2.7"/><path d="M19 12.86a10 10 0 0 0-3.6-2.4"/>'
                '<path d="M2 8.82a16 16 0 0 1 4.6-2.9"/><path d="M22 8.82a16 16 0 0 0-10.7-4.1"/>'
                '<path d="m2 2 20 20"/>',
    "coffee": '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M6 2v2"/>'
              '<path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/>',
    "shopping-basket": '<path d="m15 11-1 9"/><path d="m19 11-4-7"/><path d="M2 11h20"/>'
                       '<path d="m3.5 11 1.6 7.4a2 2 0 0 0 2 1.6h9.8a2 2 0 0 0 2-1.6l1.7-7.4"/>'
                       '<path d="M4.5 15.5h15"/><path d="m5 11 4-7"/><path d="m9 11 1 9"/>',
    "bus": '<path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/>'
           '<path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/>'
           '<circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/>'
                '<path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect x="3" y="4" width="18" height="18" rx="2"/>'
                '<path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/>'
                '<path d="M8 18h.01"/><path d="M12 18h.01"/>',
    # REV3 — Günlük çerçevelerinde kategori kartının son üç satırı için
    # (bağlam; kart bu turda DEĞİŞMEDİ). Üçü de v4 lib.py'den birebir.
    "shirt": '<path d="M20.4 14.5 16 10 4 20"/>'
             '<path d="M20.4 3.6 16 2l-4 3-4-3-4.4 1.6a2 2 0 0 0-1.2 2.5l1.6 4.4L2 22h20l-2-11.5 1.6-4.4a2 2 0 0 0-1.2-2.5Z"/>',
    "footprints": '<path d="M4 16v-2.4C4 11.5 3 10.5 3 8c0-2.7 1.5-6 4.5-6C9.4 2 10 3.8 10 5.5c0 3.1-2 5.7-2 8.7V16a2 2 0 1 1-4 0Z"/>'
                  '<path d="M20 20v-2.4c0-2.1 1-3.1 1-5.6 0-2.7-1.5-6-4.5-6C14.6 6 14 7.8 14 9.5c0 3.1 2 5.7 2 8.7V20a2 2 0 1 0 4 0Z"/>'
                  '<path d="M16 17h4"/><path d="M4 13h4"/>',
    "circle-dashed": '<path d="M10.1 2.2a10 10 0 0 1 3.8 0"/><path d="M17.6 3.7a10 10 0 0 1 2.7 2.7"/>'
                     '<path d="M21.8 10.1a10 10 0 0 1 0 3.8"/><path d="M20.3 17.6a10 10 0 0 1-2.7 2.7"/>'
                     '<path d="M13.9 21.8a10 10 0 0 1-3.8 0"/><path d="M6.4 20.3a10 10 0 0 1-2.7-2.7"/>'
                     '<path d="M2.2 13.9a10 10 0 0 1 0-3.8"/><path d="M3.7 6.4a10 10 0 0 1 2.7-2.7"/>',
    "receipt-text": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/>'
                    '<path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>',
    # REV3 (taksitler) — kilitli setten, YENİ GLİF ÇİZİLMEDİ. `pill` Sağlık
    # kategorisinin ikonu (varliklar.md §1.1); `refresh` hata durumunun
    # "Yeniden dene" glifi (v4 prototipinde zaten kullanılıyor).
    "pill": '<path d="m10.5 20.5 10-10a5 5 0 1 0-7-7l-10 10a5 5 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.8 9.8 0 0 1 6.7 2.7L21 8"/><path d="M21 3v5h-5"/>'
               '<path d="M21 12a9 9 0 0 1-9 9 9.8 9.8 0 0 1-6.7-2.7L3 16"/><path d="M3 21v-5h5"/>',
    "pencil": '<path d="M21.2 2.8a2.7 2.7 0 0 0-3.8 0l-11 11a2 2 0 0 0-.5.9l-1 3.8a1 1 0 0 0 1.2 1.2l3.8-1a2 2 0 0 0 .9-.5l11-11a2.7 2.7 0 0 0 0-3.8z"/><path d="m15 5 4 4"/>',
}


def ikon(ad: str, sinif: str = "") -> str:
    """20-24pt çizgi ikon. stroke rengi kapsayıcıdan (currentColor) gelir."""
    s = f' class="{sinif}"' if sinif else ""
    return (f'<svg{s} viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{IKON[ad]}</svg>')


# ---------------------------------------------------------------------------
# Kahraman yay geometrisi — tokens.md §7.5 (224 disk · r 86 · kalınlık 16 ·
# 270° · saat 7'de başlar). Değerler v4 prototipinden birebir.
# ---------------------------------------------------------------------------
CAP, MERKEZ, R_OLUK, SWEEP, BAS = 224, 112, 86.0, 270.0, 135.0
CEVRE = 2 * math.pi * R_OLUK * (SWEEP / 360.0)          # 405.26
TAM_CEVRE = 2 * math.pi * R_OLUK                        # 540.35


def _nokta(r: float, derece: float) -> tuple[float, float]:
    t = math.radians(derece)
    return MERKEZ + r * math.cos(t), MERKEZ + r * math.sin(t)


def _yay(r: float) -> str:
    x1, y1 = _nokta(r, BAS)
    x2, y2 = _nokta(r, BAS + SWEEP)
    return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 1 1 {x2:.2f} {y2:.2f}"


def hero_yay(oran: float, tasma_orani: float = 0.0, topuz: bool = True) -> str:
    """Kahraman yay SVG'si. `oran` 0..1 dolgu; `tasma_orani` > 0 ise
    tokens §7.5 taşma yayı (r 102, `grad.arc-over`) eklenir.

    rev2-r1 / B1: bu ekranda dolgu **biriken** demektir
    (`max(0, hesaplanan_tasarruf) / harcanabilir`). Bütçe dışı ayda biriken
    0'dır → ana yay ve topuz **çizilmez**, oluk boş kalır, taşma yayı tek
    başına konuşur. tokens §7.5'in "ana yay %100 kalır" satırı dolgunun
    *harcanan* olduğu Günlük göstergesine aittir."""
    dolgu = CEVRE * min(oran, 1.0)
    parlama = max(dolgu - 14.0, 0.0)
    kx, ky = _nokta(R_OLUK, BAS + SWEEP * min(oran, 1.0))
    tasma = ""
    if tasma_orani > 0:
        r = 102.0
        bx, by = _nokta(r, 270.0)
        ex, ey = _nokta(r, 270.0 + SWEEP)
        cevre_t = 2 * math.pi * r * (SWEEP / 360.0)
        tasma = (f'<path d="M {bx:.2f} {by:.2f} A {r} {r} 0 1 1 {ex:.2f} {ey:.2f}" '
                 f'stroke="url(#gOver)" stroke-width="8" stroke-linecap="round" fill="none" '
                 f'stroke-dasharray="{cevre_t * min(tasma_orani, 1.0):.2f} 900"/>')
    topuz_html = (
        f'<circle cx="{kx:.2f}" cy="{ky + 2:.2f}" r="13.5" fill="rgba(28,57,142,0.18)"/>'
        f'<circle cx="{kx:.2f}" cy="{ky:.2f}" r="13" fill="#FFFFFF"/>'
        f'<circle cx="{kx:.2f}" cy="{ky:.2f}" r="11" fill="none" stroke="#2F68C5" stroke-width="4"/>'
        f'<circle cx="{kx:.2f}" cy="{ky - 2:.2f}" r="8" fill="none" stroke="rgba(255,255,255,0.55)" '
        f'stroke-width="1.5"/>') if oran > 0 and topuz else ""
    dolgu_html = (
        f'<path d="{_yay(R_OLUK)}" stroke="url(#gArc)" stroke-width="16" stroke-linecap="round" '
        f'fill="none" stroke-dasharray="{dolgu:.2f} {TAM_CEVRE:.2f}"/>'
        f'<path d="{_yay(R_OLUK)}" stroke="rgba(255,255,255,0.30)" stroke-width="5" '
        f'stroke-linecap="round" fill="none" stroke-dasharray="{parlama:.2f} {TAM_CEVRE:.2f}" '
        f'stroke-dashoffset="-7"/>') if oran > 0 else ""
    return f'''<svg class="yay" width="{CAP}" height="{CAP}" viewBox="0 0 {CAP} {CAP}" role="img" aria-label="Bu ayın biriken payı">
<defs>
<linearGradient id="gArc" x1="0" y1="1" x2="1" y2="0"><stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2F68C5"/></linearGradient>
<linearGradient id="gOver" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#D97706"/><stop offset="100%" stop-color="#B45309"/></linearGradient>
</defs>
<path d="{_yay(R_OLUK)}" stroke="#E6EFFE" stroke-width="16" stroke-linecap="round" fill="none"/>
<path d="{_yay(92.5)}" stroke="rgba(28,57,142,0.13)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
<path d="{_yay(79.5)}" stroke="rgba(255,255,255,0.95)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
{dolgu_html}
{tasma}{topuz_html}
</svg>'''


def bos_yay() -> str:
    """tokens §7.8 — 176 çukur disk, oluk r 70 / kalınlık 12, dolgu ve topuz yok."""
    m, r = 88.0, 70.0
    x1, y1 = m + r * math.cos(math.radians(BAS)), m + r * math.sin(math.radians(BAS))
    x2, y2 = m + r * math.cos(math.radians(BAS + SWEEP)), m + r * math.sin(math.radians(BAS + SWEEP))
    return (f'<svg class="yay" width="176" height="176" viewBox="0 0 176 176" aria-hidden="true">'
            f'<path d="M {x1:.2f} {y1:.2f} A {r} {r} 0 1 1 {x2:.2f} {y2:.2f}" stroke="#F2F7FE" '
            f'stroke-width="12" stroke-linecap="round" fill="none"/>'
            f'<path d="M {x1:.2f} {y1:.2f} A {r} {r} 0 1 1 {x2:.2f} {y2:.2f}" '
            f'stroke="rgba(28,57,142,0.10)" stroke-width="2" stroke-linecap="round" fill="none" '
            f'transform="translate(0,-3)"/></svg>')


# ---------------------------------------------------------------------------
# Çerçeve / kabuk
# ---------------------------------------------------------------------------
STATUSBAR = '''<div class="statusbar">
<span class="saat">9:41</span>
<span class="right">
<svg viewBox="0 0 17 11" aria-hidden="true"><rect x="0" y="7" width="3" height="4" rx="0.6"/><rect x="4" y="5" width="3" height="6" rx="0.6"/><rect x="8" y="3" width="3" height="8" rx="0.6"/><rect x="12" y="0" width="3" height="11" rx="0.6"/></svg>
<svg viewBox="0 0 17 11" aria-hidden="true"><path d="M8.5 1.5C5.5 1.5 2.7 2.6 0.5 4.6L2 6.1C3.8 4.5 6.1 3.6 8.5 3.6c2.4 0 4.7 0.9 6.5 2.5l1.5-1.5c-2.2-2-5-3.1-8-3.1zM3.5 7.6L5 9.1c1-0.9 2.2-1.4 3.5-1.4 1.3 0 2.5 0.5 3.5 1.4l1.5-1.5c-1.4-1.3-3.1-2-5-2-1.9 0-3.6 0.7-5 2zM6.5 10.6l2 2 2-2c-0.5-0.5-1.2-0.8-2-0.8s-1.5 0.3-2 0.8z"/></svg>
<svg class="battery" viewBox="0 0 25 11" aria-hidden="true"><rect x="0.5" y="0.5" width="21" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-opacity="0.45"/><rect x="22" y="3.5" width="1.5" height="4" rx="0.4" fill="currentColor" fill-opacity="0.45"/><rect x="2" y="2" width="18" height="7" rx="1.4"/></svg>
</span>
</div>'''


def sekme_cubugu(aktif: str) -> str:
    """Günlük / Tasarruf / Profil — FAB YOK (rev2). Üç sekme eşit dağılır."""
    sekmeler = [("gunluk", "Günlük", "gauge"), ("tasarruf", "Tasarruf", "banknote"),
                ("profil", "Profil", "user")]
    parca = []
    for anahtar, ad, ik in sekmeler:
        a = " aktif" if anahtar == aktif else ""
        parca.append(f'<button class="sekme{a}" aria-label="{ad} sekmesi"'
                     f'{" aria-current=\"page\"" if a else ""}>'
                     f'<div class="sekme-ikon-kab">{ikon(ik)}</div><div class="ad">{ad}</div></button>')
    return ('<div class="pad" style="padding-bottom:8px">'
            '<div class="sekme-cubugu" style="justify-content:space-around">'
            + "".join(parca) + "</div></div>")


def cihaz(etiket: str, alt_etiket: str, icerik: str, not_metni: str = "") -> str:
    notu = f'<div class="not-kutu">{not_metni}</div>' if not_metni else ""
    return f'''<div class="sahne-birim">
<div class="baslik-etiket">{etiket} <span>· {alt_etiket}</span></div>
<div class="device">
<span class="btn-rail left-1" aria-hidden="true"></span><span class="btn-rail left-2" aria-hidden="true"></span>
<span class="btn-rail left-3" aria-hidden="true"></span><span class="btn-rail right-1" aria-hidden="true"></span>
<span class="island" aria-hidden="true"></span>
<div class="screen">
{STATUSBAR}
{icerik}
<div class="home-indicator"></div>
</div></div>
{notu}
</div>'''


def sayfa(baslik: str, giris: str, birimler: list[str]) -> str:
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{baslik}</title>
<link rel="stylesheet" href="../prototip-v4/stil.css" />
<link rel="stylesheet" href="stil-rev2.css" />
</head>
<body>
<div class="sayfa-basligi">
<h1>{baslik}</h1>
<p>{giris}</p>
</div>
<div class="sahne">
{"".join(birimler)}
</div>
</body>
</html>'''
