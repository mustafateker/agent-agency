# -*- coding: utf-8 -*-
"""E-17 · Limitler — arketip E (Form / ayar masası).

Mood (ekran-envanteri §6): AYAR MASASI. Her satır **tek bir karar**, açıklama
`caption`, ekranda 56pt kahraman sayı YOKTUR — burada sayıya bakılmaz, sayı
**değiştirilir**. E-10'un tek büyük nesnesinin ve E-14'ün defter ritminin
tersine, bu ekranın ritmi "etiket → değer → açıklama" üçlüsüdür.

Kil tuş takımı (tokens §7.11) burada da kullanılır: sistem klavyesi açılmaz,
düzen zıplamaz, "Kaydet" daima tuşların altında sabit durur.

Limit kaldırma **ayrı bir onay istemez** (K-029 ilkesi: etkiye göre): limit
kaldırmak veri silmez, takip durur ve tek dokunuşla geri konur.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, page, icon, push_basi, kat_kab, tus_takimi,
                 kaydet, isk, CATS)

OUT = pathlib.Path(__file__).parent.parent / "09-limitler.html"


# ------------------------------------------------------------ günlük limit
def gunluk_karti(deger="300", basili=False, secili=False, iskelet=False):
    b = " basili" if basili else ""
    ic = (f'<div class="esnek satir" style="align-items:baseline">'
          f'<div class="t-display">{deger}</div><div class="w8"></div>'
          f'<div class="t-amount c-2">₺</div></div>'
          f'{icon("pencil")}')
    kuyu = (f'<button class="kuyu-btn{b}" aria-label="Günlük limiti değiştir">{ic}</button>')
    if secili:
        kuyu = (f'<div class="kuyu-btn" style="box-shadow:var(--clay-sunken), 0 0 0 2px var(--primary-text)">'
                f'<div class="esnek satir" style="align-items:baseline"><div class="t-display">{deger}</div>'
                f'<div class="w8"></div><div class="t-amount c-2">₺</div></div>'
                f'<div class="imlec"></div></div>')
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="t-h2">Günlük limit</div>
              <div class="h8"></div>
              <div class="t-cap">Her gün sıfırlanır. Aylık plan değildir.</div>
              <div class="h12"></div>
              {kuyu}
            </div>
          </div>'''


# -------------------------------------------------------- kategori limitleri
def kat_limit_satiri(ad, deger, basili=False, hatali=False, hata=""):
    """Tek karar satırı: kategori + aylık limit değeri. Değer yoksa 'Limit yok'
    yazılır — boş bir kutu bırakmak kullanıcıya 'doldurman gerek' dedirtir;
    limitsiz kalmak geçerli bir seçimdir (brandbook: zorlamayan ton)."""
    b = " basili" if basili else ""
    h = " hatali" if hatali else ""
    # "Limit yok" bir placeholder değil, geçerli bir DEĞERdir → `text-3`
    # (placeholder rengi) kullanılmaz; `well` üzerinde 4.50 sınırda kalırdı.
    sag = (f'<div class="t-amount">{deger}</div>' if deger
           else '<div class="t-cap c-2">Limit yok</div>')
    hata_html = (f'<div class="h8"></div><div class="t-cap c-danger">{hata}</div>'
                 if hata else '')
    return f'''            <div class="kolon">
                <button class="kuyu-btn{b}{h}" aria-label="{ad} limitini değiştir">
                  {kat_kab(ad)}
                  <div class="w12"></div>
                  <div class="esnek t-strong">{ad}</div>
                  <div class="w12"></div>
                  {sag}
                  <div class="w12"></div>
                  {icon("chevron-right")}
                </button>
                {hata_html}
              </div>'''


def kat_karti(satirlar, notu=""):
    """Kategori limitleri kart İÇİNDE değil, §7.3 uyarınca **ayrı kabarık
    satırlar** olarak dizilir: 13 kategorilik uzun bir listeyi tek kartın
    içine hapsetmek kartı ekrandan taşırır, kaydırma ipucunu öldürür.
    Başlık satırı sağında "Aylık" etiketi durur — periyodu satır satır
    tekrar etmeye gerek kalmaz."""
    ic = '<div class="h8"></div>'.join(satirlar)
    not_html = (f'''          <div class="h24"></div>
          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-cap">{notu}</div>
                <div class="h4"></div>
                <div class="t-cap">Boş bırakılan kategori takip edilmez.</div>
              </div>
            </div>
          </div>''' if notu else '')
    return f'''          <div class="pad aralik">
            <div class="t-h2">Kategori limitleri</div>
            <div class="t-label c-2">Aylık</div>
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
{ic}
          </div>
{not_html}'''


def alt(kaydet_durum="aktif"):
    return f'''          <div class="alt-sabit">
            <div class="pad">{kaydet(kaydet_durum)}</div>
          </div>
'''


def liste(*ozel):
    """13 kategorinin tamamı listelenir; ilk beşi ekranda görünür.
    `ozel` sözlüğü verilen kategorinin satırını değiştirir."""
    ayar = dict(ozel)
    tam = ["Market", "Kafe", "Restoran", "Ulaşım", "Akaryakıt", "Fatura",
           "Kira ve ev", "Abonelik", "Sağlık", "Giyim", "Eğlence",
           "Alışkanlıklar", "Diğer"]
    # Gerçekçi değerler: günlük 300 ₺ ≈ aylık 9.000 ₺. Kategori toplamı
    # 7.500 ₺ — günlük limitle çelişmez. Çelişki durumu C yüzeyinde.
    varsayilan = {"Market": "3.000 ₺", "Kafe": "1.200 ₺", "Ulaşım": "900 ₺",
                  "Fatura": "2.400 ₺"}
    out = []
    for ad in tam:
        if ad in ayar:
            out.append(ayar[ad])
        else:
            out.append(kat_limit_satiri(ad, varsayilan.get(ad, "")))
    return out


SATIRLAR = liste()

# ------------------------------------------------------------------ A · dolu
A = f'''{push_basi("Limitler")}
{gunluk_karti()}
          <div class="h24"></div>
{kat_karti(SATIRLAR, "Kategori limitleri toplamı 7.500 ₺. Günlük limitinle karşılaştır.")}
          <div class="h24"></div>'''

# ------------------------------------ B · günlük limit düzenleniyor (tuş takımı)
B = f'''{push_basi("Günlük limit")}
          <div class="pad">
            <div class="clay kart-ic">
              <div class="t-cap">Her gün sıfırlanır. Aylık plan değildir.</div>
              <div class="h12"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="satir" style="justify-content:center;align-items:baseline">
                  <div class="t-hero">340</div>
                  <div class="w4"></div>
                  <div class="t-hero-simge c-2">₺</div>
                  <div class="w8"></div>
                  <div class="imlec"></div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-cap">Şu anki limitin 300 ₺.</div>
            </div>
          </div>
          <div class="h24"></div>'''

B_ALT = f'''          <div class="alt-sabit">
{tus_takimi(basili_tus="4")}
            <div class="h12"></div>
            <div class="pad">{kaydet()}</div>
          </div>
'''

# --------------------------------------------------- C · geçersiz değer hatası
C_SATIRLAR = liste(
    ("Market", kat_limit_satiri("Market", "9.000 ₺")),
    ("Kafe", kat_limit_satiri("Kafe", "0 ₺", hatali=True,
                              hata="Limit sıfırdan büyük olmalı. Takip istemiyorsan limiti kaldır.")),
)
C = f'''{push_basi("Limitler")}
{gunluk_karti()}
          <div class="h24"></div>
{kat_karti(C_SATIRLAR, "Kategori limitleri toplamı 13.500 ₺. Günlük limitinle karşılaştır.")}
          <div class="h24"></div>'''

# ------------------------------------------------------- D · Kaydet loading
D = f'''{push_basi("Limitler")}
{gunluk_karti("340")}
          <div class="h24"></div>
{kat_karti(SATIRLAR, "Kategori limitleri toplamı 7.500 ₺. Günlük limitinle karşılaştır.")}
          <div class="h24"></div>'''

# ------------------------------------------------------------ E · limit kaldırma
E_SATIRLAR = liste(("Kafe", f'''            <div class="kolon">
                <div class="kuyu-btn" style="box-shadow:var(--clay-sunken), 0 0 0 2px var(--primary-text)">
                  {kat_kab("Kafe")}
                  <div class="w12"></div>
                  <div class="esnek t-strong">Kafe</div>
                  <div class="w12"></div>
                  <div class="t-amount">1.200 ₺</div>
                  <div class="w8"></div>
                  <div class="imlec"></div>
                </div>
                <div class="h8"></div>
                <button class="btn-ghost basili" style="padding:0 16px;align-self:flex-start" aria-label="Kafe limitini kaldır">{icon("circle-slash")}<div class="w8"></div>Limiti kaldır</button>
              </div>'''))
E = f'''{push_basi("Limitler")}
{gunluk_karti()}
          <div class="h24"></div>
{kat_karti(E_SATIRLAR, "Kategori limitleri toplamı 7.500 ₺. Günlük limitinle karşılaştır.")}
          <div class="h24"></div>'''

# ------------------------------------------------------------ F · limit kaldırıldı
F_SATIRLAR = liste(("Kafe", kat_limit_satiri("Kafe", "")))
F = f'''          <div class="h8"></div>
          <div class="pad">
            <div class="toast">
              <div class="nokta"></div>
              <div class="w12"></div>
              <div class="esnek t-body">Kafe limiti kaldırıldı</div>
              <div class="w12"></div>
              <button class="btn-ghost" style="padding:0 16px;height:44px;flex:0 0 auto">Geri al</button>
            </div>
          </div>
          <div class="h12"></div>
{push_basi("Limitler")}
{gunluk_karti()}
          <div class="h24"></div>
{kat_karti(F_SATIRLAR, "Kategori limitleri toplamı 6.300 ₺. Günlük limitinle karşılaştır.")}
          <div class="h24"></div>'''

# ------------------------------------------------------------ G · yükleniyor
G = f'''{push_basi("Limitler")}
          <div class="pad">
            <div class="clay kart-ic">
              {isk("112px", "18px")}
              <div class="h8"></div>
              {isk("214px", "18px")}
              <div class="h12"></div>
              {isk("100%", "64px", "16px")}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic">
              {isk("148px", "25px")}
              <div class="h8"></div>
              {isk("196px", "18px")}
              <div class="h12"></div>
              {isk("100%", "68px", "16px")}
              <div class="h12"></div>
              {isk("100%", "68px", "16px")}
              <div class="h12"></div>
              {isk("100%", "68px", "16px")}
            </div>
          </div>
          <div class="h24"></div>'''


# ------------------------------------------- H · hiç kategori limiti yok (boş)
# ekran-envanteri §5, E-17 satırı: "boş = kategori limiti hiç yok".
# Ton kararı: bu bir EKSİKLİK DEĞİL, geçerli bir seçim. Bu yüzden
#   · bilgi şeridi YOK (toplayacak limit yok, söylenecek hesap yok),
#   · birincil buton YOK (ekranın birincil eylemi "Kaydet"tir),
#   · günlük limit kartı yerinde durur — boş olan yalnız kategori bölümü.
KAT_BOS = f"""          <div class="pad aralik">
            <div class="t-h2">Kategori limitleri</div>
            <div class="t-label c-2">Aylık</div>
          </div>
          <div class="h8"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="t-body">Kategori limiti koymak zorunda değilsin. Günlük limit tek başına çalışır.</div>
              <div class="h12"></div>
              <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px" aria-label="Kategori limiti ekle">{icon("plus")}<div class="w8"></div>Kategori limiti ekle</button>
            </div>
          </div>"""

H = f'''{push_basi("Limitler")}
{gunluk_karti()}
          <div class="h24"></div>
{KAT_BOS}
          <div class="h24"></div>'''


units = "".join([
    device("LİMİTLER", "E-17 · dolu (düzenleme)", A, sabit_alt=alt(), note=
           "<b>Mood: ayar masası.</b> Her satır tek karar: kategori · aylık limit. Limiti olmayan kategori "
           "boş kutu göstermez, <b>\"Limit yok\"</b> yazar — limitsiz kalmak geçerli bir seçimdir, eksik bir "
           "durum değil. Mavi bilgi şeridi toplamı <b>söyler ama yargılamaz</b>: \"Günlük limitinle "
           "karşılaştır.\" Karar kullanıcınındır; ürün hesabı yapar, hükmü vermez."),
    device("LİMİTLER", "E-17 · boş · hiç kategori limiti yok", H, sabit_alt=alt("pasif"), note=
           "<b>Boş durum, eksik durum değil.</b> Kategori bölümünde <b>bilgi şeridi yok</b>: toplanacak "
           "limit olmadığı için söylenecek bir hesap da yok — boş bir şeridi \"0 ₺\" ile doldurmak "
           "kullanıcıya borç hissettirir. Tek cümle + <b>ikincil</b> buton: birincil buton ekranda "
           "zaten \"Kaydet\"tir (ekran başına en fazla 1 birincil). <b>Günlük limit kartı yerinde durur</b> "
           "— limitsiz olan kategoriler, kullanıcının günlük limiti değil. Kaydet <b>pasif</b>: henüz "
           "değişen bir değer yok.<br /><b>Diğer boş durumlardan farkı:</b> E-10 ilk günün yay "
           "illüstrasyonu ve E-14'ün \"Kayıt yok\" başlığı burada tekrar edilmez — bu bir bölüm boşluğu, "
           "ekran boşluğu değil, o yüzden başlık ve illüstrasyon almaz."),
    device("LİMİTLER", "E-17 · günlük limit · kil tuş takımı", B, sabit_alt=B_ALT, note=
           "<b>Sistem klavyesi açılmaz</b> (tokens §7.11): düzen zıplamaz, \"Kaydet\" tuşların altında sabit "
           "kalır. Ekrandaki tek 56pt sayı düzenlenen değerdir. Altındaki <b>\"Şu anki limitin 300 ₺.\"</b> "
           "satırı bilinçli: kullanıcı neyi neyle değiştirdiğini görmeden kaydetmez. Geri oku sol üstte, "
           "kritik hedef değil."),
    device("LİMİTLER", "E-17 · geçersiz değer", C, sabit_alt=alt(), note=
           "<b>Hata satırın altında, kırmızı kenarlıkla.</b> \"Geçersiz\" veya \"Hata:\" yazılmaz; "
           "ne olduğu + <b>çıkış yolu</b> verilir: \"Takip istemiyorsan limiti kaldır.\" 0 ₺ bir limit değil, "
           "sessiz bir kilittir — kullanıcı her harcamada limit dışına düşerdi. Diğer satırlar bozulmaz, "
           "Kaydet pasifleşmez: kullanıcı düzeltmeden kaydetmeye çalışırsa aynı satıra döner."),
    device("LİMİTLER", "E-17 · Kaydet loading", D, sabit_alt=alt("loading"), note=
           "<b>Kaydediliyor:</b> buton genişliği sabit, sağda 20pt spinner, opaklık yok. Ekran kilitlenmez, "
           "tam ekran spinner yoktur. Günlük limit alanı yeni değeri (340 ₺) zaten gösterir — yazma "
           "başarısız olursa kullanıcı ne yazdığını görmeye devam eder."),
    device("LİMİTLER", "E-17 · limit kaldırma", E, sabit_alt=alt(), note=
           "<b>Kaldırma onay istemez</b> (K-029 ilkesi: etkiye göre). Limit kaldırmak <b>veri silmez</b>, "
           "yalnız takibi durdurur ve tek dokunuşla geri konur. Bu yüzden kırmızı buton, diyalog ve "
           "\"emin misin\" yoktur; eylem seçili satırın altında açılır ve yalnız o satıra aittir."),
    device("LİMİTLER", "E-17 · kaldırıldı + geri al", F, sabit_alt=alt(), note=
           "<b>Sonuç anlatılmıyor, gösteriliyor:</b> Kafe satırı \"Limit yok\"a döndü, toplam notu "
           "5.100 → 3.900 ₺ oldu. Toast göstergesi <b>mavi</b>: bu yıkıcı bir işlem değil. 6 sn'lik geri alma "
           "penceresi toast'ın ömrüyle birebir aynıdır."),
    device("LİMİTLER", "E-17 · yükleniyor", G, sabit_alt=alt("pasif"), note=
           "<b>İskelet gerçek düzenin kendisidir:</b> kartlar yerinde durur, içleri çukur bloklara döner. "
           "Parıldama (shimmer) ve dönen spinner yok. Kaydet pasif — henüz kaydedilecek bir değer yok; "
           "pasiflik opaklıkla değil, çukur gölge + <code>disabled-bg</code> ile verilir."),
])

OUT.write_text(page(
    "Trinkow · Limitler — prototip v3",
    "E-17 · Limitler",
    "Arketip E — Form / ayar masası · push · kil tuş takımı · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
