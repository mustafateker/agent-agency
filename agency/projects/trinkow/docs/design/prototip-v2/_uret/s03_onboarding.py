# -*- coding: utf-8 -*-
"""E-01 / E-02 / E-03 Kurulum — arketip C (Onboarding 1 of N).

Uc adim, ucu de tek soru. Sekme cubugu DUSER. Adim gostergesi hem segment
hem "Adim n/3" metni tasir (renk tek basina bilgi tasimaz).

Kisisellestirme: secilen niyet panodaki buyuk sayinin NE oldugunu degistirir
(bugun kalan / bu ay biriken / kalan borc). Bunu anlatmiyoruz, adim 1'de
secim yapilir yapilmaz kucuk bir onizlemede GOSTERIYORUZ.
"""
from lib import cat_colors, device, ico, keyboard, mini_gauge, page, steps

# niyet -> (baslik, alt satir, lucide ikonu, panodaki buyuk sayinin etiketi)
NIYET = {
    "takip":    ("Param nereye gidiyor", "Günlük harcamanı görmek istiyorsun.",
                 "route", "bugün kalan"),
    "tasarruf": ("Bütçe yaratmak", "Her ay bir miktar ayırmak istiyorsun.",
                 "piggy-bank", "bu ay biriken"),
    "borc":     ("Borç kapatmak", "Kalan borcu eritmek istiyorsun.",
                 "trending-down", "kalan borç"),
}


# --------------------------------------------------------------------------
# ortak parcalar
# --------------------------------------------------------------------------
def ust(adim: int, geri: bool = True) -> str:
    """Geri dugmesi yalnizca 1. adimdan sonra var. iOS'ta sol kenardan geri
    kaydirma da ayni isi yapar; buton onun gorunur karsiligi."""
    sol = (f'<button class="rn-iconbtn" type="button" aria-label="Geri dön">{ico("chevron-left", 24)}</button>'
           if geri else '<div style="width:44px;height:44px"></div>')
    return f"""        <div class="rn-pad rn-col">
          <div class="rn-row" style="margin-left:-12px">{sol}</div>
{steps(adim)}
        </div>"""


def soru(baslik: str, aciklama: str = "") -> str:
    ac = f'<p class="t-body c-2 mt8">{aciklama}</p>' if aciklama else ""
    return f"""          <h1 class="t-h1 mt32">{baslik}</h1>
{ac}"""


def onizleme(niyet: str, sayi: str = "", oran: float = 0.0) -> str:
    """Panonun kisisellesmesini GOSTEREN serit. Uydurma veri yazmiyoruz:
    sayi yoksa yalnizca etiket degisiyor, sayi varsa kullanicinin AZ ONCE
    girdigi gercek deger gosteriliyor.

    Yay oranı 0: kurulumda henuz hicbir sey harcanmadi/odenmedi. Ekran 1 ile
    ayni kural — yay TUKETILENI gosterir, ortadaki sayi KALANI."""
    _, _, _, etiket = NIYET[niyet]
    if sayi:
        govde = f"""              <div class="rn-col rn-fill">
                <p class="t-display">{sayi}</p>
                <p class="t-label c-2 mt4">{etiket}</p>
              </div>"""
    else:
        govde = f"""              <div class="rn-col rn-fill">
                <p class="t-label c-2">Panondaki büyük sayı</p>
                <p class="t-h2 mt4">{etiket}</p>
              </div>"""
    return f"""          <div class="rn-card flat mt24" style="background:#FDEBD8;border-radius:16px;padding:16px">
            <div class="rn-row g16">
              <div class="rn-mini-gauge">{mini_gauge(oran, "#D9661A")}</div>
{govde}
            </div>
          </div>"""


def secim(niyet: str, secili: bool = False, pressed: bool = False) -> str:
    baslik, alt, ikon, _ = NIYET[niyet]
    cls = " is-selected" if secili else (" is-pressed" if pressed else "")
    mark = f'<span class="mark">{ico("check", 24)}</span>' if secili else ""
    return f"""            <button class="rn-choice{cls}" type="button" aria-pressed="{"true" if secili else "false"}">
              <span class="ico">{ico(ikon, 24)}</span>
              <span class="rn-col rn-fill">
                <span class="t-strong">{baslik}</span>
                <span class="t-caption mt4">{alt}</span>
              </span>
              {mark}
            </button>"""


def tutar(deger: str, etiket: str, c3: bool = False, odak: bool = True) -> str:
    renk = ' class="t-display c-3"' if c3 else ' class="t-display"'
    return f"""          <p class="t-label c-2 mt32">{etiket}</p>
          <div class="rn-input amount mt8{' is-focused' if odak else ''}">
            <div class="rn-row g8">
              <span{renk}>{deger}</span>
              <span class="rn-caret"></span>
            </div>
            <span class="t-display c-2">₺</span>
          </div>"""


def oneri(secili: str = "") -> str:
    pills = ""
    for v in ("200 ₺", "350 ₺", "500 ₺"):
        on = v == secili
        st = ' style="background:#FDEBD8"' if on else ""
        dot = '<span class="dot" style="background:#D9661A"></span>' if on else ""
        pills += (f'<button class="rn-pill{" is-selected" if on else ""}" type="button"{st}>'
                  f"{dot}{v}</button>")
    return f"""          <p class="t-label c-2 mt24">Sık kullanılan</p>
          <div class="rn-row g8 mt8">{pills}</div>"""


def kat_pill(ad: str, secili: bool) -> str:
    solid, soft, _ = cat_colors(ad)
    st = f' style="background:{soft}"' if secili else ""
    dot = f'<span class="dot" style="background:{solid}"></span>' if secili else ""
    return (f'<button class="rn-pill{" is-selected" if secili else ""}" type="button"{st} '
            f'aria-pressed="{"true" if secili else "false"}">{dot}{ad}</button>')


def kategori_agi(secililer) -> str:
    """13 kategorinin tamami; gizli menu yok. Tek sarmalayan satir —
    RN: flexWrap 'wrap' + gap 8. Metin uzadiginda kirpilmaz, alt satira iner."""
    sira = ["Kafe", "Market", "Restoran", "Ulaşım", "Akaryakıt", "Fatura",
            "Kira ve ev", "Abonelik", "Sağlık", "Giyim", "Eğlence",
            "Alışkanlıklar", "Diğer"]
    pills = "".join(kat_pill(a, a in secililer) for a in sira)
    return f'          <div class="rn-row rn-wrap g8 mt16">{pills}</div>\n'


def alt_eylem(etiket: str, durum: str = "aktif", yardim: str = "") -> str:
    cls = {"aktif": "", "pressed": " is-pressed", "disabled": " is-disabled"}[durum]
    dis = ' disabled aria-disabled="true"' if durum == "disabled" else ""
    y = f'<p class="t-caption mt8" style="text-align:center">{yardim}</p>' if yardim else ""
    return f"""      <div class="rn-footer">
        <button class="rn-btn primary{cls}" type="button"{dis}>{etiket}</button>
{y}
      </div>"""


# --------------------------------------------------------------------------
# varyantlar
# --------------------------------------------------------------------------
def d1():
    icerik = f"""{ust(1, geri=False)}
        <div class="rn-pad rn-col">
{soru("Neden buradasın", "Sonra değiştirebilirsin.")}
          <div class="rn-col g12 mt24">
{secim("takip")}
{secim("tasarruf")}
{secim("borc")}
          </div>
        </div>
        <div style="height:24px"></div>"""
    return device(
        icerik, "1 · Adım 1/3 — hiçbir şey seçilmedi",
        "Tek soru, üç seçenek, tek birincil buton. Devam pasif.",
        tail=alt_eylem("Devam", "disabled"),
        note="<b>Daire ikon + başlık + tek cümle üçlüsü kurulmadı.</b> Seçenekler "
             "dikey liste; ikon satırın solunda 24pt, daire zemin yok. Üç seçenek "
             "eşit ağırlıkta — hiçbiri “önerilen” diye öne çıkarılmıyor, çünkü "
             "doğru cevabı biz bilmiyoruz.",
    )


def d2():
    icerik = f"""{ust(1, geri=False)}
        <div class="rn-pad rn-col">
{soru("Neden buradasın", "Sonra değiştirebilirsin.")}
          <div class="rn-col g12 mt24">
{secim("takip", secili=True)}
{secim("tasarruf")}
{secim("borc")}
          </div>
{onizleme("takip")}
        </div>
        <div style="height:24px"></div>"""
    return device(
        icerik, "2 · Seçim yapıldı — pano anında değişti",
        "Alttaki şerit, seçime göre panodaki büyük sayının ne olacağını gösteriyor.",
        tail=alt_eylem("Devam"),
        note="<b>Kişiselleşmeyi anlatmıyoruz, gösteriyoruz.</b> “Borç kapatmak” "
             "seçilseydi şeritte <b>kalan borç</b>, “Bütçe yaratmak” seçilseydi "
             "<b>bu ay biriken</b> yazacaktı. Şerit uydurma sayı göstermiyor — "
             "henüz veri yok, yalnız etiket değişiyor.",
    )


def d3():
    icerik = f"""{ust(2)}
        <div class="rn-pad rn-col">
{soru("Günde ne kadar harcamak istiyorsun", "Kesin olması gerekmiyor. Sonra düzeltiriz.")}
{tutar("0", "Günlük limit", c3=True)}
{oneri()}
        </div>
        <div style="height:16px"></div>"""
    return device(
        icerik, "3 · Adım 2/3 — boş, klavye açık",
        "Alan otomatik odaklı. Devam pasif; boş limitle ilerlenmiyor.",
        tail=alt_eylem("Devam", "disabled") + keyboard(),
        note="<b>Öneri çipleri tahmin değil kısayol.</b> 200/350/500 ₺ tek dokunuşla "
             "doldurur; kullanıcı kendi sayısını yazmak isterse klavye zaten açık. "
             "Hiçbir değer önceden seçili değil — yanlış bir limiti sessizce "
             "kabul ettirmiyoruz.",
    )


def d4():
    icerik = f"""{ust(2)}
        <div class="rn-pad rn-col">
{soru("Günde ne kadar harcamak istiyorsun", "Kesin olması gerekmiyor. Sonra düzeltiriz.")}
{tutar("350", "Günlük limit")}
          <p class="t-caption mt8">Ayda yaklaşık 10.500 ₺. Tahmini.</p>
{oneri("350 ₺")}
{onizleme("takip", "350 ₺", 0.0)}
        </div>
        <div style="height:16px"></div>"""
    return device(
        icerik, "4 · Adım 2/3 — 350 ₺ girildi",
        "Aylık karşılığı ve panonun günün başındaki hâli anında görünüyor.",
        tail=alt_eylem("Devam", "pressed"),
        note="<b>Önizlemedeki sayı gerçek:</b> gün başında harcama yok, kalan = limit, "
             "yay <b>boş</b>. Kullanıcı yarın sabah tam olarak bunu görecek. “Tahmini” "
             "kelimesi bilerek duruyor — 30 gün varsayımını sakladığımızda dürüst "
             "olmazdı.",
    )


def d5():
    icerik = f"""{ust(3)}
        <div class="rn-pad rn-col">
{soru("En çok neyi merak ediyorsun", "En fazla üç kategori seç.")}
{kategori_agi({"Kafe", "Market", "Restoran"})}
          <p class="t-caption mt16">Seçtiklerin panoda kategori limiti olarak görünür.</p>
        </div>
        <div style="height:24px"></div>"""
    return device(
        icerik, "5 · Adım 3/3 — Takip kipi",
        "Üçüncü soru kipe bağlı. Takip seçilince: merak edilen kategoriler.",
        tail=alt_eylem("Başla"),
        note="<b>Her kategori renk + ad taşıyor, renk tek başına bilgi değil.</b> "
             "Üç seçim panodaki üç mini göstergeye dönüşüyor — yani bu soru "
             "dekoratif değil, doğrudan bir ekranı kuruyor. 13 kategori de "
             "burada; gizli menü yok.",
    )


def d6():
    icerik = f"""{ust(3)}
        <div class="rn-pad rn-col">
{soru("Kalan borcun ne kadar", "Yaklaşık yazman yeterli.")}
{tutar("48.500", "Toplam kalan borç")}
{onizleme("borc", "48.500 ₺", 0.0)}
        </div>
        <div style="height:16px"></div>"""
    return device(
        icerik, "6 · Adım 3/3 — Borç kipi (aynı adım, başka soru)",
        "Adım 1'de “Borç kapatmak” seçilseydi üçüncü adım bu olurdu.",
        tail=alt_eylem("Başla") + keyboard(),
        note="<b>Üç kip üç ayrı üçüncü adım demek.</b> Aynı düzen, aynı ritim, "
             "başka soru — ekranlar birbirinin klonu değil ama aynı aileden. "
             "Borçta bile ton yargısız: “eritmek”, “kalan borç”; uyarı ikonu, "
             "kırmızı, ünlem yok.",
    )


if __name__ == "__main__":
    page(
        "Trinkow · Kurulum",
        "E-01 · E-02 · E-03 — Kurulum",
        "Arketip C — 1 of N. Üç adım, her adımda tek soru ve tek birincil buton. "
        "Niyet seçimi panoyu seçildiği anda kuruyor",
        "\n".join([d1(), d2(), d3(), d4(), d5(), d6()]),
        "03-onboarding.html",
    )
