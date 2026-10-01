# -*- coding: utf-8 -*-
"""E-16 · Özet — arketip F (Focus) + çizelge.
Mood: ÖLÇÜM SAYFASI. Yorum yok, sayı var. E-10 tek yuvarlak nesne,
E-14 defter ritmi; burası sütun + hairline çizelge. Ekranda 56pt yoktur,
en büyük rol 32pt (display) haftalık toplamdır.

Grafik: inline SVG (RN'de react-native-svg). Renkler yalnız 6 kategori
ailesinden + grad.action / grad.arc-over (tokens §1.8). Pasta grafik
Faz 1'de yoktur (ekran-envanteri §7).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, sekme_cubugu, icon, ay_secici, isk

OUT = pathlib.Path(__file__).parent.parent / "05-ozet.html"

GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
LIMIT = 300
W, H = 326.0, 138.0          # SVG kutusu — kart iç genişliği 326
UST, TABAN = 14.0, 138.0     # sütunun GÖRÜNEN üst/alt sınırı
KAL = 20.0                   # sütun kalınlığı
R = KAL / 2                  # yuvarlak ucun yarıçapı
HUCRE = W / 7
_sayac = [0]                 # SVG id çakışmasını önler (tokens §12 #29)


def _y(deger, olcek):
    return TABAN - (deger / olcek) * (TABAN - UST)


def sutun_grafik(degerler, bugun=-1, olcek=600, limit=LIMIT, limit_cizgisi=True):
    """Günlük toplam sütunları.

    İKİ GEOMETRİ KURALI:
    1) Yuvarlak uç (`strokeLinecap: round` = tokens `radius.arc`) çizginin
       UCUNDAN R kadar taşar. Bu yüzden çizgi [deger+R .. TABAN-R] arasına
       çizilir; GÖRÜNEN uç tam olarak değerin hizasına düşer. Aksi hâlde
       300 ₺ limitinin altındaki bir sütun limit çizgisini aşıyor görünür.
    2) Gradyan `gradientUnits="userSpaceOnUse"` olmak ZORUNDA: dikey bir
       <line>'ın sınır kutusu 0 genişliktedir, objectBoundingBox gradyanı
       hiç çizilmez (SVG 1.1 §13.2.2 — react-native-svg de aynı davranır).

    degerler: gün başına tutar · None = gün henüz gelmedi (oluk boş kalır).
    """
    _sayac[0] += 1
    n = _sayac[0]
    oluk, dolgu, parlama, defs = [], [], [], []
    for i, v in enumerate(degerler):
        x = HUCRE * i + HUCRE / 2
        oluk.append(f'<line x1="{x:.1f}" y1="{UST + R:.1f}" x2="{x:.1f}" y2="{TABAN - R:.1f}" '
                    f'stroke="#E6EFFE" stroke-width="{KAL:.0f}" stroke-linecap="round"/>')
        if v is None:
            continue
        y = _y(v, olcek)
        y1 = min(y + R, TABAN - R)
        boya = f"url(#gOver{n})" if v > limit else f"url(#gBar{n})"
        dolgu.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{TABAN - R:.1f}" '
                     f'stroke="{boya}" stroke-width="{KAL:.0f}" stroke-linecap="round"/>')
        # kabarık yüzeyin üst parlaması (grad.clay-face'in sütun karşılığı):
        # sütunun üst %45'i beyazdan saydama. Her sütunun boyu farklı olduğu
        # için gradyan sütuna özeldir.
        boy = max(24.0, (TABAN - y) * 0.45)
        defs.append(f'<linearGradient id="gP{n}_{i}" gradientUnits="userSpaceOnUse" '
                    f'x1="0" y1="{y:.1f}" x2="0" y2="{y + boy:.1f}">'
                    f'<stop offset="0%" stop-color="rgba(255,255,255,0.55)"/>'
                    f'<stop offset="100%" stop-color="rgba(255,255,255,0)"/></linearGradient>')
        parlama.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{TABAN - R:.1f}" '
                       f'stroke="url(#gP{n}_{i})" stroke-width="{KAL:.0f}" stroke-linecap="round"/>')
    yl = _y(limit, olcek)
    cizgi = '' if not limit_cizgisi else (
        f'<line x1="0" y1="{yl:.1f}" x2="{W:.0f}" y2="{yl:.1f}" stroke="#4961A5" '
        f'stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>')
    return f'''<svg viewBox="0 0 {W:.0f} {H:.0f}" style="width:100%;height:{H:.0f}px" role="img"
                   aria-label="Günlük toplamlar, günlük limit 300 ₺">
                <defs>
                  <linearGradient id="gBar{n}" gradientUnits="userSpaceOnUse" x1="0" y1="{UST}" x2="0" y2="{TABAN}">
                    <stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2F68C5"/>
                  </linearGradient>
                  <linearGradient id="gOver{n}" gradientUnits="userSpaceOnUse" x1="0" y1="{UST}" x2="0" y2="{TABAN}">
                    <stop offset="0%" stop-color="#D97706"/><stop offset="100%" stop-color="#B45309"/>
                  </linearGradient>
                  {''.join(defs)}
                </defs>
                {''.join(oluk)}
                {cizgi}
                {''.join(dolgu)}
                {''.join(parlama)}
              </svg>'''


def gun_etiketleri(degerler, bugun=-1):
    ogeler = []
    for i, ad in enumerate(GUNLER):
        if i == bugun:
            cls = "t-label c-primary"
        elif degerler[i] is None:
            cls = "t-micro c-3"
        else:
            cls = "t-micro"
        ogeler.append(f'<div class="{cls} esnek" style="text-align:center">{ad}</div>')
    return f'<div class="satir">{"".join(ogeler)}</div>'


def grafik_karti(toplam, ortalama, degerler, bugun=-1, olcek=600,
                 serit=("info", "Bu hafta 6 gün limit altında."),
                 toplam_cls="", ort_etiket="Günlük ortalama"):
    tip, metin = serit
    renk = "var(--warning-ink)" if tip == "warn" else "var(--primary-text)"
    yazi = " c-warn" if tip == "warn" else ""
    return f'''          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="aralik">
                <div class="kolon">
                  <div class="t-label c-2">Haftalık toplam</div>
                  <div class="h4"></div>
                  <div class="t-display{toplam_cls}">{toplam}</div>
                </div>
                <div class="kolon" style="align-items:flex-end">
                  <div class="t-label c-2">{ort_etiket}</div>
                  <div class="h4"></div>
                  <div class="t-amount">{ortalama}</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="aralik">
                <div class="t-label c-2">Günlük toplam</div>
                <div class="satir">
                  <div style="width:16px;height:2px;border-radius:999px;background-color:var(--text-2)"></div>
                  <div class="w8"></div>
                  <div class="t-micro">günlük limit 300 ₺</div>
                </div>
              </div>
              <div class="h8"></div>
              {sutun_grafik(degerler, bugun, olcek)}
              <div class="h8"></div>
              {gun_etiketleri(degerler, bugun)}
              <div class="h12"></div>
              <div class="serit serit-{tip}">
                <div class="ikon-kutu" style="color:{renk}">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap{yazi}">{metin}</div>
              </div>
            </div>
          </div>'''


# --- kategori dağılımı: çizelge (nokta + ad + pay + tutar), hairline ayraç ---
DAGILIM = [
    ("Market", "cat-yesil", 26, "520 ₺", "12 kayıt"),
    ("Restoran", "cat-amber", 23, "445 ₺", "6 kayıt"),
    ("Kafe", "cat-amber", 17, "338 ₺", "9 kayıt"),
    ("Ulaşım", "cat-mavi", 14, "282 ₺", "11 kayıt"),
    ("Fatura", "cat-lacivert", 11, "210 ₺", "2 kayıt"),
    ("Diğer", "cat-duman", 9, "172 ₺", "4 kayıt"),
]


def dagilim_karti(satirlar=DAGILIM, en_cok="Market", gun_etiket="7 gün",
                  basili_ad=""):
    """Her satır E-15 kategori detayına gider → <button>. RN'de hover yoktur,
    bu yüzden satırın tek geri bildirimi BASILI durumdur: hairline düşer,
    yerine çukur (clay-pressed) gelir. Basılı satır 8pt dışa taşar ki çukur
    metne yapışmasın; iç 8pt padding içeriği aynı hizada tutar."""
    segment = "".join(
        f'<div class="cubuk-dolgu" style="width:{p}%;background-color:var(--{c})"></div>'
        for _, c, p, _, _ in satirlar)
    rows = []
    for i, (ad, c, p, tutar, adet) in enumerate(satirlar):
        basili = (ad == basili_ad)
        ayrac = ("" if i == len(satirlar) - 1 or basili
                 else "border-bottom:1px solid var(--line);")
        if basili:
            kutu = ('<button class="satir basili" aria-label="Kategori detayı"'
                    ' style="min-height:44px;width:100%;border:0;border-radius:16px;'
                    'padding:0 8px;margin:0 -8px;text-align:left">')
        else:
            kutu = (f'<button class="satir" aria-label="Kategori detayı"'
                    f' style="min-height:44px;width:100%;border:0;padding:0;'
                    f'background:transparent;text-align:left;{ayrac}">')
        rows.append(f'''              {kutu}
                <div class="nokta" style="background-color:var(--{c})"></div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-body tek-satir">{ad}</div>
                </div>
                <div class="w12"></div>
                <div class="t-cap num" style="width:40px;text-align:right">%{p}</div>
                <div class="w12"></div>
                <div class="t-amount" style="width:88px;text-align:right">{tutar}</div>
              </button>''')
    return f'''          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="aralik">
                <div class="t-h2">Kategori dağılımı</div>
                <div class="t-label c-2">{gun_etiket}</div>
              </div>
              <div class="h8"></div>
              <div class="cubuk-oluk">{segment}</div>
              <div class="h12"></div>
{''.join(rows)}
              <div class="h12"></div>
              <div class="satir">
                <div class="ikon-kutu" style="color:var(--text-2)">{icon("trending-down")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap">En çok harcadığın kategori {en_cok}</div>
              </div>
            </div>
          </div>'''


def kucuk_harcama_karti(adet="19", tutar="610 ₺", ort="32 ₺"):
    return f'''          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="esnek kolon">
                <div class="t-label c-2">50 ₺ altı harcamalar</div>
                <div class="h4"></div>
                <div class="t-display">{tutar}</div>
                <div class="h8"></div>
                <div class="t-cap">{adet} harcama · ortalama {ort}</div>
              </div>
              <div class="w12"></div>
              <div class="kat-kab kat-amber">{icon("coffee")}</div>
            </div>
          </div>'''


def taksit_karti():
    return f'''          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="esnek kolon">
                <div class="t-strong">Önümüzdeki ay taksit yükü 1.041,67 ₺</div>
                <div class="h8"></div>
                <div class="t-cap">Üç seri sürüyor. Sonuncusu aralıkta biter.</div>
                <div class="h12"></div>
                <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Taksitleri gör</button>
              </div>
              <div class="w12"></div>
              <div class="kat-kab kat-lacivert">{icon("repeat")}</div>
            </div>
          </div>'''


def basi():
    return '''          <div class="ekran-basi">
            <div class="t-h1">Özet</div>
            <button class="ikon-btn" aria-label="Kategori limitlerini aç">''' + icon("sliders") + '''</button>
          </div>'''


HAFTA = ["Önceki hafta", "Sonraki hafta"]

# ------------------------------------------------------------- A · dolu hafta
A = f'''{basi()}
{ay_secici("31 Ağustos – 6 Eylül", "Tamamlanan hafta", onceki=HAFTA[0], sonraki=HAFTA[1])}
          <div class="h24"></div>
{grafik_karti("1.967 ₺", "281 ₺", [220, 290, 265, 180, 260, 512, 240])}
          <div class="h24"></div>
{dagilim_karti(basili_ad="Restoran")}
          <div class="h24"></div>
{kucuk_harcama_karti()}
          <div class="h24"></div>
{taksit_karti()}
          <div class="h24"></div>'''

# ---------------------------------------------------------- B · hafta ortası
B_DAG = [
    ("Fatura", "cat-lacivert", 31, "525 ₺", "3 kayıt"),
    ("Restoran", "cat-amber", 26, "440 ₺", "2 kayıt"),
    ("Market", "cat-yesil", 19, "320 ₺", "5 kayıt"),
    ("Ulaşım", "cat-mavi", 14, "235 ₺", "8 kayıt"),
    ("Kafe", "cat-amber", 10, "163 ₺", "4 kayıt"),
]
B = f'''{basi()}
{ay_secici("Bu hafta", "7 – 13 Eylül", onceki=HAFTA[0], sonraki=HAFTA[1])}
          <div class="h24"></div>
{grafik_karti("1.683 ₺", "421 ₺", [265, 298, 940, 180, None, None, None], bugun=3, olcek=1000,
              serit=("info", "Bu hafta 3 gün limit altında."), ort_etiket="Geçen 4 günün ortalaması")}
          <div class="h24"></div>
{dagilim_karti(B_DAG, en_cok="Fatura", gun_etiket="4 gün")}
          <div class="h24"></div>
{kucuk_harcama_karti("11", "384 ₺", "35 ₺")}
          <div class="h24"></div>'''

# -------------------------------------------------- C · tüm hafta limit dışı
C_DAG = [
    ("Restoran", "cat-amber", 34, "1.190 ₺", "9 kayıt"),
    ("Giyim", "cat-kiremit", 22, "770 ₺", "3 kayıt"),
    ("Market", "cat-yesil", 18, "630 ₺", "10 kayıt"),
    ("Eğlence", "cat-kiremit", 14, "490 ₺", "5 kayıt"),
    ("Ulaşım", "cat-mavi", 12, "420 ₺", "14 kayıt"),
]
C = f'''{basi()}
{ay_secici("24 – 30 Ağustos", "Tamamlanan hafta", onceki=HAFTA[0], sonraki=HAFTA[1])}
          <div class="h24"></div>
{grafik_karti("3.500 ₺", "500 ₺", [420, 380, 640, 450, 520, 590, 500], olcek=800,
              serit=("warn", "Bu hafta 7 gün limit dışı."), toplam_cls=" c-warn")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="kolon esnek">
                <div class="t-h2">Günlük limit 300 ₺</div>
                <div class="h8"></div>
                <div class="t-cap">Limit gerçekçi mi. Birlikte bakalım.</div>
                <div class="h12"></div>
                <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Limiti gözden geçir</button>
              </div>
              <div class="w12"></div>
              <button class="ikon-btn" aria-label="Kartı kapat">{icon("x")}</button>
            </div>
          </div>
          <div class="h24"></div>
{dagilim_karti(C_DAG, en_cok="Restoran")}
          <div class="h24"></div>'''

# ------------------------------------------------------------------ D · boş
D = f'''{basi()}
{ay_secici("Bu hafta", "7 – 13 Eylül", onceki=HAFTA[0], sonraki=HAFTA[1])}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {sutun_grafik([None] * 7, limit_cizgisi=False)}
              <div class="h8"></div>
              {gun_etiketleri([None] * 7)}
              <div class="h12"></div>
              <div class="t-h2">Özet için erken</div>
              <div class="h8"></div>
              <div class="t-body">Birkaç kayıt sonra burada haftalık dağılımı görürsün.</div>
              <div class="h12"></div>
              <button class="btn-primary" aria-label="Harcama ekle">{icon("plus")}<div class="w8"></div>Harcama ekle</button>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- E · yükleniyor
E = f'''{basi()}
          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="aralik">
                {isk("44px","44px")}
                <div class="kolon orta">{isk("104px","20px")}<div class="h4"></div>{isk("120px","16px")}</div>
                {isk("44px","44px")}
              </div>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="aralik">
                <div class="kolon">{isk("112px","18px")}<div class="h4"></div>{isk("136px","32px")}</div>
                <div class="kolon" style="align-items:flex-end">{isk("104px","18px")}<div class="h4"></div>{isk("72px","24px")}</div>
              </div>
              <div class="h12"></div>
              {sutun_grafik([None] * 7, limit_cizgisi=False)}
              <div class="h8"></div>
              {gun_etiketleri([None] * 7)}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {isk("160px","20px")}
              <div class="h8"></div>
              {isk("100%","12px")}
              <div class="h12"></div>
              <div class="satir" style="min-height:44px">{isk("8px","8px")}<div class="w12"></div>{isk("96px","16px")}<div class="esnek"></div>{isk("88px","20px")}</div>
              <div class="satir" style="min-height:44px">{isk("8px","8px")}<div class="w12"></div>{isk("112px","16px")}<div class="esnek"></div>{isk("88px","20px")}</div>
              <div class="satir" style="min-height:44px">{isk("8px","8px")}<div class="w12"></div>{isk("80px","16px")}<div class="esnek"></div>{isk("88px","20px")}</div>
            </div>
          </div>
          <div class="h24"></div>'''

units = "".join([
    device("ÖZET", "dolu · tamamlanan hafta", A, sabit_alt=sekme_cubugu("ozet"), note=
           "<b>Mood: ölçüm sayfası.</b> Yorum yok, sayı var. Sütunlar kahraman yayın <b>aynı dilinden</b>: "
           "çukur oluk + kabarık dolgu + yuvarlak uç (<code>strokeLinecap: round</code> = <code>radius.arc</code>). "
           "Limit çizgisi kesikli <code>text-2</code> — grafik değil <b>referans</b> olduğu için renk taşımaz. "
           "Dağılım çizelgesi <b>hairline</b> ayraçlıdır: E-10'un kart yığınından ve E-14'ün defterinden "
           "bilinçli olarak ayrışır. <b>Restoran satırı basılı durumda:</b> satırlar E-15'e giden birer dokunma hedefidir, "
           "RN'de hover olmadığı için basılı tek geri bildirimdir — hairline düşer, yerine çukur gelir. <b>50 ₺ altı</b> kartı ürünün varlık sebebidir — yargı yok, yalnız toplam."),
    device("ÖZET", "hafta ortası · eksik günler", B, sabit_alt=sekme_cubugu("ozet"), note=
           "<b>Gelmemiş günler uydurulmaz:</b> Cum/Cmt/Paz oluğu boş kalır, etiketleri <code>text-3</code>'e iner. "
           "Ortalama etiketi de değişir — 7'ye değil <b>geçen 4 güne</b> bölünür, aksi hâlde sayı yalan olur. "
           "Bugün (Per) etiketi <code>primary-text</code> + SemiBold. Çarşamba limit dışı olduğu için o sütun "
           "amber; ölçek 1.000 ₺'ye çıktığından diğer sütunlar orantılı olarak kısalır."),
    device("ÖZET", "tüm hafta limit dışı", C, sabit_alt=sekme_cubugu("ozet"), note=
           "<b>Yedi gün limit dışı:</b> kırmızı yok, ünlem yok, uyarı ikonu yok. Yedi amber sütun + amber "
           "haftalık toplam yeterince açık. Altındaki kart suçlamıyor, <b>limiti sorguluyor</b> — hata "
           "kullanıcıda değil sayıda olabilir. Kart kapatılabilir (x): ısrar etmez."),
    device("ÖZET", "boş · hafta boş", D, sabit_alt=sekme_cubugu("ozet", fab=False), note=
           "<b>Boş durum:</b> grafik iskeleti <b>gerçek</b> olarak durur — yedi boş oluk, doldurulacak yer "
           "belli. \"Henüz veri yok\" yazmaz. FAB düşer, tek birincil eylem karttadır. Hafta değiştirici "
           "kalır: dolu bir haftaya gitmek gerçek bir çıkış yolu."),
    device("ÖZET", "yükleniyor · iskelet", E, sabit_alt=sekme_cubugu("ozet"), note=
           "<b>Yükleniyor:</b> boş durumdan <b>farklı</b> — orada metin ve buton vardı, burada onların yerinde "
           "çukur bloklar var. Grafik oluğu ikisinde de aynı; veri gelince yalnız dolgu çizilir, düzen kaymaz."),
])

OUT.write_text(page(
    "Trinkow · Özet — prototip v3",
    "E-16 · Özet",
    "Arketip F + çizelge · mood: ölçüm sayfası · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
