# -*- coding: utf-8 -*-
"""E-26 · "Planın hazır" — anketin ÇIKTISI (K-053). Arketip F+ (sonuç ekranı).

Mood: HESAP DÖKÜMÜ. Bu ekran ne bir kutlama ne bir pano: kullanıcının
verdiği cevapların **karşılığını gösteren bir dökümdür**. Bu yüzden
ekranda rozet, konfeti, "tebrikler", puan ve derece yoktur (K-048/K-050) —
her kart tek bir soruyu cevaplar: *bu sayı nereden çıktı?*

DÖRT BAĞLAYICI KURAL BU EKRANI BELİRLEDİ:
  1. **Günlük limit buradan türetilir** (K-053): sosyal/keyfi payı ÷ maaş
     döngüsünde kalan gün. İşlem ekranda **görünür** — üç kutu ve iki işleç
     hâlinde yazılır, arka planda hesaplanıp tek sayı olarak sunulmaz.
     Anket böylece F-1'e bağlanır, havada kalmaz.
  2. **"Nasıl hesaplandı?" zorunlu.** Kara kutu çıktı güven kaybettirir.
  3. **Yatırım tavsiyesi YOK.** Enstrüman adı, getiri tahmini, risk skoru
     hiçbir yüzeyde geçmez. Tek izinli şey "yatırım payı" ETİKETİdir.
  4. **Sahte skor YOK.** "Finansal sağlık 72/100" türü uydurma metrik
     üretilmez (K-050).

PAY MODELİ — TEK SERBESTLİK DERECESİ (tasarım kararı, delta'da yazılı):
  Zorunlu pay bir **tercih değil, olgudur**: kullanıcının girdiği sabit
  giderlerin toplamıdır ve kaydırıcıyla oynatılamaz. Bu yüzden ekranda
  **tek kaydırıcı** vardır (birikim %) ve fark daima **sosyal/keyfi
  paydan** karşılanır. Toplam %100 kilidi böylece kurulur:
      birikim ↑  →  sosyal/keyfi ↓        (zorunlu sabit)
      üst sınır  =  100 − zorunlu%        (sosyal/keyfi 0'a inince durur)
  Üç kaydırıcı koyup "toplam 100 olsun" diye birbirini itmek, kullanıcıya
  her dokunuşta iki sayıyı birden kaybettirir; burada değişen tek sayı
  vardır ve nereden geldiği yazılıdır.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, icon, tus_takimi, kaydirici, pay_oluk,
                 pay_satiri, denklem, kuyu_deger, tl, yuzde, isk, icon)

OUT = pathlib.Path(__file__).parent.parent / "18-plan.html"

GUN = 28          # maaş döneminde kalan gün (17 Eylül → 14 Ekim)


# ------------------------------------------------------------------ kabuk
def basi(baslik="Planın hazır", alt_metin="Cevaplarından çıkardık. Değiştirebilirsin."):
    return f'''          <div class="ekran-basi">
            <button class="ikon-btn" aria-label="Geri dön">{icon("chevron-left")}</button>
            <div class="t-micro">Plan</div>
            <div style="width:44px;height:44px"></div>
          </div>
          <div class="pad kolon">
            <div class="t-h1">{baslik}</div>
            <div class="h8"></div>
            <div class="t-body c-2">{alt_metin}</div>
          </div>'''


def kart(ic, baslik="", sag=""):
    bas = f'''                <div class="aralik">
                  <div class="t-h2">{baslik}</div>
                  <div class="t-label c-2">{sag}</div>
                </div>
                <div class="h16"></div>''' if baslik else ""
    return f'''          <div class="pad">
            <div class="clay kart-ic kolon">
{bas}{ic}
            </div>
          </div>'''


# --------------------------------------------------------- pay dağılımı
def dagitim(zorunlu, sosyal, birikim, y_zor, y_sos, y_bir, gelir,
            yatirim="", birikim_bos=False, not_metin=""):
    paylar = [("pay-zorunlu", y_zor), ("pay-sosyal", y_sos)]
    if not birikim_bos:
        paylar.append(("pay-birikim", y_bir))
    birikim_satiri = (
        pay_satiri("nokta-birikim", "Birikim", birikim, yuzde(y_bir), yatirim)
        if not birikim_bos else f'''              <div class="satir-ust">
                <div class="kolon" style="padding-top:8px">
                  <div class="nokta nokta-birikim"></div>
                </div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-strong">Birikim</div>
                  <div class="h4"></div>
                  <div class="t-cap">Hedef girmedin.</div>
                </div>
                <div class="w12"></div>
                <div class="t-cap c-2">Girilmedi</div>
              </div>''')
    not_html = f'''
                <div class="h16"></div>
                <div class="t-cap">{not_metin}</div>''' if not_metin else ""
    ic = f'''                {pay_oluk(paylar, genislik=326.0)}
                <div class="h16"></div>
{pay_satiri("nokta-zorunlu", "Zorunlu", zorunlu, yuzde(y_zor), "Kira, fatura, ulaşım, kredi taksiti.")}
                <div class="h12"></div>
{pay_satiri("nokta-sosyal", "Sosyal ve keyfi", sosyal, yuzde(y_sos), "Günlük limitin buradan çıkar.")}
                <div class="h12"></div>
{birikim_satiri}{not_html}'''
    return kart(ic, "Aylık planın", f"Gelir {gelir}")


# ------------------------------------------------- günlük limit türetmesi
def gunluk_karti(sosyal, gun, limit, nasil_basili=False, alt_not=""):
    nb = " basili" if nasil_basili else ""
    ek = f'''
                <div class="h12"></div>
                <div class="t-cap">{alt_not}</div>''' if alt_not else ""
    ic = f'''{denklem((sosyal, "sosyal pay"), (f"{gun} gün", "kalan gün"),
                      (limit, "günlük"))}
                <div class="h16"></div>
                <div class="serit serit-info">
                  <div class="ikon-kutu" style="color:var(--primary-text)">{icon("gauge")}</div>
                  <div class="w12"></div>
                  <div class="esnek kolon">
                    <div class="t-cap" style="color:var(--text)">Panodaki büyük sayı bu olur.</div>
                    <div class="h4"></div>
                    <div class="t-cap">Her maaş döneminde yeniden bölünür.</div>
                  </div>
                </div>{ek}
                <div class="h12"></div>
                <div class="kolon" style="align-items:flex-start">
                  <button class="btn-ghost{nb}" style="padding:0 16px">{icon("info")}<div class="w8"></div>Nasıl hesaplandı</button>
                </div>'''
    return kart(ic, "Günlük limit", "Türetildi")


# ----------------------------------------------------- alışkanlık maliyeti
ALISKANLIK = [
    ("Kahve", "Günde 1 × 90 ₺", tl(2700)),
    ("Dışarıda yemek", "Haftada 1 × 380 ₺", tl(1629)),
    ("Alkol", "Haftada 1 × 220 ₺", tl(943)),
    ("Abonelikler", "Ayda 4 abonelik", tl(520)),
]


def aliskanlik_karti(kalemler=ALISKANLIK, toplam=tl(5792), bos=False):
    if bos:
        ic = f'''                <div class="t-body">Alışkanlık kartlarını cevaplamadın.</div>
                <div class="h8"></div>
                <div class="t-cap">Sıklığı ve kendi fiyatını yazarsan aylık tutarı burada görürsün.</div>
                <div class="h16"></div>
                <div class="kolon" style="align-items:flex-start">
                  <button class="btn-secondary" style="padding:0 24px">Kartlara dön</button>
                </div>'''
        return kart(ic, "Alışkanlık maliyeti", "4 kart boş")
    satirlar = []
    for ad, formul, tutar in kalemler:
        satirlar.append(f'''                <div class="satir">
                  <div class="esnek kolon">
                    <div class="t-strong">{ad}</div>
                    <div class="h4"></div>
                    <div class="t-cap">{formul}</div>
                  </div>
                  <div class="w12"></div>
                  <div class="t-amount">{tutar}</div>
                </div>''')
    ic = ('\n                <div class="h12"></div>\n'.join(satirlar) + f'''
                <div class="h16"></div>
                <div class="aralik">
                  <div class="t-strong">Toplam</div>
                  <div class="t-amount">{toplam}</div>
                </div>
                <div class="h12"></div>
                <div class="t-cap">Sosyal ve keyfi payının {toplam}'si. Yasak değil, görünür.</div>''')
    return kart(ic, "Alışkanlık maliyeti", "Kendi fiyatlarınla")


# ------------------------------------------------------- pay kaydırıcısı
def ayar_karti(oran, y_bir, tutar, basili=False, sinirda=False, degisim=""):
    d = f'''
                <div class="h12"></div>
                <div class="serit serit-info">
                  <div class="ikon-kutu" style="color:var(--primary-text)">{icon("sliders")}</div>
                  <div class="w12"></div>
                  <div class="esnek t-cap" style="color:var(--text)">{degisim}</div>
                </div>''' if degisim else ""
    ic = f'''{kaydirici(oran, "Birikim payı", f'<div class="t-display">{yuzde(y_bir)}</div>',
                        alt=f"Ayda {tutar}. Fark sosyal ve keyfi paydan iner.",
                        basili=basili, sinirda=sinirda, genislik=326.0,
                        a11y="Birikim payı yüzdesi")}
                <div class="h12"></div>
                <div class="aralik">
                  <div class="t-micro">En az %0</div>
                  <div class="t-micro">En çok %41</div>
                </div>
                <div class="h12"></div>
                <div class="t-cap">Zorunlu pay sabit kalır. O senin girdiğin sabit giderlerin toplamı.</div>{d}'''
    return kart(ic, "Payları ayarla", "Tek kaydırıcı")


PLAN_ALT = '''          <div class="alt-sabit">
            <div class="pad kolon">
              <button class="btn-primary">Planı kur</button>
              <div class="h8"></div>
              <button class="btn-ghost" style="width:100%">Şimdi değil</button>
            </div>
          </div>'''


# ------------------------------------------------------------- A · normal
A = f'''{basi()}
          <div class="h24"></div>
{dagitim(tl(18800), tl(8400), tl(4800), 59, 26, 15, tl(32000),
         yatirim="Bunun 1.920 ₺'si yatırım payı.")}
          <div class="h24"></div>
{gunluk_karti(tl(8400), GUN, tl(300))}
          <div class="h24"></div>
{aliskanlik_karti()}
          <div class="h24"></div>
{ayar_karti(0.15 / 0.41, 15, tl(4800))}
          <div class="h24"></div>'''


# ------------------------------------------- B · kaydırıcı ile değiştirildi
B = f'''{basi("Planın hazır", "Birikimi %25'e çektin. Plan yeniden bölündü.")}
          <div class="h24"></div>
{dagitim(tl(18800), tl(5200), tl(8000), 59, 16, 25, tl(32000),
         yatirim="Bunun 3.200 ₺'si yatırım payı.")}
          <div class="h24"></div>
{gunluk_karti(tl(5200), GUN, tl(185),
              alt_not="Birikimi artırdın, günlük limit 300 ₺'den 185 ₺'ye indi.")}
          <div class="h24"></div>
{ayar_karti(0.25 / 0.41, 25, tl(8000), basili=True,
            degisim="Sosyal ve keyfi pay 3.200 ₺ azaldı. Zorunlu pay değişmedi.")}
          <div class="h24"></div>
{aliskanlik_karti()}
          <div class="h24"></div>'''


# ------------------------------------------ C · "Nasıl hesaplandı?" sheet
def adim(n, baslik, govde):
    return f'''                <div class="satir-ust">
                  <div class="durak sirada"><div class="t-label">{n}</div></div>
                  <div class="w16"></div>
                  <div class="esnek kolon">
                    <div class="t-strong">{baslik}</div>
                    <div class="h4"></div>
                    <div class="t-cap">{govde}</div>
                  </div>
                </div>'''


NASIL = f'''          <div class="katman-ust">
            <div class="scrim-kat"></div>
            <div class="sheet">
              <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
              <div class="h12"></div>
              <div class="aralik">
                <div class="t-micro">Hesap</div>
                <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
              </div>
              <div class="h8"></div>
              <div class="t-h1">Nasıl hesaplandı</div>
              <div class="h24"></div>
              <div class="kolon">
{adim(1, "Sabit giderlerini topladık", "12.500 + 2.840 + 1.900 + 1.560 = 18.800 ₺. Zorunlu payın bu.")}
                <div class="h16"></div>
{adim(2, "Birikim hedefini ayırdık", "32.000 ₺ gelirin %15'i = 4.800 ₺.")}
                <div class="h16"></div>
{adim(3, "Kalanı sosyal ve keyfi paya yazdık", "32.000 − 18.800 − 4.800 = 8.400 ₺.")}
                <div class="h16"></div>
{adim(4, "Dönemde kalan güne böldük", "8.400 ₺ ÷ 28 gün = 300 ₺ günlük limit.")}
              </div>
              <div class="h24"></div>
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Hesap kuruş üzerinden yapılır.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Günlük limit tam liraya aşağı yuvarlanır. Yüzdeler tam sayıya yuvarlanır, toplamı 100'e tamamlanır.</div>
                </div>
              </div>
              <div class="h24"></div>
              <button class="btn-secondary" style="width:100%">Anladım</button>
            </div>
          </div>
'''

C = f'''{basi()}
          <div class="h24"></div>
{dagitim(tl(18800), tl(8400), tl(4800), 59, 26, 15, tl(32000),
         yatirim="Bunun 1.920 ₺'si yatırım payı.")}
          <div class="h24"></div>
{gunluk_karti(tl(8400), GUN, tl(300), nasil_basili=True)}
          <div class="h24"></div>'''


# ------------------------------------------------------------ D · gelir yok
D = f'''{basi("Limitini yazalım", "Gelirini paylaşmadın. Yüzde planı kurulmadı.")}
          <div class="h24"></div>
{kart(f'''                <div class="t-label c-2">Günlük limit</div>
                <div class="h8"></div>
                <div class="clay-kuyu" style="padding:16px;box-shadow:var(--clay-sunken), 0 0 0 2px var(--primary-text)">
                  <div class="satir" style="justify-content:center;align-items:baseline">
                    <div class="t-hero">300</div>
                    <div class="imlec"></div>
                    <div class="w8"></div>
                    <div class="t-hero-simge c-2">₺</div>
                  </div>
                </div>
                <div class="h8"></div>
                <div class="t-cap">Ayda yaklaşık 9.000 ₺. Tahmini.</div>''')}
          <div class="h24"></div>
{kart(f'''                <div class="t-body">Alışkanlık maliyeti gelirsiz de çalışır.</div>
                <div class="h8"></div>
                <div class="t-cap">Sıklığı ve fiyatı sen yazdığın için bu kart eksiksiz.</div>
                <div class="h16"></div>
                <div class="aralik">
                  <div class="t-strong">Aylık alışkanlık toplamı</div>
                  <div class="t-amount">{tl(5792)}</div>
                </div>
                <div class="h12"></div>
                <div class="t-cap">Günlük limitini yazarken bu sayıyı hesaba katabilirsin.</div>''',
      "Elimizde ne var", "Gelir olmadan")}
          <div class="h24"></div>
          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-cap" style="color:var(--text)">Gelirini sonra da ekleyebilirsin.</div>
                <div class="h4"></div>
                <div class="t-cap">Ayarlar, Plan ve profil bölümü. Yüzde planı o an kurulur.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

D_alt = f'''          <div class="alt-sabit">
{tus_takimi()}
            <div class="h12"></div>
            <div class="pad"><button class="btn-primary">Limiti kaydet</button></div>
          </div>'''


# --------------------------- E · sabit giderler gelirden büyük (negatif kalan)
E = f'''{basi("Plan bu ay kurulamadı", "Sabit giderlerin gelirinden fazla.")}
          <div class="h24"></div>
          <div class="pad">
            <div class="serit serit-warn">
              <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-cap" style="color:var(--text)">Sabit giderlerin gelirini 1.400 ₺ aşıyor.</div>
                <div class="h4"></div>
                <div class="t-cap">Bu çok rastlanan bir durum. Ölçülebilir olması iyi haber.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>
{kart(f'''                <div class="aralik">
                  <div class="t-body">Aylık net gelir</div>
                  <div class="t-amount">{tl(18000)}</div>
                </div>
                <div class="h12"></div>
                <div class="aralik">
                  <div class="t-body">Sabit giderler</div>
                  <div class="t-amount">{tl(19400)}</div>
                </div>
                <div class="h16"></div>
                <div class="aralik">
                  <div class="t-strong">Kalan</div>
                  <div class="t-amount c-warn">1.400 ₺ eksik</div>
                </div>
                <div class="h12"></div>
                <div class="t-cap">Yüzde planı kalan tutar üzerine kurulur. Kalan olmadığı için pay dağılımı yazılmadı.</div>''',
      "Hesap", "Bu ay")}
          <div class="h24"></div>
{kart(f'''                <div class="t-body">Buradan üç yol var.</div>
                <div class="h16"></div>
                <button class="btn-primary">Giderleri gözden geçir</button>
                <div class="h8"></div>
                <div class="t-cap">Kredi taksiti bitiyor mu, fatura tahmini yüksek mi.</div>
                <div class="h16"></div>
                <button class="btn-secondary">Limiti elle yaz</button>
                <div class="h8"></div>
                <div class="t-cap">Plan olmadan da günlük limit koyabilirsin.</div>
                <div class="h16"></div>
                <button class="btn-ghost" style="width:100%">Limitsiz devam et</button>
                <div class="h8"></div>
                <div class="t-cap">Takip etmek için plana ihtiyacın yok. Kayıt tutmak tek başına işe yarar.</div>''',
      "Çıkış yolu", "Seçim senin")}
          <div class="h24"></div>'''


# ------------------------------------------------- F · katman 2 yarım kaldı
F = f'''{basi("Plan yarım hazır", "Dört kart boş. Eldekiyle böldük.")}
          <div class="h24"></div>
{dagitim(tl(18800), tl(13200), "", 59, 41, 0, tl(32000), birikim_bos=True,
         not_metin="Birikim hedefi girmedin. Şimdilik kalanın tamamı sosyal ve keyfi payında.")}
          <div class="h24"></div>
{gunluk_karti(tl(13200), GUN, tl(471),
              alt_not="Birikim hedefi girersen bu sayı düşer.")}
          <div class="h24"></div>
{aliskanlik_karti(bos=True)}
          <div class="h24"></div>
          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-cap" style="color:var(--text)">Planı şimdi kurabilirsin.</div>
                <div class="h4"></div>
                <div class="t-cap">Kalan kartları doldurunca plan kendini günceller.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

F_alt = '''          <div class="alt-sabit">
            <div class="pad kolon">
              <button class="btn-primary">Planı kur</button>
              <div class="h8"></div>
              <button class="btn-ghost" style="width:100%">Kalan kartlara dön</button>
            </div>
          </div>'''


# ---------------------------------------------------------- G · yükleniyor
G = f'''          <div class="ekran-basi">
            <div style="width:44px;height:44px"></div>
            <div class="t-micro">Plan</div>
            <div style="width:44px;height:44px"></div>
          </div>
          <div class="pad kolon">
            {isk("240px", "32px", "16px")}
            <div class="h8"></div>
            {isk("300px", "18px")}
          </div>
          <div class="h24"></div>
{kart(f'''                {isk("326px", "12px")}
                <div class="h16"></div>
                <div class="satir">
                  {isk("8px", "8px")}
                  <div class="w12"></div>
                  <div class="esnek kolon">{isk("140px", "18px")}</div>
                  <div class="w12"></div>
                  {isk("80px", "18px")}
                </div>
                <div class="h12"></div>
                <div class="satir">
                  {isk("8px", "8px")}
                  <div class="w12"></div>
                  <div class="esnek kolon">{isk("180px", "18px")}</div>
                  <div class="w12"></div>
                  {isk("80px", "18px")}
                </div>
                <div class="h12"></div>
                <div class="satir">
                  {isk("8px", "8px")}
                  <div class="w12"></div>
                  <div class="esnek kolon">{isk("110px", "18px")}</div>
                  <div class="w12"></div>
                  {isk("80px", "18px")}
                </div>''')}
          <div class="h24"></div>
{kart(f'''                <div class="satir">
                  {isk("96px", "68px", "16px")}
                  <div class="w12"></div>
                  {isk("96px", "68px", "16px")}
                  <div class="w12"></div>
                  {isk("96px", "68px", "16px")}
                </div>''')}
          <div class="h24"></div>'''


units = "".join([
    device("PLANIN HAZIR", "E-26 · normal (gelir + 8 kart dolu)", A, sabit_alt=PLAN_ALT, note=
           "<b>Ekranın tezi:</b> her sayı bir cevabın karşılığı. Üstteki <b>pay çubuğu</b> tek oluk "
           "içinde üç segment; segmentler arasına <b>4pt boşluk</b> girer, oluk aradan görünür — iki "
           "mavi ton yan yana yapışmaz (WCAG 1.4.11 komşu grafik nesne). Renk tek başına bilgi "
           "taşımaz: her payın satırında <b>nokta + ad + ₺ + %</b> birlikte durur. "
           "<b>Günlük limit kartı K-053'ün bağını kuruyor:</b> 8.400 ₺ ÷ 28 gün = 300 ₺, işlem "
           "ekranda yazılı. <b>Alışkanlık maliyeti</b> kullanıcının kendi fiyatlarıyla hesaplandı "
           "(K-050) ve suçlamıyor: \"Yasak değil, görünür.\" Rozet, skor, \"finansal sağlık puanı\" yok."),
    device("PLANIN HAZIR", "E-26 · kaydırıcı çekildi · %100 kilidi", B, sabit_alt=PLAN_ALT, note=
           "<b>Bir yüzde artarsa ne olur?</b> Cevap tasarıma yazıldı: <b>zorunlu pay sabit kalır</b> "
           "(o bir tercih değil, kullanıcının girdiği sabit giderlerin toplamı), fark <b>sosyal ve "
           "keyfi paydan</b> iner. Tek kaydırıcı, tek serbestlik derecesi — üç kaydırıcıyı birbirine "
           "itmek her dokunuşta iki sayıyı birden kaybettirirdi. Sonuç <b>zincirin ucuna kadar</b> "
           "gösteriliyor: günlük limit 300 ₺'den 185 ₺'ye indi. Topuz <b>basılı</b> durumda çizildi."),
    device("PLANIN HAZIR", "E-26 · \"Nasıl hesaplandı\" (sheet)", C, sabit_alt=NASIL, note=
           "<b>K-053: kara kutu çıktı güven kaybettirir.</b> Dört adım, <b>gerçek sayılarla</b> — "
           "genel bir \"bütçe yöntemi\" anlatımı değil, bu kullanıcının kendi hesabı. Alt şerit iki "
           "yuvarlama kuralını yazıyor: hesap <b>kuruş üzerinden</b> yapılır, günlük limit tam liraya "
           "<b>aşağı</b> yuvarlanır (yukarı yuvarlamak limiti aşındırır), yüzdeler tam sayıya "
           "yuvarlanır ve <b>en büyük kalan</b> yönteminde 100'e tamamlanır. Arkada plan görünür "
           "kalır: sheet ekranı ele geçirmez."),
    device("PLANIN HAZIR", "E-26 · gelir girilmedi (zarif küçülme)", D, sabit_alt=D_alt, note=
           "<b>Model küçülür, çökmez.</b> Gelir yoksa yüzde planı <b>hiç çizilmez</b> — boş bir pay "
           "çubuğu ya da \"—\" ile dolu bir kart bırakmak, kullanıcıya eksikliğini her açılışta "
           "hatırlatır. Yerine ekranın adı bile değişir: \"Limitini yazalım\". <b>Eldekini dürüstçe "
           "söylüyor:</b> alışkanlık maliyeti gelirsiz de tam çalışır, çünkü onun girdisi "
           "kullanıcının kendi sıklığı ve kendi fiyatı. Kil tuş takımı, Kaydet tuşların altında."),
    device("PLANIN HAZIR", "E-26 · sabit giderler gelirden büyük", E, sabit_alt=None or '', note=
           "<b>Gerçek ve sık durum; suçlamıyoruz.</b> Kırmızı YOK (danger yalnız dört bağlamda) — "
           "uyarı <code>warning</code> ailesinde. Negatif sayı yazılmaz: \"-1.400 ₺\" değil "
           "<b>\"1.400 ₺ eksik\"</b> (metinler §0). Şerit durumu normalize ediyor: \"Bu çok rastlanan "
           "bir durum. Ölçülebilir olması iyi haber.\" Ve <b>üç çıkış yolu</b> veriyor: giderleri "
           "gözden geçir · limiti elle yaz · limitsiz devam et. Son satır ürünün tezi: "
           "\"Takip etmek için plana ihtiyacın yok.\" Alt sabit blok yok — kararlar kartın içinde."),
    device("PLANIN HAZIR", "E-26 · Katman 2 yarım bırakıldı", F, sabit_alt=F_alt, note=
           "<b>Eksik veriyle plan.</b> Birikim payı <b>%0 olarak çizilmedi</b> — girilmemiş bir hedefi "
           "sıfır göstermek yanlış bilgi olur; satır \"Girilmedi\" der ve çubukta segmenti yoktur. "
           "Günlük limit yine türetilir (13.200 ₺ ÷ 28 = 471 ₺) ve ne olacağı yazılır: \"Birikim "
           "hedefi girersen bu sayı düşer.\" Alışkanlık kartı <b>boş durumu</b> ile duruyor; "
           "\"Henüz veri yok\" demiyor, ne yazarsan ne göreceğini söylüyor."),
    device("PLANIN HAZIR", "E-26 · yükleniyor", G, note=
           "<b>İskelet, spinner değil:</b> ekranın düzeni zaten biliniyor, o düzen çukur bloklarla "
           "çizilir (tokens §7.10) ve içerik gelince <b>hiçbir şey zıplamaz</b>. Blok yükseklikleri "
           "gerçek satır yüksekliklerine eşit: 32 başlık, 18 satır, 12 çubuk, 68 denklem kutusu. "
           "Animasyon yok — kil yüzeyde parlayan bir shimmer, malzemenin mat karakterine aykırı."),
])

OUT.write_text(page(
    "Trinkow · Planın hazır — prototip v4",
    "E-26 · Planın hazır",
    "K-053 · anketin çıktısı · günlük limit buradan türetilir · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
