# -*- coding: utf-8 -*-
"""Mekanik öz-denetim: yalnız <main class="content"> blokları taranır."""
import re, sys, pathlib, collections

KOK = pathlib.Path(__file__).parent.parent
YASAK = ["#000000", "rgba(0,0,0", "JetBrains", "monospace", "font-mono", "Figtree",
         "Space Grotesk", "Inter", "grid", "::before", "::after", "sticky", "float:",
         "calc(", "vh", "vw", "z-index", ":hover", "textTransform", "elevation:",
         "useColorScheme", "TRINKOW", "opacity"]
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️⬀-⯿]")
# T-5/5: "4" KALDIRILDI. tokens.md §4 radius 4'ü tanımıyor; §12/9 izinli
# kümeyi tek satırda sayıyor. Sheet tutamacı 999 kullanıyor, yani izin
# bedelsizdi — açık kalsaydı `.imza-kare{radius:4}` türü sapma (K-054/6'da
# elle yakalanmıştı) bir daha yakalanmazdı.
IZIN_RADIUS = {"0", "16", "24", "32", "999", "20", "28", "36"}
IZIN_PUNTO = {"12", "13", "16", "17", "19", "26", "32", "56"}
IZIN_BOSLUK = {"0", "4", "8", "12", "16", "24", "32"}

# ---------------------------------------------------------------------------
# T-5/6 · stil.css taraması — ÖLÇÜT tokens.md, bu betik değil.
#
# Gerekçe: <main> taraması yalnız gövdeyi görüyordu; renk ve radius
# `stil.css` sınıflarında yaşıyor. "0 bulgu" cümlesi paleti kapsamıyordu.
# Bu yüzden izinli hex ve izinli radius kümeleri **tokens.md'den okunur**,
# buraya elle yazılmaz: token değişirse denetim kendiliğinden değişir.
# ---------------------------------------------------------------------------
TOKENS = KOK.parent.parent / "brand" / "tokens.md"
STIL = KOK / "stil.css"


def tokens_metni():
    """tokens.md'nin **uygulanan** kısmı: §13 ARŞİV hariç.

    §13 reddedilmiş v2/v3 paletlerini ve başka tasarım sistemlerinin
    renklerini anıyor; oradan hex toplamak beyaz listeyi kirletir."""
    m = TOKENS.read_text(encoding="utf-8")
    kes = m.find("## 13. ARŞİV")
    return m[:kes] if kes > 0 else m


def izinli_hexler():
    """Beyaz liste **yalnız tokens.md §1 RENK bölümünden** toplanır.

    v4 birleştirmesinde §7.1 ve §12.0'a üçüncü taraf (Apple/Google) ve
    işletim sistemi klavyesi renkleri yazıldı. Bunlar *istisnanın tanımı*
    olduğu için tüm dosyadan hex toplamak beyaz listeyi genişletir ve
    denetimi zayıflatırdı: `#1F1F1F` bir jeton değildir, Google'ın
    kuralıdır. Palet = §1; istisnalar CSS'te `@denetim-disi` bloklarında.
    §1.6/§1.9'daki gradyan ara durakları bilerek `rgb()` yazılıdır."""
    m = tokens_metni()
    bas = m.find("## 1. RENK")
    son = m.find("## 2. TİPOGRAFİ")
    palet = m[bas:son] if bas >= 0 and son > bas else m
    kume = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", palet)}
    # tokens §1.9 ve §12/1: saf siyah yasak. tokens.md'de yalnız "yasak"
    # satırlarında geçtiği için beyaz listeye girmemeli.
    kume.discard("#000000")
    return kume


def izinli_radius():
    """§12/9 satırı: 'border-radius değerleri | Yalnız 16, 24, 32, 999, 0
    (+ odak 20/28/36)'. Kümeyi o satırdan okuyoruz ki iki yerde tanım
    olmasın (K-040 dersi: kodda bir, dokümanda başka)."""
    for satir in tokens_metni().splitlines():
        if "border-radius" in satir and "Yalnız" in satir:
            return set(re.findall(r"\d+", satir)) - {"9"}
    return IZIN_RADIUS


def yorumsuz(css):
    """Yorum gövdelerini boşluğa çevirir, satır numaraları korunur.
    Gerekçe: gerekçe yazısında geçen bir renk kodu ("...gradyanın ortası
    #3575DD = 4.43") kural ihlali değildir; kuralı anlatan cümledir.
    `@denetim-disi` işaretleri yorumun içinde yaşadığı için onlar korunur."""
    def sil(m):
        g = m.group(0)
        if "@denetim-disi" in g:
            return g
        return "".join(k if k == "\n" else " " for k in g)
    return re.sub(r"/\*.*?\*/", sil, css, flags=re.S)


def stil_bolgeleri(css):
    """`@denetim-disi:` … `@denetim-disi-son` arası bloklar ELENİR.
    Her istisnanın gerekçesi CSS dosyasının içinde, işaretin yanında yazılı
    (kabuk · sistem klavyesi · üçüncü taraf marka varlıkları)."""
    satirlar = css.splitlines()
    disarida, ic, istisna = [], False, 0
    for i, satir in enumerate(satirlar, 1):
        if "@denetim-disi:" in satir:
            ic = True; istisna += 1; continue
        if "@denetim-disi-son" in satir:
            ic = False; continue
        if not ic:
            disarida.append((i, satir))
    return disarida, istisna


def stil_tara():
    hata = []
    css = STIL.read_text(encoding="utf-8")
    satirlar, istisna_sayisi = stil_bolgeleri(yorumsuz(css))
    if istisna_sayisi != 3:
        hata.append(f"beklenen 3 yazılı istisna bloğu, bulunan {istisna_sayisi}")
    hexler, radiuslar = izinli_hexler(), izinli_radius()
    for no, satir in satirlar:
        if satir.lstrip().startswith("/*") or satir.lstrip().startswith("*"):
            continue
        for h in re.findall(r"#[0-9A-Fa-f]{3,6}\b", satir):
            if h.upper() not in hexler:
                hata.append(f"stil.css:{no} palet dışı renk: {h}")
        for r in re.findall(r"border-radius:\s*(\d+)px", satir):
            if r not in radiuslar:
                hata.append(f"stil.css:{no} radius dışı: {r}px")
    return hata


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
    sh = stil_tara()
    print(f"--- stil.css: {len(sh)} bulgu (ölçüt: brand/tokens.md §1 palet + §12/9 radius)")
    for k in sh:
        print(f"      {k}")
    toplam += len(sh)
    for ad in hedef:
        h = tara(KOK / ad)
        c = collections.Counter(h)
        print(f"--- {ad}: {len(mains((KOK/ad).read_text(encoding='utf-8')))} yüzey · {len(h)} bulgu")
        for k, v in c.items():
            print(f"      {v}x  {k}")
        toplam += len(h)
    print("TOPLAM BULGU:", toplam)
