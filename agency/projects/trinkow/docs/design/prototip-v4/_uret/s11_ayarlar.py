# -*- coding: utf-8 -*-
"""E-19 · Ayarlar — arketip E (Form), E-17'nin kardeşi ama aynısı değil.

Mood: ARKA ODA. E-17 "ayar masası"dır (sayı değiştirilir, Kaydet vardır);
E-19'da **Kaydet yoktur** — her anahtar dokunulduğu anda geçerlidir. Bu
yüzden ekranda birincil buton hiç bulunmaz ve alt sabit blok yoktur.

Bölümler kart, kararlar kartın içinde çukur satırlardır: kabarık kart =
konu, çukur satır = değiştirilebilir değer. Kullanıcı neyin dokunulabilir
olduğunu renkten değil **derinlikten** anlar.

UI'da teknik açıklama YOKTUR (brandbook §2.8): "cihazda", "sunucu",
"yedek", "senkronizasyon" geçmez. Veri bölümü kullanıcı diliyle konuşur.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page, icon, push_basi, anahtar, kuyu_deger

OUT = pathlib.Path(__file__).parent.parent / "11-ayarlar.html"


def bolum(baslik, ic):
    return f'''          <div class="pad">
            <div class="clay kart-ic">
              <div class="t-h2">{baslik}</div>
              <div class="h8"></div>
{ic}
            </div>
          </div>'''


def anahtar_satiri(ad, aciklama, acik=True, basili=False, pasif=False):
    """Dokunma hedefi anahtarın 56×32'si değil, satırın tamamıdır (≥68pt).
    Pasif durumda opaklık kullanılmaz: anahtar çukur kalır, açıklama satırı
    değişir."""
    b = " basili" if basili else ""
    sw = anahtar(acik and not pasif, basili=False, etiket=ad)
    return f'''              <button class="ayar-satir{b}" style="padding:12px 16px">
                <div class="esnek kolon">
                  <div class="t-strong">{ad}</div>
                  <div class="h4"></div>
                  <div class="t-cap">{aciklama}</div>
                </div>
                <div class="w12"></div>
                {sw}
              </button>'''


def deger_satiri(ad, deger, basili=False):
    b = " basili" if basili else ""
    return f'''              <button class="kuyu-btn{b}" style="padding:12px 16px" aria-label="{ad}: {deger}. Değiştir">
                <div class="esnek t-strong">{ad}</div>
                <div class="w12"></div>
                <div class="t-amount">{deger}</div>
                <div class="w12"></div>
                {icon("chevron-right")}
              </button>'''


def segment(secenekler, secili, etiket=""):
    btn = "".join(
        f'<button class="segment-btn{" secili" if s == secili else ""}">{s}</button>'
        for s in secenekler)
    return f'<div class="segment">{btn}</div>'


def aciklama(metin):
    return f'''              <div class="h8"></div>
              <div class="t-cap">{metin}</div>'''


# ---------------------------------------------------------------- bölümler
def bildirim_bolumu(izin=True, saat_basili=False):
    if izin:
        ic = (anahtar_satiri("Akşam özeti", "Günde en fazla bir bildirim.", acik=True)
              + '\n              <div class="h12"></div>\n'
              + deger_satiri("Bildirim saati", "21.00", basili=saat_basili))
    else:
        ic = (anahtar_satiri("Akşam özeti", "Bildirim izni kapalı. Cihaz ayarlarından açabilirsin.",
                             acik=False, pasif=True)
              + '''\n              <div class="h12"></div>
              <div class="serit serit-info">
                <div class="ikon-kutu" style="color:var(--primary-text)">''' + icon("bell") + '''</div>
                <div class="w12"></div>
                <div class="esnek t-cap">İzin verilene kadar akşam özeti gönderilmez.</div>
              </div>''')
    return bolum("Bildirim", ic)


def gun_bolumu(secili="00.00", basili=False):
    return bolum("Gün sınırı", f'''              <div class="t-cap">Gün bu saatte başlar. Gece geç harcayanlar için.</div>
              <div class="h12"></div>
              {segment(["00.00", "03.00", "06.00"], secili)}''')


def odeme_bolumu(secili="Kart"):
    """🔴 TEK DEĞER: varsayılan ödeme tipi "Kart" (ekran-envanteri §4).
    Hiçbir yüzeyde başka bir varsayılan gösterilmez; E-11'in açılış yüzeyi de
    bunu okur. Parametre yalnız kullanıcı seçimini anlatmak için vardır."""
    return bolum("Varsayılan ödeme", f'''              <div class="t-cap">Yeni harcama bu seçimle açılır.</div>
              <div class="h12"></div>
              <div class="segment">
                <button class="segment-btn{" secili" if secili == "Nakit" else ""}">{icon("banknote")}<div class="w8"></div>Nakit</button>
                <button class="segment-btn{" secili" if secili == "Kart" else ""}">{icon("credit-card")}<div class="w8"></div>Kart</button>
              </div>''')


def kip_bolumu(deger="Bütçe"):
    return bolum("Kip", f'''              <div class="t-cap">Panodaki büyük sayıyı belirler.</div>
              <div class="h12"></div>
              {deger_satiri("Kip", deger)}''')


def hesap_bolumu(oturum=True, cikis_basili=False, sil_basili=False,
                 giris_basili=False, eposta="ayse.kaya@ogrenci.marmara.edu.tr"):
    """**Hesap** bölümü (K-052). Konum kararı: bölümün yeri ekranın BAŞI
    değil, **Veri'nin hemen üstü.** Gerekçe: hesap bu üründe isteğe bağlı
    bir kimlik katmanı; ayarları açan kullanıcı çoğunlukla bildirim/limit
    için gelir. Hesabı en üste koymak, K-052'nin \"hesap zorunlu değil\"
    kararının tersini söyleyen bir hiyerarşi kurardı. Kimlik ve veri
    yan yana durur, çünkü kullanıcının kafasındaki soru ikisinde de aynı:
    \"benim kayıtlarıma ne oluyor?\"

    Oturum KAPALIYKEN tek satır, baskı yok: birincil buton, kart içi
    reklam, \"hesabını koru\" tonu yok.
    """
    if not oturum:
        gb = " basili" if giris_basili else ""
        return bolum("Hesap", f'''              <div class="t-cap">Hesap isteğe bağlı. Kayıtların sende kalır.</div>
              <div class="h12"></div>
              <button class="kuyu-btn{gb}" style="padding:12px 16px" aria-label="Oturum aç ya da hesap oluştur">
                <div class="esnek t-strong">Oturum aç ya da hesap oluştur</div>
                <div class="w12"></div>
                {icon("chevron-right")}
              </button>''')
    cb = " basili" if cikis_basili else ""
    sb = " basili" if sil_basili else ""
    return bolum("Hesap", f'''              <div class="t-cap">Hesap yalnız seni tanımak için.</div>
              <div class="h12"></div>
              <div class="clay-kuyu kolon" style="padding:12px 16px">
                <div class="t-label c-2">E-posta</div>
                <div class="h4"></div>
                <div class="t-body tek-satir" aria-label="Hesap e-postası {eposta}">{eposta}</div>
              </div>
              <div class="h8"></div>
              <div class="t-cap">Google ile bağlı.</div>
              <div class="h12"></div>
              <div class="kolon" style="align-items:flex-start">
                <button class="btn-ghost{cb}" style="padding:0 16px" aria-label="Çıkış yap">{icon("log-out")}<div class="w8"></div>Çıkış yap</button>
              </div>
              <div class="h8"></div>
              <div class="t-cap">Çıkınca kayıtların sende kalır.</div>
              <div class="h12"></div>
              <div class="kolon" style="align-items:flex-start">
                <button class="btn-ghost{sb}" style="padding:0 16px" aria-label="Hesabı sil">{icon("trash-2")}<div class="w8"></div>Hesabı sil</button>
              </div>''')


def plan_bolumu(kurulu=True, basili=False):
    """**Plan ve profil** (K-053 · F-12). Katman 2 ayarlardan tamamlanır ve
    Katman 1'de atlanan gelir buradan sonradan girilir — onboarding'de
    atlanan hiçbir soru kaybolmaz, hepsi burada bekler.

    Bölümün yeri: **Kip'in hemen altı.** Kip panodaki büyük sayının
    *hangi* sayı olduğunu belirler, plan ise o sayının *kaç* olduğunu;
    ikisi komşu durur. Limitler (E-17) ayrı bir ekranda kalır: orada sayı
    elle yazılır, burada plandan türetilir.
    """
    b = " basili" if basili else ""
    if kurulu:
        ic = f'''              <div class="t-cap">Plan cevaplarından çıkar. İstediğin an değiştir.</div>
              <div class="h12"></div>
              {deger_satiri("Aylık net gelir", "32.000 ₺")}
              <div class="h12"></div>
              {deger_satiri("Maaş günü", "Ayın 15'i")}
              <div class="h12"></div>
              {kuyu_deger("Seni tanıyalım", "", bos="4 kart kaldı")}
              <div class="h12"></div>
              <button class="kuyu-btn{b}" style="padding:12px 16px" aria-label="Planı gör">
                <div class="esnek t-strong">Planı gör</div>
                <div class="w12"></div>
                {icon("chevron-right")}
              </button>'''
    else:
        ic = f'''              <div class="t-cap">Gelirini girmedin. Plan onsuz kurulmuyor.</div>
              <div class="h12"></div>
              {kuyu_deger("Aylık net gelir", "", bos="Girilmedi")}
              <div class="h12"></div>
              {kuyu_deger("Seni tanıyalım", "", bos="8 kart bekliyor")}
              <div class="h12"></div>
              <div class="t-cap">Günlük limitini şimdilik Limitler ekranından yazıyorsun.</div>'''
    return bolum("Plan ve profil", ic)


def veri_bolumu(basili=False):
    b = " basili" if basili else ""
    return bolum("Veri", f'''              <div class="t-body">Kayıtların sende kalır. İstediğin an hepsini silebilirsin.</div>
              <div class="h12"></div>
              <button class="btn-ghost{b}" style="padding:0 16px;align-self:flex-start" aria-label="Tüm verileri sil">{icon("trash-2")}<div class="w8"></div>Tüm verileri sil</button>''')


SURUM = '''          <div class="pad">
            <div class="t-micro">Sürüm 1.0.0</div>
          </div>'''


# ------------------------------------------------------------------ A · dolu
A = f'''{push_basi("Ayarlar")}
{bildirim_bolumu()}
          <div class="h24"></div>
{gun_bolumu()}
          <div class="h24"></div>
{odeme_bolumu()}
          <div class="h24"></div>
{kip_bolumu()}
          <div class="h24"></div>
{plan_bolumu(kurulu=True)}
          <div class="h24"></div>
{hesap_bolumu(oturum=True)}
          <div class="h24"></div>
{veri_bolumu()}
          <div class="h24"></div>
{SURUM}
          <div class="h24"></div>'''

# ------------------------------- B · bildirim izni yok + gün sınırı değişti
B = f'''{push_basi("Ayarlar")}
{bildirim_bolumu(izin=False)}
          <div class="h24"></div>
{gun_bolumu(secili="03.00")}
          <div class="h24"></div>
{odeme_bolumu()}
          <div class="h24"></div>
{kip_bolumu("Takip")}
          <div class="h24"></div>
{plan_bolumu(kurulu=False)}
          <div class="h24"></div>
{hesap_bolumu(oturum=False, giris_basili=True)}
          <div class="h24"></div>
{veri_bolumu(basili=True)}
          <div class="h24"></div>
{SURUM}
          <div class="h24"></div>'''

# ------------------------------------------------ C · tüm verileri sil onayı
C_DIALOG = f'''          <div class="katman-ust" style="justify-content:center">
            <div class="scrim-kat"></div>
            <div class="scrim-kat" style="flex:0 0 auto;padding:16px">
              <div class="dialog kart-ic kolon">
                <div class="ikon-kab-danger">{icon("trash-2")}</div>
                <div class="h12"></div>
                <div class="t-h2">Tüm kayıtların silinecek</div>
                <div class="h8"></div>
                <div class="t-body">Geri alınamaz. Limitlerin ve kurulumun kalır.</div>
                <div class="h12"></div>
                <div class="serit serit-danger">
                  <div class="ikon-kutu" style="color:var(--danger-ink)">{icon("notebook-text")}</div>
                  <div class="w12"></div>
                  <div class="esnek t-cap" style="color:var(--text)">214 kayıt · Haziran 2026'dan bugüne</div>
                </div>
                <div class="h12"></div>
                <button class="btn-danger">Sil</button>
                <div class="h8"></div>
                <button class="btn-ghost" style="width:100%">Vazgeç</button>
              </div>
            </div>
            <div class="scrim-kat"></div>
          </div>
'''


# ------------------------------------------------- D · hesabı sil onayı
# App Store 5.1.1(v): hesap açtıran uygulama hesabı SİLME yolunu da
# uygulama içinde sunmak zorundadır. Onay diyaloğu kırmızının izinli dört
# bağlamından biridir (yüksek etkili + geri alınamaz).
#
# Diyaloğun asıl işi bir soruyu cevaplamak: **"kayıtlarıma ne olacak?"**
# Cevap ekranda yazılı ve ayrımı nettir: hesap gider, KAYITLAR KALIR.
# Veri silmek isteyen kullanıcı için ayrı ve ayrı duran yol gösterilir
# ("Veri bölümü"). İki yıkıcı işlemi tek düğmeye bağlamak, kullanıcının
# kastetmediği bir şeyi silmesinin en bilinen yoludur.
D_DIALOG = f'''          <div class="katman-ust" style="justify-content:center">
            <div class="scrim-kat"></div>
            <div class="scrim-kat" style="flex:0 0 auto;padding:16px">
              <div class="dialog kart-ic kolon">
                <div class="ikon-kab-danger">{icon("trash-2")}</div>
                <div class="h12"></div>
                <div class="t-h2">Hesabın silinecek</div>
                <div class="h8"></div>
                <div class="t-body">Geri alınamaz. Bu e-posta ile bir daha oturum açamazsın.</div>
                <div class="h12"></div>
                <div class="serit serit-danger">
                  <div class="ikon-kutu" style="color:var(--danger-ink)">{icon("notebook-text")}</div>
                  <div class="w12"></div>
                  <div class="esnek t-cap" style="color:var(--text)">214 kayıt sende kalır. Silmek istersen Veri bölümünü kullan.</div>
                </div>
                <div class="h12"></div>
                <button class="btn-danger">Hesabı sil</button>
                <div class="h8"></div>
                <button class="btn-ghost" style="width:100%">Vazgeç</button>
              </div>
            </div>
            <div class="scrim-kat"></div>
          </div>
'''


units = "".join([
    device("AYARLAR", "E-19 · dolu", A, note=
           "<b>Kaydet yok.</b> Her anahtar dokunulduğu anda geçerlidir; bu yüzden ekranda birincil buton "
           "ve alt sabit blok bulunmaz — E-17'den ayrıldığı yer burasıdır. Kabarık kart = konu, "
           "<b>çukur satır = değiştirilebilir değer</b>. Anahtarın dokunma hedefi 56×32 değil, satırın "
           "tamamıdır (68pt). Platform <code>Switch</code>'i kullanılmaz: iOS/Android farklı çizer, clay dili "
           "uygulanamaz. "
           "<b>Yeni: Hesap bölümü</b> (K-052). Yeri ekranın başı değil <b>Veri'nin hemen üstü</b> — "
           "hesap bu üründe isteğe bağlı bir kimlik katmanı; en üste koymak \"hesap zorunlu\" diyen bir "
           "hiyerarşi kurardı. Kimlik ve veri komşu duruyor, çünkü kullanıcının sorusu ikisinde de aynı: "
           "\"kayıtlarıma ne oluyor?\" E-posta satırı <b>dokunulmaz çukur</b> (değiştirilemez değer, "
           "<code>ValueWell</code>'in dokunulmaz varyantı) ve uzun adres <b>kırpılır</b> "
           "(<code>ellipsizeMode=tail</code>), tam hâli <code>accessibilityLabel</code>'da. "
           "\"Google ile bağlı.\" satırı şifreyle mi sağlayıcıyla mı girdiğini söyler; bu bilgi "
           "olmadan kullanıcı \"şifremi neden soramıyorum\" sorusuna düşer."),
    device("AYARLAR", "E-19 · bildirim izni kapalı", B, note=
           "<b>İzin yoksa anahtar yalan söylemez:</b> kapalı ve çukur durur, açıklama satırı değişir "
           "(\"Cihaz ayarlarından açabilirsin.\") ve <b>bildirim saati satırı düşer</b> — kapalı bir "
           "bildirimin saatini sormak anlamsızdır. Opaklıkla pasiflik yok. Gün sınırı 03.00 seçili: "
           "gece 01.00'deki harcama <b>dünkü güne</b> yazılır. "
           "<b>Oturum kapalı Hesap bölümü:</b> tek satır, baskı yok (K-052 + F-2/F-9). Birincil buton, "
           "kart içi çağrı, \"hesabını koru\" tonu yok; yalnız nötr bir kapı: "
           "\"Oturum aç ya da hesap oluştur\". Üstünde tek cümle beklentiyi düzeltir: "
           "\"Hesap isteğe bağlı. Kayıtların sende kalır.\""),
    device("AYARLAR", "E-19 · tüm verileri sil", A, sabit_alt=C_DIALOG, note=
           "<b>Kırmızının izinli dört bağlamından biri</b> (K-029 ölçütü: yüksek etkili + geri alınamaz). "
           "İzinli bağlamlar: E-13 taksit serisi silme onayı · E-19 tüm veriyi silme onayı (bu yüzey) · "
           "form hatası kenarlığı · silme toast'ının 8pt göstergesi. Tek harcama silmek onay "
           "istemez; 214 kaydın tamamını silmek ister. <b>Ne silineceği sayıyla</b> gösterilir ve neyin "
           "<b>kalacağı</b> da söylenir (\"Limitlerin ve kurulumun kalır.\") — belirsizlik korkutur. "
           "Bu ekranda \"cihazda / sunucuda / yedek\" gibi tek bir teknik sözcük geçmez."),
    device("AYARLAR", "E-19 · hesabı sil onayı", A, sabit_alt=D_DIALOG, note=
           "<b>App Store 5.1.1(v):</b> hesap açtıran uygulama, hesabı silme yolunu da uygulama içinde "
           "sunmak zorundadır. Diyaloğun asıl işi <b>tek bir soruyu cevaplamak</b>: \"kayıtlarıma ne "
           "olacak?\" Cevap ekranda yazılı ve ayrım nettir — <b>hesap gider, kayıtlar kalır</b> "
           "(\"214 kayıt sende kalır.\"). Veri silmek isteyen kullanıcıya ayrı yol gösterilir "
           "(\"Veri bölümünü kullan\"). İki yıkıcı işlemi tek düğmeye bağlamak, kullanıcının "
           "kastetmediği şeyi silmesinin en bilinen yoludur; bu yüzden <b>iki ayrı onay, iki ayrı "
           "kapı.</b> <b>Çıkış yap için diyalog YOK</b> ve bu bilinçli: çıkmak geri alınabilir "
           "(yeniden oturum) ve kayıtlara dokunmaz — sebebi düğmenin altında tek satır yazılı "
           "(\"Çıkınca kayıtların sende kalır.\"). Her yıkıcı-olmayan eyleme diyalog koymak, "
           "diyalogların anlamını tüketir."),
])

OUT.write_text(page(
    "Trinkow · Ayarlar — prototip v4",
    "E-19 · Ayarlar",
    "Arketip E — Form / arka oda · push · Kaydet yok · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)

