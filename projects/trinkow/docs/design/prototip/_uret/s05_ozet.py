# -*- coding: utf-8 -*-
"""E-16 Ozet · E-15 Kategori detayi · E-18 Taksitler.
E-16 mood: OLCUM SAYFASI — hairline WeekStrip + tabular sayi sutunu."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

ESIK = 48   # gunluk limitin piksel karsiligi (cubuk alani 96px, 2x tasma gorunur)


def weekstrip(gunler, limit=300):
    """gunler: [(gun_no, toplam veya None)] — None = kayit girilmemis gelecek gun."""
    kolonlar = ""
    for gun, toplam in gunler:
        if toplam is None:
            ic_ = div("wbar-empty", "", "height:4px")
        elif toplam == 0:
            ic_ = div("wbar-empty", "", "height:4px")
        else:
            h = int(round(toplam / limit * ESIK))
            if toplam > limit:
                dolu = ESIK
                tasan = min(h - ESIK, 44)
                ic_ = div("wbar-over", "", f"height:{tasan}px") + div("wbar", "", f"height:{dolu}px")
            else:
                ic_ = div("wbar", "", f"height:{h}px")
        kolonlar += div("weekcol", ic_)
    cizgi = div("wthr", "", f"position:absolute;left:0;right:0;bottom:{ESIK}px")
    return div("col", div("week", kolonlar, "position:relative") + cizgi
               if False else
               f'<div class="col" style="position:relative"><div class="week">{kolonlar}</div>'
               f'<div class="wthr" style="position:absolute;left:0;right:0;bottom:{ESIK}px"></div></div>')


def gun_no_satiri(gunler):
    out = ""
    for gun, _ in gunler:
        out += div("weekcol",
                   f'<span class="t-micro c-ink2 tab-num">{gun}</span>')
    return div("week", out, "height:16px;align-items:center")


def ozet_satiri(etiket, deger, renk="c-ink", basili=False):
    return div("row between px20",
               T("t-body", "c-ink", etiket)
               + f'<span class="t-amount {renk} tab-num right">{deger}</span>',
               "min-height:56px;background:" + ("#F4F1EA" if basili else "#FFFDF8"))


def kat_satiri(ad, tutar, oran, tasma=0, basili=False):
    """oran/tasma: flex paylari. CategoryLimitBar 4pt — ayni renk kurallari."""
    if tasma:
        bar = div("minibar",
                  div("minibar-fill", "", f"flex:{oran} 1 0")
                  + div("minibar-over", "", f"flex:{tasma} 1 0"), "align-self:stretch")
    else:
        bar = div("minibar",
                  div("minibar-fill", "", f"flex:{oran} 1 0")
                  + div("", "", f"flex:{100-oran} 1 0;height:4px"), "align-self:stretch")
    return div("row px20",
               div("shrink0", ic(CAT_ICON[ad], 20, "#5C574C"), "width:20px") + wsp(16)
               + div("col grow",
                     div("row between",
                         f'<span class="t-body c-ink clip1">{ad}</span>'
                         + f'<span class="t-amount {"c-edge" if tasma else "c-ink"} tab-num">{tutar}</span>')
                     + sp(8) + bar)
               + wsp(12) + ic("chevron-right", 20, "#5C574C", 1.75, "Ayrıntıyı aç"),
               "min-height:64px;padding-top:12px;padding-bottom:12px;background:"
               + ("#F4F1EA" if basili else "#FFFDF8"))


HAFTA = [(4, 180), (5, 300), (6, 420), (7, 90), (8, 0), (9, 260), (10, 360)]
HAFTA_ORTA = [(4, 180), (5, 300), (6, 420), (7, 90), (8, None), (9, None), (10, None)]
HAFTA_DISI = [(4, 380), (5, 420), (6, 510), (7, 340), (8, 460), (9, 390), (10, 600)]
HAFTA_BOS = [(4, None), (5, None), (6, None), (7, None), (8, None), (9, None), (10, None)]

def push(baslik, govde, alt=None):
    return div("scroll",
               div("row px20",
                   iconbtn("chevron-left", "Geri dön") + wsp(4)
                   + f'<span class="t-h1 c-ink clip1">{baslik}</span>',
                   "min-height:44px")
               + sp(24) + govde) + (alt if alt else "")


if __name__ == "__main__":
    bloklar = []


    def ozet_ekran(hafta, ust_metin, alt_bloklar, basili_satir=False):
        return div("scroll",
                   div("row between px20", T("t-h1", "c-ink", "Özet"), "min-height:44px")
                   + sp(16)
                   + div("col px20",
                         div("row between",
                             T("t-label", "c-ink2", "Bu hafta")
                             + T("t-caption", "c-ink2", "4–10 Eylül"))
                         + sp(16) + weekstrip(hafta) + sp(8) + gun_no_satiri(hafta)
                         + sp(8) + f'<span class="t-caption c-ink2">{ust_metin}</span>')
                   + sp(24) + alt_bloklar) + tabbar("ozet")


    # ------------------------------------------------------------- E-16 dolu
    bloklar.append(item(
        "E-16", "Özet · dolu hafta",
        "Grafik değil çizelge: hairline çubuklar, tek yatay eşik çizgisi, "
        "ızgara yok, degrade yok, üç boyut yok. Eşiği aşan günün üst parçası Kiremit.",
        ozet_ekran(HAFTA, "Bu hafta 4 gün limit altında.",
                   div("divider")
                   + ozet_satiri("Haftalık toplam", "1.610 ₺")
                   + div("divider-56")
                   + ozet_satiri("Günlük ortalama", "230 ₺")
                   + div("divider")
                   + sp(24)
                   + div("col px20",
                         div("card",
                             T("t-label", "c-ink2", "Küçük harcamalar") + sp(8)
                             + T("t-h2", "c-ink", "50 ₺ altı 14 harcama") + sp(4)
                             + T("t-display", "c-ink", "420 ₺") + sp(8)
                             + T("t-caption", "c-ink3", "Haftalık toplamın dörtte biri.")))
                   + sp(24)
                   + div("row between px20",
                         T("t-label", "c-ink2", "En çok harcadığın kategori")
                         + T("t-label", "c-acc", "Tümünü gör"))
                   + sp(12) + div("divider")
                   + kat_satiri("Restoran", "620 ₺", 62)
                   + div("divider-56")
                   + kat_satiri("Market", "410 ₺", 41, basili=True)
                   + div("divider-56")
                   + kat_satiri("Kafe", "285 ₺", 28)
                   + div("divider"))))

    # ------------------------------------------------------------- E-16 hafta ortasi
    bloklar.append(item(
        "E-16", "Özet · hafta ortası (eksik günler)",
        "Gelecek günler yalnızca oluk — sıfır harcama gibi gösterilmez. "
        "Ortalama yalnız geçen günlere bölünür, tahmin uydurulmaz.",
        ozet_ekran(HAFTA_ORTA, "Bu hafta 2 gün limit altında.",
                   div("divider")
                   + ozet_satiri("Haftalık toplam", "990 ₺")
                   + div("divider-56")
                   + ozet_satiri("Günlük ortalama", "247 ₺")
                   + div("divider-56")
                   + ozet_satiri("Önümüzdeki ay taksit yükü", "3.124 ₺")
                   + div("divider")
                   + sp(16)
                   + div("col px20", btn_s("Taksitleri gör"))
                   + sp(24)
                   + div("row between px20",
                         T("t-label", "c-ink2", "En çok harcadığın kategori"))
                   + sp(12) + div("divider")
                   + kat_satiri("Restoran", "420 ₺", 42)
                   + div("divider-56")
                   + kat_satiri("Kafe", "285 ₺", 28)
                   + div("divider"))))

    # ------------------------------------------------------------- E-16 tum hafta disi
    bloklar.append(item(
        "E-16", "Özet · tüm hafta limit dışı",
        "Yedi gün de eşiğin üstünde. Ekran suçlayıcı bir dil kurmaz: sayıyı "
        "söyler, yorumu kullanıcıya bırakır. Kırmızı yok.",
        ozet_ekran(HAFTA_DISI, "Bu hafta 7 gün limit dışı.",
                   div("divider")
                   + ozet_satiri("Haftalık toplam", "3.100 ₺")
                   + div("divider-56")
                   + ozet_satiri("Günlük ortalama", "443 ₺", "c-edge")
                   + div("divider")
                   + sp(24)
                   + div("col px20",
                         div("card",
                             T("t-h2", "c-ink", "Bu ay 6. limit aşımı") + sp(8)
                             + T("t-body", "c-ink2", "Limit gerçekçi mi. Birlikte bakalım.")
                             + sp(24) + btn_s("Limiti gözden geçir")))
                   + sp(24)
                   + div("row between px20", T("t-label", "c-ink2", "En çok harcadığın kategori"))
                   + sp(12) + div("divider")
                   + kat_satiri("Restoran", "1.240 ₺", 100, tasma=24)
                   + div("divider-56")
                   + kat_satiri("Market", "860 ₺", 86)
                   + div("divider"))))

    # ------------------------------------------------------------- E-16 bos + yukleniyor
    bloklar.append(item(
        "E-16", "Özet · hafta boş",
        "Eşik çizgisi tek başına durur — cetvel var, ölçülecek şey yok. "
        "Metin E-10 ve E-14'ün boş metinlerinden farklıdır.",
        ozet_ekran(HAFTA_BOS, "Bu hafta henüz kayıt yok.",
                   sp(32)
                   + div("col px20 mid-x",
                         tally() + sp(24) + T("t-h2", "c-ink", "Özet için erken") + sp(8)
                         + '<span class="t-body c-ink2 mid">Birkaç kayıt sonra burada'
                           ' haftalık dağılımı görürsün.</span>'
                         + sp(24)
                         + div("btn-p", ic("plus", 24, "#FFFDF8") + wsp(8)
                               + T("t-bodys", "c-page", "Harcama ekle"),
                               "align-self:stretch")))))

    bloklar.append(item(
        "E-16", "Özet · yükleniyor",
        "Skeleton yalnız ≥150ms okuma için. Parıldama yok; hairline "
        "dikdörtgenler yerlerini tutar, düzen zıplamaz.",
        div("scroll",
            div("row between px20", T("t-h1", "c-ink", "Özet"), "min-height:44px")
            + sp(16)
            + div("col px20",
                  skeleton("88px", 18, 16) + skeleton("100%", 96, 12)
                  + skeleton("100%", 16, 16) + skeleton("208px", 18, 0))
            + sp(24) + div("divider")
            + div("col px20",
                  sp(16) + skeleton("100%", 24, 16) + skeleton("100%", 24, 16)
                  + skeleton("100%", 24, 16))
            + div("divider")
            + div("col px20", sp(24) + skeleton("100%", 112, 0)))
        + tabbar("ozet")))


    # ------------------------------------------------------------- E-15 kategori detayi


    bloklar.append(item(
        "E-15", "Kategori detayı · limit var",
        "Kategori renk taşımaz; başlıkta bile ikon + isim ile ayrışır. "
        "CategoryLimitBar 4pt, aynı renk kuralları.",
        push("Kafe",
             div("col px20",
                 div("row", ic("coffee", 24, "#5C574C") + wsp(12)
                     + T("t-label", "c-ink2", "Bu ay"))
                 + sp(4) + T("t-display", "c-ink", "1.240 ₺") + sp(16)
                 + div("minibar",
                       div("minibar-fill", "", "flex:1240 1 0")
                       + div("", "", "flex:260 1 0;height:4px"), "align-self:stretch")
                 + sp(8)
                 + T("t-caption", "c-ink2", "Aylık limit 1.500 ₺ · kalan 260 ₺")
                 + sp(8)
                 + T("t-caption", "c-ink3", "Günlük ortalama 124 ₺. Tahmini."))
             + sp(24)
             + div("row between px20",
                   T("t-label", "c-ink2", "18 kayıt")
                   + T("t-label", "c-acc", "Eylül 2026"))
             + sp(12) + div("divider")
             + spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
             + spendrow("Kafe", "Kart · 08.35", "95 ₺") + div("divider-56")
             + spendrow("Kafe", "Nakit · 15.10", "60 ₺") + div("divider-56")
             + spendrow("Kafe", "Kart · 08.42", "110 ₺") + div("divider"),
             div("col px20", btn_s("Limiti değiştir"), "padding-top:12px;padding-bottom:12px")
             + tabbar("ozet"))))

    bloklar.append(item(
        "E-15", "Kategori detayı · limit aşıldı + limit yok",
        "Üstte aylık limit aşımı (Kiremit segment), altta limitsiz kategori — "
        "çubuk çizilmez, yerine tek satır ve eylem.",
        push("Restoran",
             div("col px20",
                 div("row", ic("utensils", 24, "#5C574C") + wsp(12)
                     + T("t-label", "c-ink2", "Bu ay"))
                 + sp(4) + T("t-display", "c-edge", "2.240 ₺") + sp(4)
                 + T("t-label", "c-edge", "limit dışı") + sp(16)
                 + div("minibar",
                       div("minibar-fill", "", "flex:1500 1 0")
                       + div("minibar-over", "", "flex:740 1 0"), "align-self:stretch")
                 + sp(8) + T("t-caption", "c-edge", "Aylık limitin 740 ₺ üzerinde")
                 + sp(24) + div("divider") + sp(24)
                 + div("row", ic("shirt", 24, "#5C574C") + wsp(12)
                       + T("t-label", "c-ink2", "Giyim · bu ay"))
                 + sp(4) + T("t-h1", "c-ink", "820 ₺") + sp(8)
                 + T("t-caption", "c-ink2", "Bu kategoride limit yok.")
                 + sp(16) + btn_s("Limit belirle"))
             + sp(24) + div("divider")
             + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider-56")
             + spendrow("Restoran", "Kart · 13.05", "640 ₺", "overflow") + div("divider"),
             tabbar("ozet"))))

    bloklar.append(item(
        "E-15", "Kategori detayı · bu ay kayıt yok",
        "Boş durum kategori adını kullanır; sahte bir birincil eylem "
        "uydurulmaz, kullanıcı bu kategoriyi zorlanmaz.",
        push("Sağlık",
             div("col px20",
                 div("row", ic("pill", 24, "#5C574C") + wsp(12)
                     + T("t-label", "c-ink2", "Bu ay"))
                 + sp(4) + T("t-display", "c-ink", "0 ₺"))
             + sp(48)
             + div("col px20 mid-x",
                   tally() + sp(24) + T("t-h2", "c-ink", "Sağlık için kayıt yok") + sp(8)
                   + '<span class="t-body c-ink2 mid">Bu ay bu kategoride harcama'
                     ' yazmadın.</span>'),
             tabbar("ozet"))))

    bloklar.append(item(
        "E-15", "Kategori detayı · yükleniyor",
        "Başlık ve geri oku anında gelir (yönlendirme parametresinden bilinir), "
        "yalnız sayılar iskelet. Parıldama yok; kategori satırları 64pt ritmini "
        "korur, veri gelince düzen zıplamaz.",
        push("Kafe",
             div("col px20",
                 skeleton("88px", 18, 8) + skeleton("176px", 44, 16)
                 + skeleton("100%", 4, 12) + skeleton("232px", 18, 0))
             + sp(24) + div("divider")
             + div("col px20", sp(16) + skeleton("100%", 18, 0))
             + sp(12) + div("divider")
             + div("col",
                   div("col px20", sp(20) + skeleton("100%", 24, 0)) + sp(20)
                   + div("divider-56")
                   + div("col px20", sp(20) + skeleton("100%", 24, 0)) + sp(20)
                   + div("divider-56")
                   + div("col px20", sp(20) + skeleton("100%", 24, 0)) + sp(20)
                   + div("divider")),
             tabbar("ozet"))))

    # ------------------------------------------------------------- E-18 taksitler
    def taksit_satiri(ay, tutar, basili=False):
        return div("row between px20",
                   T("t-body", "c-ink", ay)
                   + f'<span class="t-amount c-ink tab-num right">{tutar}</span>',
                   "min-height:56px;background:" + ("#F4F1EA" if basili else "#FFFDF8"))


    def seri_satiri(kat, mevcut, toplam, aylik, bitis):
        return div("row px20",
                   div("shrink0", ic("layers", 20, "#5C574C", 1.75, "Taksitli işlem"),
                       "width:20px") + wsp(16)
                   + div("col grow",
                         f'<span class="t-body c-ink clip1">{kat} · {mevcut}/{toplam}</span>'
                         + f'<span class="t-caption c-ink2 clip1">{bitis} tarihinde bitiyor</span>')
                   + wsp(12)
                   + div("col shrink0",
                         f'<span class="t-amount c-ink tab-num right">{aylik}</span>',
                         "align-items:flex-end;min-width:96px"),
                   "min-height:64px;padding-top:12px;padding-bottom:12px;background:#FFFDF8")


    bloklar.append(item(
        "E-18", "Taksitler · dolu",
        "Taksit yükü aylara yayılmış hâlde. Sayılar tabular ve sağa hizalı — "
        "rakamlar dikeyde birbirine oturur.",
        push("Taksitler",
             div("col px20",
                 T("t-label", "c-ink2", "Bu ay") + sp(4)
                 + T("t-display", "c-ink", "3.124 ₺") + sp(8)
                 + T("t-caption", "c-ink3",
                     "Taksitler girildiği güne değil, ait olduğu aya yazılır."))
             + sp(24)
             + div("row between px20", T("t-label", "c-ink2", "Önümüzdeki aylar"))
             + sp(12) + div("divider")
             + taksit_satiri("Ekim 2026", "3.124 ₺") + div("divider-56")
             + taksit_satiri("Kasım 2026", "2.083 ₺", basili=True) + div("divider-56")
             + taksit_satiri("Aralık 2026", "1.041 ₺") + div("divider-56")
             + taksit_satiri("Ocak 2027", "1.041 ₺") + div("divider")
             + sp(24)
             + div("row between px20", T("t-label", "c-ink2", "Açık seriler"))
             + sp(12) + div("divider")
             + seri_satiri("Abonelik", 3, 12, "1.041,67 ₺", "Haziran 2027")
             + div("divider-56")
             + seri_satiri("Giyim", 2, 6, "1.041,33 ₺", "Şubat 2027")
             + div("divider-56")
             + seri_satiri("Sağlık", 6, 6, "1.041,00 ₺", "Bu ay")
             + div("divider"),
             tabbar("ozet"))))

    bloklar.append(item(
        "E-18", "Taksitler · boş",
        "Taksitli işlem yoksa sahte bir kart doldurulmaz. Metin kullanıcıya "
        "nasıl oluşacağını söyler, buton koymaz.",
        push("Taksitler",
             div("col px20",
                 T("t-label", "c-ink2", "Bu ay") + sp(4)
                 + T("t-display", "c-ink", "0 ₺"))
             + sp(48)
             + div("col px20 mid-x",
                   tally() + sp(24) + T("t-h2", "c-ink", "Taksitli işlem yok") + sp(8)
                   + '<span class="t-body c-ink2 mid">Kartla taksitli harcama'
                     ' girdiğinde burada listelenir.</span>'),
             tabbar("ozet"))))

    bloklar.append(item(
        "E-18", "Taksitler · yükleniyor",
        "Taksit yükü yerel veritabanından aylara toplanarak hesaplanır; ≥150ms "
        "sürerse iskelet çıkar. İki bölüm başlığı (\u2018Önümüzdeki aylar\u2019, "
        "\u2018Açık seriler\u2019) da iskelet olur — sahte başlık gösterilmez.",
        push("Taksitler",
             div("col px20",
                 skeleton("56px", 18, 8) + skeleton("152px", 44, 8)
                 + skeleton("100%", 18, 0))
             + sp(24)
             + div("col px20", skeleton("120px", 18, 0))
             + sp(12) + div("divider")
             + div("col",
                   div("col px20", sp(16) + skeleton("100%", 24, 0)) + sp(16)
                   + div("divider-56")
                   + div("col px20", sp(16) + skeleton("100%", 24, 0)) + sp(16)
                   + div("divider-56")
                   + div("col px20", sp(16) + skeleton("100%", 24, 0)) + sp(16)
                   + div("divider"))
             + sp(24)
             + div("col px20", skeleton("104px", 18, 0))
             + sp(12) + div("divider")
             + div("col",
                   div("col px20", sp(20) + skeleton("100%", 40, 0)) + sp(20)
                   + div("divider-56")
                   + div("col px20", sp(20) + skeleton("100%", 40, 0)) + sp(20)
                   + div("divider")),
             tabbar("ozet"))))

    bloklar.append(note("E-16 / E-15 / E-18 kararları", [
        "WeekStrip'te gün adı yerine ayın günü yazıldı: 'Pzt' gibi kısaltma kelime dağarcığında yok, tam ad ise 24pt sütuna sığmaz.",
        "Eşik çizgisi çubuk alanının tam ortasında (48/96px): 2 katına kadar taşma ölçek bozulmadan görünür.",
        "'50 ₺ altı 14 harcama' Latte Faktörü kartı ürünün varlık sebebi; yorum yapılmaz, yalnız toplanır.",
        "Kategori satırındaki 4pt mini çubuk LimitBar ile aynı renk kuralına uyar — ayrı bir mantık üretilmedi.",
        "E-15'te kategori ikonu başlıkta 24pt; daire zemine alınmadı, renk taşımadı.",
        "E-18'de biten seri (6/6) gizlenmez, listede kalır — dürüstlük (SummaryRow 'zero' kuralıyla aynı ilke).",
        "Üç yükleniyor hâli (E-16 · E-15 · E-18) aynı iskelet dilini kullanır: parıldama yok, düz #DCD5C6 dikdörtgen, gerçek içeriğin yüksekliğinde.",
        "İskelet 150ms'den önce hiç çizilmez; yerel okuma çoğu zaman bundan hızlıdır ve ekran doğrudan dolu gelir.",
    ]))

    page("E-16 · Özet + E-15 kategori + E-18 taksitler",
         "Ölçüm sayfası. 12 kare: dolu · hafta ortası · tüm hafta limit dışı · boş "
         "· yükleniyor · kategori (limit var/aşıldı/boş/yükleniyor) · taksitler "
         "(dolu/boş/yükleniyor).",
         bloklar, "05-ozet.html")
