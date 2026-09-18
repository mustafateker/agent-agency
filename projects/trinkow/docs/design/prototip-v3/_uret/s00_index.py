# -*- coding: utf-8 -*-
"""Prototip dizini. Ölü bağlantı kalmasın diye ekranlarla birlikte güncellenir."""
import pathlib
KOK = pathlib.Path(__file__).parent.parent

EKRANLAR = [
    ("01-bugun.html", "01", "Bugün (pano)", "E-10 · 6 durum: limit altı · limit dışı + uzun metin · <b>limitsiz (yay yok)</b> · boş · yükleniyor · hata + toast"),
    ("02-harcama-ekle.html", "02", "Harcama ekle", "E-11 · 11 durum: açılış · 3 dokunuş tamam · ürün adı yazılıyor (2) · eşleşme yok · öneri seçildi · kategori seçici · <b>taksit açık</b> · hata · en uzun tutar · limit dışı + kaydediliyor"),
    ("03-onboarding.html", "03", "Onboarding (3 adım)", "E-01…E-03 · 3 adım: niyet · günlük limit · kipe bağlı soru + kurulum özeti"),
    ("04-kayitlar.html", "04", "Kayıtlar", "E-14 · 6 durum: dolu + uzun tutar · 214 kayıt (FlatList) · boş · ay boş · yükleniyor · okuma hatası"),
    ("05-ozet.html", "05", "Özet", "E-16 · 5 durum: dolu · hafta ortası · tüm hafta limit dışı · boş · yükleniyor"),
    ("06-harcama-detay.html", "06", "Harcama detayı + taksit serisi silme", "E-12 / E-13 · 7 durum: detay · sil → geri al toast'ı (K-029) · taksitli · kaydediliyor · bulunamadı · seri silme onayı · siliniyor"),
    ("07-acilis.html", "07", "Açılış (splash)", "E-00 · marka adı + monogram · animasyonsuz · uygulama ikonu önizlemesi"),
    ("08-kategori-detay.html", "08", "Kategori detayı", "E-15 · 5 durum: dolu (limit var) · limit yok · limit aşıldı · boş · yükleniyor"),
    ("09-limitler.html", "09", "Limitler", "E-17 · 8 durum: düzenleme · <b>kategori limiti hiç yok</b> · kil tuş takımı · geçersiz değer · kaydediliyor · limit kaldırma · kaldırıldı + geri al · yükleniyor"),
    ("10-taksitler.html", "10", "Taksitler", "E-18 · 4 durum: yük haritası · seri bitti · boş · yükleniyor"),
    ("11-ayarlar.html", "11", "Ayarlar", "E-19 · 3 durum: dolu · bildirim izni kapalı · tüm verileri sil onayı"),
    ("12-profilleme.html", "12", "Profilleme sorusu", "E-20 · 3 durum: 2. gün gelir · 3. gün taksit (seçim basılı) · cevaptan sonra panoda ne değişti"),
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
<title>Trinkow · Prototip v3 (Claymorphism)</title>
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
      <h1>Trinkow · Prototip v3</h1>
      <p>Claymorphism · Faz 1 · 390×844 · on iki sayfa, 62 durum. Görsel otorite:
      <code>agency/vendor/design-systems/library/claymorphism/DESIGN.md</code> ·
      Token: <code>projects/trinkow/docs/brand/tokens.md</code> v3.1</p>
    </div>

{kartlar}
    <div class="bilgi">
      <b>Nasıl açılır:</b> bu dosyayı tarayıcıda aç
      (<code>projects/trinkow/docs/design/prototip-v3/index.html</code>). Fontlar
      <code>fonts/</code> klasöründen gömülü gelir, internet gerekmez.
      <br /><br />
      <b>Kapsam:</b> Faz 1'in <b>15 yüzeyinin tamamı</b> çizildi (E-00…E-20),
      toplam <b>62 durum</b>. Karanlık mod Faz 2'ye bırakıldı, tokenı üretilmedi.{eksik}
      <br /><br />
      <b>İki bölge kuralı</b> (<code>agency/reference/open-design-entegrasyon.md</code>):
      <ul>
        <li><b>Çerçeve/kabuk</b> (telefon gövdesi, Dynamic Island, durum çubuğu, sayfa zemini,
        bu dizin sayfası) React Native'e kodlanmaz — CSS serbest.</li>
        <li><b>&lt;main class="content"&gt; içi</b> birebir RN'e kodlanır: yalnız flexbox.
        Denetim taraması bu blokta yapılır (<code>python3 _uret/denetim.py</code>).</li>
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
