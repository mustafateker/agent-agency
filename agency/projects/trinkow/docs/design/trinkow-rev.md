# Trinkow Rev — uygulama delta sözleşmesi

> ⚠ **TARİHSEL BELGE.** Bu belge **23 Eylül 2026 Rev turunu** anlatır ve
> bütünüyle geçerli değildir. REV2 (24-25 Eylül 2026) ile değişen maddeler
> için otorite şunlardır: `projects/trinkow/docs/design/rev2-onboarding-kayit.md`
> (kurulum 1-4 + hesap oluştur) ve
> `projects/trinkow/docs/design/rev2-tasarruf-profil.md` (Tasarruf · Profil ·
> canlılık reçetesi). Aşağıdaki satırlardan REV2'de geçersiz kalanlar
> "(REV2: …)" notuyla işaretlendi; not taşımayan satırlar Rev turunun
> kaydıdır ve yeni iş için ölçü kaynağı olarak kullanılmaz — ölçü otoritesi
> `projects/trinkow/docs/brand/tokens.md` v4'tür.

23 Eylül 2026. Mustafa'nın revizyon kapsamı; görsel temel onaylı v4 claymorphism. `trinkow-rev.html` 390×844 örnek ekranları içerir. Yeni görsel yön, font, bağımlılık veya renk yok. Para ve tasarruf değerleri örnek veridir; üretimde backend sözleşmesi otoritedir.

## Ortak temel

- Zemin `bg`, yüzey `surface`, giriş `well`; metin `text`/`text-2`. Birincil düğme düz `primary-deep`; basılı `primary-press`. Limit aşımı `warning-ink`; kırmızı yalnız hesap/veri silme.
- Mevcut Poppins başlık (26/32, 19/25), Montserrat gövde (16/24), açıklama (13/18), tutar (17/24) rollerini kullan. Aralıklar 4/8/12/16/24/32; **kart içi 16, ekran kenarı 16** (REV2 düzeltmesi: bu belgedeki 24/24 yanlıştı, geçerli değer `tokens.md` §3.1'dir — kart iç boşluğu istisnasız 16, ekran yatay kenarı 16); radius mevcut 16/24/32 ailesi.
- Safe area üst/alt; 48 pt minimum hedef. Dinamik yazı boyutunda kartlar büyür, para satırı sarılabilir; hiçbir açıklama tek satıra zorlanmaz. Tek tema açık; hareket gerekmiyor.
- Alt çubuk `Günlük / Tasarruf / Profil`; **çubuktaki büyük `+` (FAB) kaldırıldı** (REV2: üç sekme `space-around` ile eşit dağılır; harcama ekleme girişi Günlük'teki kategori satırının `+` düğmesidir — `rev2-tasarruf-profil.md` §1.1). Profil, hesap ve uygulama ayarlarının girişidir. Eski `/kayitlar` Tasarruflar ekranına yönlenir.

## Ekranlar ve davranışlar

**Tasarruflar:** Ay gezinmesi → harcanabilir gelir → harcanan → kalan/harcanmayan → hesaplanan tasarruf → alışkanlık farkları → motivasyon. Kalan tutar henüz harcanabilecek gelir; alışkanlık tasarrufu ayrı gösterilir, toplama tekrar eklenmez. Banka bakiyesi/gerçek transfer izlenmediğinden hesaplanan tasarruf kartında `Kaydettiğin gelir ve harcamalara göre` açıklaması bulunur. Eksik veri sıfır tasarruf olarak sunulmaz. Aktif ay `Ay devam ediyor` etiketi taşır. Kategori kartında rutin beklentisi, gerçekleşen harcama ve fark ayrı satırlardır; aşım amber metinle görünür. Borç varsa `Bu tutar borcunun %…'sine denk geliyor`; borç yoksa `Bu tutarı birikim hedefin için ayırmayı düşünebilirsin.` Gerçek ödeme/yatırım getirisi vaadi yok. Özet aynı API verisini daha kısa kartla kullanır.

**Günlük kategoriler:** Market, Sağlık, Kafe, Restoran, Ulaşım, Akaryakıt, Eğlence, Giyim, Alışkanlıklar ve Diğer hızlı ekleme listesinde kalır. Abonelik, Fatura ve Kira/Ev bütçenin sabit gider tarafında kalır *(REV2: harcama ekleme ekranındaki "önceden bütçeden ayrılan sabit ödeme" bölümü **tamamen kaldırıldı**; kategori de artık o ekranda seçilmez — route param'ından ya da seçilen üründen gelir ve salt okunur gösterge olarak durur)*. Günün harcamaları ürün adı, saat ve tutarla ilgili günlük kategorinin altında görünür; satırdaki `+` aynı kategori seçili harcama formunu açar.

**Onboarding eylemleri:** *(REV2: kurulum baştan yazıldı — dört adım `1/4 niyet · 2/4 gelir ve gider · 3/4 rutinler · 4/4 plan özeti`, kendi kabuğu `SetupShell` içinde; ayrı "maaş günü" adımı **yok** ve "maaş" sözcüğü kurulum ekranlarından çıktı; varsayılan niyet seçili gelmez; rutin girişi `RoutineSheet`'e taşındı. Bağlayıcı spesifikasyon: `rev2-onboarding-kayit.md` §2-§6.)* Amaç ve aylık plan adımları `Sonraki` ile ilerler. Kurulum sırasında eklenen rutin kartında yalnız `Düzenle` ve `Rutini kaldır` bulunur; harcama/vazgeçme günlük eylemleri kurulum akışına girmez.

**Native para girişi:** `AmountWell` gerçek `TextInput` olur (REV2'de de geçerli; kurulum ve sheet'lerin alan karşılıkları `MoneyField` / `MoneyRow`). Harcama ekle/detay, onboarding, tanışma, ayarlar, plan, limitlerin tamamında özel keypad kaldırılır. Decimal klavye; virgül/nokta, yapıştırma, iki kuruş hanesi; veri integer kuruş. Form ScrollView ve keyboard avoidance ile girdiyi/ana düğmeyi görünür tutar. Sheet de klavyeye göre yükselir. `Bitti` klavyeyi kapatır; `Kaydet` tek asenkron işlem yapar. Favori → Kaydet iki dokunuş; fiyat değişikliği ayrıca bir focus ve native yazım gerektirir.

**Sık kullanılanlar:** Harcama formu başında kategori ve son fiyatı gösteren ürün çipleri. Seçim ürün+kategori+tutarı taslağa doldurur; kullanıcı tutarı değiştirir, Kaydetmeden kayıt yaratılmaz. Kategori altından `Ürün ekle` ve ürün yanındaki `+` aynı formu açar. Fiyat etiketi `Son fiyat`; yeni ücret ancak başarılı kayıttan sonra güncellenir. Ürün adı+kategori kimliği birlikte kullanılır.

**Onboarding rutinler:** *(REV2: hazır kalem çipleri + çoklu seçim kalktı. Adım 3/4 `Günlük rutinlerin` başlığıyla açılır, boşken "Eklediğin rutinler burada sıralanır." der; ekleme `Rutin ekle` → `RoutineSheet` ile yapılır — ad · kategori çip şeridi · adet · birim fiyat + ayna kuyusu. Spesifikasyon: `rev2-onboarding-kayit.md` §5.)* `Rutin harcamam yok` ile bilinçli atlama korunur; geri dönmek girdiyi silmez. Mevcut kullanıcı Profil → Rutinler üzerinden tamamlar/düzenler.

**Auth:** Giriş ekranı: Eposta/şifre → Beni hatırla ve Şifremi unuttum → Giriş yap → Hesap oluştur → ayırıcı → Apple/Google. *(REV2: **kayıt ekranının sırası bu değil.** Geçerli sıra `rev2-onboarding-kayit.md` §7'dedir: e-posta → şifre → **şifre tekrar** → iki `Checkbox` yasal onay → ipucu satırı → iki 44pt `ghost` belge satırı → `ya da` → sosyal düğmeler → "Hesabın var mı / Oturum aç" → alt-sabit birincil `Hesap oluştur`. Mahremiyet bilgi şeridi kaldırıldı, `LegalConsentText` kullanımdan düştü.)* Apple yalnız iOS; mevcut platform kuralı sürer. Meşgul düğme tekrar tıklanamaz; alan hataları altında, ağ hatası üst bilgi alanında görünür. Şifre sıfırlamada adresin kayıtlı olduğunu açıklamayan başarı metni kullanılır.

**Ayarlar:** Hesap (eposta, parola, çıkış), Bütçe ve rutinler (gelir, sabit gider, borç, limit, rutinler), Tercihler (bildirim, gün sınırı, ödeme), Yardım/SSS, Legal (kullanım şartları, gizlilik, KVKK aydınlatma), Uygulama bilgisi. Hesap silme ayrı ekran: sonuç açıklaması, iptal, son silme eylemi ve sunucu hatası. Legal sayfalar sürüm/tarih içerir; geçici metin nihai belge diye sunulmaz. Yardım metinleri uygulama içinde çalışır. Destek adresi mevcut değilse uydurulmaz. Ayar verisi yüklenemese bile çıkış ve legal bağlantılar erişilebilir kalır.

## Durum sözleşmesi ve kabul

- Yükleniyor: tutar yerine çizgi ve `Hesaplanıyor`; eski hesap verisi başka kullanıcıya gösterilmez. Bir işlem boyunca ilgili düğme pasif ve metni `Kaydediliyor…`.
- Boş: `İlk ayını birlikte oluşturalım` + gelir/rutin tamamlamaya yönlendirme; uydurma yüzde/grafik yok.
- Hata: mevcut girdiler korunur, `Bilgiler yüklenemedi` + `Yeniden dene`; ağ hatası başarı veya sıfır toplam olarak gösterilmez.
- Basılı: yüzeylerde `groove` + mevcut pressed gölge, ana düğmede `primary-press`; pasif `disabled-bg`/`text-2`. Focus görünür, erişilebilir label/state zorunlu.
- QA: yedi para formunda gerçek klavye/focus ve Kaydet görünürlüğü; küçük ekran/büyük yazı; aynı ad farklı kategori favorileri; fiyat düzenleme; geçmiş ay/gün geçişi; hesaplar arası veri izolasyonu; legal/çıkışın ağ hatasında erişimi.

## Öz denetim

Mevcut token paleti ve gömülü fontlar kullanıldı; emoji, kart üçlemesi, yeni ikon ailesi ve dekoratif gradyan metni yok. Prototip içerik düzeni flex; işletim sistemi klavyesi yeniden çizilmedi. Boş/yükleniyor/hata/meşgul/basılı örnekleri dahil. Prototip örnekleri backend hesap formülünün yerine geçmez. Tasarım incelemesi root üzerinden istenir; bu belge PASS iddiası taşımaz.
