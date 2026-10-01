# -*- coding: utf-8 -*-
"""E-18 · Taksitler — arketip D (Zaman çizelgesi / yük haritası).

Mood: YÜK HARİTASI. Bu ekranın tek işi şudur: **bugünün parasıyla
geleceğin kaç ayını rehin verdin?** Bu yüzden ağırlık merkezi liste değil,
üstteki **ay şeridi**dir: her ay bir çubuk, çubuklar birbirine göre okunur.

Diğer ekranlardan ayrıldığı yer: burada sayı "kalan" değil "gelecek".
E-10 bugüne, E-16 geçen haftaya bakar; E-18 tek ileri bakan yüzeydir.
Yorum yapılmaz ("çok taksit yapmışsın" denmez), yük gösterilir.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, push_basi, kat_kab, isk

OUT = pathlib.Path(__file__).parent.parent / "10-taksitler.html"


# --------------------------------------------------------------- ay şeridi
def ay_satiri(ay, tutar, oran, bu_ay=False):
    """Ay adı · çubuk · tutar. Çubuklar aynı ölçeği paylaşır (en yüklü ay
    %100), böylece 'gelecek ay yarıya iniyor' tek bakışta okunur."""
    ad_cls = "t-label" if bu_ay else "t-label c-2"
    return f'''              <div class="satir">
                <div class="{ad_cls}" style="width:56px;flex:0 0 auto">{ay}</div>
                <div class="w12"></div>
                <div class="yuk-oluk"><div class="yuk-dolgu" style="width:{oran}%"></div></div>
                <div class="w12"></div>
                <div class="t-amount" style="width:88px;flex:0 0 auto;text-align:right">{tutar}</div>
              </div>'''


def ay_karti(satirlar, baslik="Önümüzdeki aylar", alt=""):
    ic = '<div class="h8"></div>'.join(satirlar)
    alt_html = f'''              <div class="h12"></div>
              <div class="t-cap">{alt}</div>''' if alt else ''
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="t-h2">{baslik}</div>
              <div class="h8"></div>
{ic}
{alt_html}
            </div>
          </div>'''


# ------------------------------------------------------------- seri satırı
def seri(ad, mevcut, toplam, tutar, bitis, son=False, basili=False):
    cls = "satir-kart" + (" basili" if basili else "")
    alt = ('<div class="t-cap c-warn">Son taksit bu ay</div>' if son
           else f'<div class="t-cap tek-satir">{bitis}</div>')
    return f'''            <div class="{cls}">
              {kat_kab(ad)}
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-body">{ad} · {mevcut}/{toplam}</div>
                {alt}
              </div>
              <div class="w12"></div>
              <div class="kolon" style="align-items:flex-end;flex:0 0 auto;white-space:nowrap">
                <div class="t-amount">{tutar}</div>
                <div class="h4"></div>
                <div class="t-cap">her ay</div>
              </div>
            </div>'''


def ozet_karti(tutar, alt):
    return f'''          <div class="pad">
            <div class="clay-lg kart-ic">
              <div class="t-label c-2">Bu ay</div>
              <div class="h4"></div>
              <div class="satir" style="align-items:baseline">
                <div class="t-display">{tutar}</div>
                <div class="w8"></div>
                <div class="t-amount c-2">₺</div>
              </div>
              <div class="h12"></div>
              <div class="t-cap">{alt}</div>
            </div>
          </div>'''


def seri_basligi(adet):
    return f'''          <div class="pad aralik">
            <div class="t-h2">Süren seriler</div>
            <div class="t-label c-2">{adet}</div>
          </div>
          <div class="h8"></div>'''


# ------------------------------------------------------------------ A · dolu
A = f'''{push_basi("Taksitler")}
{ozet_karti("3.120", "Taksitler girildiği güne değil, ait olduğu aya yazılır.")}
          <div class="h24"></div>
{ay_karti([
    ay_satiri("Eylül", "3.120 ₺", 100, bu_ay=True),
    ay_satiri("Ekim", "1.560 ₺", 50),
    ay_satiri("Kasım", "1.560 ₺", 50),
    ay_satiri("Aralık", "1.560 ₺", 50),
    ay_satiri("Ocak", "1.040 ₺", 33),
    ay_satiri("Şubat", "1.040 ₺", 33),
], alt="Kalan toplam 12.480 ₺. Sonuncusu Mayıs 2027 tarihinde bitiyor.")}
          <div class="h24"></div>
{seri_basligi("3 seri")}
          <div class="pad kolon">
{seri("Diğer", 3, 12, "1.040 ₺", "Mayıs 2027 tarihinde bitiyor")}
            <div class="h8"></div>
{seri("Giyim", 2, 6, "520 ₺", "Aralık 2026 tarihinde bitiyor")}
            <div class="h8"></div>
{seri("Sağlık", 4, 4, "1.560 ₺", "", son=True)}
          </div>
          <div class="h24"></div>'''

# ------------------------------------------- B · seri bitiyor / yük düşüyor
B = f'''{push_basi("Taksitler")}
{ozet_karti("1.560", "Taksitler girildiği güne değil, ait olduğu aya yazılır.")}
          <div class="h24"></div>
{ay_karti([
    ay_satiri("Ekim", "1.560 ₺", 100, bu_ay=True),
    ay_satiri("Kasım", "1.560 ₺", 100),
    ay_satiri("Aralık", "1.560 ₺", 100),
    ay_satiri("Ocak", "1.040 ₺", 67),
    ay_satiri("Şubat", "1.040 ₺", 67),
    ay_satiri("Mart", "1.040 ₺", 67),
], alt="Kalan toplam 9.360 ₺. Sonuncusu Mayıs 2027 tarihinde bitiyor.")}
          <div class="h24"></div>
{seri_basligi("2 seri")}
          <div class="pad kolon">
{seri("Diğer", 4, 12, "1.040 ₺", "Mayıs 2027 tarihinde bitiyor", basili=True)}
            <div class="h8"></div>
{seri("Giyim", 3, 6, "520 ₺", "Aralık 2026 tarihinde bitiyor")}
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek t-cap">Sağlık serisi eylülde bitti. Aylık yük 1.560 ₺ düştü.</div>
            </div>
          </div>
          <div class="h24"></div>'''

# ------------------------------------------------------------------- C · boş
C = f'''{push_basi("Taksitler")}
          <div class="pad">
            <div class="clay-lg kart-ic kolon orta">
              <div class="hero-daire hero-daire-bos hero-bos" style="width:176px;height:176px">
                <div class="hero-orta">
                  <div class="ikon-kutu ikon-kutu-32" style="color:var(--text-2)">{icon("calendar-clock")}</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-h2">Taksitli işlem yok</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Kartla taksitli harcama girdiğinde burada listelenir.</div>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- D · yükleniyor
D = f'''{push_basi("Taksitler")}
          <div class="pad">
            <div class="clay-lg kart-ic">
              {isk("52px", "18px")}
              <div class="h4"></div>
              {isk("152px", "38px")}
              <div class="h12"></div>
              {isk("100%", "18px")}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic">
              {isk("176px", "25px")}
              <div class="h8"></div>
              {'<div class="h8"></div>'.join(f'<div class="satir">{isk("56px", "18px")}<div class="w12"></div><div class="esnek">{isk("100%", "12px")}</div><div class="w12"></div>{isk("88px", "24px")}</div>' for _ in range(6))}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad aralik">
            {isk("140px", "25px")}
            {isk("56px", "18px")}
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
            {'<div class="h8"></div>'.join(f'<div class="clay-tile" style="padding:12px 16px"><div class="satir">{isk("44px", "44px", "16px")}<div class="w12"></div><div class="esnek kolon">{isk("128px", "24px")}<div class="h4"></div>{isk("168px", "18px")}</div><div class="w12"></div>{isk("72px", "24px")}</div></div>' for _ in range(2))}
          </div>
          <div class="h24"></div>'''


units = "".join([
    device("TAKSİTLER", "E-18 · dolu (yük haritası)", A, note=
           "<b>Önümüzdeki aylara yayılmış yük ekranın merkezindedir.</b> Altı ay, altı çubuk, tek ölçek: "
           "eylül %100, ekim yarısı. Kullanıcı \"gelecek ay rahatlıyorum\" bilgisini <b>okumadan</b> görür. "
           "Yorum yok: \"çok taksit yapmışsın\" gibi bir cümle kurulmaz, sayı ve süre verilir. Ürünün tek "
           "ileriye bakan yüzeyi budur."),
    device("TAKSİTLER", "E-18 · seri bitti, yük düştü", B, note=
           "<b>Biten seri kutlanmaz, kaydedilir.</b> Konfeti/rozet yok; mavi bilgi şeridi olanı söyler: "
           "\"Sağlık serisi eylülde bitti. Aylık yük 1.560 ₺ düştü.\" Şerit <b>listenin altındadır</b> — "
           "önce durum, sonra açıklama. Şeritteki sayı çubukların yeni ölçeğiyle doğrulanabilir."),
    device("TAKSİTLER", "E-18 · boş (taksit yok)", C, note=
           "<b>Boş durum bir hata değil, iyi haberdir</b> ama öyle de sunulmaz — ürün yorum yapmaz. "
           "Buton yok: taksit buradan eklenmez, harcama eklerken oluşur; cümle tam olarak bunu söyler. "
           "İllüstrasyon E-14/E-15'le aynı kaptır, ikon farklıdır: aile aynı, mesaj farklı."),
    device("TAKSİTLER", "E-18 · yükleniyor", D, note=
           "<b>Altı ay çubuğu iskelette de altı satırdır:</b> yükleme bittiğinde düzen zıplamaz. "
           "Blokların genişlikleri gerçek içeriğin genişliğine yakın tutulur (ay adı dar, tutar 88px "
           "sabit sütun) — eşit uzunlukta gri çizgiler dizmek sahte bir içerik vaat eder."),
])

OUT.write_text(page(
    "Trinkow · Taksitler — prototip v3",
    "E-18 · Taksitler",
    "Arketip D — Zaman çizelgesi / yük haritası · push · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
