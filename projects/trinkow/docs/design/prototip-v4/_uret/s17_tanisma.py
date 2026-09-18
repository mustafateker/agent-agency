# -*- coding: utf-8 -*-
"""E-25 · "Seni tanıyalım" — **KATMAN 2** (K-053) · arketip C+E melezi.

Mood: SORUŞTURMA DEĞİL, SOHBET. Katman 1 bir kurulumdu (ilerleme çubuğu,
"Adım 1/3", geri dönüşü olmayan bir hat). Burası farklı: **hiçbir kart
zorunlu değil**, her kartta "Bu kartı atla" görünür, akış her an bırakılır
ve kaldığı yerden devam eder. Bu yüzden görsel ritim de farklıdır:
Katman 1'de ekranı bir soru doldurur, burada **bir kart** doldurur —
kartın içinde etiket, seçim ve anında geri bildirim vardır.

Sekiz kart (K-053):
  1/8 sabit giderler (kira-aidat · faturalar · ulaşım-yakıt · kredi-taksit)
  2/8 kahve · 3/8 sigara · 4/8 alkol · 5/8 dışarıda yemek · 6/8 abonelikler
  7/8 yatırım niyeti · 8/8 birikim hedefi

İKİ BAĞLAYICI YASAK BU EKRANIN TASARIMINI BELİRLEDİ:
  · **Fiyat uydurma YOK (K-050).** Hiçbir kartta hazır fiyat, "ortalama
    kahve 85 ₺" gibi bir varsayım ya da önceden seçili tutar yoktur.
    Fiyat alanı boş açılır ve kullanıcının kendi fiyatını bekler.
  · **Yargılayan dil YOK.** Sigara ve alkol kartları diğer kartlarla
    birebir aynı biçimde, aynı puntoyla, aynı tonla durur; uyarı rengi,
    sağlık mesajı, "bırakmayı düşündün mü" sorusu yoktur. Ürün ayna
    tutar, ders vermez (brandbook: farkındalık veren, utandıran değil).

Sıklık girişi **ayrık seçeneklerle** başlar ("Günde 1", "Haftada 2-3",
"Hiç"); serbest sayı **en son** seçenektir. Tersi olsaydı her kullanıcı
klavye açmak zorunda kalırdı (F-2 sürtünme kuralı).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, icon, tus_takimi, ilerleme, kuyu_deger,
                 sik_cipleri, kaydirici, tl, ikon_kab)

OUT = pathlib.Path(__file__).parent.parent / "17-tanisma.html"

SIKLIK = ["Günde 1", "Günde 2", "Haftada 2-3", "Haftada 1", "Ayda 1-2", "Hiç",
          "Kendim yazayım"]


# ------------------------------------------------------------------ kabuk
def basi(kapat=True):
    kapat_html = (f'<button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>'
                  if kapat else '<div style="width:44px;height:44px"></div>')
    return f'''            <div class="ekran-basi">
              <button class="ikon-btn" aria-label="Geri dön">{icon("chevron-left")}</button>
              <div class="t-micro">Seni tanıyalım</div>
              {kapat_html}
            </div>'''


def kart(baslik, ikon_ad, ic, aciklama=""):
    ac = f'''                <div class="h8"></div>
                <div class="t-cap">{aciklama}</div>''' if aciklama else ""
    return f'''            <div class="pad">
              <div class="clay kart-ic kolon">
                <div class="satir">
                  {ikon_kab(ikon_ad)}
                  <div class="w16"></div>
                  <div class="esnek t-h2">{baslik}</div>
                </div>{ac}
                <div class="h16"></div>
{ic}
              </div>
            </div>'''


def alt(birincil="Devam", atla="Bu kartı atla", atla_basili=False,
        pasif=False, klavye=False):
    b = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
         f'{birincil}</button>' if pasif else f'<button class="btn-primary">{birincil}</button>')
    ab = " basili" if atla_basili else ""
    atla_html = (f'''              <div class="h8"></div>
              <button class="btn-ghost{ab}" style="width:100%">{atla}</button>''' if atla else "")
    tus = f'{tus_takimi()}\n            <div class="h12"></div>\n' if klavye else ""
    return f'''          <div class="alt-sabit">
{tus}            <div class="pad kolon">
              {b}
{atla_html}
            </div>
          </div>'''


def ayna(tutar, formul):
    """Kartın içindeki **anında geri bildirim**: girilen sıklık × kullanıcının
    kendi fiyatı. Plan ekranını beklemeden aynayı burada tutuyoruz; sorunun
    karşılığı görünmezse bir sonraki kart cevaplanmaz (E-20'nin dersi)."""
    return f'''                <div class="clay-kuyu kolon" style="padding:12px 16px">
                  <div class="aralik">
                    <div class="t-strong">Ayda</div>
                    <div class="t-amount">{tutar}</div>
                  </div>
                  <div class="h4"></div>
                  <div class="t-cap">{formul}</div>
                </div>'''


# ----------------------------------------------------------- A · kapı (E-25)
A = f'''{basi()}
            <div class="h24"></div>
            <div class="pad kolon">
              <div class="t-h1">Seni tanıyalım</div>
              <div class="h8"></div>
              <div class="t-body c-2">Sekiz kart. Her birini atlayabilirsin.</div>
            </div>
            <div class="h24"></div>
            <div class="pad">
              <div class="clay kart-ic kolon">
                <div class="t-label c-2">Neler soracağız</div>
                <div class="h12"></div>
                <div class="satir">
                  {ikon_kab("house")}
                  <div class="w16"></div>
                  <div class="esnek kolon">
                    <div class="t-strong">Sabit giderler</div>
                    <div class="h4"></div>
                    <div class="t-cap">Kira, fatura, ulaşım, kredi taksiti.</div>
                  </div>
                </div>
                <div class="h12"></div>
                <div class="satir">
                  {ikon_kab("footprints")}
                  <div class="w16"></div>
                  <div class="esnek kolon">
                    <div class="t-strong">Alışkanlıklar</div>
                    <div class="h4"></div>
                    <div class="t-cap">Sıklığı ve kendi ödediğin fiyatı.</div>
                  </div>
                </div>
                <div class="h12"></div>
                <div class="satir">
                  {ikon_kab("target")}
                  <div class="w16"></div>
                  <div class="esnek kolon">
                    <div class="t-strong">Birikim hedefi</div>
                    <div class="h4"></div>
                    <div class="t-cap">Gelirinin ne kadarını ayırmak istiyorsun.</div>
                  </div>
                </div>
              </div>
            </div>
            <div class="h24"></div>
            <div class="pad">
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Fiyatları biz tahmin etmiyoruz.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Ne kadar ödediğini sen yazıyorsun.</div>
                </div>
              </div>
            </div>
            <div class="h24"></div>'''

A_alt = '''          <div class="alt-sabit">
            <div class="pad kolon">
              <button class="btn-primary">Başla</button>
              <div class="h8"></div>
              <button class="btn-ghost" style="width:100%">Şimdi değil</button>
            </div>
          </div>'''


# ------------------------------------------------- B · 1/8 sabit giderler
def sabit(kira="12.500 ₺", fatura="", ulasim="", kredi="",
          basili_ad="", toplam=None):
    satirlar = [
        kuyu_deger("Kira ve aidat", kira, basili=(basili_ad == "kira")),
        kuyu_deger("Faturalar", fatura, basili=(basili_ad == "fatura")),
        kuyu_deger("Ulaşım ve yakıt", ulasim, basili=(basili_ad == "ulasim")),
        kuyu_deger("Kredi ve taksit", kredi, basili=(basili_ad == "kredi")),
    ]
    ic = '\n                <div class="h12"></div>\n'.join(satirlar)
    if toplam:
        ic += f'''
                <div class="h16"></div>
                <div class="aralik">
                  <div class="t-strong">Toplam</div>
                  <div class="t-amount">{toplam}</div>
                </div>'''
    return f'''{basi()}
{ilerleme(1, 8)}
            <div class="h24"></div>
{kart("Sabit giderler", "house", ic,
      "Her ay kesin çıkan tutarlar. Bilmediğini boş bırak.")}
            <div class="h24"></div>'''


B = sabit(kira="", basili_ad="fatura")
C = sabit(fatura="2.840 ₺", ulasim="1.900 ₺", kredi="1.560 ₺", toplam=tl(18800))


def sabit_klavye():
    """Faturalar satırına dokunuldu: kil tuş takımı açıldı, kuyu odakta."""
    ic = '\n                <div class="h12"></div>\n'.join([
        kuyu_deger("Kira ve aidat", "12.500 ₺"),
        f'''              <div class="kolon">
                <div class="kuyu-btn" style="padding:12px 16px;box-shadow:var(--clay-sunken), 0 0 0 2px var(--primary-text)">
                  <div class="esnek t-strong">Faturalar</div>
                  <div class="w12"></div>
                  <div class="t-amount">2.84</div>
                  <div class="imlec"></div>
                </div>
              </div>''',
        kuyu_deger("Ulaşım ve yakıt", ""),
        kuyu_deger("Kredi ve taksit", ""),
    ])
    return f'''{basi()}
{ilerleme(1, 8)}
            <div class="h24"></div>
{kart("Sabit giderler", "house", ic,
      "Elektrik, su, doğal gaz, internet, telefon.")}
            <div class="h24"></div>'''


D = sabit_klavye()


# ---------------------------------------------------------- E · 2/8 kahve
def aliskanlik(n, ad, ikon_ad, baslik, aciklama, secili, fiyat_etiket,
               fiyat="", ayna_html="", ek="", pasif=False, serbest=False,
               basili_cip=""):
    fiyat_html = ""
    if secili != "Hiç":
        serbest_html = f'''                <div class="h16"></div>
                <div class="t-label c-2">Günde kaç {ad}</div>
                <div class="h8"></div>
                <div class="clay-kuyu satir" style="padding:12px 16px;box-shadow:var(--clay-sunken), 0 0 0 2px var(--primary-text)">
                  <div class="t-display">3</div>
                  <div class="imlec"></div>
                </div>''' if serbest else ""
        fiyat_html = serbest_html + f'''                <div class="h16"></div>
{kuyu_deger(fiyat_etiket, fiyat, bos="Fiyatını yaz")}'''
    ayna_blok = f'''                <div class="h16"></div>
{ayna_html}''' if ayna_html else ""
    ic = f'''                <div class="t-label c-2">Ne sıklıkla</div>
                <div class="h8"></div>
                {sik_cipleri(SIKLIK, secili=secili, basili=basili_cip)}{fiyat_html}{ayna_blok}{ek}'''
    return f'''{basi()}
{ilerleme(n, 8)}
            <div class="h24"></div>
{kart(baslik, ikon_ad, ic, aciklama)}
            <div class="h24"></div>'''


E = aliskanlik(2, "fincan", "coffee", "Kahve",
               "Dışarıda aldığın kahve. Evde yaptığın sayılmaz.",
               "Günde 1", "Bir fincan kaç lira", "90 ₺",
               ayna(tl(2700), "Günde 1 × 90 ₺ × 30 gün"))

F = aliskanlik(2, "fincan", "coffee", "Kahve",
               "Ayrık seçenek yetmiyorsa sayıyı kendin yaz.",
               "Kendim yazayım", "Bir fincan kaç lira", "90 ₺",
               ayna(tl(8100), "Günde 3 × 90 ₺ × 30 gün"),
               serbest=True)

G = aliskanlik(3, "dal", "footprints", "Sigara",
               "Sıklığı ve kendi ödediğin fiyatı yazıyorsun.",
               "Hiç", "Bir paket kaç lira", "",
               ek=f'''
                <div class="h16"></div>
                <div class="serit serit-info">
                  <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                  <div class="w12"></div>
                  <div class="esnek t-cap" style="color:var(--text)">Hiç dedin. Bu kart planda görünmez.</div>
                </div>''')

# T-5/4: "öğün" sözcüğü kaldırıldı. K-051 referans kalori uygulamasının
# bilgi mimarisini ("öğün grupları") bilinçle kategoriye çevirdi; sözcük izi
# bizim yüzeyimizde kalmaz. Etiket: `tan.yemek.fiyat`.
H = aliskanlik(5, "yemek", "utensils", "Dışarıda yemek",
               "Öğle yemeği, akşam yemeği, paket sipariş.",
               "Haftada 1", "Bir yemek kaç lira", "380 ₺",
               ayna(tl(1629), "Haftada 1 × 380 ₺ × 30 gün ÷ 7"),
               basili_cip="Haftada 2-3")


# ------------------------------------------------------- I · 7/8 yatırım
def secenek_kart(metin, alt_metin="", secili=False, basili=False):
    cls = "secim-kart"
    if secili:
        cls += " secili"
    elif basili:
        cls += " basili"
    alt_html = (f'<div class="h4"></div><div class="t-cap">{alt_metin}</div>'
                if alt_metin else "")
    return f'''                <button class="{cls}" style="padding:12px 16px">
                  <div class="esnek kolon" style="align-items:flex-start">
                    <div class="t-strong">{metin}</div>
                    {alt_html}
                  </div>
                </button>'''


I = f'''{basi()}
{ilerleme(7, 8)}
            <div class="h24"></div>
{kart("Yatırım", "landmark", f'''                <div class="kolon">
{secenek_kart("Yapıyorum", secili=True)}
                <div class="h8"></div>
{secenek_kart("Yapmayı düşünüyorum")}
                <div class="h8"></div>
{secenek_kart("İlgilenmiyorum", basili=True)}
                </div>
                <div class="h16"></div>
                <div class="serit serit-info">
                  <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                  <div class="w12"></div>
                  <div class="esnek kolon">
                    <div class="t-cap" style="color:var(--text)">Yatırım tavsiyesi vermiyoruz.</div>
                    <div class="h4"></div>
                    <div class="t-cap">Birikimin bir kısmını yatırım payı diye etiketleriz.</div>
                  </div>
                </div>''',
      "Cevabın yalnız birikimini adlandırmak için.")}
            <div class="h24"></div>'''


# ------------------------------------------------ J · 8/8 birikim hedefi
def birikim(oran=0.15 / 0.41, yuzde_metin="%15", tutar=tl(4800), basili=False,
            sinirda=False, uyari=""):
    uyari_html = f'''                <div class="h12"></div>
                <div class="serit serit-warn">
                  <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("info")}</div>
                  <div class="w12"></div>
                  <div class="esnek kolon">
                    <div class="t-cap" style="color:var(--text)">{uyari}</div>
                    <div class="h4"></div>
                    <div class="t-cap">Sosyal ve keyfi payı 0 ₺ kalır.</div>
                  </div>
                </div>''' if uyari else ""
    ic = f'''{kaydirici(oran, "Gelirin yüzdesi",
                        f'<div class="t-display">{yuzde_metin}</div>',
                        alt=f"Ayda {tutar} ayırmayı hedefliyorsun.",
                        basili=basili, sinirda=sinirda,
                        a11y="Birikim hedefi yüzdesi",
                        genislik=326.0)}
                <div class="h12"></div>
                <div class="aralik">
                  <div class="t-micro">En az %0</div>
                  <div class="t-micro">En çok %41</div>
                </div>{uyari_html}'''
    return f'''{basi()}
{ilerleme(8, 8)}
            <div class="h24"></div>
{kart("Birikim hedefi", "target", ic,
      "Sabit giderlerinden sonra kalanın içinden ayrılır.")}
            <div class="h24"></div>
            <div class="pad">
              <div class="t-cap">Üst sınır sabit giderlerine göre hesaplandı. Zorunlu payın %59.</div>
            </div>
            <div class="h24"></div>'''


J = birikim()
K = birikim(oran=1.0, yuzde_metin="%41", tutar=tl(13120), sinirda=True,
            uyari="Üst sınıra geldin. Kaydırıcı burada durur.")


# ------------------------------------------- L · yarıda bıraktı, dönüyor
L = f'''{basi(kapat=False)}
            <div class="h24"></div>
            <div class="pad kolon">
              <div class="t-h1">Kaldığın yerden</div>
              <div class="h8"></div>
              <div class="t-body c-2">Dört kart cevapladın. Dördü bekliyor.</div>
            </div>
            <div class="h24"></div>
{ilerleme(4, 8)}
            <div class="h24"></div>
            <div class="pad">
              <div class="clay kart-ic kolon">
                <div class="t-label c-2">Bekleyen kartlar</div>
                <div class="h12"></div>
                {kuyu_deger("Dışarıda yemek", "", bos="Cevaplanmadı")}
                <div class="h12"></div>
                {kuyu_deger("Abonelikler", "", bos="Cevaplanmadı")}
                <div class="h12"></div>
                {kuyu_deger("Yatırım", "", bos="Cevaplanmadı")}
                <div class="h12"></div>
                {kuyu_deger("Birikim hedefi", "", bos="Cevaplanmadı")}
              </div>
            </div>
            <div class="h24"></div>
            <div class="pad">
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Planı şimdi de görebilirsin.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Eksik kartlar planda boş satır olarak durur.</div>
                </div>
              </div>
            </div>
            <div class="h24"></div>'''

L_alt = '''          <div class="alt-sabit">
            <div class="pad kolon">
              <button class="btn-primary">Devam et</button>
              <div class="h8"></div>
              <button class="btn-ghost" style="width:100%">Planı şimdi gör</button>
            </div>
          </div>'''


units = "".join([
    device("SENİ TANIYALIM", "E-25 · kapı (atlanabilir)", A, sabit_alt=A_alt, note=
           "<b>Kapı, duvar değil.</b> Kaç kart olduğunu (8) ve her birinin atlanabildiğini "
           "<b>başlamadan önce</b> söylüyor — kaç soru geldiğini bilmeden ankete giren kullanıcı "
           "üçüncü kartta terk eder. \"Şimdi değil\" birincil butonun altında tam genişlikte. "
           "Üç satırlık liste <b>daire ikon + başlık + tek cümle üçlü sütunu DEĞİL</b>: tek kartın "
           "içinde dikey satırlar, 44pt kategori kabı solda. Alttaki şerit K-050'yi kullanıcı "
           "diline çeviriyor: \"Fiyatları biz tahmin etmiyoruz.\""),
    device("SENİ TANIYALIM", "1/8 · sabit giderler · satır basılı", B, sabit_alt=alt(pasif=True), note=
           "<b>İlerleme 8 segment olarak çizilmedi:</b> tek oluk + dolgu + \"1/8\". Sekiz segment "
           "44px'lik parçalara bölünür ve ilerlemeyi okunmaz hâle getirirdi. <b>Dört alan da boş "
           "açılır</b> — hazır tutar, önceki kullanıcı ortalaması, \"tipik kira\" yok (K-050). "
           "Değer girilmemiş satır <code>Girilmedi</code> yazar; bu bir placeholder değil, geçerli bir "
           "durumdur. Devam <b>pasif</b>, çünkü henüz hiçbir şey girilmedi — ama <b>Bu kartı atla</b> "
           "etkin: boş bırakmak da bir cevaptır."),
    device("SENİ TANIYALIM", "1/8 · faturalar yazılıyor (klavye açık)", D, sabit_alt=alt(klavye=True), note=
           "<b>Kil tuş takımı</b> harcama ekle (E-11) ve limitler (E-17) ekranlarından geliyor: "
           "sistem klavyesi açılmaz, düzen zıplamaz, <b>Devam daima tuşların altında</b> kalır "
           "(rn-tasarim-kisitlari: klavye açıkken görünmesi gereken eleman). Odaklı kuyu 2pt "
           "<code>primary-text</code> halkası + imleç taşır. Kısmi giriş \"2.84\" olarak duruyor — "
           "binlik ayracı yazarken değil, alan odaktan çıkınca biçimlenir."),
    device("SENİ TANIYALIM", "1/8 · dolu + toplam", C, sabit_alt=alt(), note=
           "Dört satır dolduğunda kart <b>Toplam</b> satırını açar: 18.800 ₺. Bu sayı plan "
           "ekranındaki <b>Zorunlu</b> payının birebir kaynağıdır; kullanıcı aynı sayıyı iki ekranda "
           "görür, ikinci ekranda \"bu nereden çıktı\" diye sormaz. Toplam bir kart değil "
           "<b>kartın son satırı</b>: aynı nesnenin özeti, ayrı bir yüzey değil."),
    device("SENİ TANIYALIM", "2/8 · kahve · sıklık + kendi fiyatı", E, sabit_alt=alt(), note=
           "<b>K-053'ün kalbi.</b> Sıklık <b>ayrık çiplerle</b> seçilir (seçili çip çukur), fiyat "
           "kullanıcıdan gelir. Kartın içindeki <b>ayna kuyusu</b> hesabı anında gösterir: "
           "<b>Ayda 2.700 ₺</b> ve altında formül — \"Günde 1 × 90 ₺ × 30 gün\". Formülü yazmak "
           "zorunlu: sayının nereden geldiğini görmeyen kullanıcı ona güvenmez. Suçlayıcı tek "
           "sözcük yok; sayı kendi kendini anlatıyor."),
    device("SENİ TANIYALIM", "2/8 · serbest sayı (son seçenek)", F, sabit_alt=alt(klavye=True), note=
           "<b>Ayrık seçim önce, serbest sayı sonra.</b> \"Kendim yazayım\" çiplerin <b>sonunda</b> "
           "durur; ilk seçenek olsaydı her kullanıcı klavyeyle başlamak zorunda kalırdı (F-2). "
           "Seçilince kartın içinde ikinci bir kuyu açılır ve ayna satırı <b>aynı formülle</b> "
           "güncellenir: 8.100 ₺. Sıklık arttıkça sayı büyür, yorum eklenmez."),
    device("SENİ TANIYALIM", "3/8 · sigara · \"Hiç\" seçili", G, sabit_alt=alt(), note=
           "<b>Yargılamayan kart.</b> Sigara kartı kahve kartıyla <b>birebir aynı</b>: aynı başlık "
           "puntosu, aynı çipler, aynı kategori kabı (<code>footprints</code> — Alışkanlıklar "
           "ailesinin ikonu). Uyarı rengi yok, sağlık mesajı yok, \"bırakmayı düşündün mü\" yok. "
           "\"Hiç\" seçilince <b>fiyat alanı kapanır</b> (cevabı olmayan soru sorulmaz) ve şerit ne "
           "olacağını söyler: \"Bu kart planda görünmez.\" Sıfırlık satır plan ekranına yazılmaz."),
    device("SENİ TANIYALIM", "5/8 · dışarıda yemek · çip basılı", H, sabit_alt=alt(atla_basili=True), note=
           "<b>İki basılı durum aynı yüzeyde:</b> \"Haftada 2-3\" çipi basılı (henüz seçilmedi — "
           "çukurluk değil, çökme), \"Bu kartı atla\" da basılı. RN'de hover olmadığı için her "
           "dokunulabilir elemanın basılı hâli tasarlanır; aksi hâlde arayüz ölü hissedilir. "
           "Haftalık sıklık aylığa <b>30/7</b> ile çevrilir ve bu formül satırda yazılıdır."),
    device("SENİ TANIYALIM", "7/8 · yatırım niyeti", I, sabit_alt=alt(), note=
           "<b>SPK sınırı tasarıma kazındı (K-053).</b> Üç seçenek niyeti sorar, tek bir enstrüman "
           "adı, getiri tahmini ya da risk skoru geçmez. Şerit sınırı açıkça yazar: \"Yatırım "
           "tavsiyesi vermiyoruz. Birikimin bir kısmını yatırım payı diye etiketleriz.\" Seçenek "
           "kartları Katman 1'in niyet kartlarıyla aynı bileşen, ama <b>ikonsuz ve daha kısa</b> — "
           "burada karar hafif, orada kurucuydu."),
    device("SENİ TANIYALIM", "8/8 · birikim hedefi · kaydırıcı", J, sabit_alt=alt(birincil="Planı gör"), note=
           "<b>Yeni bileşen: kaydırıcı.</b> Oluk 12, topuz 32, satır 44 (dokunma hedefi). Dolgu "
           "topuzun merkezinde biter. Değer <b>%15</b> olarak <code>display</code> puntosunda, ₺ "
           "karşılığı hemen altında: yüzde soyut, lira somut — ikisi birlikte duruyor. Üst sınır "
           "<b>%41</b> uydurma değil, hesaplanmış: 100 − zorunlu payı (%59). Birincil buton burada "
           "\"Planı gör\" olur ve E-26'ya çıkar."),
    device("SENİ TANIYALIM", "8/8 · üst sınıra dayandı", K, sabit_alt=alt(birincil="Planı gör"), note=
           "<b>Kilit durumu.</b> Topuz sağ uçta <b>durur</b>, zemini <code>warning-soft</code>'a "
           "döner — <b>kırmızı kullanılmadı</b>: bu bir hata değil, bir sınır (danger yalnız dört "
           "bağlamda, tokens §1.3). Şerit sebebi ve sonucu birlikte söyler: \"Sosyal ve keyfi payı "
           "0 ₺ kalır.\" Kullanıcı engellenmiyor, bilgilendiriliyor; %41'i seçmek yasak değil."),
    device("SENİ TANIYALIM", "yarıda bıraktı · kaldığı yerden", L, sabit_alt=L_alt, note=
           "<b>Aşamalı profilleme (F-12) böyle çalışır.</b> Dönen kullanıcıya hangi kartların "
           "beklediği <b>tek tek</b> gösterilir ve her biri doğrudan dokunulabilir — \"devam et\" "
           "düğmesine mahkûm edilmiyor. Geri sayım <b>kaç kart kaldı</b> üzerinden yazılır, yüzde "
           "tamamlanma oranı üzerinden değil: \"%50 tamamlandı\" bir ilerleme rozetidir, iş değil. "
           "İkinci çıkış <b>Planı şimdi gör</b>: eksik veriyle plan kurulabilir (E-26 · F yüzeyi). "
           "Bu yüzeye ayarlardaki <b>Plan ve profil</b> bölümünden de girilir."),
])

OUT.write_text(page(
    "Trinkow · Seni tanıyalım (Katman 2) — prototip v4",
    "E-25 · Seni tanıyalım · Katman 2",
    "K-053 · 8 kart · her kart atlanabilir · kaldığı yerden devam · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
