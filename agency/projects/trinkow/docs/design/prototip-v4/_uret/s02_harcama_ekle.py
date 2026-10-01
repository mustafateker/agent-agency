# -*- coding: utf-8 -*-
"""E-11 · Harcama ekle — arketip E (Checkout / form). Sekme çubuğu düşer.
Mood: tek işe kilitli, alt yarısı tuş takımıyla dolu, hızlı.

v4 · T-4 REVİZYONU — ÜRÜN ARAMA (F-18 · K-050)
===============================================================================
Ürün arama bir **fiyat girme kısayoludur**, bir ürün/besin veritabanı değildir.
Katalog **fiyat göstermez** (K-050, kesin yasak): tek izinli fiyat bilgisi
kullanıcının **kendi son kaydıdır** ("geçen sefer 95 ₺").

DOKUNUŞ BÜTÇESİ (rakam/harf tuşları veri girişidir, sayılmaz)
  Varsayılan yol (ürünsüz) : [1] FAB → [2] kategori çipi → [3] Kaydet     = 3
  Son kullandıkların       : [1] FAB → [2] çip → [3] Kaydet               = 3
                             (tuş vuruşu ~4 → 0; kategori de çipten gelir)
  Arama · kendi geçmişinden: [1] FAB → [2] arama → [3] sonuç → [4] Kaydet = 4
  Arama · katalogdan (yeni): [1] FAB → [2] arama → [3] sonuç → [4] Kaydet = 4
                             (tutarı kullanıcı yazar — katalogda fiyat yok)

🔴 ARAMA VARSAYILAN YOLU UZATMAZ — ekranda kanıtı üç tane:
  1. Arama alanı tutar kuyusunun **ALTINDADIR** ve sheet açılırken **odaklı
     değildir**; odak tutarda, kil tuş takımı hazır.
  2. Placeholder "Ne aldın? (isteğe bağlı)" — zorunlu olmadığını alanın
     kendisi söyler, ayrı bir açıklama satırı gerekmez.
  3. Tutara ilk rakam girilince "Son kullandıkların" şeridi kapanır ve
     **Kategori şeridi yukarı taşınır**: 3 dokunuşluk yol kaydırma
     gerektirmeden tamamlanır (yüzey B).

🔴 KATEGORİ ÖNCEDEN SEÇİLİ GELMEZ (ekran-envanteri §4, onaylı karar).
Kategori yalnız bir ürün seçildiğinde dolar — o zaman tahmin değil, ürünün
kataloğa yazılı bağıdır ya da kullanıcının kendi kaydıdır. Doldu**ğunda**
seçim şeridi yerine **tek satırlık açılır değer** (dropdown) gösterilir:
seçilecek bir şey kalmadı, değiştirilecek bir değer var.

🔴 VARSAYILAN ÖDEME TİPİ = "Kart" (tek değer, Ayarlar'dan gelir).

🔴 K-049 · HANGİ GÜNE YAZILIYOR: gün, tutar kuyusunun İÇİNDE, "Tutar"
etiketinin karşısındaki dokunulabilir satırdadır — kaydın günü kaydın tutarıyla
aynı yerde durur. Bugün değilse mürekkep `primary-text`e, ağırlık 600'e döner ve
kuyunun altına yazılı şerit iner. Amber/kırmızı KULLANILMAZ: tokens §1.5'e göre
amber yalnız "limit dışı" sinyalidir ve daima o sözcükle gelir (yüzey L).

🔴 KATEGORİ KONTROLÜ TEK KURALDAN TÜRER:
   kategori üründen/kayıttan doldu → **değer satırı + chevron** (dropdown)
   kategoriyi kullanıcı seçiyor    → **çip şeridi**
Otomatik dolan her şey, tutar kuyusunun altında **tek cümlede** söylenir.

🔴 KATLAMA SÖZLEŞMESİ (390×844, kil tuş takımı 324px sabit): zorunlu üç şey —
tutar kuyusu · kategori kontrolü · Kaydet — her yüzeyde katlamanın ÜSTÜNDEDİR
ya da ekrana sabittir. Katlama yalnız varsayılanı olan (Ödeme), isteğe bağlı
(Not) bloklara ya da kaydırılan liste satırlarına düşer. Yüzey bazında hesap:
delta-v4.md → T-4 → "Katlama tablosu".

🔴 KALDIRILAN: gömülü tütün FİYAT listesi (K-033/3 · K-037). K-050 kataloğa
fiyat yazmayı yasakladı. Marka adları katalogdan değil **kullanıcının kendi
geçmişinden** gelir; katalog jenerik kalemi taşır ("Sigara paketi"). Bkz.
delta-v4.md → T-4 → 🔴 Çelişkiler.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, kat_kab, CATS, tus_takimi, kaydet, isk

OUT = pathlib.Path(__file__).parent.parent / "02-harcama-ekle.html"

# Prototipin "bugün"ü v4 boyunca 17 Eylül Perşembe (s01 · delta T-3 ile aynı).
BUGUN = "Bugün · 17 Eylül"
DUN = "Dün · 16 Eylül"


def basi():
    return f'''            <div class="ekran-basi">
              <div class="t-h1">Harcama ekle</div>
              <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
            </div>'''


# ------------------------------------------------------------- tutar kuyusu
def gun_btn(metin, vurgu=False, basili=False):
    """Kaydın günü — tutar kuyusunun İÇİNDE, etiketin karşısında.
    20pt ikon + 13pt metin (dokunma hedefi hitSlop ile 44, tokens §6).
    `vurgu=True` → bugün değil: mürekkep `primary-text`, ağırlık 600.
    Dokununca E-24 Gün seçici açılır (K-049)."""
    c = " vurgu" if vurgu else ""
    b = " basili" if basili else ""
    tip = "t-label" if vurgu else "t-cap"
    return (f'<button class="gun-btn{c}{b}" aria-label="Gün seç, şu an {metin}">'
            f'<div class="ikon-kutu">{icon("calendar-days")}</div>'
            f'<div class="w8"></div><div class="{tip}">{metin}</div></button>')


def tutar_kuyusu(sayi, gun=BUGUN, vurgu=False, gun_basili=False, hata="",
                 alt_not="", oneri="", buyuk=None):
    """tokens.md §7.11: tutar 7 karakteri aşarsa (8+) `hero` → `display` iner.
    Ölçek uzunluktan otomatik hesaplanır (K-042'yi tekrarlamamak için tek yer).
    `oneri` → "Geçen sefer 95 ₺" çipi: girilmiş tutarın ÜZERİNE YAZMAZ, teklif eder.
    """
    if buyuk is None:
        buyuk = len(sayi) < 8
    cls = "t-hero" if buyuk else "t-display"
    simge = "t-hero-simge" if buyuk else "t-display"
    kuyu = "clay-kuyu" + (" giris-hatali" if hata else "")
    ek = ""
    if hata:
        ek = f'<div class="h8"></div><div class="t-cap c-danger">{hata}</div>'
    elif alt_not:
        ek = f'<div class="h8"></div><div class="t-cap">{alt_not}</div>'
    oneri_html = ""
    if oneri:
        oneri_html = f'''
              <div class="h8"></div>
              <div class="satir">
                <button class="cip" aria-label="Geçen sefer ödediğin {oneri} tutarını kullan">Geçen sefer {oneri}</button>
              </div>'''
    return f'''            <div class="pad">
              <div class="{kuyu}" style="padding:16px">
                <div class="aralik">
                  <div class="t-label c-2">Tutar</div>
                  {gun_btn(gun, vurgu=vurgu, basili=gun_basili)}
                </div>
                <div class="h8"></div>
                <div class="satir" style="justify-content:center;align-items:baseline">
                  <div class="{cls}">{sayi}</div>
                  <div class="imlec"></div>
                  <div class="w8"></div>
                  <div class="{simge} c-2">₺</div>
                </div>
              </div>
              {ek}{oneri_html}
            </div>'''


def gecmis_gun_seridi(gun="16 Eylül"):
    """Bugün değilse yanlış güne kayıt en sinir bozucu hatadır (K-049).
    Bu yüzden vurgulu çipin yanına bir de yazılı cümle iner."""
    return f'''            <div class="pad">
              <div class="serit serit-info">
                <div class="ikon-kutu c-primary">{icon("calendar-days")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap" style="color:var(--text)">Bu kayıt {gun}'e yazılacak.</div>
              </div>
            </div>'''


# -------------------------------------------------------------- arama alanı
def arama(deger="", odakli=False, urun="", yukleniyor=False):
    """Ürün arama. Boşken akışa karışmaz: odaklanmaz, hata üretmez,
    Kaydet'i engellemez. Seçilen ürün kaydın AYRI alanıdır (K-033 veri modeli).
    """
    o = " odakli" if odakli else ""
    spin = ('<div class="w8"></div><div class="spinner spinner-koyu"></div>'
            if yukleniyor else '')
    if urun:
        ic = (f'<div class="esnek t-body tek-satir">{urun}</div>'
              f'<div class="w8"></div>'
              f'<button class="ikon-btn" aria-label="Ürünü kaldır">{icon("x")}</button>')
    elif deger:
        ic = (f'<div class="esnek t-body tek-satir">{deger}</div>'
              + ('<div class="imlec"></div>' if odakli else '')
              + spin
              + f'<div class="w8"></div>'
              f'<button class="ikon-btn" aria-label="Aramayı temizle">{icon("x")}</button>')
    else:
        ic = '<div class="esnek t-body c-2 tek-satir">Ne aldın? (isteğe bağlı)</div>'
    return f'''            <div class="pad">
              <div class="giris{o}" aria-label="Ürün ara, isteğe bağlı">
                <div class="ikon-kutu c-2">{icon("search")}</div>
                <div class="w12"></div>
                {ic}
              </div>
            </div>'''


def son_kullanilanlar(items):
    """Yazmadan görünen en kısa yol: ürün + kategori + **kullanıcının kendi
    son tutarı** tek dokunuşta gelir. Tutar 0 iken durur, ilk rakam girilince
    kapanır — girilmiş bir tutarın üzerine sessizce yazan çip tuzaktır.

    Buradaki tutar KATALOG FİYATI DEĞİLDİR (K-050): kullanıcının kendi son
    kaydıdır ve şeridin başlığı bunu söyler.

    TAŞMA (tokens §7.6): çip tek satırda kalır, sarmaz; uzun ad `cip-ad`
    içinde kırpılır, tutar `cip-tutar` ile **hiç kırpılmaz**.
    """
    c = []
    for ad, tutar, renk in items:
        c.append(f'<button class="cip" aria-label="{ad}, geçen sefer {tutar}">'
                 f'<div class="nokta" style="background-color:var(--{renk})"></div>'
                 f'<div class="w8"></div><div class="cip-ad">{ad}</div>'
                 f'<div class="w8"></div><div class="cip-tutar">· {tutar}</div>'
                 f'</button><div class="w8"></div>')
    return f'''            <div class="pad">
              <div class="t-label c-2">Son kullandıkların</div>
            </div>
            <div class="h8"></div>
            <div class="yatay-kaydir pad">
              {''.join(c)}
            </div>'''


# ------------------------------------------------------------ arama sonuçları
def sonuc(ad, kategori, gecen="", basili=False, yeni=False, arama_metni=""):
    """Tek arama sonucu.

    🔴 SAĞDA TUTAR SÜTUNU YOKTUR. Katalog fiyat göstermez (K-050); kullanıcının
    kendi son tutarı ikinci satırda, **"geçen sefer" sözcüğüyle** ve `caption`
    ağırlığında durur. Fiyat gibi görünen bir sütun, olmayan bir otoriteyi
    ima ederdi.
    """
    b = " basili" if basili else ""
    if yeni:
        kab = f'<div class="kat-kab notr">{icon("plus")}</div>'
        ad_html = f'<div class="t-body tek-satir">“{arama_metni}” olarak ekle</div>'
        alt = '<div class="t-cap tek-satir">Kategoriyi ve tutarı sen seç.</div>'
    else:
        kab = kat_kab(kategori)
        ad_html = f'<div class="t-body tek-satir">{ad}</div>'
        ikinci = f"{kategori} · geçen sefer {gecen}" if gecen else kategori
        alt = f'<div class="t-cap tek-satir">{ikinci}</div>'
    return f'''              <button class="satir-kart{b}" style="width:100%">
                {kab}
                <div class="w12"></div>
                <div class="esnek kolon" style="align-items:flex-start">
                  {ad_html}
                  {alt}
                </div>
                <div class="w12"></div>
                <div class="ikon-kutu c-2">{icon("plus")}</div>
              </button>'''


def grup_basligi(baslik, alt=""):
    alt_html = (f'<div class="h4"></div><div class="pad"><div class="t-cap">{alt}</div></div>'
                if alt else '')
    return f'''            <div class="pad">
              <div class="t-label c-2">{baslik}</div>
            </div>{alt_html}
            <div class="h8"></div>'''


def yigin(satirlar):
    return ('            <div class="pad kolon">\n'
            + '<div class="h8"></div>'.join(satirlar)
            + '\n            </div>')


def isk_satir(genislik):
    return (f'<div class="satir-kart">{isk("44px","44px","16px")}<div class="w12"></div>'
            f'<div class="esnek kolon">{isk(genislik,"16px")}<div class="h8"></div>'
            f'{isk("40%","12px")}</div></div>')


# ---------------------------------------------------------------- kategori
ILK_ALTI = ["Kafe", "Market", "Ulaşım", "Restoran", "Fatura", "Akaryakıt"]


def kategori_seridi(secili="", hata=""):
    """Ürün SEÇİLMEDİĞİNDE görünen yol: frekansa göre sıralı ilk 6 çip +
    tüm kategoriler kapısı. Tek dokunuşta kategori = 3 dokunuşluk yolun ikinci adımı."""
    sira = list(ILK_ALTI)
    if secili and secili not in sira:
        sira = [secili] + sira[:5]
    cipler = []
    for ad in sira:
        s = " secili" if ad == secili else ""
        nokta = ''
        if ad == secili:
            nokta = (f'<div class="nokta" style="background-color:var(--cat-{CATS[ad][1][4:]})"></div>'
                     f'<div class="w8"></div>')
        cipler.append(f'<button class="cip{s}">{nokta}{ad}</button><div class="w8"></div>')
    hata_html = f'<div class="h8"></div><div class="t-cap c-danger">{hata}</div>' if hata else ""
    return f'''            <div class="pad">
              <div class="t-label c-2">Kategori</div>
            </div>
            <div class="h8"></div>
            <div class="yatay-kaydir pad">
              {''.join(cipler)}
              <button class="cip" aria-label="Tüm kategoriler">{icon("chevron-down")}</button>
            </div>
            <div class="pad">{hata_html}</div>'''


def kategori_deger(kategori, basili=False):
    """Ürün SEÇİLDİĞİNDE görünen yol: kategori artık bir seçim değil, dolu bir
    **değer**. Çukur satır + `chevron-down` → tek dokunuşla 13'lük seçici açılır
    (K-050 "dropdown ile değiştirilebilir").

    Nereden geldiği burada DEĞİL, **tutar kuyusunun altında tek cümlede**
    yazılır ("Tutar ve kategori son kaydından geldi. Değiştirebilirsin.") —
    otomatik dolan alanların hepsi tek cümlede toplanır, aynı bilgi iki yerde
    tekrarlanmaz.

    KURAL (tüm yüzeylerde aynı):
      kategori üründen/kayıttan doldu → **değer satırı** (bu bileşen)
      kategoriyi kullanıcı seçiyor    → **çip şeridi** (`kategori_seridi`)
    """
    b = " basili" if basili else ""
    return f'''            <div class="pad">
              <div class="t-label c-2">Kategori</div>
              <div class="h8"></div>
              <button class="kuyu-btn{b}" style="padding:12px 16px"
                      aria-label="Kategori {kategori}, değiştirmek için dokun">
                {kat_kab(kategori)}
                <div class="w12"></div>
                <div class="esnek t-strong">{kategori}</div>
                <div class="w12"></div>
                {icon("chevron-down")}
              </button>
            </div>'''


# -------------------------------------------------------------------- ödeme
def odeme(kart=True, taksit_acik=False):
    """🔴 Varsayılan DAİMA 'Kart' (Ayarlar > Varsayılan ödeme). Tek değer.
    Nakit yalnız kullanıcı seçtiğinde seçilidir (yüzey J) — F-6."""
    n = "" if kart else " secili"
    k = " secili" if kart else ""
    t = " secili" if taksit_acik else ""
    taksit = (f'<div class="w12"></div><button class="cip{t}" style="height:44px">Taksitli</button>'
              if kart else '')
    return f'''            <div class="pad">
              <div class="t-label c-2">Ödeme</div>
              <div class="h8"></div>
              <div class="satir">
                <div class="esnek segment">
                  <button class="segment-btn{n}">{icon("banknote")}<div class="w8"></div>Nakit</button>
                  <button class="segment-btn{k}">{icon("credit-card")}<div class="w8"></div>Kart</button>
                </div>
                {taksit}
              </div>
            </div>'''


def taksit_secici(secili="6", onizleme="Ayda 208,33 ₺ · 6 ay"):
    """K-023: 'Taksitli' çipi → taksit sayısı. Ayrı bir 'Uygula' adımı YOKTUR."""
    c = []
    for n in ["3", "6", "9", "12"]:
        s = " secili" if n == secili else ""
        c.append(f'<button class="cip{s}">{n} taksit</button><div class="w8"></div>')
    return f'''            <div class="h12"></div>
            <div class="pad">
              <div class="t-label c-2">Kaç taksit</div>
            </div>
            <div class="h8"></div>
            <div class="yatay-kaydir pad">
              {''.join(c)}
            </div>
            <div class="h8"></div>
            <div class="pad">
              <div class="t-cap">{onizleme}</div>
            </div>'''


def not_satiri(metin="", hata=""):
    """Gün çipi tutar kuyusuna taşındığı için burada yalnız Not kalır
    (eski "Dün" çipi düştü — gün artık kuyudan ve E-24'ten seçilir)."""
    if metin:
        govde = f'''            <div class="pad">
              <div class="t-label c-2">Not</div>
              <div class="h8"></div>
              <div class="clay-kuyu" style="padding:12px 16px">
                <div class="t-body">{metin}</div>
              </div>
            </div>'''
    else:
        govde = f'''            <div class="pad satir">
              <button class="cip" aria-label="Not ekle">Not</button>
            </div>'''
    hata_html = (f'<div class="h8"></div><div class="pad"><div class="t-cap c-danger">{hata}</div></div>'
                 if hata else '')
    return govde + hata_html


def alt_blok(durum="aktif", basili_tus=""):
    return f'''          <div class="alt-sabit">
{tus_takimi(basili_tus)}
            <div class="h12"></div>
            <div class="pad">{kaydet(durum)}</div>
          </div>'''


def alt_sade(durum="pasif"):
    """Sistem klavyesi açıkken kil tuş takımı düşer; Kaydet klavyenin üstünde kalır."""
    return f'''          <div class="alt-sabit">
            <div class="pad">{kaydet(durum)}</div>
          </div>'''


# ------------------------------------------------------- kategori seçici sheet
def kat_sec_sheet(secili="Kafe"):
    oge = []
    for ad in CATS:
        s = " secili" if ad == secili else ""
        oge.append(f'''<div class="kat-sec-oge"><button class="kat-sec-kutu{s}">
                    {kat_kab(ad)}<div class="h8"></div>
                    <div class="t-label" style="text-align:center">{ad}</div></button></div>''')
    return f'''              <div class="sheet">
                <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
                <div class="h12"></div>
                <div class="aralik">
                  <div class="t-h2">Kategori</div>
                  <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
                </div>
                <div class="h12"></div>
                <div class="kat-sec">{''.join(oge)}</div>
              </div>'''


SON = [("Sütlü kahve", "95 ₺", "cat-amber"),
       ("Marlboro Touch Blue 20'lik", "95 ₺", "cat-duman"),
       ("İstanbulkart", "100 ₺", "cat-mavi"),
       ("Haftalık market", "1.240 ₺", "cat-yesil")]

# ===========================================================================
# A · açılış · arama boş → son kullandıkların
# ===========================================================================
A = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{arama()}
            <div class="h24"></div>
{son_kullanilanlar(SON)}
            <div class="h24"></div>
{kategori_seridi()}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# B · varsayılan · tutar girildi + kategori çipi = 3 dokunuş
# ===========================================================================
B = f'''{basi()}
{tutar_kuyusu("180")}
            <div class="h8"></div>
{arama()}
            <div class="h24"></div>
{kategori_seridi(secili="Market")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# C · arama yazılıyor · kendi geçmişi + katalog
# ===========================================================================
C = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{arama("kah", odakli=True)}
            <div class="h24"></div>
{grup_basligi("Son kullandıkların")}
{yigin([sonuc("Sütlü kahve", "Kafe", gecen="95 ₺")])}
            <div class="h24"></div>
{grup_basligi("Ürünler")}
{yigin([
    sonuc("Filtre kahve", "Kafe"),
    sonuc("Türk kahvesi", "Kafe", basili=True),
    sonuc("Soğuk kahve", "Kafe"),
    sonuc("Kahvaltı tabağı", "Restoran"),
])}
            <div class="h24"></div>'''

# ===========================================================================
# D · arama · marka adı kullanıcıdan, katalog jenerik (K-050 kanıtı)
# ===========================================================================
D = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{arama("sigara", odakli=True)}
            <div class="h24"></div>
{grup_basligi("Son kullandıkların")}
{yigin([sonuc("Marlboro Touch Blue 20'lik", "Alışkanlıklar", gecen="95 ₺")])}
            <div class="h24"></div>
{grup_basligi("Ürünler")}
{yigin([
    sonuc("Sigara paketi", "Alışkanlıklar"),
    sonuc("Sarma tütün", "Alışkanlıklar"),
    sonuc("Nargile", "Alışkanlıklar"),
])}
            <div class="h24"></div>'''

# ===========================================================================
# E · sonuç yok → kendi kalemini ekle (çıkmaz sokak yok)
# ===========================================================================
E = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{arama("fotokopi", odakli=True)}
            <div class="h24"></div>
{yigin([sonuc("", "", yeni=True, arama_metni="fotokopi")])}
            <div class="h24"></div>
{kategori_seridi()}
            <div class="h24"></div>'''

# ===========================================================================
# F · ürün seçildi (kendi geçmişinden) · tutar doldu + kategori değeri
# ===========================================================================
F = f'''{basi()}
{tutar_kuyusu("95", alt_not="Tutar geçen seferkinden geldi. Değiştirebilirsin.")}
            <div class="h8"></div>
{arama(urun="Sütlü kahve")}
            <div class="h24"></div>
{kategori_deger("Kafe")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# G · ürün katalogdan seçildi · tutar YOK (fiyat uydurulmuyor)
# ===========================================================================
G = f'''{basi()}
{tutar_kuyusu("0", alt_not="Tutarı sen yaz. Fiyat tahmini yapmıyoruz.")}
            <div class="h8"></div>
{arama(urun="Döner")}
            <div class="h24"></div>
{kategori_deger("Restoran")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# H · "geçen sefer" önerisi · yazılmış tutarın üzerine yazılmaz
# ===========================================================================
H = f'''{basi()}
{tutar_kuyusu("120", oneri="95 ₺")}
            <div class="h8"></div>
{arama(urun="Sütlü kahve")}
            <div class="h24"></div>
{kategori_deger("Kafe")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# I · kategori seçici açık (13 kategori)
# ===========================================================================
I = f'''{basi()}
{tutar_kuyusu("95")}
            <div class="h8"></div>
{arama(urun="Sütlü kahve")}
            <div class="h24"></div>
{kategori_deger("Kafe", basili=True)}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# J · ödeme · nakit (kullanıcı seçti)
# ===========================================================================
J = f'''{basi()}
{tutar_kuyusu("45", alt_not="Kategori üründen geldi. Değiştirebilirsin.")}
            <div class="h8"></div>
{arama(urun="Simit")}
            <div class="h24"></div>
{kategori_deger("Kafe")}
            <div class="h24"></div>
{odeme(kart=False)}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# K · taksitli (yalnız kart)
# ===========================================================================
K = f'''{basi()}
{tutar_kuyusu("1.250")}
            <div class="h8"></div>
{arama(urun="Kablosuz kulaklık")}
            <div class="h24"></div>
{kategori_seridi(secili="Diğer")}
            <div class="h24"></div>
{odeme(taksit_acik=True)}
{taksit_secici()}
            <div class="h24"></div>'''

# ===========================================================================
# L · geçmiş güne ekleme (K-049)
# ===========================================================================
L = f'''{basi()}
{tutar_kuyusu("260", gun=DUN, vurgu=True)}
            <div class="h8"></div>
{gecmis_gun_seridi()}
            <div class="h8"></div>
{arama()}
            <div class="h24"></div>
{kategori_seridi(secili="Restoran")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# M · hata · iki doğrulama aynı yüzeyde
# ===========================================================================
M = f'''{basi()}
{tutar_kuyusu("0,00", gun="13 Eylül Cuma", vurgu=True, gun_basili=True,
              hata="Tutar sıfırdan büyük olmalı.")}
            <div class="h8"></div>
{arama()}
            <div class="h24"></div>
{kategori_seridi(secili="", hata="Bir kategori seç.")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# N · uzun tutar + uzun ürün adı + uzun not
# ===========================================================================
N = f'''{basi()}
{tutar_kuyusu("1.250.000,50")}
            <div class="h8"></div>
{arama(urun="Marlboro Touch Blue 20'lik · yıllık stok")}
            <div class="h24"></div>
{kategori_seridi(secili="Kira ve ev")}
            <div class="h24"></div>
{not_satiri("Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü")}
            <div class="h24"></div>'''

# ===========================================================================
# O · limit dışı önizleme + kaydediliyor
# ===========================================================================
O = f'''{basi()}
{tutar_kuyusu("240", alt_not="Kategori son kaydından geldi. Değiştirebilirsin.")}
            <div class="h8"></div>
            <div class="pad">
              <div class="serit serit-warn">
                <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap c-warn">Bu harcama günlük limitin 120 ₺ üzerine çıkarır.</div>
              </div>
            </div>
            <div class="h8"></div>
{arama(urun="Haftalık market")}
            <div class="h24"></div>
{kategori_deger("Market")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# P · arama · yükleniyor (iskelet)
# ===========================================================================
P = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{arama("marke", odakli=True, yukleniyor=True)}
            <div class="h24"></div>
{grup_basligi("Ürünler")}
            <div class="pad kolon">
              {isk_satir("62%")}
              <div class="h8"></div>
              {isk_satir("48%")}
              <div class="h8"></div>
              {isk_satir("55%")}
            </div>
            <div class="h24"></div>'''

# ===========================================================================
# Q · kayıt yazılamadı · form olduğu gibi duruyor
# ===========================================================================
Q_TOAST = f'''          <div class="katman-bas">
            <div class="h8"></div>
            <div class="pad">
              <div class="toast">
                <div class="nokta" style="background-color:var(--primary)"></div>
                <div class="w12"></div>
                <div class="esnek t-body">Kayıt yazılamadı. Yeniden dene.</div>
              </div>
            </div>
          </div>
'''

Q = f'''{basi()}
{tutar_kuyusu("95", alt_not="Tutar ve kategori son kaydından geldi. Değiştirebilirsin.")}
            <div class="h8"></div>
{arama(urun="Sütlü kahve")}
            <div class="h24"></div>
{kategori_deger("Kafe")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

units = "".join([
    device("HARCAMA EKLE", "açılış · arama boş · son kullandıkların", A,
           "<b>Sheet açıldığı an:</b> odak <b>tutarda</b>, kil tuş takımı hazır — arama alanı "
           "<b>odaklı değil</b> ve tutarın <b>altında</b>. Ürün arama eklemek varsayılan yolu "
           "uzatmadı, çünkü aramayı isteyen kullanıcı ona <b>uzanır</b>; istemeyen görmezden gelir. "
           "Placeholder zorunlu olmadığını söylüyor: \"Ne aldın? (isteğe bağlı)\". "
           "<b>Son kullandıkların</b> şeridindeki tutar <b>katalog fiyatı değil</b>, kullanıcının "
           "kendi son kaydıdır (K-050) — başlık bunu söyler. Kaydet <b>pasif</b>: tutar 0 iken "
           "kaydedilecek bir şey yok, bu yüzden \"Tutar boş kalamaz\" hatası hiç doğmaz. "
           "Gün, <b>tutar kuyusunun içinde</b> dokunulabilir bir çip: kaydın günü kaydın tutarıyla "
           "aynı yerde durur (K-049).",
           sabit_alt=alt_blok("pasif")),

    device("HARCAMA EKLE", "varsayılan · 3 dokunuş tamam", B,
           "<b>3 dokunuş:</b> [1] FAB · [2] kategori çipi · [3] Kaydet. Rakam tuşları veri girişidir, "
           "sayılmaz. <b>İlk rakam girilince Son kullandıkların şeridi kapandı</b> ve Kategori "
           "şeridi yukarı taşındı: 3 dokunuşluk yol <b>kaydırma gerektirmiyor</b>. Kapanmanın ikinci "
           "sebebi: girilmiş tutarın üzerine yazan bir kısayol tuzağa dönüşür. Arama alanı boş kaldı "
           "ve akışa hiç karışmadı — isteğe bağlı alan, isteğe bağlı davranır.",
           sabit_alt=alt_blok("aktif", basili_tus="8")),

    device("HARCAMA EKLE", "arama · kendi geçmişi + katalog", C,
           "<b>İki grup, tek biçim:</b> önce kullanıcının kendi kayıtları, sonra katalog. Ayrım "
           "<b>ikinci satırda</b>: kendi kaydında \"Kafe · geçen sefer 95 ₺\", katalogda yalnız "
           "\"Kafe\". <b>Sağda tutar sütunu yok</b> — fiyat sütunu, olmayan bir otoriteyi ima "
           "ederdi (K-050). Kategori adı her satırda yazılı: ürün seçilince kategorinin <b>neden</b> "
           "dolduğu önceden görünür. Metin klavyesi işletim sistemininkidir; kil tuş takımı yalnız "
           "rakama aittir, ikisi karışmaz. Klavye açıkken <b>Kaydet yerinde kalır</b> (pasif).",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "arama · marka adı kullanıcıdan gelir", D,
           "<b>K-050'nin en görünür sonucu.</b> Katalog <b>jenerik</b> kalem taşır (\"Sigara paketi\"), "
           "marka adı <b>kullanıcının kendi geçmişinden</b> gelir (\"Marlboro Touch Blue 20'lik\") ve "
           "fiyatı da onun kendi kaydıdır. Eski gömülü <b>tütün fiyat listesi kaldırıldı</b>: zamla "
           "eskiyen bir fiyatı \"ön-dolgu\" diye göstermek güveni tek seferde bitirir. Listenin "
           "<b>nereden geldiği anlatılmaz</b> — teknik açıklama arayüz metni değildir.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "sonuç yok · kendi kalemini ekle", E,
           "<b>Çıkmaz sokak yok.</b> Bu bir boş durum ya da hata değil, normal bir yol: illüstrasyon, "
           "kırmızı, \"bulunamadı\" ve ünlem yok. Yazdığı ad <b>diğer sonuçlarla aynı biçimde</b> "
           "seçilebilir bir satır olur; tek fark <b>nötr ikon kabı</b> (kategori rengi taşımaz, çünkü "
           "kategori henüz yok) ve ikinci satırın ne yapacağını söylemesi. Hemen altında <b>Kategori "
           "şeridi</b> duruyor: kullanıcı aramayı bırakıp iki adımlık yola geri dönebilir.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "ürün seçildi · kendi geçmişinden", F,
           "<b>En büyük hız kazancı:</b> tek dokunuş ürün + kategori + <b>kendi son tutarını</b> "
           "getirdi; sheet içi adım 3 → 1, tuş vuruşu ~4 → 0. Ve <b>söylenir</b>: \"Tutar geçen "
           "seferkinden geldi. Değiştirebilirsin.\" Kategori artık bir <b>seçim değil değer</b>: çip "
           "şeridi yerine tek satırlık <b>çukur değer + chevron</b> geldi, tek dokunuşla 13'lük "
           "seçici açılır (K-050 dropdown). Tuş takımı yerinde: tutar hâlâ düzenlenebilir.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "ürün katalogdan · tutar boş", G,
           "<b>Katalogda fiyat yok, uydurulmuyor</b> (K-050): \"Tutarı sen yaz. Fiyat tahmini "
           "yapmıyoruz.\" Kategori üründen doldu (Döner → Restoran), tutar 0 kaldı ve odak tuş "
           "takımında. Bu, ürün aramanın <b>ne olduğunu</b> tek yüzeyde anlatan durum: bir fiyat "
           "kaynağı değil, <b>kategori + ad kısayolu</b>. Kaydet pasif, çünkü tutar hâlâ 0.",
           sabit_alt=alt_blok("aktif", basili_tus="5")),

    device("HARCAMA EKLE", "geçen sefer önerisi · üzerine yazmaz", H,
           "<b>Sıra tersine döndüğünde:</b> kullanıcı önce 120 yazdı, sonra ürünü seçti. Uygulama "
           "girilmiş tutarı <b>sessizce değiştirmez</b> — kendi son tutarını <b>teklif eder</b>: "
           "\"Geçen sefer 95 ₺\" çipi, tek dokunuşla kabul. Ekran okuyucu tam cümleyi okur: "
           "\"Geçen sefer ödediğin 95 ₺ tutarını kullan.\" Bu, K-050'nin izin verdiği tek fiyat "
           "bilgisinin doğru biçimidir: <b>kullanıcının kendi verisi, kullanıcının onayıyla.</b>",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "kategori seçici · 13 kategori", I,
           "<b>Dropdown'ın açtığı yüzey:</b> 13 kategori, 6 renk ailesi — ayrım <b>ikon + ad</b> ile, "
           "yalnız renkle değil. Seçili kutu kabarık değil <b>çukur</b>; onay ikonu ve halka yok "
           "(K-040). Arkada kategori satırı <b>basılı</b> duruyor: RN'de hover olmadığı için "
           "kullanıcının tek geri bildirimi budur. Ürün adı ve kategori <b>ayrı alanlardır</b>; "
           "biri diğerinin yerine geçmez.",
           sabit_alt=f'<div class="katman-ust"><div class="scrim-kat"></div>{kat_sec_sheet()}</div>'),

    device("HARCAMA EKLE", "ödeme · nakit (kullanıcı seçti)", J,
           "<b>F-6 nakit/kart ayrımı.</b> Varsayılan <b>daima Kart</b>; bu yüzeyde nakit <b>seçili</b> "
           "çünkü kullanıcı dokundu — varsayılan değişmedi. Segment <b>çukur oluk + kabarık seçili "
           "düğme</b>: fiziksel bir anahtar gibi, iki değerden hangisinin açık olduğu tek bakışta "
           "belli. Nakitte <b>Taksitli çipi görünmez</b>: nakit taksit diye bir şey yok, pasif bir "
           "düğme göstermek yerine kaldırdık.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "taksitli · +2 dokunuş", K,
           "<b>Taksit yolu +2 dokunuş</b> (K-023): \"Taksitli\" çipi → taksit sayısı. <b>Ayrı bir "
           "\"Uygula\" adımı yoktur</b>, sayıya dokunmak seçimi bitirir. Altında aylık karşılığı "
           "yazar (\"Ayda 208,33 ₺ · 6 ay\") — kullanıcı bölmeyi kafasında yapmaz. Kategori kaynağı "
           "dürüst: <b>ürün listede yoktu</b>, kategoriyi kullanıcı seçti; satır bunu yazıyor.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "geçmiş güne ekleme (K-049)", L,
           "<b>Yanlış güne kayıt en sinir bozucu hatadır</b>, bu yüzden gün <b>iki kez</b> söylenir: "
           "tutar kuyusundaki çip <b>vurgulu</b> (primary-soft + nokta) ve altında şerit — \"Bu kayıt "
           "16 Eylül'e yazılacak.\" <b>Amber ve kırmızı kullanılmadı:</b> tokens §1.5'e göre amber "
           "yalnız <b>limit dışı</b> sinyalidir ve daima o sözcükle gelir; geçmiş gün bir hata değil, "
           "istenen bir durumdur. Bu yüzeye çoğunlukla <b>Günlük'te o güne kaydırıp \"+\"ya basarak</b> "
           "gelinir — tarih hazır gelir, kullanıcı ayarlamaz, yalnız <b>doğrular</b>.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "hata · iki doğrulama", M,
           "<b>Matristeki iki hata aynı yüzeyde:</b> <b>0 ₺</b> ve <b>kategori yok</b>. \"Boş tutar\" "
           "satırı <b>çizilmez çünkü oluşamaz</b>: tutar boşken Kaydet pasiftir (yüzey A), hata hiç "
           "doğmaz — önlemek uyarmaktan iyidir. Her hata <b>kendi alanının altında</b>; tepede toplu "
           "hata kutusu yok. Kuyu 2pt <code>danger</code> çerçeve alır. Gün çipi <b>basılı</b>: "
           "kullanıcı tarihi düzeltmeye gidiyor. \"Geçersiz\", \"Hata:\", ünlem ve büyük harf yok. "
           "Kaydet <b>pasifleşmez</b>: kullanıcı düzeltip yeniden basar.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "uzun tutar · uzun ad · uzun not", N,
           "<b>En uzun tutar</b> (1.250.000,50 ₺) 56pt'ye sığmadığı için rol <b>bir basamak iner</b>: "
           "hero 56 → display 32 (tokens §7.11). Keyfi ara punto üretilmez, kuyu yüksekliği sabit "
           "kalır. Uzun ürün adı arama alanında <b>tek satıra kırpılır</b>, alan büyümez. 60 "
           "karakterli not <b>çukur kutuda</b> iki satıra sarar — not okunmak için yazılır, "
           "kırpılmaz; sarması gereken tek metin odur.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "limit dışı önizleme · kaydediliyor", O,
           "<b>Kaydetmeden önce</b> bilgilendirir, engellemez: amber şerit, kırmızı değil, ünlem yok — "
           "limit aşımı yıkıcı bir işlem değildir, <code>danger</code> görmez. Şerit <b>\"limit dışı\" "
           "bağlamının</b> tek amber kullanımıdır, kategori amberiyle (Kafe/Restoran çipi) aynı "
           "yüzeyde kesişmez. Kaydet <b>loading</b>: metin \"Kaydediliyor\", genişlik sabit, opaklık "
           "yok, ekran kilitlenmez.",
           sabit_alt=alt_blok("loading")),

    device("HARCAMA EKLE", "arama · yükleniyor (iskelet)", P,
           "<b>Yükleniyor durumu iskelettir</b> (tokens §7.10): gerçek düzenin kutuları yerinde durur, "
           "içleri <b>çukur</b> bloklara döner. Parıldayan süpürme ve tam ekran spinner yok; tek "
           "spinner <b>arama alanının içinde</b>, 20pt ve koyu varyant (beyaz halka açık zeminde "
           "görünmez). Sonuçlar ertelenirse <b>kaç satır geleceği</b> önceden bellidir, ekran "
           "zıplamaz. Kaydet pasif kalır: tutar hâlâ 0.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "kayıt yazılamadı · form duruyor", Q,
           "<b>Yazma hatası formu silmez.</b> Tutar, ürün, kategori ve ödeme <b>olduğu gibi</b> "
           "yerinde; kullanıcı yeniden Kaydet'e basar. Bildirim <b>toast</b>: üstte, 8pt mavi bilgi "
           "noktası, 4 sn. Modal değil — kullanıcıyı onay istemeye zorlamak kaybettiği kaydı geri "
           "getirmez. Metin <b>ne olduğunu değil ne yapacağını</b> söyler: \"Kayıt yazılamadı. "
           "Yeniden dene.\" Depolama/mimari sözcüğü geçmez.",
           sabit_alt=alt_blok("aktif") + Q_TOAST),
])

OUT.write_text(page(
    "Trinkow · Harcama ekle — prototip v4",
    "E-11 · Harcama ekle · ürün arama (T-4)",
    "Arketip E — Checkout / form · sekme çubuğu düşer · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
