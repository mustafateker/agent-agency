# -*- coding: utf-8 -*-
"""E-10 · Günlük (tarih sayfalanabilir gün ekranı) — arketip F (Focus / hero card).

v4 (K-049): sekme adı "Bugün" → **"Günlük"**; ekran yatay sayfalanır.
Mood: sakin, tek büyük nesne + **iki uçlu ölçüm aleti**. Gün geçişi okları
kahraman göstergenin iki yanında durur; sayfalama böylece ekstra dikey yer
harcamadan görünür olur ve sınırlar (bugün / ilk kayıt günü) okun `disabled`
hâliyle okunur. **Nokta dizisi göstergesi yoktur** (anti-pattern).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, hero_gauge, satir, sekme_cubugu, icon, kat_kab,
                 para_hero, isk)

OUT = pathlib.Path(__file__).parent.parent / "01-gunluk.html"


# ---------------------------------------------------------------- başlık
def seri_cip(gun: int | None, basili: bool = False) -> str:
    """Seri çipi — başlığın sağ üstünde, dokununca E-21 Seri ekranını açar.

    Neden ikon yok: brandbook §2.4 kip pill'i "metin, ikon değil" diye
    kilitler; aynı kural burada da geçerli. Alev/şimşek ikonu ayrıca
    oyunlaştırma klişesidir ve "Alışkanlıklar" kategorisinin ikonuyla
    (`footprints`) karışır. Seri **yok/kapalı** ise çip hiç çizilmez —
    ölü arayüz üretilmez.
    """
    if gun is None:
        return ""
    b = " basili" if basili else ""
    # K-054/7: görünen metinde **birim geri kondu** — "Seri 12" birimsizdi
    # ve 12'nin neyi saydığı (gün mü, harcama mı) çipten okunmuyordu.
    # Ölçüm (fontTools, 390pt): "Seri 12 gün" çipi 104px · takvim 44px ·
    # aralar 16px = 164px; en uzun başlık "03/09 Perşembe" 218px (Poppins
    # 26) ile toplam 338 ≤ 358 iç genişlik → üç hedef çakışmadan sığıyor.
    return (f'<button class="cip{b}" style="flex:0 0 auto" '
            f'aria-label="Seri {gun} gün. Seri ekranını aç">Seri {gun} gün</button>')


def basi(ust: str, baslik: str, seri: int | None = 12, seri_basili: bool = False,
         seri_iskelet: bool = False, takvim_basili: bool = False) -> str:
    """Üst satır: solda iki satırlı başlık, sağda seri çipi.

    Üst satır (`caption`) **başlığın taşımadığı bilgiyi** taşır:
      başlık "Bugün" / "Dün"  → üst satır tam tarih ("17 Eylül Perşembe")
      başlık "10/09 Perşembe" → üst satır uzaklık ("7 gün önce")
    Böylece iki satır hiçbir durumda aynı şeyi iki kez yazmaz ve başlık
    yüksekliği sayfalar arasında sabit kalır (sayfa geçişinde zıplama yok).

    Sağ üstte iki hedef var (referans uyarlaması): **seri çipi** (→ E-21) ve
    **takvim düğmesi** (→ E-24). Takvim düğmesi kaydırmanın erişilebilir
    karşılığıdır: "üç hafta önceki cumartesi" kaydırmayla bulunmaz, ekran
    okuyucuyla ise kaydırma hiç çalışmaz. Düğme veriye bağlı olmadığı için
    yükleniyor durumunda da iskelet olmaz — yerinde durur.
    """
    sag = isk("104px", "40px") if seri_iskelet else seri_cip(seri, seri_basili)
    ara = '<div class="w8"></div>' if sag else ""
    tb = " basili" if takvim_basili else ""
    takvim = (f'<button class="ikon-btn{tb}" aria-label="Gün seç">'
              f'{icon("calendar-days")}</button>')
    return f'''          <div class="ekran-basi">
            <div class="esnek kolon">
              <div class="t-cap">{ust}</div>
              <div class="t-h1 tek-satir">{baslik}</div>
            </div>
            <div class="w8"></div>
            {sag}
            {ara}
            {takvim}
          </div>'''


# ------------------------------------------------------- gün geçişi okları
def ok(yon: str, pasif: bool = False, basili: bool = False) -> str:
    cls = "ikon-btn"
    if pasif:
        cls += " pasif"
    if basili:
        cls += " basili"
    ad = "Önceki gün" if yon == "sol" else "Sonraki gün"
    ek = ' disabled aria-disabled="true"' if pasif else ""
    ikon = "chevron-left" if yon == "sol" else "chevron-right"
    return f'<button class="{cls}" aria-label="{ad}"{ek}>{icon(ikon)}</button>'


def limit_deger(metin: str, dokunulur: bool = True, basili: bool = False) -> str:
    """Kahraman kartın sağ üstü. **Bugün** sayfasında dokunulur (→ E-17):
    limitin kendisi, limiti değiştirmenin en doğru kapısıdır. **Geçmiş gün**
    sayfasında dokunulmaz değerdir — o günün limiti artık değiştirilemez."""
    if not dokunulur:
        return f'<div class="t-label c-2">{metin}</div>'
    b = " basili" if basili else ""
    return (f'<button class="cip{b}" style="flex:0 0 auto" aria-label="{metin}. Limitleri aç">'
            f'{metin}<div class="w8"></div>{icon("chevron-right")}</button>')


def hero(sayi, etiket, alt_metin, oran, over=0.0, sayi_cls="", bos=False,
         cap=224, limit_html="", sol_pasif=False, sag_pasif=False,
         sol_basili=False, kip="Takip"):
    daire_cls = "hero-daire" + (" hero-daire-bos hero-bos" if cap == 176 else "")
    return f'''          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: {kip}"><div class="nokta"></div><div class="w8"></div>{kip}</div>
                {limit_html}
              </div>
              <div class="h12"></div>
              <div class="aralik" style="width:100%">
                {ok("sol", sol_pasif, sol_basili)}
                <div class="{daire_cls}">
                  {hero_gauge(oran, over, bos, cap)}
                  <div class="hero-orta">
                    {para_hero(sayi, sayi_cls)}
                    <div class="t-label c-2">{etiket}</div>
                  </div>
                </div>
                {ok("sag", sag_pasif)}
              </div>
              <div class="h12"></div>
              <div class="t-body" style="text-align:center">{alt_metin}</div>
            </div>
          </div>'''


def hero_yaysiz(sayi, etiket, alt_metin, sag_etiket="Limit yok",
                sol_pasif=False, sag_pasif=True):
    """`HeroPlain` — YAYSIZ kahraman (limitsiz varyantı, v3'ten korundu).

    Yay bir **oranı** anlatır; limit yoksa dolacak bir eşik de yoktur.
    v4'te tek değişiklik: gün geçişi okları sayının iki yanına gelir —
    limitsiz modda da geçmiş günler gezilebilir.
    """
    return f'''          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                <div class="t-label c-2">{sag_etiket}</div>
              </div>
              <div class="h24"></div>
              <div class="aralik" style="width:100%">
                {ok("sol", sol_pasif)}
                <div class="kolon orta">
                  {para_hero(sayi)}
                  <div class="t-label c-2">{etiket}</div>
                </div>
                {ok("sag", sag_pasif)}
              </div>
              <div class="h24"></div>
              <div class="t-body" style="text-align:center">{alt_metin}</div>
            </div>
          </div>'''


# -------------------------------------------------------------- şeritler
def serit(tur, ikon, metin, kapatilabilir=False):
    renk = {"info": "var(--primary-text)", "warn": "var(--warning-ink)"}[tur]
    kapat = (f'<div class="w12"></div><button class="ikon-btn" aria-label="İpucunu kapat">{icon("x")}</button>'
             if kapatilabilir else "")
    return f'''          <div class="pad">
            <div class="serit serit-{tur}">
              <div class="ikon-kutu" style="color:{renk}">{icon(ikon)}</div>
              <div class="w12"></div>
              <div class="esnek t-cap" style="color:var(--text)">{metin}</div>
              {kapat}
            </div>
          </div>'''


def grup_satiri(ad, aylik, limit, yuzde, renk_var, bugun, kalan,
                tasma=False, ekle_basili=False):
    """**Kategori grubu satırı** — referansın "öğün grubu" satırının karşılığı.

    PM revizyonu (T-2): önceki sürümde satırın BİRİNCİL sağ değeri
    "bugün 95 ₺", çubuğu ise **aylık** limitti; iki farklı zaman ölçeği aynı
    satırın aynı hiyerarşi katmanında okunuyordu. Düzeltme:

      · birincil satır  → **aylık toplam / aylık limit** (çubukla aynı ölçek)
      · çubuk           → aylık toplam ÷ aylık kategori limiti
      · ikincil satır   → **bugün {tutar}** + kalan / limit dışı

    Böylece çubuk ve yanındaki sayı aynı şeyi ölçer; "bugün" bilgisi
    kaybolmaz, bir katman aşağı iner. Uydurma bir **günlük kategori
    limiti** yine ÜRETİLMEDİ (K-050): Trinkow'da kategori limiti aylıktır
    (E-17), günlüğü icat etmek referansı taklit etmek olurdu.

    `bugun=None` → o kategoride bugün kayıt yok. Satır gizlenmez: boş yuva
    hem hatırlatır hem "+" ile davet eder.
    """
    tam = max(100, yuzde)
    ic = round(min(yuzde, 100) * 100 / tam, 1)
    dis = round(max(0, yuzde - 100) * 100 / tam, 1)
    dolgu = (f'<div class="cubuk-dolgu" style="width:{ic}%;background-color:{renk_var}"></div>'
             + (f'<div class="cubuk-dolgu" style="width:{dis}%;background-color:var(--warning)"></div>'
                if dis else ''))
    # Birincil sağ küme küçülmez (`flex:0 0 auto`), ad küçülür ve gerekirse
    # kırpılır: "Alışkanlıklar" + "2.180 ₺ / 3.000 ₺" satırı taşırmasın.
    ust_sag = (f'<div class="satir" style="flex:0 0 auto">'
               f'<div class="t-amount">{aylik}</div><div class="w8"></div>'
               f'<div class="t-cap">/ {limit}</div></div>')
    alt_sol = ('<div class="t-cap">bugün kayıt yok</div>' if bugun is None
               else f'<div class="t-cap">bugün {bugun}</div>')
    alt_sag = (f'<div class="t-label c-warn" style="flex:0 0 auto">{kalan} limit dışı</div>' if tasma
               else f'<div class="t-label c-2" style="flex:0 0 auto">kalan {kalan}</div>')
    eb = " basili" if ekle_basili else ""
    return f'''              <div class="satir">
                {kat_kab(ad)}
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="aralik">
                    <div class="t-strong esnek tek-satir">{ad}</div>
                    <div class="w12"></div>
                    {ust_sag}
                  </div>
                  <div class="h8"></div>
                  <div class="cubuk-oluk">{dolgu}</div>
                  <div class="h4"></div>
                  <div class="aralik">
                    {alt_sol}
                    <div class="w12"></div>
                    {alt_sag}
                  </div>
                </div>
                <div class="w12"></div>
                <button class="ekle-btn{eb}" aria-label="{ad} kategorisine harcama ekle">{icon("plus")}</button>
              </div>'''


def grup_karti(tasma=False, ekle_basili=False):
    """Kategori grupları kartı. **Aylık** limit taşıdığı için yalnız "Bugün"
    sayfasında görünür: geçmiş gün sayfasında bu ayın sayısını göstermek, o
    günün sayfasında o güne ait olmayan bir sayı göstermek olurdu.

    Sıra **bugünkü tutara göre** azalan: ekranın üstünde bugün parayı en çok
    nereye verdiğin durur. En sonda bugün kaydı olmayan bir grup: boş yuva
    hem hatırlatır hem "+" ile davet eder.
    """
    satirlar = [
        grup_satiri("Kafe", "940 ₺", "800 ₺" if tasma else "1.200 ₺",
                    118 if tasma else 78, "var(--cat-amber)",
                    bugun="95 ₺", kalan="140 ₺" if tasma else "260 ₺", tasma=tasma),
        grup_satiri("Market", "2.180 ₺", "3.000 ₺", 73, "var(--cat-yesil)",
                    bugun="43 ₺", kalan="820 ₺"),
        grup_satiri("Ulaşım", "410 ₺", "600 ₺", 68, "var(--cat-mavi)",
                    bugun="42 ₺", kalan="190 ₺", ekle_basili=ekle_basili),
        grup_satiri("Restoran", "480 ₺", "700 ₺", 69, "var(--cat-amber)",
                    bugun=None, kalan="220 ₺"),
    ]
    ic = '\n              <div class="h16"></div>\n'.join(satirlar)
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="aralik">
                <div class="kolon">
                  <div class="t-h2">Kategoriler</div>
                  <div class="h4"></div>
                  <div class="t-cap tek-satir">Bu ay · kategori limiti</div>
                </div>
                <button class="btn-ghost" style="padding:0 16px;flex:0 0 auto" aria-label="Tüm kategoriler"><div class="tek-satir">Tümünü gör</div></button>
              </div>
              <div class="h16"></div>
{ic}
            </div>
          </div>'''


def liste_basligi(baslik, sag):
    return f'''          <div class="pad aralik">
            <div class="t-h2">{baslik}</div>
            <div class="t-label c-2">{sag}</div>
          </div>'''


def liste(satirlar):
    ic = '\n            <div class="h8"></div>\n            '.join(satirlar)
    return f'''          <div class="pad kolon">
            {ic}
          </div>'''


# ---------------------------------------------------- A · bugün, limit altı
A = f'''{basi("17 Eylül Perşembe", "Bugün")}
{hero("120", "bugün kalan", "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", 0.60,
      limit_html=limit_deger("Günlük limit 300 ₺"), sag_pasif=True)}
          <div class="h24"></div>
{grup_karti()}
          <div class="h24"></div>
{liste_basligi("Bugünkü kayıtlar", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
{liste([satir("Kafe", "08.20 · Nakit", "95 ₺"),
        satir("Ulaşım", "09.05 · Kart", "42 ₺"),
        satir("Market", "09.20 · Kart", "43 ₺")])}
          <div class="h24"></div>'''

# ------------------------------------------- A2 · ilk açılış, kaydırma ipucu
# K-057/8 · KESME HİZASI. Bu yüzeyin v4 ilk turundaki hâli 669px'lik kaydırma
# alanında **ikinci liste satırını ortasından** kesiyordu: tutarın üst yarısı
# görünüyor, alt yarısı kalıyordu ve "95 ₺" yanlış okunabiliyordu. Ayrıca
# liste başlığı "Günlük toplam 180 ₺" derken listede iki satır (137 ₺) vardı —
# üçüncü kayıt hiç çizilmemişti, yani veri de kendi içinde tutarsızdı.
#
# Çözüm **pikselden değil içerikten**: bu yüzey artık **tek kayıtlı bir gün**.
# Kaydırma ipucu şeridi (68 + 24) zaten bu yüzeye özgü; onunla birlikte
# içerik 659px'te biter → 669px'lik alanda **hiçbir nesne kesilmez** ve
# dikey ritmin (tokens §3.1) tek bir değeri bile değişmez. Dikey kaydırma
# ipucu asıl yüzeyde (A) üç kayıt + kategori kartıyla zaten var; bu yüzeyin
# işi **yatay** sayfalamayı öğretmek.
A2 = f'''{basi("17 Eylül Perşembe", "Bugün")}
{hero("205", "bugün kalan", "Bugün 95 ₺. Limitinin 205 ₺ altındasın.", 0.3167,
      limit_html=limit_deger("Günlük limit 300 ₺"), sag_pasif=True, sol_basili=True)}
          <div class="h24"></div>
{serit("info", "chevron-left", "Geçmiş günler solda. Sağa kaydır.", kapatilabilir=True)}
          <div class="h24"></div>
{liste_basligi("Bugünkü kayıtlar", "Günlük toplam 95 ₺")}
          <div class="h8"></div>
{liste([satir("Kafe", "08.20 · Nakit", "95 ₺")])}
          <div class="h24"></div>'''

# ----------------------------------------------- I · milestone kutlaması
KUTLAMA = f'''          <div class="katman-bas">
            <div class="pad" style="padding-top:8px">
              <button class="kutlama kart-ic kolon orta" style="width:100%" aria-label="Kutlamayı kapat">
                <div class="kutlama-disk"><div class="t-display">7</div></div>
                <div class="h12"></div>
                <div class="t-h2">7 gün</div>
                <div class="h8"></div>
                <div class="t-body" style="text-align:center">Seri 7 güne ulaştı. Sıradaki durak 14 gün.</div>
                <div class="h8"></div>
                <div class="t-cap">Dokununca kapanır</div>
              </button>
            </div>
          </div>'''

I = f'''{basi("17 Eylül Perşembe", "Bugün", seri=7)}
{hero("120", "bugün kalan", "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", 0.60,
      limit_html=limit_deger("Günlük limit 300 ₺"), sag_pasif=True)}
          <div class="h24"></div>
{liste_basligi("Bugünkü kayıtlar", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
{liste([satir("Kafe", "08.20 · Nakit", "95 ₺"),
        satir("Ulaşım", "09.05 · Kart", "42 ₺")])}
          <div class="h24"></div>'''

# ------------------------------------------ B · bugün, limit dışı, uzun metin
B = f'''{basi("17 Eylül Perşembe", "Bugün")}
{hero("60", "limit dışı", "Limitin 60 ₺ üzerindesin.", 1.0, over=0.20,
      sayi_cls=" c-warn", limit_html=limit_deger("Günlük limit 300 ₺", basili=True),
      sag_pasif=True)}
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
{grup_karti(tasma=True)}
          <div class="h24"></div>
{liste_basligi("Bugünkü kayıtlar", "Günlük toplam 360 ₺")}
          <div class="h8"></div>
{liste([satir("Restoran", "21.30 · Kart · Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü", "1.250,50 ₺", limit_disi=True),
        satir("Kafe", "08.20 · Nakit", "95 ₺"),
        satir("Akaryakıt", "17.10 · Kart", "820 ₺", basili=True)])}
          <div class="h24"></div>'''

# --------------------------------------------------------------- G1 · Dün
G1 = f'''{basi("16 Eylül Çarşamba", "Dün")}
{hero("290", "o gün harcanan", "Gün kapandı. 4 kayıt, 290 ₺.", 0.967,
      limit_html=limit_deger("O gün limiti 300 ₺", dokunulur=False))}
          <div class="h24"></div>
{serit("info", "check", "Bu gün seriye sayıldı.")}
          <div class="h24"></div>
{liste_basligi("O günün kayıtları", "Günlük toplam 290 ₺")}
          <div class="h8"></div>
{liste([satir("Kafe", "08.10 · Nakit", "60 ₺"),
        satir("Ulaşım", "08.45 · Kart", "42 ₺"),
        satir("Market", "13.20 · Kart", "118 ₺"),
        satir("Restoran", "20.15 · Kart", "70 ₺")])}
          <div class="h24"></div>'''

# ------------------------------------------ G2 · eski gün, limit dışı kapandı
G2 = f'''{basi("7 gün önce", "10/09 Perşembe")}
{hero("360", "o gün harcanan", "Gün kapandı. 360 ₺, limitin 60 ₺ üzerinde.", 1.0,
      over=0.20, sayi_cls=" c-warn",
      limit_html=limit_deger("O gün limiti 300 ₺", dokunulur=False))}
          <div class="h24"></div>
{serit("warn", "circle-slash", "Bu gün seriye sayılmadı.")}
          <div class="h24"></div>
{liste_basligi("O günün kayıtları", "Günlük toplam 360 ₺")}
          <div class="h8"></div>
{liste([satir("Akaryakıt", "17.10 · Kart", "820 ₺", limit_disi=True),
        satir("Market", "12.05 · Kart", "215 ₺"),
        satir("Kafe", "08.30 · Nakit", "45 ₺")])}
          <div class="h24"></div>'''

# ----------------------------- G3 · ilk kayıt günü (SOL uç · geriye sınır)
G3 = f'''{basi("97 gün önce", "12/06 Cuma")}
{hero("180", "o gün harcanan", "Gün kapandı. 2 kayıt, 180 ₺.", 0.72,
      limit_html=limit_deger("O gün limiti 250 ₺", dokunulur=False), sol_pasif=True)}
          <div class="h24"></div>
{serit("info", "info", "İlk kaydın bu gün. Daha geriye kayıt yok.")}
          <div class="h24"></div>
{liste_basligi("O günün kayıtları", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
{liste([satir("Market", "19.40 · Kart", "155 ₺"),
        satir("Kafe", "09.15 · Nakit", "25 ₺")])}
          <div class="h24"></div>'''

# ---------------------------------------------- G4 · harcamasız gün işaretleme
G4 = f'''{basi("14 gün önce", "03/09 Perşembe")}
{hero("0", "o gün harcanan", "O gün hiç kayıt yazmadın.", 0, bos=True, cap=176,
      limit_html=limit_deger("O gün limiti 300 ₺", dokunulur=False))}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="t-h2">Harcamasız gün</div>
              <div class="h8"></div>
              <div class="t-body">O gün kayıt yok. Kayıtsız gün seriye sayılmaz.</div>
              <div class="h8"></div>
              <div class="t-cap">Harcamasız geçtiyse işaretle, seri korunur.</div>
              <div class="h12"></div>
              <button class="btn-secondary">{icon("check")}<div class="w8"></div>Harcamasız işaretle</button>
            </div>
          </div>
          <div class="h24"></div>'''

# ------------------------------------------------------------- F · limitsiz
F = f'''{basi("17 Eylül Perşembe", "Bugün", seri=None)}
{hero_yaysiz("180", "bugün harcanan",
             "Bugün 3 kayıt yazdın. Limit koymadığın için kalan gösterilmiyor.")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic satir-ust">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-strong">Seri kapalı</div>
                <div class="h8"></div>
                <div class="t-cap">Seri için günlük limit gerekir.</div>
                <div class="h12"></div>
                <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Limit belirle</button>
              </div>
            </div>
          </div>
          <div class="h24"></div>
{grup_karti()}
          <div class="h24"></div>
{liste_basligi("Bugünkü kayıtlar", "3 kayıt")}
          <div class="h8"></div>
{liste([satir("Kafe", "08.20 · Nakit", "95 ₺"),
        satir("Ulaşım", "09.05 · Kart", "42 ₺"),
        satir("Market", "09.20 · Kart", "43 ₺")])}
          <div class="h24"></div>'''

# ------------------------------------------------------ C · boş · ilk gün
C = f'''{basi("17 Eylül Perşembe", "Bugün", seri=None)}
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                <div class="cip secili" aria-label="Kip: Takip"><div class="nokta"></div><div class="w8"></div>Takip</div>
                {limit_deger("Günlük limit 300 ₺")}
              </div>
              <div class="h12"></div>
              <div class="aralik" style="width:100%">
                {ok("sol", True)}
                <div class="hero-daire hero-daire-bos">
                  {hero_gauge(0, bos=True, cap=176)}
                  <div class="hero-orta">
                    {para_hero("300")}
                    <div class="t-label c-2">bugün kalan</div>
                  </div>
                </div>
                {ok("sag", True)}
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
                <div class="t-strong">Seri bugün başlar</div>
                <div class="h8"></div>
                <div class="t-cap">Günü limit altında kapatırsan seri 1 gün olur.</div>
              </div>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- D · yükleniyor
D = f'''{basi("17 Eylül Perşembe", "Bugün", seri_iskelet=True)}
          <div class="pad">
            <div class="hero-kart kart-ic kolon orta">
              <div class="aralik" style="width:100%">
                {isk("88px","40px")}
                {isk("120px","16px")}
              </div>
              <div class="h12"></div>
              <div class="aralik" style="width:100%">
                {ok("sol")}
                <div class="hero-daire">
                  {hero_gauge(0, bos=True)}
                  <div class="hero-orta">{isk("128px","40px")}<div class="h8"></div>{isk("88px","16px")}</div>
                </div>
                {ok("sag", True)}
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
{basi("17 Eylül Perşembe", "Bugün", seri=None)}
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


SEKME = sekme_cubugu("gunluk")

units = "".join([
    device("GÜNLÜK", "bugün · limit altı · seri aktif", A, sabit_alt=SEKME, note=
           "<b>Mood:</b> tek ağırlık merkezi + iki uçlu ölçüm aleti. <b>Sayfalama göstergesi nokta dizisi "
           "DEĞİL:</b> gün geçişi okları kahraman göstergenin iki yanında durur — sıfır ek dikey yer harcar "
           "ve yönü doğrudan gösterir. Sağ ok <b>pasif</b>: bugün en sağdaki sayfa, geleceğe gidilmez "
           "(pasiflik opaklıkla değil <code>disabled-bg</code> + <code>clay.sunken</code> ile). "
           "Sağ üstte <b>iki</b> hedef var: <b>Seri 12</b> çipi E-21'e, <b>takvim düğmesi</b> E-24 gün seçiciye gider; çip ikon değil metin taşır (brandbook §2.4) ve alev/şimşek klişesi yok. "
           "<b>Kategoriler kartı (T-2'de düzeltildi):</b> satırın birincil sağ değeri artık <b>aylık toplam / aylık limit</b>, yani <b>çubukla aynı zaman ölçeği</b>; \"bugün 95 ₺\" bir katman aşağıya, ikincil satıra indi. Önceki sürümde \"bugün\" tutarı ile aylık çubuk aynı hiyerarşide duruyordu ve satır iki farklı zaman ölçeğini aynı anda okutuyordu. Uydurma bir <b>günlük kategori limiti</b> yine ÜRETİLMEDİ (K-050): kategori limiti Trinkow'da aylıktır (E-17). Son satır <b>bugün kayıt yok</b> — boş yuva referanstaki \"0 / 928\" satırı gibi davet eder. "
           "Kahraman kartın sağ üstündeki <b>Günlük limit 300 ₺</b> artık dokunulur (→ E-17) ve v3'teki "
           "<code>sliders</code> ikon-butonunun yerini alır: limitin değeri, limiti değiştirmenin en "
           "doğru kapısıdır ve başlık satırı seri çipine yer açar."),
    device("GÜNLÜK", "bugün · ilk açılış · kaydırma ipucu", A2, sabit_alt=SEKME, note=
           "<b>Keşfedilebilirlik ikinci katman:</b> ilk üç açılışta bir kez görünen, kapatılabilir şerit. "
           "Oklar jesti öğretmez, jestin <b>var olduğunu</b> bu şerit söyler. Sol ok <b>basılı (pressed)</b> "
           "durumda çizildi — RN'de hover yoktur, dokunmanın tek geri bildirimi budur. "
           "<b>K-055 · yön (çevrildi):</b> bugün <b>en sağdaki</b> sayfa, geçmiş günler <b>solda</b>. "
           "İpucu tek satırda iki şey söylüyor: geçmişin nerede durduğunu ve parmağın ne yapacağını — "
           "\"Geçmiş günler solda. Sağa kaydır.\" <b>K-057/8 · kesme hizası:</b> bu yüzey tek kayıtlı "
           "bir gün; içerik 659px'te bitiyor, 669px'lik alanda <b>hiçbir satır kesilmiyor</b> ve "
           "dikey ritim değişmedi. <b>Kanal ayrımı bilinçli:</b> ok ve ikon "
           "daima <b>sayfanın yönünü</b> gösterir (sol = geçmiş), jest yönü yalnız <b>yazıyla</b> "
           "söylenir. İkisini aynı kanaldan anlatmak (sağa bakan ok + sola giden sayfa) kullanıcıda "
           "çelişki üretirdi."),
    device("GÜNLÜK", "milestone kutlaması · 7 gün", I,
           sabit_alt=f'{KUTLAMA}{SEKME}', note=
           "<b>Kutlama:</b> konfeti yok, emoji yok, parlayan gradyan patlaması yok. Ekranın üst bandında "
           "beliren tek bir <b>kil kart</b>: çukur disk içinde durak sayısı. <b>Scrim yok</b> — kutlama modal "
           "değildir; katman yalnız üst bandı kaplar, sekme çubuğunu ve FAB'ı engellemez. Süre: giriş 250ms "
           "(<code>motion.arc</code>) + bekleme 700ms + çıkış 250ms = <b>1.2 sn</b>, dokunmayla anında atlanır. "
           "Metin övgü içermez (\"tebrikler/harika\" yasak): yalnız tespit + sıradaki durak."),
    device("GÜNLÜK", "bugün · limit dışı · uzun metin", B, sabit_alt=SEKME, note=
           "<b>Limit dışı utandırmadan:</b> kırmızı yok, ünlem yok. <b>Seri uyarısı da yok:</b> "
           "\"serini kaybediyorsun\" kaybetme korkusu üretir ve brandbook §2.3'te birebir yasaktır. "
           "Seri çipi 12 günde kalır — gün henüz kapanmadı. Restoran satırı hem <b>limit dışı</b> hem "
           "<b>en uzun tutar/not</b> testi; Akaryakıt satırı <b>basılı</b>, limit çipi <b>basılı</b>."),
    device("GÜNLÜK", "dün · limit altı · seriye sayıldı", G1, sabit_alt=SEKME, note=
           "<b>Kahraman sayının anlamı gün kapanınca değişir:</b> \"bugün kalan\" → <b>\"o gün harcanan\"</b>. "
           "Kapanmış günde \"kalan\" diye bir şey yoktur; harcanacak bir şey kalmadı. Yay aynı kalır, o günün "
           "limitine göre dolar. Sağ üstteki limit <b>dokunulmaz değer</b>: geçmiş günün limiti değiştirilemez. "
           "<b>Kategoriler kartı burada YOK</b> — o kart aylık limit taşır, kapanmış bir günün sayfasına ait değildir. "
           "FAB duruyor: geçmiş güne <b>geç kayıt</b> eklenebilir (K-049), tarih o günle ön dolu gelir."),
    device("GÜNLÜK", "eski gün · tarihli başlık · seriye sayılmadı", G2, sabit_alt=SEKME, note=
           "<b>Başlık biçimi:</b> bugün/dün dışında <code>10/09 Perşembe</code>; üst satır ise başlığın "
           "taşımadığı bilgiyi verir (<code>7 gün önce</code>). İki satır hiçbir durumda aynı şeyi yazmaz. "
           "Şerit <b>amber</b>: \"Bu gün seriye sayılmadı.\" — fiil nötr, suç atfı yok, kırmızı yok."),
    device("GÜNLÜK", "ilk kayıt günü · geriye sınır", G3, sabit_alt=SEKME, note=
           "<b>Sol sınır:</b> ilk kaydın gününden geriye sayfa yok → sol ok <b>pasif</b> + tek satırlık "
           "açıklama. Sınır sessizce çalışmaz; kullanıcı neden ilerlemediğini okur. "
           "<b>O günün limiti 250 ₺</b>: limit o tarihte farklıydı ve sayfa bugünün limitini değil "
           "<b>o günün</b> limitini gösterir."),
    device("GÜNLÜK", "harcamasız gün · işaretleme", G4, sabit_alt=SEKME, note=
           "<b>Hile kapısı (K-048) arayüzde:</b> kayıt yazılmamış gün seriye sayılmaz — çünkü ürünün tezi "
           "kayıt alışkanlığıdır. Kullanıcı o günü gerçekten harcamasız geçirdiyse <b>ikincil</b> butonla "
           "işaretler ve seri korunur. Gösterge <b>boş durum yayı</b> (176pt, dolgu ve topuz yok), "
           "kahraman sayı <b>0 ₺</b> — sayı gizlenmez, dürüstlük. İşaretlendikten sonra kart yerini "
           "\"Harcamasız gün. Seriye sayıldı.\" bilgi şeridine bırakır ve buton düşer."),
    device("GÜNLÜK", "limitsiz mod · yay yok · seri kapalı", F, sabit_alt=SEKME, note=
           "<b>Limit yoksa yay da yok</b> (v3 kararı korundu, <code>HeroPlain</code>). Sağ üstte seri çipi "
           "<b>hiç çizilmez</b> — pasif bir çip ölü arayüzdür. Seri yalnızca bir kez, kartın içinde "
           "açıklanır: \"Seri için günlük limit gerekir.\" + <b>ikincil</b> \"Limit belirle\". "
           "<b>Bilinçli sapma:</b> v3'te limitsiz varyantta hiç limit çağrısı yoktu (limitsiz kalmak geçerli "
           "bir seçim). K-048 seriyi ürüne soktuğu için tek bir nötr kapı eklendi; amber renk, ünlem ve "
           "\"eksik kurulum\" tonu yine yok."),
    device("GÜNLÜK", "boş · ilk gün", C, sabit_alt=sekme_cubugu("gunluk", fab=False), note=
           "<b>İlk gün iki sınır birlikte:</b> ne geriye ne ileriye sayfa var → iki ok da pasif. "
           "Bu, sayfalamanın ilk günden itibaren <b>var olduğunu ama henüz boş olduğunu</b> dürüstçe söyler. "
           "<b>FAB gizlenir:</b> ekranın tek birincil eylemi karttaki butondur. Alt kart seriyi tanıtır "
           "ama sayı vermez — \"Seri 0 gün\" yazmak sıfırı bir başarısızlık gibi gösterirdi."),
    device("GÜNLÜK", "yükleniyor · iskelet", D, sabit_alt=SEKME, note=
           "<b>Yükleniyor:</b> shimmer yok, spinner yok. <b>Başlık gerçek kalır</b> — tarih cihazdan gelir, "
           "okumayı beklemez; yalnız seri çipi iskelet olur, çünkü seri hesaplanır. Gün okları da gerçek "
           "kalır: navigasyon veri değildir."),
    device("GÜNLÜK", "hata + toast", E, sabit_alt=SEKME, note=
           "<b>Hata:</b> ne olduğunu değil <b>ne yapılacağını</b> söyler. Seri çipi düşer: seri "
           "hesaplanamadığı için yanlış bir sayı göstermek yerine hiç gösterilmez. En üstte limit dışı "
           "<b>toast</b>: amber nokta + Geri al, modal değil."),
])

OUT.write_text(page(
    "Trinkow · Günlük (tarih sayfalanabilir) — prototip v4",
    "E-10 · Günlük",
    "Arketip F — Focus / hero card · yatay tarih sayfalama (K-049) · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)

