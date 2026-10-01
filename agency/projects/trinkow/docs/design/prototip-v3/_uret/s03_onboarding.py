# -*- coding: utf-8 -*-
"""E-01…E-03 · Onboarding (3 adım) — arketip C (Onboarding 1 of N).
Sekme çubuğu yok. Mood: ferah, tek soru, büyük Poppins başlık, bol boşluk.
En fazla 3 soru sorulur; her adım tek karar taşır.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, tus_takimi, CATS, kat_kab

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

# ------------------------------------------------------------- E-02 · limit
B = f'''{basi(2)}
            <div class="h24"></div>
{soru("Günde ne kadar harcamak istiyorsun", "Kesin olması gerekmiyor. Sonra düzeltiriz.")}
            <div class="h24"></div>
            <div class="pad">
              <div class="t-label c-2">Günlük limit</div>
              <div class="h8"></div>
              <div class="clay-kuyu" style="padding:16px">
                <div class="satir" style="justify-content:center;align-items:baseline">
                  <div class="t-hero">300</div>
                  <div class="imlec"></div>
                  <div class="w8"></div>
                  <div class="t-hero-simge c-2">₺</div>
                </div>
              </div>
              <div class="h8"></div>
              <div class="t-cap">Ayda yaklaşık 9.000 ₺. Tahmini.</div>
            </div>
            <div class="h12"></div>
            <div class="pad kolon">
              <div class="t-label c-2">Sık kullanılan</div>
              <div class="h8"></div>
              <div class="satir">
                <button class="cip">200 ₺</button><div class="w8"></div>
                <button class="cip">350 ₺</button><div class="w8"></div>
                <button class="cip basili">500 ₺</button>
              </div>
            </div>
            <div class="h24"></div>'''

B_alt = f'''          <div class="alt-sabit">
{tus_takimi()}
            <div class="h12"></div>
            <div class="pad"><button class="btn-primary">Devam</button></div>
          </div>'''

# ------------------------------------------------ E-03 · takip kipi soru 3
def kategori_agi(secililer):
    o = []
    for ad in CATS:
        s = " secili" if ad in secililer else ""
        nokta = (f'<div class="nokta" style="background-color:var(--cat-{CATS[ad][1][4:]})"></div><div class="w8"></div>'
                 if ad in secililer else '')
        o.append(f'<div class="cip-ag-oge"><button class="cip{s}">{nokta}{ad}</button></div>')
    return f'<div class="cip-ag">{"".join(o)}</div>'


C = f'''{basi(3)}
            <div class="h24"></div>
{soru("En çok neyi merak ediyorsun", "En fazla üç kategori seç.")}
            <div class="h24"></div>
            <div class="pad">
{kategori_agi(["Kafe", "Market", "Ulaşım"])}
            </div>
            <div class="h8"></div>
            <div class="pad">
              <div class="t-cap">Seçtiklerin panoda kategori limiti olarak görünür.</div>
            </div>
            <div class="h24"></div>
            <div class="pad">
              <div class="clay kart-ic kolon">
                <div class="t-label c-2">Kurulum özeti</div>
                <div class="h8"></div>
                <div class="aralik">
                  <div class="t-body">Kip</div>
                  <div class="t-strong">Takip</div>
                </div>
                <div class="h8"></div>
                <div class="aralik">
                  <div class="t-body">Günlük limit</div>
                  <div class="t-amount">300 ₺</div>
                </div>
                <div class="h8"></div>
                <div class="aralik">
                  <div class="t-body">İzlenen kategori</div>
                  <div class="t-amount">3</div>
                </div>
              </div>
            </div>
            <div class="h24"></div>'''

C_alt = '''          <div class="alt-sabit">
            <div class="pad"><button class="btn-primary">Başla</button></div>
          </div>'''

units = "".join([
    device("ONBOARDING", "adım 1/3 · niyet", A,
           "<b>Mood:</b> ferah, tek karar. Seçenekler <b>dikey kart</b> — \"daire ikon + başlık + tek cümle\" "
           "üçlü sütun kurulmadı. Seçili kart <b>çukur</b>, seçilmemiş kartlar <b>kabarık</b>; üçüncüsü "
           "<b>basılı (pressed)</b> gösteriliyor. Alttaki şerit seçimin panoda ne yapacağını gösterir.",
           sabit_alt=A_alt),
    device("ONBOARDING", "adım 2/3 · günlük limit", B,
           "Aynı <b>kil tuş takımı</b> harcama ekle ekranından geliyor — kullanıcı aynı hareketi ikinci kez "
           "öğrenmiyor. Sık kullanılan tutar çipleri kısayol; üçüncüsü <b>basılı</b>. "
           "\"Ayda yaklaşık 9.000 ₺. Tahmini.\" tahmini olduğunu açıkça söyler.",
           sabit_alt=B_alt),
    device("ONBOARDING", "adım 3/3 · kipe bağlı soru", C,
           "Soru <b>kipe bağlı</b>: Takip kipinde kategori seçimi gelir. 13 çip <b>sarmalı satır</b> olarak "
           "dizilir (grid değil — RN'de <code>flexWrap</code>). Seçili üç çip çukur + kategori noktalı. "
           "Altta kurulum özeti: kullanıcı Başla'ya basmadan ne kurduğunu görüyor.",
           sabit_alt=C_alt),
])

OUT.write_text(page(
    "Trinkow · Onboarding (3 adım) — prototip v3",
    "E-01 … E-03 · Onboarding",
    "Arketip C — Onboarding (1 of N) · sekme çubuğu yok · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
