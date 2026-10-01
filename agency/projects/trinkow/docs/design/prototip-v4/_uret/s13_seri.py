# -*- coding: utf-8 -*-
"""E-21 · Seri (yeni ekran · K-048) — arketip: **ölçüm sayfası**, push.

Mood: E-10'un "tek büyük nesne" sakinliği DEĞİL; burada üç ölçek üst üste
okunur: bugünkü sayı (56pt) → duraklar şeridi (44pt) → son 4 haftanın gün
ızgarası (44pt). Ekran bir kupa vitrini değil, bir **çetele**dir:
rozet/puan/seviye/lig yoktur (K-048 ile yasak).

Renk kararı: "limit altında" günler **mavi** (yayın dolgu dili), "limit dışı"
günler **amber** (yayın taşma dili), "kayıt yok" günler **çukur boş kutu**.
Yeşil/amber ikilisi bilinçli olarak kullanılmadı — trafik ışığı semantiği
tokens §1.10'da yasaktır ve gün kutusu göstergenin diliyle aynı kalmalı.
"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, push_basi, isk

OUT = pathlib.Path(__file__).parent.parent / "13-seri.html"

AYLAR = {6: "Haziran", 7: "Temmuz", 8: "Ağustos", 9: "Eylül"}
BUGUN = datetime.date(2026, 9, 17)
DURAKLAR = [3, 7, 14, 30, 60, 100, 180, 365]


# ------------------------------------------------------------ kahraman blok
def hero(sayi: str, govde: str, en_uzun: str = "21 gün",
         en_uzun_alt: str = "Temmuz 2026") -> str:
    """Kahraman: gün sayısı + tek satır tespit + "en uzun seri" çukuru.

    Kahraman sayı **gün**dür, para değildir; `₺` yoktur. `hero` rolü ekranda
    tek. "En uzun seri" kahraman kartın İÇİNDE durur, çünkü kırılma anında
    kullanıcının göreceği ilk şey kaybı değil **sahip olduğu rekoru** olsun
    (K-048: kırılma yıkıcı olmaz).
    """
    return f'''          <div class="pad">
            <div class="hero-kart kart-ic kolon">
              <div class="kolon orta">
                <div class="t-hero">{sayi}</div>
                <div class="t-label c-2">gün</div>
                <div class="h12"></div>
                <div class="t-body" style="text-align:center">{govde}</div>
              </div>
              <div class="h12"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="aralik">
                  <div class="kolon">
                    <div class="t-strong">En uzun seri</div>
                    <div class="h4"></div>
                    <div class="t-cap">{en_uzun_alt}</div>
                  </div>
                  <div class="w12"></div>
                  <div class="t-amount">{en_uzun}</div>
                </div>
              </div>
            </div>
          </div>'''


# --------------------------------------------------------- duraklar şeridi
def durak(n: int, durum: str) -> str:
    cls = {"gecildi": " gecildi", "sirada": " sirada", "ileri": ""}[durum]
    ad = {"gecildi": "geçildi", "sirada": "sırada", "ileri": "ileride"}[durum]
    return (f'<div class="durak{cls}" aria-label="{n} gün durağı {ad}">'
            f'<div class="t-label">{n}</div></div>')


def bag(oran: float) -> str:
    """İki durak arasındaki yol. Oran = o aralıkta katedilen kısım.
    RN: iki View (oluk + dolgu); dolgu genişliği yüzdeyle verilir."""
    if oran <= 0:
        return '<div class="durak-bag"></div>'
    return (f'<div class="durak-bag"><div class="durak-bag-dolu" '
            f'style="width:{round(oran * 100)}%"></div></div>')


def duraklar(seri: int, sag_etiket: str) -> str:
    parcalar = []
    for i, n in enumerate(DURAKLAR):
        if i:
            onceki = DURAKLAR[i - 1]
            if seri >= n:
                oran = 1.0
            elif seri <= onceki:
                oran = 0.0
            else:
                oran = (seri - onceki) / (n - onceki)
            parcalar.append(bag(oran))
        if seri >= n:
            parcalar.append(durak(n, "gecildi"))
        elif not [x for x in DURAKLAR if x > seri and x < n]:
            parcalar.append(durak(n, "sirada"))
        else:
            parcalar.append(durak(n, "ileri"))
    return f'''          <div class="pad aralik">
            <div class="t-h2">Duraklar</div>
            <div class="t-label c-2">{sag_etiket}</div>
          </div>
          <div class="h8"></div>
          <div class="yatay-kaydir">
            <div class="satir" style="padding:0 16px">
              {''.join(parcalar)}
            </div>
          </div>'''


# ---------------------------------------------------------- gün ızgarası
def pencere(bitis: datetime.date = None, adet: int = 28):
    """Son 28 KAPANMIŞ gün (bugün dahil değil).

    Neden 28: dört tam hafta → 7 sütunlu ızgara artık kalmadan oturur ve
    satır sonu ritmi bozulmaz. Neden bugün yok: bugün kapanmadı, seriye
    sayılıp sayılmayacağı belli değil — dördüncü bir kutu durumu üretmek
    yerine pencere dünde biter (başlık tarih aralığını yazar)."""
    bitis = bitis or (BUGUN - datetime.timedelta(days=1))
    return [bitis - datetime.timedelta(days=adet - 1 - i) for i in range(adet)]


def gun_kutu(tarih: datetime.date, durum: str) -> str:
    cls = {"altinda": " altinda", "disinda": " disinda", "yok": ""}[durum]
    ad = {"altinda": "limit altında", "disinda": "limit dışı", "yok": "kayıt yok"}[durum]
    return (f'<div class="gun-ag-oge"><div class="gun-kutu{cls}" '
            f'aria-label="{tarih.day} {AYLAR[tarih.month]}, {ad}">'
            f'<div class="t-label">{tarih.day}</div></div></div>')


def lejant() -> str:
    def oge(cls, metin):
        return (f'<div class="gun-kutu{cls}" style="width:24px;height:24px"></div>'
                f'<div class="w8"></div><div class="t-cap">{metin}</div>')
    return f'''          <div class="pad satir">
            {oge(" altinda", "limit altında")}
            <div class="w12"></div>
            {oge(" disinda", "limit dışı")}
            <div class="w12"></div>
            {oge("", "kayıt yok")}
          </div>'''


def izgara(durumlar, alt_etiket: str = "", bos_not: str = "") -> str:
    gunler = pencere()
    ilk, son = gunler[0], gunler[-1]
    aralik = f"{ilk.day} {AYLAR[ilk.month]} – {son.day} {AYLAR[son.month]}"
    kutular = "".join(gun_kutu(g, d) for g, d in zip(gunler, durumlar))
    ek = (f'          <div class="pad"><div class="t-cap">{bos_not}</div></div>\n'
          f'          <div class="h12"></div>\n' if bos_not else "")
    return f'''          <div class="pad aralik">
            <div class="t-h2">Son 4 hafta</div>
            <div class="t-label c-2">{alt_etiket or aralik}</div>
          </div>
          <div class="h8"></div>
{ek}          <div class="pad">
            <div class="gun-ag">
              {kutular}
            </div>
          </div>
          <div class="h12"></div>
{lejant()}'''


def kural_karti() -> str:
    return f'''          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="t-h2">Seri nasıl işler</div>
              <div class="h8"></div>
              <div class="t-body">Günü günlük limitin altında kapatırsan seri sürer.</div>
              <div class="h8"></div>
              <div class="t-body">Kayıt yazmadığın gün sayılmaz. Harcamasız geçtiyse işaretle.</div>
            </div>
          </div>'''


# ------------------------------------------------ veri: 28 günlük pencereler
# A · seri 12 (5–16 Eylül). 4 Eylül limit dışı → seri orada kırılmıştı.
D_AKTIF = (["altinda", "altinda", "yok", "altinda", "altinda", "altinda",
            "disinda", "altinda", "altinda", "altinda", "altinda", "altinda",
            "altinda", "altinda", "yok", "disinda"] + ["altinda"] * 12)
# B · seri dün (16 Eylül) kırıldı → son kutu limit dışı, seri 0.
D_KIRIK = D_AKTIF[:-1] + ["disinda"]
# D · ilk gün: hiç kayıt yok.
D_BOS = ["yok"] * 28

assert len(D_AKTIF) == 28 and len(D_KIRIK) == 28


# --------------------------------------------------------- A · aktif seri
A = f'''{push_basi("Seri")}
{hero("12", "12 gündür limit altında kapatıyorsun.")}
          <div class="h24"></div>
{duraklar(12, "2 gün kaldı")}
          <div class="h24"></div>
{izgara(D_AKTIF)}
          <div class="h24"></div>
{kural_karti()}
          <div class="h24"></div>'''

# ---------------------------------------------------------- B · seri kırıldı
B = f'''{push_basi("Seri", geri_basili=True)}
{hero("0", "Seri dün kırıldı. Bugün yeniden başlıyor.")}
          <div class="h24"></div>
{duraklar(0, "Sıradaki durak 3 gün")}
          <div class="h24"></div>
{izgara(D_KIRIK)}
          <div class="h24"></div>
{kural_karti()}
          <div class="h24"></div>'''

# ------------------------------------------------- C · seri kapalı (limitsiz)
C = f'''{push_basi("Seri")}
          <div class="pad">
            <div class="hero-kart kart-ic kolon">
              <div class="t-h2">Seri kapalı</div>
              <div class="h8"></div>
              <div class="t-body">Seri için günlük limit gerekir.</div>
              <div class="h8"></div>
              <div class="t-cap">Limit kurduğunda duraklar ve günler burada görünür.</div>
              <div class="h12"></div>
              <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Limit belirle</button>
              <div class="h12"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="aralik">
                  <div class="kolon">
                    <div class="t-strong">En uzun seri</div>
                    <div class="h4"></div>
                    <div class="t-cap">Temmuz 2026</div>
                  </div>
                  <div class="w12"></div>
                  <div class="t-amount">21 gün</div>
                </div>
              </div>
            </div>
          </div>
          <div class="h24"></div>
{kural_karti()}
          <div class="h24"></div>'''

# ------------------------------------------------------ D · henüz seri yok
D = f'''{push_basi("Seri")}
          <div class="pad">
            <div class="hero-kart kart-ic kolon">
              <div class="kolon orta">
                <div class="t-hero">0</div>
                <div class="t-label c-2">gün</div>
                <div class="h12"></div>
                <div class="t-body" style="text-align:center">Seri henüz başlamadı. Bugünü limit altında kapat.</div>
              </div>
              <div class="h12"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="aralik">
                  <div class="t-strong">En uzun seri</div>
                  <div class="w12"></div>
                  <div class="t-label c-2">Henüz yok</div>
                </div>
              </div>
            </div>
          </div>
          <div class="h24"></div>
{duraklar(0, "Sıradaki durak 3 gün")}
          <div class="h24"></div>
{izgara(D_BOS, bos_not="Günleri yazdıkça buraya dolacak.")}
          <div class="h24"></div>
{kural_karti()}
          <div class="h24"></div>'''

# ---------------------------------------------------------- E · yükleniyor
def isk_durak():
    p = []
    for i, n in enumerate(DURAKLAR):
        if i:
            p.append('<div class="durak-bag"></div>')
        p.append('<div class="durak"></div>')
    return "".join(p)


E = f'''{push_basi("Seri")}
          <div class="pad">
            <div class="hero-kart kart-ic kolon">
              <div class="kolon orta">
                {isk("104px","56px")}
                <div class="h8"></div>
                {isk("48px","16px")}
                <div class="h12"></div>
                {isk("240px","16px")}
              </div>
              <div class="h12"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="aralik">
                  {isk("120px","20px")}
                  {isk("64px","20px")}
                </div>
              </div>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad aralik">
            <div class="t-h2">Duraklar</div>
            {isk("88px","18px")}
          </div>
          <div class="h8"></div>
          <div class="yatay-kaydir">
            <div class="satir" style="padding:0 16px">
              {isk_durak()}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad aralik">
            <div class="t-h2">Son 4 hafta</div>
            {isk("136px","18px")}
          </div>
          <div class="h8"></div>
          <div class="pad">
            <div class="gun-ag">
              {''.join('<div class="gun-ag-oge"><div class="gun-kutu"></div></div>' for _ in range(28))}
            </div>
          </div>
          <div class="h24"></div>'''


units = "".join([
    device("SERİ", "E-21 · aktif seri · 12 gün", A, note=
           "<b>Üç ölçek üst üste:</b> gün sayısı (56pt) → duraklar (44pt) → 28 gün ızgarası (44pt). "
           "<b>Rozet/puan/seviye/lig yok</b> (K-048): ekran bir kupa vitrini değil çetele. "
           "Kahraman sayı <b>gün</b>dür, <code>₺</code> yoktur. <b>En uzun seri kahraman kartın "
           "içindedir</b> — kırıldığı gün kullanıcının göreceği ilk şey kaybı değil rekoru olsun. "
           "Duraklar şeridi yatay kaydırılır (8 durak 390'a sığmaz); yarım görünen 60 durağı "
           "kaydırılabildiğini söyler. 7 ↔ 14 arasındaki yol <b>%71 dolu</b>: ilerleme aralığın "
           "kendi içinde okunur, ayrı bir yüzde metni yazılmaz (Faz 1'de yüzde kullanılmaz)."),
    device("SERİ", "E-21 · seri kırıldı · suçlayıcı olmayan dil", B, note=
           "<b>Kırılma:</b> \"Seri dün kırıldı. Bugün yeniden başlıyor.\" — brandbook §2.3'ten birebir. "
           "\"Kaybettin\", \"kaçırdın\", ünlem, kırmızı ve uyarı ikonu <b>yok</b>. Sayı dürüstçe <b>0</b> "
           "yazar, gizlenmez; hemen altında rekor durur. Izgaranın son kutusu amber: kırılmanın nedeni "
           "<b>gösterilir</b>, anlatılmaz. Geri oku <b>basılı (pressed)</b> durumda."),
    device("SERİ", "E-21 · seri kapalı · limitsiz mod", C, note=
           "<b>Limitsiz mod:</b> seri işlemez (K-048). Ölü bir \"0 gün\" sayısı göstermek yerine kahraman "
           "sayı <b>hiç çizilmez</b> — ölçülecek bir eşik yok. Duraklar şeridi ve ızgara da düşer: "
           "değerlendirilmeyen günleri boş boş çizmek yalan olurdu. Tek nötr kapı: <b>ikincil</b> "
           "\"Limit belirle\" (→ E-17). Rekor yine görünür: limitten vazgeçmek geçmişi silmez."),
    device("SERİ", "E-21 · boş · henüz seri yok", D, note=
           "<b>Boş durum \"Henüz veri yok\" demez:</b> ekranın kendisi sıfır hâlidir. \"En uzun seri\" "
           "satırı <b>gizlenmez</b>, \"Henüz yok\" yazar — satırın kaybolması düzeni zıplatır. "
           "Izgara 28 çukur kutu olarak durur: dolacak yer önceden görünür. Sıradaki durak <b>3 gün</b>, "
           "ilk durağın küçük olması bilinçli (K-048 durak dizisi 3'ten başlar)."),
    device("SERİ", "E-21 · yükleniyor · iskelet", E, note=
           "<b>Yükleniyor:</b> shimmer yok, spinner yok. Bölüm başlıkları (\"Duraklar\", \"Son 4 hafta\") "
           "gerçek kalır — onlar veri değil düzendir. Gün kutusunun <b>varsayılan hâli zaten çukur</b>, "
           "bu yüzden iskelet ayrı bir kutu ailesi üretmez: aynı ızgara, içi boş."),
])

OUT.write_text(page(
    "Trinkow · Seri (E-21) — prototip v4",
    "E-21 · Seri",
    "Push ekran · seri + duraklar + son 4 hafta · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
