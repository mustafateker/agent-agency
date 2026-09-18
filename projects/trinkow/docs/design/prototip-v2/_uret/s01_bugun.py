# -*- coding: utf-8 -*-
"""E-10 Bugun / pano — arketip F (Focus / hero card).
Kahraman: 200pt dairesel gosterge. Ekranda 56pt sayi TEK tanedir.
"""
from lib import cat_box, cat_colors, hero_gauge, ico, mini_gauge, device, page, tabbar


def header(baslik: str = "Bugün", tarih: str = "11 Eylül Perşembe") -> str:
    return f"""        <div class="rn-header" data-od-id="header">
          <div class="rn-col">
            <p class="t-caption">{tarih}</p>
            <h1 class="t-h1 mt4">{baslik}</h1>
          </div>
          <button class="rn-iconbtn" type="button" aria-label="Ayarları aç">{ico('settings', 24)}</button>
        </div>"""


def hero(ratio, sayi, etiket, alt_satir, limit_satir="Günlük limit 300 ₺",
         gid="a", over=0.0, sayi_renk="", kip="Takip", etiket_renk=""):
    """Kahraman gosterge karti. 56pt sayi + 13pt etiket => oran 4.3x (>=4 sarti)."""
    renk = f' style="color:{sayi_renk}"' if sayi_renk else ""
    ecls = "t-label mt4" + ("" if etiket_renk else " c-2")
    erenk = f' style="color:{etiket_renk}"' if etiket_renk else ""
    now = int(round(ratio * 300))
    tight = "" if over > 0 else " tight"
    return f"""          <div class="rn-hero-card" data-od-id="hero">
            <div class="rn-row rn-between" style="width:100%">
              <button class="rn-pill is-selected" type="button" style="background:#FDEBD8" aria-label="Kip: {kip}. Değiştir">{kip}</button>
              <p class="t-caption">{limit_satir}</p>
            </div>
            <div class="rn-gauge{tight} mt12" role="progressbar" aria-label="Günlük limit kullanımı"
                 aria-valuemin="0" aria-valuemax="300" aria-valuenow="{now}"
                 aria-valuetext="{now} ₺ / 300 ₺ kullanıldı">
              {hero_gauge(ratio, gid, over)}
              <div class="rn-gauge-center">
                <div class="rn-hero-num">
                  <span class="t-hero"{renk}>{sayi}</span>
                  <span class="t-display"{renk}>₺</span>
                </div>
                <p class="{ecls}"{erenk}>{etiket}</p>
              </div>
            </div>
            <p class="t-body mt16" style="text-align:center">{alt_satir}</p>
          </div>"""


def bolum_basligi(baslik, eylem="Tümünü gör", alt=""):
    alt_html = f'<p class="t-caption mt4">{alt}</p>' if alt else ""
    return f"""          <div class="rn-row rn-between mt24">
            <div class="rn-col">
              <h2 class="t-h2">{baslik}</h2>
              {alt_html}
            </div>
            <button class="rn-btn ghost auto" type="button">{eylem}</button>
          </div>"""


def kategori_kutusu(ad, ratio, tutar):
    """Renk + ikon + metin birlikte: mini gostergenin rengi aile, ortadaki ikon
    aile icindeki kategori, altindaki ad da metin karsiligi."""
    solid, soft, icon = cat_colors(ad)
    return f"""            <div class="rn-card tile rn-fill" style="align-items:center;padding:16px 8px">
              <div class="rn-mini-gauge">
                {mini_gauge(ratio, solid)}
                <span style="color:{solid};display:flex">{ico(icon, 20)}</span>
              </div>
              <p class="t-amount mt8">{tutar}</p>
              <p class="t-micro mt4" style="text-align:center">{ad}</p>
            </div>"""


def kayit_satiri(ad, alt, tutar, ekstra="", cls=""):
    ek = f'<p class="t-caption c-edge">{ekstra}</p>' if ekstra else ""
    return f"""            <div class="rn-row-item{cls}">
              {cat_box(ad)}
              <div class="rn-col rn-fill">
                <p class="t-body ellipsis">{ad}</p>
                <p class="t-caption ellipsis mt4">{alt}</p>
              </div>
              <div class="rn-col" style="align-items:flex-end">
                <p class="t-amount">{tutar}</p>
                {ek}
              </div>
            </div>"""


SEP = '            <div class="rn-sep"></div>'


def icerik(gid: str = "pano"):
    kayitlar = "\n".join([
        kayit_satiri("Kafe", "09.15 · Nakit", "45 ₺"),
        SEP,
        kayit_satiri("Ulaşım", "08.40 · Kart", "30 ₺"),
        SEP,
        kayit_satiri("Restoran", "13.10 · Kart · İki kişilik öğle yemeği", "85 ₺"),
        SEP,
        kayit_satiri("Market", "18.25 · Kart", "20 ₺"),
    ])
    return f"""{header()}
        <div class="rn-pad rn-col">
{hero(0.6, "120", "bugün kalan", "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", gid=gid)}
{bolum_basligi("Bugünkü kayıtlar", "Tümünü gör", alt="4 kayıt · toplam 180 ₺")}
        </div>
        <div class="rn-col mt8">
{kayitlar}
        </div>
        <div class="rn-pad rn-col">
{bolum_basligi("Kategori limitleri", "Tümünü gör", alt="Bu ay kullanılan")}
          <div class="rn-row g12 mt12" style="align-items:stretch">
{kategori_kutusu("Market", 0.42, "1.260 ₺")}
{kategori_kutusu("Kafe", 0.78, "545 ₺")}
{kategori_kutusu("Ulaşım", 0.30, "360 ₺")}
          </div>
        </div>
        <div style="height:24px"></div>"""


if __name__ == "__main__":
    page(
        "Trinkow · Bugün",
        "E-10 · Bugün",
        "Arketip F — tek kahraman öğe. 56pt sayı ekranda bir tane; kalan her şey ondan sonra gelir",
        device(
            icerik(),
            "Varsayılan hâl · Takip kipi",
            "300 ₺ limitin 180 ₺'si harcandı · yayın grisi kalanı gösterir",
            warm=True,
            tail=tabbar("bugun"),
            note="<b>Ruhu veren:</b> göz önce göstergeye, sonra tek cümleye, sonra listeye "
                 "gidiyor. Kategori kutuları renk taşıyor ama renk tek başına bilgi değil — "
                 "her birinde ikon ve ad da var. Kahraman kart zeminden <b>elev.2</b> ile "
                 "kalkıyor, altındaki kutular <b>gölgesiz</b>: derinlik hiyerarşiyi anlatıyor, "
                 "süslemiyor.",
        ),
        "01-bugun.html",
    )
