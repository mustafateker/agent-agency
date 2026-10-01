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
from lib import device, page, icon, push_basi, anahtar

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


units = "".join([
    device("AYARLAR", "E-19 · dolu", A, note=
           "<b>Kaydet yok.</b> Her anahtar dokunulduğu anda geçerlidir; bu yüzden ekranda birincil buton "
           "ve alt sabit blok bulunmaz — E-17'den ayrıldığı yer burasıdır. Kabarık kart = konu, "
           "<b>çukur satır = değiştirilebilir değer</b>. Anahtarın dokunma hedefi 56×32 değil, satırın "
           "tamamıdır (68pt). Platform <code>Switch</code>'i kullanılmaz: iOS/Android farklı çizer, clay dili "
           "uygulanamaz."),
    device("AYARLAR", "E-19 · bildirim izni kapalı", B, note=
           "<b>İzin yoksa anahtar yalan söylemez:</b> kapalı ve çukur durur, açıklama satırı değişir "
           "(\"Cihaz ayarlarından açabilirsin.\") ve <b>bildirim saati satırı düşer</b> — kapalı bir "
           "bildirimin saatini sormak anlamsızdır. Opaklıkla pasiflik yok. Gün sınırı 03.00 seçili: "
           "gece 01.00'deki harcama <b>dünkü güne</b> yazılır."),
    device("AYARLAR", "E-19 · tüm verileri sil", A, sabit_alt=C_DIALOG, note=
           "<b>Kırmızının izinli dört bağlamından biri</b> (K-029 ölçütü: yüksek etkili + geri alınamaz). "
           "İzinli bağlamlar: E-13 taksit serisi silme onayı · E-19 tüm veriyi silme onayı (bu yüzey) · "
           "form hatası kenarlığı · silme toast'ının 8pt göstergesi. Tek harcama silmek onay "
           "istemez; 214 kaydın tamamını silmek ister. <b>Ne silineceği sayıyla</b> gösterilir ve neyin "
           "<b>kalacağı</b> da söylenir (\"Limitlerin ve kurulumun kalır.\") — belirsizlik korkutur. "
           "Bu ekranda \"cihazda / sunucuda / yedek\" gibi tek bir teknik sözcük geçmez."),
])

OUT.write_text(page(
    "Trinkow · Ayarlar — prototip v3",
    "E-19 · Ayarlar",
    "Arketip E — Form / arka oda · push · Kaydet yok · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
