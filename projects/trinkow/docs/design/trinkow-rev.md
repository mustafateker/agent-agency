# Trinkow Rev — uygulama delta sözleşmesi

23 Eylül 2026. Mustafa'nın revizyon kapsamı; görsel temel onaylı v4 claymorphism. `trinkow-rev.html` 390×844 örnek ekranları içerir. Yeni görsel yön, font, bağımlılık veya renk yok. Para ve tasarruf değerleri örnek veridir; üretimde backend sözleşmesi otoritedir.

## Ortak temel

- Zemin `bg`, yüzey `surface`, giriş `well`; metin `text`/`text-2`. Birincil düğme düz `primary-deep`; basılı `primary-press`. Limit aşımı `warning-ink`; kırmızı yalnız hesap/veri silme.
- Mevcut Poppins başlık (26/32, 19/25), Montserrat gövde (16/24), açıklama (13/18), tutar (17/24) rollerini kullan. Aralıklar 4/8/12/16/24/32; kart içi 24, ekran kenarı 24; radius mevcut 16/24/32 ailesi.
- Safe area üst/alt; 48 pt minimum hedef. Dinamik yazı boyutunda kartlar büyür, para satırı sarılabilir; hiçbir açıklama tek satıra zorlanmaz. Tek tema açık; hareket gerekmiyor.
- Alt çubuk `Günlük / Tasarruf / Profil`; mevcut harcama ekleme düğmesi korunur. Profil, hesap ve uygulama ayarlarının girişidir. Eski `/kayitlar` Tasarruflar ekranına yönlenir.

## Ekranlar ve davranışlar

**Tasarruflar:** Ay gezinmesi → harcanabilir gelir → harcanan → kalan/harcanmayan → hesaplanan tasarruf → alışkanlık farkları → motivasyon. Kalan tutar henüz harcanabilecek gelir; alışkanlık tasarrufu ayrı gösterilir, toplama tekrar eklenmez. Banka bakiyesi/gerçek transfer izlenmediğinden hesaplanan tasarruf kartında `Kaydettiğin gelir ve harcamalara göre` açıklaması bulunur. Eksik veri sıfır tasarruf olarak sunulmaz. Aktif ay `Ay devam ediyor` etiketi taşır. Kategori kartında rutin beklentisi, gerçekleşen harcama ve fark ayrı satırlardır; aşım amber metinle görünür. Borç varsa `Bu tutar borcunun %…'sine denk geliyor`; borç yoksa `Bu tutarı birikim hedefin için ayırmayı düşünebilirsin.` Gerçek ödeme/yatırım getirisi vaadi yok. Özet aynı API verisini daha kısa kartla kullanır.

**Günlük kategoriler:** Market, Sağlık, Kafe, Restoran, Ulaşım, Akaryakıt, Eğlence, Giyim, Alışkanlıklar ve Diğer hızlı ekleme listesinde kalır. Abonelik, Fatura ve Kira/Ev planlı ödeme alanına ayrılır. Günün harcamaları ürün adı, saat ve tutarla ilgili günlük kategorinin altında görünür; satırdaki `+` aynı kategori seçili harcama formunu açar.

**Onboarding eylemleri:** Amaç ve maaş/aylık plan adımları `Sonraki` ile ilerler. Rutin adımı hazır rutin kısayolları göstermeden doğrudan ekleme formunu açar. Kurulum sırasında eklenen rutin kartında yalnız `Düzenle` ve `Rutini kaldır` bulunur; harcama/vazgeçme günlük eylemleri kurulum akışına girmez.

**Native para girişi:** `AmountWell` gerçek `TextInput` olur. Harcama ekle/detay, onboarding, tanışma, ayarlar, plan, limitlerin tamamında özel keypad kaldırılır. Decimal klavye; virgül/nokta, yapıştırma, iki kuruş hanesi; veri integer kuruş. Form ScrollView ve keyboard avoidance ile girdiyi/ana düğmeyi görünür tutar. Sheet de klavyeye göre yükselir. `Bitti` klavyeyi kapatır; `Kaydet` tek asenkron işlem yapar. Favori → Kaydet iki dokunuş; fiyat değişikliği ayrıca bir focus ve native yazım gerektirir.

**Sık kullanılanlar:** Harcama formu başında kategori ve son fiyatı gösteren ürün çipleri. Seçim ürün+kategori+tutarı taslağa doldurur; kullanıcı tutarı değiştirir, Kaydetmeden kayıt yaratılmaz. Kategori altından `Ürün ekle` ve ürün yanındaki `+` aynı formu açar. Fiyat etiketi `Son fiyat`; yeni ücret ancak başarılı kayıttan sonra güncellenir. Ürün adı+kategori kimliği birlikte kullanılır.

**Onboarding rutinler:** Gelir adımından sonra `Günlük rutin harcamaların neler?`; kahve, sigara, yemek, ulaşım, atıştırmalık ve `Kendim ekleyeyim`. Çoklu seçim; seçili kalem altında günlük adet ve birim fiyat native girdileri. `Rutin harcamam yok` ile bilinçli atlama; ilerleme seçilmiş kalemlerin geçerli fiyat/adediyle açılır. Geri dönmek girdiyi silmez. Mevcut kullanıcı Ayarlar → Rutinlerim üzerinden tamamlar/düzenler.

**Auth:** Eposta/şifre → Beni hatırla ve Şifremi unuttum → Giriş yap → Hesap oluştur → ayırıcı → Apple/Google. Kayıtta da sosyal seçenekler altta. Apple yalnız iOS; mevcut platform kuralı sürer. Meşgul düğme tekrar tıklanamaz; alan hataları altında, ağ hatası üst bilgi alanında görünür. Şifre sıfırlamada adresin kayıtlı olduğunu açıklamayan başarı metni kullanılır.

**Ayarlar:** Hesap (eposta, parola, çıkış), Bütçe ve rutinler (gelir, sabit gider, borç, limit, rutinler), Tercihler (bildirim, gün sınırı, ödeme), Yardım/SSS, Legal (kullanım şartları, gizlilik, KVKK aydınlatma), Uygulama bilgisi. Hesap silme ayrı ekran: sonuç açıklaması, iptal, son silme eylemi ve sunucu hatası. Legal sayfalar sürüm/tarih içerir; geçici metin nihai belge diye sunulmaz. Yardım metinleri uygulama içinde çalışır. Destek adresi mevcut değilse uydurulmaz. Ayar verisi yüklenemese bile çıkış ve legal bağlantılar erişilebilir kalır.

## Durum sözleşmesi ve kabul

- Yükleniyor: tutar yerine çizgi ve `Hesaplanıyor`; eski hesap verisi başka kullanıcıya gösterilmez. Bir işlem boyunca ilgili düğme pasif ve metni `Kaydediliyor…`.
- Boş: `İlk ayını birlikte oluşturalım` + gelir/rutin tamamlamaya yönlendirme; uydurma yüzde/grafik yok.
- Hata: mevcut girdiler korunur, `Bilgiler yüklenemedi` + `Yeniden dene`; ağ hatası başarı veya sıfır toplam olarak gösterilmez.
- Basılı: yüzeylerde `groove` + mevcut pressed gölge, ana düğmede `primary-press`; pasif `disabled-bg`/`text-2`. Focus görünür, erişilebilir label/state zorunlu.
- QA: yedi para formunda gerçek klavye/focus ve Kaydet görünürlüğü; küçük ekran/büyük yazı; aynı ad farklı kategori favorileri; fiyat düzenleme; geçmiş ay/gün geçişi; hesaplar arası veri izolasyonu; legal/çıkışın ağ hatasında erişimi.

## Öz denetim

Mevcut token paleti ve gömülü fontlar kullanıldı; emoji, kart üçlemesi, yeni ikon ailesi ve dekoratif gradyan metni yok. Prototip içerik düzeni flex; işletim sistemi klavyesi yeniden çizilmedi. Boş/yükleniyor/hata/meşgul/basılı örnekleri dahil. Prototip örnekleri backend hesap formülünün yerine geçmez. Tasarım incelemesi root üzerinden istenir; bu belge PASS iddiası taşımaz.
