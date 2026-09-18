# -*- coding: utf-8 -*-
"""E-11 Harcama ekle — arketip E (Checkout / form).

Tek olcut: **3 dokunus.** (1) Ekle  (2) kategori  (3) Kaydet.
Tutar alani otomatik odakli acilir, klavye hazir gelir; alana dokunmak
gerekmez. Tarih/odeme/taksit varsayilanlari 0 ek dokunus.

Sekme cubugu DUSER — sheet acikken gezinme yok, tek is var.
"""
from lib import cat_colors, device_sheet, ico, page
from s01_bugun import icerik as pano

LIMIT = "300 ₺"

# --------------------------------------------------------------------------
# parcalar
# --------------------------------------------------------------------------


def tutar_alani(deger: str, durum: str = "focus", hata: str = "") -> str:
    """durum: focus | bos | hata | blur.  tokens 7.4 — yukseklik 54, radius 16,
    odakli kenarlik accent-deep 1.5pt (kalinlik degismez)."""
    cls = {"focus": " is-focused", "hata": " is-error", "bos": " is-focused", "blur": ""}[durum]
    renk = ' class="t-display c-3"' if durum == "bos" else ' class="t-display"'
    caret = '<span class="rn-caret"></span>' if durum in ("focus", "bos", "hata") else ""
    hata_html = ""
    if hata:
        hata_html = f'<p class="t-caption c-danger mt8">{hata}</p>'
    return f"""            <p class="t-label c-2 mt16">Tutar</p>
            <div class="rn-input amount{cls} mt8">
              <div class="rn-row g8">
                <span{renk}>{deger}</span>
                {caret}
              </div>
              <span class="t-display c-2">₺</span>
            </div>
{hata_html}"""


def kat_pill(ad: str, secili: bool = False, pressed: bool = False) -> str:
    solid, soft, _ = cat_colors(ad)
    if secili:
        stil = f' style="background:{soft}"'
        dot = f'<span class="dot" style="background:{solid}"></span>'
        cls = " is-selected"
    else:
        stil, dot, cls = "", "", ""
    if pressed:
        cls += " is-pressed"
    return (f'<button class="rn-pill{cls}" type="button"{stil} '
            f'aria-pressed="{"true" if secili else "false"}">{dot}{ad}</button>')


def meta_pill(metin: str, secili=False, ikon="", pressed=False, dot_renk="#D9661A") -> str:
    cls = " is-selected" if secili else ""
    if pressed:
        cls += " is-pressed"
    stil = ' style="background:#FDEBD8"' if secili else ""
    dot = f'<span class="dot" style="background:{dot_renk}"></span>' if secili else ""
    ik = ico(ikon, 20) if ikon else ""
    return f'<button class="rn-pill{cls}" type="button"{stil}>{dot}{metin}{ik}</button>'


def kategori_bolumu(secili: str = "", pressed: str = "") -> str:
    """Frekansa gore siralanmis ilk 6 kategori + tum kategoriler kapisi.
    Onceden secili GELMEZ (ekran-envanteri 4: bilincli olarak odenen 1 dokunus)."""
    ilk = ["Kafe", "Market", "Ulaşım", "Restoran"]
    ikinci = ["Fatura", "Kira ve ev"]
    r1 = "".join(kat_pill(a, a == secili, a == pressed) for a in ilk)
    r2 = "".join(kat_pill(a, a == secili, a == pressed) for a in ikinci)
    r2 += ('<button class="rn-pill" type="button">Tüm kategoriler'
           + ico("chevron-down", 20) + "</button>")
    return f"""            <p class="t-label c-2 mt24">Kategori</p>
            <div class="rn-row rn-wrap g8 mt8">{r1}</div>
            <div class="rn-row rn-wrap g8 mt8">{r2}</div>"""


def meta_bolumu(odeme: str = "Kart", taksitli: bool = False, not_acik: bool = False,
                tarih: str = "Bugün") -> str:
    """Odeme + tarih + taksit + not — tek saran satir, hepsi varsayilanli.
    Varsayilanlar dogruysa kullanici buraya hic dokunmaz (0 ek dokunus).
    RN: flexWrap 'wrap'; nakitte taksit pill'i hic uretilmez.
    Ikon yalniz "Bugün"de (chevron) — cunku tek acilir secici o. Digerleri
    dokununca yerinde degisiyor, ikon eklemek gurultu olurdu."""
    p = [
        meta_pill("Nakit", odeme == "Nakit"),
        meta_pill("Kart", odeme == "Kart"),
        meta_pill(tarih, ikon="chevron-down"),
    ]
    if odeme == "Kart":           # taksit yalniz kartta anlamli
        p.append(meta_pill("Taksitli", taksitli))
    p.append(meta_pill("Not", not_acik))
    # Etiket yok: her pill kendi guncel degerini yaziyor (Kart / Bugun),
    # bir grup basligina ihtiyaci yok. Ustundeki hairline, bu satirin
    # kategori bolumune ait olmadigini soyluyor.
    return f"""            <div class="rn-hairline mt16"></div>
            <div class="rn-row rn-wrap g8 mt16">{"".join(p)}</div>"""


def taksit_paneli(secili: int = 4, aylik: str = "1.250 ₺") -> str:
    """AYRI "Uygula" butonu YOK: sayiya dokunmak onizlemeyi aninda gunceller,
    onay zaten Kaydet'tir. Boylece taksitli yol +3 degil **+2 dokunus**
    (ekran-envanteri.md 4'teki butce bu yonde guncellenmeli — PM notu)."""
    pills = "".join(
        f'<button class="rn-pill{" is-selected" if n == secili else ""}" type="button"'
        f'{" style=\'background:#FDEBD8\'" if n == secili else ""}>'
        f'{"<span class=\'dot\' style=\'background:#D9661A\'></span>" if n == secili else ""}'
        f"{n}</button>"
        for n in (2, 3, 4, 6, 9, 12))
    return f"""            <div class="rn-card flat mt16" style="background:#EFEAE3;border-radius:16px;padding:16px">
              <p class="t-label c-2">Kaç taksit</p>
              <div class="rn-row rn-wrap g8 mt8">{pills}</div>
              <p class="t-strong mt12">Ayda {aylik} · {secili} ay</p>
              <p class="t-caption mt4">Taksitler girildiği güne değil, ait olduğu aya yazılır.</p>
            </div>"""


def not_alani(metin: str = "", placeholder: bool = False) -> str:
    govde = (f'<p class="t-body c-3">Kısa bir not</p>' if placeholder
             else f'<p class="t-body">{metin}</p>')
    return f"""            <p class="t-label c-2 mt24">Not (isteğe bağlı)</p>
            <div class="rn-textarea is-focused mt8" style="min-height:54px">{govde}</div>"""


def uyari(fark: str) -> str:
    """Limit disi UYARISI — kirmizi degil, mürdüm (edge). Kaydi engellemez.
    Sheet'in ALT bolumunde, Kaydet'in hemen ustunde durur: nitelediigi eylemin
    yanindadir ve gövde kaydirilsa bile gorunur kalir."""
    return f"""            <div class="rn-strip mb12" style="background:#F0E4EF">
              <span class="dot" style="background:#6E3B6B"></span>
              <p class="t-caption rn-fill" style="color:#17181C">Bu harcama günlük limitin {fark} üzerine çıkarır.</p>
            </div>"""


def kaydet(durum: str = "aktif") -> str:
    """durum: aktif | pressed | disabled | loading"""
    if durum == "loading":
        return ('<button class="rn-btn primary is-disabled" type="button" disabled '
                'style="background:#17181C;color:#FFFCF8">Kaydediliyor'
                '<span class="rn-spinner"></span></button>')
    cls = {"aktif": "", "pressed": " is-pressed", "disabled": " is-disabled"}[durum]
    dis = ' disabled aria-disabled="true"' if durum == "disabled" else ""
    return f'<button class="rn-btn primary{cls}" type="button"{dis}>Kaydet</button>'


def sheet(govde: str, alt: str) -> str:
    return f"""        <div class="rn-sheet">
          <div class="rn-sheet-head">
            <div class="rn-row rn-between">
              <h2 class="t-h2">Harcama ekle</h2>
              <button class="rn-iconbtn" type="button" aria-label="Kapat">{ico('x', 24)}</button>
            </div>
          </div>
          <div class="rn-sheet-body">
{govde}
          </div>
          <div class="rn-sheet-foot">
{alt}
          </div>
        </div>"""


# --------------------------------------------------------------------------
# varyantlar
# --------------------------------------------------------------------------
def d1():
    govde = (tutar_alani("0", "bos")
             + "\n" + kategori_bolumu()
             + "\n" + meta_bolumu())
    return device_sheet(
        pano("s2a"), sheet(govde, kaydet("disabled")),
        "1 · Açılış — dokunuş 1 bitti",
        "Tutar alanı otomatik odaklı, klavye hazır. Kullanıcı alana dokunmuyor.",
        warm=True,
        note="<b>Dokunuş bütçesi:</b> sheet açıldığı anda odak tutarda; sıradaki iş "
             "rakam yazmak. Kaydet <b>pasif</b> çünkü yazacak bir şey yok — "
             "kullanıcı boş kayıtla duvara toslamıyor, buton baştan söylüyor. "
             "Pasiflik <b>renkle</b> veriliyor, opaklıkla değil.",
    )


def d2():
    govde = (tutar_alani("45", "focus")
             + "\n" + kategori_bolumu(secili="Kafe")
             + "\n" + meta_bolumu())
    return device_sheet(
        pano("s2b"), sheet(govde, kaydet("pressed")),
        "2 · Üç dokunuş tamam",
        "45 yazıldı · Kafe seçildi (2) · Kaydet basılı (3). Kart ve Bugün varsayılan.",
        warm=True,
        note="<b>Basılı durum</b> tek geri bildirim: RN'de hover yok. Kaydet zemini "
             "<b>#2C2E34</b>'e geçiyor, ölçek animasyonu yok. Kategori seçimi renk + "
             "nokta + metin taşıyor; renk tek başına bilgi değil.",
    )


def d3():
    govde = (tutar_alani("200", "focus")
             + "\n" + kategori_bolumu(secili="Market")
             + "\n" + meta_bolumu(odeme="Nakit"))
    return device_sheet(
        pano("s2c"), sheet(govde, uyari("80 ₺") + kaydet("aktif")),
        "3 · Limit dışına çıkaracak",
        "Uyarı yazıyor, engellemiyor. Nakit seçili → Taksitli seçeneği hiç görünmüyor.",
        warm=True,
        note="<b>Kırmızı yok.</b> Limit dışı rengi <b>#6E3B6B</b> (mürdüm); kırmızı "
             "yalnız geri alınamaz işlemler için ayrıldı. Cümle ne olduğunu söylüyor, "
             "kullanıcıyı durdurmuyor: karar onun. Ünlem ve uyarı üçgeni yok.",
    )


def d4():
    govde = (tutar_alani("1.250.000,50", "blur")
             + "\n" + kategori_bolumu(secili="Kira ve ev")
             + "\n" + meta_bolumu(not_acik=True)
             + "\n" + not_alani("Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü"))
    return device_sheet(
        pano("s2d"), sheet(govde, kaydet("aktif")),
        "4 · Uzun tutar + uzun not",
        "1.250.000,50 ₺ ve 58 karakterlik not. Düzen kırılmıyor, kırpma yok.",
        warm=False, kb=False,
        note="<b>Taşma testi:</b> en uzun tutar 32pt tabular rakamla tam sığıyor, ₺ "
             "sağ uçta duruyor. Not <b>iki satıra sarıyor</b>, üç nokta ile kesilmiyor — "
             "kullanıcının yazdığı metni gizlemek dürüst değil. Sheet gövdesi bu "
             "hâlde kaydırılabilir; Kaydet kaydırmanın dışında, hep yerinde.",
    )


def d5():
    govde = (tutar_alani("5.000", "blur")
             + "\n" + kategori_bolumu(secili="Kira ve ev")
             + "\n" + meta_bolumu(taksitli=True)
             + "\n" + taksit_paneli(4, "1.250 ₺"))
    return device_sheet(
        pano("s2e"), sheet(govde, kaydet("aktif")),
        "5 · Taksitli (+2 dokunuş, seyrek yol)",
        "Taksitli → sayı. Onay yok, Kaydet zaten onay. Varsayılan akışın dışında.",
        warm=False, kb=False,
        note="<b>Maliyetli yol görünür ama yolun ortasında değil.</b> Taksit paneli "
             "yalnız istenince açılıyor; açılınca klavye kapanıyor ve yer açılıyor. "
             "Önizleme (“Ayda 1.250 ₺ · 4 ay”) kullanıcıya ne kaydedeceğini "
             "<b>kaydetmeden önce</b> gösteriyor; ayrı bir onay butonu gereksiz.",
    )


def d6():
    govde = (tutar_alani("45", "blur")
             + "\n" + kategori_bolumu(secili="Kafe")
             + "\n" + meta_bolumu())
    return device_sheet(
        pano("s2f"), sheet(govde, kaydet("loading")),
        "6 · Kaydediliyor",
        "Buton genişliği sabit, metin yerinde kalıyor, ikinci dokunuş kilitli.",
        warm=True, kb=False,
        note="<b>Yükleniyor</b> = butonun kendi durumu; ekranı kaplayan bir örtü yok. "
             "Genişlik sabit olduğu için düzen zıplamıyor. Bittiğinde sheet kapanır ve "
             "üstte toast çıkar: “45 ₺ kaydedildi”.",
    )


def d7():
    govde = (tutar_alani("0,00", "hata", hata="Tutar sıfırdan büyük olmalı.")
             + "\n" + kategori_bolumu(secili="Kafe")
             + "\n" + meta_bolumu())
    return device_sheet(
        pano("s2g"), sheet(govde, kaydet("disabled")),
        "7 · Hata — sıfır tutar",
        "Kenarlık danger, altında tek cümle. “Hata:”, büyük harf, ünlem yok.",
        warm=True,
        note="<b>Hata metni ne yapacağını söyler, ne olduğunu değil.</b> Kenarlık "
             "kalınlığı değişmiyor (1.5pt) — yalnız renk değişiyor, bu yüzden düzen "
             "oynamıyor. Hata rengi <b>#9B2C1F</b>; limit aşımında kullanılmıyor.",
    )


if __name__ == "__main__":
    page(
        "Trinkow · Harcama ekle",
        "E-11 · Harcama ekle",
        "Arketip E — checkout. Tek ölçüt: <b>3 dokunuş</b>. Sekme çubuğu düşer, "
        "Kaydet klavyenin üstünde kalır",
        "\n".join([d1(), d2(), d3(), d4(), d5(), d6(), d7()]),
        "02-harcama-ekle.html",
    )
