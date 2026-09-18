# -*- coding: utf-8 -*-
"""E-23 · Hesap oluştur — E-22'nin kardeşi, kopyası değil.

**Neden "Kayıt ol" değil "Hesap oluştur":** `metinler.md` §0.1 kelime
dağarcığı "kayıt"ı **harcama kaydı** için kilitledi ("Bugünkü kayıtlar",
"214 kayıt"). "Kayıt ol" demek, ürünün en sık kullanılan sözcüğünü ikinci
bir anlama bağlardı. Ekran kodu E-23 "Kayıt" olarak kalır, arayüz metni
**Hesap oluştur** olur.

Mood: SÖZLEŞME MASASI. E-22 geri dönen kullanıcının kapısıdır, hızlıdır.
Burada kullanıcı **yeni bir karar** veriyor: ekranın alt yarısı bu yüzden
mahremiyet şeridi + yasal satır taşır ve mahremiyet cümlesi sessiz bir
`caption` değil, `primary-soft` zeminli bir **şerit** — karar noktasında
okunması gereken cümle odur.

Şifre kuralı geri bildirimi (brief): **karmaşıklık göstergesi klişesine
düşmeden.** Zayıf/orta/güçlü renkli çubuk yok, dört maddelik onay listesi
yok. Tek kural var (en az 8 karakter), o kural tek satırda yazılı ve
karşılandığında satır onay ikonuna dönüşür. Uydurma "güç" skoru üretmek,
K-050'nin yasakladığı sahte skor mantığının aynısı olurdu.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, icon, push_basi, sosyal_kume, ayirac,
                 metin_alani, goz_btn)

OUT = pathlib.Path(__file__).parent.parent / "16-kayit.html"

MAHREMIYET = "Harcamaların sende kalır. Hesap yalnız seni tanır."
EPOSTA = "ayse.kaya@example.com"


def kural_satiri(karsilandi=False):
    """Şifre kuralı. İki durum, tek kural, tek satır."""
    if not karsilandi:
        return ('\n              <div class="h8"></div>'
                '\n              <div class="t-cap">En az 8 karakter.</div>')
    return ('\n              <div class="h8"></div>'
            '\n              <div class="satir">'
            f'\n                <div class="ikon-kutu" style="color:var(--success-ink)">{icon("check")}</div>'
            '\n                <div class="w8"></div>'
            '\n                <div class="t-cap">Uzunluk yeterli.</div>'
            '\n              </div>')


def serit_mahremiyet():
    return f'''          <div class="pad">
            <div class="serit serit-info">
              <div class="ikon-kutu" style="color:var(--primary-text)">{icon("info")}</div>
              <div class="w12"></div>
              <div class="esnek t-cap" style="color:var(--text)">{MAHREMIYET} Yedekleme sonraki sürümlerde.</div>
            </div>
          </div>'''


def serit_baglanti():
    return f'''          <div class="pad">
            <div class="serit serit-warn">
              <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("wifi-off")}</div>
              <div class="w12"></div>
              <div class="esnek t-cap" style="color:var(--text)">Hesap açmak için bağlantı gerekir. Kayıtların bağlantısız çalışır.</div>
            </div>
          </div>'''


def yasal(sartlar_basili=False, gizlilik_basili=False):
    """Yasal satır. RN karşılığı: iç içe `Text` (`onPress` taşıyan iki
    `Text` çocuğu) — `accessibilityRole="link"` ve dikey
    `hitSlop={{top:12,bottom:12}}` ile dokunma hedefi 44'e tamamlanır;
    12pt satırı 44pt kutuya çevirmek cümleyi parçalardı.
    Belgelerin METNİ henüz yazılmadı (K-052 şartı) — bağlantı hedefleri
    yer tutucudur."""
    s = " basili-metin" if sartlar_basili else ""
    g = " basili-metin" if gizlilik_basili else ""
    return f'''          <div class="pad">
            <div class="t-micro">Hesap oluşturarak <span class="t-micro c-primary{s}">Kullanım şartları</span> ve <span class="t-micro c-primary{g}">Gizlilik politikasını</span> kabul ediyorsun.</div>
          </div>'''


def giris_satiri(basili=False):
    b = " basili" if basili else ""
    return f'''          <div class="pad aralik">
            <div class="t-cap">Hesabın var mı</div>
            <button class="btn-ghost{b}" style="padding:0 16px">Oturum aç</button>
          </div>'''


def alt_sabit(durum="pasif", hesapsiz_basili=False):
    hb = " basili" if hesapsiz_basili else ""
    if durum == "pasif":
        btn = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
               'Hesap oluştur</button>')
    elif durum == "loading":
        btn = ('<button class="btn-primary basili" disabled aria-disabled="true">'
               'Hesap oluşturuluyor<div class="w8"></div><div class="spinner"></div></button>')
    else:
        btn = '<button class="btn-primary">Hesap oluştur</button>'
    return f'''          <div class="alt-sabit">
            <div class="pad kolon">
              {btn}
              <div class="h8"></div>
              <button class="btn-ghost{hb}" style="width:100%">Hesapsız devam et</button>
            </div>
          </div>'''


def govde(eposta="", eposta_hata="", sifre="", sifre_odakli=False,
          sifre_gorunur=False, imlec=False, kural=False, serit="",
          kaydirilmis=False, giris_basili=False, apple_basili=False,
          google_basili=False, sartlar_basili=False, platform="ios"):
    s = [] if kaydirilmis else [push_basi("Hesap oluştur")]
    if serit:
        s += ['          <div class="h24"></div>', serit]
    s += [
        '' if kaydirilmis else '          <div class="h24"></div>',
        sosyal_kume(apple_basili=apple_basili, google_basili=google_basili,
                    platform=platform),
        '          <div class="h12"></div>',
        ayirac(),
        '          <div class="h12"></div>',
        metin_alani("E-posta", deger=eposta, placeholder="ornek@eposta.com",
                    hata=eposta_hata, a11y="E-posta adresi"),
        '          <div class="h12"></div>',
        metin_alani("Şifre", deger=sifre, placeholder="Şifre belirle",
                    odakli=sifre_odakli, imlec=imlec,
                    sag_html=goz_btn(sifre_gorunur),
                    alt_html=kural_satiri(kural), a11y="Şifre"),
        '          <div class="h24"></div>',
    ]
    if kaydirilmis:
        # Klavye açıkken kaydırma alanı 429px'e iner. Şifre alanının ALTINDAKİ
        # bloklar (mahremiyet şeridi, yasal satır, giriş satırı) ekranın
        # aşağısında kalır; buraya çizilse şerit ortasından dilimlenirdi
        # (tokens §12/11c). Görünen içerik 383px → kesme 24'lük boşlukta.
        return "\n".join(s)
    s += [
        serit_mahremiyet(),
        '          <div class="h24"></div>',
        yasal(sartlar_basili=sartlar_basili),
        '          <div class="h12"></div>',
        giris_satiri(basili=giris_basili),
        '          <div class="h24"></div>',
    ]
    return "\n".join(s)


# ------------------------------------------------------------------ A · boş
A = govde()

# ------------------------- B · yazılıyor · kural henüz karşılanmadı (klavye)
B = govde(eposta=EPOSTA, sifre="•••••", sifre_odakli=True, imlec=True,
          kaydirilmis=True)

# ------------------------ C · kural karşılandı · şifre görünür · Apple basılı
C = govde(eposta=EPOSTA, sifre="kirazli2026", sifre_gorunur=True, kural=True,
          apple_basili=True, sartlar_basili=True)

# ------------------------------------------------ D · e-posta zaten kayıtlı
D = govde(eposta=EPOSTA, eposta_hata="Bu e-posta ile hesap var. Oturum aç.",
          sifre="•••••••••••", kural=True, giris_basili=True)

# ---------------------------------------------------------- E · gönderiliyor
E = govde(eposta=EPOSTA, sifre="•••••••••••", kural=True)

# -------------------------------------------------------------- F · ağ hatası
F = govde(eposta=EPOSTA, sifre="•••••••••••", kural=True,
          serit=serit_baglanti())


# ------------------------------- G · Android derlemesi (yalnız Google)
G = govde(platform="android")


units = "".join([
    device("HESAP OLUŞTUR", "E-23 · boş · varsayılan", A, sabit_alt=alt_sabit(), note=
           "<b>Neden \"Hesap oluştur\", \"Kayıt ol\" değil:</b> <code>metinler.md</code> §0.1 \"kayıt\" "
           "sözcüğünü <b>harcama kaydı</b> için kilitledi (\"214 kayıt\", \"Bugünkü kayıtlar\"). "
           "\"Kayıt ol\" ürünün en sık kullanılan sözcüğünü ikinci bir anlama bağlardı. "
           "<b>Mood farkı (E-22'den):</b> orada mahremiyet cümlesi başlık altında sessiz bir "
           "<code>caption</code>; burada <b>şerit</b> — kullanıcı yeni bir karar veriyor, cümlenin "
           "okunması gerekiyor. Şerit ayrıca <b>söz vermediğimiz şeyi de söylüyor</b>: "
           "\"Yedekleme sonraki sürümlerde.\" (K-052: Faz 1'de harcama senkronu yok). "
           "<b>Yasal satır</b> 12pt <code>micro</code> (tokens §2.2 \"yasal metin\" rolü), iki bağlantı "
           "<code>primary-text</code> 5.12:1. Belge metinleri henüz yazılmadı — bağlantı hedefleri "
           "yer tutucu, bu delta'da PM'e bildirildi."),
    device("HESAP OLUŞTUR", "E-23 · yazılıyor · kural karşılanmadı · klavye açık", B,
           sabit_alt=alt_sabit(), klavye=True, note=
           "<b>Şifre kuralı geri bildirimi, klişeye düşmeden:</b> zayıf/orta/güçlü renkli çubuk YOK, "
           "dört maddelik onay listesi YOK. <b>Tek kural</b> var ve tek satırda yazılı: \"En az 8 karakter.\" "
           "Uydurma bir \"güç skoru\" üretmek, K-050'nin yasakladığı sahte skor mantığının aynısıdır; "
           "ayrıca ölçtüğü şey (entropi) kullanıcının anladığı şey değildir. "
           "<b>Birincil buton pasif kalır</b> çünkü kural henüz karşılanmadı — kullanıcı boşuna dokunup "
           "hata yemiyor. Ekran <b>kaydırılmış</b> çizildi: klavye açıkken kaydırma alanı 429px, "
           "kesme boşluk bandına düşüyor."),
    device("HESAP OLUŞTUR", "E-23 · kural karşılandı · şifre görünür · Apple basılı", C,
           sabit_alt=alt_sabit("aktif"), note=
           "<b>Kural karşılanınca satır onay ikonuna döner:</b> 20pt <code>check</code>, renk "
           "<code>success-ink</code> (zemin <code>bg</code> üzerinde 4.24:1 — grafik eşiği 3:1 ✅; "
           "<code>success #16A34A</code> bu zeminde 2.85 ile kalıyordu, o yüzden ham yeşil kullanılmadı). "
           "Metin <code>text-2</code> kalır: yeşil METİN yazmıyoruz, yeşil yalnız işarettir. "
           "<b>Apple düğmesi basılı (pressed):</b> siyah zemin 1A1A1A'ya açılır + <code>clay.pressed</code> — "
           "lacivert iç gölge siyah üzerinde görünmediği için geri bildirimi <b>zemin tonu</b> taşır. "
           "Bu, üçüncü taraf yüzeyinde kil dilinin sınırının bilinçli kabulüdür. "
           "<b>Yasal bağlantı basılı:</b> metin bağlantısının <code>pressed</code> hâli renk "
           "koyulaşmasıdır (<code>primary-press</code>) — 12pt bir satıra kil kabartma "
           "uygulanamaz, opaklık ise yasak (tokens §6)."),
    device("HESAP OLUŞTUR", "E-23 · e-posta zaten kayıtlı", D, sabit_alt=alt_sabit("aktif"), note=
           "<b>Tek yerde çelişki yok:</b> hata alan düzeyinde (\"Bu e-posta ile hesap var. Oturum aç.\") ve "
           "çözümü <b>iki satır aşağıda duruyor</b> — \"Hesabın var mı / Oturum aç\" satırı basılı "
           "gösterildi, yani kullanıcı hatadan çıkışa tek dokunuşla gidiyor. Kayıtlı e-postayı burada "
           "söylemek gizlilik sızıntısı değil: adresi zaten kullanıcının kendisi yazdı. "
           "(E-22'deki genel mesaj mantığı orada geçerli, çünkü orada saldırgan adres <b>deniyor</b>.)"),
    device("HESAP OLUŞTUR", "E-23 · gönderiliyor", E, sabit_alt=alt_sabit("loading"), note=
           "<b>Düğme meşgul:</b> \"Hesap oluşturuluyor\" + spinner, genişlik sabit, <code>disabled</code>. "
           "Metin butonu taşırmıyor: 56pt yükseklik, tek satır, kırpılma yok. Alanlar yerinde durur; "
           "iskelete çevrilmez, çünkü kullanıcının yazdığı veri kaybolmuş gibi görünmemeli."),
    device("HESAP OLUŞTUR", "E-23 · Android derlemesi · yalnız Google", G,
           sabit_alt=alt_sabit(), note=
           "<b>Aynı platform kuralı kayıt ekranında da geçerli:</b> Android'de Apple düğmesi çizilmez, "
           "küme tek düğmeye iner (Mustafa kararı). <b>Yasal satır ve mahremiyet şeridi değişmez</b> — "
           "onlar sağlayıcıya değil hesabın kendisine bağlı. Ekran 56pt kısaldığı için alt bloklar "
           "yukarı çıkar ve <b>kaydırma ihtiyacı kalmaz</b>: Android'de bu ekran tek ekrana sığar."),
    device("HESAP OLUŞTUR", "E-23 · ağ hatası", F, sabit_alt=alt_sabit("aktif"), note=
           "<b>Dürüst ağ hatası:</b> \"Hesap açmak için bağlantı gerekir. Kayıtların bağlantısız "
           "çalışır.\" Şerit en üstte, çünkü hem sağlayıcı düğmelerini hem formu etkiliyor — tek alana "
           "bağlanamaz. <b>Amber, kırmızı değil:</b> geri alınamaz bir şey olmadı. Kullanıcı bu ekranda "
           "kilitli kalmıyor: \"Hesapsız devam et\" hâlâ çalışıyor ve uygulamanın tamamı açık (K-052)."),
])


OUT.write_text(page(
    "Trinkow · Hesap oluştur — prototip v4",
    "E-23 · Hesap oluştur",
    "Arketip E — Form / sözleşme masası · push · Apple + Google + e-posta · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
