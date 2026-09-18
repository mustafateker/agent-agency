# -*- coding: utf-8 -*-
"""E-10 · Bugün (pano) — arketip F (Focus / hero card).
Mood: sakin, tek büyük nesne. Ekranın ağırlık merkezi mavi kil panel.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, hero_gauge, satir, sekme_cubugu, icon, kat_kab, para_hero)

OUT = pathlib.Path(__file__).parent.parent / "01-bugun.html"


def basi(sag_basili=False):
    b = " basili" if sag_basili else ""
    return f'''          <div class="ekran-basi">
            <div class="kolon">
              <div class="t-cap">10 Eylül Perşembe</div>
              <div class="t-h1">Bugün</div>
            </div>
            <button class="ikon-btn{b}" aria-label="Limitleri aç">{icon("sliders")}</button>
          </div>'''


def hero(sayi, etiket, alt_metin, oran, over=0.0, sayi_cls="", bos=False, limit_satiri="Günlük limit 300 ₺"):
    return f'''          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                <div class="t-label c-2">{limit_satiri}</div>
              </div>
              <div class="h12"></div>
              <div class="hero-daire{' hero-bos' if bos else ''}">
                {hero_gauge(oran, over, bos)}
                <div class="hero-orta">
                  {para_hero(sayi, sayi_cls)}
                  <div class="t-label c-2">{etiket}</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-body" style="text-align:center">{alt_metin}</div>
            </div>
          </div>'''


def kat_satiri(ad, harcanan, limit, yuzde, renk_var, tasma=False):
    # Taşma varsa oluk 100'u değil toplamı temsil eder; iki dolgu birlikte %100 yapar.
    tam = max(100, yuzde)
    ic = round(min(yuzde, 100) * 100 / tam, 1)
    dis = round(max(0, yuzde - 100) * 100 / tam, 1)
    dolgu = (f'<div class="cubuk-dolgu" style="width:{ic}%;background-color:{renk_var}"></div>'
             + (f'<div class="cubuk-dolgu" style="width:{dis}%;background-color:var(--warning)"></div>' if dis else ''))
    sag = f'<div class="t-label c-warn">{limit} limit dışı</div>' if tasma else f'<div class="t-label c-2">{limit}</div>'
    return f'''              <div class="satir">
                {kat_kab(ad)}
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="aralik">
                    <div class="t-strong">{ad}</div>
                    <div class="t-amount">{harcanan}</div>
                  </div>
                  <div class="h8"></div>
                  <div class="cubuk-oluk">{dolgu}</div>
                  <div class="h4"></div>
                  <div class="aralik">
                    <div class="t-cap">aylık</div>
                    {sag}
                  </div>
                </div>
              </div>'''


def kat_karti(tasma=False):
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="aralik">
                <div class="t-h2">Kategori limitleri</div>
                <button class="btn-ghost" style="padding:0 16px" aria-label="Tüm kategoriler">Tümünü gör</button>
              </div>
              <div class="h8"></div>
{kat_satiri("Market", "2.180 ₺", "3.000 ₺", 73, "var(--cat-yesil)")}
              <div class="h12"></div>
{kat_satiri("Kafe", "940 ₺", "800 ₺" if tasma else "1.200 ₺", 118 if tasma else 78, "var(--cat-amber)", tasma)}
            </div>
          </div>'''


def liste_basligi(toplam):
    return f'''          <div class="pad aralik">
            <div class="t-h2">Bugünkü kayıtlar</div>
            <div class="t-label c-2">{toplam}</div>
          </div>'''



def hero_yaysiz(sayi, etiket, alt_metin, sag_etiket="Limit yok"):
    """`HeroPlain` — YAYSIZ kahraman (E-10 · limitsiz varyantı).

    Neden yay yok: yay bir **oranı** anlatır. Limit yoksa dolacak bir şey de
    yoktur; boş bir oluk çizmek "bir şey eksik" yalanını söyler. `EmptyGauge`
    (tokens §7.8) da uygun değildir — o, *veri* beklenen yerde kullanılır;
    burada veri var, **eşik** yok.

    Kahraman sayının anlamı değişir: "bugün kalan" değil **"bugün harcanan"**.
    Ekran bir ölçüm aleti değil, bir bilgi ekranıdır: kullanıcı limit koymamayı
    seçmiştir, bu bir hata durumu değildir — bu yüzden burada "Limit belirle"
    çağrısı, uyarı rengi ve ikon yoktur.

    Ritim (§3.1): chip satırı → 24 → sayı → 24 → gün özeti. Kart yay
    varyantından kısadır; daha az bilgi daha az yer tutar, boşluk doldurulmaz.
    """
    return f'''          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                <div class="t-label c-2">{sag_etiket}</div>
              </div>
              <div class="h24"></div>
              {para_hero(sayi)}
              <div class="t-label c-2">{etiket}</div>
              <div class="h24"></div>
              <div class="t-body" style="text-align:center">{alt_metin}</div>
            </div>
          </div>'''

# ---------------------------------------------------------------- A · normal
A = f'''{basi()}
{hero("120", "bugün kalan", "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", 0.60)}
          <div class="h24"></div>
{kat_karti()}
          <div class="h24"></div>
{liste_basligi("Günlük toplam 180 ₺")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Ulaşım", "09.05 · Kart", "42 ₺")}
            <div class="h8"></div>
            {satir("Market", "18.40 · Kart", "43 ₺")}
          </div>
          <div class="h24"></div>'''

# ------------------------------------------------------------ B · limit dışı
B = f'''{basi()}
{hero("60", "limit dışı", "Limitin 60 ₺ üzerindesin.", 1.0, over=0.20, sayi_cls=" c-warn")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="kolon esnek">
                <div class="t-h2">Bu ay 6. limit aşımı</div>
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
{kat_karti(tasma=True)}
          <div class="h24"></div>
{liste_basligi("Günlük toplam 360 ₺")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Restoran", "21.30 · Kart · Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü", "1.250,50 ₺", limit_disi=True)}
            <div class="h8"></div>
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Akaryakıt", "17.10 · Kart", "820 ₺", basili=True)}
          </div>
          <div class="h24"></div>'''


# ------------------------------------------------------------- F · limitsiz
# ekran-envanteri §5, E-10 satırı: "boş = ... var **limitsiz**".
# Günlük limit yok → yay yok. Kategori limitleri AYRI bir karardır ve
# duruyor: ikisinin birbirine bağlı olmadığı bu yüzeyde görünür.
F = f'''{basi()}
{hero_yaysiz("180", "bugün harcanan",
             "Bugün 3 kayıt yazdın. Limit koymadığın için kalan gösterilmiyor.")}
          <div class="h24"></div>
{kat_karti()}
          <div class="h24"></div>
{liste_basligi("3 kayıt")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Ulaşım", "09.05 · Kart", "42 ₺")}
            <div class="h8"></div>
            {satir("Market", "18.40 · Kart", "43 ₺")}
          </div>
          <div class="h24"></div>'''

# ------------------------------------------------------------------ C · boş
C = f'''{basi()}
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                <div class="t-label c-2">Günlük limit 300 ₺</div>
              </div>
              <div class="h12"></div>
              <div class="hero-daire hero-daire-bos">
                {hero_gauge(0, bos=True, cap=176)}
                <div class="hero-orta">
                  {para_hero("300")}
                  <div class="t-label c-2">bugün kalan</div>
                </div>
              </div>
              <div class="h12"></div>
              <div class="t-h2">Bugün boş</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Bugün henüz bir şey yazmadın. İlk kahve iyi bir başlangıç.</div>
              <div class="h12"></div>
              <button class="btn-primary" aria-label="Harcama ekle">{icon("plus")}<div class="w8"></div>Harcama ekle</button>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-strong">Kategori limitleri</div>
                <div class="h8"></div>
                <div class="t-cap">Aylık. Boş bırakırsan takip edilmez.</div>
                <div class="h12"></div>
                <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Limit belirle</button>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- D · yükleniyor
def isk(w, h, r="999px"):
    return f'<div class="iskelet" style="width:{w};height:{h};border-radius:{r}"></div>'


D = f'''{basi()}
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                {isk("88px","40px")}
                {isk("120px","16px")}
              </div>
              <div class="h12"></div>
              <div class="hero-daire">
                {hero_gauge(0, bos=True)}
                <div class="hero-orta">{isk("128px","40px")}<div class="h8"></div>{isk("88px","16px")}</div>
              </div>
              <div class="h12"></div>
              {isk("240px","16px")}
              <div class="h8"></div>
              {isk("176px","16px")}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {isk("160px","20px")}
              <div class="h8"></div>
              <div class="satir">{isk("44px","44px","16px")}<div class="w12"></div><div class="esnek kolon">{isk("120px","24px")}<div class="h8"></div>{isk("100%","12px")}<div class="h4"></div>{isk("80px","18px")}</div></div>
              <div class="h12"></div>
              <div class="satir">{isk("44px","44px","16px")}<div class="w12"></div><div class="esnek kolon">{isk("120px","24px")}<div class="h8"></div>{isk("100%","12px")}<div class="h4"></div>{isk("80px","18px")}</div></div>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad kolon">
            <div class="satir-kart">{isk("44px","44px","16px")}<div class="w12"></div><div class="esnek kolon">{isk("70%","16px")}<div class="h8"></div>{isk("45%","12px")}</div></div>
            <div class="h8"></div>
            <div class="satir-kart">{isk("44px","44px","16px")}<div class="w12"></div><div class="esnek kolon">{isk("55%","16px")}<div class="h8"></div>{isk("40%","12px")}</div></div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------------- E · hata
# Toast tokens.md §7.9 uyarınca ÜSTTE, durum çubuğunun hemen altında.
E = f'''          <div class="h8"></div>
          <div class="pad">
            <div class="toast">
              <div class="nokta" style="background-color:var(--warning)"></div>
              <div class="w12"></div>
              <div class="esnek t-body">95 ₺ kaydedildi · 60 ₺ limit dışı</div>
              <div class="w12"></div>
              <button class="btn-ghost" style="padding:0 16px;height:44px;flex:0 0 auto">Geri al</button>
            </div>
          </div>
          <div class="h12"></div>
{basi()}
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="hata-daire">{icon("refresh")}</div>
              <div class="h24"></div>
              <div class="t-h2">Kayıtlar açılamadı</div>
              <div class="h8"></div>
              <div class="t-body" style="text-align:center">Bir şey ters gitti. Yeniden denemek çoğu zaman yeterli.</div>
              <div class="h24"></div>
              <button class="btn-primary" aria-label="Yeniden dene">{icon("refresh")}<div class="w8"></div>Yeniden dene</button>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad kolon">
            <div class="satir-kart">
              <div class="kat-kab kat-duman">{icon("circle-dashed")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-body c-2">Bugünkü kayıtlar</div>
                <div class="t-cap tek-satir">Liste açılınca burada görünür.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

units = "".join([
    device("BUGÜN", "limit altı · varsayılan", A, sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Mood:</b> tek ağırlık merkezi. Mavi kil panel → beyaz kil topak → çukur oluk → "
           "kabarık yay → kabarık topuz: dört katmanlı derinlik. Kahraman sayı ekranda tektir (56pt)."),
    device("BUGÜN", "limit dışı · uzun metin", B, sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Limit dışı utandırmadan:</b> kırmızı yok, ünlem yok, ikon değişmiyor. Ana yay dolu kalır, "
           "dışına ikinci amber yay çıkar. Restoran satırı hem <b>limit dışı</b> hem <b>en uzun tutar/not</b> "
           "testidir; not tek satıra kırpılır. Akaryakıt satırı <b>basılı (pressed)</b> durumdadır."),
    device("BUGÜN", "limitsiz · yay yok", F, sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Limit yoksa yay da yok.</b> Yay bir oranı anlatır; dolacak bir eşik olmadığında boş oluk "
           "çizmek \"bir şey eksik\" yalanı söyler. <code>EmptyGauge</code> de kullanılmadı — o, verinin "
           "beklendiği yerde durur; burada <b>veri var, eşik yok</b>. Yeni bileşen: <code>HeroPlain</code>. "
           "<b>Kahraman sayının anlamı değişti:</b> \"bugün kalan\" → <b>\"bugün harcanan\"</b>. "
           "Sağ üstte \"Limit yok\" bir uyarı değil, bir <b>değerdir</b> (E-17'deki satırlarla aynı dize). "
           "\"Limit belirle\" çağrısı, amber renk ve ünlem <b>bilinçli olarak yok</b>: limitsiz kalmak "
           "geçerli bir seçim, kapatılacak bir açık değil. Liste başlığı \"Günlük toplam\" yerine "
           "\"3 kayıt\" der — toplam zaten kahraman sayıdır, iki kez yazılmaz. Kategori limitleri kartı "
           "duruyor: aylık kategori limiti, günlük limitten <b>bağımsız</b> bir karardır."),
    device("BUGÜN", "boş durum · ilk gün", C, sabit_alt=sekme_cubugu("bugun", fab=False), note=
           "<b>Boş durum:</b> yay çizilmez, oluk boş çukur olarak durur. Kahraman sayı yerinde kalır — "
           "limitin tamamı duruyor. <b>FAB gizlenir:</b> ekranın tek birincil eylemi karttaki butondur "
           "(ekran başına en fazla 1 birincil buton)."),
    device("BUGÜN", "yükleniyor · iskelet", D, sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Yükleniyor:</b> shimmer yok, spinner yok. Gerçek düzenin kutuları yerinde kalır, içleri "
           "çukur bloklara döner — sayfa zıplamaz."),
    device("BUGÜN", "hata + toast", E, sabit_alt=sekme_cubugu("bugun"), note=
           "<b>Hata:</b> ne olduğunu değil <b>ne yapılacağını</b> söyler — depolama/mimari anlatılmaz. "
           "İllüstrasyon boş durumdan <b>farklı</b>: yay değil, küçük çukur daire. En üstte limit dışı "
           "<b>toast</b>: amber nokta + Geri al, 4 sn sonra kaybolur, modal değil."),
])

OUT.write_text(page(
    "Trinkow · Bugün (pano) — prototip v3",
    "E-10 · Bugün (pano)",
    "Arketip F — Focus / hero card · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
