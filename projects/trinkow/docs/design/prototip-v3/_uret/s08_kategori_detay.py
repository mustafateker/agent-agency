# -*- coding: utf-8 -*-
"""E-15 · Kategori detayı — arketip C (Karne / tek konunun sayfası).

Mood: KARNE. Tek bir kategorinin ayını anlatır. E-14'ten ayrılan şey
**listenin sol sütunudur**: burada her satırda aynı kategori ikonu
tekrarlanmaz (13 kez aynı fincanı çizmek bilgi taşımaz), yerine **gün
kutusu** gelir — bu ekranda değişen şey kategori değil, gündür.

Ölçü nesnesi de farklıdır: E-10'un dairesel yayı değil, §7.5'teki
**kategori çubuğu** (12pt, oluk + dolgu). Kategori rengi yalnız kabında
ve çubuk dolgusunda görünür; metinde asla (tokens §1.4).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, icon, push_basi, kat_kab, ay_secici, isk, CATS)

OUT = pathlib.Path(__file__).parent.parent / "08-kategori-detay.html"

AY_KISA = "Eyl"


# ------------------------------------------------------------- kayıt satırı
def kayit_satiri(gun, saat_odeme, tutar, limit_disi=False, basili=False, not_=""):
    """Sol sütun gün kutusudur, kategori ikonu değil: bu ekranda kategori
    sabittir. Gün kutusu `clay.sunken` çukurdur — satırın kendisi kabarık,
    içindeki kutu oyuk: clay dilinde 'bu bilgi satıra gömülü' demek."""
    cls = "satir-kart" + (" limit-disi" if limit_disi else "") + (" basili" if basili else "")
    ek = ('<div class="h4"></div><div class="t-cap c-warn">limit dışı</div>'
          if limit_disi else "")
    alt = f"{saat_odeme} · {not_}" if not_ else saat_odeme
    return f'''            <div class="{cls}">
              <div class="gun-kutu">
                <div class="t-label">{gun}</div>
                <div class="t-micro">{AY_KISA}</div>
              </div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-body tek-satir">{alt}</div>
              </div>
              <div class="w12"></div>
              <div class="kolon" style="align-items:flex-end;flex:0 0 auto;white-space:nowrap">
                <div class="t-amount">{tutar}</div>
                {ek}
              </div>
            </div>'''


# ---------------------------------------------------------------- özet kartı
def ozet(ad, tutar, dolu=None, limit="", asim="", limit_yok=False,
         ortalama="", adet=""):
    """dolu: 0..100 arası oran · asim: limit üstü tutar (varsa amber taşma)."""
    if limit_yok:
        alt = f'''              <div class="h12"></div>
              <div class="t-body">Bu kategoride limit yok.</div>
              <div class="h12"></div>
              <button class="btn-secondary" style="align-self:flex-start;padding:0 24px">Limit belirle</button>'''
    else:
        renk = f"var(--{CATS[ad][1][4:].replace('kat-', '')})"
        renk = "var(--cat-" + CATS[ad][1][4:] + ")"
        if asim:
            tam = 100 + 22
            ic = round(100 * 100 / tam, 1)
            dis = round(22 * 100 / tam, 1)
            dolgu = (f'<div class="cubuk-dolgu" style="width:{ic}%;background-color:{renk}"></div>'
                     f'<div class="cubuk-dolgu" style="width:{dis}%;background-color:var(--warning)"></div>')
            sag = f'<div class="t-label c-warn">{asim}</div>'
        else:
            dolgu = f'<div class="cubuk-dolgu" style="width:{dolu}%;background-color:{renk}"></div>'
            sag = f'<div class="t-label c-2">{limit}</div>'
        alt = f'''              <div class="h12"></div>
              <div class="cubuk-oluk">{dolgu}</div>
              <div class="h4"></div>
              <div class="aralik">
                <div class="t-cap">aylık</div>
                {sag}
              </div>'''
    return f'''          <div class="pad">
            <div class="clay-lg kart-ic">
              <div class="satir">
                {kat_kab(ad)}
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-label c-2">Bu ay</div>
                  <div class="h4"></div>
                  <div class="satir" style="align-items:baseline">
                    <div class="t-display">{tutar}</div>
                    <div class="w8"></div>
                    <div class="t-amount c-2">₺</div>
                  </div>
                </div>
              </div>
{alt}
              <div class="h12"></div>
              <div class="aralik">
                <div class="t-cap">{ortalama}</div>
                <div class="t-cap">{adet}</div>
              </div>
            </div>
          </div>'''


def liste_basligi(adet):
    return f'''          <div class="pad aralik">
            <div class="t-h2">Bu ayki kayıtlar</div>
            <div class="t-label c-2">{adet}</div>
          </div>
          <div class="h8"></div>'''


def liste(satirlar):
    return f'''          <div class="pad kolon">
{'<div class="h8"></div>'.join(satirlar)}
          </div>'''


KAYITLAR = [
    kayit_satiri("10", "08.20 · Nakit", "95 ₺"),
    kayit_satiri("9", "09.40 · Kart", "78 ₺"),
    kayit_satiri("8", "08.15 · Nakit", "88 ₺"),
    kayit_satiri("6", "16.30 · Kart", "142 ₺", not_="İki kişi"),
    kayit_satiri("5", "08.05 · Nakit", "95 ₺", basili=True),
    kayit_satiri("4", "10.20 · Kart", "110 ₺"),
    kayit_satiri("3", "08.30 · Nakit", "88 ₺"),
]

# ------------------------------------------------------------------ A · dolu
A = f'''{push_basi("Kafe")}
{ay_secici("Eylül 2026", "18 kayıt")}
          <div class="h24"></div>
{ozet("Kafe", "1.840", dolu=92, limit="Aylık limit 2.000 ₺",
      ortalama="Günlük ortalama 61 ₺. Tahmini.", adet="18 kayıt")}
          <div class="h24"></div>
{liste_basligi("18 kayıt")}
{liste(KAYITLAR)}
          <div class="h24"></div>'''

# ----------------------------------------------------------- B · limit yok
B_KAYIT = [
    kayit_satiri("10", "19.30 · Kart", "640 ₺", not_="Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü"),
    kayit_satiri("7", "13.10 · Kart", "285 ₺"),
    kayit_satiri("2", "20.45 · Nakit", "410 ₺"),
    kayit_satiri("1", "12.30 · Kart", "190 ₺"),
]
B = f'''{push_basi("Restoran")}
{ay_secici("Eylül 2026", "9 kayıt")}
          <div class="h24"></div>
{ozet("Restoran", "2.960", limit_yok=True,
      ortalama="Günlük ortalama 98 ₺. Tahmini.", adet="9 kayıt")}
          <div class="h24"></div>
{liste_basligi("9 kayıt")}
{liste(B_KAYIT)}
          <div class="h24"></div>'''

# ------------------------------------------------------ C · limit aşıldı
C_KAYIT = [
    kayit_satiri("10", "21.10 · Kart", "420 ₺", limit_disi=True),
    kayit_satiri("9", "13.20 · Kart", "265 ₺"),
    kayit_satiri("7", "20.40 · Kart", "380 ₺"),
    kayit_satiri("4", "19.15 · Nakit", "225 ₺"),
    kayit_satiri("2", "12.50 · Kart", "160 ₺"),
]
C = f'''{push_basi("Market")}
{ay_secici("Eylül 2026", "24 kayıt")}
          <div class="h24"></div>
{ozet("Market", "3.660", asim="Aylık limitin 660 ₺ üzerinde",
      ortalama="Günlük ortalama 122 ₺. Tahmini.", adet="24 kayıt")}
          <div class="h24"></div>
{liste_basligi("24 kayıt")}
{liste(C_KAYIT)}
          <div class="h24"></div>'''

# ------------------------------------------------------------------ D · boş
D = f'''{push_basi("Kafe")}
{ay_secici("Temmuz 2026", "0 kayıt")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay-lg kart-ic kolon orta">
              <div class="hero-daire hero-daire-bos hero-bos" style="width:176px;height:176px">
                <div class="hero-orta">
                  <div class="kat-kab kat-amber">{icon("coffee")}</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-h2">Kafe için kayıt yok</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Bu ay bu kategoride harcama yazmadın.</div>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- E · yükleniyor
E = f'''{push_basi("Kafe")}
{ay_secici("Eylül 2026", "18 kayıt")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay-lg kart-ic">
              <div class="satir">
                {isk("44px", "44px", "16px")}
                <div class="w12"></div>
                <div class="esnek kolon">
                  {isk("52px", "18px")}
                  <div class="h4"></div>
                  {isk("136px", "38px")}
                </div>
              </div>
              <div class="h12"></div>
              {isk("100%", "12px")}
              <div class="h4"></div>
              {isk("148px", "18px")}
              <div class="h12"></div>
              {isk("196px", "18px")}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad aralik">
            {isk("160px", "25px")}
            {isk("64px", "18px")}
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
            {'<div class="h8"></div>'.join(f'<div class="clay-tile" style="padding:12px 16px"><div class="satir">{isk("44px", "44px", "16px")}<div class="w12"></div><div class="esnek">{isk("152px", "24px")}</div><div class="w12"></div>{isk("72px", "24px")}</div></div>' for _ in range(4))}
          </div>
          <div class="h24"></div>'''


units = "".join([
    device("KATEGORİ DETAYI", "E-15 · dolu (limit var)", A, note=
           "<b>Mood: karne.</b> Sol sütun gün kutusudur — aynı kategori ikonunu 18 kez tekrarlamak bilgi "
           "taşımaz, burada değişen gündür. Kategori kimliği <b>tek yerde</b> durur: özet kartındaki kap. "
           "Ölçü nesnesi dairesel yay değil <b>kategori çubuğu</b>; iki ekran aynı grafiği paylaşmaz. "
           "\"Günlük ortalama 61 ₺. <b>Tahmini.</b>\" — ürün tahminini tahmin olarak etiketler."),
    device("KATEGORİ DETAYI", "E-15 · kategori limiti yok", B, note=
           "<b>Limit yoksa çubuk çizilmez.</b> Boş bir oluk göstermek \"burada bir eksik var\" der; oysa "
           "limitsiz izlemek geçerli bir kullanımdır. Yerine tek cümle + <b>ikincil</b> buton gelir: "
           "birincil buton olsaydı ürün limit koymaya bastırmış olurdu. En uzun not dizesi (60 karakter) "
           "bu yüzeyde test edilir: satır tek satırda kırpılır, tutar sütunu kaymaz."),
    device("KATEGORİ DETAYI", "E-15 · kategori limiti aşıldı", C, note=
           "<b>Aşım amberdir, kırmızı değildir.</b> Çubuk %100'de renk değiştirmez; limitin üzerine "
           "<b>ikinci bir dolgu</b> eklenir ve oluk artık toplamı temsil eder. Sayı verilir: \"Aylık limitin "
           "660 ₺ üzerinde\". Aşıma sebep olan satır amber zeminlidir ama ünlem, üstü çizili yazı ve "
           "kırmızı yoktur — kullanıcı utandırılmaz."),
    device("KATEGORİ DETAYI", "E-15 · boş (bu ay kayıt yok)", D, note=
           "<b>Boş durum kategoriye özgüdür:</b> illüstrasyonun ortasında o kategorinin kendi ikonu ve "
           "rengi durur, genel bir kutu değil. Buton <b>yok</b> — kullanıcı buraya harcama eklemeye değil "
           "bakmaya geldi; ay değiştirici zaten yukarıda duruyor. \"Henüz veri yok\" yazılmaz."),
    device("KATEGORİ DETAYI", "E-15 · yükleniyor", E, note=
           "<b>İskelet gerçek düzendir:</b> özet kartı, çubuk ve dört satır yerinde durur, içleri çukur "
           "bloklara döner. Ay değiştirici ve başlık <b>gerçek veriyle</b> gelir (zaten biliniyorlar) — "
           "bilinen bir şeyi iskelete çevirmek sahte bir bekleme üretir. Shimmer ve tam ekran spinner yok."),
])

OUT.write_text(page(
    "Trinkow · Kategori detayı — prototip v3",
    "E-15 · Kategori detayı",
    "Arketip C — Karne · push · kategori çubuğu · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
