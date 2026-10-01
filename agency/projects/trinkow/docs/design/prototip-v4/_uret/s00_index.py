# -*- coding: utf-8 -*-
"""Prototip dizini. Ölü bağlantı kalmasın diye ekranlarla birlikte güncellenir."""
import pathlib
KOK = pathlib.Path(__file__).parent.parent

EKRANLAR = [
    ("01-gunluk.html", "01", "Günlük (tarih sayfalanabilir)", "E-10 · 12 durum: bugün · kaydırma ipucu · <b>milestone kutlaması</b> · limit dışı · dün · eski gün · geriye sınır · harcamasız gün · limitsiz · boş · yükleniyor · hata"),
    ("02-harcama-ekle.html", "02", "Harcama ekle", "E-11 · 17 durum: açılış + son kullandıkların · 3 dokunuşta tamam · <b>ürün arama</b> (kendi geçmişi + katalog) · marka adı kullanıcıdan · eşleşme yok → <b>kendi kalemini ekle</b> · geçmişten seçildi (tutar doldu) · katalogdan seçildi (<b>tutar boş — fiyat uydurulmaz</b>) · \"geçen sefer\" önerisi · kategori seçici · nakit · <b>taksit açık</b> · <b>geçmiş güne ekleme</b> · hata · uzun içerik · limit dışı + kaydediliyor · arama yükleniyor · kayıt yazılamadı"),
    ("03-onboarding.html", "03", "Onboarding · Katman 1 (3 soru)", "E-01…E-03 · 6 durum: niyet · aylık gelir (girildi) · gelir boş + <b>Atla basılı</b> · maaş günü · düzensiz gelir · <b>günlük limit önerisi</b> (K-059/5 · tek dokunuşla onay)"),
    ("04-kayitlar.html", "04", "Kayıtlar", "E-14 · 6 durum: dolu + uzun tutar · 214 kayıt (FlatList) · boş · ay boş · yükleniyor · okuma hatası"),
    ("05-ozet.html", "05", "Özet", "E-16 · 5 durum: dolu · hafta ortası · tüm hafta limit dışı · boş · yükleniyor"),
    ("06-harcama-detay.html", "06", "Harcama detayı + taksit serisi silme", "E-12 / E-13 · 7 durum: detay · sil → geri al toast'ı (K-029) · taksitli · kaydediliyor · bulunamadı · seri silme onayı · siliniyor"),
    ("07-acilis.html", "07", "Açılış (splash)", "E-00 · marka adı + monogram · animasyonsuz · uygulama ikonu önizlemesi"),
    ("08-kategori-detay.html", "08", "Kategori detayı", "E-15 · 5 durum: dolu (limit var) · limit yok · limit aşıldı · boş · yükleniyor"),
    ("09-limitler.html", "09", "Limitler", "E-17 · 8 durum: düzenleme · <b>kategori limiti hiç yok</b> · kil tuş takımı · geçersiz değer · kaydediliyor · limit kaldırma · kaldırıldı + geri al · yükleniyor"),
    ("10-taksitler.html", "10", "Taksitler", "E-18 · 4 durum: yük haritası · seri bitti · boş · yükleniyor"),
    ("11-ayarlar.html", "11", "Ayarlar (+ Hesap bölümü)", "E-19 · 4 durum: dolu + <b>oturum açık Hesap</b> · bildirim izni kapalı + <b>oturum kapalı Hesap</b> · tüm verileri sil onayı · <b>hesabı sil onayı</b>"),
    ("12-profilleme.html", "12", "Profilleme sorusu", "E-20 · 3 durum: 2. gün <b>bekleyen kart (yatırım)</b> · 3. gün taksit (seçim basılı) · cevaptan sonra panoda ne değişti"),
    ("13-seri.html", "13", "Seri (streak)", "E-21 · 5 durum: aktif seri · <b>seri kırıldı</b> · seri kapalı (limitsiz) · boş · yükleniyor"),
    ("14-gun-secici.html", "14", "Gün seçici (ay ızgarası)", "E-24 · 5 durum: Eylül (bugün işaretli · sonraki ay yok) · gün kutusu basılı · <b>başlangıç ayı (geriye sınır)</b> · boş ay · yükleniyor"),
    ("15-giris.html", "15", "Oturum aç", "E-22 · 8 durum: boş · yazılıyor (klavye açık, şifre görünür) · geçersiz e-posta · şifre yanlış · gönderiliyor · ağ hatası · <b>Android: yalnız Google</b> · şifre bağlantısı gönderildi"),
    ("16-kayit.html", "16", "Hesap oluştur", "E-23 · 7 durum: boş · kural karşılanmadı (klavye açık) · kural karşılandı + şifre görünür · e-posta zaten kayıtlı · gönderiliyor · <b>Android: yalnız Google</b> · ağ hatası"),
    ("17-tanisma.html", "17", "Seni tanıyalım · Katman 2", "E-25 · 12 durum: kapı · sabit giderler (boş · klavye · dolu) · kahve · serbest sayı · sigara \"Hiç\" · dışarıda yemek · yatırım niyeti · birikim kaydırıcısı · <b>üst sınır kilidi</b> · yarıda bıraktı"),
    ("18-plan.html", "18", "Planın hazır", "E-26 · 7 durum: normal · <b>kaydırıcı + %100 kilidi</b> · nasıl hesaplandı · gelir yok (elle limit) · <b>sabit giderler gelirden büyük</b> · Katman 2 yarım · yükleniyor"),
]

kartlar = "\n".join(f'''    <a class="dizin-kart" href="{d}">
      <div class="dizin-no">{n}</div>
      <div class="dizin-govde">
        <div class="ad">{ad}</div>
        <div class="alt">{alt}</div>
      </div>
    </a>
''' for d, n, ad, alt in EKRANLAR if (KOK / d).exists())

yok = [ad for d, n, ad, alt in EKRANLAR if not (KOK / d).exists()]
eksik = ("<br /><br /><b>Bu turda çizilmedi:</b> " + ", ".join(yok) + ".") if yok else ""

HTML = f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Trinkow · Prototip v4 (Claymorphism)</title>
<link rel="stylesheet" href="stil.css" />
<style>
  .dizin {{ max-width: 880px; margin: 0 auto; }}
  .dizin-kart {{ display: flex; flex-direction: row; align-items: center; padding: 20px 24px;
    border-radius: 24px; background-color: #FFFFFF; background-image: var(--clay-face);
    box-shadow: var(--clay-raised); text-decoration: none; color: var(--text); margin-bottom: 16px; }}
  .dizin-no {{ width: 56px; height: 56px; border-radius: 16px; background-color: var(--primary-soft);
    box-shadow: var(--clay-sunken); display: flex; align-items: center; justify-content: center;
    font-family: 'Montserrat'; font-weight: 700; font-size: 19px; color: var(--primary-text); }}
  .dizin-govde {{ flex: 1 1 auto; margin-left: 16px; }}
  .dizin-govde .ad {{ font-family: 'Poppins'; font-weight: 600; font-size: 19px; letter-spacing: -0.3px; }}
  .dizin-govde .alt {{ font-size: 13px; color: var(--text-2); margin-top: 4px; }}
  .bilgi {{ border-radius: 24px; background-color: rgba(255,255,255,0.66); padding: 20px 24px; margin-top: 32px; font-size: 13px; line-height: 1.6; color: var(--text-2); }}
  .bilgi b {{ color: var(--text); }}
  .bilgi ul {{ margin: 8px 0 0; padding-left: 18px; }}
  .bilgi code {{ font-family: 'Montserrat'; font-weight: 600; color: var(--primary-text); }}
</style>
</head>
<body>
  <div class="dizin">
    <div class="sayfa-basligi">
      <h1>Trinkow · Prototip v4</h1>
      <p>Claymorphism · Faz 1 · 390×844 · v3 üzerine <b>Günlük (E-10 revizyonu)</b> ve <b>Seri (E-21)</b> eklendi. Görsel otorite:
      <code>vendor/design-systems/library/claymorphism/DESIGN.md</code> ·
      Token: <code>projects/trinkow/docs/brand/tokens.md</code> v3.1</p>
    </div>

{kartlar}
    <div class="bilgi">
      <b>Nasıl açılır:</b> bu dosyayı tarayıcıda aç
      (<code>projects/trinkow/docs/design/prototip-v4/index.html</code>). Fontlar
      <code>fonts/</code> klasöründen gömülü gelir, internet gerekmez.
      <br /><br />
      <b>T-3 · profilleme ve plan (K-053):</b> onboarding <b>iki katmana</b> ayrıldı. Katman 1
      <b>üç soruda</b> kapanır (niyet · aylık gelir <b>atlanabilir</b> · maaş günü) ve uygulama o an
      çalışır. Katman 2 <b>\"Seni tanıyalım\"</b> sekiz karttır, <b>her kartı atlanabilir</b>, her an
      bırakılıp kaldığı yerden sürer, ayarlardaki <b>Plan ve profil</b> bölümünden tamamlanır.
      Çıktı <b>Planın hazır</b> (E-26): zorunlu · sosyal-keyfi · birikim dağılımı ₺ ve %, ve
      <b>günlük limit oradan türetilir</b> (sosyal-keyfi payı ÷ dönemde kalan gün). Fiyatlar
      kullanıcıdan gelir, biz tahmin etmeyiz (K-050); <b>yatırım tavsiyesi yoktur</b> (K-053) —
      yalnız \"yatırım payı\" etiketi. Kimlik doğrulama sözcüğü artık <b>\"Oturum aç\"</b> (K-057/6);
      \"giriş\" yalnız veri girmek için kullanılır.
      <br /><br />
      <b>T-4 · ürün arama ve limit önerisi:</b> harcama eklemeye <b>ürün arama</b> girdi (K-050).
      Katalog yereldir, uygulamayla gelir ve <b>fiyat GÖSTERMEZ</b> — tek izinli fiyat bilgisi
      kullanıcının kendi son tutarıdır (\"geçen sefer 95 ₺\") ve tek dokunuşla kabul edilir.
      Ürün seçmek <b>zorunlu değildir</b>: tutar + kategori çipi ile iki adımlık yol her yüzeyde
      açık kalır. Eşleşme yoksa çıkmaz sokak yok, kullanıcı <b>kendi kalemini</b> ekler.
      Onboarding'in çıkışına <b>günlük limit önerisi</b> eklendi (K-059/5): gelir girildiyse
      belgelenmiş varsayılan dağılımdan (%50 zorunlu · %30 sosyal ve keyfi · %20 birikim) bir
      limit <b>önerilir</b> ve tek dokunuşla onaylanır; hesap ekranda yazılıdır, sayının yanında
      <b>\"Öneri\" pulu</b> durur, reddedip <b>limitsiz</b> devam etmek her zaman mümkündür.
      Gerekçe: limitsiz kipte seri çalışmaz (K-048), yani Katman 2'yi atlayan kullanıcı
      oyunlaştırmayı hiç görmezdi.
      <br /><br />
      <b>T-5 · denetim düzeltmeleri (K-061):</b> üç bloklayıcı kapandı.
      (1) <b>Kontrast:</b> dolu gün kutusundan ve seri durağından gradyan kalktı;
      44pt kutunun içindeki beyaz sayı artık düz <code>primary-deep</code> üstünde
      duruyor — ölçülen <b>5.37:1</b> (gradyan ortasında 4.43 idi, AA altı).
      Hacim gradyandan değil, kil gölgesinden geliyor.
      (2) <b>Tek seçim dili:</b> seçim kartından halka kaldırıldı. Bu üründe seçim
      halkayla anlatılmaz (K-040 → K-045 → K-054/6): <b>seçimde derinlik</b>
      (<code>primary-soft</code> + <code>clay.sunken</code> + ikonun tersine kabarması),
      <b>gün ızgarasında dolgu</b>. İki dil, iki ayrı iş.
      (3) <b>Gelir bir kez sorulur:</b> E-20'nin \"aylık gelir aralığı\" sorusu emekliye
      ayrıldı; gelir yalnız E-02'de <b>tam tutar</b> olarak alınır (plan formülleri tam tutar
      ister). E-20 artık E-25'in <b>cevaplanmamış kartlarından birini</b> soruyor.
      <br /><br />
      <b>Kapsam:</b> v4'te en sol sekme <b>Günlük</b> oldu (K-049); <b>Seri</b> (K-048),
      <b>Gün seçici</b> (K-049) ve <b>Oturum aç / Hesap oluştur</b> (K-052) ekranları eklendi.
      Ayarlara <b>Hesap</b> bölümü girdi (çıkış yap · hesabı sil). Sekme sayısı 3'te kaldı.
      Karanlık mod Faz 2'ye bırakıldı, tokenı üretilmedi.
      <br /><br />
      <b>Hesap ne değildir:</b> harcama verisi cihazda kalır, sunucuya senkron yoktur (K-052);
      hesap yalnız kimlik içindir ve <b>oturum duvarı yoktur</b> — \"Hesapsız devam et\" her iki
      ekranda görünür bir çıkıştır. Apple/Google düğmelerinin dolgusu, logosu ve etiketi
      sahibinin marka kılavuzundan gelir; kap (56pt, radius 999, clay) bizimdir.
      <b>Sağlayıcı kümesi platforma göre değişir:</b> iOS'ta Apple + Google, Android'de
      yalnız Google + e-posta/şifre. Apple'la açılmış hesap Android'de \"Şifremi unuttum\"
      yolundan açılır.{eksik}
      <br /><br />
      <b>İki bölge kuralı</b> (<code>reference/open-design-entegrasyon.md</code>):
      <ul>
        <li><b>Çerçeve/kabuk</b> (telefon gövdesi, Dynamic Island, durum çubuğu, sayfa zemini,
        bu dizin sayfası) React Native'e kodlanmaz — CSS serbest.</li>
        <li><b>&lt;main class="content"&gt; içi</b> birebir RN'e kodlanır: yalnız flexbox.
        Denetim taraması bu blokta yapılır (<code>python3 _uret/denetim.py</code>).
        T-5'ten sonra betik <b><code>stil.css</code>'i de tarıyor</b>: palet dışı hex ve
        izinsiz radius, ölçüt <code>brand/tokens.md</code>. Üç yazılı istisna
        (<code>@denetim-disi</code>) var ve gerekçeleri CSS'in içindedir: kabuk,
        sistem klavyesi, üçüncü taraf marka düğmeleri.</li>
      </ul>
      <br />
      <b>Üretim:</b> ekran HTML'leri <code>_uret/*.py</code> ile üretilir
      (<code>python3 _uret/s09_limitler.py</code>). Elle düzenlemek yerine script güncellenir.
    </div>
  </div>
</body>
</html>
'''
(KOK / "index.html").write_text(HTML, encoding="utf-8")
print("yazıldı:", KOK / "index.html")
