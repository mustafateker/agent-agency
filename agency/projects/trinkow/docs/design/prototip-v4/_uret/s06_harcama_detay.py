# -*- coding: utf-8 -*-
"""E-12 · Harcama detayı (sheet) + E-13 · Taksit serisi silme onayı (dialog).

🔴 K-029 (Mustafa, seçenek C) — silme **etkiye göre** ikiye ayrıldı:

  · Tek harcama  → E-12'de "Sil" → **onay yok**, kayıt gider,
                   6 sn'lik **geri al toast'ı** çıkar.
  · Taksit serisi → E-12'de "Taksit serisini sil" → **E-13 onay diyaloğu**
                   ("Kalan 9 taksit de silinecek. Geri alınamaz.").

Gerekçe: tek harcama silmek sık ve düşük etkili bir iştir; her seferinde
onay istemek onayı anlamsızlaştırır ve gerçekten tehlikeli olan taksit
serisi silmeyi de sıradanlaştırır. Taksit serisi aylara yayılmış birden
çok kaydı siler, geri alınamaz — orada durdurma haklıdır.

Arketip B — Detail. Sekme çubuğu DÜŞER (örtüşen yüzey); arkadaki liste
görünür kalır ki kullanıcı nereden geldiğini kaybetmesin.

`danger #DC2626`nın TÜM prototipteki izinli DÖRT bağlamı (K-029 ölçütü:
yüksek etkili + geri alınamaz):
  1) E-13 taksit serisi silme onayı   2) E-19 tüm veriyi silme onayı
  3) form hatası kenarlığı + metni    4) silme toast'ının 8pt göstergesi
Tek harcama silme onay diyaloğu görmez (geri al toast'ı yeterlidir);
limit dışı hiçbir yerde kırmızı değildir — o warning ailesindedir.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import (device, page, satir, icon, ay_secici, gun_basligi,
                 sekme_cubugu, CATS)

OUT = pathlib.Path(__file__).parent.parent / "06-harcama-detay.html"


# ---------------------------------------------------- arka plan: E-14 listesi
def arka():
    return f'''          <div class="ekran-basi">
            <div class="t-h1">Kayıtlar</div>
            <button class="ikon-btn" aria-label="Taksitli işlemleri aç">{icon("repeat")}</button>
          </div>
{ay_secici("Eylül 2026", "48 kayıt · 12.480 ₺")}
          <div class="h24"></div>
{gun_basligi("Bugün · 10 Eylül", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Ulaşım", "09.05 · Kart", "42 ₺")}
          </div>
          <div class="h24"></div>
{gun_basligi("Dün · 9 Eylül", "", limit_disi="940 ₺ · limit dışı")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Restoran", "21.30 · Kart", "640 ₺", limit_disi=True, basili=True)}
          </div>
          <div class="h24"></div>'''


# ------------------------------------------------------------- E-12 parçaları
def tutar_alani(sayi="640", tarih="9 Eylül · 21.30"):
    return f'''                <div class="clay-kuyu" style="padding:16px">
                  <div class="aralik">
                    <div class="t-label c-2">Tutar</div>
                    <div class="t-cap">{tarih}</div>
                  </div>
                  <div class="h8"></div>
                  <div class="satir" style="justify-content:center;align-items:baseline">
                    <div class="t-display">{sayi}</div>
                    <div class="w8"></div>
                    <div class="t-amount c-2">₺</div>
                  </div>
                </div>'''


def kategori_alani(ad="Restoran"):
    renk = CATS[ad][1][4:]
    return f'''                <div class="t-label c-2">Kategori</div>
                <div class="h8"></div>
                <button class="secim-ozet" aria-label="Kategoriyi değiştir">
                  <div class="nokta" style="background-color:var(--cat-{renk})"></div>
                  <div class="w12"></div>
                  <div class="esnek t-body" style="text-align:left">{ad}</div>
                  <div class="w12"></div>
                  {icon("chevron-down")}
                </button>'''


def odeme_alani(kart=True):
    n = "" if kart else " secili"
    k = " secili" if kart else ""
    return f'''                <div class="t-label c-2">Ödeme</div>
                <div class="h8"></div>
                <div class="segment">
                  <button class="segment-btn{n}">{icon("banknote")}<div class="w8"></div>Nakit</button>
                  <button class="segment-btn{k}">{icon("credit-card")}<div class="w8"></div>Kart</button>
                </div>'''


def not_alani(metin="Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü"):
    return f'''                <div class="t-label c-2">Not</div>
                <div class="h8"></div>
                <div class="giris">
                  <div class="esnek t-body tek-satir">{metin}</div>
                </div>'''


def alt_eylem(durum="aktif", sil_basili=False, taksit=False):
    """Tek harcama: Sil (ghost, dar) + Kaydet yan yana — silme onaysızdır,
    geri al toast'ı korur. Taksit serisi: Kaydet üstte tam genişlik, altında
    tam genişlik "Taksit serisini sil" — ağır eylem yanlışlıkla basılmasın
    diye Kaydet'in yanından alınır ve kendi satırına konur (K-029)."""
    sb = " basili" if sil_basili else ""
    if durum == "loading":
        kaydet = ('<button class="btn-primary basili" disabled aria-disabled="true">Kaydediliyor'
                  '<div class="w8"></div><div class="spinner"></div></button>')
    else:
        kaydet = '<button class="btn-primary">Kaydet</button>'
    if taksit:
        return f'''                {kaydet}
                <div class="h8"></div>
                <button class="btn-ghost{sb}" style="width:100%" aria-label="Taksit serisini sil">{icon("trash-2")}<div class="w8"></div>Taksit serisini sil</button>'''
    return f'''                <div class="satir">
                  <button class="btn-ghost{sb}" style="padding:0 16px;flex:0 0 auto" aria-label="Bu harcamayı sil">{icon("trash-2")}<div class="w8"></div>Sil</button>
                  <div class="w8"></div>
                  <div class="esnek">{kaydet}</div>
                </div>'''


def sheet(ic):
    return f'''          <div class="katman-ust">
            <div class="scrim-kat"></div>
            <div class="sheet">
              <div class="satir" style="justify-content:center"><div class="sheet-tutamac"></div></div>
              <div class="h12"></div>
              <div class="aralik">
                <div class="t-h2">Harcama</div>
                <button class="ikon-btn" aria-label="Kapat">{icon("x")}</button>
              </div>
              <div class="h24"></div>
{ic}
            </div>
          </div>
'''


def detay(taksit=False, durum="aktif"):
    taksit_serit = ""
    if taksit:
        taksit_serit = f'''                <div class="h8"></div>
                <div class="serit serit-info">
                  <div class="ikon-kutu" style="color:var(--primary-text)">{icon("repeat")}</div>
                  <div class="w12"></div>
                  <div class="esnek kolon">
                    <div class="t-cap">3/12 taksit · her ay 1.040 ₺</div>
                    <div class="h4"></div>
                    <div class="t-cap">Düzenleme tüm taksit serisini etkiler.</div>
                  </div>
                </div>'''
    ic = f'''{tutar_alani("1.040,00" if taksit else "640", "9 Eylül · 21.30" if not taksit else "12 Haziran · 19.40")}
{taksit_serit}
              <div class="h24"></div>
{kategori_alani("Diğer" if taksit else "Restoran")}
              <div class="h24"></div>
{odeme_alani()}
              <div class="h24"></div>
{not_alani("Yeni telefon, 12 taksit" if taksit else "Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü")}
              <div class="h24"></div>
              <div class="t-cap">9 Eylül · 21.32 eklendi</div>
              <div class="h24"></div>
{alt_eylem(durum, sil_basili=(durum == "sil-basili"), taksit=taksit)}'''
    return sheet(ic)


def bulunamadi():
    ic = f'''              <div class="kolon orta">
                <div class="hata-daire">{icon("list-x")}</div>
                <div class="h12"></div>
                <div class="t-h2">Bu kayıt bulunamadı</div>
                <div class="h8"></div>
                <div class="t-body" style="text-align:center">Silinmiş olabilir. Listeye dönebilirsin.</div>
                <div class="h12"></div>
                <button class="btn-primary">Listeye dön</button>
              </div>
              <div class="h24"></div>'''
    return sheet(ic)


# ------------------------------------ silinen tek harcama → geri al toast'ı
# K-029: tek harcama silmede onay diyaloğu YOKTUR. Kayıt anında gider,
# üstte 6 sn duran geri al toast'ı çıkar. 640 ₺ silinince 9 Eylül limit
# içine döner — gün başlığı amber "limit dışı" etiketini bırakır. Silmenin
# sonucu anlatılmaz, GÖSTERİLİR.
def silindi_toast():
    return f'''          <div class="h8"></div>
          <div class="pad">
            <div class="toast">
              <div class="nokta" style="background-color:var(--danger)"></div>
              <div class="w12"></div>
              <div class="esnek t-body">Harcama silindi</div>
              <div class="w12"></div>
              <button class="btn-ghost" style="padding:0 16px;height:44px;flex:0 0 auto">Geri al</button>
            </div>
          </div>
          <div class="h12"></div>
          <div class="ekran-basi">
            <div class="t-h1">Kayıtlar</div>
            <button class="ikon-btn" aria-label="Taksitli işlemleri aç">{icon("repeat")}</button>
          </div>
{ay_secici("Eylül 2026", "47 kayıt · 11.840 ₺")}
          <div class="h24"></div>
{gun_basligi("Bugün · 10 Eylül", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Kafe", "08.20 · Nakit", "95 ₺")}
            <div class="h8"></div>
            {satir("Ulaşım", "09.05 · Kart", "42 ₺")}
          </div>
          <div class="h24"></div>
{gun_basligi("Dün · 9 Eylül", "Günlük toplam 180 ₺")}
          <div class="h8"></div>
          <div class="pad kolon">
            {satir("Market", "11.20 · Kart", "180 ₺")}
          </div>
          <div class="h24"></div>'''


# ------------------------------- E-13 · taksit serisi silme onayı (dialog)
# K-029: bu diyalog artık YALNIZ taksit serisi silmede açılır.
def onay(durum="aktif"):
    if durum == "loading":
        sil = ('<button class="btn-danger basili" disabled aria-disabled="true">Siliniyor'
               '<div class="w8"></div><div class="spinner"></div></button>')
    elif durum == "basili":
        sil = '<button class="btn-danger basili">Sil</button>'
    else:
        sil = '<button class="btn-danger">Sil</button>'
    return f'''          <div class="katman-ust" style="justify-content:center">
            <div class="scrim-kat"></div>
            <div class="scrim-kat" style="flex:0 0 auto;padding:16px">
              <div class="dialog kart-ic kolon">
                <div class="ikon-kab-danger">{icon("trash-2")}</div>
                <div class="h12"></div>
                <div class="t-h2">Bu taksit serisi silinecek</div>
                <div class="h8"></div>
                <div class="t-body">Kalan 9 taksit de silinecek. Geri alınamaz.</div>
                <div class="h12"></div>
                {satir("Diğer", "12 Haziran · Kart · 3/12 taksit", "1.040,00 ₺")}
                <div class="h12"></div>
                {sil}
                <div class="h8"></div>
                <button class="btn-ghost" style="width:100%">Vazgeç</button>
              </div>
            </div>
            <div class="scrim-kat"></div>
          </div>
'''


units = "".join([
    device("HARCAMA DETAYI", "E-12 · dolu", arka(), sabit_alt=detay(), note=
           "<b>Arketip B — Detail.</b> Sheet ekranın tamamını kaplamaz: arkadaki satır (basılı durumda) "
           "görünür kalır, kullanıcı nereden geldiğini bilir. <b>Sekme çubuğu düşer.</b> Tutar kuyusu "
           "E-11'in aynısıdır ama <code>display</code> (32pt) ölçüsünde — 56pt kahraman rol bu yüzeyde "
           "kullanılmaz. <b>K-029:</b> \"Sil\" tek harcamayı <b>onay sormadan</b> siler; koruma onay "
           "diyaloğu değil, 6 sn'lik geri al toast'ıdır. Bu yüzden buton kırmızı değil, <code>ghost</code>."),
    device("HARCAMA DETAYI", "E-12 · Sil → geri al toast'ı", silindi_toast(), sabit_alt=sekme_cubugu("kayitlar"), note=
           "<b>K-029 · tek harcama silme.</b> Ara ekran yok: kayıt gider, liste kapanır, üstte "
           "<b>6 sn</b> duran toast belirir. Pencere toast'ın ömrüyle birebir aynıdır — düğme kaybolduğu an "
           "silme kalıcıdır, görünmeyen geri alma süresi yoktur. Silmenin sonucu <b>anlatılmıyor, "
           "gösteriliyor</b>: 640 ₺ gidince 9 Eylül limit içine döndü, gün başlığındaki amber \"limit dışı\" "
           "etiketi kendiliğinden düştü, ay özeti 48 → 47 kayda indi."),
    device("HARCAMA DETAYI", "E-12 · taksitli kayıt", arka(), sabit_alt=detay(taksit=True), note=
           "<b>Taksitli kayıt:</b> tutar alanı <b>aylık</b> taksiti gösterir, toplam değil. Mavi bilgi şeridi "
           "iki satırdır: ne olduğu + sonucu. Silme butonu burada <b>Kaydet'in yanından alınıp kendi "
           "satırına</b> konur ve adı \"Taksit serisini sil\" olur — ağır eylem, yanlışlıkla basılacak "
           "yerde durmaz ve ne sildiğini adıyla söyler."),
    device("HARCAMA DETAYI", "E-12 · Kaydet loading", arka(), sabit_alt=detay(durum="loading"), note=
           "<b>Kaydediliyor:</b> buton genişliği sabit, metin \"Kaydediliyor\", sağda 20pt spinner, buton "
           "pasif. Sheet kapanmaz, alanlar yerinde kalır — yazma başarısız olursa kullanıcı verisini "
           "kaybetmez. Opaklıkla pasiflik yok."),
    device("HARCAMA DETAYI", "E-12 · kayıt bulunamadı", arka(), sabit_alt=bulunamadi(), note=
           "<b>Kayıt bulunamadı:</b> aynı oturumda silinmiş olabilir. Sheet kapanıp kullanıcıyı şaşırtmak "
           "yerine <b>ne olduğunu ve çıkışı</b> gösterir. İllüstrasyon E-14'ün hata dairesiyle aynı kaptır, "
           "ikon farklıdır — aile aynı, mesaj farklı."),
    device("TAKSİT SERİSİ SİLME", "E-13 · onay", arka(), sabit_alt=onay(), note=
           "<b>Kırmızının izinli dört bağlamından biri.</b> K-029 sonrası <code>danger #DC2626</code> tüm üründe "
           "yalnız şu dörtte görünür: <b>E-13 taksit serisi</b> onayı (bu yüzey) · <b>E-19 tüm veriyi silme</b> "
           "onayı · form hatası kenarlığı · silme toast'ının 8pt göstergesi. Onayla durdurmayı hak eden tek "
           "tek-harcama-dışı silme budur: aylara yayılmış <b>9 kayıt birden</b> gider ve geri alınamaz. Gövdenin ilk cümlesi "
           "kullanıcının beklemediği sonuçtur, sayı verilir (\"9 taksit\") çünkü belirsizlik korkutur."),
    device("TAKSİT SERİSİ SİLME", "E-13 · Sil loading", arka(), sabit_alt=onay(durum="loading"), note=
           "<b>Siliniyor:</b> buton pasif + spinner. İşlem başladıysa geri alınmaz; bu yüzden 250ms'den kısa "
           "sürer ve diyalog kendiliğinden kapanır. Tam ekran kaplayan spinner yoktur. Bu akışta geri al "
           "toast'ı <b>yoktur</b> — koruma önceden, onayla alınmıştır."),
])

OUT.write_text(page(
    "Trinkow · Harcama detayı + taksit serisi silme — prototip v4",
    "E-12 · Harcama detayı  ·  E-13 · Taksit serisi silme onayı",
    "Arketip B — Detail · sheet + dialog · K-029: tek harcama onaysız + geri al, taksit serisi onaylı · 390×844",
    units), encoding="utf-8")
print("yazıldı:", OUT)
