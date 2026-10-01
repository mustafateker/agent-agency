# -*- coding: utf-8 -*-
"""E-18 Taksitler — **kategori → ürün kırılımı** (REV3-r1 · 390×844, 9 durum).

Spesifikasyon: ../rev3-taksitler.md
Çalıştır    :  python3 _uret/uret_taksitler.py
Çıktı       :  ../taksitler.html

Mustafa'nın direktifi: "toplam da görünsün, aldığım ürün bazlı da takip
edebileyim". Ekran bu yüzden ÜÇ düzeye ayrıldı ve sıra DEĞİŞTİ:
  1) Bu ay toplamı (kahraman kart — v4'ten aynen)
  2) Süren taksitler → kategori akordiyonu → ürün satırı  (YENİ)
  3) Önümüzdeki aylar yük haritası (v4'ten aynen, bir blok AŞAĞI indi)

Yeni renk / punto / radius / boşluk / gölge / ikon YOK. Akordiyon deseni
Tasarruf'tan (`stil-rev2.css` §9-§10, `rev2-tasarruf-profil.md` §3.12)
yeniden kullanıldı; `stil-rev2.css`'e §13 bloğu EKLENMEDİ çünkü gerekmedi.

SAYI MODELİ (r1): ekrandaki her tutar `rev3-taksitler.md` §5.3'teki kuruş
tablosundan türetildi. İki bağlayıcı kural:
  * gösterimde kuruş **atılır** (aşağı yuvarlama, `// 100`) — tokens §14.2/6
    `gunluk_limit_kurus` ile aynı yön;
  * yuvarlama **yapraklarda** yapılır, üst düzeyler **görünen** değerleri
    toplar: kategori = Σ satır, ay toplamı = Σ kategori.
Bu yüzden Telefon serisinin aylığı 1.041,72 ₺'dir (toplam 12.500,64) —
o sayı hem 1.041 ₺ satırını hem 17.693 / 14.832 ₺ kalan toplamlarını
aynı anda tutan tek modeldir.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import cihaz, ikon, sayfa  # noqa: E402

KOK = pathlib.Path(__file__).parent.parent


def h(n: int) -> str:
    return f'<div class="h{n}"></div>'


def w(n: int) -> str:
    return f'<div class="w{n}"></div>'


def iskelet(gen: str, yuk: int, radius: int = 999) -> str:
    return f'<div class="iskelet" style="width:{gen};height:{yuk}px;border-radius:{radius}px"></div>'


# ---------------------------------------------------------------------------
# Kabuk: push ekranı — sekme çubuğu YOK (E-18 Profil'den itilir).
# Kaydırma alanı: 844 − 47 (durum çubuğu) − 28 (ana çubuk) = **769**.
# ---------------------------------------------------------------------------
def basi() -> str:
    return ('<div class="ekran-basi">'
            f'<button class="ikon-btn" aria-label="Geri dön">{ikon("chevron-left")}</button>'
            '<div class="esnek satir" style="justify-content:center">'
            '<div class="t-h1 tek-satir">Taksitler</div></div>'
            '<div style="width:44px;height:44px"></div></div>')


def ekran(icerik: str) -> str:
    return f'<main class="content"><div class="kaydir">{basi()}{icerik}{h(24)}</div></main>'


# ---------------------------------------------------------------------------
# 1) Kahraman kart — "Bu ay" toplamı. v4'ten BİREBİR (bilgi kaybı yok).
# ---------------------------------------------------------------------------
def hero(tutar: str) -> str:
    return ('<div class="pad"><div class="clay-lg kart-ic">'
            '<div class="t-label c-2">Bu ay</div>' + h(4) +
            '<div class="satir" style="align-items:baseline">'
            f'<div class="t-display num">{tutar}</div>{w(8)}'
            '<div class="t-amount c-2">₺</div></div>' + h(12) +
            '<div class="t-cap">Taksitler girildiği güne değil, ait olduğu aya '
            'yazılır.</div></div></div>')


# ---------------------------------------------------------------------------
# 2) Bölüm başlığı + kategori akordiyonu + ürün satırı
# ---------------------------------------------------------------------------
def bolum_basi(sag: str, ik: str = "", aile: str = "", ad: str = "Süren taksitler") -> str:
    """Bölüm başlığı — iki düzen, TEK yapı. Sağdaki özet DAİMA "ürün" sayar.

    ÇOK kategori: `h2` "Süren taksitler" + sağda "3 kategori · 6 ürün".
    TEK kategori (K-T2): akordiyon kurulmadığı için akordiyon başlığının
    **yapısı** buraya taşınır → `.kat-kab` + `h2` **kategori adı** + sağda
    "{adet} ürün". Jenerik "Süren taksitler" başlığı bu düzende **düşer**:
    K-T2 başlığın işini kategoriye devrediyor, ikisi birlikte durursa
    44pt ikon kabı kategori adına değil ilgisiz bir başlığa komşu olur ve
    aynı bileşen (kab + h2 + sağ özet) tek ekranda iki anlam taşır.

    Ayrım: burada `chevron-down` **yok** — bu başlık açılıp kapanmaz.
    Aynı gerekçeyle kategori **tutarı** da yazılmaz: tek kategoride
    kategori toplamı kahraman sayının kendisidir (r2)."""
    kab = (f'<div class="kat-kab kat-{aile}" style="flex:0 0 auto">{ikon(ik)}</div>'
           + w(12)) if ik else ""
    return ('<div class="pad aralik">' + kab +
            f'<div class="t-h2 esnek tek-satir">{ad}</div>' + w(12) +
            f'<div class="t-label c-2 num tek-satir" style="flex:0 0 auto">{sag}</div></div>')


def urun_ici(ad: str, tutar: str, no: int, toplam: int, kalan: str, aile: str,
             son: bool = False) -> str:
    """Satırın orta kolonu — üç yatay blok, hepsi 4pt aralıklı (aynı nesne).

    BİRİNCİL: ürün adı + bu ayki tutar (üst satır).
    İKİNCİL : ilerleme çubuğu + "{no}/{toplam} · kalan {tutar}".
    Son taksitte "kalan" satırı yerine olgu yazılır: kalan 0 ₺ demek
    bilgi değil, gürültüdür.
    """
    oran = round(no * 100 / toplam)
    alt = ('<div class="t-label c-primary tek-satir">Son taksit bu ay</div>' if son else
           f'<div class="t-cap num tek-satir">{no}/{toplam} · kalan {kalan}</div>')
    return ('<div class="esnek kolon">'
            '<div class="aralik">'
            f'<div class="t-strong esnek tek-satir">{ad}</div>{w(12)}'
            f'<div class="t-amount num" style="flex:0 0 auto">{tutar}</div></div>'
            + h(4) +
            f'<div class="cubuk-oluk"><div class="cubuk-dolgu" style="width:{oran}%;'
            f'background-color:var(--cat-{aile})"></div></div>'
            + h(4) + alt + '</div>')


def a11y(ad: str, tutar: str, no: int, toplam: int, kalan: str, son: bool) -> str:
    if son:
        return f"{ad}. Bu ay {tutar}. Son taksit. Ayrıntıyı aç"
    return (f"{ad}. Bu ay {tutar}. {no}. taksit, {toplam} taksitten. "
            f"Kalan {kalan}. Ayrıntıyı aç")


def urun_satiri(ad: str, tutar: str, no: int, toplam: int, kalan: str, aile: str,
                son: bool = False, basili: bool = False, kuyu: bool = True) -> str:
    """Ürün satırı — iki hâli var, farkı YALNIZ yüzey basamağı:
      * `kuyu=True`  akordiyonun İÇİNDE → `well` + `clay.sunken` (§10)
      * `kuyu=False` akordiyon kurulmadığında (tek kategori) → kabarık

    Sağda 20pt `chevron-right`: satır artık ilerleme çubuğu + iki sayı
    taşıyan bir veri bloğu gibi okunuyor, dokunulabilir olduğunu söyleyen
    bir işaret gerekiyor. Ok 12 + 20 = 32pt'yi **esneyen ad** sütunundan
    alır; tutar `flex:0 0 auto` olduğu için hiç kırpılmaz."""
    sinif = "satir-kart kuyu" if kuyu else "satir-kart"
    b = " basili" if basili else ""
    return (f'<div class="{sinif}{b}" role="button" '
            f'aria-label="{a11y(ad, tutar, no, toplam, kalan, son)}">'
            + urun_ici(ad, tutar, no, toplam, kalan, aile, son) + w(12)
            + '<div class="ikon-kutu" style="flex:0 0 auto;color:var(--text-2)">'
            + ikon("chevron-right") + '</div></div>')


def tumunu_goster(adet: int, basili: bool = False) -> str:
    """Tek yönlü açma — iç içe akordiyon DEĞİL (§3.12.3 yasağı). Basıldığında
    kalan satırlar eklenir ve düğme düşer; hiçbir içerik geri katlanmaz."""
    b = " basili" if basili else ""
    return (f'<button class="btn-ghost{b}" style="padding:0 16px;width:100%" '
            f'aria-label="{adet} ürünün tamamını göster">'
            '<div class="tek-satir">Tümünü göster</div></button>')


def akordiyon(ad: str, ik: str, aile: str, ozet: str, satirlar: list[str] | None = None,
              basili: bool = False, iskelet_ozet: bool = False) -> str:
    """Kategori bölümü — Tasarruf'la AYNI bileşen (`.akordiyon`).
    Kapalı hâl asla boş başlık değildir: sağda "{tutar} · {n} ürün" durur.
    Açıkken özet çizilmez (§3.12.4) — aynı tutar iki santim arayla iki kez
    yazılmaz; kategorinin toplamı satırların toplamıdır."""
    acik = bool(satirlar)
    if iskelet_ozet:
        sag = f'<div style="flex:0 0 auto">{iskelet("104px", 18)}</div>' + w(12)
    elif acik:
        sag = ""
    else:
        sag = (f'<div class="t-label c-2 num tek-satir" style="flex:0 0 auto">{ozet}</div>'
               + w(12))
    bas = (f'<button class="akordiyon-bas" aria-expanded="{"true" if acik else "false"}" '
           f'aria-label="{ad}. {ozet}">'
           f'<div class="kat-kab kat-{aile}" style="flex:0 0 auto">{ikon(ik)}</div>{w(12)}'
           f'<div class="t-h2 esnek tek-satir">{ad}</div>{w(12)}{sag}'
           f'{ikon("chevron-down", "cev-acik" if acik else "")}</button>')
    govde = (h(12) + f'{h(12)}'.join(satirlar)) if acik else ""
    b = " basili" if basili else ""
    return f'<div class="pad"><div class="akordiyon{b}">{bas}{govde}</div></div>'


# ---------------------------------------------------------------------------
# 3) Önümüzdeki aylar — v4'ten BİREBİR (yalnız konumu bir blok aşağı indi)
#    Çubuk oranı = round(ay / EN BÜYÜK ay × 100). Tek seri baskın olduğunda
#    (T4) çubuklar düzleşir; ayrımı sağdaki sayı taşır, çubuk taşımaz.
# ---------------------------------------------------------------------------
def ay_satiri(ay: str, tutar: str, oran: int, simdi: bool = False) -> str:
    c = "" if simdi else " c-2"
    return ('<div class="satir">'
            f'<div class="t-label{c}" style="width:56px;flex:0 0 auto">{ay}</div>{w(12)}'
            f'<div class="yuk-oluk"><div class="yuk-dolgu" style="width:{oran}%"></div></div>'
            f'{w(12)}<div class="t-amount num" style="width:88px;flex:0 0 auto;'
            f'text-align:right">{tutar}</div></div>')


def ay_karti(aylar: list[tuple[str, str, int]], dip: str) -> str:
    ic = f'{h(8)}'.join(ay_satiri(a, t, o, i == 0) for i, (a, t, o) in enumerate(aylar))
    return ('<div class="pad"><div class="clay kart-ic">'
            '<div class="t-h2">Önümüzdeki aylar</div>' + h(8) + ic + h(12) +
            f'<div class="t-cap num">{dip}</div></div></div>')


# Eylül 2026 referansı. Modeli: spec §5.3 tablo A (6 seri).
AYLAR = [("Eylül", "3.120 ₺", 100), ("Ekim", "2.861 ₺", 92), ("Kasım", "2.861 ₺", 92),
         ("Aralık", "2.601 ₺", 83), ("Ocak", "2.601 ₺", 83), ("Şubat", "2.081 ₺", 67)]
DIP = "Kalan toplam 17.693 ₺. Sonuncusu Mayıs 2027 tarihinde bitiyor."

# Ekim 2026 referansı — süpürge (259 ₺) Eylül'de bitti, 5 seri kaldı.
# Kalan toplam = 17.693,76 − Ekim (2.861,72) = 14.832,04 → 14.832 ₺.
AYLAR_DUSMUS = [("Ekim", "2.861 ₺", 100), ("Kasım", "2.861 ₺", 100),
                ("Aralık", "2.601 ₺", 91), ("Ocak", "2.601 ₺", 91),
                ("Şubat", "2.081 ₺", 73), ("Mart", "2.081 ₺", 73)]
DIP_DUSMUS = "Kalan toplam 14.832 ₺. Sonuncusu Mayıs 2027 tarihinde bitiyor."


# ---------------------------------------------------------------------------
# Üç kategori · altı ürün — T1/T2'nin ortak verisi (spec §5.3 tablo A)
# 1.041 + 520 + 259 = 1.820 · 1.820 + 780 + 520 = 3.120
# ---------------------------------------------------------------------------
def uc_kategori(satir_basili: int = -1, kategori_basili: bool = False) -> str:
    satirlar = [
        urun_satiri("Telefon", "1.041 ₺", 4, 12, "8.333 ₺", "duman",
                    basili=satir_basili == 0),
        urun_satiri("Buzdolabı", "520 ₺", 5, 9, "2.080 ₺", "duman",
                    basili=satir_basili == 1),
        urun_satiri("Elektrikli süpürge", "259 ₺", 6, 6, "0 ₺", "duman", son=True,
                    basili=satir_basili == 2),
    ]
    return (hero("3.120")
            + h(24) + bolum_basi("3 kategori · 6 ürün") + h(8)
            + akordiyon("Diğer", "circle-dashed", "duman", "1.820 ₺ · 3 ürün", satirlar)
            + h(8) + akordiyon("Giyim", "shirt", "kiremit", "780 ₺ · 2 ürün",
                               basili=kategori_basili)
            + h(8) + akordiyon("Sağlık", "pill", "yesil", "520 ₺ · 1 ürün")
            + h(24) + ay_karti(AYLAR, DIP))


# ---------------------------------------------------------------------------
# Tek kategori · sekiz ürün — T4/T9'un ortak verisi (spec §5.3 tablo B)
# Görünen 6 satır 107.195 ₺; gizli 2 ürün (Kulaklık 120 + Filtre 75) 195 ₺
# → 107.390 ₺ = kahraman sayı. Kalan toplam sekiz serinin TAMAMINI kapsar.
# ---------------------------------------------------------------------------
AYLAR_TEK = [("Eylül", "107.390 ₺", 100), ("Ekim", "107.131 ₺", 100),
             ("Kasım", "107.131 ₺", 100), ("Aralık", "107.131 ₺", 100),
             ("Ocak", "107.131 ₺", 100), ("Şubat", "105.208 ₺", 98)]
DIP_TEK = "Kalan toplam 1.161.862 ₺. Sonuncusu Ağustos 2027 tarihinde bitiyor."


def tek_kategori(satir_basili: int = -1, btn_basili: bool = False) -> str:
    satirlar = [
        ("Mutfak yenileme", "104.167 ₺", 1, 12, "1.145.837 ₺"),
        ("Telefon", "1.041 ₺", 4, 12, "8.333 ₺"),
        ("Oturma odası için üç kişilik kanepe takımı", "833 ₺", 2, 6, "3.332 ₺"),
        ("Buzdolabı", "520 ₺", 5, 9, "2.080 ₺"),
        ("Bisiklet", "375 ₺", 8, 12, "1.500 ₺"),
        ("Elektrikli süpürge", "259 ₺", 6, 6, "0 ₺"),
    ]
    ciz = [urun_satiri(ad, tut, no, top, kal, "duman", son=(no == top),
                       basili=(i == satir_basili), kuyu=False)
           for i, (ad, tut, no, top, kal) in enumerate(satirlar)]
    return (hero("107.390")
            + h(24) + bolum_basi("8 ürün", "circle-dashed", "duman", "Diğer") + h(8)
            + '<div class="pad kolon">' + f'{h(8)}'.join(ciz)
            + h(12) + tumunu_goster(8, basili=btn_basili) + '</div>'
            + h(24) + ay_karti(AYLAR_TEK, DIP_TEK))


# ===========================================================================
# T1 — dolu · üç kategori · en büyüğü açık  (ÖLÇÜLEN ÇERÇEVE)
# ===========================================================================
T1 = ekran(uc_kategori())

# ===========================================================================
# T2 — basılı: kapalı kategori kabı + akordiyon içindeki (kuyu) satır
# ===========================================================================
T2 = ekran(uc_kategori(satir_basili=0, kategori_basili=True))

# ===========================================================================
# T3 — TEK seri · akordiyon kurulmaz · ürün adı yok (kategoriye düşer)
# ===========================================================================
T3 = ekran(
    hero("520")
    + h(24) + bolum_basi("1 ürün", "pill", "yesil", "Sağlık") + h(8)
    + '<div class="pad kolon">'
    + urun_satiri("Sağlık taksidi", "520 ₺", 3, 10, "3.640 ₺", "yesil", kuyu=False)
    + '</div>'
    + h(24) + ay_karti(
        [("Eylül", "520 ₺", 100), ("Ekim", "520 ₺", 100), ("Kasım", "520 ₺", 100),
         ("Aralık", "520 ₺", 100), ("Ocak", "520 ₺", 100), ("Şubat", "520 ₺", 100)],
        "Kalan toplam 3.640 ₺. Sonuncusu Nisan 2027 tarihinde bitiyor."))

# ===========================================================================
# T4 — TEK kategori · 8 ürün · liste sınırı 6 + Tümünü göster · uzun ad ·
#      yedi haneli kalan tutar
# ===========================================================================
T4 = ekran(tek_kategori())

# ===========================================================================
# T5 — geçen ay biten seri şeridi · yük düştü · son taksit satırı kalktı
# ===========================================================================
T5 = ekran(
    hero("2.861")
    + h(24) + bolum_basi("3 kategori · 5 ürün") + h(8)
    + akordiyon("Diğer", "circle-dashed", "duman", "1.561 ₺ · 2 ürün", [
        urun_satiri("Telefon", "1.041 ₺", 5, 12, "7.292 ₺", "duman"),
        urun_satiri("Buzdolabı", "520 ₺", 6, 9, "1.560 ₺", "duman"),
    ])
    + h(8) + akordiyon("Giyim", "shirt", "kiremit", "780 ₺ · 2 ürün")
    + h(8) + akordiyon("Sağlık", "pill", "yesil", "520 ₺ · 1 ürün")
    + h(24) + ay_karti(AYLAR_DUSMUS, DIP_DUSMUS)
    + h(24) + '<div class="pad"><div class="serit serit-info">'
    f'<div class="ikon-kutu" style="color:var(--primary-text)">{ikon("info")}</div>'
    + w(12) + '<div class="esnek t-cap">Elektrikli süpürge taksidi eylül ayında '
    'bitti. Aylık yük 259 ₺ düştü.</div></div></div>')

# ===========================================================================
# T6 — boş: taksitli işlem yok  (v4'ten aynen)
# ===========================================================================
T6 = ekran(
    '<div class="pad"><div class="clay-lg kart-ic kolon orta">'
    '<div class="hero-daire hero-daire-bos hero-bos" style="width:176px;height:176px">'
    '<div class="hero-orta"><div class="ikon-kutu ikon-kutu-32" '
    f'style="color:var(--text-2)">{ikon("calendar-clock")}</div></div></div>'
    + h(12) + '<div class="t-h2">Taksitli işlem yok</div>' + h(8) +
    '<div class="t-body" style="text-align:center">Kartla taksitli harcama '
    'girdiğinde burada listelenir.</div></div></div>')

# ===========================================================================
# T7 — yükleniyor: iskelet gerçek düzenin yerini tutar
#      Chevron yeri boş bırakılır: ok bir eylem işaretidir, yüklenmemiş
#      satır dokunulabilir değildir — ama 32pt'lik yer tutulur ki düzen
#      yükleme bitince zıplamasın.
# ===========================================================================
ISK_SATIR = ('<div class="satir-kart kuyu"><div class="esnek kolon">'
             '<div class="aralik">' + iskelet("96px", 24) + w(12)
             + iskelet("72px", 24) + '</div>' + h(4)
             + iskelet("100%", 12) + h(4) + iskelet("136px", 18) + '</div>'
             + w(12) + '<div style="width:20px;height:20px;flex:0 0 auto"></div></div>')

ISK_AKORDIYON_KAPALI = ('<div class="pad"><div class="akordiyon">'
                        '<div class="akordiyon-bas">'
                        + iskelet("44px", 44, 16) + w(12) + iskelet("96px", 25)
                        + '<div class="esnek"></div>' + w(12)
                        + iskelet("104px", 18) + w(12)
                        + iskelet("20px", 20) + '</div></div></div>')

T7 = ekran(
    '<div class="pad"><div class="clay-lg kart-ic">'
    + iskelet("52px", 18) + h(4) + iskelet("152px", 38) + h(12)
    + iskelet("100%", 18) + '</div></div>'
    + h(24)
    # Bölüm başlığı için 25pt ayrılır (r3): iskelet, **çizdiği düzenin**
    # yüksekliğini ayırır. Aşağıda üç akordiyon var, yani bu iskelet ÇOK
    # kategorili düzeni tahmin ediyor ve o düzende başlık 25'tir. 44 ayırmak
    # (r2) iskeletin kendi içinde çelişmesiydi: çok kategori çözüldüğünde
    # başlık 19px yukarı zıplıyordu. Kategori sayısı yüklenmeden bilinmez;
    # tek kategori çıkarsa 19px'lik **aşağı oturma** kabul edilir (§4.2).
    + '<div class="pad aralik">'
    + iskelet("176px", 25) + iskelet("128px", 18) + '</div>'
    + h(8)
    + '<div class="pad"><div class="akordiyon"><div class="akordiyon-bas">'
    + iskelet("44px", 44, 16) + w(12) + iskelet("80px", 25)
    + '<div class="esnek"></div>' + w(12) + iskelet("20px", 20) + '</div>'
    + h(12) + ISK_SATIR + h(12) + ISK_SATIR + '</div></div>'
    + h(8) + ISK_AKORDIYON_KAPALI
    + h(8) + ISK_AKORDIYON_KAPALI
    + h(24)
    + '<div class="pad"><div class="clay kart-ic">' + iskelet("176px", 25) + h(8)
    + f'{h(8)}'.join(
        '<div class="satir">' + iskelet("56px", 18) + w(12)
        + '<div class="esnek">' + iskelet("100%", 12) + '</div>' + w(12)
        + iskelet("88px", 24) + '</div>' for _ in range(6))
    + '</div></div>')

# ===========================================================================
# T8 — ağ hatası: tek okuma yolu, tek hata yüzeyi
# ===========================================================================
T8 = ekran(
    '<div class="pad"><div class="clay-lg kart-ic kolon orta">'
    f'<div class="hata-daire">{ikon("wifi-off")}</div>' + h(24) +
    '<div class="t-h2">Taksitler açılamadı</div>' + h(8) +
    '<div class="t-body" style="text-align:center">Bir şey ters gitti. Yeniden '
    'denemek çoğu zaman yeterli.</div>' + h(24) +
    '<button class="btn-primary" aria-label="Yeniden dene">'
    f'{ikon("refresh")}{w(8)}Yeniden dene</button></div></div>')

# ===========================================================================
# T9 — basılı: KABARIK satır + "Tümünü göster". T2 akordiyon dilini
#      gösteriyor, bu çerçeve akordiyon KURULMAYAN düzenin iki hedefini.
# ===========================================================================
T9 = ekran(tek_kategori(satir_basili=1, btn_basili=True))

# ===========================================================================
BIRIMLER = [
    cihaz("E-18 TAKSİTLER", "dolu · üç kategori · en büyüğü açık", T1,
          "<b>Üç düzey, tek ekran.</b> Kahraman kart “bu ay 3.120 ₺” diyor "
          "(toplam kaybolmadı), akordiyonlar o toplamı <b>kategoriye</b>, satırlar "
          "<b>ürüne</b> bölüyor: 1.041 + 520 + 259 = 1.820 → 1.820 + 780 + 520 = 3.120. "
          "Toplama <b>ekrandaki</b> sayılarla yapılır: yuvarlama yapraklarda olur, üst "
          "düzeyler görünen değerleri toplar — yoksa üç düzeyi kafasında toplayan "
          "kullanıcı 2 ₺ eksik bulurdu. Satırda birincil olan iki şey üst satırda — "
          "<b>ürün adı</b> ve <b>bu ayki tutar</b>; ilerleme çubuğu ve “4/12 · kalan "
          "8.333 ₺” ikincil. Çubuk dolgusu kategorinin kendi rengi (tokens §1.4). "
          "Ölçüm: kaydırma alanı <b>769px</b> (844 − 47 durum çubuğu − 28 ana çubuk; "
          "sekme çubuğu yok, bu bir push ekranı) ve kesme <b>Sağlık</b> bölümünün "
          "725-769 arası başlık bloğundan sonra, kabın 16pt alt iç boşluğunda "
          "kalıyor — hiçbir satır, sayı ya da metin ortasından bölünmüyor."),
    cihaz("E-18 TAKSİTLER", "basılı · akordiyon dili · hover yoktur", T2,
          "RN'de hover yok, geri bildirimin tamamı <b>basılı</b> durumdur. Bu çerçevede "
          "iki hedef çöküyor: kapalı <b>Giyim</b> kabının tamamı (<b>groove + "
          "clay.pressed</b>) ve açık bölümdeki <b>Telefon</b> satırı (kuyu → groove). "
          "Ne scale ne opaklık kullanılıyor — nesne küçülmez, çöker. Akordiyon "
          "kurulmayan düzenin iki hedefi (kabarık satır + “Tümünü göster”) son "
          "çerçevede. Satırın sağındaki <b>20pt ok</b> dokunulabilirliği basılı duruma "
          "bırakmıyor, önceden söylüyor; okun 32pt'si esneyen <b>ad</b> sütunundan "
          "alınır, tutar sütunundan değil — tutar hiç kırpılmaz."),
    cihaz("E-18 TAKSİTLER", "tek seri · ürün adı yok · akordiyon kurulmaz", T3,
          "<b>Tek seride akordiyon çizilmez</b> — tek çocuklu bir kap yalnız dokunma "
          "maliyeti ekler. Akordiyonun <b>başlık yapısı</b> bu yüzden bölüm başlığına "
          "taşınır: solda <b>tek</b> 44pt ikon kabı, yanında <b>h2 “Sağlık”</b>, sağda "
          "“1 ürün” — ok yok, çünkü bu başlık açılıp kapanmıyor. Jenerik “Süren "
          "taksitler” başlığı bu düzende <b>düşer</b>: kab kategori adının yanında "
          "durmalı, yoksa 358px'lik satırın iki ucunda ilgisiz iki şey kalır ve aynı "
          "bileşen tek ekranda iki anlam taşır. Satır ikon kabını "
          "tekrarlamaz; aynı glifi her satırda yeniden çizmek, §4'ün “3 satırda 3 kez "
          "aynı ikon gürültüdür” kuralının tersi olurdu. Ürün adı boş kaydedilmiş seri "
          "“{Kategori} taksidi” olur: liste asla adsız satır göstermez, uydurma ad da "
          "üretmez."),
    cihaz("E-18 TAKSİTLER", "tek kategori · 8 ürün · liste sınırı · uzun ad", T4,
          "Bir kategoride <b>en çok 6 satır</b> çizilir; kalanı <b>Tümünü göster</b> "
          "ile <b>tek yönlü</b> açılır (iç içe akordiyon yasak, §3.12.3 — ve tek yönlü "
          "olması kaydırma konumunun kullanıcının altından çekilmesini engeller). "
          "Görünmeyen iki ürün de sayılara <b>dahildir</b>: 107.195 görünen + 195 gizli "
          "= <b>107.390 ₺</b> kahraman sayı, dip satırındaki <b>1.161.862 ₺</b> sekiz "
          "serinin tamamının kalanı. Başlıktaki “8 ürün” bu yüzden gerekli — altı satır "
          "sayıları açıklamıyor. Başlık burada <b>“Diğer · 8 ürün”</b> değil, "
          "akordiyon başlığının yapısı: kab + <b>h2 “Diğer”</b> + sağda “8 ürün”; "
          "kategori <b>tutarı</b> yazılmaz, çünkü tek kategoride o sayı kahraman "
          "kartın kendisidir. Uzun ürün adı tek satırda kırpılır, <b>tutar asla "
          "kırpılmaz</b>. Ay çubukları burada düzleşiyor: ölçek en büyük aya göredir ve "
          "104.167 ₺'lik seri her ayı domine ediyor — farkı sağdaki sayı taşıyor."),
    cihaz("E-18 TAKSİTLER", "seri bitti · yük düştü", T5,
          "Biten seri <b>listeden düşer</b>, kutlanmaz, kaydedilir: mavi bilgi şeridi "
          "artık <b>ürünü adıyla</b> anıyor (“Elektrikli süpürge taksidi eylül ayında "
          "bitti. Aylık yük 259 ₺ düştü.”). Şerit <b>en altta</b> — önce durum, sonra "
          "açıklama. Düşüş her düzeyde doğrulanabilir: Diğer 1.820 → 1.561 ₺, özet "
          "“3 ürün” → “2 ürün”, kalan toplam 17.693 → <b>14.832 ₺</b>. Kalan daima "
          "<b>bu aydan sonrasını</b> sayar, o yüzden düşen ay <b>Ekim</b>'dir "
          "(17.693 − 2.861), Eylül'ün 3.120'si değil."),
    cihaz("E-18 TAKSİTLER", "boş · taksitli işlem yok", T6,
          "Boş durum v4'ten <b>değişmedi</b>. Buton yok: taksit buradan eklenmez, "
          "harcama girilirken oluşur — cümle tam olarak bunu söylüyor. Kategori/ürün "
          "kırılımı için ayrı bir boş durum <b>üretilmedi</b>: seri yoksa kategori de "
          "yoktur, iki boş kutu üst üste koymak bilgi değil gürültüdür."),
    cihaz("E-18 TAKSİTLER", "yükleniyor · iskelet", T7,
          "İskelet <b>gerçek düzenin</b> yerini tutuyor: bir açık bölüm iki satırla, "
          "iki kapalı bölüm özet bloğuyla, ay kartı altı satırla. Kategori adları "
          "yüklenmeden <b>bilinmediği</b> için başlık da bloktur (Günlük'teki rutin "
          "bölümünde başlık gerçekti, çünkü orada metin sabittir) ve <b>44pt</b> yer "
          "ayırır: kategori sayısı 1 çıkarsa başlık ikon kabı alıp 44'e büyür (§4.2), "
          "25 ayırmak orada 19px zıplama demekti. Satırın sağındaki "
          "ok <b>çizilmez</b> — yüklenmemiş satır dokunulamaz — ama 32pt'lik yeri "
          "tutulur, yükleme bitince düzen zıplamaz. Parıldama ve tam ekran spinner yok."),
    cihaz("E-18 TAKSİTLER", "ağ hatası · tek okuma yolu", T8,
          "Üç düzeyin tamamı <b>aynı okumadan</b> gelir, bu yüzden kısmi hata durumu "
          "<b>yoktur</b> ve uydurulmadı: ya hepsi gelir ya tek hata yüzeyi çıkar. "
          "Mesaj ne olduğunu değil <b>ne yapacağını</b> söyler; “sunucu”, “bağlantı "
          "kodu” gibi teknik sözcük geçmez (brandbook §2.8)."),
    cihaz("E-18 TAKSİTLER", "basılı · akordiyonsuz düzenin iki hedefi", T9,
          "Akordiyon kurulmadığında basılı dil değişmez, <b>basamak</b> değişir: "
          "kabarık satır (<b>surface + clay.raised</b>) basılınca <b>groove + "
          "clay.pressed</b>'e çöker — kuyu satırla aynı son değere iner, çünkü basılı "
          "hâl tek bir dildir. <b>Tümünü göster</b> ghost düğmesi basılıyken "
          "<b>well + clay.pressed</b> olur: ghost'un zemini yok, o yüzden basılı hâli "
          "bir basamak yukarıdan başlar. İki hedef aynı çerçevede çizildi ki "
          "aralarındaki fark görülebilsin; gerçek kullanımda tek seferde biri basılır."),
]

GIRIS = ('E-18 Taksitler · <b>kategori → ürün kırılımı</b> · 390×844 (kaydırma alanı '
         '769px) · claymorphism (tokens.md v4) · push ekranı (sekme çubuğu yok) · '
         'akordiyon deseni Tasarruf'"'"'tan yeniden kullanıldı (stil-rev2.css §9-§10) · '
         'spesifikasyon: <a href="../rev3-taksitler.md">rev3-taksitler.md</a>')

(KOK / "taksitler.html").write_text(
    sayfa("Trinkow REV3 — Taksitler: kategori ve ürün kırılımı", GIRIS, BIRIMLER),
    encoding="utf-8")
print("yazıldı:", (KOK / "taksitler.html").relative_to(KOK.parent))
