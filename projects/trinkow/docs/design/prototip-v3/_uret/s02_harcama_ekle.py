# -*- coding: utf-8 -*-
"""E-11 · Harcama ekle — arketip E (Checkout / form). Sekme çubuğu düşer.
Mood: tek işe kilitli, alt yarısı tuş takımıyla dolu, hızlı.

DOKUNUŞ BÜTÇESİ (ekran-envanteri §4 · ölçüm: rakam/harf tuşları sayılmaz)
  Varsayılan yol : [1] FAB → [2] kategori çipi → [3] Kaydet          = 3
  Sık alınan yolu: [1] FAB → [2] öneri çipi   → [3] Kaydet           = 3
                   (sheet içi adım 3 → 2; tuş vuruşu ~4 → 0)
  Ürün arama yolu: [1] FAB → [2] ürün alanı → [3] öneri → [4] Kaydet = 4
                   (yalnız listede olmayan / adı önemli ürünler için)

🔴 KATEGORİ ÖNCEDEN SEÇİLİ GELMEZ (ekran-envanteri §4, onaylı karar).
Tahmin etmek 1 dokunuş kazandırırdı ama yanlış kategoriye sessizce kayıt
riski doğururdu; marka *Dürüst*. Kategori yalnız kullanıcının kendi
geçmişinden gelen bir öneri seçildiğinde dolar — çünkü o zaman tahmin
değil, kullanıcının kendi kaydıdır.

🔴 VARSAYILAN ÖDEME TİPİ = "Kart" (tokens/ekran-envanteri §4, tek değer).

ÜRÜN ADI (K-033): opsiyoneldir ve varsayılan akışı UZATMAZ. Veri modeli
ayrı alanlardır: ürün adı · tutar · tarih (serbest metin değil).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, kat_kab, CATS, tus_takimi, kaydet

OUT = pathlib.Path(__file__).parent.parent / "02-harcama-ekle.html"

# ---------------------------------------------------------------------------
# TÜTÜN FİYAT LİSTESİ — kaynak/tarih notu KULLANICIYA GÖSTERİLMEZ
#   Kaynak   : üreticilerin kamuya açık bayi liste fiyatları
#              (Philip Morris TR · JTI TR · BAT TR · TEKEL).
#   Liste tarihi: 2026-09-12  (prototip örnek verisi)
#   Uygulamada bu iki alan `assets/tutun-listesi.json` içindeki
#   `kaynak` ve `liste_tarihi` alanlarına yazılır; arayüzde gösterilmez.
#   TR'de tütün ULUSAL TEK FİYATtır → sunucu/API gerekmez, liste pakete gömülür.
#   🔴 ZAMLA ESKİR: fiyat yalnızca ÖN-DOLGUdur, her zaman düzenlenebilir.
#      Arayüzde "güncel fiyat" / "resmi fiyat" iddiası YAZILMAZ.
#   Ürün adı listeden gelse de kullanıcının kaydına AYRI ALAN olarak yazılır
#   (backlog Ü-5: ileride kendi fiyat verimizi toplarsak dönüşüm gerekmesin).
# ---------------------------------------------------------------------------
TUTUN = [
    ("Marlboro Touch Blue", "20'lik paket", "95 ₺"),
    ("Marlboro Touch", "20'lik paket", "95 ₺"),
    ("Marlboro Red", "20'lik paket", "95 ₺"),
    ("Marlboro Double Fusion", "20'lik paket", "95 ₺"),
]


def basi():
    return f'''            <div class="ekran-basi">
              <div class="t-h1">Harcama ekle</div>
              <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
            </div>'''


def tutar_kuyusu(sayi, buyuk=None, hata="", tarih="Bugün", alt_not=""):
    # tokens.md §7.11: tutar 7 karakteri aşarsa (8+) `hero` -> `display` iner.
    # Elle geçilmediği sürece ölçek uzunluktan otomatik hesaplanır; prototip
    # ile tokens.md'nin ayrışmasını (K-042) tekrarlamamak için tek yerde karar verilir.
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
    return f'''            <div class="pad">
              <div class="{kuyu}" style="padding:16px">
                <div class="aralik">
                  <div class="t-label c-2">Tutar</div>
                  <div class="t-cap">{tarih}</div>
                </div>
                <div class="h8"></div>
                <div class="satir" style="justify-content:center;align-items:baseline">
                  <div class="{cls}">{sayi}</div>
                  <div class="imlec"></div>
                  <div class="w8"></div>
                  <div class="{simge} c-2">₺</div>
                </div>
              </div>
              {ek}
            </div>'''


# --------------------------------------------------------------- ürün alanı
def urun_alani(deger="", odakli=False):
    """Opsiyonel ürün adı. Boşken akışa hiç karışmaz: odaklanmaz, hata
    üretmez, Kaydet'i engellemez. Veri modelinde kendi alanıdır."""
    o = " odakli" if odakli else ""
    if deger:
        ic = (f'<div class="esnek t-body tek-satir">{deger}</div>'
              + ('<div class="imlec"></div>' if odakli else '')
              + f'<div class="w8"></div>'
              f'<button class="ikon-btn" aria-label="Ürün adını temizle">{icon("x")}</button>')
    else:
        ic = '<div class="esnek t-body c-2 tek-satir">Ne aldın? (isteğe bağlı)</div>'
    return f'''            <div class="pad">
              <div class="giris{o}" aria-label="Ürün adı, isteğe bağlı">
                {ic}
              </div>
            </div>'''


def sik_cipler(items):
    """Yazmadan görünen kısa yol. Tutar 0 iken durur, ilk rakam girilince
    kapanır: girilmiş bir tutarın üzerine sessizce yazan çip tuzaktır.

    TAŞMA (tokens §7.6): ürün adları uzun olabilir ("Marlboro Touch Blue
    20'lik"). Çip **tek satırda** kalır, sarmaz; uzun ad `cip-ad` içinde
    ellipsis ile kırpılır, tutar `cip-tutar` ile **hiç kırpılmaz** — `₺`
    okunmazsa çip karar vermeye yaramaz. Tam ad, çip seçildikten sonra
    ürün alanında görünür.
    """
    c = []
    for ad, tutar, renk in items:
        c.append(f'<button class="cip" aria-label="{ad}, {tutar}">'
                 f'<div class="nokta" style="background-color:var(--{renk})"></div>'
                 f'<div class="w8"></div><div class="cip-ad">{ad}</div>'
                 f'<div class="w8"></div><div class="cip-tutar">· {tutar}</div>'
                 f'</button><div class="w8"></div>')
    return f'''            <div class="pad">
              <div class="t-label c-2">Sık alınanlar</div>
            </div>
            <div class="h8"></div>
            <div class="yatay-kaydir pad">
              {''.join(c)}
            </div>'''


# ------------------------------------------------------------- öneri paneli
def oneri_satiri(ad, alt, tutar, kategori="Alışkanlıklar", basili=False,
                 yeni=False):
    b = " basili" if basili else ""
    kab = (f'<div class="kat-kab kat-duman">{icon("plus")}</div>' if yeni
           else kat_kab(kategori))
    sag = (f'<div class="w12"></div><div class="t-amount">{tutar}</div>'
           if tutar else '')
    return f'''              <button class="satir-kart{b}" style="width:100%">
                {kab}
                <div class="w12"></div>
                <div class="esnek kolon" style="align-items:flex-start">
                  <div class="t-body tek-satir">{ad}</div>
                  <div class="t-cap tek-satir">{alt}</div>
                </div>
                {sag}
              </button>'''


def grup_basligi(baslik, alt=""):
    alt_html = (f'<div class="h4"></div><div class="pad"><div class="t-cap">{alt}</div></div>'
                if alt else '')
    return f'''            <div class="pad">
              <div class="t-label c-2">{baslik}</div>
            </div>{alt_html}
            <div class="h8"></div>'''


def panel(*bloklar):
    return "".join(bloklar)


def satir_yigini(satirlar):
    return ('            <div class="pad kolon">\n'
            + '<div class="h8"></div>'.join(satirlar)
            + '\n            </div>')


# ------------------------------------------------------------------ kategori
ILK_ALTI = ["Kafe", "Market", "Ulaşım", "Restoran", "Fatura", "Akaryakıt"]


def kategori_seridi(secili="", hata=""):
    """Frekansa göre sıralı ilk 6 çip. Seçili kategori listede yoksa
    (öneriden geldiyse) en sola alınır — kullanıcı ne seçildiğini
    kaydırmadan görür."""
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


# -------------------------------------------------------------------- ödeme
def odeme(kart=True, taksit_acik=False):
    """🔴 Varsayılan DAİMA 'Kart' (Ayarlar > Varsayılan ödeme). Tek değer."""
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
    """K-023: 'Taksitli' çipi → taksit sayısı. Ayrı bir 'Uygula' adımı YOKTUR;
    sayıya dokunmak seçimi bitirir. Toplam yol: +2 dokunuş."""
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


def not_satiri(dun=False, tarih_cip="", hata=""):
    d = " secili" if dun else ""
    ilk = (f'<button class="cip secili"><div class="nokta"></div><div class="w8"></div>{tarih_cip}</button>'
           if tarih_cip else
           f'<button class="cip{d}" aria-label="Tarihi dün yap">Dün</button>')
    hata_html = (f'<div class="h8"></div><div class="pad"><div class="t-cap c-danger">{hata}</div></div>'
                 if hata else '')
    return f'''            <div class="pad satir">
              {ilk}
              <div class="w8"></div>
              <button class="cip" aria-label="Not ekle">Not</button>
            </div>{hata_html}'''


def alt_blok(durum="aktif", basili_tus=""):
    return f'''          <div class="alt-sabit">
{tus_takimi(basili_tus)}
            <div class="h12"></div>
            <div class="pad">{kaydet(durum)}</div>
          </div>'''


def alt_sade(durum="pasif"):
    """Metin klavyesi açıkken tuş takımı düşer; Kaydet klavyenin üstünde kalır."""
    return f'''          <div class="alt-sabit">
            <div class="pad">{kaydet(durum)}</div>
          </div>'''


SIK = [("Sütlü kahve", "95 ₺", "cat-amber"),
       ("Marlboro Touch Blue 20'lik", "95 ₺", "cat-duman"),
       ("İstanbulkart", "100 ₺", "cat-mavi")]

# ===========================================================================
# A · boş / açılış — varsayılan 3 dokunuşun başlangıcı
# ===========================================================================
A = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{urun_alani()}
            <div class="h8"></div>
{sik_cipler(SIK)}
            <div class="h24"></div>
{kategori_seridi()}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# B · varsayılan · tutar girildi, kategori seçildi
# ===========================================================================
B = f'''{basi()}
{tutar_kuyusu("180")}
            <div class="h8"></div>
{urun_alani()}
            <div class="h24"></div>
{kategori_seridi(secili="Market")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# C · ürün adı yazılıyor → kullanıcının kendi geçmişi
# ===========================================================================
C = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{urun_alani("sütlü", odakli=True)}
            <div class="h24"></div>
{grup_basligi("Sık alınanlar")}
{satir_yigini([
    oneri_satiri("Sütlü kahve", "Kafe · en son dün", "95 ₺", "Kafe"),
    oneri_satiri("Sütlü Nesquik 500 ml", "Market · en son 4 Eylül", "68 ₺", "Market"),
    oneri_satiri("Sütlaç", "Restoran · en son 28 Ağustos", "140 ₺", "Restoran"),
])}
            <div class="h24"></div>'''

# ===========================================================================
# D · ürün adı yazılıyor → gömülü tütün listesi eşleşmesi
# ===========================================================================
D = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{urun_alani("marl", odakli=True)}
            <div class="h24"></div>
{grup_basligi("Sık alınanlar")}
{satir_yigini([
    oneri_satiri("Marlboro Touch Blue 20'lik", "Alışkanlıklar · en son dün", "95 ₺", basili=True),
])}
            <div class="h24"></div>
{grup_basligi("Sigara ve tütün", "Fiyatı sonra değiştirebilirsin.")}
{satir_yigini([oneri_satiri(ad, alt, fiyat) for ad, alt, fiyat in TUTUN])}
            <div class="h24"></div>'''

# ===========================================================================
# E · eşleşme yok → manuel giriş (hata DEĞİL, normal yol)
# ===========================================================================
E = f'''{basi()}
{tutar_kuyusu("0")}
            <div class="h8"></div>
{urun_alani("fotokopi", odakli=True)}
            <div class="h24"></div>
{satir_yigini([
    oneri_satiri("“fotokopi” olarak kaydet", "Tutarı ve kategoriyi sen seç.", "", yeni=True),
])}
            <div class="h24"></div>'''

# ===========================================================================
# F · öneri seçildi → tutar + kategori doldu
# ===========================================================================
F = f'''{basi()}
{tutar_kuyusu("95", alt_not="Tutar ve kategori son kaydından geldi. Değiştirebilirsin.")}
            <div class="h8"></div>
{urun_alani("Marlboro Touch Blue 20'lik")}
            <div class="h24"></div>
{kategori_seridi(secili="Alışkanlıklar")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# G · kategori seçici (13 kategori)
# ===========================================================================
def kat_sec_sheet(secili="Restoran"):
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


G = f'''{basi()}
{tutar_kuyusu("1.250,50")}
            <div class="h8"></div>
{urun_alani("Akşam yemeği")}
            <div class="h24"></div>
{kategori_seridi(secili="Restoran")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# H · taksit açık (özel durum)
# ===========================================================================
H = f'''{basi()}
{tutar_kuyusu("1.250")}
            <div class="h8"></div>
{urun_alani("Kablosuz kulaklık")}
            <div class="h24"></div>
{kategori_seridi(secili="Diğer")}
            <div class="h24"></div>
{odeme(taksit_acik=True)}
{taksit_secici()}
            <div class="h24"></div>
{not_satiri()}
            <div class="h24"></div>'''

# ===========================================================================
# I · hata · üç doğrulama aynı anda
# ===========================================================================
I = f'''{basi()}
{tutar_kuyusu("0,00", hata="Tutar sıfırdan büyük olmalı.", tarih="13 Eylül Cuma")}
            <div class="h8"></div>
{urun_alani()}
            <div class="h24"></div>
{kategori_seridi(secili="", hata="Bir kategori seç.")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>
{not_satiri(tarih_cip="13 Eylül", hata="Gelecek tarihe harcama yazılamaz.")}
            <div class="h24"></div>'''

# ===========================================================================
# J · en uzun tutar
# ===========================================================================
J = f'''{basi()}
{tutar_kuyusu("1.250.000,50")}
            <div class="h8"></div>
{urun_alani("Ödenen kira ve aidat")}
            <div class="h24"></div>
{kategori_seridi(secili="Kira ve ev")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''

# ===========================================================================
# K · limit dışı önizleme + kaydediliyor
# ===========================================================================
K = f'''{basi()}
{tutar_kuyusu("240")}
            <div class="h8"></div>
            <div class="pad">
              <div class="serit serit-warn">
                <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap c-warn">Bu harcama günlük limitin 120 ₺ üzerine çıkarır.</div>
              </div>
            </div>
            <div class="h8"></div>
{urun_alani("Haftalık market")}
            <div class="h24"></div>
{kategori_seridi(secili="Market")}
            <div class="h24"></div>
{odeme()}
            <div class="h24"></div>'''


units = "".join([
    device("HARCAMA EKLE", "boş · açılış · 3 dokunuşun başı", A,
           "<b>Sheet açıldığı an:</b> tutar alanı odaklı, kil tuş takımı hazır — alana dokunmak gerekmez. "
           "<b>Kategori seçimsizdir</b> (onaylı karar): tahmin 1 dokunuş kazandırırdı ama yanlış kategoriye "
           "sessizce kayıt riski doğururdu. Ödeme <b>Kart</b> — Ayarlar'daki tek varsayılan. "
           "Kaydet <b>pasif</b>: tutar 0 iken kaydedilecek bir şey yok; bu yüzden \"Tutar boş kalamaz\" "
           "hatası hiç gösterilmez, buton zaten basılamaz. <b>Sık alınanlar</b> yazmayı gerektirmez. "
           "<b>Çip taşma kuralı</b> (tokens §7.6): çip tek satırda kalır, sarmaz. Uzun ürün adı "
           "120pt'ta ellipsis ile kırpılır (\"Marlboro Touch Blue 20'lik\" → \"Marlboro Touch B…\"), "
           "tutar hiç kırpılmaz. Tam ad çipe dokunulunca ürün alanında görünür; ekran okuyucu tam adı okur.",
           sabit_alt=alt_blok("pasif")),

    device("HARCAMA EKLE", "varsayılan · 3 dokunuş tamam", B,
           "<b>3 dokunuş:</b> [1] FAB · [2] kategori çipi · [3] Kaydet. Rakam tuşları veri girişidir, "
           "sayılmaz. <b>Sık alınanlar şeridi kapandı:</b> tutar girildikten sonra bir çipe dokunmak "
           "girilmiş tutarın üzerine yazardı — kısa yol tuzağa dönerdi. Ürün adı boş kaldı ve akışa hiç "
           "karışmadı: opsiyonel alan, opsiyonel davranır.",
           sabit_alt=alt_blok("aktif", basili_tus="8")),

    device("HARCAMA EKLE", "ürün adı yazılıyor · sık alınanlar", C,
           "<b>Öneriler kullanıcının kendi geçmişinden gelir</b>, tahminden değil: her satır gerçekten "
           "yazdığı bir kayıttır, ne zaman yazdığı da görünür. Metin klavyesi işletim sistemininkidir — "
           "kil tuş takımı yalnız rakama aittir, ikisi karışmaz. Klavye açıkken <b>Kaydet yerinde kalır</b> "
           "(pasif, çünkü tutar hâlâ 0). Öneri satırları kabarıktır: kabarık = seçilebilir.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "ürün adı yazılıyor · tütün eşleşmesi", D,
           "<b>Önce kullanıcının kendi kaydı, sonra liste.</b> İlk satır basılı durumda. Fiyatlar "
           "<b>ön-dolgudur</b>: \"Fiyatı sonra değiştirebilirsin.\" — \"güncel fiyat\" iddiası hiçbir yerde "
           "geçmez, çünkü liste zamla eskir ve uygulama yalan söylemez. Listenin <b>nereden geldiği "
           "anlatılmaz</b>: kullanıcı bunu bilmek zorunda değil, teknik açıklama arayüz metni değildir.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "eşleşme yok · manuel giriş", E,
           "<b>Bu bir boş durum ya da hata değil, normal bir yol.</b> Bu yüzden illüstrasyon, kırmızı, "
           "\"bulunamadı\" ve ünlem yok: yazdığı ad, seçilebilir tek satır olarak <b>diğer önerilerle aynı "
           "biçimde</b> karşısına çıkar. Tek fark ikon kabı (artı) ve ikinci satırın ne yapacağını "
           "söylemesi. Kullanıcı listede olmayan bir şey aldığı için cezalandırılmaz.",
           sabit_alt=alt_sade(), klavye=True),

    device("HARCAMA EKLE", "öneri seçildi · sheet içi 2 adım", F,
           "<b>Akış kısaldı:</b> sheet içi adım 3 → 2 (öneri · Kaydet) ve tuş vuruşu ~4 → 0. Kategori burada "
           "<b>dolu gelir</b> ve bu A1 kararıyla çelişmez: bu bir tahmin değil, kullanıcının kendi kaydından "
           "gelen bir kopyadır — ve <b>söylenir</b>: \"Tutar ve kategori son kaydından geldi.\" Kategori "
           "<b>Alışkanlıklar</b> ilk altıda olmadığı için şeridin en soluna alındı; kullanıcı ne seçildiğini "
           "kaydırmadan görür. Tuş takımı geri gelir: tutar hâlâ düzenlenebilir.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "kategori seçici · 13 kategori", G,
           "<b>Kategori seçici:</b> 13 kategori, 6 renk ailesi — ayrım <b>ikon + ad</b> ile, yalnız renkle "
           "değil. Seçili kutu kabarık değil <b>çukur</b>: ayrıca onay ikonu gerekmiyor. Ürün adı "
           "(\"Akşam yemeği\") kategoriden bağımsız ayrı bir alandır; biri diğerinin yerine geçmez.",
           sabit_alt=f'<div class="katman-ust"><div class="scrim-kat"></div>{kat_sec_sheet()}</div>'),

    device("HARCAMA EKLE", "özel durum · taksit açık", H,
           "<b>Taksit yolu +2 dokunuş</b> (K-023): \"Taksitli\" çipi → taksit sayısı. <b>Ayrı bir \"Uygula\" "
           "adımı yoktur</b>, sayıya dokunmak seçimi bitirir. Hemen altında aylık karşılığı yazar "
           "(\"Ayda 208,33 ₺ · 6 ay\") — kullanıcı bölmeyi kafasında yapmaz. Taksit yalnız <b>Kart</b> "
           "seçiliyken görünür: nakit taksit diye bir şey yok.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "hata · üç doğrulama", I,
           "<b>Matristeki üç hata aynı yüzeyde:</b> <b>0 ₺</b> · <b>gelecek tarih</b> · ve dördüncü olarak kategori yok. Matrisin \"boş tutar\" satırı burada <b>çizilmez çünkü oluşamaz</b>: tutar boşken Kaydet pasiftir (yüzey 1), hata hiç doğmaz — önlemek uyarmaktan iyidir. Her hata <b>kendi alanının "
           "altında</b> durur, tepede toplu bir hata kutusu yoktur. Kuyu 2pt <code>danger</code> çerçeve "
           "alır. \"Geçersiz\", \"Hata:\", ünlem ve büyük harf yok. Kaydet <b>pasifleşmez</b>: kullanıcı "
           "düzeltip yeniden basar, buton kaybolup onu kilitlemez.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "özel durum · en uzun tutar", J,
           "<b>En uzun tutar</b> (1.250.000,50 ₺) 56pt'ye sığmadığı için rol <b>bir basamak iner</b>: "
           "hero 56 → display 32. Keyfi ara punto üretilmez, düzen kaymaz. Ürün adı da uzun "
           "(\"Ödenen kira ve aidat\") ve tek satıra kırpılır — alan büyümez, ekran zıplamaz.",
           sabit_alt=alt_blok("aktif")),

    device("HARCAMA EKLE", "limit dışı önizleme · kaydediliyor", K,
           "<b>Kaydetmeden önce</b> bilgilendirir, engellemez: amber şerit, kırmızı değil, ünlem yok — "
           "limit aşımı yıkıcı bir işlem değildir, <code>danger</code> görmez. Kaydet <b>loading</b>: "
           "metin \"Kaydediliyor\", genişlik sabit, opaklık yok, ekran kilitlenmez.",
           sabit_alt=alt_blok("loading")),
])

OUT.write_text(page(
    "Trinkow · Harcama ekle — prototip v3",
    "E-11 · Harcama ekle",
    "Arketip E — Checkout / form · sekme çubuğu düşer · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
