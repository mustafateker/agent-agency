# -*- coding: utf-8 -*-
"""rev2 mekanik öz-denetimi — prototip-v4/_uret/denetim.py'nin rev2 kabuğu.

Ölçüt tekrar yazılmadı: yasak dizeler, izinli hex/radius/punto/boşluk
kümeleri ve `danger` bağlam kuralı v4 betiğinden **birebir** alınır
(`tokens.md` §1/§12'den okuyan fonksiyonlar dahil). Bu dosyanın tek işi
tarama hedefini değiştirmek: rev2 HTML'leri + `stil-rev2.css`.

Fark: `stil-rev2.css` bir DELTA dosyasıdır, `@denetim-disi` bloğu yoktur
(v4 betiği stil.css'te tam 3 blok bekler) — bu yüzden stil taraması
burada yeniden kuruldu, ölçütü yine v4'ün fonksiyonları veriyor.

Çalıştır:  python3 _uret/denetim.py
"""
from __future__ import annotations

import collections
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).parent.parent
V4 = KOK.parent / "prototip-v4" / "_uret"
sys.path.insert(0, str(V4))
from denetim import izinli_hexler, izinli_radius, mains, tara, yorumsuz  # noqa: E402

STIL = KOK / "stil-rev2.css"


def stil_tara() -> list[str]:
    hata: list[str] = []
    hexler, radiuslar = izinli_hexler(), izinli_radius()
    for no, satir in enumerate(yorumsuz(STIL.read_text(encoding="utf-8")).splitlines(), 1):
        if satir.lstrip().startswith(("/*", "*")):
            continue
        for h in re.findall(r"#[0-9A-Fa-f]{3,6}\b", satir):
            if h.upper() not in hexler:
                hata.append(f"{STIL.name}:{no} palet dışı renk: {h}")
        for r in re.findall(r"border-radius:\s*(\d+)px", satir):
            if r not in radiuslar:
                hata.append(f"{STIL.name}:{no} radius dışı: {r}px")
    return hata


if __name__ == "__main__":
    hedef = sys.argv[1:] or sorted(p.name for p in KOK.glob("*.html"))
    toplam = 0
    sh = stil_tara()
    print(f"--- {STIL.name}: {len(sh)} bulgu (ölçüt: brand/tokens.md §1 palet + §12/9 radius)")
    for k in sh:
        print(f"      {k}")
    toplam += len(sh)
    for ad in hedef:
        yol = KOK / ad
        h = tara(yol)
        print(f"--- {ad}: {len(mains(yol.read_text(encoding='utf-8')))} yüzey · {len(h)} bulgu")
        for k, v in collections.Counter(h).items():
            print(f"      {v}x  {k}")
        toplam += len(h)
    print("TOPLAM BULGU:", toplam)
