# -*- coding: utf-8 -*-
"""E-22 · Oturum aç — arketip E (Form), ama **kapı** modunda.

Mood: EŞİK. Bu ekran bir duvar değil, bir kapı (K-052: oturum duvarı YOK).
Bu yüzden düzen tek sütun, dar ve sakin; ekranda tek birincil buton var ve
"Hesapsız devam et" gerçekten görünür bir çıkış — gri, küçük, köşeye
sıkıştırılmış bir bağlantı değil, 44pt'lik `ghost` buton.

Ayrıştığı yer (E-23'ten): burada kullanıcı **geri dönüyor**, ikna edilmeye
ihtiyacı yok → mahremiyet cümlesi başlığın altında sessiz bir `caption`;
ekranın ağırlık merkezi ise iki sağlayıcı düğmesi ve form.

Sıralama kararı: sosyal düğmeler formun ÜSTÜNDE. Geri dönen kullanıcı için
en kısa yol tek dokunuş; e-posta/şifre yolu isteyen kullanıcı iki alanı
zaten arar.

**Sağlayıcı kümesi platforma göre değişir** (Mustafa kararı, 2026-09-17):
iOS'ta **Apple + Google** (App Store 4.8 Apple girişini zorunlu kılar,
Apple üstte), Android'de **yalnız Google** + e-posta/şifre. Apple'la
açılmış hesap Android'de "Şifremi unuttum" → şifre belirle yolundan
açılır; yeni ekran gerekmedi.

Şifremi unuttum **ayrı ekran değildir** (brief): ekrandaki e-posta alanı
zaten dolu; düğme o adrese bağlantı gönderir ve ekran tek bir onay
durumuna döner (G durumu). Alan boşsa alan düzeyinde hata verir.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, icon, push_basi, sosyal_kume, ayirac,
                 metin_alani, goz_btn)

OUT = pathlib.Path(__file__).parent.parent / "15-giris.html"

MAHREMIYET = "Harcamaların sende kalır. Hesap yalnız seni tanır."
EPOSTA = "ayse.kaya@example.com"
GIZLI = "••••••••••"


def kutu_ikon(ad, renk="var(--primary-text)"):
    return (f'<div class="clay-kuyu satir" style="width:44px;height:44px;'
            f'justify-content:center;color:{renk}"><div class="ikon-kutu">{icon(ad)}</div></div>')


def basi_alti(metin=MAHREMIYET):
    return f'''          <div class="pad kolon">
            <div class="t-cap">{metin}</div>
          </div>'''


def serit_baglanti():
    """Ağ hatası. Offline-first bir uygulamada oturum açmanın internet istemesi
    kullanıcıya **dürüstçe** söylenir; aynı cümle uygulamanın geri kalanının
    bağlantısız çalıştığını da hatırlatır, böylece hata korkutmaz."""
    return f'''          <div class="pad">
            <div class="serit serit-warn">
              <div class="ikon-kutu" style="color:var(--warning-ink)">{icon("wifi-off")}</div>
              <div class="w12"></div>
              <div class="esnek t-cap" style="color:var(--text)">Oturum açmak için bağlantı gerekir. Kayıtların bağlantısız çalışır.</div>
            </div>
          </div>'''


def alt_satir(unuttum_basili=False, kayit_basili=False):
    """İki kaçış yolu tek satırda: solda şifre kurtarma, sağda hesap açma.
    İkisi de `ghost` — eşit ağırlık, çünkü hangisinin gerektiğini yalnız
    kullanıcı bilir."""
    u = " basili" if unuttum_basili else ""
    k = " basili" if kayit_basili else ""
    return f'''          <div class="pad aralik">
            <button class="btn-ghost{u}" style="padding:0 16px">Şifremi unuttum</button>
            <button class="btn-ghost{k}" style="padding:0 16px">Hesap oluştur</button>
          </div>'''


def alt_sabit(durum="aktif", hesapsiz_basili=False):
    hb = " basili" if hesapsiz_basili else ""
    if durum == "pasif":
        btn = ('<button class="btn-primary pasif" disabled aria-disabled="true">'
               'Oturum aç</button>')
    elif durum == "loading":
        btn = ('<button class="btn-primary basili" disabled aria-disabled="true">'
               'Oturum açılıyor<div class="w8"></div><div class="spinner"></div></button>')
    else:
        btn = '<button class="btn-primary">Oturum aç</button>'
    return f'''          <div class="alt-sabit">
            <div class="pad kolon">
              {btn}
              <div class="h8"></div>
              <button class="btn-ghost{hb}" style="width:100%">Hesapsız devam et</button>
            </div>
          </div>'''


def govde(eposta="", eposta_hata="", sifre="", sifre_hata="", sifre_odakli=False,
          sifre_gorunur=False, imlec=False, eposta_odakli=False,
          serit="", unuttum_basili=False, apple_basili=False, google_basili=False,
          kaydirilmis=False, platform="ios"):
    """`kaydirilmis=True` → klavye açık durumun DÜRÜST çizimi: kullanıcı
    şifre alanına dokununca RN odaklanan alanı görünür alana kaydırır,
    başlık ve mahremiyet satırı yukarıda kalır. Kaydırma alanı 429px'e
    düşüyor (844 − 47 durum çubuğu − 116 alt blok − 28 home − 224 klavye);
    içerik 401px, yani alt kesme **24'lük boşluk bandına** denk gelir —
    hiçbir alan ortasından dilimlenmez (tokens §12/11c)."""
    s = [] if kaydirilmis else [push_basi("Oturum aç"), basi_alti()]
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
                    hata=eposta_hata, odakli=eposta_odakli,
                    a11y="E-posta adresi"),
        '          <div class="h12"></div>',
        metin_alani("Şifre", deger=sifre, placeholder="Şifreni yaz",
                    hata=sifre_hata, odakli=sifre_odakli, imlec=imlec,
                    sag_html=goz_btn(sifre_gorunur), a11y="Şifre"),
        '          <div class="h12"></div>',
        alt_satir(unuttum_basili=unuttum_basili),
        '          <div class="h24"></div>',
    ]
    return "\n".join(s)


# ------------------------------------------------------------------ A · boş
A = govde()

# ------------------------------------------- B · yazılıyor · şifre görünür
B = govde(eposta=EPOSTA, sifre="kirazli2026", sifre_odakli=True,
          sifre_gorunur=True, imlec=True, kaydirilmis=True)

# ----------------------------------------------------- D · şifre yanlış
# Mesaj BİLEREK genel: "e-posta kayıtlı değil" demek, hangi adreslerin
# kayıtlı olduğunu sızdırır. Hata şifre alanına bağlanır, çünkü kullanıcı
# eylemi orada yapacak.
D = govde(eposta=EPOSTA, sifre=GIZLI,
          sifre_hata="E-posta ya da şifre yanlış. Yeniden dene.")

# --------------------------------------------------- E · gönderiliyor
E = govde(eposta=EPOSTA, sifre=GIZLI)

# ------------------------------------------------------- F · ağ hatası
F = govde(eposta=EPOSTA, sifre=GIZLI, serit=serit_baglanti())

# ------------------------------- H · Android derlemesi (yalnız Google)
H = govde(platform="android", google_basili=True)

# ------------------------------------ G · şifre bağlantısı gönderildi
G = f'''{push_basi("Oturum aç")}
          <div class="h24"></div>
          <div class="pad">
            <div class="clay kart-ic kolon">
              {kutu_ikon("mail-check")}
              <div class="h12"></div>
              <div class="t-h2">Bağlantıyı gönderdik</div>
              <div class="h8"></div>
              <div class="t-body">{EPOSTA} adresine şifre bağlantısı gitti.</div>
              <div class="h8"></div>
              <div class="t-cap">Gelmediyse istenmeyen klasörüne bak.</div>
              <div class="h12"></div>
              <button class="btn-secondary pasif" disabled aria-disabled="true">Yeniden gönder</button>
              <div class="h8"></div>
              <div class="t-cap">60 saniye sonra yeniden gönderebilirsin.</div>
            </div>
          </div>
          <div class="h24"></div>
          <div class="pad kolon">
            <button class="btn-ghost" style="width:100%">Oturum açmaya dön</button>
          </div>
          <div class="h24"></div>'''


units = "".join([
    device("GİRİŞ", "E-22 · boş · varsayılan", A, sabit_alt=alt_sabit("pasif"), note=
           "<b>Mood: eşik.</b> Bu ekran duvar değil kapı (K-052: oturum duvarı yok) — <b>Hesapsız devam et</b> "
           "44pt'lik gerçek bir düğme, dipnot değil. <b>Mahremiyet cümlesi</b> başlığın hemen altında ve "
           "dürüst: \"Harcamaların sende kalır. Hesap yalnız seni tanımak için.\" — \"sunucu yok / hesap yok\" "
           "ifadesi K-052'den sonra YANLIŞ olduğu için kullanılmadı; \"cihaz/sunucu/senkron\" gibi teknik "
           "sözcükler de girmedi (brandbook §2.8). "
           "<b>Üçüncü taraf düğmeleri:</b> App Store 4.8 gereği Apple ve Google birlikte ve eşit ağırlıkta. "
           "Uzlaşma kuralı <b>kap bizim, içerik onların</b>: kap 56pt/radius 999/<code>clay.raised</code>, "
           "dolgu-logo-etiket sağlayıcının kılavuzundan (Apple siyah stil, Google açık stil + 1px "
           "<code>#747775</code> kontur). Logolar bozulmadı, renklendirilmedi, yeniden çizilmedi. "
           "<b>Birincil buton pasif:</b> alanlar boş; pasiflik opaklıkla değil <code>disabled-bg</code> + "
           "<code>clay.sunken</code> ile. <b>\"ya da\" ayracında saç teli çizgi yok</b> — "
           "<code>line</code> sayfa zemininde 1.08:1, yani görünmez bir çizgi olurdu."),
    device("GİRİŞ", "E-22 · yazılıyor · klavye açık · form kaydırıldı", B, sabit_alt=alt_sabit(), klavye=True, note=
           "<b>Ekran kaydırılmış hâlde çizildi:</b> şifre alanına dokunulunca RN odaklanan alanı görünür "
           "alana taşır; başlık ve mahremiyet satırı yukarıda kalır. Kaydırma alanı klavyeyle 429px'e "
           "iner, içerik 401px → <b>alt kesme 24'lük boşluk bandına denk gelir</b>, hiçbir alan "
           "ortasından dilimlenmez. "
           "<b>Klavye açıkken de birincil buton görünür</b> (sistem klavyesi bölge [A]'da çizildi): RN'de "
           "<code>KeyboardAvoidingView</code> şart, çünkü bu ekran tutar girişi gibi kil tuş takımı "
           "kullanamaz — e-posta/şifre sistem klavyesi ister. <b>Şifre görünürlüğü</b> bir durum değil bir "
           "eylem: ikon <code>eye</code> ↔ <code>eye-off</code>, etiket \"Şifreyi göster\" ↔ \"Şifreyi gizle\". "
           "Odaklı alan 2pt <code>primary-text</code> kenarlık + 3pt imleç. Alan yüksekliği 56, dokunma "
           "hedefi tamamı; göz düğmesi 44pt ve alanın sağ iç boşluğu 16 → 8'e iner."),
    device("GİRİŞ", "E-22 · geçersiz e-posta + Şifremi unuttum basılı",
           govde(eposta="ayse.kaya@example", eposta_hata="Geçerli bir e-posta yaz.",
                 sifre=GIZLI, unuttum_basili=True),
           sabit_alt=alt_sabit(), note=
           "<b>Alan düzeyinde hata:</b> 2pt <code>danger</code> kenarlık + altında 8 boşlukla "
           "<code>caption</code>/<code>danger-ink</code> — kırmızının izinli dört bağlamından biri "
           "(\"form hatası kenarlığı + metni\"). Hata <b>hangi alanda</b> olduğunu gösterir, ekranın "
           "tepesinde genel bir kırmızı şerit yoktur. <b>Şifremi unuttum basılı (pressed)</b> çizildi: "
           "bu düğme ayrı bir ekran açmaz, ekrandaki e-posta adresine bağlantı gönderir ve ekran "
           "G durumuna döner. Adres boşsa bu alan aynı desende \"Önce e-postanı yaz.\" hatası alır."),
    device("GİRİŞ", "E-22 · şifre yanlış", D, sabit_alt=alt_sabit(), note=
           "<b>Mesaj bilerek genel:</b> \"Bu e-posta kayıtlı değil\" demek, hangi adreslerin kayıtlı "
           "olduğunu sızdırır (hesap sayımı saldırısı). Metin \"E-posta ya da şifre yanlış. Yeniden dene.\" — "
           "ne olduğunu değil <b>ne yapılacağını</b> söyleyen ton, <code>hata.*</code> satırlarının aynısı. "
           "Hata şifre alanına bağlandı: kullanıcı eylemi orada yapacak. Suçlayıcı dil, ünlem ve "
           "\"başarısız\" sözcüğü yok."),
    device("GİRİŞ", "E-22 · gönderiliyor", E, sabit_alt=alt_sabit("loading"), note=
           "<b>Düğme meşgul:</b> metin \"Oturum açılıyor\" + 20pt spinner, genişlik sabit, "
           "<code>disabled</code>. Spinner yalnız buton içinde (tokens §7.10) — tam ekran kaplayan "
           "dönen çark yok. <b>Hesapsız devam et açık kalır:</b> ağ takılırsa kullanıcı hapis kalmaz. "
           "Alanlar yerinde durur, iskelete dönmez: yazdığı şey kaybolmadı."),
    device("GİRİŞ", "E-22 · ağ hatası", F, sabit_alt=alt_sabit(), note=
           "<b>Offline-first bir uygulamada oturum açmanın internet istemesi dürüstçe söylenir.</b> Şeridin "
           "ikinci yarısı korkuyu alır: \"Kayıtların bağlantısız çalışır.\" — yani bu hata ürünü değil "
           "yalnız kimliği durdurur. Şerit <b>amber</b> (<code>warning</code> ailesi), kırmızı değil: "
           "geri alınamaz bir şey olmadı. Düğme etiketi \"Oturum aç\" kalır; \"Yeniden dene\" yazmak "
           "kullanıcıya ikinci bir kelime öğretmek olurdu."),
    device("GİRİŞ", "E-22 · Android derlemesi · yalnız Google", H,
           sabit_alt=alt_sabit("pasif"), note=
           "<b>Android'de Apple düğmesi hiç çizilmez</b> (Mustafa kararı): App Store kuralı 4.8 yalnız "
           "iOS'u bağlar, Android'de Apple akışı web köprüsü ister — ek iş, ek hata yüzeyi. "
           "<b>Yarım çalışan bir düğme, hiç olmayan düğmeden kötüdür.</b> Küme tek düğmeye inince "
           "düzen bozulmuyor: \"ya da\" ayracı ve form aynı yerde kalır, ekran 56pt kısalır. "
           "<b>Apple ile açılmış hesap Android'de kilitli kalmaz:</b> Apple'ın verdiği e-posta hesabın "
           "kimliğidir → kullanıcı <b>Şifremi unuttum</b> ile o adrese bağlantı ister, şifre belirler ve "
           "e-posta/şifre ile girer. Bu yol için <b>yeni ekran üretilmedi</b>; G durumu bu boşluğu "
           "zaten kapatıyor. <b>Google düğmesi basılı (pressed)</b> çizildi."),
    device("GİRİŞ", "E-22 · şifre bağlantısı gönderildi", G, note=
           "<b>Şifremi unuttum için ayrı ekran YOK</b> — aynı ekranın bir durumu. Kart ne olduğunu, "
           "nereye gittiğini ve gelmezse ne yapılacağını söyler. <b>\"Yeniden gönder\" pasif</b> ve "
           "sebebi hemen altında yazılı (60 sn): sayaç göstermek yerine tek cümle, çünkü tik tak eden "
           "bir sayı bekleme hissini büyütür. <b>Alt sabit blok düşer:</b> bu durumda birincil eylem "
           "yoktur, kullanıcı ya postasına gider ya oturum açmaya döner — sahte bir birincil buton bırakmak "
           "ekranı yalancı yapardı."),
])

OUT.write_text(page(
    "Trinkow · Oturum aç — prototip v4",
    "E-22 · Oturum aç",
    "Arketip E — Form / kapı · push · Apple + Google + e-posta · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)

