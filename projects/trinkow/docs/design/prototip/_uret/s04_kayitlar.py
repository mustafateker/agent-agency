# -*- coding: utf-8 -*-
"""E-14 Kayitlar · E-12 Harcama detayi · E-13 Silme onayi.
E-14 mood: DEFTER — sik dikey ritim, 1px ayraclar, hic kart yok."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from s02_ekle import sheet_bas, amountbox, kat_alani, odeme_satiri, katchip, tumu_chip


def ay_secici(ay="Eylül 2026", sol_basili=False):
    return div("row between px20",
               iconbtn("chevron-left", "Önceki ay", sol_basili)
               + T("t-h2", "c-ink", ay)
               + iconbtn("chevron-right", "Sonraki ay"),
               "min-height:44px")


def gun_basligi(gun, toplam, disi=False):
    sag = (T("t-caption", "c-edge", toplam) if disi
           else T("t-caption", "c-ink2", toplam))
    return div("row between px20",
               T("t-label", "c-ink2", gun) + sag,
               "min-height:32px;background:#F4F1EA")


def swipe_sil(kategori, alt, tutar):
    panel = div("col mid-x mid-y bg-dan shrink0",
                ic("trash", 20, "#FFFDF8", 1.75, "Harcamayı sil") + sp(4)
                + T("t-label", "c-page", "Sil"), "width:88px;align-self:stretch")
    return div("row hide-x",
               div("row", panel + div("shrink0", spendrow(kategori, alt, tutar),
                                      "width:390px"), "width:478px"),
               "width:390px")


def swipe_tekrar(kategori, alt, tutar):
    panel = div("col mid-x mid-y bg-acc shrink0",
                ic("rotate-cw", 20, "#FFFDF8", 1.75, "Bu harcamayı tekrarla") + sp(4)
                + T("t-label", "c-page", "Tekrarla"), "width:88px;align-self:stretch")
    return div("row hide-x",
               div("row", div("shrink0", spendrow(kategori, alt, tutar),
                              "width:390px") + panel,
                   "width:478px;margin-left:-88px"),
               "width:390px")


BUGUN = (spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
         + spendrow("Ulaşım", "Kart · 09.05", "35 ₺") + div("divider-56")
         + spendrow("Market", "Nakit · 13.20", "50 ₺") + div("divider-56")
         + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider"))

DUN = (spendrow("Kafe", "Kart · 08.35", "95 ₺") + div("divider-56")
       + spendrow("Abonelik", "Kart · 10.00 · 3/12 taksit", "1.041 ₺", taksit=True)
       + div("divider-56")
       + spendrow("Market", "Kart · 18.10", "265 ₺") + div("divider"))

bloklar = []

# ------------------------------------------------------------- E-14 dolu
bloklar.append(item(
    "E-14", "Kayıtlar · dolu (defter ritmi)",
    "Kart yok, gölge yok. Gün başlıkları Kağıt zeminde, satırlar Sayfa "
    "zemininde; ayrım yalnız yüzey tonu + 1px ayraç.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici() + sp(8)
        + gun_basligi("Bugün · 10 Eylül", "Günlük toplam 360 ₺") + BUGUN
        + gun_basligi("Dün · 9 Eylül", "Günlük toplam 1.401 ₺") + DUN
        + gun_basligi("8 Eylül Salı", "60 ₺ limit dışı", disi=True)
        + spendrow("Akaryakıt", "Kart · 07.50", "360 ₺", "overflow"))
    + tabbar("kayitlar")))

# ------------------------------------------------------------- E-14 kaydirma
bloklar.append(item(
    "E-14", "Kayıtlar · kaydırma eylemleri",
    "Sağa kaydır → Sil (Vişne, her zaman onay diyaloğu). Sola kaydır → "
    "Tekrarla (Petrol). Latte Faktörü akışı 2 dokunuşta biter.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici() + sp(8)
        + gun_basligi("Bugün · 10 Eylül", "Günlük toplam 360 ₺")
        + swipe_sil("Kafe", "Kart · 08.40", "95 ₺") + div("divider")
        + swipe_tekrar("Ulaşım", "Kart · 09.05", "35 ₺") + div("divider")
        + spendrow("Market", "Nakit · 13.20", "50 ₺", "pressed") + div("divider-56")
        + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider"))
    + div("col px20", toast("95 ₺ yeniden eklendi", "info", "Geri al"),
          "padding-bottom:12px")
    + tabbar("kayitlar")))

# ------------------------------------------------------------- E-14 bos
bloklar.append(item(
    "E-14", "Kayıtlar · hiç kayıt yok",
    "E-10'un boş metniyle AYNI cümle kullanılmaz. Buradaki metin kullanıcıyı "
    "alttaki butona yönlendirir.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici() + sp(64)
        + div("col px20 mid-x",
              tally() + sp(24) + T("t-h2", "c-ink", "Kayıt yok") + sp(8)
              + '<span class="t-body c-ink2 mid">Aşağıdaki butonla ilkini ekle.</span>'))
    + div("col px20",
          div("btn-p", ic("plus", 24, "#FFFDF8") + wsp(8)
              + T("t-bodys", "c-page", "Harcama ekle"), "align-self:stretch"),
          "padding-top:12px;padding-bottom:12px")
    + tabbar("kayitlar")))

# ------------------------------------------------------------- E-14 bos ay + yukleniyor
bloklar.append(item(
    "E-14", "Kayıtlar · seçilen ayda kayıt yok",
    "Farklı boş durum, farklı metin, butonsuz — çözüm ay değiştiricide, "
    "sahte bir birincil eylem uydurulmadı.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici("Temmuz 2026", sol_basili=True) + sp(64)
        + div("col px20 mid-x",
              tally() + sp(24) + T("t-h2", "c-ink", "Bu ayda kayıt yok") + sp(8)
              + '<span class="t-body c-ink2 mid">Başka bir ay seçebilirsin.</span>'))
    + tabbar("kayitlar")))

bloklar.append(item(
    "E-14", "Kayıtlar · yükleniyor ve okuma hatası",
    "Üstte Skeleton (parıldama yok), altta ErrorState. 150ms'nin altındaki "
    "okumada hiçbir gösterge çizilmez.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici() + sp(16)
        + div("col px20",
              skeleton("112px", 18, 16) + skeleton("100%", 40, 12)
              + skeleton("100%", 40, 12) + skeleton("100%", 40, 24)
              + skeleton("96px", 18, 16) + skeleton("100%", 40, 12))
        + sp(24) + div("divider") + sp(24)
        + div("col px20 mid-x",
              T("t-h2", "c-ink", "Kayıtlar açılamadı") + sp(8)
              + '<span class="t-body c-ink2 mid">Veriler bu cihazda tutuluyor ve'
                ' şu an okunamadı.</span>'
              + sp(24) + btn_s("Yeniden dene", "default", "align-self:stretch")
              + sp(8) + btn_g("Ayrıntıyı gör", "default", "c-ink2", "align-self:center")))
    + tabbar("kayitlar")))

# ------------------------------------------------------------- E-14 uzun liste
uzun = ""
veri = [("Kafe", "Kart · 08.40", "95 ₺", "default", False),
        ("Ulaşım", "Kart · 09.05", "35 ₺", "default", False),
        ("Market", "Nakit · 13.20", "1.250.000 ₺", "default", False),
        ("Kira ve ev", "Kart · 14.00 · Akşam yemeği, iki kişi, arkadaşımla ödeme "
         "sonradan bölündü", "12.480 ₺", "default", False),
        ("Abonelik", "Kart · 15.30 · 12/12 taksit", "1.041 ₺", "default", True),
        ("Alışkanlıklar", "Nakit · 17.05", "180 ₺", "overflow", False),
        ("Sağlık", "Kart · 18.20", "640 ₺", "overflow", False)]
for i, (k, a, t, d, tk) in enumerate(veri):
    uzun += spendrow(k, a, t, d, tk)
    uzun += div("divider-56") if i < len(veri) - 1 else div("divider")

bloklar.append(item(
    "E-14", "Kayıtlar · uzun metin ve uzun tutar",
    "Tutar ASLA kırpılmaz, sütun genişler; kategori/not satırı tek satıra "
    "kırpılır. 200+ kayıtta FlatList kullanılır, hepsi birden render edilmez.",
    div("scroll",
        div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
        + sp(8) + ay_secici() + sp(8)
        + gun_basligi("10 Eylül Perşembe", "Günlük toplam 1.264.471 ₺") + uzun)
    + tabbar("kayitlar")))


# ------------------------------------------------------------- E-12 detay
def detay_sheet(ic_, arka=None):
    icerik = arka if arka else div("col",
                                   div("row between px20",
                                       T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
                                   + sp(8) + ay_secici() + sp(8)
                                   + gun_basligi("Bugün · 10 Eylül", "Günlük toplam 360 ₺")
                                   + BUGUN)
    return ('<div class="frame">' + chrome_top()
            + div("scroll", icerik + div("scrim", div("sheet", ic_)),
                  "position:relative")
            + chrome_bottom() + '</div>')


def det_satir(etiket, deger, renk="c-ink"):
    return div("row between px20",
               T("t-label", "c-ink2", etiket)
               + f'<span class="t-body {renk}">{deger}</span>',
               "min-height:44px")


bloklar.append(div("g-item", detay_sheet(
    sheet_bas("Harcama") + sp(16)
    + div("col px20", T("t-label", "c-ink2", "Tutar") + sp(8))
    + div("col px20", amountbox("180,00", "default"))
    + sp(16) + kat_alani(secili="Restoran")
    + sp(8) + odeme_satiri()
    + sp(8) + div("col px20", div("divider")) + sp(8)
    + det_satir("Eklenme", "10 Eylül · 19.50 eklendi", "c-ink2")
    + sp(12) + div("col px20", btn_p("Kaydet"))
    + sp(8)
    + div("row px20", div("btn-g", ic("trash", 24, "#8E2F20", 1.75, "Harcamayı sil")
                          + wsp(8) + T("t-bodys", "c-dan", "Sil"),
                          "align-self:stretch;flex:1 1 auto"))
    + sp(12))
    + div("g-cap", T("t-label", "c-acc", "E-12 · Harcama detayı")
          + sp(4) + T("t-caption", "c-ink2",
                      "Düzenleme ve silme aynı sheet'te. Sil ghost varyant "
                      "(Vişne metin) — ekranda tek birincil buton kuralı korunur."))))

bloklar.append(div("g-item", detay_sheet(
    sheet_bas("Harcama") + sp(16)
    + div("col px20", T("t-label", "c-ink2", "Tutar") + sp(8))
    + div("col px20", amountbox("1.041,67", "default"))
    + sp(8)
    + div("row px20",
          div("toast-strip", "", "height:40px;flex-shrink:0") + wsp(12)
          + '<span class="t-caption c-acc grow">3/12 taksit · her ay 1.041,67 ₺.'
            ' Düzenleme tüm taksit serisini etkiler.</span>', "min-height:48px")
    + sp(8) + kat_alani(secili="Abonelik")
    + sp(8) + det_satir("Eklenme", "9 Eylül · 10.00 eklendi", "c-ink2")
    + sp(12) + div("col px20", btn_p("Kaydet", "loading"))
    + sp(8)
    + div("row px20", div("btn-g btn-g-press",
                          ic("trash", 24, "#8E2F20", 1.75, "Harcamayı sil")
                          + wsp(8) + T("t-bodys", "c-dan", "Sil"),
                          "align-self:stretch;flex:1 1 auto"))
    + sp(12))
    + div("g-cap", T("t-label", "c-acc", "E-12 · taksitli kayıt · Kaydet loading · Sil basılı")
          + sp(4) + T("t-caption", "c-ink2",
                      "Taksit uyarısı Petrol şeritli bilgi kutusu — Kiremit değil, "
                      "çünkü bu bir limit durumu değil."))))

bloklar.append(div("g-item", detay_sheet(
    sheet_bas("Harcama") + sp(32)
    + div("col px20 mid-x",
          tally() + sp(24) + T("t-h2", "c-ink", "Kayıt bulunamadı") + sp(8)
          + '<span class="t-body c-ink2 mid">Bu kayıt silinmiş olabilir.'
            ' Listeyi yenilemeyi dene.</span>'
          + sp(24) + btn_s("Yeniden dene", "default", "align-self:stretch"))
    + sp(32))
    + div("g-cap", T("t-label", "c-acc", "E-12 · kayıt bulunamadı")
          + sp(4) + T("t-caption", "c-ink2",
                      "Sheet kapanıp kullanıcıyı şaşırtmaz; hata kendi "
                      "bağlamında gösterilir."))))


# ------------------------------------------------------------- E-13 dialog
def dialog_frame(ic_):
    icerik = div("col",
                 div("row between px20", T("t-h1", "c-ink", "Kayıtlar"), "min-height:44px")
                 + sp(8) + ay_secici() + sp(8)
                 + gun_basligi("Bugün · 10 Eylül", "Günlük toplam 360 ₺") + BUGUN)
    return ('<div class="frame">' + chrome_top()
            + div("scroll", icerik + div("scrim-mid", div("dialog", ic_)),
                  "position:relative")
            + chrome_bottom() + '</div>')


bloklar.append(div("g-item", dialog_frame(
    T("t-h2", "c-ink", "Bu harcama silinecek") + sp(8)
    + T("t-body", "c-ink2", "Geri alınamaz.") + sp(24)
    + div("btn-d", T("t-bodys", "c-page", "Sil"), "align-self:stretch") + sp(8)
    + div("btn-g", T("t-bodys", "c-ink2", "Vazgeç"), "align-self:stretch"))
    + div("g-cap", T("t-label", "c-acc", "E-13 · silme onayı")
          + sp(4) + T("t-caption", "c-ink2",
                      "Kırmızı (#8E2F20) ürünün TEK kırmızı yüzeyi burasıdır. "
                      "Eylemler dikey: üstte Sil, altında Vazgeç."))))

bloklar.append(div("g-item", dialog_frame(
    T("t-h2", "c-ink", "Bu harcama silinecek") + sp(8)
    + T("t-body", "c-ink2", "Kalan 9 taksit de silinecek. Geri alınamaz.") + sp(24)
    + div("btn-d", T("t-bodys", "c-page", "Siliniyor") + wsp(8) + div("spin-acc"),
          "align-self:stretch") + sp(8)
    + div("btn-g", T("t-bodys", "c-ink2", "Vazgeç"), "align-self:stretch"))
    + div("g-cap", T("t-label", "c-acc", "E-13 · taksitli kayıt · Sil loading")
          + sp(4) + T("t-caption", "c-ink2",
                      "Serinin tamamının gideceği ÖNCEDEN söylenir. Sonuç Toast'ı "
                      "Vişne şeritli ve 'Geri al' içerir."))))

bloklar.append(note("E-14 / E-12 / E-13 kararları", [
    "Kayıtlar ekranında hiç kart yok — defter metaforu kartla değil ayraçla kurulur.",
    "Gün başlığı Kağıt zeminde kalır; RN'de FlatList stickySectionHeadersEnabled ile yapışır (CSS sticky kullanılmadı).",
    "Limit dışı satır: zemin #F3E3DB, tutar #A24A2A. Ünlem, üstü çizili, kalın kırmızı çizgi yok.",
    "Kaydırma eylemleri iki yön: sağa Sil (yıkıcı, onay ister), sola Tekrarla (yapıcı, tek Toast).",
    "Silme onayı ürünün tek kırmızı yüzeyi; limit aşımı ASLA dialog ile bildirilmez.",
    "Uzun tutar sütunu genişletir, metin kırpılır — tersi değil.",
    "200+ kayıt kenar durumu ayrı kare olarak çizilmedi: liste sonsuz uzasa da görsel dil değişmez (aynı 64pt satır, aynı ayraç, aynı gün başlığı). Ölçek sorunu tasarımda değil uygulamada çözülür: SectionList + getItemLayout + windowSize, ay bazlı sayfalama, sayfa sonunda tek satır 'Daha eski kayıtlar' ghost butonu.",
    "Sonsuz kaydırma yok — kullanıcı ay değiştiriciyle gezer; böylece liste hiçbir zaman sınırsız büyümez.",
]))

page("E-14 · Kayıtlar + E-12 detay + E-13 silme",
     "Defter ritmi. 11 kare: dolu · kaydırma · boş · boş ay · yükleniyor + hata "
     "· uzun metin · detay (3 durum) · silme onayı (2 durum).",
     bloklar, "04-kayitlar.html")
