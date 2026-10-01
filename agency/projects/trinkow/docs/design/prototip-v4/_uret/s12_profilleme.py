# -*- coding: utf-8 -*-
"""E-20 · Profilleme sorusu (sheet) — arketip G (Tek soru).

Mood: KISA NEFES. Onboarding'in E-01…E-03 ekranlarıyla aynı aile: tek soru,
çok boşluk, tek karar. Farkı, buraya kullanıcı gelmedi — soru **onun gününe
düştü**. Bu yüzden üç şey zorunludur:

  1. Soru **tek**tir ve gün başına yalnız bir kez çıkar.
  2. **Atlanabilir**: "Şimdi değil" birincil butonla aynı ağırlıkta durur,
     kapatma (X) da açıktır. Zorlama yok, 14 gün geri gelmez.
  3. Cevaptan sonra **ne değiştiği gösterilir** — soru bir şey karşılığında
     sorulmuştu, karşılığı görünmezse bir dahakine cevap verilmez.

Sheet arkasında pano görünür kalır: kullanıcı ürünün neresinde olduğunu
kaybetmez, soru ekranı ele geçirmez.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, hero_gauge, satir, sekme_cubugu, icon,
                 para_hero)

OUT = pathlib.Path(__file__).parent.parent / "12-profilleme.html"


# -------------------------------------------------------- arka plan: pano
def pano(taksit_karti=False, serit=False):
    ek = ""
    if taksit_karti:
        serit_html = f'''              <div class="h12"></div>
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek t-cap">Cevabına göre eklendi. Ayarlardan kaldırabilirsin.</div>
              </div>''' if serit else ""
        ek = f'''          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic">
              <div class="aralik">
                <div class="t-h2">Taksit yükü</div>
                <div class="t-label c-2">Önümüzdeki ay</div>
              </div>
              <div class="h12"></div>
              <div class="satir" style="align-items:baseline">
                <div class="t-display">1.560</div>
                <div class="w8"></div>
                <div class="t-amount c-2">₺</div>
              </div>
              <div class="h4"></div>
              <div class="t-cap">İki seri sürüyor. Sonuncusu Mayıs 2027 tarihinde bitiyor.</div>
              <div class="h12"></div>
              <button class="btn-secondary" style="align-self:flex-start;padding:0 24px">Taksitleri gör</button>
{serit_html}
            </div>
          </div>'''
    return f'''          <div class="ekran-basi">
            <div class="kolon">
              <div class="t-cap">11 Eylül Cuma</div>
              <div class="t-h1">Bugün</div>
            </div>
            <button class="ikon-btn" aria-label="Limitleri aç">{icon("sliders")}</button>
          </div>
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                <div class="t-label c-2">Günlük limit 300 ₺</div>
              </div>
              <div class="h12"></div>
              <div class="hero-daire">
                {hero_gauge(0.41)}
                <div class="hero-orta">
                  {para_hero("176")}
                  <div class="t-label c-2">bugün kalan</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-body" style="text-align:center">Bugün 124 ₺. Limitinin 176 ₺ altındasın.</div>
            </div>
          </div>
{ek}
          <div class="h24"></div>
          <div class="pad aralik">
            <div class="t-h2">Bugünkü kayıtlar</div>
            <div class="t-label c-2">Günlük toplam 124 ₺</div>
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Ulaşım", "09.05 · Kart", "29 ₺")}
          </div>
          <div class="h24"></div>'''


# ------------------------------------------------------------ soru sheet'i
def secenek(metin, secili=False, basili=False):
    cls = "secim-kart"
    if secili:
        cls += " secili"
    if basili:
        cls += " basili"
    return f'''                <button class="{cls}">
                  <div class="esnek t-body" style="text-align:left">{metin}</div>
                </button>'''


def soru(baslik, secenekler, adim="2. gün",
         alt_baslik="Cevabın panonu sana göre ayarlar.", ek=""):
    ic = '\n                <div class="h8"></div>\n'.join(secenekler)
    return f'''          <div class="katman-ust">
            <div class="scrim-kat"></div>
            <div class="sheet">
              <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
              <div class="h12"></div>
              <div class="aralik">
                <div class="t-micro">{adim}</div>
                <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
              </div>
              <div class="h8"></div>
              <div class="t-h1">{baslik}</div>
              <div class="h8"></div>
              <div class="t-cap">{alt_baslik}</div>
              <div class="h24"></div>
              <div class="kolon">
{ic}
              </div>{ek}
              <div class="h12"></div>
              <button class="btn-ghost" style="width:100%">Şimdi değil</button>
            </div>
          </div>
'''


# --- B-3 (K-061/3) · EMEKLİYE AYRILDI --------------------------------
# Burada bir zamanlar "Aylık gelirin hangi aralıkta?" sorusu duruyordu
# (dört aralık + "Söylemek istemiyorum"). Kaldırıldı ve geri konmayacak:
# geliri Katman 1 (E-02) **tam tutar** olarak alıyor ve E-26'nın plan
# formülleri (`gelir_kurus`) tam tutarla çalışıyor. Aynı olguyu bir yerde
# aralık, bir yerde tutar olarak sormak iki ayrı doğru üretir — hangisi
# kazanacağı kodda belirlenir, tasarımda değil. Eksik geliri tamamlama
# yolu zaten tek ve yazılı: Ayarlar > Plan ve profil (K-053/F-12).
#
# Yerine E-25'in **cevaplanmamış kartlarından biri** geliyor. Seçim
# "Yatırım": tek soruluk, tutarsız, ayrık seçenekli — sheet biçimine
# birebir oturan tek kart. Başlık, üç seçenek ve bilgi şeridi
# `s17_tanisma.py`'deki 7/8 kartından **kelimesi kelimesine** alındı;
# B-3'ün dersi tam olarak budur: aynı soru iki yüzeyde aynı sözcüklerle
# sorulur, yoksa iki farklı veri olur.
A = soru("Yatırım yapıyor musun?", [
    secenek("Yapıyorum"),
    secenek("Yapmayı düşünüyorum"),
    secenek("İlgilenmiyorum"),
], adim="2. gün",
    alt_baslik="Cevabın yalnız birikimini adlandırmak için.",
    ek=f'''
              <div class="h16"></div>
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-cap" style="color:var(--text)">Yatırım tavsiyesi vermiyoruz.</div>
                  <div class="h4"></div>
                  <div class="t-cap">Birikimin bir kısmını yatırım payı diye etiketleriz.</div>
                </div>
              </div>''')

B = soru("Taksitli alışveriş yapar mısın?", [
    secenek("Sık sık", basili=True),
    secenek("Bazen"),
    secenek("Neredeyse hiç"),
], adim="3. gün")


units = "".join([
    device("PROFİLLEME", "E-20 · 2. gün · bekleyen kart (yatırım)", pano(), sabit_alt=A, note=
           "<b>Tek soru, üç seçenek, tek ekran.</b> Arkada pano görünür kalır — soru ürünü ele "
           "geçirmez. Bu yüzey artık gelir sormuyor (<b>T-5 · B-3</b>): geliri E-02 tam tutar olarak "
           "alıyor, aynı şeyi ikinci kez aralık olarak sormak iki ayrı doğru üretirdi. Yerine "
           "E-25'in <b>cevaplanmamış kartlarından biri</b> geliyor; başlık, seçenekler ve bilgi "
           "şeridi 7/8 kartından <b>kelimesi kelimesine</b> aynı. <b>\"İlgilenmiyorum\" "
           "diğerleriyle aynı ağırlıktadır</b>: küçültülmemiş, griye çekilmemiş, en alta "
           "sürülmemiş. \"Şimdi değil\" ve kapatma (X) birlikte durur; iki ayrı çıkış kapısı "
           "bilinçlidir. Alt başlık ürünün ne kazanacağını değil <b>cevabın nereye gittiğini</b> "
           "söyler: \"Cevabın yalnız birikimini adlandırmak için.\" Şerit K-053'ün sınırını yüzeyde "
           "tutuyor: tavsiye yok, enstrüman yok, getiri yok — yalnız bir etiket."),
    device("PROFİLLEME", "E-20 · 3. gün · taksit · seçim basılı", pano(), sabit_alt=B, note=
           "<b>Basılı durum tek geri bildirimdir</b> (hover yok): seçenek çöker, zemini oluk olur. "
           "Onay ikonu eklenmez — çukurluk zaten \"seçildi\" der. Seçildiği an sheet kapanır, ayrı bir "
           "\"Kaydet\" yoktur: tek soruluk bir formda ikinci dokunuş istemek kabalıktır. Üç seçenek, "
           "\"Şimdi değil\" yine yerinde."),
    device("PROFİLLEME", "E-20 · cevaptan sonra panoda ne değişti", pano(taksit_karti=True, serit=True),
           sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Sorunun karşılığı gösterilir.</b> \"Sık sık\" cevabı panoya <b>Taksit yükü</b> kartını "
           "ekledi; mavi şerit bunu açıkça söyler ve geri alma yolunu verir: \"Cevabına göre eklendi. "
           "Ayarlardan kaldırabilirsin.\" Karşılığı görünmeyen soru, ikinci kez cevaplanmaz. Kutlama, "
           "rozet, \"teşekkürler\" ekranı yok — değişen şey ekranın kendisidir."),
])

OUT.write_text(page(
    "Trinkow · Profilleme sorusu — prototip v4",
    "E-20 · Profilleme sorusu",
    "Arketip G — Tek soru · sheet · atlanabilir · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
