/**
 * Arayüz metinleri — tek kaynak: projects/trinkow/docs/content/metinler.md.
 * Kodda cümle uydurulmaz. Yeni metin gerekiyorsa önce metinler.md'ye eklenir.
 *
 * Anahtarlar metinler.md'deki i18n anahtarlarıyla birebir aynıdır.
 */
export const t = {
  // §1 genel ve navigasyon
  'sekme.gunluk': 'Günlük',
  'sekme.kayitlar': 'Kayıtlar',
  'sekme.ozet': 'Özet',
  'eylem.kaydet': 'Kaydet',
  'eylem.vazgec': 'Vazgeç',
  'eylem.sil': 'Sil',
  'eylem.kapat': 'Kapat',
  'eylem.yeniden_dene': 'Yeniden dene',
  'eylem.harcama_ekle': 'Harcama ekle',
  'eylem.tum_kategoriler': 'Tüm kategoriler',
  'eylem.tekrarla': 'Tekrarla',
  'eylem.geri': 'Geri',
  'eylem.simdi_degil': 'Şimdi değil',
  'eylem.devam': 'Devam',

  // §2 Katman 1 — Onboarding (E-01…E-03 · K-053, 3 soru · D-2d-3a)
  'ob.adim': 'Adım 1/3',
  'ob.adim2': 'Adım 2/3',
  'ob.adim3': 'Adım 3/3',
  'a11y.kurulum_ilerlemesi': 'Kurulum ilerlemesi',
  'ob.niyet.baslik': 'Neden buradasın',
  'ob.niyet.aciklama': 'Sonra değiştirebilirsin.',
  'ob.niyet.takip': 'Param nereye gidiyor',
  'ob.niyet.takip.alt': 'Günlük harcamanı görmek istiyorsun.',
  'ob.niyet.tasarruf': 'Bütçe yaratmak',
  'ob.niyet.tasarruf.alt': 'Her ay bir miktar ayırmak istiyorsun.',
  'ob.niyet.borc': 'Borç kapatmak',
  'ob.niyet.borc.alt': 'Kalan borcu eritmek istiyorsun.',
  'ob.onizleme.etiket': 'Panondaki büyük sayı',
  'ob.gelir.baslik': 'Aylık net gelirin ne kadar',
  'ob.gelir.aciklama': 'Planı buna göre kuruyoruz. İstemezsen atla.',
  'ob.gelir.etiket': 'Aylık net gelir',
  'ob.gelir.net': 'Eline geçen tutar. Kesintiden sonrası.',
  'ob.gelir.bos': 'Kesin olması gerekmiyor. Yaklaşık yeter.',
  'ob.gelir.mahremiyet': 'Gelirin hesabında kalır.',
  'ob.gelir.atlarsan': 'Atlarsan günlük limiti sen yazarsın.',
  'ob.gelir.atla': 'Atla',
  'a11y.ob.gelir_atla': 'Gelir sorusunu atla',
  'ob.maas.baslik': 'Maaşın hangi gün yatıyor',
  'ob.maas.aciklama': 'Günlük limit maaş dönemine bölünür.',
  'ob.maas.duzensiz': 'Düzensiz geliyor',
  'ob.maas.duzensiz.not': 'Dönem 30 gün sayılır. Maaş günü değişirse ayarlardan düzeltebilirsin.',
  'ob.bitir': 'Başla',
  'ob.ozet.limit_yok': 'Henüz yok',
  'ob.ozet.limit_not': 'Günlük limiti plan kurunca ya da elle yazınca belirlersin.',
  'onboarding.ozet.limitSatiri': 'Gelirini yazdığın için sana bir günlük limit önerebiliriz. Kabul etmek zorunda değilsin.',
  /**
   * `ob.ozet.*_label` ve `ob.ozet.maas_duzensiz` metinler.md'nin "Katman 1
   * özeti" tablosunda henüz ayrı anahtar olarak yok; satır etiketleri
   * ("Niyet" · "Maaş günü" · "Günlük limit") ve "Düzensiz" değeri onaylı
   * prototipten (03-onboarding.html) birebir alındı. PM'e bildirildi.
   */
  'ob.ozet.baslik': 'Kurulum özeti',
  'ob.ozet.niyet_label': 'Niyet',
  'ob.ozet.maas_label': 'Maaş günü',
  'ob.ozet.limit_label': 'Günlük limit',
  'ob.ozet.maas_duzensiz': 'Düzensiz',

  // §27.2 Günlük limit önerisi (Katman 1 çıkışı · K-059/5 · D-2d-3a)
  'oneri.baslik': 'Günlük limit önerimiz',
  'oneri.pul': 'Öneri',
  'oneri.alt': 'Sen onaylamadan limit olmaz.',
  'oneri.nasil.baslik': 'Nasıl hesaplandı',
  'oneri.nasil.2':
    'Yaygın bir varsayılan dağılım kullandık: %50 zorunlu, %30 sosyal ve keyfi, %20 birikim.',
  'oneri.serit.1': 'Bu sayı senin cevaplarından değil, varsayılan dağılımdan çıktı.',
  'oneri.serit.2': 'Sekiz kartı doldurursan plan kendi giderlerinle kurulur.',
  'oneri.btn.kabul': 'Limiti kabul et',
  'oneri.btn.degistir': 'Başka bir sayı yaz',
  'oneri.btn.red': 'Limitsiz devam et',
  /**
   * Denklem kutusunun mikro etiketleri — prototipte (satır 430-434) var ama
   * metinler.md §27.2 tablosunda henüz ayrı anahtar değil. PM'e bildirildi.
   */
  'oneri.denklem.sosyal': 'sosyal ve keyfi pay',
  'oneri.denklem.kalan_gun': 'kalan gün',
  'oneri.denklem.gunluk': 'günlük',

  // §23.1 E-10 Günlük — sayfalama ve gün başlığı (v4 · K-049/K-055)
  'gunluk.onceki_gun': 'Önceki gün',
  'gunluk.sonraki_gun': 'Sonraki gün',
  'gunluk.ipucu': 'Geçmiş günler solda. Sağa kaydır.',
  'gunluk.ipucu_kapat': 'İpucunu kapat',
  'gunluk.sinir.ilk_kayit': 'İlk kaydın bu gün. Daha geriye kayıt yok.',
  'gunluk.a11y.takvim': 'Gün seç',

  // §23.2 kapanmış (geçmiş) sayfa
  'gunluk.hero.gecmis': 'o gün harcanan',
  'gunluk.seriye_sayildi': 'Bu gün seriye sayıldı.',
  'gunluk.seriye_sayilmadi': 'Bu gün seriye sayılmadı.',
  'gunluk.liste_baslik.gecmis': 'O günün kayıtları',

  // §23.3 harcamasız gün
  'gunluk.harcamasiz.baslik': 'Harcamasız gün',
  'gunluk.harcamasiz.govde': 'O gün kayıt yok. Kayıtsız gün seriye sayılmaz.',
  'gunluk.harcamasiz.ipucu': 'Harcamasız geçtiyse işaretle, seri korunur.',
  'gunluk.harcamasiz.eylem': 'Harcamasız işaretle',
  'gunluk.harcamasiz.isaretli': 'Harcamasız gün. Seriye sayıldı.',
  'gunluk.seri_baslar.baslik': 'Seri bugün başlar',
  'gunluk.seri_baslar.govde': 'Günü limit altında kapatırsan seri 1 gün olur.',

  // §23.4 kategoriler kartı (yalnız Bugün sayfası)
  'gunluk.grup.baslik': 'Kategoriler',
  'gunluk.grup.alt': 'Bu ay · kategori limiti',
  'gunluk.grup.bugun_yok': 'bugün kayıt yok',

  // §23.5 E-21 Seri
  'seri.baslik': 'Seri',
  'seri.hero.birim': 'gün',
  'seri.kirildi': 'Seri dün kırıldı. Bugün yeniden başlıyor.',
  'seri.bos.govde': 'Seri henüz başlamadı. Bugünü limit altında kapat.',
  'seri.en_uzun': 'En uzun seri',
  'seri.en_uzun_bos': 'Henüz yok',
  'seri.duraklar': 'Duraklar',
  'seri.pencere.bos': 'Günleri yazdıkça buraya dolacak.',
  'seri.lejant.altinda': 'limit altında',
  'seri.lejant.disinda': 'limit dışı',
  'seri.lejant.kayit_yok': 'kayıt yok',
  'seri.kural.baslik': 'Seri nasıl işler',
  'seri.kural.1': 'Günü günlük limitin altında kapatırsan seri sürer.',
  'seri.kural.2': 'Kayıt yazmadığın gün sayılmaz. Harcamasız geçtiyse işaretle.',
  'seri.kapali.baslik': 'Seri kapalı',
  'seri.kapali.govde': 'Seri için günlük limit gerekir.',
  'seri.kapali.ipucu': 'Limit kurduğunda duraklar ve günler burada görünür.',
  'kutlama.kapat': 'Dokununca kapanır',
  'kutlama.a11y_kapat': 'Kutlamayı kapat',

  // §24 E-24 Gün seçici
  'gunsec.baslik': 'Gün seç',
  'gunsec.bugune_don': 'Bugüne dön',
  'gunsec.alt.kayit_yok': 'kayıt yok',
  'gunsec.lejant.altinda': 'limit altı',
  'gunsec.lejant.disinda': 'limit dışı',
  'gunsec.lejant.kayit_yok': 'kayıt yok',
  'gunsec.lejant.bugun': 'Kutunun altındaki nokta bugünü gösterir.',
  'gunsec.bos.baslik': 'Bu ayda kayıt yok',
  'gunsec.bos.govde': 'Kayıt yazdığın günler burada işaretlenir. Bugünden başlayabilirsin.',
  'gunsec.ozet.kayitli_gun': 'Kayıt yazılan gün',
  'gunsec.ozet.limit_alti': 'Limit altı gün',
  'gunsec.ozet.biriken': 'Limit altı günlerde biriken',
  'gunsec.onceki_ay': 'Önceki ay',
  'gunsec.sonraki_ay': 'Sonraki ay',
  'gunsec.onceki_ay_yok': 'Önceki ay yok',
  'gunsec.sonraki_ay_yok': 'Sonraki ay yok',

  // §4 E-11 harcama ekle
  'ekle.baslik': 'Harcama ekle',
  'ekle.tutar.etiket': 'Tutar',
  'ekle.kategori.etiket': 'Kategori',
  'ekle.odeme.etiket': 'Ödeme',
  'ekle.odeme.nakit': 'Nakit',
  'ekle.odeme.kart': 'Kart',
  'ekle.taksit.baglanti': 'Taksitli',
  'ekle.taksit.baslik': 'Kaç taksit',
  'ekle.tarih.bugun': 'Bugün',
  'ekle.tarih.dun': 'Dün',
  'ekle.not.ac': 'Not',
  'ekle.not.etiket': 'Not (isteğe bağlı)',
  'ekle.not.placeholder': 'Kısa bir not',
  'ekle.urun.placeholder': 'Ne aldın? (isteğe bağlı)',
  'ekle.sik_alinanlar': 'Sık alınanlar',

  // §27.1 E-11 ürün arama (F-18 · T-4)
  'ekle.arama.placeholder': 'Ne aldın? (isteğe bağlı)',
  'ekle.arama.grup.gecmis': 'Son kullandıkların',
  'ekle.arama.grup.katalog': 'Ürünler',
  'ekle.tutar.alt.gecmisten': 'Tutar geçen seferkinden geldi. Değiştirebilirsin.',
  'ekle.tutar.alt.katalogdan': 'Tutarı sen yaz. Fiyat tahmini yapmıyoruz.',
  'ekle.tutar.alt.kategori': 'Kategori üründen geldi. Değiştirebilirsin.',
  'ekle.hata.tutar': 'Tutar sıfırdan büyük olmalı.',
  'ekle.hata.kategori': 'Bir kategori seç.',
  'ekle.hata.yazilamadi': 'Kayıt yazılamadı. Yeniden dene.',
  'a11y.ekle.arama': 'Ürün ara, isteğe bağlı',
  'a11y.ekle.aramaTemizle': 'Aramayı temizle',
  'a11y.ekle.urunKaldir': 'Ürünü kaldır',

  // §14 hata ve doğrulama
  'hata.tutar_buyuk': 'Bu tutar çok büyük görünüyor. Kontrol et.',
  'hata.kategori_yok': 'Bir kategori seç.',
  'hata.yazma': 'Kayıt yazılamadı. Yeniden dene.',
  'hata.okuma.baslik': 'Kayıtlar açılamadı',
  'hata.okuma.govde': 'Bir şey ters gitti. Yeniden denemek çoğu zaman yeterli.',
  'hata.okuma.eylem': 'Yeniden dene',

  // §5 / §21.3 E-12 / E-13 detay ve silme
  'detay.baslik': 'Harcama',
  'detay.taksit_uyari': 'Düzenleme tüm taksit serisini etkiler.',
  'detay.tutar_kilit': 'Taksitli kayıtta tutar değiştirilemez.',
  'detay.sil_taksit': 'Taksit serisini sil',
  'detay.not.etiket': 'Not',
  'detay.sil': 'Bu harcamayı sil',
  'detay.bulunamadi.baslik': 'Bu kayıt bulunamadı',
  'detay.bulunamadi.govde': 'Silinmiş olabilir. Listeye dönebilirsin.',
  'detay.bulunamadi.eylem': 'Listeye dön',
  'sil.baslik': 'Bu taksit serisi silinecek',
  'sil.onayla': 'Sil',
  'sil.vazgec': 'Vazgeç',
  'sil.siliniyor': 'Siliniyor',

  // §21.1 E-14 kayıtlar
  'kayitlar.baslik': 'Kayıtlar',
  'kayitlar.taksitleri_ac': 'Taksitli işlemleri aç',
  'kayitlar.onceki_ay': 'Önceki ay',
  'kayitlar.sonraki_ay': 'Sonraki ay',
  'kayitlar.ay_ozet_bos': '0 kayıt',
  'kayitlar.yer_tutucu.govde': 'Liste açılınca burada görünür.',
  // metinler.md §13'te anahtarsız verilen boş durum metinleri
  'bos.kayitlar.baslik': 'Kayıt yok',
  'bos.kayitlar.govde': 'Aşağıdaki butonla ilkini ekle.',
  'bos.kayitlar_ay.baslik': 'Bu ayda kayıt yok',
  'bos.kayitlar_ay.govde': 'Başka bir ay seçebilirsin.',

  // §15 toast
  'toast.silindi': 'Harcama silindi',
  'toast.geri_al': 'Geri al',
  'toast.geri_alindi': 'İşlem geri alındı',
  'toast.taksit_silindi': 'Taksit serisi silindi.',

  // §3 E-10 pano
  'pano.bugun_baslik': 'Bugün',
  'pano.liste_baslik': 'Bugünkü kayıtlar',
  'pano.kalan_kategori': 'Kategori limitleri',
  'pano.tumunu_gor': 'Tümünü gör',
  'pano.kip.takip': 'Takip',
  'pano.kip.tasarruf': 'Tasarruf',
  'pano.kip.borc': 'Borç',
  'pano.hero.takip': 'bugün kalan',
  'pano.hero.tasarruf': 'bu ay biriken',
  'pano.hero.borc': 'kalan borç',
  /**
   * tokens.md §7.5 / §1.5 — limit dışında kahraman sayının altındaki etiket
   * birebir "limit dışı" sözcüğüdür. metinler.md'de henüz anahtarı yok;
   * PM'e bildirildi (öneri: `pano.hero.limit_disi`).
   */
  'pano.hero.limit_disi': 'limit dışı',
  'pano.alt.bos': 'Bugün henüz bir şey yazmadın.',
  'pano.limit_sorgu.govde': 'Limit gerçekçi mi. Birlikte bakalım.',
  'pano.limit_sorgu.eylem': 'Limiti gözden geçir',

  // §3.2b limitsiz varyant (`HeroPlain`)
  'pano.limitsiz.deger': 'Limit yok',
  'pano.hero.limitsiz': 'bugün harcanan',
  'pano.liste.adet': 'kayıt',

  // §13 boş durumlar — E-10 ilk gün
  'bos.pano.baslik': 'Bugün boş',
  'bos.pano.govde': 'Bugün henüz bir şey yazmadın. İlk kahve iyi bir başlangıç.',

  // diğer ekranlardan ödünç alınan, E-10'da geçen dizeler
  'limitler.kategori_aciklama': 'Aylık. Boş bırakırsan takip edilmez.',
  'kategori.limit_ekle': 'Limit belirle',

  // §7 / §22.1 E-15 kategori detayı
  'kategori.limit_yok': 'Bu kategoride limit yok.',
  'kategori.bar_periyot': 'aylık',
  'kategori.liste_baslik': 'Bu ayki kayıtlar',
  'kategori.bos_govde': 'Bu ay bu kategoride harcama yazmadın.',

  // §8 / §21.2 E-16 özet
  'ozet.baslik': 'Özet',
  'ozet.hafta_bu': 'Bu hafta',
  'ozet.hafta_tamamlanan': 'Tamamlanan hafta',
  'ozet.onceki_hafta': 'Önceki hafta',
  'ozet.sonraki_hafta': 'Sonraki hafta',
  'ozet.hafta_toplam': 'Haftalık toplam',
  'ozet.gunluk_ortalama': 'Günlük ortalama',
  'ozet.gunluk_toplam': 'Günlük toplam',
  'ozet.en_cok': 'En çok harcadığın kategori',
  'ozet.kategori_dagilimi': 'Kategori dağılımı',
  'ozet.kucuk_harcama_baslik': '50 ₺ altı harcamalar',
  'ozet.taksitleri_gor': 'Taksitleri gör',
  /**
   * Prototipte E-16 üst sağ ikon butonunun `aria-label`'ı — metinler.md'de
   * henüz anahtarı yok (05-ozet.html satır 36). `kayitlar.taksitleri_ac` ile
   * aynı desen ("X'i aç"); PM'e bildirildi.
   */
  'ozet.limitleri_ac': 'Kategori limitlerini aç',

  // §13 E-16 boş hafta
  'bos.ozet.baslik': 'Özet için erken',
  'bos.ozet.govde': 'Birkaç kayıt sonra burada haftalık dağılımı görürsün.',

  // §9 / §22.2 E-17 limitler
  'limitler.baslik': 'Limitler',
  'limitler.gunluk': 'Günlük limit',
  'limitler.gunluk_aciklama': 'Her gün sıfırlanır. Aylık plan değildir.',
  'limitler.kategori_baslik': 'Kategori limitleri',
  'limitler.kategori_periyot': 'Aylık',
  'limitler.limit_yok': 'Limit yok',
  'limitler.limit_kaldir': 'Limiti kaldır',
  'limitler.bos_takip': 'Boş bırakılan kategori takip edilmez.',
  'limitler.kategori_bos': 'Kategori limiti koymak zorunda değilsin. Günlük limit tek başına çalışır.',
  'limitler.kategori_ekle': 'Kategori limiti ekle',
  'hata.limit_sifir': 'Limit sıfırdan büyük olmalı. Takip istemiyorsan limiti kaldır.',
  'hata.limit_negatif': 'Limit sıfırdan küçük olamaz.',
  'a11y.gunluk_limit_degistir': 'Günlük limiti değiştir',

  // §10 / §22.3 E-18 taksitler
  'taksit.baslik': 'Taksitler',
  'taksit.bu_ay_etiket': 'Bu ay',
  'taksit.aciklama': 'Taksitler girildiği güne değil, ait olduğu aya yazılır.',
  'taksit.gelecek_baslik': 'Önümüzdeki aylar',
  'taksit.seriler_baslik': 'Süren seriler',
  'taksit.her_ay': 'her ay',
  'taksit.son_taksit': 'Son taksit bu ay',
  'bos.taksit.baslik': 'Taksitli işlem yok',
  'bos.taksit.govde': 'Kartla taksitli harcama girdiğinde burada listelenir.',

  // §26/§27 D-2d-3b · Katman 2 "Seni tanıyalım" (E-25)
  'tan.baslik': 'Seni tanıyalım',
  'tan.aciklama': 'Sekiz kart. Her birini atlayabilirsin.',
  'tan.fiyat_vaadi': 'Fiyatları biz tahmin etmiyoruz.',
  'tan.fiyat_vaadi.alt': 'Ne kadar ödediğini sen yazıyorsun.',
  'tan.atla': 'Bu kartı atla',
  /** Kapı (giriş) yüzeyi "Neler soracağız" özeti — prototipte anahtarsız, PM'e bildirildi. */
  'tan.kapi.neler': 'Neler soracağız',
  'tan.kapi.aliskanlik.baslik': 'Alışkanlıklar',
  'tan.kapi.aliskanlik.alt': 'Sıklığı ve kendi ödediğin fiyatı.',
  'tan.kapi.birikim.alt': 'Gelirinin ne kadarını ayırmak istiyorsun.',
  /** Katman 2'nin birikim kartında gelir paylaşılmamışsa — prototipte örneklenmedi (yalnız E-26'da var), PM'e bildirildi. */
  'tan.birikim.gelirsiz': 'Gelirini paylaşmadığın için yüzde hesaplanamıyor. Bu kartı atlayabilirsin.',
  'a11y.tan.geri': 'Geri dön',
  'a11y.tan.kapat': 'Kapat',
  'tan.sabit.baslik': 'Sabit giderler',
  'tan.sabit.aciklama': 'Her ay kesin çıkan tutarlar. Bilmediğini boş bırak.',
  'tan.sabit.kira': 'Kira ve aidat',
  'tan.sabit.fatura': 'Faturalar',
  'tan.sabit.ulasim': 'Ulaşım ve yakıt',
  'tan.sabit.kredi': 'Kredi ve taksit',
  'tan.sabit.toplam': 'Toplam',
  'tan.girilmedi': 'Girilmedi',
  'tan.siklik.etiket': 'Ne sıklıkla',
  'tan.siklik.gun1': 'Günde 1',
  'tan.siklik.gun2': 'Günde 2',
  'tan.siklik.hafta2_3': 'Haftada 2-3',
  'tan.siklik.hafta1': 'Haftada 1',
  'tan.siklik.ay1_2': 'Ayda 1-2',
  'tan.siklik.hic': 'Hiç',
  'tan.siklik.serbest': 'Kendim yazayım',
  'tan.ayda': 'Ayda',
  'tan.kahve.baslik': 'Kahve',
  'tan.kahve.aciklama': 'Dışarıda aldığın kahve. Evde yaptığın sayılmaz.',
  'tan.kahve.fiyat': 'Bir fincan kaç lira',
  'tan.kahve.birim': 'fincan',
  'tan.sigara.baslik': 'Sigara',
  'tan.sigara.aciklama': 'Sıklığı ve kendi ödediğin fiyatı yazıyorsun.',
  'tan.sigara.fiyat': 'Bir paket kaç lira',
  'tan.sigara.birim': 'paket',
  /**
   * `tan.alkol.*` ve `tan.abonelik.*` onaylı prototipte (17-tanisma.html)
   * kart olarak ÖRNEKLENMEDİ — yalnız E-26'nın örnek verisinde adları geçiyor
   * ("Alkol · Haftada 1 × 220 ₺", "Abonelikler · Ayda 4 abonelik"). Metinler
   * sigara kartının BİREBİR kalıbından (K-053: "yargılamayan kart, aynı
   * bileşen") türetildi; PM/içerik yazarına bildirildi, metinler.md'ye
   * işlenmeli.
   */
  'tan.alkol.baslik': 'Alkol',
  'tan.alkol.aciklama': 'Sıklığı ve kendi ödediğin fiyatı yazıyorsun.',
  'tan.alkol.fiyat': 'Bir kadeh kaç lira',
  'tan.alkol.birim': 'kadeh',
  'tan.hic.not': 'Hiç dedin. Bu kart planda görünmez.',
  'tan.yemek.baslik': 'Dışarıda yemek',
  'tan.yemek.aciklama': 'Öğle yemeği, akşam yemeği, paket sipariş.',
  'tan.yemek.fiyat': 'Bir yemek kaç lira',
  'tan.yemek.birim': 'yemek',
  'tan.abonelik.baslik': 'Abonelikler',
  'tan.abonelik.aciklama': 'Dijital ve fiziksel tüm abonelikler.',
  'tan.abonelik.adet': 'Kaç abonelik',
  'tan.abonelik.ortalama': 'Ortalama aylık ücret',
  'tan.yatirim.baslik': 'Yatırım',
  'tan.yatirim.aciklama': 'Cevabın yalnız birikimini adlandırmak için.',
  'tan.yatirim.yapiyorum': 'Yapıyorum',
  'tan.yatirim.dusunuyorum': 'Yapmayı düşünüyorum',
  'tan.yatirim.ilgilenmiyorum': 'İlgilenmiyorum',
  'tan.yatirim.sinir': 'Yatırım tavsiyesi vermiyoruz.',
  'tan.yatirim.sinir.alt': 'Birikimin bir kısmını yatırım payı diye etiketleriz.',
  'tan.birikim.baslik': 'Birikim hedefi',
  'tan.birikim.aciklama': 'Sabit giderlerinden sonra kalanın içinden ayrılır.',
  'tan.birikim.etiket': 'Gelirin yüzdesi',
  'tan.birikim.sinir': 'Üst sınıra geldin. Kaydırıcı burada durur.',
  'tan.birikim.sinir.alt': 'Sosyal ve keyfi payı 0 ₺ kalır.',
  'tan.donus.baslik': 'Kaldığın yerden',
  'tan.donus.bekleyen': 'Bekleyen kartlar',
  'tan.donus.cevaplanmadi': 'Cevaplanmadı',
  'tan.donus.plan': 'Planı şimdi gör',
  'tan.donus.devam': 'Devam et',
  'tan.fiyat.bos': 'Fiyatını yaz',
  'tan.gor.plan': 'Planı gör',

  // §28 D-2d-3b · Plan (E-26)
  'plan.ustbaslik': 'Plan',
  'plan.baslik': 'Planın hazır',
  'plan.aciklama': 'Cevaplarından çıkardık. Değiştirebilirsin.',
  'plan.aylik_planin': 'Aylık planın',
  'plan.turetildi': 'Türetildi',
  'plan.pay.zorunlu': 'Zorunlu',
  'plan.pay.zorunlu.alt': 'Kira, fatura, ulaşım, kredi taksiti.',
  'plan.pay.sosyal': 'Sosyal ve keyfi',
  'plan.pay.sosyal.alt': 'Günlük limitin buradan çıkar.',
  'plan.pay.birikim': 'Birikim',
  'plan.limit.baslik': 'Günlük limit',
  'plan.limit.pano': 'Panodaki büyük sayı bu olur.',
  'plan.limit.pano.alt': 'Her maaş döneminde yeniden bölünür.',
  'plan.denklem.sosyal': 'sosyal pay',
  'plan.denklem.kalan_gun': 'kalan gün',
  'plan.denklem.gunluk': 'günlük',
  'plan.nasil': 'Nasıl hesaplandı',
  'plan.nasil.hesap': 'Hesap',
  'plan.nasil.anladim': 'Anladım',
  'plan.nasil.1': 'Sabit giderlerini topladık',
  'plan.nasil.2': 'Birikim hedefini ayırdık',
  'plan.nasil.3': 'Kalanı sosyal ve keyfi paya yazdık',
  'plan.nasil.4': 'Dönemde kalan güne böldük',
  'plan.nasil.yuvarlama': 'Hesap kuruş üzerinden yapılır.',
  'plan.nasil.yuvarlama.alt':
    'Günlük limit tam liraya aşağı yuvarlanır. Yüzdeler tam sayıya yuvarlanır, toplamı 100\'e tamamlanır.',
  'plan.aliskanlik.baslik': 'Alışkanlık maliyeti',
  'plan.aliskanlik.sag': 'Kendi fiyatlarınla',
  'plan.aliskanlik.bos': 'Alışkanlık kartlarını cevaplamadın.',
  'plan.aliskanlik.bos.alt': 'Sıklığı ve kendi fiyatını yazarsan aylık tutarı burada görürsün.',
  'plan.aliskanlik.kartlara_don': 'Kartlara dön',
  'plan.ayar.baslik': 'Payları ayarla',
  'plan.ayar.tek_kaydirici': 'Tek kaydırıcı',
  'plan.ayar.etiket': 'Birikim payı',
  'plan.ayar.not': 'Zorunlu pay sabit kalır. O senin girdiğin sabit giderlerin toplamı.',
  'plan.ayar.aralik_en_az': 'En az %0',
  'plan.gelirsiz.baslik': 'Limitini yazalım',
  'plan.gelirsiz.aciklama': 'Gelirini paylaşmadın. Yüzde planı kurulmadı.',
  'plan.gelirsiz.limit_etiket': 'Günlük limit',
  'plan.gelirsiz.elimizde_baslik': 'Elimizde ne var',
  'plan.gelirsiz.elimizde_alt': 'Gelir olmadan',
  'plan.gelirsiz.eldeki': 'Alışkanlık maliyeti gelirsiz de çalışır.',
  'plan.gelirsiz.eldeki_alt': 'Sıklığı ve fiyatı sen yazdığın için bu kart eksiksiz.',
  'plan.gelirsiz.aylik_toplam': 'Aylık alışkanlık toplamı',
  'plan.gelirsiz.limit_not': 'Günlük limitini yazarken bu sayıyı hesaba katabilirsin.',
  'plan.gelirsiz.sonra': 'Gelirini sonra da ekleyebilirsin.',
  'plan.gelirsiz.sonra_alt': 'Ayarlar, Plan ve profil bölümü. Yüzde planı o an kurulur.',
  'plan.gelirsiz.kaydet': 'Limiti kaydet',
  'plan.eksi.baslik': 'Plan bu ay kurulamadı',
  'plan.eksi.aciklama': 'Sabit giderlerin gelirinden fazla.',
  'plan.eksi.normalize': 'Bu çok rastlanan bir durum. Ölçülebilir olması iyi haber.',
  'plan.eksi.hesap': 'Hesap',
  'plan.eksi.bu_ay': 'Bu ay',
  'plan.eksi.net_gelir': 'Aylık net gelir',
  'plan.eksi.sabit_giderler': 'Sabit giderler',
  'plan.eksi.kalan_etiket': 'Kalan',
  'plan.eksi.yuzde_yok': 'Yüzde planı kalan tutar üzerine kurulur. Kalan olmadığı için pay dağılımı yazılmadı.',
  'plan.eksi.cikis_baslik': 'Çıkış yolu',
  'plan.eksi.cikis_alt': 'Seçim senin',
  'plan.eksi.uc_yol': 'Buradan üç yol var.',
  'plan.eksi.yol1': 'Giderleri gözden geçir',
  'plan.eksi.yol1.alt': 'Kredi taksiti bitiyor mu, fatura tahmini yüksek mi.',
  'plan.eksi.yol2': 'Limiti elle yaz',
  'plan.eksi.yol2.alt': 'Plan olmadan da günlük limit koyabilirsin.',
  'plan.eksi.yol3': 'Limitsiz devam et',
  'plan.eksi.yol3.alt': 'Takip etmek için plana ihtiyacın yok. Kayıt tutmak tek başına işe yarar.',
  'plan.yarim.baslik': 'Plan yarım hazır',
  'plan.yarim.aciklama': 'Dört kart boş. Eldekiyle böldük.',
  'plan.yarim.birikim': 'Hedef girmedin.',
  'plan.yarim.not': 'Birikim hedefi girmedin. Şimdilik kalanın tamamı sosyal ve keyfi payında.',
  'plan.yarim.limit_not': 'Birikim hedefi girersen bu sayı düşer.',
  'plan.yarim.kalan_kartlara_don': 'Kalan kartlara dön',
  'plan.kur': 'Planı kur',

  // §11 · §22.4 D-2c-1 · E-19 — Ayarlar
  'ayar.baslik': 'Ayarlar',
  'ayar.bildirim': 'Akşam özeti',
  'ayar.bildirim_aciklama': 'Günde en fazla bir bildirim.',
  'ayar.bildirim_saat': 'Bildirim saati',
  'ayar.bildirim_izni_kapali_not': 'Bildirim izni kapalı. Cihaz ayarlarından açabilirsin.',
  'ayar.bildirim_kapali_not': 'İzin verilene kadar akşam özeti gönderilmez.',
  'ayar.gun_siniri': 'Gün sınırı',
  'ayar.gun_siniri_aciklama': 'Gün bu saatte başlar. Gece geç harcayanlar için.',
  'ayar.gun_siniri.0': '00.00',
  'ayar.gun_siniri.3': '03.00',
  'ayar.gun_siniri.6': '06.00',
  'ayar.varsayilan_odeme': 'Varsayılan ödeme',
  'ayar.odeme_aciklama': 'Yeni harcama bu seçimle açılır.',
  'ayar.kip': 'Kip',
  'ayar.kip_aciklama': 'Panodaki büyük sayıyı belirler.',
  'ayar.kip_degistir': 'Kip seç',
  'ayar.plan.baslik': 'Plan ve profil',
  'ayar.plan.aciklama': 'Plan cevaplarından çıkar. İstediğin an değiştir.',
  'ayar.plan.gelir': 'Aylık net gelir',
  'ayar.plan.gelir_girilmedi': 'Girilmedi',
  'ayar.plan.maas_gunu': 'Maaş günü',
  'ayar.plan.gelirsiz': 'Gelirini girmedin. Plan onsuz kurulmuyor.',
  'ayar.plan.tanit': 'Seni tanıyalım',
  'ayar.plan.gor': 'Planı gör',
  'ayar.hesap.baslik': 'Hesap',
  'ayar.hesap.aciklama': 'Hesap yalnız seni tanımak için.',
  'ayar.hesap.eposta': 'E-posta',
  'ayar.hesap.saglayici.google': 'Google ile bağlı.',
  'ayar.hesap.saglayici.apple': 'Apple ile bağlı.',
  'ayar.hesap.saglayici.sifre': 'Şifre ile bağlı.',
  'ayar.hesap.cikis': 'Çıkış yap',
  'ayar.hesap.cikis_not': 'Çıkınca kayıtların hesabında kalır.',
  'ayar.hesap.sil': 'Hesabı sil',
  'ayar.hesap.kapali': 'Hesap zorunlu. Kayıtların hesabında kalır.',
  'ayar.hesap.kapali_kapi': 'Oturum aç ya da hesap oluştur',

  // §25 D-2c-2 · E-22 Oturum aç · E-23 Hesap oluştur (metinler.md §25)
  'hesap.mahremiyet': 'Harcamaların hesabında kalır. Hesap yalnız seni tanır.',
  'hesap.mahremiyet.ek': 'Yedekleme sonraki sürümlerde.',
  'giris.ayirac': 'ya da',
  'giris.hesapsiz': 'Hesapsız devam et',
  'giris.sosyal.apple': 'Apple ile Devam Et',
  'giris.sosyal.google': 'Google ile devam et',
  'alan.eposta': 'E-posta',
  'alan.eposta_ph': 'ornek@eposta.com',
  'alan.sifre': 'Şifre',
  'alan.sifre_ph.giris': 'Şifreni yaz',
  'alan.sifre_ph.kayit': 'Şifre belirle',
  'alan.sifre.gorunur': 'Şifreyi göster',
  'alan.sifre.gizli': 'Şifreyi gizle',
  'giris.baslik': 'Oturum aç',
  'giris.eylem': 'Oturum aç',
  'giris.mesgul': 'Oturum açılıyor',
  'giris.unuttum': 'Şifremi unuttum',
  'giris.kayit_kapisi': 'Hesap oluştur',
  'hata.eposta_bicim': 'Geçerli bir e-posta yaz.',
  'hata.kimlik': 'E-posta ya da şifre yanlış. Yeniden dene.',
  'hata.eposta_bos': 'Önce e-postanı yaz.',
  'hata.baglanti.giris': 'Oturum açmak için bağlantı gerekir.',
  'sifirla.baslik': 'Bağlantıyı gönderdik',
  'sifirla.ipucu': 'Gelmediyse istenmeyen klasörüne bak.',
  'sifirla.yeniden': 'Yeniden gönder',
  'sifirla.bekle': '60 saniye sonra yeniden gönderebilirsin.',
  'sifirla.geri': 'Oturum açmaya dön',
  'kayit.baslik': 'Hesap oluştur',
  'kayit.eylem': 'Hesap oluştur',
  'kayit.mesgul': 'Hesap oluşturuluyor',
  'kayit.sifre_kural': 'En az 8 karakter.',
  'kayit.sifre_kural_tamam': 'Uzunluk yeterli.',
  'kayit.yasal': 'Hesap oluşturarak **Kullanım şartları** ve **Gizlilik politikasını** kabul ediyorsun.',
  'kayit.giris_kapisi.soru': 'Hesabın var mı',
  'kayit.giris_kapisi.aksiyon': 'Oturum aç',
  'hata.eposta_kayitli': 'Bu e-posta ile hesap var. Oturum aç.',
  'hata.baglanti.kayit': 'Hesap açmak için bağlantı gerekir.',

  'hesapsil.baslik': 'Hesabın silinecek',
  'hesapsil.govde': 'Geri alınamaz. Bu e-posta ile bir daha oturum açamazsın.',
  'hesapsil.eylem': 'Hesabı sil',
  'ayar.veri': 'Veri',
  'ayar.veri_aciklama': 'Kayıtların hesabında kalır. İstediğin an hepsini silebilirsin.',
  'ayar.veri_sil': 'Tüm verileri sil',
  'ayar.veri_sil_baslik': 'Tüm kayıtların silinecek',
  'ayar.veri_sil_govde': 'Geri alınamaz. Limitlerin ve kurulumun kalır.',
  'ayar.surum': 'Sürüm {surum}',

  // §12 · §22.5 D-2c-1 · E-20 — Aşamalı profilleme (F-12). K-061/3: gelir sorusu
  // (`prof.gelir`) EMEKLİYE AYRILDI, kodlanmadı — bkz. task brief madde 4.
  'prof.yatirim': 'Yatırım yapıyor musun?',
  'prof.taksit': 'Taksitli alışveriş yapar mısın?',
  'prof.taksit.sik_sik': 'Sık sık',
  'prof.taksit.bazen': 'Bazen',
  'prof.taksit.nadiren': 'Neredeyse hiç',
  'prof.bildirim': 'Akşam kısa bir özet göndereyim mi?',
  'prof.bildirim.gonder': 'Gönder',
  'prof.bildirim.gonderme': 'Gönderme',
  'prof.aciklama': 'Cevabın panonu sana göre ayarlar.',
  'prof.simdi_degil': 'Şimdi değil',
  'prof.degisti': 'Cevabına göre eklendi. Ayarlardan kaldırabilirsin.',
  'a11y.prof.kapat': 'Profilleme sorusunu kapat',
} as const;

/** `Bugün {harcanan}. Limitinin {fark} altındasın.` */
export function altAltinda(harcanan: string, fark: string): string {
  return `Bugün ${harcanan}. Limitinin ${fark} altındasın.`;
}

/** `Günlük limitin doldu. Bugün {harcanan}.` */
export function altDoldu(harcanan: string): string {
  return `Günlük limitin doldu. Bugün ${harcanan}.`;
}

/** `Limitin {fark} üzerindesin.` */
export function altDisinda(fark: string): string {
  return `Limitin ${fark} üzerindesin.`;
}

/** `pano.limitsiz.ozet` — "Bugün {adet} kayıt yazdın. Limit koymadığın için kalan gösterilmiyor." */
export function panoLimitsizOzet(adet: number): string {
  return `Bugün ${adet} kayıt yazdın. Limit koymadığın için kalan gösterilmiyor.`;
}

/** `Günlük limit {tutar}` — kahraman kartın sağ üst etiketi (prototip). */
export function gunlukLimitEtiketi(tutar: string): string {
  return `Günlük limit ${tutar}`;
}

/** `Günlük toplam {tutar}` — `kayitlar.gun_toplam` */
export function gunToplamEtiketi(tutar: string): string {
  return `Günlük toplam ${tutar}`;
}

/** `Bu ay {sira}. limit aşımı` — `pano.limit_sorgu.baslik` */
export function limitSorguBasligi(sira: number): string {
  return `Bu ay ${sira}. limit aşımı`;
}

/** `ekle.taksit.onizleme` — "Ayda {tutar} · {ay} ay" */
export function ekleTaksitOnizleme(tutar: string, ay: number): string {
  return `Ayda ${tutar} · ${ay} ay`;
}

/** `ekle.limit_disi_uyari` — "Bu harcama günlük limitin {fark} üzerine çıkarır." */
export function ekleLimitDisiUyari(fark: string): string {
  return `Bu harcama günlük limitin ${fark} üzerine çıkarır.`;
}

/** `toast.kaydedildi` — "{tutar} kaydedildi" */
export function toastKaydedildi(tutar: string): string {
  return `${tutar} kaydedildi`;
}

/** `toast.kaydedildi_limit_disi` — "{tutar} kaydedildi · {fark} limit dışı" */
export function toastKaydedildiLimitDisi(tutar: string, fark: string): string {
  return `${tutar} kaydedildi · ${fark} limit dışı`;
}

/** `toast.tekrarlandi` — "{tutar} yeniden eklendi" (Akış C · Latte Faktörü) */
export function toastTekrarlandi(tutar: string): string {
  return `${tutar} yeniden eklendi`;
}

/** `detay.taksit_bilgi` — "{mevcut}/{toplam} taksit · her ay {tutar}" */
export function detayTaksitBilgi(mevcut: number, toplam: number, tutar: string): string {
  return `${mevcut}/${toplam} taksit · her ay ${tutar}`;
}

/** `sil.govde_taksit` — "Kalan {adet} taksit de silinecek. Geri alınamaz." */
export function silGovdeTaksit(adet: number): string {
  return `Kalan ${adet} taksit de silinecek. Geri alınamaz.`;
}

/** `kayitlar.gun_toplam_limit_disi` — "{tutar} · limit dışı" */
export function kayitlarGunToplamLimitDisi(tutar: string): string {
  return `${tutar} · limit dışı`;
}

/** `kayitlar.ay_ozet` — "{adet} kayıt · {tutar}" */
export function kayitlarAyOzeti(adet: number, tutar: string): string {
  return `${adet} kayıt · ${tutar}`;
}

/** `kayitlar.yer_tutucu.baslik` — "{ay} kayıtları" */
export function kayitlarYerTutucuBasligi(ay: string): string {
  return `${ay} kayıtları`;
}

/* --------------------------------------------------------- E-15 kategori */

/** `kategori.bu_ay` — "Bu ay {tutar}" */
export function kategoriBuAy(tutar: string): string {
  return `Bu ay ${tutar}`;
}

/** `kategori.limit_ust` — "Aylık limit {tutar}" */
export function kategoriLimitUst(tutar: string): string {
  return `Aylık limit ${tutar}`;
}

/** `kategori.limit_disi` — "Aylık limitin {fark} üzerinde" */
export function kategoriLimitDisi(fark: string): string {
  return `Aylık limitin ${fark} üzerinde`;
}

/** `kategori.ortalama` — "Günlük ortalama {tutar}. Tahmini." */
export function kategoriOrtalama(tutar: string): string {
  return `Günlük ortalama ${tutar}. Tahmini.`;
}

/** `kategori.adet` — "{adet} kayıt" */
export function kategoriAdet(adet: number): string {
  return `${adet} kayıt`;
}

/** boş durum başlığı — "{kategori} için kayıt yok" */
export function kategoriBosBaslik(kategoriAdi: string): string {
  return `${kategoriAdi} için kayıt yok`;
}

/** `a11y.kategori_gun` — "{gun} {ay}" (E-15 satır erişilebilirliği) */
export function kategoriGunEtiketi(gun: string, ay: string): string {
  return `${gun} ${ay}`;
}

/* ------------------------------------------------------------- E-16 özet */

/** `ozet.hafta_araligi` biçiminde tarih aralığı zaten `lib/tarih.ts#haftaAraligi`de. */

/** `ozet.gecen_gun_ortalama` — "Geçen {adet} günün ortalaması" */
export function ozetGecenGunOrtalama(adet: number): string {
  return `Geçen ${adet} günün ortalaması`;
}

/** `ozet.limit_cizgisi` — "günlük limit {tutar}" */
export function ozetLimitCizgisi(tutar: string): string {
  return `günlük limit ${tutar}`;
}

/** `ozet.limit_alti_gun` — "Bu hafta {adet} gün limit altında." */
export function ozetLimitAltiGun(adet: number): string {
  return `Bu hafta ${adet} gün limit altında.`;
}

/** `ozet.limit_disi_gun` — "Bu hafta {adet} gün limit dışı." */
export function ozetLimitDisiGun(adet: number): string {
  return `Bu hafta ${adet} gün limit dışı.`;
}

/** `ozet.en_cok` + kategori adı — "En çok harcadığın kategori {kategori}" */
export function ozetEnCok(kategoriAdi: string): string {
  return `${t['ozet.en_cok']} ${kategoriAdi}`;
}

/** `ozet.dagilim_gun` — "{adet} gün" */
export function ozetDagilimGun(adet: number): string {
  return `${adet} gün`;
}

/** `ozet.pay` — "%{oran}" */
export function ozetPay(oran: number): string {
  return `%${oran}`;
}

/** `ozet.kucuk_harcama_alt` — "{adet} harcama · ortalama {tutar}" */
export function ozetKucukHarcamaAlt(adet: number, ortalama: string): string {
  return `${adet} harcama · ortalama ${ortalama}`;
}

/** `ozet.taksit_yuku` — "Önümüzdeki ay taksit yükü {tutar}" */
export function ozetTaksitYuku(tutar: string): string {
  return `Önümüzdeki ay taksit yükü ${tutar}`;
}

/** `ozet.limit_sorgu.baslik` — "Günlük limit {tutar}" */
export function ozetLimitSorguBasligi(tutar: string): string {
  return `Günlük limit ${tutar}`;
}

/**
 * `pano.taksit_yuku.alt` (§22.5) — "{adet} seri sürüyor. Sonuncusu {ayYil}
 * tarihinde bitiyor." E-16'daki taksit yükü kartı da aynı cümleyi kullanır
 * (E-10 ve E-16 aynı kavramı — gelecek ayın taksit yükünü — anlatır).
 */
export function taksitYukuAltMetni(adet: number, ayYil: string): string {
  return `${adet} seri sürüyor. Sonuncusu ${ayYil} tarihinde bitiyor.`;
}

/* ---------------------------------------------------------- E-17 limitler */

/** `limitler.toplam_notu` — "Kategori limitleri toplamı {tutar}. Günlük limitinle karşılaştır." */
export function limitlerToplamNotu(tutar: string): string {
  return `Kategori limitleri toplamı ${tutar}. Günlük limitinle karşılaştır.`;
}

/** `limitler.su_anki` — "Şu anki limitin {tutar}." */
export function limitlerSuAnki(tutar: string): string {
  return `Şu anki limitin ${tutar}.`;
}

/** `toast.limit_kaldirildi` — "{kategori} limiti kaldırıldı" */
export function toastLimitKaldirildi(kategoriAdi: string): string {
  return `${kategoriAdi} limiti kaldırıldı`;
}

/** `toast.limit_guncellendi` — "Günlük limit {tutar} olarak güncellendi" */
export function toastLimitGuncellendi(tutar: string): string {
  return `Günlük limit ${tutar} olarak güncellendi`;
}

/** `a11y.kategori_limit_degistir` — "{kategori} limitini değiştir" */
export function a11yKategoriLimitDegistir(kategoriAdi: string): string {
  return `${kategoriAdi} limitini değiştir`;
}

/** `a11y.kategori_limit_kaldir` — "{kategori} limitini kaldır" */
export function a11yKategoriLimitKaldir(kategoriAdi: string): string {
  return `${kategoriAdi} limitini kaldır`;
}

/* --------------------------------------------------------- E-18 taksitler */

/** `taksit.gelecek` — "{ay} ayında {tutar}" */
export function taksitGelecek(ay: string, tutar: string): string {
  return `${ay} ayında ${tutar}`;
}

/** `taksit.seri` — "{kategori} · {mevcut}/{toplam}" */
export function taksitSeri(kategoriAdi: string, mevcut: number, toplam: number): string {
  return `${kategoriAdi} · ${mevcut}/${toplam}`;
}

/** `taksit.bitis` — "{ay} {yil} tarihinde bitiyor" (ay parametresi zaten "Mayıs 2027" biçiminde). */
export function taksitBitis(ayYil: string): string {
  return `${ayYil} tarihinde bitiyor`;
}

/** `taksit.kalan_toplam` — "Kalan toplam {tutar}. Sonuncusu {ayYil} tarihinde bitiyor." */
export function taksitKalanToplam(tutar: string, ayYil: string): string {
  return `Kalan toplam ${tutar}. Sonuncusu ${ayYil} tarihinde bitiyor.`;
}

/** `taksit.seri_bitti` — "{kategori} serisi {ay} ayında bitti. Aylık yük {tutar} düştü." */
export function taksitSeriBitti(kategoriAdi: string, ay: string, tutar: string): string {
  return `${kategoriAdi} serisi ${ay} ayında bitti. Aylık yük ${tutar} düştü.`;
}

/* --------------------------------------------------- v4 · E-10 Günlük */

/** `gunluk.o_gun_limiti` — "O gün limiti {tutar}" */
export function gunlukOGunLimiti(tutar: string): string {
  return `O gün limiti ${tutar}`;
}

/** `gunluk.gun_kapandi` — "Gün kapandı. {adet} kayıt, {tutar}." */
export function gunlukGunKapandi(adet: number, tutar: string): string {
  return `Gün kapandı. ${adet} kayıt, ${tutar}.`;
}

/** `gunluk.gun_kapandi_disinda` — "Gün kapandı. {tutar}, limitin {fark} üzerinde." */
export function gunlukGunKapandiDisinda(tutar: string, fark: string): string {
  return `Gün kapandı. ${tutar}, limitin ${fark} üzerinde.`;
}

/** `seri.cip` a11y — "Seri {n} gün. Seri ekranını aç" · görünen etiket "Seri {n} gün" */
export function seriCipEtiketi(n: number): string {
  return `Seri ${n} gün`;
}
export function seriCipA11y(n: number): string {
  return `Seri ${n} gün. Seri ekranını aç`;
}

/** `gunluk.grup.bugun` / `.kalan` / `.limit_disi` — kategori satırı ikincil bilgisi */
export function gunlukGrupBugun(tutar: string): string {
  return `bugün ${tutar}`;
}
export function gunlukGrupKalan(tutar: string): string {
  return `kalan ${tutar}`;
}
export function gunlukGrupLimitDisi(tutar: string): string {
  return `${tutar} limit dışı`;
}

/** `gunluk.a11y.gruba_ekle` — "{kategori} kategorisine harcama ekle" */
export function gunlukA11yGrubaEkle(kategoriAdi: string): string {
  return `${kategoriAdi} kategorisine harcama ekle`;
}

/* --------------------------------------------------------- v4 · E-21 Seri */

/** `seri.aktif.govde` — "{n} gündür limit altında kapatıyorsun." */
export function seriAktifGovde(n: number): string {
  return `${n} gündür limit altında kapatıyorsun.`;
}

/** `seri.durak.kalan` — "{n} gün kaldı" */
export function seriDurakKalan(n: number): string {
  return `${n} gün kaldı`;
}

/** `seri.durak.sonraki` — "Sıradaki durak {n} gün" */
export function seriDurakSonraki(n: number): string {
  return `Sıradaki durak ${n} gün`;
}

/** `seri.durak.a11y` — "{n} gün durağı geçildi / sırada / ileride" */
export function seriDurakA11y(n: number, hal: 'gecildi' | 'sirada' | 'ileride'): string {
  const kelime = hal === 'gecildi' ? 'geçildi' : hal === 'sirada' ? 'sırada' : 'ileride';
  return `${n} gün durağı ${kelime}`;
}

/** `seri.pencere` — "Son 4 hafta" başlığının altındaki tarih aralığı zaten `haftaAraligi`de. */
export const SERI_PENCERE_BASLIK = 'Son 4 hafta';

/** `seri.gun.a11y` — "{g} {Ay}, limit altında / limit dışı / kayıt yok" */
export function seriGunA11y(gunAy: string, durum: 'altinda' | 'disinda' | 'bos'): string {
  const metin = durum === 'altinda' ? 'limit altında' : durum === 'disinda' ? 'limit dışı' : 'kayıt yok';
  return `${gunAy}, ${metin}`;
}

/** `kutlama.baslik` — "{n} gün" */
export function kutlamaBaslik(n: number): string {
  return `${n} gün`;
}

/** `kutlama.govde` — "Seri {n} güne ulaştı. Sıradaki durak {m} gün." (son durak: "Sıradaki durak yok.") */
export function kutlamaGovde(n: number, sonrakiDurak: number | null): string {
  return sonrakiDurak
    ? `Seri ${n} güne ulaştı. Sıradaki durak ${sonrakiDurak} gün.`
    : `Seri ${n} güne ulaştı.`;
}

/* ----------------------------------------------------- v4 · E-24 Gün seçici */

/** `gunsec.alt.kayitli` — "{n} gün kayıtlı" */
export function gunsecAltKayitli(n: number): string {
  return `${n} gün kayıtlı`;
}

/** `gunsec.alt.acik_gun` — "Açık gün {g} {Ay}" */
export function gunsecAltAcikGun(gAy: string): string {
  return `Açık gün ${gAy}`;
}

/** `gunsec.sinir.baslangic` — "Trinkow'a {g} {Ay}'ta başladın. Daha öncesi yok." */
export function gunsecSinirBaslangic(gAy: string): string {
  return `Trinkow'a ${gAy}'ta başladın. Daha öncesi yok.`;
}

/** `gunsec.ozet.baslik` — "{Ay} özeti" */
export function gunsecOzetBasligi(ayAdi: string): string {
  return `${ayAdi} özeti`;
}

/** `gunsec.a11y.gun` — "{g} {Ay} {GünAdı}, {durum}[, bugün]" */
export function gunsecA11yGun(gAyGunAdi: string, durum: string, bugunMu: boolean): string {
  return bugunMu ? `${gAyGunAdi}, ${durum}, bugün` : `${gAyGunAdi}, ${durum}`;
}

/* ----------------------------------------------------- v4 · E-11 ürün arama */

/** `ekle.arama.satir.gecen` — "{kategori} · geçen sefer {tutar}" */
export function ekleAramaSatirGecen(kategoriAdi: string, tutar: string): string {
  return `${kategoriAdi} · geçen sefer ${tutar}`;
}

/** `ekle.arama.yeni.baslik` — `"{arama}" olarak ekle` */
export function ekleAramaYeniBaslik(arama: string): string {
  return `"${arama}" olarak ekle`;
}

/** `ekle.arama.yeni.alt` — "Kategoriyi ve tutarı sen seç." */
export const EKLE_ARAMA_YENI_ALT = 'Kategoriyi ve tutarı sen seç.';

/** `ekle.tutar.oneri.cip` — "Geçen sefer {tutar}" */
export function ekleTutarOneriCip(tutar: string): string {
  return `Geçen sefer ${tutar}`;
}

/** `ekle.gun.serit` — "Bu kayıt {gün}'e yazılacak." */
export function ekleGunSeridi(gun: string): string {
  return `Bu kayıt ${gun}'e yazılacak.`;
}

/** `a11y.ekle.gun` — "Gün seç, şu an {gün}" */
export function a11yEkleGun(gun: string): string {
  return `Gün seç, şu an ${gun}`;
}

/** `a11y.ekle.kategoriDeger` — "Kategori {ad}, değiştirmek için dokun" */
export function a11yEkleKategoriDeger(ad: string): string {
  return `Kategori ${ad}, değiştirmek için dokun`;
}

/** `a11y.ekle.oneriCip` — "Geçen sefer ödediğin {tutar} tutarını kullan" */
export function a11yEkleOneriCip(tutar: string): string {
  return `Geçen sefer ödediğin ${tutar} tutarını kullan`;
}

/** `a11y.ekle.sonKullanilan` — "{ad}, geçen sefer {tutar}" */
export function a11yEkleSonKullanilan(ad: string, tutar: string): string {
  return `${ad}, geçen sefer ${tutar}`;
}

/* ------------------------------------------------- D-2d-3a · Onboarding */

/** `a11y.ob.gun` — "Ayın {n}. günü" (E-03 gün ızgarası, prototip aria-label deseni). */
export function a11yObGun(gun: number): string {
  return `Ayın ${gun}. günü`;
}

/**
 * `ob.maas.donem` — metinler.md şablonu "Dönem ayın {gun}'inde başlar."
 * statik "'inde" ekini yalnız örnek gün (15) için doğru yazmıştı; 31 günün
 * çoğunda ünlü uyumu farklıdır (bkz. `lib/tarih.ts#gunBulunmaEki`). PM'e
 * bildirildi — metinler.md §2 şablonu güncellenmeli, ek burada TEK yerden
 * hesaplanır (K-040).
 */
export function obMaasDonem(gunEki: string): string {
  return `Dönem ayın ${gunEki} başlar. Limit kalan güne bölünür.`;
}

/** `ob.ozet` maaş günü değeri — 15 → "Ayın 15'i" (`lib/tarih.ts#gunIyelikEki`). */
export function obOzetMaasGunu(gunEki: string): string {
  return `Ayın ${gunEki}`;
}

/** `oneri.nasil.1` — "Aylık net gelirin {tutar}." */
export function oneriNasil1(tutar: string): string {
  return `Aylık net gelirin ${tutar}.`;
}

/** `oneri.nasil.3` — "Sosyal ve keyfi pay {tutar} oldu, maaş döneminde kalan {n} güne bölündü." */
export function oneriNasil3(tutar: string, gunSayisi: number): string {
  return `Sosyal ve keyfi pay ${tutar} oldu, maaş döneminde kalan ${gunSayisi} güne bölündü.`;
}

/** `oneri.denklem.kalan_gun` değeri — "{n} gün" */
export function oneriDenklemKalanGun(gunSayisi: number): string {
  return `${gunSayisi} gün`;
}

/* ------------------------------------------------ D-2d-3b · Katman 2 + Plan */

/** Alışkanlık kartı ayna kuyusu formül satırı — "Günde 1 × 90 ₺ × 30 gün" / "Haftada 1 × 380 ₺ × 30 gün ÷ 7" / "Ayda 1-2 × 130 ₺". */
export function tanFormulMetni(siklikEtiket: string, fiyatYazi: string, haftalikMi: boolean, aylikSayiMi: boolean): string {
  if (aylikSayiMi) return `${siklikEtiket} × ${fiyatYazi}`;
  return haftalikMi ? `${siklikEtiket} × ${fiyatYazi} × 30 gün ÷ 7` : `${siklikEtiket} × ${fiyatYazi} × 30 gün`;
}

/** `tan.yemek.birim` notu — "Günde kaç {birim}" (serbest sayı sorusu etiketi). */
export function tanGundeKac(birim: string): string {
  return `Günde kaç ${birim}`;
}

/** Birikim kartı (E-25) kaydırıcı altı — "Ayda 4.800 ₺ ayırmayı hedefliyorsun." (prototip 17-tanisma.html, anahtarsız). */
export function tanBirikimHedef(tutar: string): string {
  return `Ayda ${tutar} ayırmayı hedefliyorsun.`;
}

/** Birikim kartı alt notu — "Üst sınır sabit giderlerine göre hesaplandı. Zorunlu payın %59." */
export function tanBirikimUstSinirNotu(zorunluYuzde: number): string {
  return `Üst sınır sabit giderlerine göre hesaplandı. Zorunlu payın %${zorunluYuzde}.`;
}

/** `tan.donus.aciklama` — "Dört kart cevapladın. Dördü bekliyor." */
export function tanDonusAciklama(cevaplanan: number, bekleyen: number): string {
  return `${cevaplanan} kart cevapladın. ${bekleyen} bekliyor.`;
}

/** `tan.X.Y kartın Z. kartı` a11y — "8 kartın {n}. kartı" */
export function a11yTanKart(n: number): string {
  return `8 kartın ${n}. kartı`;
}

/** Plan kartı başlığı altı — "Gelir 32.000 ₺" */
export function planGelirEtiketi(tutar: string): string {
  return `Gelir ${tutar}`;
}

/** `plan.pay.yatirim` — "Bunun {tutar}'si yatırım payı." */
export function planPayYatirim(tutar: string): string {
  return `Bunun ${tutar}'si yatırım payı.`;
}

/** Pay satırı yüzde — "%59" (işaret önce, boşluk yok — K-053/K-059/1). */
export function planYuzde(yuzde: number): string {
  return `%${yuzde}`;
}

/** `plan.denklem.kalan_gun` değeri — "{n} gün" */
export function planDenklemKalanGun(gunSayisi: number): string {
  return `${gunSayisi} gün`;
}

/** `plan.nasil.1` — "12.500 + 2.840 + 1.900 + 1.560 = 18.800 ₺. Zorunlu payın bu." (kalemler sıfırsa listeden düşer). */
export function planNasil1(kalemler: string[], toplam: string): string {
  return `${kalemler.join(' + ')} = ${toplam}. Zorunlu payın bu.`;
}

/** `plan.nasil.2` — "32.000 ₺ gelirin %15'i = 4.800 ₺." */
export function planNasil2(gelir: string, yuzde: number, tutar: string): string {
  return `${gelir} gelirin %${yuzde}'i = ${tutar}.`;
}

/** `plan.nasil.3` — "32.000 − 18.800 − 4.800 = 8.400 ₺." */
export function planNasil3(gelir: string, zorunlu: string, birikim: string, sosyal: string): string {
  return `${gelir} − ${zorunlu} − ${birikim} = ${sosyal}.`;
}

/** `plan.nasil.4` — "8.400 ₺ ÷ 28 gün = 300 ₺ günlük limit." */
export function planNasil4(sosyal: string, gunSayisi: number, gunlukLimit: string): string {
  return `${sosyal} ÷ ${gunSayisi} gün = ${gunlukLimit} günlük limit.`;
}

/** Alışkanlık maliyeti listesi satır altı — "Günde 1 × 90 ₺" (formülün kısa hâli, ×30 kartın kendisinde). */
export function planAliskanlikSatirAlt(siklikEtiket: string, fiyatYazi: string): string {
  return `${siklikEtiket} × ${fiyatYazi}`;
}

/** Abonelikler satır altı / ayna kuyusu formülü — "{adet} × {tutar}" (E-25 ve E-26 aynı biçimi kullanır, K-040). */
export function abonelikFormulMetni(adet: number, ortalamaTutar: string): string {
  return `${adet} × ${ortalamaTutar}`;
}

/** `plan.aliskanlik.toplam_not` — "Sosyal ve keyfi payının {tutar}'si. Yasak değil, görünür." */
export function planAliskanlikToplamNot(tutar: string): string {
  return `Sosyal ve keyfi payının ${tutar}'si. Yasak değil, görünür.`;
}

/** `plan.ayar.degisim` — "Sosyal ve keyfi pay {tutar} azaldı. Zorunlu pay değişmedi." */
export function planAyarDegisim(tutar: string, azaldiMi: boolean): string {
  return `Sosyal ve keyfi pay ${tutar} ${azaldiMi ? 'azaldı' : 'arttı'}. Zorunlu pay değişmedi.`;
}

/** Kaydırıcı altı ilk metin (henüz değiştirilmemiş) — "Ayda {tutar}. Fark sosyal ve keyfi paydan iner." */
export function planAyarAltMetin(tutar: string): string {
  return `Ayda ${tutar}. Fark sosyal ve keyfi paydan iner.`;
}

/** `plan.ayar.aralik_en_cok` — "En çok %41" */
export function planAralikEnCok(yuzde: number): string {
  return `En çok %${yuzde}`;
}

/** Gelirsiz limit kartı — "Ayda yaklaşık {tutar}. Tahmini." (günlük × 30) */
export function planGelirsizAylikTahmin(tutar: string): string {
  return `Ayda yaklaşık ${tutar}. Tahmini.`;
}

/** `plan.eksi.tutar` — "Sabit giderlerin gelirini {tutar} aşıyor." */
export function planEksiTutar(tutar: string): string {
  return `Sabit giderlerin gelirini ${tutar} aşıyor.`;
}

/** `plan.eksi.kalan` — "{tutar} eksik" */
export function planEksiKalan(tutar: string): string {
  return `${tutar} eksik`;
}

/* ---------------------------------------------------------- D-2c-1 · E-19 */

/** `ayar.surum` — "Sürüm {surum}" */
export function ayarSurum(surum: string): string {
  return `Sürüm ${surum}`;
}

/** `ayar.plan.kalan` / `.bekliyor` — "{n} kart kaldı" · "8 kart bekliyor" (metinler.md §26.3). */
export function ayarPlanKalan(n: number): string {
  return `${n} kart kaldı`;
}
export function ayarPlanBekliyor(n: number): string {
  return `${n} kart bekliyor`;
}

/** `a11y` — "Maaş günü: {deger}. Değiştir" / "Kip: {deger}. Değiştir" / "Bildirim saati: {deger}. Değiştir" desenleri. */
export function a11yDegerDegistir(etiket: string, deger: string): string {
  return `${etiket}: ${deger}. Değiştir`;
}

/** `hesapsil.veri` — "{n} kayıt dahil tüm verilerin silinir." */
export function hesapsilVeri(n: number): string {
  return `${n} kayıt dahil tüm verilerin silinir.`;
}

/** `sifirla.govde` — "{eposta} adresine şifre bağlantısı gitti." */
export function sifirlaGovde(eposta: string): string {
  return `${eposta} adresine şifre bağlantısı gitti.`;
}

/** `ayar.veri_sil_ozet` — "{adet} kayıt · {ay} {yil}'dan bugüne" */
export function ayarVeriSilOzet(adet: number, ayYil: string): string {
  return `${adet} kayıt · ${ayYil}'dan bugüne`;
}

/* ---------------------------------------------------------- D-2c-1 · E-20 */

/** `prof.gun` — "{n}. gün" */
export function profGun(n: number): string {
  return `${n}. gün`;
}
