# -*- coding: utf-8 -*-
"""E-01…E-03 · Onboarding — **KATMAN 1** (K-053) · arketip C (Onboarding 1 of N).

v4 · T-3 revizyonu. K-053 onboarding'i iki katmana ayırdı ve Katman 1'i
üç soruda kilitledi (F-9 korunur):

  1/3  ana niyet          Takip · Tasarruf · Borçtan çıkış
  2/3  aylık net gelir    **ATLANABİLİR — zorunlu değil** (en yüksek terk noktası)
  3/3  maaş günü          günlük limitin bölüneceği dönem buradan gelir

Bu üç cevaptan sonra uygulama **çalışır durumdadır**: kayıt tutulur, gün
kapanır, seri işler. Eksik olan tek şey günlük limittir ve o **uydurulmaz**
(K-050 ruhu: veri yoksa sayı icat edilmez) — kullanıcı ya "Seni tanıyalım"
kartlarıyla plan kurar (E-25 → E-26), ya limiti elle yazar.

v3'ten DÜŞEN iki soru: "Günde ne kadar harcamak istiyorsun" (artık plandan
türetilir) ve kipe bağlı kategori seçimi (kategori limitleri E-17'de kurulur).
Sekme çubuğu yok. Mood: ferah, tek soru, bol boşluk.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, tus_takimi, tl, denklem

OUT = pathlib.Path(__file__).parent.parent / "03-onboarding.html"


def basi(adim, geri=True):
    dolu = "".join('<div class="adim-dolu"></div><div class="w8"></div>' if i < adim
                   else '<div class="adim-oluk"></div><div class="w8"></div>' for i in range(3))
    geri_btn = (f'<button class="ikon-btn" aria-label="Geri dön">{icon("chevron-left")}</button>'
                if geri else '<div style="width:44px;height:44px"></div>')
    return f'''            <div class="ekran-basi">
              {geri_btn}
              <div class="t-micro">Adım {adim}/3</div>
              <button class="btn-ghost" style="padding:0 16px;height:44px">Şimdi değil</button>
            </div>
            <div class="pad satir" aria-label="Kurulum ilerlemesi" style="margin-right:-8px">
              {dolu}
            </div>'''


def soru(baslik, aciklama):
    return f'''            <div class="pad kolon">
              <div class="t-h1">{baslik}</div>
              <div class="h8"></div>
              <div class="t-body c-2">{aciklama}</div>
            </div>'''


def secim(ikon, baslik, alt, secili=False, basili=False):
    c = " secili" if secili else (" basili" if basili else "")
    return f'''              <button class="secim-kart{c}">
                <div class="secim-ikon">{icon(ikon)}</div>
                <div class="w16"></div>
                <div class="esnek kolon">
                  <div class="t-strong">{baslik}</div>
                  <div class="h8"></div>
                  <div class="t-cap">{alt}</div>
                </div>
              </button>'''


# ------------------------------------------------------------- E-01 · niyet
A = f'''{basi(1, geri=False)}
            <div class="h24"></div>
{soru("Neden buradasın", "Sonra değiştirebilirsin.")}
            <div class="h24"></div>
            <div class="pad kolon">
{secim("target", "Param nereye gidiyor", "Günlük harcamanı görmek istiyorsun.", secili=True)}
              <div class="h8"></div>
{secim("landmark", "Bütçe yaratmak", "Her ay bir miktar ayırmak istiyorsun.")}
              <div class="h8"></div>
{secim("trending-down", "Borç kapatmak", "Kalan borcu eritmek istiyorsun.", basili=True)}
            </div>
            <div class="h24"></div>
            <div class="pad">
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("gauge")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-label c-2">Panondaki büyük sayı</div>
                  <div class="h4"></div>
                  <div class="t-strong">bugün kalan</div>
                </div>
              </div>
            </div>
            <div class="h24"></div>'''

A_alt = '''          <div class="alt-sabit">
            <div class="pad"><button class="btn-primary">Devam</button></div>
          </div>'''


# -------------------------------------------------------- E-02 · aylık gelir
def gelir(deger="", imlec=True, devam_pasif=False, atla_basili=False):
    """Tek zorunlu olmayan soru. **Atla** birincil butonun hemen altında,
    tam genişlikte ve aynı dokunma hedefi boyunda durur; küçültülmüş ya da
    en alta sürülmüş bir "hayır" yolu bırakmak K-053'ün açık yasağıdır."""
    ic = (f'<div class="t-hero">{deger}</div>' if deger
          else '<div class="t-hero c-3">0</div>')
    imlec_html = '<div class="imlec"></div>' if imlec else ''
    aylik = ('<div class="t-cap">Eline geçen tutar. Kesintiden sonrası.</div>'
             if deger else
             '<div class="t-cap">Kesin olması gerekmiyor. Yaklaşık yeter.</div>')
    return f'''{basi(2)}
            <div class="h24"></div>
{soru("Aylık net gelirin ne kadar", "Planı buna göre kuruyoruz. İstemezsen atla.")}
            <div class="h24"></div>
            <div class="pad">
              <div class="t-label c-2">Aylık net gelir</div>
              <div class="h8"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="satir" style="justify-content:center;align-items:baseline">
                  {ic}
                  {imlec_html}
                  <div class="w8"></div>
                  <div class="t-hero-simge c-2">₺</div>
                </div>
              </div>
              <div class="h8"></div>
              {aylik}
            </div>
            <div class="h12"></div>
            <div class="pad">
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Gelirin telefonunda kalır.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Atlarsan günlük limiti sen yazarsın.</div>
                </div>
              </div>
            </div>
            <div class="h24"></div>'''


def gelir_alt(devam_pasif=False, atla_basili=False):
    devam = ('<button class="btn-primary pasif" disabled aria-disabled="true">Devam</button>'
             if devam_pasif else '<button class="btn-primary">Devam</button>')
    ab = " basili" if atla_basili else ""
    return f'''          <div class="alt-sabit">
{tus_takimi()}
            <div class="h12"></div>
            <div class="pad kolon">
              {devam}
              <div class="h8"></div>
              <button class="btn-ghost{ab}" style="width:100%" aria-label="Gelir sorusunu atla">Atla</button>
            </div>
          </div>'''


B = gelir(deger="32.000")
C = gelir(deger="", imlec=False)


# --------------------------------------------------------- E-03 · maaş günü
def gun_agi(secili=15):
    o = []
    for g in range(1, 32):
        c = " secili" if g == secili else ""
        o.append(f'''<div class="gun-ag-oge"><button class="gun-kutu{c}" aria-label="Ayın {g}. günü">'''
                 f'''<div class="t-label">{g}</div></button></div>''')
    return f'<div class="gun-ag">{"".join(o)}</div>'


def ozet(satirlar):
    ic = '\n                <div class="h8"></div>\n'.join(satirlar)
    return f'''            <div class="pad">
              <div class="clay kart-ic kolon">
                <div class="t-label c-2">Kurulum özeti</div>
                <div class="h8"></div>
{ic}
              </div>
            </div>'''


def ozet_satiri(ad, deger, vurgu=False):
    cls = "t-amount" if vurgu else "t-strong"
    return f'''                <div class="aralik">
                  <div class="t-body">{ad}</div>
                  <div class="{cls}">{deger}</div>
                </div>'''


def maas(secili=15, duzensiz=False, duzensiz_basili=False):
    if duzensiz:
        ag = ""
        alt_not = ("Dönem 30 gün sayılır. Maaş günü değişirse ayarlardan "
                   "düzeltebilirsin.")
        ozet_gun = "Düzensiz"
    else:
        ag = f'''            <div class="pad">
{gun_agi(secili)}
            </div>
            <div class="h12"></div>'''
        alt_not = f"Dönem ayın {secili}'inde başlar. Limit kalan güne bölünür."
        ozet_gun = f"Ayın {secili}'i"
    db = " basili" if duzensiz_basili else ""
    ds = " secili" if duzensiz else ""
    return f'''{basi(3)}
            <div class="h24"></div>
{soru("Maaşın hangi gün yatıyor", "Günlük limit maaş dönemine bölünür.")}
            <div class="h24"></div>
{ag}            <div class="pad kolon">
              <div class="satir">
                <div class="cip-ag-oge"><button class="cip{ds}{db}">Düzensiz geliyor</button></div>
              </div>
              <div class="t-cap">{alt_not}</div>
            </div>
            <div class="h24"></div>
{ozet([ozet_satiri("Niyet", "Takip"),
       ozet_satiri("Aylık net gelir", tl(32000), vurgu=True),
       ozet_satiri("Maaş günü", ozet_gun),
       ozet_satiri("Günlük limit", "Henüz yok")])}
            <div class="h8"></div>
            <div class="pad">
              <div class="t-cap">Gelirini yazdığın için sana bir günlük limit önerebiliriz. Kabul etmek zorunda değilsin.</div>
            </div>
            <div class="h24"></div>'''


D = maas(secili=15)
E = maas(duzensiz=True, duzensiz_basili=False)

D_alt = '''          <div class="alt-sabit">
            <div class="pad"><button class="btn-primary">Başla</button></div>
          </div>'''



# ===========================================================================
# F · K-059/5 · GÜNLÜK LİMİT ÖNERİSİ (Katman 1 çıkışı)
# ===========================================================================
# NEDEN VAR: E-10 varsayılanı limitsizdir, limitsiz kipte seri çalışmaz
# (K-048) — yani Katman 2'yi atlayan kullanıcı oyunlaştırmayı hiç görmezdi.
# K-059/5 boşluğu tek bir onayla kapatıyor: **gelir girildiyse** belgelenmiş
# bir varsayılan dağılımdan bir limit ÖNERİLİR, kullanıcı tek dokunuşla
# onaylar. Gelir girilmediyse bu yüzey HİÇ açılmaz, limitsiz kip aynen kalır.
#
# SAYI UYDURMA SINIRI (K-050 ruhu): burada uydurulan hiçbir şey yok —
#   • gelir kullanıcının kendi girdisi,
#   • dağılım (%50 zorunlu · %30 sosyal ve keyfi · %20 birikim) belgelenmiş
#     ve ekranda açıkça yazılı bir varsayılan, gizli bir katsayı değil,
#   • bölen (28 gün) kullanıcının maaş gününden çıkıyor,
#   • ve sonuç **onaydan geçmeden limit olmuyor.**
# Bu yüzden sayının yanında "Öneri" pulu durur; kabul edilince pul düşer.
#
# ÜÇ ÇIKIŞ, ÜÇ AĞIRLIK: kabul (primary) · değiştir (secondary) · limitsiz
# devam (ghost). Reddetme yolu küçültülmedi: tam genişlik, 44pt dokunma hedefi.
ONERI_DAGILIM = [
    ("1", f"Aylık net gelirin {tl(32000)}."),
    ("2", "Yaygın bir varsayılan dağılım kullandık: %50 zorunlu, "
          "%30 sosyal ve keyfi, %20 birikim."),
    ("3", f"Sosyal ve keyfi pay {tl(9600)} oldu, maaş döneminde kalan 28 güne bölündü."),
]


def adim_satiri(no, metin):
    return f'''                <div class="satir-ust">
                  <div class="t-label c-2" style="width:12px">{no}</div>
                  <div class="w12"></div>
                  <div class="esnek"><div class="t-cap">{metin}</div></div>
                </div>'''


def limit_onerisi(kabul_basili=False):
    kb = " basili" if kabul_basili else ""
    adimlar = '\n                <div class="h8"></div>\n'.join(
        adim_satiri(n, m) for n, m in ONERI_DAGILIM)
    return f'''          <div class="katman-ust">
            <div class="scrim-kat"></div>
            <div class="sheet">
              <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
              <div class="h12"></div>
              <div class="satir">
                <div class="esnek t-h2">Günlük limit önerimiz</div>
                <div class="w12"></div>
                <div class="oneri-pul">Öneri</div>
              </div>
              <div class="h8"></div>
              <div class="t-cap">Sen onaylamadan limit olmaz.</div>
              <div class="h16"></div>
{denklem((tl(9600), "sosyal ve keyfi pay"), ("28 gün", "kalan gün"), (tl(342), "günlük"))}
              <div class="h16"></div>
              <div class="t-label c-2">Nasıl hesaplandı</div>
              <div class="h12"></div>
              <div class="kolon">
{adimlar}
              </div>
              <div class="h16"></div>
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Bu sayı senin cevaplarından değil, varsayılan dağılımdan çıktı.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Sekiz kartı doldurursan plan kendi giderlerinle kurulur.</div>
                </div>
              </div>
              <div class="h16"></div>
              <button class="btn-primary{kb}">{icon("check")}<div class="w8"></div>Limiti kabul et</button>
              <div class="h8"></div>
              <button class="btn-secondary">{icon("pencil")}<div class="w8"></div>Başka bir sayı yaz</button>
              <div class="h8"></div>
              <button class="btn-ghost" style="width:100%">Limitsiz devam et</button>
            </div>
          </div>'''


F = maas(secili=15)


units = "".join([
    device("KATMAN 1", "adım 1/3 · niyet", A,
           "<b>Mood:</b> ferah, tek karar. Seçenekler <b>dikey kart</b> — \"daire ikon + başlık + tek cümle\" "
           "üçlü sütun kurulmadı. Seçili kart <b>çukur</b>, seçilmemiş kartlar <b>kabarık</b>; üçüncüsü "
           "<b>basılı (pressed)</b> gösteriliyor. Alttaki şerit seçimin panoda ne yapacağını gösterir.",
           sabit_alt=A_alt),
    device("KATMAN 1", "adım 2/3 · aylık gelir (girildi)", B,
           "<b>K-053'ün en kırılgan sorusu.</b> Zorunlu değil ve bu ekranda <b>iki yerden</b> okunuyor: "
           "başlıkta (\"İstemezsen atla\") ve butonun altındaki <b>tam genişlikte Atla</b>. Mahremiyet "
           "cümlesi kullanıcı faydası dilinde: \"Gelirin telefonunda kalır\" — mimari sözcük yok (K-057/1). "
           "Aynı <b>kil tuş takımı</b> harcama ekle ekranından geliyor; kullanıcı ikinci bir giriş biçimi "
           "öğrenmiyor.",
           sabit_alt=gelir_alt()),
    device("KATMAN 1", "adım 2/3 · boş · Atla basılı", C,
           "<b>Atlamak birinci sınıf bir yol.</b> Alan boşken <b>Devam pasif</b>, <b>Atla</b> ise etkin ve "
           "<b>basılı</b> çizildi: kullanıcının tek geri bildirimi budur (RN'de hover yok). Kuyudaki 0 "
           "<code>text-3</code> placeholder rengiyle duruyor, imleç yok — alan henüz odakta değil. "
           "Sayı uydurup \"ortalama gelir\" yazmıyoruz.",
           sabit_alt=gelir_alt(devam_pasif=True, atla_basili=True)),
    device("KATMAN 1", "adım 3/3 · maaş günü · ayın 15'i", D,
           "31 gün <b>sarmalı satır</b> (grid değil — RN <code>flexWrap</code>): 44×44 kutu + 8 boşluk, "
           "satıra 7 kutu (356 ≤ 358). Seçili gün <b>dolgu + kil kabartma</b> ile belirtilir, "
           "<b>halka yok</b> (K-054/6). Kurulum özeti son satırda dürüst duruyor: <b>Günlük limit — "
           "Henüz yok.</b> Uydurma bir limit yazmıyoruz. Gelir girildiği için son satır bir sonraki yüzeye bağlanır: <b>öneri</b>, onay bekleyen bir sayıdır.",
           sabit_alt=D_alt),
    device("KATMAN 1", "K-059/5 · günlük limit ÖNERİSİ (gelir girildi)", F,
           "<b>K-059/5'in kapattığı boşluk:</b> limitsiz kipte seri çalışmaz (K-048), yani Katman 2'yi "
           "atlayan kullanıcı oyunlaştırmayı hiç görmezdi. Gelir girildiyse limit <b>önerilir</b>, "
           "dayatılmaz. Sayının yanındaki <b>\"Öneri\" pulu</b> onay beklediğini söyler ve kabul edilince "
           "düşer. Hesap <b>kara kutu değil</b>: denklem üstte, üç adımlık \"Nasıl hesaplandı\" hemen "
           "altında, kullanılan varsayılan dağılım (%50/%30/%20) <b>ekranda yazılı</b> — gizli katsayı "
           "yok, uydurma sayı yok (K-050). Üç yol üç ağırlıkta: <b>kabul</b> (primary, basılı çizildi) · "
           "<b>başka bir sayı yaz</b> (secondary) · <b>limitsiz devam et</b> (ghost, tam genişlik, 44pt "
           "dokunma hedefi — reddetme yolu küçültülmedi). Arkadaki adım 3/3 scrim altında görünür kalır: bu bir ekran "
           "değil, Katman 1'in çıkışında açılan tek yüzeydir.",
           sabit_alt=limit_onerisi(kabul_basili=True)),
    device("KATMAN 1", "adım 3/3 · düzensiz gelir (uç durum)", E,
           "<b>Serbest çalışan gerçeği.</b> Maaş günü yoksa gün ızgarası kapanır ve dönem <b>30 gün</b> "
           "sayılır; bu varsayım ekranda <b>yazılı</b> duruyor, arka planda saklanmıyor. Özet satırı "
           "\"Düzensiz\" der. Kip pill'i gibi çip <b>metin taşır, ikon taşımaz.</b>",
           sabit_alt=D_alt),
])

OUT.write_text(page(
    "Trinkow · Onboarding Katman 1 (3 soru) — prototip v4",
    "E-01 … E-03 · Onboarding · Katman 1",
    "Arketip C — Onboarding (1 of N) · K-053: 3 soru, gelir atlanabilir · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
