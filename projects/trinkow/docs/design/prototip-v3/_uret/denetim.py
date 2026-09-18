# -*- coding: utf-8 -*-
"""Mekanik öz-denetim: yalnız <main class="content"> blokları taranır."""
import re, sys, pathlib, collections

KOK = pathlib.Path(__file__).parent.parent
YASAK = ["#000000", "rgba(0,0,0", "JetBrains", "monospace", "font-mono", "Figtree",
         "Space Grotesk", "Inter", "grid", "::before", "::after", "sticky", "float:",
         "calc(", "vh", "vw", "z-index", ":hover", "textTransform", "elevation:",
         "useColorScheme", "TRINKOW", "opacity"]
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️⬀-⯿]")
IZIN_RADIUS = {"0", "16", "24", "32", "999", "20", "28", "36", "4"}  # 4 = sheet tutamacı (999 zaten) kontrol altında
IZIN_PUNTO = {"12", "13", "16", "17", "19", "26", "32", "56"}
IZIN_BOSLUK = {"0", "4", "8", "12", "16", "24", "32"}

def mains(html):
    return re.findall(r'<main class="content".*?</main>', html, re.S)

def tara(dosya):
    html = dosya.read_text(encoding="utf-8")
    hata = []
    for m in mains(html):
        for y in YASAK:
            if y in m:
                hata.append(f"yasak dize: {y!r}")
        if EMOJI.search(m):
            hata.append("emoji bulundu")
        for u in re.findall(r'>([^<]*!)[^<]*<', m):
            hata.append(f"ünlem: {u.strip()[:40]}")
        for v in re.findall(r'(?:width|height|padding|margin|top|bottom|left|right)\s*:\s*(-?\d+)px', m):
            pass
        # inline stil boşlukları
        for prop, val in re.findall(r'(padding|margin|gap|padding-top|padding-bottom|margin-top|margin-bottom)\s*:\s*([^;"]+)', m):
            for tok in re.findall(r'(-?\d+)px', val):
                if tok.lstrip("-") not in IZIN_BOSLUK:
                    hata.append(f"boşluk dışı {prop}:{tok}px")
        for tok in re.findall(r'border-radius\s*:\s*(\d+)px', m):
            if tok not in IZIN_RADIUS:
                hata.append(f"radius dışı: {tok}px")
        for tok in re.findall(r'font-size\s*:\s*(\d+)px', m):
            if tok not in IZIN_PUNTO:
                hata.append(f"punto dışı: {tok}px")
        if m.count('class="t-hero"') > 1 or m.count("t-hero ") > 1:
            hata.append("birden fazla 56pt")
        # danger ailesi — izinli DÖRT bağlam (tokens §1.3 · K-029 ölçütü:
        # yüksek etkili + geri alınamaz):
        #   1) E-13 taksit serisi silme onayı   (btn-danger / ikon-kab-danger)
        #   2) E-19 tüm veriyi silme onayı      (btn-danger / ikon-kab-danger)
        #   3) form hatası kenarlığı + metni    (giris-hatali / c-danger)
        #   4) silme toast'ının 8pt göstergesi  (§7.9 · nokta)
        # Taranan tüm kırmızı jetonlar: ham kod + üç değişken. --danger-ink ve
        # --danger-soft de buraya girer, yoksa kırmızı bu ikisiyle sızabilir.
        kalan = m
        # E-19 onay diyaloğundaki "ne silinecek" şeridi: kırmızı yalnız
        # serit-danger'ın HEMEN içindeki ikona izinli (bağlama bağlı kural).
        kalan = re.sub(r'<div class="serit serit-danger">\s*'
                       r'<div class="ikon-kutu" style="color:var\(--danger-ink\)">',
                       '', kalan)
        for izin in ('<button class="btn-danger', '<div class="ikon-kab-danger"',
                     'class="giris hatali"', 'class="giris-hatali"',
                     'class="t-cap c-danger"', 'class="t-body c-danger"',
                     '<div class="nokta" style="background-color:var(--danger)"></div>'):
            kalan = kalan.replace(izin, "")
        for jeton in ("#DC2626", "#C62222", "#FAE1E1", "var(--danger)",
                      "var(--danger-ink)", "var(--danger-soft)"):
            if jeton in kalan:
                hata.append(f"danger izinli bağlam dışında: {jeton}")
    return hata

if __name__ == "__main__":
    hedef = sys.argv[1:] or sorted(p.name for p in KOK.glob("*.html") if p.name != "index.html")
    toplam = 0
    for ad in hedef:
        h = tara(KOK / ad)
        c = collections.Counter(h)
        print(f"--- {ad}: {len(mains((KOK/ad).read_text(encoding='utf-8')))} yüzey · {len(h)} bulgu")
        for k, v in c.items():
            print(f"      {v}x  {k}")
        toplam += len(h)
    print("TOPLAM BULGU:", toplam)
