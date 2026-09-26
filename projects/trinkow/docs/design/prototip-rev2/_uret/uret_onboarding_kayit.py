# -*- coding: utf-8 -*-
"""Trinkow rev2 · Kurulum (onboarding, 4 adım) + E-16 Hesap oluştur.

Bu betik **yalnız HTML üretir**. Görsel otorite değişmedi:
  · renk / punto / boşluk / radius / gölge  -> projects/trinkow/docs/brand/tokens.md v4
  · sınıflar                                -> ../prototip-v4/stil.css + ../stil-rev2.css
  · ortak parçalar (cihaz çerçevesi, ikonlar, sosyal düğmeler)
                                            -> ../../prototip-v4/_uret/lib.py

Yeni CSS yalnız `stil-rev2.css` §3-§4'te: `Checkbox` (`.onay-*`) ve
`MoneyRow` kuyusu (`.para-kuyu`). Gerekçeleri rev2-onboarding-kayit.md'de.

Çalıştırma:  python3 _uret/uret_onboarding_kayit.py
Çıktı     :  ../onboarding-kayit.html
"""
from __future__ import annotations

import importlib.util
import pathlib

# prototip-v4/_uret/lib.py'yi DOSYA YOLUYLA yükle: bu dizinde de bir `lib.py`
# var (tasarruf-profil üreteci) — modül adı çakışmasın.
_V4_LIB = pathlib.Path(__file__).resolve().parents[2] / "prototip-v4" / "_uret" / "lib.py"
_spec = importlib.util.spec_from_file_location("v4lib", _V4_LIB)
lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lib)

ic = lib.icon


def dev(*a, sabit_ust: str = "", **kw) -> str:
    """`lib.device`ın rev2 sarmalayıcısı.

    **B2:** `sabit_ust` bloğu `.kaydir`ın DIŞINA, `.content`ın ilk çocuğu
    olarak yazılır. Gerekçe: kurulumun başlık çubuğu ve adım göstergesi
    kaydırma alanının içindeyken 2/4 formu kaydırılınca ekrandan çıkıyordu —
    ilerleme göstergesi kaydırmayla kaybolamaz. RN karşılığı: `<View>` +
    `<ScrollView>` **kardeş** (bir arada değil).
    """
    html = lib.device(*a, **kw)
    if sabit_ust:
        im = '          <div class="kaydir" data-od-id="scroll">'
        assert im in html
        html = html.replace(im, sabit_ust + "\n" + im, 1)
    return html


# ----------------------------------------------------------------- parçalar
def kurulum_basi(adim: int, geri: bool = True, geri_basili: bool = False) -> str:
    """Kurulum başlığı: SOLDA 44pt geri (görsel olarak zayıf ikincil eylem),
    ORTADA `micro` sayaç "n/4", SAĞDA 44pt denge kutusu.
    `h1` KULLANILMAZ — adım numarası artık ekranın başlığı değil.

    **Bu blok kaydırma alanının DIŞINDADIR** (`dev(..., sabit_ust=...)`):
    dört adımın ortak çerçevesi ekrana sabittir, içerik onun altında kayar.
    """
    sol = (f'<button class="ikon-btn{" basili" if geri_basili else ""}" '
           f'aria-label="Önceki adıma dön">{ic("chevron-left")}</button>'
           if geri else '<div style="width:44px;height:44px"></div>')
    dolu = "".join('<div class="adim-dolu"></div><div class="w8"></div>' for _ in range(adim))
    bos = "".join('<div class="adim-oluk"></div><div class="w8"></div>' for _ in range(4 - adim))
    return f'''          <div class="ekran-basi">
            {sol}
            <div class="t-micro">{adim}/4</div>
            <div style="width:44px;height:44px"></div>
          </div>
          <div class="pad satir" role="progressbar" aria-label="Kurulum ilerlemesi"
               aria-valuemin="1" aria-valuemax="4" aria-valuenow="{adim}" style="margin-right:-8px">
            {dolu}{bos}
          </div>'''


def baslik_blok(h1: str, govde: str) -> str:
    return f'''          <div class="pad kolon">
            <div class="t-h1">{h1}</div>
            <div class="h8"></div>
            <div class="t-body c-2">{govde}</div>
          </div>'''


def secim_kart(ikon: str, ad: str, alt: str, secili: bool = False, basili: bool = False) -> str:
    cls = "secim-kart" + (" secili" if secili else "") + (" basili" if basili else "")
    sec = ' aria-pressed="true"' if secili else ' aria-pressed="false"'
    return f'''<button class="{cls}"{sec} aria-label="{ad}, {alt}">
                <div class="secim-ikon">{ic(ikon)}</div>
                <div class="w16"></div>
                <div class="esnek kolon">
                  <div class="t-strong">{ad}</div>
                  <div class="h8"></div>
                  <div class="t-cap">{alt}</div>
                </div>
              </button>'''


def bolum_basi(ad: str, sag: str = "") -> str:
    """`SectionHeader` — kartsız tek satır. Sağ taraf `label`/`text-2`."""
    sag_html = f'<div class="t-label c-2 num">{sag}</div>' if sag else ""
    return f'''          <div class="pad aralik">
            <div class="t-h2">{ad}</div>
            {sag_html}
          </div>'''


def para_alani(etiket: str, deger: str = "", ph: str = "0", odakli: bool = False,
               hata: str = "", not_metni: str = "") -> str:
    """Tam genişlik para alanı (`MoneyField`): etiket ÜSTTE, kuyu 56.
    Rev kararı: sistem ondalık klavyesi — kil tuş takımı kullanılmaz."""
    cls = "giris" + (" hatali" if hata else (" odakli" if odakli else ""))
    ic_html = (f'<div class="esnek t-amount num">{deger}</div>' if deger
               else f'<div class="esnek t-body c-3">{ph}</div>')
    imlec = '<div class="imlec"></div><div class="w8"></div>' if odakli else ""
    hata_html = (f'\n            <div class="h8"></div>'
                 f'\n            <div class="t-cap c-danger">{hata}</div>' if hata else "")
    not_html = (f'\n            <div class="h8"></div>'
                f'\n            <div class="t-cap">{not_metni}</div>' if not_metni else "")
    return f'''            <div class="t-label c-2">{etiket}</div>
            <div class="h8"></div>
            <div class="{cls}" aria-label="{etiket}">
              {ic_html}{imlec}<div class="t-label c-2">₺</div>
            </div>{hata_html}{not_html}'''


def para_satir(etiket: str, deger: str = "", ph: str = "0", odakli: bool = False,
               hatali: bool = False, birim: str = "₺", hata: str = "") -> str:
    """Kompakt para satırı (`MoneyRow`, 56): etiket solda, kuyu sağda 144×44.
    Sabit gider gibi **aynı ailenin tekrarlayan** alanları için.

    **B5 · `birim`:** kuyunun son eki parametredir, gövdeye gömülü değil.
    `birim="₺"` para alanı (değer + 8 + `₺`), `birim=""` **adet** alanı
    (son ek yok — "2 ₺" yazılamaz). Kuyu genişliği iki durumda da **144**:
    aynı ailenin satırları hizada kalır.
    Hata metni satırın **hemen altında** 8 boşlukla; kuyu 56 kalır.
    """
    cls = "para-kuyu" + (" hatali" if (hatali or hata) else (" odakli" if odakli else ""))
    ic_html = (f'<div class="esnek t-amount num sag">{deger}</div>' if deger
               else f'<div class="esnek t-body c-3 sag">{ph}</div>')
    birim_html = (f'<div class="w8"></div><div class="t-label c-2">{birim}</div>'
                  if birim else "")
    hata_html = (f'\n              <div class="h8"></div>'
                 f'\n              <div class="t-cap c-danger">{hata}</div>' if hata else "")
    return f'''<div class="kolon">
                <div class="satir" style="height:56px">
                  <div class="esnek t-body tek-satir">{etiket}</div>
                  <div class="w12"></div>
                  <div class="{cls}" aria-label="{etiket}">
                    {ic_html}{birim_html}
                  </div>
                </div>{hata_html}
              </div>'''


def serit(ikon: str, ust: str, alt: str = "", tur: str = "info") -> str:
    alt_html = f'<div class="h4"></div><div class="t-cap">{alt}</div>' if alt else ""
    renk = {"info": "var(--primary-text)", "warn": "var(--warning-ink)"}[tur]
    return f'''          <div class="pad">
            <div class="serit serit-{tur}">
              <div class="ikon-kutu" style="color:{renk}">{ic(ikon)}</div>
              <div class="w12"></div>
              <div class="esnek kolon">
                <div class="t-cap" style="color:var(--text)">{ust}</div>
                {alt_html}
              </div>
            </div>
          </div>'''


def ozet_satir(ad: str, deger: str, sayi: bool = True) -> str:
    """`SummaryRow`. **Ö3:** `amount` rolü liste TUTARI ve gün sayısıdır;
    metin değer ("Birikim yapmak") `body-strong` yazılır — rolü genişletmek
    jeton değişikliği olurdu. **Ö6:** etiket iki satıra sarabilir
    (`tek-satir` yalnız değer tarafında yok); kırpma yok."""
    # Sayı değer KIRPILMAZ ve SARMAZ (`flex:0 0 auto`, tabular). Metin değer
    # sarabilir (`flex:0 1 auto` + sağa hizalı): 200% yazı boyutunda
    # "Paramı kontrol altına almak" iki satıra iner, taşmaz.
    cls = "t-amount num" if sayi else "t-strong sag"
    stil = "flex:0 0 auto" if sayi else "flex:0 1 auto"
    return f'''<div class="satir-ust">
                <div class="esnek t-body">{ad}</div>
                <div class="w12"></div>
                <div class="{cls}" style="{stil}">{deger}</div>
              </div>'''


def rutin_satir(kat: str, ad: str, alt: str, tutar: str, basili: bool = False) -> str:
    cls = "satir-kart" + (" basili" if basili else "")
    return f'''<button class="{cls}" style="width:100%;border:0;text-align:left"
                      aria-label="{ad}, {alt}, günlük {tutar}. Düzenle">
                {lib.kat_kab(kat)}
                <div class="w12"></div>
                <div class="esnek kolon">
                  <div class="t-body tek-satir">{ad}</div>
                  <div class="t-cap tek-satir">{alt}</div>
                </div>
                <div class="w12"></div>
                <div class="t-amount num" style="flex:0 0 auto">{tutar}</div>
                <div class="w12"></div>
                <div class="ikon-kutu" style="color:var(--text-2);flex:0 0 auto">{ic("pencil")}</div>
              </button>'''


def alt_blok(*satirlar: str) -> str:
    ic_html = '\n              <div class="h8"></div>\n              '.join(satirlar)
    return f'''          <div class="alt-sabit">
            <div class="pad kolon">
              {ic_html}
            </div>
          </div>
'''


def belge_satir(etiket: str, basili: bool = False) -> str:
    """**Ö4:** iki yasal belge, onay grubunun altında 44pt `button.ghost`
    **satırı** olarak açılır. Onay cümlesinin içine bağlantı gömülmüyor:
    `hitSlop` bir `Pressable` prop'udur, iç içe `<Text onPress>`'te yoktur →
    gömülü bağlantının dokunma hedefi 18pt'de kalırdı (44 altı).
    Ölçü/renk/punto tokens §7.1 `button.ghost`tan; yalnız hizalama sola."""
    b = " basili" if basili else ""
    # İkon YOK: `notebook-text` kilitli sette Kayıtlar sekmesinin ikonudur
    # (varliklar.md §1) — yasal belgeye takılsa iki anlam taşırdı. Yeni ikon
    # eklemek onay gerektirir. Satırın eylem olduğu 44pt yükseklik, sola
    # hizalı `body-strong` ve `pressed` hâliyle anlaşılır (aynı dil:
    # "Oturum aç" ghost'u da ikonsuz).
    return (f'<button class="btn-ghost belge{b}" aria-label="{etiket} belgesini aç">'
            f'{etiket}</button>')


def onay_satir(metin: str, a11y: str, isaretli: bool = False, basili: bool = False,
               odakli: bool = False, hatali: bool = False, pasif: bool = False) -> str:
    """`Checkbox`. Etiket **bağlantısız düz metin** (Ö4): satırın tamamı
    tek işi yapar — kutuyu çevirir. Belgeler ayrı ghost satırlarda."""
    kutu = "onay-kutu"
    if isaretli:
        kutu += " isaretli"
    if odakli:
        kutu += " odakli"
    if hatali:
        kutu += " hatali"
    if pasif:
        kutu += " pasif"
    glif = ic("check") if isaretli else ""
    return f'''<div class="onay-satir{" basili" if basili else ""}" role="checkbox"
                   aria-checked="{"true" if isaretli else "false"}"
                   aria-label="{a11y}">
                <div class="{kutu}">{glif}</div>
                <div class="w12"></div>
                <div class="esnek t-cap" style="color:var(--text)">{metin}</div>
              </div>'''


# -------------------------------------------------------------- 1/4 · niyet
NIYET = {
    "takip": ("gauge", "Paramı kontrol altına almak", "Günün nereye gittiğini net göreceksin."),
    "tasarruf": ("landmark", "Birikim yapmak", "Her ay kenara bir pay ayıracaksın."),
    "borc": ("trending-down", "Borcumu bitirmek", "Kalan borcu adım adım eriteceksin."),
}


def adim1(secili: str = "", basili: str = "") -> str:
    """**B3:** varsayılan `secili` artık **boş** — her kullanıcının gördüğü
    ilk hâl "hiçbir kart seçili değil"dir."""
    kartlar = [secim_kart(i, ad, alt, secili=(k == secili), basili=(k == basili))
               for k, (i, ad, alt) in NIYET.items()]
    return ('          <div class="h24"></div>\n'
            + baslik_blok("Hadi başlayalım",
                          "Neyi hedefliyorsun? Günlük harcama limitini buna göre kuruyoruz.")
            + '\n          <div class="h24"></div>\n'
            + '          <div class="pad kolon">\n              '
            + '\n              <div class="h8"></div>\n              '.join(kartlar)
            + '\n          </div>\n          <div class="h24"></div>')


# ------------------------------------------------------ 2/4 · gelir ve gider
GIDER = [("Kira ya da aidat", "9.500"), ("Sabit faturalar", "2.400"),
         ("Zorunlu ulaşım", "1.800"), ("Kredi ve taksitler", "3.200")]

HEDEF_ETIKET = {
    "tasarruf": "Aylık hedef birikim",
    "borc": "Aylık hedef borç kapatma",
    "takip": "Aylık kenara ayırmak istediğin tutar",
}

# Ö6 · ÖZET satırının kısa karşılığı. Form etiketi uzun olabilir (alanın
# üstünde tam genişlik durur); özet satırında değerin yanında ~244pt yer
# vardır. Kırpmak yerine **kısa karşılık** yazılır — anlam korunur.
HEDEF_OZET = {
    "tasarruf": "Aylık hedef birikim",
    "borc": "Aylık hedef borç kapatma",
    "takip": "Aylık kenara ayırdığın",
}


def adim2(niyet: str = "tasarruf", gelir: str = "32.000", gelir_hata: str = "",
          gider_dolu: bool = True, hedef: str = "4.000", borc: str = "",
          odak: str = "") -> str:
    giderler = [para_satir(ad, tutar if gider_dolu else "", odakli=(odak == f"gider{i}"))
                for i, (ad, tutar) in enumerate(GIDER)]
    toplam = "16.900 ₺" if gider_dolu else "0 ₺"
    # Hedef ve borç alanları TAM GENİŞLİK: etiketleri uzun ("Aylık hedef borç
    # kapatma") ve niyete göre değişiyor — 144'lük kuyunun yanında kırpılırdı.
    hedef_alani = para_alani(HEDEF_ETIKET[niyet], hedef, odakli=(odak == "hedef"),
                             not_metni="Zorunlu değil. Sonra Profil'den değiştirebilirsin.")
    borc_alani = para_alani("Kalan toplam borç", borc, odakli=(odak == "borc"),
                            not_metni="Borcun yoksa boş bırakabilirsin.")
    return ('          <div class="h24"></div>\n'
            + baslik_blok("Gelir ve gider",
                          "Gelirini ve giderlerini inceleyip sana en uygun planı kuruyoruz. "
                          "Hedefine en kısa yoldan ulaşırsın.")
            + '\n          <div class="h24"></div>\n'
            + bolum_basi("Gelirin")
            + f'''\n          <div class="h8"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
{para_alani("Aylık net gelir", gelir, odakli=(odak == "gelir"), hata=gelir_hata,
            not_metni="Eline geçen tutar, kesintiden sonrası.")}
            </div>
          </div>
          <div class="h24"></div>
'''
            + bolum_basi("Sabit giderlerin", toplam)
            + f'''\n          <div class="h8"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {'<div class="h8"></div>'.join(giderler)}
            </div>
          </div>
          <div class="h24"></div>
'''
            + bolum_basi("Hedefin")
            + f'''\n          <div class="h8"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
{hedef_alani}
              <div class="h12"></div>
{borc_alani}
            </div>
          </div>
          <div class="h24"></div>''')


# --------------------------------------------------------- 3/4 · rutinler
def adim3(rutinler: bool = True, hata: bool = False, basili_satir: int = -1) -> str:
    if rutinler:
        satirlar = [
            rutin_satir("Kafe", "Sabah kahvesi", "Her gün 2 × 45 ₺", "90 ₺",
                        basili=(basili_satir == 0)),
            rutin_satir("Alışkanlıklar", "Marlboro Touch Blue 20'lik", "Her gün 1 × 95 ₺", "95 ₺",
                        basili=(basili_satir == 1)),
            rutin_satir("Ulaşım", "Servis yerine metro", "Her gün 2 × 27,50 ₺", "55 ₺",
                        basili=(basili_satir == 2)),
        ]
        liste = (bolum_basi("Eklediklerin", "Günlük 240 ₺")
                 + '\n          <div class="h8"></div>\n'
                 + '          <div class="pad kolon">\n              '
                 + '\n              <div class="h8"></div>\n              '.join(satirlar)
                 + '\n          </div>')
    else:
        liste = '''          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="t-cap">Eklediğin rutinler burada sıralanır.</div>
            </div>
          </div>'''
    hata_html = (serit("wifi-off", "Rutinler kaydedilemedi.",
                       "Yazdıkların duruyor, yeniden deneyebilirsin.", tur="warn")
                 + '\n          <div class="h24"></div>\n') if hata else ""
    return ('          <div class="h24"></div>\n'
            + baslik_blok("Günlük rutinlerin",
                          "Kahve, sigara, ulaşım gibi her gün tekrar edenler. "
                          "Ekledikçe planın gerçeğe yaklaşır.")
            + '\n          <div class="h24"></div>\n'
            + hata_html
            + liste
            + '''\n          <div class="h12"></div>
          <div class="pad"><button class="btn-secondary">Rutin ekle</button></div>
          <div class="h24"></div>\n'''
            + serit("info", "Rutinleri sonra Profil → Rutinlerim'den değiştirebilirsin.")
            + '\n          <div class="h24"></div>')


# ------------------------------------------------- 3/4 · RoutineSheet (B4)
# §5.2'nin çizili karşılığı. Adıma ilk girişte kendiliğinden açılır (Rev
# kararı), bu yüzden 3/4'ün GERÇEK ilk hâli bu yüzeydir. Rutini olmayan
# kullanıcı scrim'e dokunmak zorunda kalmasın diye sheet'in içinde
# `ghost` "Rutin harcamam yok" çıkışı vardır (B4/b).
RUTIN_KAT = ["Kafe", "Ulaşım", "Market", "Fatura", "Abonelik", "Alışkanlıklar"]


def kat_cip(ad: str, secili: bool = False, basili: bool = False) -> str:
    """Kategori çipi (tokens §7.6): 40 yükseklik, radius 999, yatay iç
    boşluk 16, aralar 8. Seçili: `cat.*.soft` + `clay.sunken` + solda 8pt
    `cat.*.solid` nokta. **Halka yok, onay ikonu yok.**"""
    _, renk = lib.CATS[ad]
    ton = renk.replace("kat-", "cat-")
    if secili:
        return (f'<button class="cip secili" style="background-color:var(--{ton}-soft)" '
                f'aria-pressed="true" aria-label="{ad}">'
                f'<div class="nokta" style="background-color:var(--{ton})"></div>'
                f'<div class="w8"></div>{ad}</button>')
    b = " basili" if basili else ""
    return f'<button class="cip{b}" aria-pressed="false" aria-label="{ad}">{ad}</button>'


def cip_seridi(secili: str = "", basili: str = "") -> str:
    """Yatay kaydırılan çip şeridi (RN: `horizontal ScrollView`). Hazır
    rutin ÖNERİSİ değildir — yalnız kategori seçer; fiyat ve ad
    kullanıcınındır (K-050)."""
    ciplar = [kat_cip(k, secili=(k == secili), basili=(k == basili)) for k in RUTIN_KAT]
    ciplar.append('<button class="cip" aria-label="Tüm kategorileri aç">Tüm kategoriler</button>')
    return ('<div class="yatay-kaydir">'
            + '<div class="w8"></div>'.join(ciplar) + '</div>')


def ayna_kuyu(tutar: str, formul: str) -> str:
    """`MirrorWell` — v4 E-25'teki ayna kuyusuyla **aynı** geometri:
    `well` + `clay.sunken`, radius 16, iç boşluk 12/16, üst satır
    `body-strong` + `amount`, altında 4 boşlukla `caption` formül.
    Yalnız iki alan da doluyken çizilir; boşken yer tutmaz."""
    return f'''<div class="clay-kuyu kolon" style="padding:12px 16px">
                  <div class="aralik">
                    <div class="t-strong">Ayda</div>
                    <div class="t-amount num">{tutar}</div>
                  </div>
                  <div class="h4"></div>
                  <div class="t-cap">{formul}</div>
                </div>'''


def rutin_sheet(ad: str = "", kat: str = "", adet: str = "", fiyat: str = "",
                ad_odakli: bool = False, fiyat_hata: str = "",
                ayna: tuple = (), duzenle: bool = False) -> str:
    """`RoutineSheet` — üç bölge: **tutamak** (sabit) · **form** (kayan) ·
    **alt blok** (sabit birincil + ghost). Klavye açıldığında sheet'e kalan
    yükseklik ~475pt'ye iner, formun doğal yüksekliği 513pt'dir → orta
    bölge kaydırır, birincil düğme görünür kalır (tokens §12/11c).
    Üst köşeler 32 · zemin `bg` · `clay.raised-lg` · scrim
    `rgba(28,57,142,0.38)` · tutamak 44×4, üstten 16, altında 12.
    """
    ad_ic = (f'<div class="esnek t-body tek-satir">{ad}</div>' if ad
             else '<div class="esnek t-body c-3 tek-satir">Sabah kahvesi</div>')
    imlec = '<div class="imlec"></div>' if ad_odakli else ""
    ayna_html = ('\n                <div class="h16"></div>\n                '
                 + ayna_kuyu(*ayna)) if ayna else ""
    tam = bool(ad and adet and fiyat)
    if tam:
        birincil = ('<button class="btn-primary">'
                    + ("Değişikliği kaydet" if duzenle else "Rutini ekle") + '</button>')
    else:
        birincil = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
                    + ("Değişikliği kaydet" if duzenle else "Rutini ekle") + '</button>')
    alt_ghost = ('<button class="btn-ghost" style="width:100%">Rutini kaldır</button>'
                 if duzenle else
                 '<button class="btn-ghost" style="width:100%">Rutin harcamam yok</button>')
    return f'''          <div class="katman-ust">
            <div class="scrim-kat"></div>
            <div class="sheet sheet-bolgeli">
              <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
              <div class="h12"></div>
              <div class="sheet-form">
                <div class="t-h2">{"Rutini düzenle" if duzenle else "Rutin ekle"}</div>
                <div class="h16"></div>
                <div class="t-label c-2">Ne?</div>
                <div class="h8"></div>
                <div class="giris{" odakli" if ad_odakli else ""}" aria-label="Ne?">
                  {ad_ic}{imlec}
                </div>
                <div class="h16"></div>
                <div class="t-label c-2">Kategori</div>
                <div class="h8"></div>
                {cip_seridi(secili=kat)}
                <div class="h16"></div>
                {para_satir("Günlük adet", adet, birim="")}
                <div class="h8"></div>
                {para_satir("Birim fiyat", fiyat, hata=fiyat_hata)}{ayna_html}
              </div>
              <div class="h16"></div>
              {birincil}
              <div class="h8"></div>
              {alt_ghost}
            </div>
          </div>
'''


# ------------------------------------------------------ 4/4 · plan özeti
def adim4(limit: str = "370", iskelet: bool = False, uzun: bool = False,
          niyet: str = "tasarruf") -> str:
    """4/4 plan özeti.

    **Ö1 · günlük limit formülü (tek satır, §6):**
    `gunluk_limit = (gelir − sabit_giderler − aylık_hedef) ÷ 30`, tam liraya
    aşağı. Rutinler **düşülmez**: rutin harcaması günlük limitin *içinden*
    yapılır, iki kez düşmek limiti çift aşındırır. Özet satırındaki günlük
    rutin toplamı bu yüzden bilgi satırıdır ve kartın altındaki iki cümle
    bunu ekranda **yazılı** söyler (K-050: gizli katsayı yok).
      · 32.000 − 16.900 − 4.000 = 11.100 ÷ 30 = **370**
      · 1.250.000 − 16.900 − 4.000 = 1.229.100 ÷ 30 = **40.970**
    """
    aciklama = {
        "tasarruf": "Bu limitin altında kaldığın her gün birikimin büyür.",
        "borc": "Bu limitin altında kaldığın her gün borcun küçülür.",
        "takip": "Bu limitin altında kaldığın her gün planın tutar.",
    }[niyet]
    if iskelet:
        hero_ic = '''<div class="t-label c-2">Günlük harcama limitin</div>
              <div class="h8"></div>
              <div class="satir">
                <div class="iskelet" style="width:132px;height:32px"></div>
                <div class="w12"></div>
                <div class="t-body c-2">Hesaplanıyor</div>
              </div>'''
    elif uzun:
        # Ö2 · `₺` sayıyla AYNI renkte (tokens §2.3). `c-2` tutar GİRİŞİ
        # ekranının ipucu dilidir; özet panelinde simgeyi soluklaştırmak
        # sayıyı ikiye böler.
        hero_ic = f'''<div class="t-label c-2">Günlük harcama limitin</div>
              <div class="h8"></div>
              <div class="satir" style="align-items:baseline">
                <div class="t-display num">{limit}</div>
                <div class="w8"></div>
                <div class="t-amount">₺</div>
              </div>'''
    else:
        hero_ic = f'''<div class="t-label c-2">Günlük harcama limitin</div>
              <div class="h8"></div>
              <div class="satir" style="align-items:baseline">
                <div class="t-hero num">{limit}</div>
                <div class="w8"></div>
                <div class="t-hero-simge">₺</div>
              </div>'''
    satirlar = [
        ozet_satir("Amacın", NIYET[niyet][1], sayi=False),
        ozet_satir("Aylık gelirin", "1.250.000 ₺" if uzun else "32.000 ₺"),
        ozet_satir("Sabit giderlerin", "16.900 ₺"),
        ozet_satir(HEDEF_OZET[niyet], "4.000 ₺"),
        ozet_satir("Günlük rutinlerin", "240 ₺"),
    ]
    return ('          <div class="h24"></div>\n'
            + baslik_blok("Planın hazır", aciklama)
            + f'''\n          <div class="h24"></div>
          <div class="pad">
            <div class="hero-kart kart-ic kolon" style="align-items:flex-start">
              {hero_ic}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {'<div class="h8"></div>'.join(satirlar)}
            </div>
          </div>
          <div class="h8"></div>
          <div class="pad kolon">
            <div class="t-cap">Gelirinden sabit giderlerini ve hedefini çıkarıp 30 güne bölüyoruz.</div>
            <div class="h4"></div>
            <div class="t-cap">Rutinlerin bu limitin içinden harcanır.</div>
          </div>
          <div class="h24"></div>
'''
            + serit("info", "Limitini Profil → Bütçe ve rutinler'den her zaman değiştirebilirsin.")
            + '\n          <div class="h24"></div>')


# ------------------------------------------------------------ E-16 · kayıt
def kayit(dolu: bool = False, onay1: bool = False, onay2: bool = False,
          tekrar_hata: str = "", ag_hatasi: bool = False, mesgul: bool = False,
          onay_basili: bool = False, onay_odakli: bool = False,
          onay_hatasi: bool = False, apple_basili: bool = False):
    """E-16 Hesap oluştur.

    **B1 — sosyal düğmeler ETKİN kalır.** Pasifleştirme kaldırıldı:
    sağlayıcının marka kılavuzu düğmenin görünümünü kilitler ve tokens
    §7.1'de `button.social.disabled` diye bir durum yoktur. Onaylar
    işaretsizken sosyal düğmeye dokunulursa iki `Checkbox` `error` hâline
    geçer ve grubun altında `hata.onay_gerekli` satırı görünür
    (`onay_hatasi=True`). **Birincil düğme** onaylar işaretlenmeden
    pasif kalmaya devam eder — iki yolun kapısı aynı, geri bildirimi farklı.

    **Ö4 — yasal belgeler.** Onay cümlesi bağlantısız düz metindir; iki
    belge onay grubunun altında 44pt `button.ghost` satırı olarak açılır.
    """
    ag = (serit("wifi-off", "Hesap açmak için bağlantı gerekir.",
                "Yazdıkların duruyor.", tur="warn")
          + '\n          <div class="h24"></div>\n') if ag_hatasi else ""
    eposta = lib.metin_alani("E-posta", deger="ayse.kaya@example.com" if dolu else "",
                             placeholder="ornek@eposta.com")
    sifre = lib.metin_alani(
        "Şifre", deger="•••••••••" if dolu else "", placeholder="Şifre belirle",
        sag_html=lib.goz_btn(), a11y="Şifre",
        alt_html=('\n              <div class="h8"></div>'
                  '\n              <div class="satir">'
                  f'\n                <div class="ikon-kutu" style="color:var(--success-ink)">{ic("check")}</div>'
                  '\n                <div class="w8"></div>'
                  '\n                <div class="t-cap">Uzunluk yeterli.</div>'
                  '\n              </div>' if dolu else
                  '\n              <div class="h8"></div>'
                  '\n              <div class="t-cap">En az 8 karakter.</div>'))
    tekrar = lib.metin_alani(
        "Şifre tekrar", deger="•••••••" if (dolu or tekrar_hata) else "",
        placeholder="Şifreyi yeniden yaz", sag_html=lib.goz_btn(), a11y="Şifre tekrar",
        hata=tekrar_hata)
    if onay_hatasi:
        alt_satir = ('\n              <div class="h8"></div>'
                     '\n              <div class="t-cap c-danger">Devam etmek için iki onay da gerekiyor.</div>')
    elif onay1 and onay2:
        alt_satir = ""
    else:
        alt_satir = ('\n              <div class="h8"></div>'
                     '\n              <div class="t-cap">İki onayı da işaretleyince hesabını oluşturabilirsin.</div>')
    onaylar = f'''          <div class="pad kolon">
              {onay_satir("Kullanım şartlarını okudum, kabul ediyorum.",
                          "Kullanım şartlarını kabul et", isaretli=onay1,
                          basili=onay_basili, odakli=onay_odakli, hatali=onay_hatasi)}
              <div class="h8"></div>
              {onay_satir("Gizlilik politikasını okudum, kabul ediyorum.",
                          "Gizlilik politikasını kabul et", isaretli=onay2,
                          hatali=onay_hatasi)}{alt_satir}
              <div class="h12"></div>
              {belge_satir("Kullanım şartları")}
              <div class="h8"></div>
              {belge_satir("Gizlilik politikası")}
          </div>'''
    pasif = not (onay1 and onay2 and dolu) or bool(tekrar_hata)
    if mesgul:
        birincil = ('<button class="btn-primary" aria-busy="true">Hesap oluşturuluyor'
                    '<div class="w8"></div><div class="spinner"></div></button>')
    elif pasif:
        birincil = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
                    'Hesap oluştur</button>')
    else:
        birincil = '<button class="btn-primary">Hesap oluştur</button>'
    govde = (lib.push_basi("Hesap oluştur")
             + '\n          <div class="h24"></div>\n'
             + ag
             + eposta
             + '\n          <div class="h12"></div>\n'
             + sifre
             + '\n          <div class="h12"></div>\n'
             + tekrar
             + '\n          <div class="h24"></div>\n'
             + onaylar
             + '\n          <div class="h12"></div>\n'
             + lib.ayirac()
             + '\n          <div class="h12"></div>\n'
             + lib.sosyal_kume(apple_basili=apple_basili)
             + '''\n          <div class="h24"></div>
          <div class="pad aralik">
            <div class="t-cap">Hesabın var mı</div>
            <button class="btn-ghost" style="padding:0 16px">Oturum aç</button>
          </div>
          <div class="h24"></div>''')
    return govde, alt_blok(birincil)


# ------------------------------------------------------------------ sahne
def main() -> None:
    birimler = []
    devam = '<button class="btn-primary">Devam</button>'
    devam_pasif = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
                   'Devam</button>')
    rutin_alt = alt_blok('<button class="btn-primary">Plan özetine geç</button>',
                         '<button class="btn-ghost" style="width:100%">Rutin harcamam yok</button>')

    # ------------------------------------------------------------ 1/4 niyet
    birimler.append(dev(
        "KURULUM 1/4", "niyet · gerçek ilk hâl · hiçbir kart seçili değil",
        adim1(),
        sabit_ust=kurulum_basi(1, geri=False),
        note="<b>Her kullanıcının gördüğü ilk ekran budur.</b> Varsayılan niyet "
             "kaldırıldı (kodda <code>useState('tasarruf')</code> ile bir seçenek "
             "seçili geliyordu): kimse karar vermeden ilerlemiyor. Üç kart da kabarık, "
             "<code>Devam</code> pasif ve <b>gerekçesi düğmenin üstünde</b> 8 boşlukla "
             "yazılı — pasif düğme sessiz kalmıyor. Başlık çubuğu ve dört oluk "
             "<b>kaydırma alanının dışında</b>, ekrana sabit.",
        sabit_alt=alt_blok('<div class="t-cap">Birini seçince devam edebilirsin.</div>',
                           devam_pasif)))

    birimler.append(dev(
        "KURULUM 1/4", "niyet · Birikim seçili · üçüncü kart basılı",
        adim1("tasarruf", basili="borc"),
        sabit_ust=kurulum_basi(1, geri=False),
        note="<b>Mood:</b> tek karar, ferah. Seçili kart <b>çukura iner</b>, ikon kabı "
             "<b>tersine kabarır</b>; halka ve onay ikonu yok (tokens §5.4). Üçüncü kart "
             "basılı hâlde: parmak altında zemin <code>groove</code>, gölge "
             "<code>clay.pressed</code>. Seçim yapıldığı an ipucu satırı düşer ve "
             "<code>Devam</code> etkinleşir.",
        sabit_alt=alt_blok(devam)))

    # --------------------------------------------------- 2/4 gelir ve gider
    birimler.append(dev(
        "KURULUM 2/4", "gelir ve gider · dolu · niyet: birikim",
        adim2("tasarruf", odak="gider1"),
        sabit_ust=kurulum_basi(2),
        note="Hedef alanının etiketi <b>1. adımdaki niyete göre</b> değişir: burada "
             "\"Aylık hedef birikim\". Sabit giderler kompakt <b>MoneyRow</b> satırları, "
             "toplam bölüm başlığının sağında. Bu ekran kaydırır; <b>adım göstergesi "
             "kaydırmaz</b> — çubuk ve sayaç yukarıda yerinde durur.",
        sabit_alt=alt_blok(devam)))

    birimler.append(dev(
        "KURULUM 2/4", "niyet: borç · gelir boş · alan hatası · Devam pasif",
        adim2("borc", gelir="", gelir_hata="Planı kurmak için gelirini yazman gerekiyor.",
              gider_dolu=False, hedef="", borc="185.000"),
        sabit_ust=kurulum_basi(2),
        note="Aynı alan, niyet <b>borç</b> olduğunda \"Aylık hedef borç kapatma\" olur. "
             "Gelir boşken birincil eylem pasif: zemin <code>disabled-bg</code>, metin "
             "<code>text-2</code>, gölge <code>clay.sunken</code> — <b>opaklık kullanılmadı</b>. "
             "Gider toplamı gizlenmedi, dürüstçe <b>0 ₺</b> yazıyor.",
        sabit_alt=alt_blok(devam_pasif)))

    birimler.append(dev(
        "KURULUM 2/4", "uzun tutar · niyet: takip · birincil eylem meşgul",
        adim2("takip", gelir="1.250.000", hedef="120.000", borc=""),
        sabit_ust=kurulum_basi(2, geri_basili=True),
        note="Uzun tutar denemesi: <code>1.250.000</code> 17pt <code>amount</code> "
             "rolünde kuyuya sığar, satır kaymaz. <code>takip</code> niyetinin uzun "
             "etiketi (\"Aylık kenara ayırmak istediğin tutar\") <b>tam genişlik</b> "
             "alanda durduğu için kırpılmaz. Geri düğmesi basılı hâlde; meşgul düğmenin "
             "genişliği sabit, tekrar dokunulamaz.",
        sabit_alt=alt_blok('<button class="btn-primary" aria-busy="true">Plan kuruluyor'
                           '<div class="w8"></div><div class="spinner"></div></button>')))

    # -------------------------------------------------------- 3/4 rutinler
    birimler.append(dev(
        "KURULUM 3/4 · SHEET", "adıma ilk giriş · sheet kendiliğinden açık · boş",
        adim3(False),
        sabit_ust=kurulum_basi(3),
        note="<b>3/4'ün gerçek ilk hâli.</b> Adıma girince <code>RoutineSheet</code> "
             "kendiliğinden açılır (Rev kararı). Rutini olmayan kullanıcı scrim'e "
             "dokunmak zorunda değil: sheet'in içinde tam genişlik <b>ghost \"Rutin "
             "harcamam yok\"</b> çıkışı var — form bir duvar değil. Üç bölge: tutamak "
             "(44×4, üstten 16), kayan form, sabit alt blok. \"Rutini ekle\" pasif, "
             "çünkü ad ve fiyat henüz boş.",
        sabit_alt=rutin_sheet()))

    birimler.append(dev(
        "KURULUM 3/4 · SHEET", "klavye açık · \"Ne?\" odaklı · form kayar",
        adim3(False),
        sabit_ust=kurulum_basi(3),
        klavye=True,
        note="Formun doğal yüksekliği <b>513pt</b>. Gerçek cihazda iOS TR klavyesi "
             "(~291pt) sheet'e <b>~475pt</b> bırakır → <b>orta bölge kaydırır</b>, "
             "birincil düğme ve ghost çıkış görünür kalır. Buradaki klavye bölge [A] "
             "temsilidir (224pt), o yüzden kaydırma tetiklenmiyor: yüzey <b>yapıyı</b> "
             "gösterir. Kategori çipleri yatay şeritte (RN: yatay "
             "<code>ScrollView</code>); hazır rutin önerisi değil, yalnız kategori — "
             "adı ve fiyatı uygulama uydurmaz (K-050).",
        sabit_alt=rutin_sheet(ad_odakli=True)))

    birimler.append(dev(
        "KURULUM 3/4 · SHEET", "dolu · ayna kuyusu · Rutini ekle etkin",
        adim3(True),
        sabit_ust=kurulum_basi(3),
        note="İki alan da dolduğu an <b>ayna kuyusu</b> belirir: \"Ayda 2.700 ₺\" + "
             "hesabın kendisi. Kullanıcı çarpmayı kafasında yapmıyor, uygulama da "
             "gizlemiyor. <b>Günlük adet</b> kuyusunda <code>₺</code> <b>yok</b> — aynı "
             "bileşenin <code>birim</code> parametresi boş (144 genişlik değişmez); "
             "para satırında <code>₺</code> var.",
        sabit_alt=rutin_sheet(ad="Sabah kahvesi", kat="Kafe", adet="2", fiyat="45",
                              ayna=("2.700 ₺", "Her gün 2 × 45 ₺ × 30 gün"))))

    birimler.append(dev(
        "KURULUM 3/4 · SHEET", "düzenleme kipi · birim fiyat silinmiş · alan hatası",
        adim3(True, basili_satir=0),
        sabit_ust=kurulum_basi(3),
        note="Satıra dokunmak sheet'i <b>düzenleme kipinde</b> açar: başlık \"Rutini "
             "düzenle\", alt çıkış <b>\"Rutini kaldır\"</b> — yıkıcı hedef listede "
             "değil, burada. Fiyat silinip kaydedilmek istenince kuyu 2pt "
             "<code>danger</code> kenarlık alır ve hata metni <b>satırın hemen altında</b> "
             "durur; satır yüksekliği (56) bozulmaz, ayna kuyusu düşer.",
        sabit_alt=rutin_sheet(ad="Sabah kahvesi", kat="Kafe", adet="2", fiyat="",
                              fiyat_hata="Rutini kaydetmek için birim fiyat gerekiyor.",
                              duzenle=True)))

    birimler.append(dev(
        "KURULUM 3/4", "rutinler · üç kayıt · ikinci satır basılı",
        adim3(True, basili_satir=1),
        sabit_ust=kurulum_basi(3),
        note="Uzun ürün adı (<code>Marlboro Touch Blue 20'lik</code>) kırpılır, "
             "<b>tutar kırpılmaz</b>. Satırın tamamı dokunma hedefi: dokununca sheet "
             "düzenleme kipinde açılır. Sheet kapatıldıktan sonra görünen ekran budur.",
        sabit_alt=rutin_alt))

    birimler.append(dev(
        "KURULUM 3/4", "boş durum · sheet kapatıldı · hiç rutin yok",
        adim3(False),
        sabit_ust=kurulum_basi(3),
        note="Boş durum: çukur tek satır. \"Henüz veri yok\" yazılmadı, kutlama da "
             "yapılmadı; rutin olmaması <b>geçerli bir durum</b>. Bu yüzden "
             "<code>EmptyGauge</code> çizilmedi — beklenen bir veri yok.",
        sabit_alt=rutin_alt))

    birimler.append(dev(
        "KURULUM 3/4", "yazma hatası · girdiler korunur",
        adim3(True, hata=True),
        sabit_ust=kurulum_basi(3),
        note="Hata şeridi <b>amber</b> ailesindedir, kırmızı değil: kayıp yok, yeniden "
             "denenebilir bir durum. Kırmızı yalnız geri alınamaz işlemlere ve form "
             "alanı hatasına ayrılmıştır.",
        sabit_alt=alt_blok('<button class="btn-primary">Yeniden dene</button>',
                           '<button class="btn-ghost" style="width:100%">Rutin harcamam yok</button>')))

    # ------------------------------------------------------ 4/4 plan özeti
    birimler.append(dev(
        "KURULUM 4/4", "plan özeti · günlük limit hazır",
        adim4("370"),
        sabit_ust=kurulum_basi(4),
        note="Ekranda <b>tek</b> 56pt sayı; <code>₺</code> 32pt ve <b>sayıyla aynı "
             "renkte</b> (tokens §2.3). Hesap ekranda yazılı: "
             "<b>32.000 − 16.900 − 4.000 = 11.100 ÷ 30 = 370</b>. Rutinler limitten "
             "düşülmez, limitin <b>içinden</b> harcanır — kartın altındaki iki cümle "
             "bunu söylüyor. Kutlama sessiz: konfeti, rozet, puan yok (K-048).",
        sabit_alt=alt_blok('<button class="btn-primary">Trinkow’u kullanmaya başla</button>')))

    birimler.append(dev(
        "KURULUM 4/4", "limit hesaplanıyor · iskelet · niyet: borç",
        adim4(iskelet=True, niyet="borc"),
        sabit_ust=kurulum_basi(4),
        note="≥150ms okuma: sayının yerinde <b>çukur blok</b> + \"Hesaplanıyor\" durur. "
             "Parıldama ve tam ekran spinner yok; düzen kaymaz. Birincil eylem bu sürede "
             "pasif. Açıklama cümlesi niyete göre değişir: burada \"borcun küçülür\".",
        sabit_alt=alt_blok('<button class="btn-primary pasif" disabled aria-disabled="true">'
                           'Trinkow’u kullanmaya başla</button>')))

    birimler.append(dev(
        "KURULUM 4/4", "uzun tutar · niyet: takip · uzun etiket",
        adim4("40.970", uzun=True, niyet="takip"),
        sabit_ust=kurulum_basi(4),
        note="6+ karakterli limit <code>hero</code> 56 → <code>display</code> 32'ye iner "
             "(tokens §7.5), <code>₺</code> da bir basamak iner ama rengi değişmez. "
             "<b>1.250.000 − 16.900 − 4.000 = 1.229.100 ÷ 30 = 40.970.</b> "
             "<code>takip</code> niyetinin uzun hedef etiketi özet satırında kısa "
             "karşılığıyla durur (\"Aylık kenara ayırdığın\") — kırpma yok.",
        sabit_alt=alt_blok('<button class="btn-primary">Trinkow’u kullanmaya başla</button>')))

    # ---------------------------------------------------- E-16 hesap oluştur
    govde, alt = kayit(dolu=False)
    birimler.append(dev(
        "E-16 HESAP OLUŞTUR", "boş form · onaylar işaretsiz · birincil pasif",
        govde, note="Mahremiyet şeridi ve pasif yasal cümle <b>kaldırıldı</b>. Yerine iki "
                    "ayrı onay kutusu geldi; kutu boşken <b>çukur</b> (kuyu), işaretliyken "
                    "<b>kabarık düz <code>primary-deep</code></b> + beyaz onay glifi. Onay "
                    "cümleleri <b>bağlantı taşımaz</b>: iki belge grubun altında 44pt ghost "
                    "satırı olarak açılır — gömülü bağlantının dokunma hedefi 18pt'de "
                    "kalırdı. <b>Sosyal düğmeler etkin</b>, pasif değil.",
        sabit_alt=alt))

    govde, alt = kayit(onay_hatasi=True, apple_basili=True)
    birimler.append(dev(
        "E-16 HESAP OLUŞTUR", "onaysız sosyal dokunuş · iki kutu hata hâlinde",
        govde, note="<b>Sosyal düğmeler pasif değildir</b> (sağlayıcı marka kılavuzu + "
                    "tokens §7.1'de <code>social.disabled</code> yok). Onaylar işaretsizken "
                    "Apple'a dokunulunca akış durur ve <b>eksik olan şey işaretlenir</b>: "
                    "iki kutu 2pt <code>danger</code> halkaya geçer, grubun altındaki ipucu "
                    "satırı yerini hata cümlesine bırakır (<code>danger-ink</code>, "
                    "<code>accessibilityLiveRegion=\"polite\"</code>). Birincil düğme zaten "
                    "pasif; iki yol aynı kapıdan geçer.",
        sabit_alt=alt))

    govde, alt = kayit(dolu=True, onay1=True, onay2=True)
    birimler.append(dev(
        "E-16 HESAP OLUŞTUR", "dolu · iki onay işaretli · birincil etkin",
        govde, note="Şifre kuralı karşılandığında satır <code>check</code> + "
                    "\"Uzunluk yeterli.\" olur — renkli güç çubuğu yok (K-050). İki onay "
                    "işaretlenince ipucu satırı düşer ve birincil düğme etkinleşir; belge "
                    "satırları yerinde kalır, çünkü belgeler her an okunabilir olmalı.",
        sabit_alt=alt))

    govde, alt = kayit(dolu=True, onay1=True, tekrar_hata="İki şifre aynı değil. Yeniden yaz.",
                       ag_hatasi=True, onay_basili=True)
    birimler.append(dev(
        "E-16 HESAP OLUŞTUR", "şifre tekrar eşleşmiyor · ağ hatası · onay basılı",
        govde, note="İki hata bir arada: alan hatası alanın <b>altında</b> (2pt "
                    "<code>danger</code> + <code>danger-ink</code> satır), bağlantı hatası "
                    "formun <b>üstünde</b> şerit olarak. Birinci onay kutusu basılı hâlde: "
                    "işaretsiz kutu parmak altında <code>groove</code> + "
                    "<code>clay.pressed</code>.",
        sabit_alt=alt))

    govde, alt = kayit(dolu=True, onay1=True, onay2=True, mesgul=True)
    birimler.append(dev(
        "E-16 HESAP OLUŞTUR", "meşgul · Hesap oluşturuluyor",
        govde, note="Yazma işleminde geri bildirim <b>düğmenin içindedir</b>: metin "
                    "\"Hesap oluşturuluyor\", sağında 20pt spinner, genişlik sabit, düğme "
                    "pasif. Sosyal düğmelerin görünümü değişmez (sağlayıcı kilidi), dokunuşları "
                    "bu sürede yok sayılır — çakışan iki kayıt isteği önlenir.",
        sabit_alt=alt))

    html = f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Trinkow rev2 · Kurulum (4 adım) + Hesap oluştur — prototip</title>
<link rel="stylesheet" href="../prototip-v4/stil.css" />
<link rel="stylesheet" href="stil-rev2.css" />
</head>
<body>
  <div class="sayfa-basligi">
    <h1>rev2 · Kurulum 1-4 + E-16 Hesap oluştur</h1>
    <p>Delta spesifikasyonu: <a href="../rev2-onboarding-kayit.md">rev2-onboarding-kayit.md</a>
       · 390×844 · claymorphism v4 · stil kaynağı
       <a href="../prototip-v4/index.html">prototip-v4</a> + <code>stil-rev2.css</code></p>
  </div>
  <div class="sahne">
{"".join(birimler)}  </div>
</body>
</html>
'''
    cikti = pathlib.Path(__file__).resolve().parents[1] / "onboarding-kayit.html"
    cikti.write_text(html, encoding="utf-8")
    print(f"yazıldı: {cikti} · {len(birimler)} yüzey")


if __name__ == "__main__":
    main()
