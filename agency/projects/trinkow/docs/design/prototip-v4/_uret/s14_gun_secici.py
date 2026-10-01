# -*- coding: utf-8 -*-
"""E-24 · Gün seçici (ay ızgarası) — arketip G (Grid / instrument).

Nereden gelir: E-10 Günlük başlığındaki takvim düğmesi. Görevi tek:
**herhangi bir güne atlamak.** Kaydırma komşu günler için hızlıdır
(**K-055:** geçmiş solda durur, geçmişe gitmek için parmak **sağa**
kaydırılır), ama "3 hafta önceki cumartesi" için kaydırma işkencedir;
ayrıca kaydırma ekran okuyucuyla güvenilir değil. Bu ekran o yolun
erişilebilir karşılığı.

Yön dili E-10 ile birebir aynıdır ve bu ekranda da **sol = geçmiş**:
ay okunda sol ok geriye (önceki ay), sağ ok bugüne doğru gider ve
bulunulan ay bugünün ayıysa sağ ok **pasiftir** — gelecek yok.

Referans uyarlaması (kalori uygulaması 02-takvim):
  ALINDI   → ay ızgarası · her günün durumu zeminde · ay ileri/geri ·
             ızgaranın altında üç istatistik · gün seçince gün ekranına dönüş
  ALINMADI → yeşil onay rozeti yerine kil zemin (rozet, ızgarada 30 kez
             tekrarlanınca gürültü olur) · "Başarını Paylaş" (Faz 1'de
             paylaşım yok) · "Kilo" istatistiğinin uydurma parasal karşılığı

Mood: alet paneli. Günlük ekranı tek büyük nesnedir; burası tam tersi —
otuz küçük eşit nesne. İki ekran aynı aileden ama aynı değil.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, push_basi, isk

OUT = pathlib.Path(__file__).parent.parent / "14-gun-secici.html"

GUN_ADI = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
KISA = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]

DURUM_SOZU = {
    "altinda": "limit altı",
    "disinda": "limit dışı",
    "yok": "kayıt yok",
    "pasif": "seçilemez",
}


def ay_gezinti(ay: str, alt: str, onceki_pasif: bool = False,
               sonraki_pasif: bool = False, sol_basili: bool = False) -> str:
    """Ay değiştirici. `lib.ay_secici`nin E-24 sürümü: burada okların
    **pasif** hâli var, çünkü K-049 iki uçta da sınır koyuyor (geleceğe ve
    ilk kayıt gününden öncesine gidilmez). Pasif ok gizlenmez: gizlenen ok
    düzeni kaydırır ve kullanıcı "ok nereye gitti" diye düşünür.
    """
    def ok(yon: str, pasif: bool, basili: bool = False) -> str:
        cls = "ikon-btn" + (" pasif" if pasif else "") + (" basili" if basili else "")
        ad = ("Önceki ay" if yon == "sol" else "Sonraki ay")
        if pasif:
            ad += " yok"
        ek = ' disabled aria-disabled="true"' if pasif else ""
        ikon = "chevron-left" if yon == "sol" else "chevron-right"
        return f'<button class="{cls}" aria-label="{ad}"{ek}>{icon(ikon)}</button>'

    return f'''          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="aralik">
                {ok("sol", onceki_pasif, sol_basili)}
                <div class="kolon orta">
                  <div class="t-strong">{ay}</div>
                  <div class="h4"></div>
                  <div class="t-cap">{alt}</div>
                </div>
                {ok("sag", sonraki_pasif)}
              </div>
            </div>
          </div>'''


# ------------------------------------------------------------------ hücre
def bos_hucre() -> str:
    """Ayın başındaki/sonundaki boş hücre. Dokunulur değil, etiketi yok."""
    return ('<div class="ay-hucre"><div style="width:44px;height:44px"></div>'
            '<div class="h4"></div><div class="gun-imza bos"></div></div>')


def hucre(gun: int, ay: str, hafta_gunu: int, durum: str,
          bugun: bool = False, basili: bool = False) -> str:
    """Tek gün kutusu.

    Durum ÜÇ yerden birden okunur: zemin rengi, derinlik (kayıt varsa
    kabarık, yoksa çukur) ve `accessibilityLabel`. Yalnız renge yüklenen bir
    ayrım renk körlüğünde kaybolur — bu yüzden etiket durumu kelimeyle söyler.

    **"Seçili" durumu yok.** K-040 halkayı kaldırdı, derinlik ise "kayıt
    var/yok" için harcandı; dördüncü bir görsel dil üretmek yerine açık gün
    ay başlığının alt satırında yazıyla söylenir.
    """
    cls = "gun-kutu"
    if durum in ("altinda", "disinda", "pasif"):
        cls += f" {durum}"
    if basili:
        cls += " basili"

    parcalar = [f"{gun} {ay} {GUN_ADI[hafta_gunu]}", DURUM_SOZU[durum]]
    if bugun:
        parcalar.append("bugün")
    etiket = ", ".join(parcalar)

    ek = ' disabled aria-disabled="true"' if durum == "pasif" else ""
    # "Bugün" işareti kutunun ALTINDA durur: zemin rengi durumu anlatmak için
    # zaten harcanmıştır, aynı yüzeye ikinci anlam yüklenmez.
    imza = "gun-imza"
    if not bugun:
        imza += " bos"
    elif durum == "altinda":
        imza += " ters"          # koyu mavi zemin üstünde beyaz nokta
    return (f'<div class="ay-hucre">'
            f'<button class="{cls}" aria-label="{etiket}"{ek}><div class="t-label">{gun}</div></button>'
            f'<div class="h4"></div><div class="{imza}"></div></div>')


def hafta_basliklari() -> str:
    hucreler = "".join(f'<div class="ay-hucre"><div class="t-micro">{k}</div></div>' for k in KISA)
    return f'<div class="ay-satir">{hucreler}</div>'


def izgara(satirlar: list[str]) -> str:
    ic = '\n              <div class="h8"></div>\n              '.join(satirlar)
    return ic


def gosterge() -> str:
    """Zemin renklerinin sözlüğü. Renk kodunu ekranda açıklamayan ızgara,
    kullanıcıya bilmece çözdürür."""
    def oge(sinif, metin):
        s = f" {sinif}" if sinif else ""
        return (f'<div class="satir" style="flex:0 0 auto">'
                f'<div class="imza-kare{s}"></div><div class="w8"></div>'
                f'<div class="t-micro">{metin}</div></div>')
    return f'''              <div class="satir">
                {oge("altinda", "limit altı")}
                <div class="w16"></div>
                {oge("disinda", "limit dışı")}
                <div class="w16"></div>
                {oge("", "kayıt yok")}
              </div>
              <div class="h8"></div>
              <div class="t-micro">Kutunun altındaki nokta bugünü gösterir.</div>'''


def ay_karti(satirlar: list[str]) -> str:
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              {hafta_basliklari()}
              <div class="h8"></div>
              {izgara(satirlar)}
              <div class="h16"></div>
{gosterge()}
            </div>
          </div>'''


def ozet_karti(baslik: str, satirlar: list[tuple[str, str]]) -> str:
    ic = []
    for i, (etiket, deger) in enumerate(satirlar):
        if i:
            ic.append('<div class="h12"></div>')
        ic.append(f'''<div class="aralik">
                <div class="esnek t-body">{etiket}</div>
                <div class="w12"></div>
                <div class="t-amount">{deger}</div>
              </div>''')
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="t-h2">{baslik}</div>
              <div class="h12"></div>
              {''.join(ic)}
            </div>
          </div>'''


def bugun_cipi(basili: bool = False) -> str:
    b = " basili" if basili else ""
    return (f'<button class="cip{b}" style="flex:0 0 auto" aria-label="Bugüne dön">'
            f'Bugün</button>')


# ---------------------------------------------------------------- A · Eylül
# 1 Eylül 2026 = Salı. Bugün 17 Eylül Perşembe (s01 ile aynı gün).
# Hikâye: 4 Eylül'de hiç kayıt yok, 5 Eylül limit dışı kapandı, 6 Eylül'den
# bugüne 12 gün üst üste limit altı → E-21'deki "Seri 12 gün" ile birebir aynı.
EYLUL = {d: "altinda" for d in list(range(1, 4)) + list(range(6, 18))}
EYLUL[4] = "yok"
EYLUL[5] = "disinda"
for d in range(18, 31):
    EYLUL[d] = "pasif"


def eylul_satirlari(basili_gun: int | None = None) -> list[str]:
    satirlar = []
    # ilk satır: Pazartesi boş, ay Salı'dan başlıyor
    ilk = [bos_hucre()] + [
        hucre(d, "Eylül", i + 1, EYLUL[d], bugun=(d == 17),
              basili=(d == basili_gun))
        for i, d in enumerate(range(1, 7))]
    satirlar.append(f'<div class="ay-satir">{"".join(ilk)}</div>')
    for bas in (7, 14, 21, 28):
        h = []
        for i in range(7):
            d = bas + i
            if d > 30:
                h.append(bos_hucre())
            else:
                h.append(hucre(d, "Eylül", i, EYLUL[d], bugun=(d == 17),
                               basili=(d == basili_gun)))
        satirlar.append(f'<div class="ay-satir">{"".join(h)}</div>')
    return satirlar


A = f'''{push_basi("Gün seç")}
{ay_gezinti("Eylül 2026", "16 gün kayıtlı", sonraki_pasif=True)}
          <div class="h16"></div>
{ay_karti(eylul_satirlari())}
          <div class="h24"></div>
{ozet_karti("Eylül özeti", [("Kayıt yazılan gün", "16 / 17"),
                            ("Limit altı gün", "15 / 17"),
                            ("Limit altı günlerde biriken", "1.240 ₺")])}
          <div class="h24"></div>'''

# ----------------------------------------------- A2 · gün kutusuna basılıyor
A2 = f'''{push_basi("Gün seç")}
{ay_gezinti("Eylül 2026", "16 gün kayıtlı", sonraki_pasif=True)}
          <div class="h16"></div>
{ay_karti(eylul_satirlari(basili_gun=12))}
          <div class="h24"></div>
{ozet_karti("Eylül özeti", [("Kayıt yazılan gün", "16 / 17"),
                            ("Limit altı gün", "15 / 17"),
                            ("Limit altı günlerde biriken", "1.240 ₺")])}
          <div class="h24"></div>'''

# -------------------------------------------------------------- B · Ağustos
# 1 Ağustos 2026 = Cumartesi. İlk kayıt 28 Ağustos → 1-27 seçilemez.
AGUSTOS = {d: "pasif" for d in range(1, 28)}
AGUSTOS.update({28: "altinda", 29: "altinda", 30: "disinda", 31: "altinda"})


def agustos_satirlari() -> list[str]:
    satirlar = []
    ilk = [bos_hucre()] * 5 + [
        hucre(1, "Ağustos", 5, AGUSTOS[1]), hucre(2, "Ağustos", 6, AGUSTOS[2])]
    satirlar.append(f'<div class="ay-satir">{"".join(ilk)}</div>')
    for bas in (3, 10, 17, 24, 31):
        h = []
        for i in range(7):
            d = bas + i
            if d > 31:
                h.append(bos_hucre())
            else:
                h.append(hucre(d, "Ağustos", i, AGUSTOS[d]))
        satirlar.append(f'<div class="ay-satir">{"".join(h)}</div>')
    return satirlar


B = f'''{push_basi("Gün seç", sag=bugun_cipi())}
{ay_gezinti("Ağustos 2026", "Açık gün 30 Ağustos", onceki_pasif=True)}
          <div class="h16"></div>
          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek t-cap" style="color:var(--text)">Trinkow'a 28 Ağustos'ta başladın. Daha öncesi yok.</div>
            </div>
          </div>
          <div class="h16"></div>
{ay_karti(agustos_satirlari())}
          <div class="h24"></div>
{ozet_karti("Ağustos özeti", [("Kayıt yazılan gün", "4 / 4"),
                              ("Limit altı gün", "3 / 4"),
                              ("Limit altı günlerde biriken", "210 ₺")])}
          <div class="h24"></div>'''

# --------------------------------------------------------- C · boş ay (yeni)
BOS = {d: "yok" for d in range(1, 18)}
for d in range(18, 31):
    BOS[d] = "pasif"


def bos_satirlar() -> list[str]:
    satirlar = []
    ilk = [bos_hucre()] + [hucre(d, "Eylül", i + 1, BOS[d], bugun=(d == 17))
                           for i, d in enumerate(range(1, 7))]
    satirlar.append(f'<div class="ay-satir">{"".join(ilk)}</div>')
    for bas in (7, 14, 21, 28):
        h = []
        for i in range(7):
            d = bas + i
            h.append(bos_hucre() if d > 30 else
                     hucre(d, "Eylül", i, BOS[d], bugun=(d == 17)))
        satirlar.append(f'<div class="ay-satir">{"".join(h)}</div>')
    return satirlar


C = f'''{push_basi("Gün seç")}
{ay_gezinti("Eylül 2026", "kayıt yok", sonraki_pasif=True)}
          <div class="h16"></div>
{ay_karti(bos_satirlar())}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              <div class="t-h2">Bu ayda kayıt yok</div>
              <div class="h8"></div>
              <div class="t-body">Kayıt yazdığın günler burada işaretlenir. Bugünden başlayabilirsin.</div>
              <div class="h16"></div>
              <button class="btn-secondary" style="width:auto;align-self:flex-start;padding:0 24px">Bugüne dön</button>
            </div>
          </div>
          <div class="h24"></div>'''

# ----------------------------------------------------------- D · yükleniyor
def isk_satir() -> str:
    hucreler = "".join('<div class="ay-hucre">' + isk("44px", "44px", "16px") +
                       '<div class="h4"></div><div class="gun-imza bos"></div></div>'
                       for _ in range(7))
    return f'<div class="ay-satir">{hucreler}</div>'


D = f'''{push_basi("Gün seç")}
          <div class="pad">
            <div class="clay-kuyu" style="padding:16px">
              <div class="aralik">
                {isk("44px", "44px", "999px")}
                <div class="kolon orta">{isk("104px", "20px")}<div class="h4"></div>{isk("72px", "16px")}</div>
                {isk("44px", "44px", "999px")}
              </div>
            </div>
          </div>
          <div class="h16"></div>
          <div class="pad">
            <div class="clay kart-ic">
              {hafta_basliklari()}
              <div class="h8"></div>
              {izgara([isk_satir() for _ in range(5)])}
              <div class="h16"></div>
              {isk("208px", "16px")}
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic">
              {isk("128px", "24px")}
              <div class="h12"></div>
              <div class="aralik">{isk("152px", "16px")}{isk("56px", "20px")}</div>
              <div class="h12"></div>
              <div class="aralik">{isk("120px", "16px")}{isk("56px", "20px")}</div>
              <div class="h12"></div>
              <div class="aralik">{isk("176px", "16px")}{isk("72px", "20px")}</div>
            </div>
          </div>
          <div class="h24"></div>'''


units = "".join([
    device("GÜN SEÇİCİ", "Eylül · bugün seçili · sonraki ay yok", A, note=
           "<b>Mood karşıtlığı bilinçli:</b> E-10 tek büyük nesne, burası otuz küçük eşit nesne. "
           "Aynı kil dili, farklı cümle. <b>Durum zeminle kodlanır:</b> limit altı = birincil kil "
           "dolgu, limit dışı = amber yumuşak, kayıt yok = boş çukur, seçilemez = düz gri (gölge "
           "kaldırılır, çünkü bu dilde gölge \"basılabilir\" demek). <b>Bugün</b> kutunun altındaki "
           "noktadır — zemin rengi durumu anlatmak için zaten harcanmış; ızgarada \"seçili\" diye dördüncü bir dil üretilmedi (K-040 halka kararı). Sonraki ay yok: ok "
           "<code>disabled</code>, opaklıkla soldurulmuyor. Dokunma hedefi 44×44, hücre aralığı "
           "flex ile dağıtılır (<b>CSS grid yok</b>)."),
    device("GÜN SEÇİCİ", "gün kutusu basılı (12 Eylül)", A2, note=
           "<b>Basılı durum:</b> hover olmadığı için tek geri bildirim bu. Kutu içe çöker "
           "(<code>clay-pressed</code>), zemin <code>groove</code>'a döner. Dokunuş bırakılınca "
           "ekran <b>kapanır ve Günlük o güne gider</b> — ayrıca \"Seç\" butonu yoktur, iki adım "
           "bir adımdır."),
    device("GÜN SEÇİCİ", "başlangıç ayı · geriye sınır", B, note=
           "<b>K-049/K-055 sınırı görünür:</b> ilk kayıt 28 Ağustos, öncesi <code>disabled</code>. "
           "Yön dili E-10 ile aynı: <b>sol = geçmiş</b>, sağ = bugüne doğru; bugünün ayında sağ ok pasif. "
           "Neden gizlemedik: 1-27 Ağustos'u ızgaradan silmek ayı sakat gösterir; gri ama duran "
           "gün \"burada veri yok\" der. Şerit sebebi söylüyor, suçlayıcı değil. Sağ üstte "
           "<b>Bugün</b> çipi: başka bir aya gidildiğinde geri dönüş tek dokunuş."),
    device("GÜN SEÇİCİ", "boş · hiç kayıt yok", C, note=
           "<b>Boş durum:</b> \"veri yok\" demekle bitmiyor; ızgara yine çizilir (yapı öğretilir), "
           "altındaki kart ne yapılacağını söyler. <b>Özet kartı gizlenir</b> — sıfırlarla dolu "
           "üç satır göstermek sahte veri hissi verir."),
    device("GÜN SEÇİCİ", "yükleniyor · iskelet", D, note=
           "<b>Yükleniyor:</b> spinner/shimmer yok. Gerçek düzenin kutuları yerinde durur, içleri "
           "çukur bloklara döner; veri gelince sayfa zıplamaz. Hafta başlıkları iskelet değildir — "
           "onlar veriye bağlı değil, her zaman aynı."),
])

OUT.write_text(page(
    "Trinkow · Gün seçici — prototip v4",
    "E-24 · Gün seçici",
    "Arketip G — ay ızgarası · 390×844 · claymorphism · K-049 sınırları",
    units), encoding="utf-8")
print("yazıldı:", OUT)
