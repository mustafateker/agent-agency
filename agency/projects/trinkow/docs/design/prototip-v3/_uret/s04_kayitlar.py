# -*- coding: utf-8 -*-
"""E-14 · Kayıtlar — arketip A (Feed / liste).
Mood: DEFTER. Gün başlıkları listeyi böler, kart yoktur; sık dikey ritim,
her satır kendi kabarık yüzeyi. E-10'un tek büyük nesnesinin tam tersi:
burada ekranda 56pt sayı YOKTUR, ağırlık merkezi listenin kendisidir.

Sapma notu: ekran-envanteri §6 bu ekran için "1px ayraç + yapışkan gün
başlığı" diyordu. v3 clay dilinde satır ayracı gölgedir (tokens §7.3) ve
`sticky` <main> içinde yasaktır (rn-tasarim-kisitlari). Defter hissi
bunun yerine sık ritim + kartsız gün başlığı ile kuruldu.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, satir, sekme_cubugu, icon, ay_secici,
                 gun_basligi, isk)

OUT = pathlib.Path(__file__).parent.parent / "04-kayitlar.html"


def basi(sag_basili=False):
    b = " basili" if sag_basili else ""
    return f'''          <div class="ekran-basi">
            <div class="t-h1">Kayıtlar</div>
            <button class="ikon-btn{b}" aria-label="Taksitli işlemleri aç">{icon("repeat")}</button>
          </div>'''


def grup(gun, toplam, satirlar, limit_disi=""):
    ic = '<div class="h8"></div>'.join(satirlar)
    return f'''{gun_basligi(gun, toplam, limit_disi)}
          <div class="h8"></div>
          <div class="pad kolon">
            {ic}
          </div>'''


# ---------------------------------------------------------------- A · dolu
# Gün başlığı kuralı: sağ taraf DAİMA günlük toplamı gösterir. Gün limit
# dışıysa toplam `warning-ink` olur ve yanına birebir "limit dışı" sözcüğü
# eklenir (tokens §1.5 — amber sinyali daima bu sözcükle gelir).
A = f'''{basi()}
{ay_secici("Eylül 2026", "48 kayıt · 12.480 ₺")}
          <div class="h24"></div>
{grup("Bugün · 10 Eylül", "Günlük toplam 180 ₺", [
    satir("Kafe", "08.20 · Nakit", "95 ₺"),
    satir("Ulaşım", "09.05 · Kart", "42 ₺"),
    satir("Market", "18.40 · Kart", "43 ₺"),
])}
          <div class="h24"></div>
{grup("Dün · 9 Eylül", "", [
    satir("Restoran", "21.30 · Kart · Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü", "640 ₺", limit_disi=True),
    satir("Market", "11.20 · Kart", "180 ₺"),
], limit_disi="820 ₺ · limit dışı")}
          <div class="h24"></div>
{grup("8 Eylül Salı", "Günlük toplam 298 ₺", [
    satir("Fatura", "19.00 · Kart", "210 ₺"),
    satir("Kafe", "08.15 · Nakit", "88 ₺"),
])}
          <div class="h24"></div>
{grup("7 Eylül Pazartesi", "Günlük toplam 265 ₺", [
    satir("Akaryakıt", "17.10 · Kart", "177 ₺", basili=True),
    satir("Sağlık", "12.15 · Nakit", "88 ₺"),
])}
          <div class="h24"></div>'''

# --------------------------------------------------------- B · 200+ kayıt
# En uzun tutar testi (metinler.md §19) burada: 1.250.000,50 ₺ — tek seferlik
# büyük harcama. Sağ sütun tabular olduğu için hizalama bozulmaz.
uzun_gunler = []
_veri = [
    ("31 Ağustos Pazartesi", "Günlük toplam 512 ₺", "",
     [("Restoran", "20.10 · Kart", "312 ₺", False),
      ("Kafe", "15.30 · Nakit", "120 ₺", False),
      ("Eğlence", "13.00 · Kart", "80 ₺", False)]),
    ("30 Ağustos Pazar", "", "1.250.620 ₺ · limit dışı",
     [("Diğer", "13.05 · Kart · Araç alımı, tek seferlik", "1.250.000,50 ₺", True),
      ("Market", "11.20 · Kart", "620 ₺", False)]),
    ("29 Ağustos Cumartesi", "", "940 ₺ · limit dışı",
     [("Giyim", "16.45 · Kart", "690 ₺", True),
      ("Market", "11.00 · Kart", "180 ₺", False),
      ("Kafe", "09.10 · Nakit", "70 ₺", False)]),
    ("28 Ağustos Cuma", "Günlük toplam 176 ₺", "",
     [("Alışkanlıklar", "22.00 · Nakit", "96 ₺", False),
      ("Ulaşım", "08.50 · Kart", "80 ₺", False)]),
]
for g, t, ld, rows in _veri:
    uzun_gunler.append(grup(g, t, [satir(a, b, c, limit_disi=d) for a, b, c, d in rows], limit_disi=ld))

B = f'''{basi()}
{ay_secici("Ağustos 2026", "214 kayıt · 38.920 ₺", sol_basili=True)}
          <div class="h24"></div>
{'''
          <div class="h24"></div>
'''.join(uzun_gunler)}
          <div class="h24"></div>'''

# --------------------------------------------------- C · boş (hiç kayıt yok)
C = f'''{basi()}
          <div class="pad">
            <div class="clay-lg kart-ic kolon orta">
              <div class="hero-daire hero-daire-bos hero-bos" style="width:176px;height:176px">
                <div class="hero-orta">
                  <div class="ikon-kutu ikon-kutu-32" style="color:var(--text-2)">{icon("notebook-text")}</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-h2">Kayıt yok</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Aşağıdaki butonla ilkini ekle.</div>
              <div class="h12"></div>
              <button class="btn-primary" aria-label="Harcama ekle">{icon("plus")}<div class="w8"></div>Harcama ekle</button>
            </div>
          </div>
          <div class="h24"></div>'''

# ------------------------------------------------------------- C2 · ay boş
C2 = f'''{basi()}
{ay_secici("Temmuz 2026", "0 kayıt")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon orta">
              <div class="hata-daire">{icon("calendar-days")}</div>
              <div class="h12"></div>
              <div class="t-h2">Bu ayda kayıt yok</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Başka bir ay seçebilirsin.</div>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- D · yükleniyor
def isk_satir(w1, w2):
    return (f'<div class="satir-kart">{isk("44px","44px","16px")}<div class="w12"></div>'
            f'<div class="esnek kolon">{isk(w1,"16px")}<div class="h8"></div>{isk(w2,"12px")}</div>'
            f'<div class="w12"></div>{isk("72px","20px")}</div>')


def isk_grup(genislikler):
    ic = '<div class="h8"></div>'.join(isk_satir(a, b) for a, b in genislikler)
    return f'''          <div class="pad aralik">
            {isk("140px","18px")}
            {isk("104px","18px")}
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
            {ic}
          </div>'''


D = f'''{basi()}
          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="aralik">
                {isk("44px","44px")}
                <div class="kolon orta">{isk("104px","20px")}<div class="h4"></div>{isk("136px","16px")}</div>
                {isk("44px","44px")}
              </div>
            </div>
          </div>
          <div class="h24"></div>
{isk_grup([("62%", "40%"), ("48%", "34%"), ("55%", "44%")])}
          <div class="h24"></div>
{isk_grup([("58%", "38%"), ("44%", "30%")])}
          <div class="h24"></div>'''

# ----------------------------------------------------------------- E · hata
E = f'''{basi()}
{ay_secici("Eylül 2026", "48 kayıt · 12.480 ₺")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon orta">
              <div class="hata-daire">{icon("refresh")}</div>
              <div class="h12"></div>
              <div class="t-h2">Kayıtlar açılamadı</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Bir şey ters gitti. Yeniden denemek çoğu zaman yeterli.</div>
              <div class="h12"></div>
              <button class="btn-primary" aria-label="Yeniden dene">{icon("refresh")}<div class="w8"></div>Yeniden dene</button>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad kolon">
            <div class="satir-kart">
              <div class="kat-kab kat-duman">{icon("circle-dashed")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-body c-2">Eylül kayıtları</div>
                <div class="t-cap tek-satir">Liste açılınca burada görünür.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

units = "".join([
    device("KAYITLAR", "dolu · uzun tutar · taksit", A, sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>Mood: defter.</b> E-10 tek büyük nesne kurar; burada 56pt sayı <b>yoktur</b>, ekranın ritmi "
           "listenin kendisidir. Gün başlığı kart değil, listeyi bölen tek satırdır — RN'de FlatList'in normal "
           "öğesi, <b>yapışkan değil</b> (<code>sticky</code> yasak). <b>Para sütunu:</b> tutarlar sağa hizalı, "
           "Montserrat <code>tabular-nums</code>, sol metin kırpılır (<code>numberOfLines=1</code>). "
           "<b>Gün başlığı kuralı:</b> sağda daima günlük toplam; gün limit dışıysa toplam amber olur ve "
           "yanına birebir \"limit dışı\" yazılır — amber hiçbir yerde yalnız başına anlam taşımaz."),
    device("KAYITLAR", "önceki ay · 214 kayıt (FlatList)", B, sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>200+ kayıt:</b> tek <code>FlatList</code>, gün başlıkları da liste öğesidir (<code>SectionList</code> "
           "yerine düz veri + tip alanı — <code>getItemLayout</code> ile sabit yükseklik hesaplanabilsin diye). "
           "<code>initialNumToRender=12</code> · <code>windowSize=7</code> · <code>removeClippedSubviews</code>. "
           "Kaydırma <b>sonsuz değil</b>: ay sınırında biter, sonraki aya ok tuşuyla geçilir — konum kaybolmaz. "
           "Önceki ay okunda <b>basılı</b> durum görülüyor. <b>En uzun tutar testi burada:</b> "
           "<code>1.250.000,50 ₺</code> 17pt tabular ile taşmadan sığar; aynı sütundaki 70 ₺ ile ondalık "
           "hizası bozulmaz."),
    device("KAYITLAR", "boş · hiç kayıt yok", C, sabit_alt=sekme_cubugu("kayitlar", fab=False), note=
           "<b>Boş durum (ilk kullanım):</b> ay değiştirici <b>gizlenir</b> — seçilecek ay yokken boş bir kontrol "
           "göstermek yalan olur. İllüstrasyon E-10'un yayı değil, çukur defter dairesi: her boş ekran farklı. "
           "FAB düşer, ekranın tek birincil eylemi karttaki butondur."),
    device("KAYITLAR", "boş · seçili ayda kayıt yok", C2, sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>İkinci boş durum, farklı cümle:</b> kullanıcının kaydı var ama bu ayda yok. Ay değiştirici "
           "<b>kalır</b> (çözüm orada), buton yoktur — eylem zaten üstteki oktur. \"Henüz veri yok\" hiçbir "
           "yerde yazılmaz."),
    device("KAYITLAR", "yükleniyor · iskelet", D, sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>Yükleniyor:</b> gerçek düzenin kabarık kutuları yerinde kalır, içleri çukur bloklara döner. "
           "Shimmer/spinner yok. Satır sayısı son bilinen gün yapısına göre çizilir — liste gelince zıplama olmaz. "
           "150ms'den kısa okumalarda iskelet <b>hiç gösterilmez</b>."),
    device("KAYITLAR", "okuma hatası", E, sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>Hata:</b> depolama/mimari anlatılmaz, ne yapılacağı söylenir. Ay değiştirici <b>etkin kalır</b> — "
           "başka ay denemek gerçek bir çıkış yoludur. Altta kapalı bir yer tutucu satır, listenin nereye "
           "geleceğini gösterir."),
])

OUT.write_text(page(
    "Trinkow · Kayıtlar — prototip v3",
    "E-14 · Kayıtlar",
    "Arketip A — Feed / liste · mood: defter · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
