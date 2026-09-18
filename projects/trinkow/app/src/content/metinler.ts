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
  'pano.hero.takip': 'bugün kalan',
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
