# -*- coding: utf-8 -*-
"""E-10 Günlük — **rutin hızlı eylem bölümü** (REV3-r1 · 390×844, 8 durum).

Spesifikasyon: ../rev3-gunluk-rutin.md
Çalıştır    :  python3 _uret/uret_gunluk_rutin.py
Çıktı       :  ../gunluk-rutin.html

Çerçeveler ekranı **kaydırılmış** gösterir: rutin bölümü 10 kategori
satırının altındadır, yani gerçek cihazda ilk katın dışındadır. Kategori
kartının üst kenarı bu yüzden düzleşir (`.kirpik-ust`, bölge [A]) ve kesme
bir satırın ortasından değil iki satır ARASINDAN geçer (K-057/8).

Kategori kartı ve alt liste BU BELGENİN KAPSAMI DEĞİL: bugünkü kodun
(`CategoryQuickAddCard`) çizimi, yalnız bağlam için duruyor. Değişen tek
şey kartın ALTINA inen rutin bölümüdür.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import cihaz, ikon, sayfa, sekme_cubugu  # noqa: E402

KOK = pathlib.Path(__file__).parent.parent


def h(n: int) -> str:
    return f'<div class="h{n}"></div>'


def w(n: int) -> str:
    return f'<div class="w{n}"></div>'


def iskelet(gen: str, yuk: int) -> str:
    return f'<div class="iskelet" style="width:{gen};height:{yuk}px"></div>'


# ---------------------------------------------------------------------------
# [bağlam] kategori kartının kırpılmış alt ucu — bugünkü kod, DEĞİŞMEDİ
# ---------------------------------------------------------------------------
KAT_SON = [
    ("kat-kiremit", "shirt", "Giyim", "Bugün harcama yok"),
    ("kat-duman", "footprints", "Alışkanlıklar", "Bugün harcama yok"),
    ("kat-duman", "circle-dashed", "Diğer", "Bugün harcama yok"),
]


def kategori_satiri(sinif: str, ik: str, ad: str, alt: str) -> str:
    return (f'<div class="satir"><div class="kat-kab {sinif}">{ikon(ik)}</div>{w(12)}'
            f'<div class="esnek kolon"><div class="t-strong tek-satir">{ad}</div>'
            f'<div class="t-cap tek-satir">{alt}</div></div>{w(12)}'
            f'<button class="ekle-btn" aria-label="{ad} kategorisine harcama ekle">'
            f'{ikon("plus")}</button></div>')


def ayrac() -> str:
    return (f'{h(8)}<div class="satir"><div style="width:56px"></div>'
            f'<div class="esnek" style="height:1px;background-color:var(--line)"></div>'
            f'</div>{h(8)}')


def kategori_kirpik() -> str:
    """10 kategorinin son 3'ü (13 kategoriden sabit ödeme olan üçü listede
    yok — `GUNLUK_HARCAMA_KATEGORILERI`). Kart yukarıda devam ediyor."""
    ic = ayrac().join(kategori_satiri(*k) for k in KAT_SON)
    return ('<div class="pad"><div class="clay kart-ic kirpik-ust">'
            + ic + '</div></div>')


ALT_LISTE = ('<div class="pad aralik"><div class="t-h2">Planlı ödemeler</div>'
             '<div class="t-label c-2 num">Günlük toplam 116 ₺</div></div>'
             + h(8) +
             '<div class="pad"><div class="satir-kart">'
             f'<div class="kat-kab kat-lacivert">{ikon("receipt-text")}</div>{w(12)}'
             '<div class="esnek kolon"><div class="t-body tek-satir">İnternet</div>'
             '<div class="t-cap tek-satir">07.40 · Kart</div></div>' + w(12) +
             '<div class="t-amount num" style="flex:0 0 auto">320 ₺</div></div></div>')


# ---------------------------------------------------------------------------
# rutin bölümü
# ---------------------------------------------------------------------------
def eylem(ad: str, ik: str, etiket: str, secili: bool = False, basili: bool = False,
          pasif: bool = False, a11y: str = "", spinner: bool = False) -> str:
    """REV3-r1 · B2 — `spinner=True` yazma sırasındaki düğmedir: **`<button>`
    olarak kalır ve `disabled` taşır** (rol ve pasif semantiği kaybolmaz).
    Görsel olarak `pasif` (disabled-bg) ÇİZİLMEZ: kullanıcının o an dokunduğu
    düğme iyimser olarak işaretli görünür, çünkü geri bildirim onun dokunuşudur.
    Kilitlenen ama dokunulmayan öteki düğme `pasif` çizilir."""
    sinif = "rutin-eylem"
    if secili:
        sinif += " secili"
    if basili:
        sinif += " basili"
    if pasif:
        sinif += " pasif"
    kilitli = pasif or spinner
    ek = ' disabled aria-disabled="true"' if kilitli else ""
    bas = f' aria-pressed="{"true" if secili else "false"}"' if not kilitli else ""
    ic = '<div class="spinner"></div>' if spinner else ikon(ik)
    return (f'<button class="{sinif}" aria-label="{a11y or ad}"{bas}{ek}>{ic}'
            f'{h(4)}<div class="t-micro">{etiket}</div></button>')


def rutin_satiri(ad: str, tutar: str, durum: str = "bos", alt: str = "",
                 basili: str = "", yukleniyor: str = "", gun: str = "") -> str:
    """REV3 §4 — satırda YALNIZ ad · mali değer · iki eylem vardır.
    Kategori, günlük adet ve geçmiş bu satırda GÖRÜNMEZ (rutin yönetimi
    `/rutinler` ekranındadır). Tutar **günün tamamıdır**: günlük adet 2 olan
    31 ₺'lik kahve satırda 62 ₺ yazar (Ö3 · §4).

    `durum`: bos | aldim | almadim. `alt` yalnız işaretli durumlarda yazılır;
    işaretsiz satır tek satırdır ve dikeyde ortalanır (satır yüksekliği
    değişmez: metin kolonu 46, düğmeler 44).

    `yukleniyor`: hangi eylemin isteği uçuşta. B2 — bu hâlde **iki düğme de**
    `disabled`; dokunulan düğme spinner taşır, öteki `pasif` çizilir.

    `gun`: geçmiş gün etiketi. B3 — verildiğinde eylem etiketleri günü de
    söyler ("Kahve, 16 Eylül. Aldım olarak işaretle, 31 ₺"); görsel etiket
    gün-nötr kalır (§8)."""
    alt_html = f'{h(4)}<div class="t-cap tek-satir">{alt}</div>' if alt else ""
    on = f"{ad}, {gun}. " if gun else f"{ad} "
    fiil_aldim = "Aldım olarak işaretle" if gun else "aldım olarak işaretle"
    fiil_almadim = "Almadım olarak işaretle" if gun else "almadım olarak işaretle"
    aldim = eylem(ad, "plus", "Aldım",
                  secili=(durum == "aldim" or yukleniyor == "aldim"),
                  basili=(basili == "aldim"),
                  pasif=(yukleniyor == "almadim"),
                  spinner=(yukleniyor == "aldim"),
                  a11y=(f"{ad} yazılıyor" if yukleniyor == "aldim"
                        else f"{on}{fiil_aldim}, {tutar}"))
    almadim = eylem(ad, "circle-slash", "Almadım",
                    secili=(durum == "almadim" or yukleniyor == "almadim"),
                    basili=(basili == "almadim"),
                    pasif=(durum == "aldim" or yukleniyor == "aldim"),
                    spinner=(yukleniyor == "almadim"),
                    a11y=(f"{ad} işaretleniyor" if yukleniyor == "almadim"
                          else f"{on}{fiil_almadim}, {tutar} rutin tasarrufu"))
    return (f'<div class="satir"><div class="esnek kolon">'
            f'<div class="aralik"><div class="t-strong esnek tek-satir">{ad}</div>{w(8)}'
            f'<div class="t-amount num" style="flex:0 0 auto">{tutar}</div></div>'
            f'{alt_html}</div>{w(12)}{aldim}{w(12)}{almadim}</div>')


def rutin_bolum(ozet: str, icerik: str = "", basili: bool = False,
                gun_etiketi: str = "", iskelet_ozet: bool = False) -> str:
    """Açılır bölüm — Tasarruf akordiyonuyla AYNI bileşen (`.akordiyon`).

    Başlığın sağı: **kapalıyken özet değer**, açıkken boş — kapsam (gün)
    ekran başlığında zaten yazılı. TEK İSTİSNA geçmiş gündür (`gun_etiketi`):
    eylemin anlamı güne bağlı olduğu için gün açıkken de başlıkta durur.

    B3 — geçmiş günde gün bilgisi **ekran okuyucuya da** ulaşır:
    etiket "Rutinler. 16 Eylül. {özet}" olur (`a11y.gunlukRutin.bolumGecmis`).
    Ö5 — iskelet hâlinde etiket boş kalmaz: "Rutinler. Yükleniyor"."""
    # `iskelet_ozet` bu ifadeye GİRMEZ: kapalı + yükleniyor çağrısında
    # `acik` true olsaydı hem aria-expanded="true" hem 104x18 özet yer tutucusu
    # çizilirdi — §3.1 "açık bölüm özet taşımaz" kuralıyla çelişir.
    # (uret.py `akordiyon()` ile aynı hâl.)
    acik = bool(icerik)
    sag = ""
    if iskelet_ozet and not icerik:
        # Özetin YERİ yalnız bölüm KAPALI yüklenirken korunur. Açık iskelette
        # korunmaz, çünkü yüklü açık bölüm de özet taşımaz — placeholder
        # konsa yükleme bitince başlık satırı zıplardı (uret.py `akordiyon`
        # ile aynı kural).
        sag = f'<div style="flex:0 0 auto">{iskelet("104px", 18)}</div>' + w(12)
    elif gun_etiketi:
        sag = (f'<div class="t-label c-2 tek-satir" style="flex:0 0 auto">{gun_etiketi}'
               f'</div>' + w(12))
    elif not acik:
        sag = (f'<div class="t-label c-2 num tek-satir" style="flex:0 0 auto">{ozet}</div>'
               + w(12))
    if iskelet_ozet:
        etiket = "Rutinler. Yükleniyor"
    elif gun_etiketi:
        etiket = f"Rutinler. {gun_etiketi}. {ozet}"
    else:
        etiket = f"Rutinler. {ozet}"
    bas = (f'<button class="akordiyon-bas" aria-expanded="{"true" if acik else "false"}" '
           f'aria-label="{etiket}">'
           f'<div class="t-h2 esnek tek-satir">Rutinler</div>{w(12)}{sag}'
           f'{ikon("chevron-down", "cev-acik" if acik else "")}</button>')
    b = " basili" if basili else ""
    return (f'<div class="pad"><div class="akordiyon{b}">{bas}'
            f'{(h(12) + icerik) if acik else ""}</div></div>')


def satirlar(liste: list[str]) -> str:
    return f'{h(12)}'.join(liste)


def ekran(icerik: str) -> str:
    return (f'<main class="content"><div class="kaydir">{icerik}{h(24)}</div>'
            f'{sekme_cubugu("gunluk")}</main>')


TUMU = (h(12) + '<button class="btn-ghost" style="padding:0 16px" '
        'aria-label="Tüm rutinleri aç"><div class="tek-satir">Tüm rutinler</div></button>')

# ===========================================================================
# G1 — bölüm AÇIK · üç durum yan yana + bir düğme basılı
# ===========================================================================
# B4 — sıra AÇILIŞTA kurulur (mali değeri büyük olan önce: 60 · 31 · 28) ve
# işaretleme sonrası satırlar YERİNDE kalır. Bu çerçeve o yüzden geçerli bir
# hâldir: kullanıcı Sigara ve Kahve'yi işaretledi, satırlar zıplamadı.
G1 = ekran(
    kategori_kirpik() + h(8)
    + rutin_bolum("3 rutin · 1 işaretsiz", satirlar([
        rutin_satiri("Sigara", "60 ₺", "almadim", "Vazgeçtin · rutin tasarrufu"),
        rutin_satiri("Kahve", "31 ₺", "aldim", "Yazıldı · 08.20"),
        rutin_satiri("Enerji içeceği", "28 ₺", basili="almadim"),
    ]))
    + h(24) + ALT_LISTE)

# ===========================================================================
# G2 — bölüm KAPALI + "Geri al" toast'ı
# ===========================================================================
TOAST = ('<div class="katman-bas"><div class="pad" style="padding-top:8px">'
         '<div class="toast"><div class="nokta"></div>' + w(12) +
         '<div class="t-body esnek">Sigara almadın olarak işaretlendi.</div>' + w(12) +
         '<button class="btn-ghost" style="padding:0 16px" aria-label="İşlemi geri al">'
         '<div class="t-strong c-primary tek-satir">Geri al</div></button></div></div></div>')

G2 = ('<main class="content"><div class="kaydir">'
      + kategori_kirpik() + h(8)
      + rutin_bolum("3 rutin · 1 işaretsiz")
      + h(24) + ALT_LISTE + h(24)
      + '</div>' + sekme_cubugu("gunluk") + TOAST + "</main>")

# ===========================================================================
# G2B — kapalı bölümün İKİNCİ özet varyantı: günün işi bitmiş
# ===========================================================================
G2B = ekran(
    kategori_kirpik() + h(8)
    + rutin_bolum("3 rutin · hepsi işaretli")
    + h(24) + ALT_LISTE)

# ===========================================================================
# G3 — liste sınırı (6 rutin → 5 satır) · uzun ad · "Almadım" pasif
# ===========================================================================
G3 = ekran(
    kategori_kirpik() + h(8)
    # B4 — açılış sırası: 95 · 62 · 60 · 28 · 27; altıncı satır (Simit 12 ₺)
    # kesildi. Ö3 — "Kahve" günlük adedi 2 olan rutindir: satır 2 × 31 = 62 ₺
    # yazar, adet satırda GÖRÜNMEZ (doğrulama /rutinler'de).
    + rutin_bolum("6 rutin · 4 işaretsiz", satirlar([
        rutin_satiri("Öğle yemeği yerine evden getirdiğim kumanya", "95 ₺"),
        rutin_satiri("Kahve", "62 ₺", "aldim", "Yazıldı · 08.20"),
        rutin_satiri("Sigara", "60 ₺", yukleniyor="aldim"),
        rutin_satiri("Enerji içeceği", "28 ₺"),
        rutin_satiri("Otobüs", "27 ₺", "almadim", "Vazgeçtin · rutin tasarrufu"),
    ]) + TUMU)
    + h(24) + ALT_LISTE)

# ===========================================================================
# G4 — rutinler yükleniyor (iskelet) + bir satırda eylem yazılıyor
# ===========================================================================
G4 = ekran(
    kategori_kirpik() + h(8)
    + rutin_bolum("", satirlar([
        f'<div class="satir"><div class="esnek kolon">{iskelet("96px", 24)}{h(4)}'
        f'{iskelet("136px", 18)}</div>{w(12)}'
        f'<div class="iskelet" style="width:64px;height:44px;border-radius:16px"></div>'
        f'{w(12)}<div class="iskelet" style="width:64px;height:44px;border-radius:16px">'
        f'</div></div>',
        f'<div class="satir"><div class="esnek kolon">{iskelet("72px", 24)}</div>{w(12)}'
        f'<div class="iskelet" style="width:64px;height:44px;border-radius:16px"></div>'
        f'{w(12)}<div class="iskelet" style="width:64px;height:44px;border-radius:16px">'
        f'</div></div>',
    ]), iskelet_ozet=True)
    + h(24) + ALT_LISTE)

# ===========================================================================
# G5 — işaret kaydedilemedi (ağ hatası) · satır eski hâline döner
# ===========================================================================
G5 = ekran(
    kategori_kirpik() + h(8)
    + rutin_bolum("3 rutin · 2 işaretsiz",
                  '<div class="serit serit-warn">'
                  f'<div class="ikon-kutu c-warn">{ikon("wifi-off")}</div>{w(12)}'
                  '<div class="t-cap esnek" style="color:var(--text)">İşaret kaydedilemedi. '
                  'Yeniden dene.</div></div>' + h(12) + satirlar([
                      rutin_satiri("Sigara", "60 ₺"),
                      rutin_satiri("Kahve", "31 ₺", "aldim", "Yazıldı · 08.20"),
                      rutin_satiri("Enerji içeceği", "28 ₺"),
                  ]))
    + h(24) + ALT_LISTE)

# ===========================================================================
# G6 — rutin yok: bölüm HİÇ çizilmez
# ===========================================================================
G6 = ekran(kategori_kirpik() + h(24) + ALT_LISTE)

# ===========================================================================
# G7 — geçmiş gün · gün-nötr etiketler, başlıkta gün
# ===========================================================================
G7 = ekran(
    kategori_kirpik() + h(8)
    # B3 — gün bilgisi sesli katmanda da var: bölüm etiketi "Rutinler.
    # 16 Eylül. 3 rutin · 2 işaretsiz", eylem etiketleri "… , 16 Eylül. …".
    + rutin_bolum("3 rutin · 2 işaretsiz", satirlar([
        rutin_satiri("Sigara", "60 ₺", gun="16 Eylül"),
        rutin_satiri("Kahve", "31 ₺", "aldim", "Yazıldı · 08.20", gun="16 Eylül"),
        rutin_satiri("Enerji içeceği", "28 ₺", gun="16 Eylül"),
    ]), gun_etiketi="16 Eylül")
    + h(24) + ALT_LISTE)

# ===========================================================================
BIRIMLER = [
    cihaz("E-10 GÜNLÜK · RUTİN", "bölüm açık · üç durum",
          G1,
          "Rutinler kategori kartının <b>altında</b>, aynı açılır bileşenle "
          "(<b>.akordiyon</b>) duruyor. Satırda yalnız <b>ad · mali değer · iki eylem</b> "
          "var; kategori, günlük adet ve geçmiş burada görünmez. Ayrım renkte değil "
          "<b>ikon + görünür etiket</b>te: <b>plus/Aldım</b> ve <b>circle-slash/Almadım</b> "
          "(kilitli set, varliklar.md §1.2c). İki hedef 44 yüksekliğinde ve aralarında "
          "12pt var; “Kahve” aldım işaretli olduğu için “Almadım” <b>pasif</b> (zemin "
          "disabled-bg, opaklık yok). Üçüncü satırın “Almadım” düğmesi <b>basılı</b>. "
          "Satır sırası <b>açılışta</b> kurulur (60 · 31 · 28) ve işaretleme sonrası "
          "<b>yerinde kalır</b>: parmağın altındaki satır listenin sonuna zıplamaz."),
    cihaz("E-10 GÜNLÜK · RUTİN", "bölüm kapalı · geri al toast'ı",
          G2,
          "Kapalı hâl <b>boş bir başlık değil</b>: sağında “3 rutin · 1 işaretsiz” duruyor, "
          "yani kullanıcı açmadan ne olduğunu biliyor. Her iki eylem de <b>6 sn</b> "
          "“Geri al” taşıyor (K-029 deseni, <b>undoInfo</b> varyantı — silme kırmızısı "
          "kullanılmaz). Yanlış dokunuş sessiz kalmaz: satır anında durum değiştirir."),
    cihaz("E-10 GÜNLÜK · RUTİN", "kapalı bölüm · günün işi bitti",
          G2B,
          "Özetin ikinci varyantı: <b>“3 rutin · hepsi işaretli”</b>. Aynı yüzey, aynı "
          "ölçü — değişen yalnız cümle. Hiçbiri işaretli değilken üçüncü varyant yazılır "
          "(“3 rutin · işaretlenmedi”). Kapalı bölüm hiçbir hâlde boş başlık olmaz, yani "
          "kullanıcı açmadan günün işini bitirip bitirmediğini bilir."),
    cihaz("E-10 GÜNLÜK · RUTİN", "liste sınırı · uzun ad · pasif eylem",
          G3,
          "Açık listede <b>en çok 5 satır</b> (işaretsizler önce, sonra tutarı büyük "
          "olan); kalanı <b>Tüm rutinler</b> → /rutinler. Uzun rutin adı tek satırda "
          "kırpılır, <b>tutar asla kırpılmaz</b>. Özet “6 rutin · 4 işaretsiz” toplamı "
          "söylüyor, yani liste sınırı bilgi kaybı değil. Üçüncü satır <b>yazma "
          "sırasında</b>: düğme iyimser olarak işaretliye geçer, ikonun yerini 20pt "
          "spinner alır, etiket ve genişlik sabit kalır — ve <b>aynı satırın “Almadım”ı "
          "da kilitlenir</b> (pasif + disabled), çünkü bir gün iki işaret birlikte "
          "duramaz. İkinci satır <b>günlük adedi 2</b> olan rutindir: 31 ₺'lik kahve "
          "satırda <b>62 ₺</b> (2 × 31) yazar; adet satırda görünmez, tek dokunuş günün "
          "tamamını işaretler, doğrulama ve kısmi işaret <b>/rutinler</b>dedir."),
    cihaz("E-10 GÜNLÜK · RUTİN", "yükleniyor · iskelet",
          G4,
          "Rutinler ayrı bir okumadan gelir: ≥150ms sürerse <b>iskelet</b>. Başlık ve "
          "chevron gerçek (metin hemen hazır), iki satırın yeri çukur bloklarla korunur — "
          "yükleme bitince düzen zıplamaz. Bölüm <b>açık</b> yüklendiği için özetin yeri "
          "<b>ayrılmaz</b>: yüklü açık bölüm de özet taşımaz, placeholder konsa başlık "
          "satırı yükleme bitince zıplardı (özetin 104×18 yeri yalnız <b>kapalı</b> "
          "yüklenen bölümde korunur). Ekran okuyucu boş başlık duymaz: etiket "
          "<b>“Rutinler. Yükleniyor”</b>dur (Ö5)."),
    cihaz("E-10 GÜNLÜK · RUTİN", "işaret kaydedilemedi",
          G5,
          "İyimser güncelleme geri alınır ve satır eski hâline döner; hata <b>bölümün "
          "içinde</b> tek satır şerit olarak durur (ekranın geri kalanı çalışmaya devam "
          "eder). Teknik hata kodu ve “sunucu” sözcüğü yok (brandbook §2.8)."),
    cihaz("E-10 GÜNLÜK · RUTİN", "rutin yok · bölüm çizilmez",
          G6,
          "Rutini olmayan kullanıcıda bölüm <b>hiç görünmez</b> — Günlük en çok açılan "
          "ekran, kurulmamış bir özelliğin boş kutusu burada yer tutmaz. Rutin kurma "
          "yolu ikisi de yerinde: onboarding ve Profil → Rutinler. İlk rutin eklendiği "
          "an bölüm kendiliğinden görünür."),
    cihaz("E-10 GÜNLÜK · RUTİN", "geçmiş gün · gün-nötr etiketler",
          G7,
          "Geçmiş gün (takip başlangıcından sonra) <b>işaretlenebilir</b> — API bunu "
          "zaten “bugün ve geçmiş takipli günler” için açıyor. Etiketler bu yüzden "
          "gün-nötrdür (“Aldım”, “Bugün aldım” değil) ve başlığın sağında <b>gün</b> "
          "durur, bölüm açıkken bile: eylemin anlamı güne bağlıysa gün gizlenmez. "
          "Gün bilgisi <b>yalnız görsel kanalda değil</b>: bölüm etiketi “Rutinler. "
          "16 Eylül. 3 rutin · 2 işaretsiz”, her eylem etiketi de günü söyler — "
          "ekran okuyucu kullanıcısı hangi güne yazdığını duyar. "
          "Gelecek gün yoktur; takip başlangıcından önceki günde bölüm çizilmez."),
]

GIRIS = ('E-10 Günlük · <b>rutin hızlı eylem bölümü</b> · 390×844 · claymorphism '
         '(tokens.md v4) · ekranlar kategori listesine <b>kaydırılmış</b> hâlde '
         '(rutin bölümü 10 kategori satırının altındadır) · spesifikasyon: '
         '<a href="../rev3-gunluk-rutin.md">rev3-gunluk-rutin.md</a>')

(KOK / "gunluk-rutin.html").write_text(
    sayfa("Trinkow REV3 — Günlük rutin satırı", GIRIS, BIRIMLER), encoding="utf-8")
print("yazıldı:", (KOK / "gunluk-rutin.html").relative_to(KOK.parent))
