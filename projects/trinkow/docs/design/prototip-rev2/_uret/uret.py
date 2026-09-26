# -*- coding: utf-8 -*-
"""E-27 Tasarruf + E-28 Profil — rev2/REV3 prototipi (390×844, 15 durum).

Çalıştır:  python3 _uret/uret.py
Çıktı   :  ../tasarruf-profil.html
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import bos_yay, cihaz, hero_yay, ikon, sayfa, sekme_cubugu  # noqa: E402

KOK = pathlib.Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# yardımcılar
# ---------------------------------------------------------------------------
def h(n: int) -> str:
    return f'<div class="h{n}"></div>'


def w(n: int) -> str:
    return f'<div class="w{n}"></div>'


def ekran_basi(cap: str, h1: str, sag: str = "") -> str:
    return (f'<div class="ekran-basi"><div class="esnek kolon">'
            f'<div class="t-cap">{cap}</div><div class="t-h1 tek-satir">{h1}</div></div>{sag}</div>')


def kart(ic: str, sinif: str = "clay") -> str:
    return f'<div class="pad"><div class="{sinif} kart-ic">{ic}</div></div>'


def bolum(baslik: str, sag: str = "") -> str:
    sag_html = f'<div class="t-label c-2" style="flex:0 0 auto">{sag}</div>' if sag else ""
    return (f'<div class="pad aralik"><div class="t-h2 esnek tek-satir">{baslik}</div>'
            f'{w(12) if sag else ""}{sag_html}</div>')


def ikon_btn(ad: str, etiket: str, pasif: bool = False) -> str:
    p = " pasif" if pasif else ""
    ek = ' disabled aria-disabled="true"' if pasif else ""
    return f'<button class="ikon-btn{p}" aria-label="{etiket}"{ek}>{ikon(ad)}</button>'


def cip(metin: str, etiket: str, secili: bool = False, nokta: bool = False,
        chevron: bool = False) -> str:
    s = " secili" if secili else ""
    ic = ('<div class="nokta"></div>' + w(8)) if nokta else ""
    ic += f'<div class="cip-ad">{metin}</div>'
    if chevron:
        ic += w(8) + ikon("chevron-right")
    etiketli = f' aria-label="{etiket}"' if etiket else ""
    return f'<button class="cip{s}" style="flex:0 0 auto"{etiketli}>{ic}</button>'


def denklem(kutular: list[tuple[str, str, str]], isaretler: tuple[str, str] = ("−", "=")) -> str:
    parca = []
    for i, (etiket, tutar, sinif) in enumerate(kutular):
        if i:
            parca.append(f'<div class="denklem-op"><div class="t-body c-2">{isaretler[i - 1]}</div></div>')
        parca.append(f'<div class="denklem-kutu {sinif}"><div class="t-micro">{etiket}</div>'
                     f'{h(4)}<div class="t-amount num">{tutar}</div></div>')
    return f'<div class="denklem">{"".join(parca)}</div>'


def gun_sayaci(sag: str) -> str:
    """Ö11 — tamamlanan gün artık ÇUBUK değil, tek satır metin.
    Gerekçe: aynı ekranda 8pt `grad.action` (zaman) ile 12pt `grad.action`
    (birikim hedefi) yan yana iki farklı şey anlatıyordu. Mavi ilerleme dili
    bu ekranda tek: hedef çubuğu."""
    return (f'<div class="aralik"><div class="t-cap esnek">Tamamlanan gün</div>{w(12)}'
            f'<div class="t-micro num" style="flex:0 0 auto">{sag}</div></div>')


def hedef_cubuk(yuzde: float) -> str:
    dolgu = (f'<div class="yuk-dolgu" style="width:{yuzde:.1f}%"></div>' if yuzde > 0 else "")
    return f'<div class="cubuk-oluk">{dolgu}</div>'


def hareket_satiri(gun: str, ay_kisa: str, birincil: str, not_metni: str,
                   tutar: str, tutar_alti: str = "", basili: bool = False) -> str:
    """Ö8 — sol kap artık `banknote` değil, E-15'teki `.gun-kutu` deseni:
    kategori sabitken sol sütun **günü** taşır. Yeni glif eklenmedi, `banknote`
    tekrarı bitti ve tarih ikincil satırdan öne çıktı.

    Not yoksa ikincil satır **çizilmez** (boş satır bırakılmaz); satır 68pt
    minimumunda kalır, birincil satır dikeyde ortalanır."""
    b = " basili" if basili else ""
    alt = f'{h(4)}<div class="t-cap">{tutar_alti}</div>' if tutar_alti else ""
    ikincil = f'<div class="t-cap tek-satir">{not_metni}</div>' if not_metni else ""
    # REV3 — satır artık akordiyon bölümünün İÇİNDE duruyor: kap `clay.raised`
    # olduğu için satır bir basamak iner (`kuyu` = well + clay.sunken) ve
    # içindeki gün kutusu bir basamak çıkar. Aynı yükseklik iç içe iki kez
    # söylenmez (§9/3).
    return (f'<div class="satir-kart kuyu{b}">'
            f'<div class="gun-kutu"><div class="t-label num">{gun}</div>'
            f'<div class="t-micro">{ay_kisa}</div></div>{w(12)}'
            f'<div class="esnek kolon"><div class="t-body tek-satir">{birincil}</div>'
            f'{ikincil}</div>{w(12)}'
            f'<div class="kolon" style="align-items:flex-end;flex:0 0 auto">'
            f'<div class="t-amount num">{tutar}</div>{alt}</div></div>')


def kategori_satiri(sinif: str, ikon_ad: str, ad: str, tutar: str, oran: float,
                    pay: str, ek: str = "") -> str:
    renk = sinif.replace("kat-", "--cat-")
    ek_html = f'<div class="t-label c-2" style="flex:0 0 auto">{ek}</div>' if ek else ""
    return (f'<div class="satir"><div class="kat-kab {sinif}">{ikon(ikon_ad)}</div>{w(12)}'
            f'<div class="esnek kolon">'
            f'<div class="aralik"><div class="t-strong esnek tek-satir">{ad}</div>{w(12)}'
            f'<div class="t-amount num" style="flex:0 0 auto">{tutar}</div></div>{h(8)}'
            f'<div class="cubuk-oluk"><div class="cubuk-dolgu" '
            f'style="width:{oran:.1f}%;background-color:var({renk})"></div></div>{h(4)}'
            f'<div class="aralik"><div class="t-cap">{pay}</div>{w(12)}{ek_html}</div>'
            f'</div></div>')


def serit(tur: str, ikon_ad: str, metin: str) -> str:
    renk = "c-warn" if tur == "serit-warn" else "c-primary"
    return (f'<div class="pad"><div class="serit {tur}">'
            f'<div class="ikon-kutu {renk}">{ikon(ikon_ad)}</div>{w(12)}'
            f'<div class="t-cap esnek" style="color:var(--text)">{metin}</div></div></div>')


def iskelet(gen: str, yuk: int) -> str:
    return f'<div class="iskelet" style="width:{gen};height:{yuk}px"></div>'


def bos_disk(ikon_ad: str) -> str:
    """tokens §7.8 — 176pt KABARIK disk (surface + clay.raised-lg), içindeki
    oluk çukur (groove). Ortada 32pt ikon."""
    return (f'<div class="hero-daire hero-daire-bos">{bos_yay()}'
            f'<div class="hero-orta"><div class="ikon-kutu ikon-kutu-32 c-2">{ikon(ikon_ad)}'
            f'</div></div></div>')


def akordiyon(baslik: str, ozet: str, icerik: str = "", basili: bool = False,
              iskelet_ozet: bool = False) -> str:
    """REV3 — E-27'nin bölüm kabı (`Accordion`).

    · Dokunma hedefi **başlık satırı** (358×44+), görsel geri bildirim
      **kabın tamamı** (`.akordiyon.basili` → groove + clay.pressed).
    · Başlığın sağı **kapalıyken özet değer** taşır: kapalı bölüm asla boş
      bir başlık değildir. **Açıkken özet çizilmez** — içerik o değeri
      zaten taşıyor (A: denklem sonuç kutusu · B: tutar satırı ·
      C: "Harcanan" satırı · D: "Vazgeçtiğin rutinler" satırı) ve iki
      santim arayla aynı sayıyı iki kez yazmak bilgi değil gürültüdür.
    · Ok tek glif: `chevron-down`, açıkken 180° döner (yeni glif yok).
    · Birden çok bölüm açık kalabilir; kullanıcı bir bölümü açınca başka
      bölüm kapanmaz (kapanma kaydırma konumunu altından çeker).
    """
    acik = bool(icerik)
    if iskelet_ozet and not acik:
        # Yükleme: başlık gerçek, özetin YERİ korunur (yükleme bitince
        # başlık satırı zıplamaz).
        sag = f'<div style="flex:0 0 auto">{iskelet("104px", 18)}</div>' + w(12)
    elif acik:
        sag = ""
    else:
        sag = (f'<div class="t-label c-2 num tek-satir" style="flex:0 0 auto">{ozet}</div>'
               + w(12))
    # Ö5 — özet BOŞ geldiğinde (yalnız iskelet hâli) etiket "{başlık}. " diye
    # yarım kalmaz: ekran okuyucu ne beklediğini duyar.
    ozet_etiket = ozet or "Yükleniyor"
    bas = (f'<button class="akordiyon-bas" aria-expanded="{"true" if acik else "false"}" '
           f'aria-label="{baslik}. {ozet_etiket}">'
           f'<div class="t-h2 esnek tek-satir">{baslik}</div>{w(12)}{sag}'
           f'{ikon("chevron-down", "cev-acik" if acik else "")}</button>')
    b = " basili" if basili else ""
    return (f'<div class="pad"><div class="akordiyon{b}">{bas}'
            f'{(h(12) + icerik) if acik else ""}</div></div>')


def ekran(icerik: str, aktif: str, sarmala: bool = True) -> str:
    if not sarmala:
        return f'<main class="content">{icerik}</main>'
    return (f'<main class="content"><div class="kaydir">{icerik}{h(24)}</div>'
            f'{sekme_cubugu(aktif)}</main>')


# ---------------------------------------------------------------------------
# kahraman kart (E-27)
# ---------------------------------------------------------------------------
def hero_kart(butce_cip: str, gosterge: str, cumle: str, onceki_pasif: bool = False,
              sonraki_pasif: bool = True, ek: str = "") -> str:
    return f'''<div class="pad"><div class="hero-kart kart-ic kolon orta">
<div class="aralik" style="width:100%">
{cip("Tasarruf", "Kip: Tasarruf. Değiştirmek için ayarları aç", secili=True, nokta=True)}
{butce_cip}
</div>
{h(12)}
<div class="aralik" style="width:100%">
{ikon_btn("chevron-left", "Önceki ay", onceki_pasif)}
{gosterge}
{ikon_btn("chevron-right", "Sonraki ay", sonraki_pasif)}
</div>
{h(12)}
{cumle}
{ek}
</div></div>'''


def gosterge_dolu(sayi: str, etiket: str, oran: float, tasma: float = 0.0,
                  uyari: bool = False) -> str:
    """tokens §7.5 — yayın iç alanı 2×(86−8) = **156px** (tek değer; §2.3'teki
    198 rakamı 296'lık eski diskten kalmıştı, rev2-r1'de düzeltildi).

    `{sayi} ₺` 6 karakteri aşıyorsa rol bir basamak iner: hero 56 -> display 32,
    ₺ 32 -> amount 17. Ara punto üretilmez. Ölçüldü (Montserrat-Bold.ttf,
    prototip-v4/fonts) — H3: ölçüm `tabular-nums` genişliğiyle yapılır, çünkü
    tokens §2.3 para için tabular'ı zorunlu kılar (her rakam 700/1000 em):
    `820 ₺` hero 139px ✅ · `1.250 ₺` = `6.240 ₺` hero 189px ❌ ·
    `12.500 ₺` hero 226px ❌ → 4+ haneli tutar daima `display`.

    B1 — dolgu formülü (tek kaynak; §3.2 ve §5 birebir aynı):
        dolgu  = max(0, hesaplanan_tasarruf) / harcanabilir
        taşma  = min(1, |min(0, hesaplanan_tasarruf)| / harcanabilir)
    Bütçe dışı ayda dolgu 0'dır: ana yay ve topuz çizilmez."""
    u = " c-warn" if uyari else ""
    genis = len(f"{sayi} ₺") > 6
    sayi_rolu = "t-display" if genis else "t-hero"
    simge_rolu = "t-amount" if genis else "t-hero-simge"
    simge_u = (" c-warn" if uyari else "") if genis else u
    return (f'<div class="hero-daire">{hero_yay(oran, tasma, topuz=oran > 0)}<div class="hero-orta">'
            f'<div class="para-hero"><div class="{sayi_rolu} num{u}">{sayi}</div>{w(4)}'
            f'<div class="{simge_rolu}{simge_u}">₺</div></div>{h(4)}'
            f'<div class="t-label {"c-warn" if uyari else "c-2"}">{etiket}</div></div></div>')


# ===========================================================================
# F1 — Tasarruf · dolu ay
# ===========================================================================
# "rutin {tutar}" etiketi rutin kartıyla BİREBİR toplanır (§3.8 kuralı:
# yalnız `rutin_tasarruf_kurus > 0` olan kategoride görünür):
#   Kafe   = Kahve 620 + Enerji içeceği 140 = 760 ₺
#   Market = Sigara 480                     = 480 ₺
#   toplam 1.240 ₺  →  rutin kartının başlık tutarı ve Profil'deki
#   "3 rutin · bu ay 1.240 ₺ tasarruf" satırı ile aynı sayı.
KATEGORILER = [
    ("kat-yesil", "shopping-basket", "Market", "4.180 ₺", 100.0, "payı %27", "rutin 480 ₺"),
    ("kat-amber", "coffee", "Kafe", "3.240 ₺", 77.5, "payı %21", "rutin 760 ₺"),
    ("kat-amber", "utensils", "Restoran", "2.940 ₺", 70.3, "payı %19", ""),
    ("kat-mavi", "bus", "Ulaşım", "1.860 ₺", 44.5, "payı %12", ""),
]

RUTINLER = [("Kahve", "620 ₺"), ("Sigara", "480 ₺"), ("Enerji içeceği", "140 ₺")]

# Ö10 — listede en çok 5 satır; kalanı "Tüm hareketler" ghost düğmesinde.
# Eylül'ün 7 hareketinden en yenisi 5'i çizilir. Görünen net +4.000 ₺,
# gizli iki hareketle birlikte ayın neti +4.600 ₺ (kartın sağ üst satırı).
# İkinci satır NOT'tur; notsuz hareket (19 Eylül) tek satır kalır.
HAREKETLER = [
    ("22", "Eyl", "Birikime eklendi", "Kenara ayırdım", "1.500 ₺", "", False),
    ("19", "Eyl", "Birikime eklendi", "", "600 ₺", "", False),
    ("12", "Eyl", "Birikime eklendi", "Maaş günü", "2.000 ₺", "", False),
    ("6", "Eyl", "Birikimden çekildi", "Acil gider", "500 ₺", "çekildi", True),
    ("3", "Eyl", "Birikime eklendi", "Bozuk para kavanozu", "400 ₺", "", False),
]


def ghost(etiket: str, a11y: str) -> str:
    return (f'<button class="btn-ghost" style="padding:0 16px" aria-label="{a11y}">'
            f'<div class="tek-satir">{etiket}</div></button>')


def serit_ic(tur: str, ikon_ad: str, metin: str) -> str:
    """`serit()`in `.pad` sarmalayıcısı olmayan ikizi — akordiyon bölümünün
    İÇİNDE kullanılır. Kap kabarık (`clay.raised`), şerit çukur
    (`clay.sunken`): iki basamak birbirinden ayrı okunur."""
    renk = "c-warn" if tur == "serit-warn" else "c-primary"
    return (f'<div class="serit {tur}"><div class="ikon-kutu {renk}">{ikon(ikon_ad)}</div>'
            f'{w(12)}<div class="t-cap esnek" style="color:var(--text)">{metin}</div></div>')


# --- A · bütçe ------------------------------------------------------------
def butce_icerik(kutular, sabit: str, gun: str, kumulatif: str, ust: str = "") -> str:
    """REV3 — akordiyon bölümü A'nın içeriği. Başlık ve özet kabuğa taşındı;
    "1–30 Eylül" satırı KALDIRILDI (ekran başlığı ayı zaten söylüyor ve
    gün sayacı aynı satırda gün sayısını veriyor)."""
    return ((ust + h(12) if ust else "") + denklem(kutular) + h(12) +
            f'<div class="t-cap">{sabit}</div>' + h(12) + gun_sayaci(gun) + h(12) +
            f'<div class="t-cap">{kumulatif}</div>')


# --- B · gerçek birikim + hareketler (REV3'te tek bölüm) ------------------
def birikim_icerik(tutar: str, ay_satiri: str, yuzde: float, hedef: str,
                   motivasyon: str = "", hareketler=(), sayi: str = "",
                   bos_cumle: str = "") -> str:
    """REV3 — "Gerçek birikim" ve "Birikim hareketleri" **tek bölümde**
    birleşti: ikisi aynı kavramın değeri ve kanıtıdır (§1.2). Bölüm sayısı
    5'ten 4'e indi, ekranın bilgi yoğunluğu düştü.

    B4 korunuyor: tutar `amount` 17'dir, `display` 32 değil — ekranın tek
    kahraman sayısı göstergenin ortasındadır."""
    ic = ('<div class="aralik"><div class="t-cap esnek tek-satir">' + ay_satiri + '</div>' +
          w(12) + f'<div class="t-amount num" style="flex:0 0 auto">{tutar}</div></div>' +
          h(12) + hedef_cubuk(yuzde) + h(4) +
          f'<div class="aralik"><div class="t-cap">Hedef {hedef}</div>' + w(12) +
          f'<div class="t-label c-2 num" style="flex:0 0 auto">%{yuzde:.0f}</div></div>')
    if motivasyon:
        ic += h(12) + serit_ic("serit-info", "target", motivasyon)
    ic += (h(12) + '<button class="btn-secondary" aria-label="Birikim hareketi ekle">'
           + ikon("plus") + w(8) + '<div class="tek-satir">Birikim hareketi ekle</div></button>')
    if hareketler:
        ic += (h(12) + '<div class="aralik"><div class="t-label c-2">Son hareketler</div>' +
               w(12) + f'<div class="t-label c-2 num" style="flex:0 0 auto">{sayi}</div></div>' +
               h(8) + f'{h(8)}'.join(hareket_satiri(*s) for s in hareketler) +
               h(12) + ghost("Tüm hareketler", "Tüm birikim hareketlerini aç"))
    elif bos_cumle:
        # Akordiyon içinde boş bölüm ILLÜSTRASYONSUZDUR: 176pt kabarık disk
        # (tokens §7.8) bir EKRAN/bölüm boşluğu için tanımlı; 358pt genişlikte
        # bir bölüm kabının içine girince kapla aynı yüksekliği iki kez söyler
        # ve açılan bölümü ikinci bir kahramana çevirir.
        ic += h(12) + f'<div class="t-cap">{bos_cumle}</div>'
    return ic


# --- C · kategori dağılımı ------------------------------------------------
def kategori_icerik(satirlar, harcanan: str = "", bos: tuple[str, str] = ()) -> str:
    if not satirlar:
        return (f'<div class="t-body">{bos[0]}</div>' + h(8) +
                f'<div class="t-cap">{bos[1]}</div>')
    # B3 — kategori satırları arası 12 (tokens §3.1 bağlayıcı tablosu).
    ic = ('<div class="aralik"><div class="t-cap">Harcanan</div>' + w(12) +
          f'<div class="t-amount num" style="flex:0 0 auto">{harcanan}</div></div>' + h(12))
    ic += f'{h(12)}'.join(kategori_satiri(*s) for s in satirlar)
    return ic + h(12) + ghost("Tümünü gör", "Tüm kategori paylarını aç")


# --- D · rutin tasarrufu --------------------------------------------------
def rutin_icerik(toplam: str, satirlar, bos_cumle: str = "") -> str:
    """REV3 — bölüm KALDI, çünkü rutin tasarrufunun toplamı ürünün başka
    hiçbir yüzeyinde toplanmıyor (kategori satırlarında parça parça, Profil
    satırında tek satır). Kalkan şey hızlı eylemdir: "bugün aldım/almadım"
    artık Günlük ekranındaki rutin satırında (rev3-gunluk-rutin.md).

    Satırlarda `repeat` ikon kabı YOK: üç satırın üçü de rutin olduğu için
    aynı glif hiçbir şeyi ayırmıyordu (Ö8'in gerekçesiyle aynı)."""
    if satirlar:
        ic = ('<div class="aralik"><div class="t-cap esnek">Vazgeçtiğin rutinler</div>' +
              w(12) + f'<div class="t-amount num" style="flex:0 0 auto">{toplam}</div></div>' +
              h(4) + '<div class="t-cap">Bütçedeki kalana eklenmez.</div>' + h(12) +
              f'{h(12)}'.join(
                  f'<div class="aralik"><div class="t-body esnek tek-satir">{ad}</div>{w(12)}'
                  f'<div class="t-amount num" style="flex:0 0 auto">{tutar}</div></div>'
                  for ad, tutar in satirlar))
    else:
        ic = f'<div class="t-cap">{bos_cumle}</div>'
    return ic + h(12) + ghost("Rutinleri aç", "Rutinleri aç")


# REV3 — dört bölümün özet değerleri tek yerde (kapalı hâl asla boş başlık
# değildir). Metin karşılıkları metinler.md §28.3'te.
OZET = {
    "butce": "Kalan 8.760 ₺",
    "birikim": "9.500 ₺ · hedefin %95'i",
    "kategori": "Harcanan 15.240 ₺",
    "rutin": "1.240 ₺ · 3 rutin",
}

F1 = ekran(
    ekran_basi("Eylül 2026 · ay devam ediyor", "Tasarruf")
    + hero_kart(
        cip("Bütçe 24.000 ₺", "Bütçe 24.000 ₺. Bütçeyi aç", chevron=True),
        gosterge_dolu("6.240", "bu ay biriken", 0.26),
        '<div class="t-body" style="text-align:center">Kaydettiğin gelir ve harcamalara göre '
        '22 gün hesaplandı.</div>')
    + h(8)
    # B1 (REV3-r1) — kahraman ↔ akordiyon grubu arası 24 DEĞİL 8. Kaydırma
    # alanı 844 − 47 − 28 − 76 = 693 (yüzen sekme çubuğu bu alanın DIŞINDA).
    # 24 ile A'nın kabı 704'te bitiyordu, yani kesme kartın alt kenarından
    # geçiyordu; 8 ile A 688'de bitiyor ve kesme A ile B arasındaki 8pt
    # boşluğa düşüyor. Ölçümün tamamı rev2-tasarruf-profil.md §3.12.1'de.
    + akordiyon("Bu ayın bütçesi", OZET["butce"], butce_icerik(
        [("Harcanabilir", "24.000 ₺", ""), ("Harcanan", "15.240 ₺", ""),
         ("Kalan", "8.760 ₺", "sonuc")],
        "Sabit ödemeler dahil toplam 18.400 ₺", "22/30 gün",
        "Takip başından beri biriken 21.180 ₺"))
    + h(8)
    + akordiyon("Gerçek birikim", OZET["birikim"])
    + h(8)
    + akordiyon("Kategori dağılımı", OZET["kategori"])
    + h(8)
    + akordiyon("Rutin tasarrufu", OZET["rutin"])
    , "tasarruf")

# ===========================================================================
# F12 — Tasarruf · "Gerçek birikim" bölümü açık (B)
# ===========================================================================
F12 = ekran(
    ekran_basi("Eylül 2026 · ay devam ediyor", "Tasarruf")
    + hero_kart(
        cip("Bütçe 24.000 ₺", "Bütçe 24.000 ₺. Bütçeyi aç", chevron=True),
        gosterge_dolu("6.240", "bu ay biriken", 0.26),
        '<div class="t-body" style="text-align:center">Kaydettiğin gelir ve harcamalara göre '
        '22 gün hesaplandı.</div>')
    + h(8)
    # Basılı KAPALI başlık: kullanıcı B açıkken A'yı da açıyor — "çoklu açık
    # serbest" kuralının kendisi. Geri bildirim kabın tamamının çökmesidir.
    + akordiyon("Bu ayın bütçesi", OZET["butce"], basili=True)
    + h(8)
    + akordiyon("Gerçek birikim", OZET["birikim"], birikim_icerik(
        "9.500 ₺", "Bu ay 4.600 ₺ eklendi", 95.0, "10.000 ₺",
        motivasyon="Bu tutarı birikim hedefin için ayırmayı düşünebilirsin.",
        hareketler=HAREKETLER, sayi="7 kayıt"))
    + h(8)
    + akordiyon("Kategori dağılımı", OZET["kategori"])
    + h(8)
    + akordiyon("Rutin tasarrufu", OZET["rutin"])
    , "tasarruf")

# ===========================================================================
# F13 — Tasarruf · C ve D birlikte açık + bir başlık basılı
# ===========================================================================
# Bu çerçeve ekranı **kaydırılmış** gösterir: açık bölümlerin içeriği ilk
# katın altındadır. Kesme bir kart sınırından geçer (başlık ve kahraman kart
# yukarıda kaldı), hiçbir nesne ortasından bölünmez — K-057/8.
F13 = ekran(
    akordiyon("Bu ayın bütçesi", OZET["butce"])
    + h(8)
    + akordiyon("Gerçek birikim", OZET["birikim"])
    + h(8)
    # Basılı AÇIK başlık: aynı kap çöker, ok 180° dönmüş hâlde kalır. Kapalı
    # hâlin basılı karşılığı F12'de (A) duruyor.
    + akordiyon("Kategori dağılımı", OZET["kategori"],
                kategori_icerik(KATEGORILER, "15.240 ₺"), basili=True)
    + h(8)
    + akordiyon("Rutin tasarrufu", OZET["rutin"], rutin_icerik("1.240 ₺", RUTINLER))
    , "tasarruf")

# ===========================================================================
# F14 — Tasarruf · kısmi hata (B açılamadı) + veri olmayan açık bölüm (C)
# ===========================================================================
# Bu çerçeve ekranı **kaydırılmış** gösterir: açık bölümlerin içeriği ilk
# katın altındadır. Kesme bir kart sınırından geçer (başlık ve kahraman kart
# yukarıda kaldı), hiçbir nesne ortasından bölünmez — K-057/8.
F14 = ekran(
    akordiyon("Bu ayın bütçesi", OZET["butce"])
    + h(8)
    + akordiyon("Gerçek birikim", "Açılamadı",
                serit_ic("serit-warn", "wifi-off", "Birikim kayıtları açılamadı.") + h(12) +
                '<button class="btn-secondary" aria-label="Yeniden dene">' + ikon("repeat") +
                w(8) + '<div class="tek-satir">Yeniden dene</div></button>')
    + h(8)
    + akordiyon("Kategori dağılımı", "Harcama yok",
                kategori_icerik([], bos=("Bu ay henüz harcama yazmadın.",
                                         "İlk kaydından sonra kategori payları burada görünür.")))
    + h(8)
    + akordiyon("Rutin tasarrufu", "Rutin eklemedin")
    , "tasarruf")

# ===========================================================================
# F2 — Tasarruf · bütçe dışı kapanmış ay + eksik gelir günü
# ===========================================================================
F2 = ekran(
    ekran_basi("Ağustos 2026 · ay kapandı", "Tasarruf")
    + hero_kart(
        cip("Bütçe 22.000 ₺", "Bütçe 22.000 ₺. Bütçeyi aç", chevron=True),
        # B1: bütçe dışı ayda dolgu = max(0, −2.150)/22.000 = 0 → ana yay
        # ÇİZİLMEZ, oluk boş kalır. Taşma yayı tek başına konuşur.
        gosterge_dolu("2.150", "bütçe dışı", 0.0, 2150 / 22000, uyari=True),
        '<div class="t-body" style="text-align:center">Ağustos\'ta harcaman bütçenin 2.150 ₺ '
        'üzerinde.</div>',
        sonraki_pasif=False)
    + h(8)
    # B5: seçili ay geçmiş ay → "Bu ayın bütçesi" değil "Ayın bütçesi";
    # "bu ay …" kalıbı "Ağustos'ta …" olur. REV3: eksik gelir şeridi artık
    # ekranın ortasında değil, ilgili bölümün İÇİNDE — hangi sayıyı
    # etkilediği belirsiz kalmıyor.
    + akordiyon("Ayın bütçesi", "Bütçe dışı 2.150 ₺", butce_icerik(
        [("Harcanabilir", "22.000 ₺", ""), ("Harcanan", "24.150 ₺", ""),
         ("Bütçe dışı", "2.150 ₺", "disinda")],
        "Sabit ödemeler dahil toplam 26.900 ₺", "31/31 gün",
        "Takip başından beri biriken 14.940 ₺",
        ust=serit_ic("serit-warn", "info", "3 günün geliri eksik. O günler hesaba katılmadı.")))
    + h(8)
    + akordiyon("Gerçek birikim", "9.500 ₺ · Ağustos'ta kayıt yok")
    + h(8)
    + akordiyon("Kategori dağılımı", "Harcanan 24.150 ₺")
    + h(8)
    + akordiyon("Rutin tasarrufu", "0 ₺ · 3 rutin")
    , "tasarruf")

# ===========================================================================
# F3 — Tasarruf · ilk ay, gelir yok (HeroPlain + tek birincil eylem)
# ===========================================================================
F3 = ekran(
    ekran_basi("Eylül 2026 · ay devam ediyor", "Tasarruf")
    + hero_kart(
        cip("Bütçe yok", "Bütçe tanımlı değil. Bütçeyi aç", chevron=True),
        bos_disk("landmark"),
        '<div class="t-h2">Gelirini ekle</div>' + h(8) +
        '<div class="t-body" style="text-align:center">Aylık gelirini yazınca bu ayın payını '
        'hesaplarız.</div>',
        ek=h(12) + '<button class="btn-primary" aria-label="Bütçeyi düzenle">'
                   '<div class="tek-satir">Bütçeyi düzenle</div></button>')
    + h(8)
    # Gelir yokken A bölümünün içeriği denklem DEĞİL, tek satır olgudur:
    # uydurma bir "0 ₺ − 0 ₺ = 0 ₺" denklemi kurulmaz. İkinci bir birincil
    # düğme de yok — "Bütçeyi düzenle" 200px yukarıda, kahramanın içinde.
    + akordiyon("Bu ayın bütçesi", "Gelir eksik",
                serit_ic("serit-info", "info",
                         "Takip 23 Eylül'de başladı. Ayın 8 günü hesaplanacak.") + h(12) +
                '<div class="t-cap">Gelirini yazınca harcanabilir, harcanan ve kalan burada '
                'görünür.</div>')
    + h(8)
    + akordiyon("Gerçek birikim", "0 ₺ · hedef 10.000 ₺")
    + h(8)
    + akordiyon("Kategori dağılımı", "Harcama yok")
    + h(8)
    + akordiyon("Rutin tasarrufu", "Rutin eklemedin")
    , "tasarruf")

# ===========================================================================
# F4 — Tasarruf · yükleniyor (iskelet)
# ===========================================================================
def iskelet_yay() -> str:
    from lib import _yay  # noqa: PLC0415
    return (f'<svg class="yay" width="224" height="224" viewBox="0 0 224 224" aria-hidden="true">'
            f'<path d="{_yay(86.0)}" stroke="#E6EFFE" stroke-width="16" stroke-linecap="round" fill="none"/>'
            f'<path d="{_yay(92.5)}" stroke="rgba(28,57,142,0.13)" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
            f'<path d="{_yay(79.5)}" stroke="rgba(255,255,255,0.95)" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
            f'</svg>')


F4 = ekran(
    ekran_basi("Eylül 2026", "Tasarruf")
    + f'''<div class="pad"><div class="hero-kart kart-ic kolon orta">
<div class="aralik" style="width:100%">{cip("Tasarruf", "Kip: Tasarruf. Değiştirmek için ayarları aç", secili=True, nokta=True)}
{iskelet("132px", 40)}</div>
{h(12)}
<div class="aralik" style="width:100%">{ikon_btn("chevron-left", "Önceki ay")}
<div class="hero-daire">{iskelet_yay()}<div class="hero-orta">{iskelet("140px", 38)}{h(4)}
{iskelet("88px", 18)}</div></div>
{ikon_btn("chevron-right", "Sonraki ay", True)}</div>
{h(12)}<div class="t-cap">Hesaplanıyor</div>{h(12)}{iskelet("60%", 18)}
</div></div>'''
    + h(8)
    # REV3 — akordiyon iskeleti: BAŞLIKLAR GERÇEK (metin ilk karede hazır),
    # yalnız özet değerlerin ve açık bölümün içeriğinin yeri çukur bloklarla
    # korunur. Ö14 kuralı sürüyor: iskelet yüklü düzenin birebir aynası,
    # yükleme bitince hiçbir satır zıplamaz.
    + akordiyon("Bu ayın bütçesi", "", icerik=(
        '<div class="denklem">' +
        '<div class="denklem-op"></div>'.join(
            f'<div class="denklem-kutu">{iskelet("64%", 12)}{h(4)}{iskelet("100%", 24)}</div>'
            for _ in range(3)) +
        "</div>" + h(12) + iskelet("100%", 18) + h(12) +
        '<div class="aralik">' + iskelet("112px", 18) + w(12) +
        '<div style="flex:0 0 auto">' + iskelet("72px", 16) + "</div></div>" + h(12) +
        iskelet("60%", 18)))
    + h(8)
    + akordiyon("Gerçek birikim", "", iskelet_ozet=True)
    + h(8)
    + akordiyon("Kategori dağılımı", "", iskelet_ozet=True)
    + h(8)
    + akordiyon("Rutin tasarrufu", "", iskelet_ozet=True)
    , "tasarruf")

# ===========================================================================
# F5 — Tasarruf · hata (ay gezinmesi çalışmaya devam eder)
# ===========================================================================
F5 = ekran(
    ekran_basi("Tasarruf verisi", "Tasarruf")
    + '<div class="pad aralik">' + ikon_btn("chevron-left", "Önceki ay") +
    '<div class="t-label">Eylül 2026</div>' + ikon_btn("chevron-right", "Sonraki ay", True) + "</div>"
    + h(24)
    + kart('<div class="kolon orta">'
           f'<div class="hata-daire">{ikon("wifi-off")}</div>' + h(12) +
           '<div class="t-h2">Bilgiler yüklenemedi</div>' + h(8) +
           '<div class="t-body" style="text-align:center">Bağlantını kontrol edip yeniden '
           'dene.</div>' + h(12) +
           '<button class="btn-secondary" aria-label="Yeniden dene">' + ikon("repeat") + w(8) +
           '<div class="tek-satir">Yeniden dene</div></button></div>', "clay-lg")
    , "tasarruf")

# ===========================================================================
# F6 / F7 — Birikim hareketi bottom sheet (varsayılan · hatalı)
# ===========================================================================
# İşletim sisteminin ondalık klavyesi — bölge [A], RN'e kodlanmaz.
# Prototipte yalnız "klavye açıkken ekranın ne kadarı kalıyor" sorusuna
# dürüst cevap vermek için duruyor; marka dili bilerek uygulanmadı.
KLAVYE = '''<div class="sistem-klavye">
<div class="ksatir"><div class="ktus">1</div><div class="ktus">2</div><div class="ktus">3</div></div>
<div class="ksatir"><div class="ktus">4</div><div class="ktus">5</div><div class="ktus">6</div></div>
<div class="ksatir"><div class="ktus">7</div><div class="ktus">8</div><div class="ktus">9</div></div>
<div class="ksatir"><div class="ktus koyu">,</div><div class="ktus">0</div><div class="ktus koyu">Sil</div></div>
</div>'''


def sheet(hatali: bool, klavye: bool, duzenleme: bool = False) -> str:
    """B2 — kuyu (`well`) zemininde `text-3` KULLANILMAZ (4.50, tokens §1.2):
    pasif tutar ve "İsteğe bağlı" placeholder'ı `text-2` (5.13 AA).

    Ö9 — `duzenleme=True`: var olan bir hareketin kipi. Başlık "Hareketi
    düzenle", altında `button.ghost` "Sil". Kaydırma kısayol olarak kalır,
    ama silme artık keşfedilebilir."""
    giris_sinif = "giris giris-hatali" if hatali else "giris odakli"
    tutar_ic = ('<div class="t-display num c-2">0</div>' if hatali
                else '<div class="t-display num">1.500</div>')
    hata_satiri = (h(8) + '<div class="t-cap c-danger">Tutar boş kalamaz.</div>') if hatali else ""
    kaydet = ('<button class="btn-primary pasif" disabled aria-disabled="true" '
              'aria-label="Kaydet"><div class="tek-satir">Kaydet</div></button>' if hatali else
              '<button class="btn-primary" aria-label="Kaydet">'
              '<div class="tek-satir">Kaydet</div></button>')
    # H2 — ghost'un yatay iç boşluğu tokens §7.1 gereği **istisnasız 16**;
    # sınıf varsayılanı 24 olduğu için her ghost bu override'ı taşır (ALT_BILGI
    # ve K2 ile aynı kural). Bu düğme override'ı almamıştı.
    sil = (h(8) + '<button class="btn-ghost" style="padding:0 16px" '
                  'aria-label="Bu hareketi sil">'
                  '<div class="tek-satir">Sil</div></button>') if duzenleme else ""
    baslik = "Hareketi düzenle" if duzenleme else "Birikim hareketi"
    klavye_html = KLAVYE if klavye else ""
    return f'''<div class="sheet">
<div class="satir orta" style="justify-content:center"><div class="sheet-tutamac"></div></div>
{h(12)}
<div class="aralik"><div class="t-h2 esnek">{baslik}</div>{w(12)}
{ikon_btn("x", "Kapat")}</div>
{h(12)}
<div class="segment"><button class="segment-btn secili" aria-label="Birikime ekledim"
aria-pressed="true">Ekledim</button><button class="segment-btn" aria-label="Birikimden çektim"
aria-pressed="false">Çektim</button></div>
{h(12)}
<div class="t-label">Tutar</div>
{h(8)}
<div class="{giris_sinif}">{tutar_ic}{w(4)}<div class="t-amount c-2">₺</div>
{"" if hatali else w(8) + '<div class="imlec"></div>'}<div class="esnek"></div></div>
{hata_satiri}
{h(12)}
<div class="t-label">Tarih</div>
{h(8)}
<button class="kuyu-btn" aria-label="Tarihi değiştir. 23 Eylül 2026">
<div class="t-body esnek tek-satir">23 Eylül 2026</div>{w(12)}{ikon("calendar")}</button>
{h(12)}
<div class="t-label">Not</div>
{h(8)}
<div class="giris"><div class="t-body c-2 esnek tek-satir">İsteğe bağlı</div></div>
{h(12)}
{kaydet}{sil}
{h(8)}
</div>
{klavye_html}'''


def sheet_ekrani(hatali: bool, klavye: bool, duzenleme: bool = False) -> str:
    arka = (ekran_basi("Eylül 2026 · ay devam ediyor", "Tasarruf")
            + hero_kart(cip("Bütçe 24.000 ₺", "Bütçe 24.000 ₺. Bütçeyi aç", chevron=True),
                        gosterge_dolu("6.240", "bu ay biriken", 0.26),
                        '<div class="t-body" style="text-align:center">Kaydettiğin gelir ve '
                        'harcamalara göre 22 gün hesaplandı.</div>')
            + h(8)
            # Sheet, "Gerçek birikim" bölümü AÇIKKEN açılır (eylem orada);
            # arkada o bölümün üst bloğu görünür kalır.
            + akordiyon("Gerçek birikim", OZET["birikim"], birikim_icerik(
                "9.500 ₺", "Bu ay 4.600 ₺ eklendi", 95.0, "10.000 ₺",
                motivasyon="Bu tutarı birikim hedefin için ayırmayı düşünebilirsin.")))
    return ('<main class="content"><div class="katman">'
            f'<div class="kaydir">{arka}{h(24)}</div>{sekme_cubugu("tasarruf")}'
            f'<div class="katman-ust"><div class="scrim-kat"></div>'
            f'{sheet(hatali, klavye, duzenleme)}</div>'
            "</div></main>")


F6 = sheet_ekrani(False, klavye=False)
F7 = sheet_ekrani(True, klavye=True)
F7B = sheet_ekrani(False, klavye=False, duzenleme=True)

# ===========================================================================
# F8..F11 — Profil
# ===========================================================================
AYARLAR = [
    ("Planın", [
        ("banknote", "Maaş ve bütçe", "Aylık net gelir 24.000 ₺ · 5 sabit gider"),
        ("limitler", "Limitler", "Günlük 300 ₺ · 4 kategori limiti"),
        ("repeat", "Rutinler", "3 rutin · bu ay 1.240 ₺ tasarruf"),
    ]),
    ("Kayıt kolaylıkları", [
        ("notebook", "Favoriler", "14 ürün, son fiyatlarıyla"),
        ("calendar-clock", "Taksitler", "2 seri · bu ay 1.350 ₺"),
    ]),
    ("Takip", [
        ("chart", "Aylık özet", "Kategori payları ve haftalık ritim"),
        ("trending-up", "Seri", "12 gün · en uzun 21 gün"),
    ]),
    ("Uygulama", [
        ("ayarlar", "Tüm ayarlar", "Hesap, bildirim, gün sınırı, yasal"),
        ("info", "Yardım", "Sık sorulan sorular"),
    ]),
]


def kimlik_paneli(ic: str, etiket: str = "") -> str:
    """Ö7 — Profil'in aksanı burada. Kart (`surface` · radius 24 · raised)
    değil **kahraman panel**: zemin `primary-soft`, radius 32,
    `clay.raised-lg` — E-27'nin kahraman kartıyla aynı yüzey dili. Yeni
    token yok; `.hero-kart` sınıfı v4'ten birebir.

    Üç derinlik bu panelde tamamlanıyor: panel `raised-lg` · içindeki 48pt
    `.secim-ikon` kabı `sunken` · altındaki ayar satırları `raised`.
    Ekranın ilk katındaki `primary-soft` yüzey ölçümü §8/2'de yazılı."""
    if etiket:
        return (f'<div class="pad"><button class="hero-kart kart-ic satir" '
                f'style="width:100%;border:0;text-align:left" aria-label="{etiket}">'
                f'{ic}</button></div>')
    return f'<div class="pad"><div class="hero-kart kart-ic">{ic}</div></div>'


def olgu_serit(olgu: str, baglam: str) -> str:
    """Ö7 TAKVİYESİ — kimlik panelinin içindeki `clay.sunken` olgu şeridi.

    Yeni bileşen değil: §3.3'ün `InfoStrip` geometrisi (`.serit` — iç boşluk
    12/16, radius 16, `clay.sunken`) + v4'ün `.clay-kuyu` zemini (`well`).
    `serit-info` burada kullanılamaz: zemini `primary-soft`tur, yani panelin
    kendi zeminiyle aynı olur ve şerit kaybolur. `well` seçildi, `groove`
    seçilmedi — `groove` bu sistemde **basılı** yüzeyin zeminidir, statik bir
    şeride verilince "bu şerit basılı" yalanını söyler. Yeni token / renk /
    radius / ikon YOK.

    Rol disiplini (PM kısıtı): olgu satırı `label`, bağlam satırı `caption`.
    Profil'in kahraman sayısı yoktur (§8/1) ve Tasarruf'un tek kahramanı
    bozulmaz. Veri ekranda zaten var: aynı sayılar `Seri` ayar satırında.
    İkon `trending-up` — Seri satırının glifinin aynısı; tekrar kasıtlı,
    şerit ile o satırı bağlıyor (yeni glif açmak yerine).
    """
    return (f'<div class="serit clay-kuyu" style="width:100%">'
            f'<div class="ikon-kutu c-primary">{ikon("trending-up")}</div>{w(12)}'
            f'<div class="esnek kolon"><div class="t-label">{olgu}</div>{h(4)}'
            f'<div class="t-cap">{baglam}</div></div></div>')


def ayar_satir(ik: str, baslik: str, aciklama: str, basili: bool = False) -> str:
    b = " basili" if basili else ""
    return (f'<button class="ayar-satir{b}" aria-label="{baslik}. {aciklama}">'
            f'<div class="kat-kab notr">{ikon(ik)}</div>{w(12)}'
            f'<div class="esnek kolon"><div class="t-strong tek-satir">{baslik}</div>{h(4)}'
            f'<div class="t-cap tek-satir">{aciklama}</div></div>{w(12)}'
            f'<div class="ikon-kutu c-2">{ikon("chevron-right")}</div></button>')


def ayar_gruplari(basili_ilk: bool = False) -> str:
    parca = []
    for i, (baslik, satirlar) in enumerate(AYARLAR):
        parca.append(bolum(baslik))
        parca.append(h(8))
        govde = []
        for j, (ik, ad, ac) in enumerate(satirlar):
            govde.append(ayar_satir(ik, ad, ac, basili=(basili_ilk and i == 0 and j == 1)))
        parca.append('<div class="pad kolon">' + f'{h(8)}'.join(govde) + "</div>")
        if i < len(AYARLAR) - 1:
            parca.append(h(24))
    return "".join(parca)


ALT_BILGI = ('<div class="pad kolon orta">'
             '<div class="t-micro">Trinkow · sürüm 1.0.0</div>' + h(8) +
             '<div class="satir">'
             '<button class="btn-ghost" style="height:44px;padding:0 16px" '
             'aria-label="Kullanım şartlarını aç"><div class="t-micro c-primary">Kullanım '
             'şartları</div></button>'
             '<div class="t-micro c-2">·</div>'
             '<button class="btn-ghost" style="height:44px;padding:0 16px" '
             'aria-label="Gizlilik metnini aç"><div class="t-micro c-primary">Gizlilik</div>'
             '</button></div></div>')

PROFIL_BASI = ekran_basi(
    "Hesabın ve planın", "Profil",
    w(8) + f'<button class="ikon-btn" aria-label="Ayarları aç">{ikon("ayarlar")}</button>')

F8 = ekran(
    PROFIL_BASI
    + kimlik_paneli(
        # Ö7 takviyesi: kimlik satırı + olgu şeridi. Panel 80 -> 156pt.
        '<div class="kolon" style="width:100%">'
        '<div class="satir" style="width:100%">'
        f'<div class="secim-ikon">{ikon("user")}</div>{w(12)}'
        '<div class="esnek kolon"><div class="t-strong tek-satir">'
        'mustafa.teker.1988@uzunsirketalanadi.com.tr</div>' + h(4) +
        '<div class="t-cap tek-satir">Google ile oturum açıldı</div></div>' + w(12) +
        f'<div class="ikon-kutu c-2">{ikon("chevron-right")}</div></div>' + h(12) +
        olgu_serit("12 gündür kayıt giriyorsun", "En uzun 21 gün.") +
        '</div>',
        "Hesabını aç. mustafa.teker.1988@uzunsirketalanadi.com.tr, "
        "Google ile oturum açıldı. 12 gündür kayıt giriyorsun, en uzun 21 gün")
    + h(24)
    + ayar_gruplari(basili_ilk=True)
    + h(24)
    + ALT_BILGI
    , "profil")

F9 = ekran(
    PROFIL_BASI
    + kimlik_paneli(
        f'<div class="kolon" style="width:100%"><div class="satir">'
        f'<div class="secim-ikon">{ikon("user")}</div>{w(12)}'
        '<div class="esnek kolon"><div class="t-strong">Hesapsız kullanıyorsun</div>' + h(4) +
        '<div class="t-cap">Harcamaların telefonunda kalır.</div></div></div>' + h(12) +
        '<button class="btn-secondary" aria-label="Oturum aç">'
        '<div class="tek-satir">Oturum aç</div></button></div>')
    + h(24)
    + ayar_gruplari()
    + h(24)
    + ALT_BILGI
    , "profil")

F10 = ekran(
    PROFIL_BASI
    + kimlik_paneli(
        f'<div class="kolon" style="width:100%"><div class="satir-ust">'
        f'<div class="secim-ikon">{ikon("wifi-off")}</div>{w(12)}'
        '<div class="esnek kolon"><div class="t-strong">Hesap bilgisi açılamadı</div>' + h(4) +
        '<div class="t-cap">Ayarların ve yasal metinler açık kalır.</div></div></div>' + h(12) +
        '<button class="btn-secondary" aria-label="Yeniden dene">' + ikon("repeat") + w(8) +
        '<div class="tek-satir">Yeniden dene</div></button></div>')
    + h(24)
    + ayar_gruplari()
    + h(24)
    + ALT_BILGI
    , "profil")

F11 = ekran(
    PROFIL_BASI
    + kimlik_paneli(
        # Panel yüklenmiş düzenle AYNI yüzeydir (yükleme bitince zıplamaz);
        # iskelet bloklarını `primary-soft` üstünde renk değil `clay.sunken`
        # çukurluğu ayırır — F4'teki kahraman kart iskeletiyle aynı dil.
        # Ö7 takviyesi: panel yüklü hâliyle aynı 156pt yüksekliği korur —
        # şeridin yerinde tek parça çukur blok durur (şeridin kendisi de
        # çukur olduğu için içine ikinci kat çukur çubuk konmadı).
        f'<div class="kolon" style="width:100%">'
        f'<div class="satir" style="width:100%"><div class="iskelet" '
        f'style="width:48px;height:48px;border-radius:16px"></div>{w(12)}'
        f'<div class="esnek kolon">{iskelet("208px", 16)}{h(4)}'
        f'{iskelet("136px", 13)}</div></div>{h(12)}'
        f'<div class="iskelet" style="width:100%;height:64px;'
        f'border-radius:16px"></div></div>')
    + h(24)
    + "".join(
        bolum(baslik) + h(8) + '<div class="pad kolon">' + f'{h(8)}'.join(
            f'<div class="ayar-satir"><div class="iskelet" style="width:44px;height:44px;'
            f'border-radius:16px"></div>{w(12)}<div class="esnek kolon">{iskelet("120px", 16)}'
            f'{h(4)}{iskelet("176px", 13)}</div></div>' for _ in satirlar) + "</div>" +
        (h(24) if i < len(AYARLAR) - 1 else "")
        for i, (baslik, satirlar) in enumerate(AYARLAR))
    , "profil")

# ===========================================================================
BIRIMLER = [
    cihaz("E-27 TASARRUF", "dolu ay · akordiyon (ilk bölüm açık)",
          F1,
          "<b>REV3:</b> kahramanın altındaki altı kart <b>dört akordiyon bölümüne</b> indi "
          "ve yalnız <b>ilk bölüm açık</b> geliyor: kahraman sayının “nereden çıktığı”. "
          "Kapalı bölümler boş başlık değil — her biri sağında <b>özet değer</b> taşıyor. "
          "<b>İlk kat ölçümü (REV3-r1):</b> kaydırma alanı 844 − 47 durum çubuğu − 28 ana "
          "çubuk − 76 <b>yüzen sekme çubuğu</b> = <b>693</b> (çubuk kaydırma alanının "
          "dışındadır). Yığın: başlık 74 + kahraman 368 + 8 + açık bölüm 238 = <b>688</b>, "
          "yani A <b>bütün olarak</b> ilk kata giriyor ve kesme A ile B arasındaki 8pt "
          "boşluğa düşüyor — hiçbir kart, satır ya da tutar kesilmiyor (K-057/8). "
          "B · C · D ilk katta <b>görünmez</b>; özetleri kapalı hâlde değer taşıdığı için "
          "kaydırma sonrası tek bakışta okunurlar. <b>Kahraman:</b> bu ay biriken; "
          "4+ haneli tutar tokens §7.5 gereği <b>display 32</b>'ye iner (56pt'de tabular "
          "189px, yayın iç alanı 156px). Motivasyon şeridi ekranın ortasından çıktı, "
          "eylemiyle aynı bölüme (B) girdi."),
    cihaz("E-27 TASARRUF", "kapanmış ay · bütçe dışı · eksik gelir günü",
          F2,
          "Dolgu bu ekranda <b>biriken</b> demektir; bütçe dışı ayda biriken 0'dır → "
          "ana yay ve topuz <b>çizilmez</b>, oluk boş kalır ve taşma yayı "
          "(<b>grad.arc-over</b>, r 102) tek başına konuşur. Kahraman sayı "
          "<b>warning-ink</b>, etiketi birebir “bütçe dışı”. Kırmızı ve ünlem yok. "
          "Geçmiş ay seçiliyken metinler ay adıyla yazılır: “Ayın bütçesi”, "
          "“Ağustos'ta kayıt yok” — kapalı bölümlerin <b>özetleri de</b> ay adını taşır. "
          "Eksik gelir şeridi artık ekranın ortasında değil, etkilediği <b>bölümün "
          "içinde</b>: hangi sayının eksik olduğu belirsiz kalmıyor."),
    cihaz("E-27 TASARRUF", "ilk ay · gelir yok (HeroPlain)",
          F3,
          "Gelir olmadan pay hesaplanamaz: yay çizilmez, 176pt çukur disk + tek birincil "
          "eylem. Açık bölümde <b>uydurma denklem yok</b> (“0 − 0 = 0” kurulmaz): takip "
          "başlangıcı şeridi + tek satır olgu. Dört özetin dördü de <b>veri yokken bile "
          "dolu</b>: “Gelir eksik” · “0 ₺ · hedef 10.000 ₺” · “Harcama yok” · “Rutin "
          "eklemedin”."),
    cihaz("E-27 TASARRUF", "yükleniyor · iskelet",
          F4,
          "Gerçek düzen yerinde durur, içler çukur bloklara döner. Shimmer ve tam ekran "
          "spinner yok; gösterge oluğu çizilir, dolgu ve topuz çizilmez. Akordiyonda "
          "<b>başlıklar gerçek</b> (metin ilk karede hazırdır), yalnız özet değerlerin "
          "yeri korunur — yükleme bitince başlık satırı zıplamaz. Kahraman kartın alt "
          "bloğu da <b>iki satır yer tutuyor</b> (“Hesaplanıyor” + bir çukur satır), yani "
          "iskelet kahraman yüklü kahramanla <b>aynı 368pt</b>: veri gelince akordiyon "
          "grubu 26px yukarı zıplamaz. Ekran okuyucu etiketi “{başlık}. Yükleniyor”."),
    cihaz("E-27 TASARRUF", "hata · ay gezinmesi çalışır",
          F5,
          "Hata kahraman kartın yerine geçer; <b>ay okları</b> kendi satırında kalır ki "
          "kullanıcı başka aya geçip veriyi görebilsin. Teknik hata kodu yok. "
          "Tüm ekran hatasında akordiyon <b>çizilmez</b>: hiçbir bölümün özet değeri "
          "yoktur, kapalı başlıklar boş kalırdı."),
    cihaz("E-27 TASARRUF", "“Gerçek birikim” bölümü açık",
          F12,
          "REV3'te <b>Gerçek birikim</b> ve <b>Birikim hareketleri</b> tek bölüm: biri "
          "değer, öteki kanıt. Sıra: tutar → hedef çubuğu → motivasyon şeridi → tek "
          "<b>secondary</b> eylem → son 5 hareket → ghost “Tüm hareketler”. Kap kabarık "
          "olduğu için hareket satırları bir basamak <b>iniyor</b> (well + clay.sunken) ve "
          "içlerindeki gün kutusu bir basamak çıkıyor — aynı yükseklik iç içe iki kez "
          "söylenmiyor (§9/3). Tutar hâlâ <b>amount 17</b>: ekranın tek kahraman sayısı "
          "göstergededir. Üstteki <b>Bu ayın bütçesi</b> başlığı <b>basılı</b>: kullanıcı "
          "B açıkken A'yı da açıyor — bir bölümü açmak başkasını kapatmıyor."),
    cihaz("E-27 TASARRUF", "iki bölüm birlikte açık · başlık basılı (kaydırılmış)",
          F13,
          "Ekran <b>kaydırılmış</b>: başlık ve kahraman kart yukarıda kaldı, kesme bir "
          "kart sınırından geçiyor. Akordiyon <b>tek-açık değil</b>: bir bölümü açmak başkasını kapatmaz, çünkü "
          "kapanma kaydırma konumunu kullanıcının altından çeker. <b>Açık</b> “Kategori "
          "dağılımı” bölümünün başlığı <b>basılı</b> durumda: hedef başlık satırı, geri "
          "bildirim <b>kabın tamamı</b> (çöker, küçülmez; ok dönmüş hâlde kalır). Kapalı "
          "hâlin basılı karşılığı bir önceki çerçevededir. <b>Rutin tasarrufu</b> ekrandan kalkmadı, en dar hâline "
          "indi: tutar + tek cümle + üç satır; `repeat` ikon kabı düştü (üç satırın üçü de "
          "rutin, glif hiçbir şeyi ayırmıyordu)."),
    cihaz("E-27 TASARRUF", "kısmi hata + veri olmayan açık bölüm (kaydırılmış)",
          F14,
          "Ekran <b>kaydırılmış</b> (başlık ve kahraman yukarıda). İki okuma var (ay özeti · birikim kayıtları); biri düşerse <b>yalnız o bölüm</b> "
          "hata durumuna geçer ve <b>açık</b> gelir: içinde tek satır şerit + “Yeniden dene” "
          "durur. <b>Ö4:</b> “Açılamadı” özeti kullanıcı o bölümü <b>kapattığında</b> "
          "başlığın sağında görünür — hata hâli, “açıkken özet çizilmez” kuralının ikinci "
          "istisnası değildir; kapalı hâl özetini korur. Ekranın kalanı okunur kalır. Açık ama <b>verisi olmayan</b> "
          "bölüm (Kategori dağılımı) illüstrasyonsuz bölüm boşluğu kullanır: 176pt disk bir "
          "bölüm kabının içine girince açılan bölümü ikinci bir kahramana çevirirdi."),
    cihaz("E-27 · SHEET", "birikim hareketi · açılış",
          F6,
          "Form sayfadan çıkıp bottom sheet'e taşındı. Yön seçimi iki yarışan düğme değil "
          "tek <b>segment</b>. Sheet ekranı kaplamaz: arkadaki kahraman kart görünür kalır."),
    cihaz("E-27 · SHEET", "alan hatası · klavye açık",
          F7,
          "Tutar boşken 2pt <b>danger</b> kenarlık + tek satır hata + Kaydet pasif (opaklık "
          "yok, zemin <b>disabled-bg</b>). Klavye açıkken Kaydet görünür kalır."),
    cihaz("E-27 · SHEET", "düzenleme kipi · silme keşfedilebilir",
          F7B,
          "Hareket satırına dokunmak aynı sheet'i <b>düzenleme kipinde</b> açar: başlık "
          "“Hareketi düzenle”, Kaydet'in altında <b>ghost “Sil”</b>. Kaydırma (sağdan "
          "sola) kısayol olarak kalır ama silmenin tek yolu değildir."),
    cihaz("E-28 PROFİL", "oturum açık · uzun e-posta",
          F8,
          "Kimlik kartı <b>kahraman panel</b>: `primary-soft` · radius 32 · "
          "<b>clay.raised-lg</b> — ekranın aksanı ve üç derinliğin tamamı burada "
          "(panel raised-lg · ikon kabı sunken · ayar satırları raised). Düz ikincil "
          "düğme listesi bitti: her satır kendi kabarık yüzeyi, 44pt nötr ikon kabı ve "
          "<b>gerçek değeri</b> taşır. İkinci satır <b>basılı</b> durumda. E-posta tek "
          "satır, sonu kırpılır. <b>Ö7 takviyesi:</b> e-postanın altında tek bir "
          "<b>clay.sunken olgu şeridi</b> (well + inset) — içeriği ekranda zaten olan "
          "seri değeri, rolleri label/caption; kahraman sayı üretilmedi. Panel 80 → "
          "<b>156pt</b>, ilk kattaki primary-soft yüzey %14,2 → <b>%23,5</b>."),
    cihaz("E-28 PROFİL", "hesapsız",
          F9,
          "Hesap hiçbir özelliği kilitlemez; bu panel uygulamanın tek hesap davetidir. "
          "Olgu şeridi burada <b>çizilmez</b>: davetin altına ikinci bir mesaj konsa "
          "tek davet ikiye bölünürdü; şeridin yerini secondary düğme alır (panel 144pt, "
          "oturum açık hâlin 156'sına yakın — durum değişince düzen zıplamaz). "
          "Ayar grupları aynen çalışır."),
    cihaz("E-28 PROFİL", "hesap bilgisi hatası",
          F10,
          "Yalnız kimlik paneli hata durumuna geçer. Ayarlar ve yasal bağlantılar "
          "erişilebilir kalır — ağ hatası ekranı kilitlemez. Olgu şeridi burada da "
          "çizilmez: panelin işi hata + yeniden dene; şeridin yerini o blok alır."),
    cihaz("E-28 PROFİL", "yükleniyor · iskelet",
          F11,
          "Satır sayısı ve sütun genişlikleri gerçek içeriğe yakın; yükleme bittiğinde "
          "düzen zıplamaz. Panel 156pt'yi korur: olgu şeridinin yerinde tek parça "
          "çukur blok (326×64, radius 16) durur — şerit zaten çukur olduğu için içine "
          "ikinci kat çukur çubuk konmadı."),
]

GIRIS = ('E-27 Tasarruf (<b>REV3 akordiyon</b>) · E-28 Profil · 390×844 · claymorphism '
         '(tokens.md v4) · alt çubuk Günlük / Tasarruf / Profil, FAB yok · '
         'spesifikasyon: <a href="../rev2-tasarruf-profil.md">rev2-tasarruf-profil.md</a>')

(KOK / "tasarruf-profil.html").write_text(
    sayfa("Trinkow rev2 — Tasarruf ve Profil", GIRIS, BIRIMLER), encoding="utf-8")
print("yazıldı:", (KOK / "tasarruf-profil.html").relative_to(KOK.parent))
