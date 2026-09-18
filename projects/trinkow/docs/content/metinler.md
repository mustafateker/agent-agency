# Trinkow — Arayüz Metinleri (P-4)

> **Bu dosya tek metin kaynağıdır.** Tasarımda ve kodda buradaki metin
> birebir kullanılır; ajanlar ekranda kendiliğinden cümle uydurmaz.
> Yeni metin gerekiyorsa buraya eklenir, sonra kullanılır.
>
> Ton kaynağı: `projects/trinkow/docs/brand/brandbook.md` §2.2-2.5. Faz 1 · Türkçe.
> Tarih: 2026-09-11 (K-019 temizliği: depolama/mimari anlatan satırlar
> kullanıcı diline çevrildi; `hata.okuma.ayrinti` kaldırıldı)
>
> **v4 birleştirmesi (2026-09-18):** §1'de sekme 1 **"Günlük"** (K-049) ·
> §2 **yeniden yazıldı** (K-053: gelir + maaş günü; geçersiz E-02/E-03
> anahtarları kaldırıldı, K-059/2) · §12 E-20'nin gelir sorusu **emekliye
> ayrıldı** (K-061/3) · §18 "yüzde kullanılmaz" maddesi **kaldırıldı**
> (K-059/1) · §23-§27 yeni ekran metinleri.
> **Bir anahtar bu dosyada tek kez tanımlanır** (K-046); bir metin
> değiştiyse eski satır silinir, "değişti" diye ikinci satır yazılmaz.
>
> **Anahtar sütunu** i18n anahtarıdır (`t('pano.hero.kalan')`). Faz 1'de
> tek dil var ama anahtar üzerinden çalışmak metnin tek yerden
> değişmesini sağlar.

---

## 0. Yazım kuralları (her satır bunlara uyar)

| Kural | Değer |
|---|---|
| Hitap | **sen** — "siz" yok, argo yok |
| Ünlem `!` | **Yasak** (tüm yüzeyler) |
| Emoji | **Yasak** (tüm yüzeyler) |
| Cümle uzunluğu | En fazla **12 kelime** |
| Sıra | Önce **sayı**, sonra (gerekiyorsa) cümle |
| Övgü | Yok ("harika", "süper", "bravo", "tebrikler" yasak) |
| Buton | 1-3 kelime, **fiil önce**: "Harcama ekle", "Kaydet" |
| Buton — **tek istisna** | Üçüncü taraf oturum açma etiketleri (K-057/5): "Apple ile Devam Et" · "Google ile devam et". Sağlayıcının yerelleştirmesidir; kısaltılmaz, yeniden yazılmaz |
| Soru işareti | Yasak değildir (ünlem yasaktır). Soru cümlesi `?` ile biter |
| Yüzde | `%59` — **işaret önce, boşluk yok** (K-053 · K-059/1) |
| Mahremiyet cümlesi | **Kullanıcı faydası dili izinli** ("Harcamaların sende kalır."), **mimari sözcükleri yasak** (SQLite, sunucu, senkron, şifreleme, token) — K-057/1 |
| Para | `1.250,50 ₺` · liste ve kahraman sayıda kuruş yok |
| Negatif | `-60 ₺` yazılmaz → **"60 ₺ limit dışı"** |
| Marka adı | Yalnız `Trinkow`, ek daima kesme işaretiyle |

### 0.1 Kelime dağarcığı (tutarlılık için kilitli)

| Kullanılır | Kullanılmaz |
|---|---|
| limit dışı | aşım, taşma, ihlal, eksi bakiye, borç (limit için) |
| kalan | bakiye, kalan bütçe |
| harcama | işlem, gider, masraf |
| kayıt | veri, entry |
| **oturum aç** (kimlik doğrulama) | **giriş yap** — "giriş" yalnız veri girme anlamında kalır (harcama girişi). Aynı sözcüğün iki anlamı istisnayla değil, sözcüğü ayırarak çözüldü (K-057/6) |
| hesap oluştur | kayıt ol (— "kayıt" harcama kaydına kilitli) |
| seri | streak, alev, zincir |
| biriken | tasarruf ettin, kazandın, kâr |
| öneri | tavsiye, hedef (limit önerisi için) |
| yemek | öğün (K-051: kalori uygulamasının bilgi mimarisi izi taşınmaz) |
| kategori limiti | zarf, kılıf, kova |
| gün sınırı | gün başlangıcı, reset saati |
| nakit / kart | peşin / kredi |
| taksit | vade |

---

## 1. Genel ve navigasyon

| Anahtar | Metin |
|---|---|
| `app.ad` | Trinkow |
| `sekme.gunluk` | Günlük |
| `sekme.kayitlar` | Kayıtlar |
| `sekme.ozet` | Özet |
| `eylem.kaydet` | Kaydet |
| `eylem.kaydediliyor` | Kaydediliyor |
| `eylem.vazgec` | Vazgeç |
| `eylem.sil` | Sil |
| `eylem.duzenle` | Düzenle |
| `eylem.devam` | Devam |
| `eylem.geri` | Geri |
| `eylem.kapat` | Kapat |
| `eylem.simdi_degil` | Şimdi değil |
| `eylem.yeniden_dene` | Yeniden dene |
| `eylem.geri_al` | Geri al |
| `eylem.tekrarla` | Tekrarla |
| `eylem.harcama_ekle` | Harcama ekle |
| `eylem.limiti_degistir` | Limiti değiştir |
| `eylem.tum_kategoriler` | Tüm kategoriler |

---

## 2. Katman 1 — Onboarding (3 soru · K-053)

> **v4'te yeniden yazıldı.** v3'ün E-02 "Günlük limit" ve E-03 "kipe bağlı
> soru" anahtarları **geçersizdir ve silindi** (K-059/2): limit artık
> onboarding'de sorulmuyor, plandan ya da öneriden geliyor. Katman 1
> **zorunlu**, 3 soru; Katman 2 (E-25) isteğe bağlı 8 karttır.

### E-01 — Adım 1/3 · Niyet

| Anahtar | Metin |
|---|---|
| `ob.adim` | Adım 1/3 |
| `ob.niyet.baslik` | Neden buradasın |
| `ob.niyet.aciklama` | Sonra değiştirebilirsin. |
| `ob.niyet.takip` | Param nereye gidiyor |
| `ob.niyet.takip.alt` | Günlük harcamanı görmek istiyorsun. |
| `ob.niyet.tasarruf` | Bütçe yaratmak |
| `ob.niyet.tasarruf.alt` | Her ay bir miktar ayırmak istiyorsun. |
| `ob.niyet.borc` | Borç kapatmak |
| `ob.niyet.borc.alt` | Kalan borcu eritmek istiyorsun. |

> Seçenekler `Card` olarak dikey dizilir; **daire ikon + tek cümle üçlüsü
> kurulmaz.** İkon satırın solunda 24pt.

### E-02 — Adım 2/3 · Aylık net gelir (**atlanabilir**)

| Anahtar | Metin |
|---|---|
| `ob.adim2` | Adım 2/3 |
| `ob.gelir.baslik` | Aylık net gelirin ne kadar |
| `ob.gelir.aciklama` | Planı buna göre kuruyoruz. İstemezsen atla. |
| `ob.gelir.etiket` | Aylık net gelir |
| `ob.gelir.net` | Eline geçen tutar. Kesintiden sonrası. |
| `ob.gelir.bos` | Kesin olması gerekmiyor. Yaklaşık yeter. |
| `ob.gelir.mahremiyet` | Gelirin telefonunda kalır. |
| `ob.gelir.atlarsan` | Atlarsan günlük limiti sen yazarsın. |
| `ob.gelir.atla` | Atla |

### E-03 — Adım 3/3 · Maaş günü

| Anahtar | Metin |
|---|---|
| `ob.adim3` | Adım 3/3 |
| `ob.maas.baslik` | Maaşın hangi gün yatıyor |
| `ob.maas.aciklama` | Günlük limit maaş dönemine bölünür. |
| `ob.maas.duzensiz` | Düzensiz geliyor |
| `ob.maas.donem` | Dönem ayın {gun}'inde başlar. Limit kalan güne bölünür. |
| `ob.maas.duzensiz.not` | Dönem 30 gün sayılır. Maaş günü değişirse ayarlardan düzeltebilirsin. |
| `ob.bitir` | Başla |

### Katman 1 özeti (adım 3/3'ün altında)

| Anahtar | Metin |
|---|---|
| `ob.ozet.limit_yok` | Henüz yok |
| `ob.ozet.limit_not` | Günlük limiti plan kurunca ya da elle yazınca belirlersin. |
| `onboarding.ozet.limitSatiri` | Gelirini yazdığın için sana bir günlük limit önerebiliriz. Kabul etmek zorunda değilsin. |

> `ob.ozet.limit_not` **gelir girilmediğinde**, `onboarding.ozet.limitSatiri`
> **gelir girildiğinde** kullanılır (K-059/5). "Günlük limit — Henüz yok"
> satırı iki hâlde de aynıdır: öneri onaylanana kadar gerçekten limit yoktur.

---

## 3. E-10 — Bugün (Pano)

### 3.1 Kahraman sayı etiketi (kipe göre — brandbook §2.4)

| Kip | Anahtar | Etiket |
|---|---|---|
| Takip | `pano.hero.takip` | bugün kalan |
| Tasarruf | `pano.hero.tasarruf` | bu ay biriken |
| Borç | `pano.hero.borc` | kalan borç |

Kip çipi: `pano.kip.takip` = "Takip" · `pano.kip.tasarruf` = "Tasarruf" ·
`pano.kip.borc` = "Borç". (Arayüzde "Borç Avcısı Modu" **geçmez.**)

### 3.2 Çubuğun altındaki tek satır

| Durum | Anahtar | Metin |
|---|---|---|
| Hiç kayıt yok | `pano.alt.bos` | Bugün henüz bir şey yazmadın. |
| Limit altı | `pano.alt.altinda` | Bugün {harcanan}. Limitinin {fark} altındasın. |
| Limit doldu | `pano.alt.doldu` | Günlük limitin doldu. Bugün {harcanan}. |
| Limit dışı | `pano.alt.disinda` | Limitin {fark} üzerindesin. |
| Limit dışı, çok kayıt | `pano.alt.disinda_adet` | Bugün limit dışı {adet} harcama var. |
| Limit tanımsız | `pano.alt.limitsiz` | Günlük limit tanımlı değil. |

Örnek dolu hâlleri:
- "Bugün 180 ₺. Limitinin 120 ₺ altındasın."
- "Günlük limitin doldu. Bugün 412 ₺."
- "Limitin 60 ₺ üzerindesin."

### 3.2b Limitsiz varyant (günlük limit tanımlı değil · `HeroPlain`)

| Anahtar | Metin |
|---|---|
| `pano.limitsiz.deger` | Limit yok |
| `pano.hero.limitsiz` | bugün harcanan |
| `pano.limitsiz.ozet` | Bugün {adet} kayıt yazdın. Limit koymadığın için kalan gösterilmiyor. |
| `pano.liste.adet` | {adet} kayıt |

Dolu hâli: "Bugün 3 kayıt yazdın. Limit koymadığın için kalan gösterilmiyor."

> `pano.alt.limitsiz` ("Günlük limit tanımlı değil.") **kullanımdan kalktı**:
> ekranın kendisi zaten limitin olmadığını gösteriyor, cümle tekrar ediyordu.
> Sağ üstteki `pano.limitsiz.deger` bir uyarı değil bir **değerdir** — E-17'deki
> `limitler.limit_yok` ile **aynı dize**, iki ekranda aynı şeye aynı ad verilir.
> Liste başlığının sağındaki etiket bu varyantta `pano.liste.adet` olur:
> günlük toplam zaten kahraman sayıdır, iki kez yazılmaz.

### 3.3 Limit kurulumunu sorgulayan kart (imza metni)

| Anahtar | Metin |
|---|---|
| `pano.limit_sorgu.baslik` | Bu ay 6. limit aşımı |
| `pano.limit_sorgu.govde` | Limit gerçekçi mi. Birlikte bakalım. |
| `pano.limit_sorgu.eylem` | Limiti gözden geçir |

> Kural: bu kart ayda **bir kez** gösterilir, 5. aşımdan sonra çıkar,
> kapatılabilir. Suç kullanıcıya değil kuruluma atılır.

### 3.4 Diğer başlıklar

| Anahtar | Metin |
|---|---|
| `pano.bugun_baslik` | Bugün |
| `pano.liste_baslik` | Bugünkü kayıtlar |
| `pano.kalan_kategori` | Kategori limitleri |
| `pano.tumunu_gor` | Tümünü gör |

---

## 4. E-11 — Harcama ekle

| Anahtar | Metin |
|---|---|
| `ekle.baslik` | Harcama ekle |
| `ekle.tutar.etiket` | Tutar |
| `ekle.kategori.etiket` | Kategori |
| `ekle.odeme.etiket` | Ödeme |
| `ekle.odeme.nakit` | Nakit |
| `ekle.odeme.kart` | Kart |
| `ekle.taksit.baglanti` | Taksitli |
| `ekle.taksit.baslik` | Kaç taksit |
| `ekle.taksit.onizleme` | Ayda {tutar} · {ay} ay |
| `ekle.taksit.uygula` | Uygula |
| `ekle.tarih.bugun` | Bugün |
| `ekle.tarih.dun` | Dün |
| `ekle.not.etiket` | Not (isteğe bağlı) |
| `ekle.not.placeholder` | Kısa bir not |
| `ekle.urun.placeholder` | Ne aldın? (isteğe bağlı) |
| `ekle.sik_alinanlar` | Sık alınanlar |
| `ekle.kaydet` | Kaydet |
| `ekle.limit_disi_uyari` | Bu harcama günlük limitin {fark} üzerine çıkarır. |

> Son satır **kaydetmeden önce** gösterilir, kaydı engellemez, kırmızı
> değildir (`edge` şeridi). Kullanıcı durdurulmaz, bilgilendirilir.

---

## 5. E-12 / E-13 — Detay, düzenleme, silme

| Anahtar | Metin |
|---|---|
| `detay.baslik` | Harcama |
| `detay.eklenme` | {tarih} · {saat} eklendi |
| `detay.taksit_bilgi` | {mevcut}/{toplam} taksit · her ay {tutar} |
| `detay.taksit_uyari` | Düzenleme tüm taksit serisini etkiler. |
| `detay.tutar_kilit` | Taksitli kayıtta tutar değiştirilemez. |
| `detay.sil_taksit` | Taksit serisini sil |
| `sil.baslik` | Bu taksit serisi silinecek |
| `sil.govde_taksit` | Kalan {adet} taksit de silinecek. Geri alınamaz. |
| `sil.onayla` | Sil |
| `sil.vazgec` | Vazgeç |

> **D-2a (M-1)** — `detay.tutar_kilit`: taksitli kayıtta tutar tutarı **kilitlidir**
> (satırın tüm serisi etkileneceği için); kategori/ödeme/not gibi tutar da
> düzenlenebilir olsaydı tek bir taksitin tutarını değiştirmek serinin
> toplamıyla tutarsız kalırdı. Tutar yalnız **taksitsiz** kayıtta E-11'deki
> `AmountWell` + `ClayKeypad` deseniyle düzenlenir (bkz. `ekran-envanteri.md`
> F-8).
>
> **K-029 (onaylandı, seçenek C) — silme etkiye göre ikiye ayrılır.**
> `sil.govde` ("Geri alınamaz.") **kaldırıldı**, çünkü artık tek harcama
> silmenin onay diyaloğu yoktur:
>
> | | Tek harcama | Taksit serisi |
> |---|---|---|
> | Onay diyaloğu | **Yok** — dokununca silinir | **Var** (E-13) |
> | Geri alma | `toast.silindi` + `toast.geri_al`, **6 sn** | Yok |
> | Gerekçe | Sık, düşük etkili; her seferinde onay istemek onayı anlamsızlaştırır | Aylara yayılan birden çok kayıt siliniyor |
>
> Bu ayrım §15 (`toast.geri_al`) ve §20 (silme duyurusu) ile tutarlıdır;
> §21.5'teki çelişki böylece kapandı.

---

## 6. E-14 — Kayıtlar

| Anahtar | Metin |
|---|---|
| `kayitlar.baslik` | Kayıtlar |
| `kayitlar.gun.bugun` | Bugün |
| `kayitlar.gun.dun` | Dün |
| `kayitlar.gun.tarih` | {gun} {ay} {gunAdi} |
| `kayitlar.gun_toplam` | Günlük toplam {tutar} |
| `kayitlar.gun_limit_disi` | {tutar} limit dışı |
| `kayitlar.ay_secici` | {ay} {yil} |
| `kayitlar.satir.limit_disi` | limit dışı |
| `kayitlar.satir.taksit` | {mevcut}/{toplam} taksit |
| `kayitlar.satir.nakit` | Nakit |
| `kayitlar.satir.kart` | Kart |

---

## 7. E-15 — Kategori detayı

| Anahtar | Metin |
|---|---|
| `kategori.baslik` | {kategori} |
| `kategori.bu_ay` | Bu ay {tutar} |
| `kategori.limit_var` | Aylık limit {tutar} · kalan {kalan} |
| `kategori.limit_disi` | Aylık limitin {fark} üzerinde |
| `kategori.limit_yok` | Bu kategoride limit yok. |
| `kategori.limit_ekle` | Limit belirle |
| `kategori.ortalama` | Günlük ortalama {tutar}. Tahmini. |
| `kategori.adet` | {adet} kayıt |

---

## 8. E-16 — Özet

| Anahtar | Metin |
|---|---|
| `ozet.baslik` | Özet |
| `ozet.bugun` | Bugün |
| `ozet.hafta` | Bu hafta |
| `ozet.hafta_toplam` | Haftalık toplam |
| `ozet.gunluk_ortalama` | Günlük ortalama |
| `ozet.limit_alti_gun` | Bu hafta {adet} gün limit altında. |
| `ozet.limit_disi_gun` | Bu hafta {adet} gün limit dışı. |
| `ozet.en_cok` | En çok harcadığın kategori |
| `ozet.kucuk_harcama` | 50 ₺ altı {adet} harcama · toplam {tutar} |
| `ozet.taksit_yuku` | Önümüzdeki ay taksit yükü {tutar} |
| `ozet.taksitleri_gor` | Taksitleri gör |

> `ozet.kucuk_harcama` ürünün varlık sebebidir (Latte Faktörü):
> yorum yapılmaz, yalnızca toplanır ve gösterilir.

---

## 9. E-17 — Limitler

| Anahtar | Metin |
|---|---|
| `limitler.baslik` | Limitler |
| `limitler.gunluk` | Günlük limit |
| `limitler.gunluk_aciklama` | Her gün sıfırlanır. Aylık plan değildir. |
| `limitler.kategori_baslik` | Kategori limitleri |
| `limitler.kategori_aciklama` | Aylık. Boş bırakırsan takip edilmez. |
| `limitler.toplam_notu` | Kategori limitleri toplamı {tutar}. Günlük limitinle karşılaştır. |
| `limitler.kaydet` | Kaydet |

---

## 10. E-18 — Taksitler

| Anahtar | Metin |
|---|---|
| `taksit.baslik` | Taksitler |
| `taksit.bu_ay` | Bu ay {tutar} |
| `taksit.gelecek` | {ay} ayında {tutar} |
| `taksit.seri` | {kategori} · {mevcut}/{toplam} |
| `taksit.bitis` | {ay} {yil} tarihinde bitiyor |
| `taksit.aciklama` | Taksitler girildiği güne değil, ait olduğu aya yazılır. |

---

## 11. E-19 — Ayarlar

| Anahtar | Metin |
|---|---|
| `ayar.baslik` | Ayarlar |
| `ayar.bildirim` | Akşam özeti |
| `ayar.bildirim_aciklama` | Günde en fazla bir bildirim. |
| `ayar.bildirim_saat` | Bildirim saati |
| `ayar.bildirim_izin_yok` | Bildirim izni kapalı. Cihaz ayarlarından açabilirsin. |
| `ayar.gun_siniri` | Gün sınırı |
| `ayar.gun_siniri_aciklama` | Gün bu saatte başlar. Gece geç harcayanlar için. |
| `ayar.gun_siniri.0` | 00.00 |
| `ayar.gun_siniri.3` | 03.00 |
| `ayar.gun_siniri.6` | 06.00 |
| `ayar.varsayilan_odeme` | Varsayılan ödeme |
| `ayar.kip` | Kip |
| `ayar.kip_aciklama` | Panodaki büyük sayıyı belirler. |
| `ayar.veri` | Veri |
| `ayar.veri_aciklama` | Kayıtların sende kalır. İstediğin an hepsini silebilirsin. |
| `ayar.veri_sil` | Tüm verileri sil |
| `ayar.veri_sil_onay` | Tüm kayıtların silinecek. Geri alınamaz. |
| `ayar.surum` | Sürüm {surum} |

---

## 12. E-20 — Aşamalı profilleme (F-12)

| Gün | Anahtar | Soru | Seçenekler |
|---|---|---|---|
| 2 | `prof.yatirim` | Yatırım yapıyor musun? | "Yapıyorum" · "Yapmayı düşünüyorum" · "İlgilenmiyorum" |
| 3 | `prof.taksit` | Taksitli alışveriş yapar mısın | "Sık sık" · "Bazen" · "Neredeyse hiç" |
| 4 | `prof.bildirim` | Akşam kısa bir özet göndereyim mi | "Gönder" · "Gönderme" |

| Anahtar | Metin |
|---|---|
| `prof.aciklama` | Cevabın panonu sana göre ayarlar. |
| `prof.simdi_degil` | Şimdi değil |

> **K-061/3 · gelir sorusu emekliye ayrıldı.** `prof.gelir` ve
> `prof.gelir.2` anahtarları **geçersizdir**, kullanılmaz. Gerekçe: gelir
> Katman 1'de (`ob.gelir.etiket`) **tam tutar** olarak alınıyor ve plan
> formülleri (tokens §14.2) tam tutar istiyor; aynı olguyu bir yerde
> aralık, bir yerde tutar olarak sormak iki ayrı doğru üretir. Eksik
> gelir **Ayarlar > Plan ve profil**'den tamamlanır.
> Yerine gelen 2. gün sorusu **Yatırım**'dır ve metni E-25'in 7/8
> kartıyla **birebir aynıdır** (`tan.yatirim.*`, §26): tek soru, tek
> dokunuş, klavye açılmaz.

---

## 13. Boş durumlar (her biri farklı — aynı cümle tekrar edilmez)

| Yer | Başlık | Açıklama | Buton |
|---|---|---|---|
| E-10 ilk gün | Bugün boş | Bugün henüz bir şey yazmadın. İlk kahve iyi bir başlangıç. | Harcama ekle |
| E-17 kategori limiti hiç yok | — (başlık yok) | Kategori limiti koymak zorunda değilsin. Günlük limit tek başına çalışır. | Kategori limiti ekle (ikincil) |
| E-14 hiç kayıt | Kayıt yok | Aşağıdaki butonla ilkini ekle. | Harcama ekle |
| E-14 ay boş | Bu ayda kayıt yok | Başka bir ay seçebilirsin. | — |
| E-15 kategori boş | {kategori} için kayıt yok | Bu ay bu kategoride harcama yazmadın. | — |
| E-16 hafta boş | Özet için erken | Birkaç kayıt sonra burada haftalık dağılımı görürsün. | Harcama ekle |
| E-18 taksit yok | Taksitli işlem yok | Kartla taksitli harcama girdiğinde burada listelenir. | — |

> "Henüz veri yok" **hiçbir yerde yazılmaz** (brandbook §7.8).
>
> **Düzeltme (Tur 2 · son kapsam):** "E-10 limit yok" satırı bu tablodan
> **çıkarıldı.** Limit koymamak bir boş durum değil, **geçerli bir seçimdir**;
> "Bir limit olmadan kalan gösterilemez." + "Limit belirle" ikilisi kullanıcıyı
> kapatması gereken bir açık varmış gibi konumluyordu. Yerine §3.5'teki
> **limitsiz** metinleri geçti (`HeroPlain`). E-17'nin kategori boşluğu ise
> bir **bölüm** boşluğudur: başlık ve illüstrasyon almaz, tek cümle + ikincil
> buton alır.

---

## 14. Hata ve doğrulama metinleri

| Anahtar | Metin | Nerede |
|---|---|---|
| `hata.tutar_bos` | Tutar boş kalamaz. | E-11, E-02 |
| `hata.tutar_sifir` | Tutar sıfırdan büyük olmalı. | E-11 |
| `hata.tutar_buyuk` | Bu tutar çok büyük görünüyor. Kontrol et. | E-11 |
| `hata.kategori_yok` | Bir kategori seç. | E-11 |
| `hata.tarih_gelecek` | Gelecek tarihe harcama yazılamaz. | E-11 |
| `hata.limit_negatif` | Limit sıfırdan küçük olamaz. | E-17 |
| `hata.okuma.baslik` | Kayıtlar açılamadı | E-10, E-14 |
| `hata.okuma.govde` | Bir şey ters gitti. Yeniden denemek çoğu zaman yeterli. | E-10, E-14 |
| `hata.okuma.eylem` | Yeniden dene | — |
| `hata.yazma` | Kayıt yazılamadı. Yeniden dene. | E-11 |
| `hata.bilinmeyen` | Beklenmedik bir durum oldu. Yeniden dene. | Genel |

Hata metinlerinde "Hata:", "Geçersiz", ünlem ve büyük harf uyarı yok.

**Depolama/mimari anlatılmaz** (brandbook §2.8): "cihazda", "sunucu",
"veritabanı", "yerel", "senkronizasyon" hiçbir arayüz metninde geçmez.
Hata metni **ne olduğunu değil ne yapacağını** söyler. Bu yüzden Faz 1'de
"Ayrıntıyı gör" gibi teknik bir kapı da yoktur — gösterecek bir şey olsaydı
bile kullanıcının işine yaramazdı.

### 14.1 Tur A'da eklenen anahtarlar (prototip v2 ile birlikte)

| Anahtar | Metin | Nerede |
|---|---|---|
| `ekle.not.ac` | Not | E-11 · not alanını açan pill (alan etiketi yine "Not (isteğe bağlı)") |
| `ob.onizleme.etiket` | Panondaki büyük sayı | E-01 · niyet seçilince çıkan önizleme şeridi |
| ~~`ob.s3.takip.alt`~~ | **GEÇERSİZ** (K-053 · K-059/3): v3'ün E-03 "kategori tohumlama" sorusu düştü. Kategori limitleri artık plandan otomatik tohumlanır ya da E-17'den kurulur | — |
| `a11y.kurulum_ilerlemesi` | Kurulum ilerlemesi | E-01…E-03 · adım göstergesinin `accessibilityLabel`'ı |
| `a11y.cubuk_degeri` | {harcanan} ₺ / {limit} ₺ kullanıldı | E-10 · kahraman göstergenin `accessibilityValue` metni |

---

## 15. Toast metinleri (4 sn, otomatik kaybolur)

| Anahtar | Metin | Şerit rengi |
|---|---|---|
| `toast.kaydedildi` | {tutar} kaydedildi | `accent` |
| `toast.kaydedildi_limit_disi` | {tutar} kaydedildi · {fark} limit dışı | `edge` |
| `toast.silindi` | Harcama silindi | `danger` |
| `toast.tekrarlandi` | {tutar} yeniden eklendi | `accent` |
| `toast.taksit_silindi` | Taksit serisi silindi. | `accent` |
| `toast.limit_guncellendi` | Günlük limit {tutar} olarak güncellendi | `accent` |
| `toast.geri_alindi` | İşlem geri alındı | `accent` |
| `toast.geri_al` | Geri al | eylem etiketi |

> **Geri alma penceresi: 6 sn** (tokens.md §7.9). Geri al düğmesi taşıyan
> toast 4 sn değil **6 sn** durur; pencere toast'ın ömrüyle **birebir**
> aynıdır, böylece görünmeyen bir geri alma süresi oluşmaz. Süre dolunca
> silme kalıcıdır. Kullanılan yerler: `toast.silindi` · `toast.tekrarlandi`.

---

## 16. Bildirim metinleri (günde en fazla 1, akşam)

| Anahtar | Başlık | Gövde |
|---|---|---|
| `bildirim.gunluk_ozet` | Trinkow | Bugün {adet} harcama, {toplam}. Kalan {kalan}. |
| `bildirim.gunluk_ozet_limit_disi` | Trinkow | Bugün {toplam}. Limitin {fark} üzerinde. |
| `bildirim.kayit_yok` | Trinkow | Dün hiç kayıt yok. 20 saniyede tamamlayabilirsin. |
| `bildirim.hafta_sonu` | Trinkow | Bu hafta {toplam}. Günlük ortalama {ortalama}. |

Yasak bildirim kalıpları: "Seni özledik", "Girmeyi unuttun", "Bütçen
tehlikede", "Son şansın", kampanya/duyuru bildirimi.

---

## 17. Kategori adları (Faz 1 — 13 sabit kategori)

Market · Kafe · Restoran · Ulaşım · Akaryakıt · Fatura · Kira ve ev ·
Abonelik · Sağlık · Giyim · Eğlence · Alışkanlıklar · Diğer

İkon eşleşmesi: `projects/trinkow/docs/design/varliklar.md` §1.1.
Kullanıcı kategorisi ekleme **Faz 2**. Kategori adları yargı içermez
(örn. "Gereksiz", "Keyfi" gibi bir kategori yoktur).

---

## 18. Sayı, tarih ve saat biçimleri

> **K-059/1:** "Yüzde Faz 1'de kullanılmaz" maddesi **kaldırıldı.** Mustafa
> yüzde istedi ("maaşın yüzde kaçı birikim"); plan ekranı (E-26), birikim
> kaydırıcısı ve limit önerisi yüzde kullanır.
> Türetilmiş sayıların **formülleri** burada değil, `tokens.md` §14'tedir
> (kalan gün · günlük limit · biriken · öneri) — tek kaynak kuralı.

| Tür | Biçim | Örnek |
|---|---|---|
| Tutar (liste, kahraman) | binlik nokta, kuruş yok | `1.250 ₺` |
| Tutar (giriş, detay) | kuruş virgülle | `1.250,50 ₺` |
| Limit dışı tutar | etiketle | `60 ₺ limit dışı` |
| Gün başlığı | gün + ay + gün adı | `10 Eylül Perşembe` |
| Bugün/dün | özel ad | `Bugün` · `Dün` |
| Saat | nokta ile | `21.30` |
| Ay adları | tam ad | Ocak … Aralık |
| Gün adları | tam ad | Pazartesi … Pazar |
| Yüzde | işaret önce, boşluk yok | `%59` |
| Gün sayısı | sayı + birim | `21 gün` · `28 gün` |
| Tarih (kısa başlık) | gg/aa + gün adı | `10/09 Perşembe` |
| Ay aralığı | iki tarih, en-dash | `21 Ağustos – 17 Eylül` |

---

## 19. Uzun metin / taşma test dizeleri (Tur 2'de bu değerlerle çizilir)

| Test | Değer |
|---|---|
| En uzun tutar | `1.250.000,50 ₺` |
| En uzun kategori adı | `Kira ve ev` |
| En uzun not (60 karakter) | `Akşam yemeği, iki kişi, arkadaşımla ödeme sonradan bölündü` |
| En uzun gün başlığı | `10 Eylül Perşembe · Günlük toplam 12.480 ₺` |
| En uzun buton etiketi | `Limiti gözden geçir` |
| En uzun boş durum cümlesi | `Bugün henüz bir şey yazmadın. İlk kahve iyi bir başlangıç.` |
| Türkçe glif testi | `ğĞ ıI iİ şŞ çÇ öÖ üÜ âîû` |
| Taksit satırı | `12/12 taksit · her ay 1.041,67 ₺` |
| En uzun ürün adı (çip taşması) | `Marlboro Touch Blue 20'lik` |

---

## 20. Erişilebilirlik duyuruları (ekran okuyucu)

| Durum | Duyuru |
|---|---|
| Çubuk (`accessibilityLabel`) | Günlük limit kullanımı |
| Çubuk değeri | {harcanan} / {limit} |
| Kayıt eklendikten sonra | {tutar} kaydedildi. Kalan {kalan}. |
| Limit dışına çıkıldığında | {tutar} kaydedildi. Limitin {fark} üzerinde. |
| Silme sonrası (tek harcama) | Harcama silindi. Geri almak için Geri al düğmesi. |
| Silme sonrası (taksit serisi) | Taksit serisi silindi. |
| Liste satırı | {kategori}, {tutar}, {saat} |

Duyurularda da ünlem ve emoji yoktur; ton aynıdır.

---

## 21. Tur D'de eklenen anahtarlar (E-14 · E-16 · E-12/E-13 · E-00)

> Prototip `projects/trinkow/docs/design/prototip-v3/04…07` çizilirken gereken, §1-§20'de
> karşılığı olmayan metinler. Yazım kuralları §0 ile aynıdır.

### 21.1 E-14 — Kayıtlar

| Anahtar | Metin |
|---|---|
| `kayitlar.ay_ozet` | {adet} kayıt · {tutar} |
| `kayitlar.ay_ozet_bos` | 0 kayıt |
| `kayitlar.onceki_ay` | Önceki ay |
| `kayitlar.sonraki_ay` | Sonraki ay |
| `kayitlar.taksitleri_ac` | Taksitli işlemleri aç |
| `kayitlar.gun_toplam_limit_disi` | {tutar} · limit dışı |
| `kayitlar.yer_tutucu.baslik` | {ay} kayıtları |
| `kayitlar.yer_tutucu.govde` | Liste açılınca burada görünür. |

> `kayitlar.gun_toplam_limit_disi`: gün başlığının sağ tarafı **daima**
> günlük toplamı gösterir. Gün limit dışıysa toplam `warning-ink` olur ve
> yanına birebir "limit dışı" yazılır — amber sinyali hiçbir yerde yalnız
> başına anlam taşımaz (tokens §1.5). Aşım tutarı burada tekrar edilmez;
> o sayı E-10 ve E-16'dadır.

### 21.2 E-16 — Özet

| Anahtar | Metin |
|---|---|
| `ozet.hafta_bu` | Bu hafta |
| `ozet.hafta_araligi` | {bas} – {bit} |
| `ozet.hafta_tamamlanan` | Tamamlanan hafta |
| `ozet.onceki_hafta` | Önceki hafta |
| `ozet.sonraki_hafta` | Sonraki hafta |
| `ozet.gunluk_toplam` | Günlük toplam |
| `ozet.limit_cizgisi` | günlük limit {tutar} |
| `ozet.gecen_gun_ortalama` | Geçen {adet} günün ortalaması |
| `ozet.gun_kisa` | Pzt · Sal · Çar · Per · Cum · Cmt · Paz |
| `ozet.kategori_dagilimi` | Kategori dağılımı |
| `ozet.dagilim_gun` | {adet} gün |
| `ozet.pay` | %{oran} |
| `ozet.kucuk_harcama_baslik` | 50 ₺ altı harcamalar |
| `ozet.kucuk_harcama_alt` | {adet} harcama · ortalama {tutar} |
| `ozet.taksit_alt` | Üç seri sürüyor. Sonuncusu aralıkta biter. |
| `ozet.limit_sorgu.baslik` | Günlük limit {tutar} |

> `ozet.gecen_gun_ortalama` hafta ortasında `ozet.gunluk_ortalama`nın
> **yerini alır**: hafta bitmeden 7'ye bölmek sayıyı yalan yapar.
> `ozet.limit_sorgu.baslik` + mevcut `pano.limit_sorgu.govde` birlikte
> kullanılır; kart kapatılabilir, ısrar etmez.

### 21.3 E-12 / E-13 — Detay ve silme

| Anahtar | Metin |
|---|---|
| `detay.not.etiket` | Not |
| `detay.sil` | Bu harcamayı sil |
| `detay.bulunamadi.baslik` | Bu kayıt bulunamadı |
| `detay.bulunamadi.govde` | Silinmiş olabilir. Listeye dönebilirsin. |
| `detay.bulunamadi.eylem` | Listeye dön |
| `sil.siliniyor` | Siliniyor |

> `detay.not.etiket` E-11'deki `ekle.not.etiket` ("Not (isteğe bağlı)")
> değildir: detayda not zaten yazılmıştır, "isteğe bağlı" bilgisi
> gereksizdir.

### 21.4 Erişilebilirlik etiketleri (Tur D)

| Yer | `accessibilityLabel` |
|---|---|
| E-14 ay okları | Önceki ay · Sonraki ay |
| E-16 hafta okları | Önceki hafta · Sonraki hafta |
| E-16 sütun grafiği | Günlük toplamlar, günlük limit 300 ₺ |
| E-12 kategori kutusu | Kategoriyi değiştir |
| E-12 sil butonu | Bu harcamayı sil |
| E-00 monogram | Trinkow monogramı |

### 21.5 ✅ ÇÖZÜLDÜ — K-029 (Mustafa, seçenek C)

Çelişki: §5 `sil.govde` "Geri alınamaz." derken §20 duyurusu "Geri almak
için Geri al düğmesi." diyordu. **Karar: etkiye göre ayrıştırma.**

- **Tek harcama silme** → onay diyaloğu **yok**, 6 sn'lik **geri al toast'ı** var.
- **Taksit serisi silme** → onay diyaloğu **kalır** (`sil.govde_taksit`).

Uygulandı: §5 tablosu + not · §15 geri alma penceresi · §20 iki duyuru ·
prototip `06-harcama-detay.html` · `ekran-envanteri.md` E-13.

---

## 22. Tur E'de eklenen anahtarlar (E-15 · E-17 · E-18 · E-19 · E-20)

> Prototip `projects/trinkow/docs/design/prototip-v3/08…12` çizilirken gereken, §1-§21'de
> karşılığı olmayan metinler. Yazım kuralları §0 ile aynıdır.

### 22.1 E-15 — Kategori detayı

| Anahtar | Metin |
|---|---|
| `kategori.ay_etiketi` | Bu ay |
| `kategori.limit_ust` | Aylık limit {tutar} |
| `kategori.bar_periyot` | aylık |
| `kategori.liste_baslik` | Bu ayki kayıtlar |
| `a11y.kategori_gun` | {gun} {ay} |

> E-15'te liste satırlarının solunda **kategori ikonu tekrarlanmaz** (bu
> ekranda kategori sabittir); yerine gün kutusu gelir. Bu yüzden satırın
> ekran okuyucu okunuşu E-14'ten farklıdır: "{gun} {ay}, {tutar}, {saat}".

### 22.2 E-17 — Limitler

| Anahtar | Metin |
|---|---|
| `limitler.kategori_periyot` | Aylık |
| `limitler.limit_yok` | Limit yok |
| `limitler.limit_kaldir` | Limiti kaldır |
| `limitler.su_anki` | Şu anki limitin {tutar}. |
| `limitler.bos_takip` | Boş bırakılan kategori takip edilmez. |
| `hata.limit_sifir` | Limit sıfırdan büyük olmalı. Takip istemiyorsan limiti kaldır. |
| `toast.limit_kaldirildi` | {kategori} limiti kaldırıldı |
| `a11y.gunluk_limit_degistir` | Günlük limiti değiştir |
| `a11y.kategori_limit_degistir` | {kategori} limitini değiştir |
| `a11y.kategori_limit_kaldir` | {kategori} limitini kaldır |
| `limitler.kategori_bos` | Kategori limiti koymak zorunda değilsin. Günlük limit tek başına çalışır. |
| `limitler.kategori_ekle` | Kategori limiti ekle |

> `limitler.kategori_aciklama` ("Aylık. Boş bırakırsan takip edilmez.")
> ekranda **iki parçaya** ayrıldı: periyot bilgisi bölüm başlığının sağında
> etiket olarak (`limitler.kategori_periyot`), takip bilgisi ise listenin
> altındaki bilgi şeridinde (`limitler.bos_takip`). Sebep: 13 satırlık bir
> listenin üstünde iki cümlelik açıklama, listeyi ekrandan aşağı itiyordu.
>
> **Limit kaldırma onay istemez** (K-029 ilkesi): veri silinmiyor, takip
> duruyor. Koruma 6 sn'lik `toast.limit_kaldirildi` + "Geri al".

### 22.3 E-18 — Taksitler

| Anahtar | Metin |
|---|---|
| `taksit.bu_ay_etiket` | Bu ay |
| `taksit.gelecek_baslik` | Önümüzdeki aylar |
| `taksit.seriler_baslik` | Süren seriler |
| `taksit.seri_adet` | {adet} seri |
| `taksit.her_ay` | her ay |
| `taksit.son_taksit` | Son taksit bu ay |
| `taksit.kalan_toplam` | Kalan toplam {tutar}. Sonuncusu {ay} {yil} tarihinde bitiyor. |
| `taksit.seri_bitti` | {kategori} serisi {ay} ayında bitti. Aylık yük {tutar} düştü. |

### 22.4 E-19 — Ayarlar

| Anahtar | Metin |
|---|---|
| `ayar.bildirim_kapali_not` | İzin verilene kadar akşam özeti gönderilmez. |
| `ayar.odeme_aciklama` | Yeni harcama bu seçimle açılır. |
| `ayar.veri_sil_baslik` | Tüm kayıtların silinecek |
| `ayar.veri_sil_govde` | Geri alınamaz. Limitlerin ve kurulumun kalır. |
| `ayar.veri_sil_ozet` | {adet} kayıt · {ay} {yil}'dan bugüne |

> `ayar.veri_sil_onay` diyalogda **başlık + gövde** olarak ikiye ayrıldı ve
> gövdeye neyin **kalacağı** eklendi: "Limitlerin ve kurulumun kalır."
> Belirsizlik korkutur; kullanıcı kurulumu baştan yapacağını sanmamalı.
> `ayar.veri_sil_ozet` ne kadar veri gideceğini sayıyla söyler.
>
> E-19'da **Kaydet yoktur** — her ayar dokunulduğu anda geçerlidir.
> Veri bölümünde tek bir teknik sözcük geçmez (brandbook §2.8).

### 22.5 E-20 — Profilleme

| Anahtar | Metin |
|---|---|
| `prof.gun` | {n}. gün |
| `prof.yatirim` | Yatırım yapıyor musun? |
| `prof.taksit` | Taksitli alışveriş yapar mısın? |
| `prof.bildirim` | Akşam kısa bir özet göndereyim mi? |
| `prof.degisti` | Cevabına göre eklendi. Ayarlardan kaldırabilirsin. |
| `pano.taksit_yuku.baslik` | Taksit yükü |
| `pano.taksit_yuku.periyot` | Önümüzdeki ay |
| `pano.taksit_yuku.alt` | {adet} seri sürüyor. Sonuncusu {ay} {yil} tarihinde bitiyor. |

> **Düzeltme:** §12'deki üç soru tabloda soru işaretsiz yazılmıştı; ekranda
> soru cümlesi **soru işaretiyle** biter (Türkçe yazım). Ünlem yasağı
> sürüyor, soru işareti yasak değildir.
> Tutar aralığı yazılırsa kısa çizgi yerine **en-dash** kullanılır
> (`30.000 – 60.000 ₺`), §18 ile uyumlu.
>
> Cevap verildiği an sheet kapanır, ayrı "Kaydet" yoktur. Cevabın
> **karşılığı** panoda görünür (`prof.degisti` + Taksit yükü kartı):
> karşılığı görünmeyen soru ikinci kez cevaplanmaz.

---

## 23. E-10 Günlük (sayfalama · gruplar) ve E-21 Seri — v4

> Sekme 1'in adı **"Günlük"**dür (`sekme.gunluk`, K-049). Gün sayfalama:
> **geçmiş günler solda**; bugün en sağdaki sayfadır (K-055).

### 23.1 Gün sayfalama ve gün başlığı

| Anahtar | Metin |
|---|---|
| `gunluk.baslik.bugun` / `.dun` | Bugün · Dün |
| `gunluk.baslik.tarih` | {gg}/{aa} {GünAdı} → "10/09 Perşembe" |
| `gunluk.ust.tarih` | {g} {Ay} {GünAdı} *(yalnız Bugün/Dün sayfasında)* |
| `gunluk.ust.uzaklik` | {n} gün önce *(tarihli başlıklı sayfalarda)* |
| `gunluk.onceki_gun` / `.sonraki_gun` | Önceki gün · Sonraki gün *(a11y)* |
| `gunluk.ipucu` | Geçmiş günler solda. Sağa kaydır. |
| `gunluk.sinir.ilk_kayit` | İlk kaydın bu gün. Daha geriye kayıt yok. |
| `gunluk.a11y.takvim` | Gün seç |

### 23.2 Kapanmış gün (geçmiş sayfa)

| Anahtar | Metin |
|---|---|
| `gunluk.hero.gecmis` | o gün harcanan |
| `gunluk.o_gun_limiti` | O gün limiti {tutar} |
| `gunluk.gun_kapandi` | Gün kapandı. {adet} kayıt, {tutar}. |
| `gunluk.gun_kapandi_disinda` | Gün kapandı. {tutar}, limitin {fark} üzerinde. |
| `gunluk.seriye_sayildi` / `.seriye_sayilmadi` | Bu gün seriye sayıldı. · Bu gün seriye sayılmadı. |
| `gunluk.liste_baslik.gecmis` | O günün kayıtları |
| `gunluk.gun_bos.hero` | o gün harcanan *(0 ₺ ile)* |

### 23.3 Harcamasız gün ve seri başlangıcı

| Anahtar | Metin |
|---|---|
| `gunluk.harcamasiz.baslik` | Harcamasız gün |
| `gunluk.harcamasiz.govde` | O gün kayıt yok. Kayıtsız gün seriye sayılmaz. |
| `gunluk.harcamasiz.ipucu` | Harcamasız geçtiyse işaretle, seri korunur. |
| `gunluk.harcamasiz.eylem` | Harcamasız işaretle |
| `gunluk.harcamasiz.isaretli` | Harcamasız gün. Seriye sayıldı. |
| `gunluk.seri_baslar.baslik` / `.govde` | Seri bugün başlar · Günü limit altında kapatırsan seri 1 gün olur. |

> Buton **"Harcamasız işaretle"** (2 kelime, §0 sınırı); tam cümle kart
> gövdesinde durur.

### 23.4 Kategoriler kartı (E-10 · yalnız Bugün sayfasında)

| Anahtar | Metin |
|---|---|
| `gunluk.grup.baslik` | Kategoriler |
| `gunluk.grup.alt` | Bu ay · kategori limiti |
| `gunluk.grup.bugun` / `.kalan` / `.limit_disi` | bugün {tutar} · kalan {tutar} · {tutar} limit dışı |
| `gunluk.grup.bugun_yok` | bugün kayıt yok |
| `gunluk.a11y.gruba_ekle` | {kategori} kategorisine harcama ekle |

> **Tek zaman ölçeği kuralı (K-056):** satırın birincil sağ değeri
> **aylık toplam / aylık limit**tir (çubukla aynı ölçek); bugünkü tutar
> ikincil satıra iner. **Günlük kategori limiti diye bir şey yoktur.**

### 23.5 E-21 Seri

| Anahtar | Metin |
|---|---|
| `seri.cip` | Seri {n} gün · *a11y:* "Seri {n} gün. Seri ekranını aç" |
| `seri.baslik` | Seri |
| `seri.hero.birim` | gün |
| `seri.aktif.govde` | {n} gündür limit altında kapatıyorsun. |
| `seri.kirildi` | Seri dün kırıldı. Bugün yeniden başlıyor. |
| `seri.bos.govde` | Seri henüz başlamadı. Bugünü limit altında kapat. |
| `seri.en_uzun` / `.en_uzun_bos` | En uzun seri · Henüz yok |
| `seri.duraklar` | Duraklar |
| `seri.durak.kalan` / `.sonraki` | {n} gün kaldı · Sıradaki durak {n} gün |
| `seri.durak.a11y` | {n} gün durağı geçildi / sırada / ileride |
| `seri.pencere` | Son 4 hafta · {ilk} – {son} |
| `seri.pencere.bos` | Günleri yazdıkça buraya dolacak. |
| `seri.lejant` | limit altında · limit dışı · kayıt yok |
| `seri.gun.a11y` | {g} {Ay}, limit altında / limit dışı / kayıt yok |
| `seri.kural.baslik` | Seri nasıl işler |
| `seri.kural.1` | Günü günlük limitin altında kapatırsan seri sürer. |
| `seri.kural.2` | Kayıt yazmadığın gün sayılmaz. Harcamasız geçtiyse işaretle. |
| `seri.kapali.baslik` / `.govde` / `.ipucu` | Seri kapalı · Seri için günlük limit gerekir. · Limit kurduğunda duraklar ve günler burada görünür. |
| `kutlama.baslik` / `.govde` / `.kapat` | {n} gün · Seri {n} güne ulaştı. Sıradaki durak {m} gün. · Dokununca kapanır *(a11y: "Kutlamayı kapat")* |

> `seri.kirildi` brandbook §2.3'ten **birebir** alınmıştır. Övgü sözcüğü
> ("tebrikler", "harika", "bravo"), ünlem ve emoji hiçbirinde yoktur;
> kutlama metni **tespit + sıradaki durak**tır. Seri tanımı: tokens §14.5.

---

## 24. E-24 Gün seçici (ay ızgarası)

| Anahtar | Metin |
|---|---|
| `gunsec.baslik` | Gün seç |
| `gunsec.bugune_don` | Bugüne dön |
| `gunsec.alt.kayitli` | {n} gün kayıtlı |
| `gunsec.alt.kayit_yok` | kayıt yok |
| `gunsec.alt.acik_gun` | Açık gün {g} {Ay} |
| `gunsec.lejant.altinda` / `.disinda` / `.kayit_yok` | limit altı · limit dışı · kayıt yok |
| `gunsec.lejant.bugun` | Kutunun altındaki nokta bugünü gösterir. |
| `gunsec.sinir.baslangic` | Trinkow'a {g} {Ay}'ta başladın. Daha öncesi yok. |
| `gunsec.bos.baslik` | Bu ayda kayıt yok |
| `gunsec.bos.govde` | Kayıt yazdığın günler burada işaretlenir. Bugünden başlayabilirsin. |
| `gunsec.ozet.baslik` | {Ay} özeti |
| `gunsec.ozet.kayitli_gun` | Kayıt yazılan gün |
| `gunsec.ozet.limit_alti` | Limit altı gün |
| `gunsec.ozet.biriken` | Limit altı günlerde biriken |
| `ozet.biriken.aciklama` | Limit altında kapattığın günlerde artan tutarların toplamı. Limit dışı günler sıfır sayılır. |
| `gunsec.a11y.gun` | {g} {Ay} {GünAdı}, {durum}[, bugün] |
| `gunsec.a11y.onceki_ay` / `.sonraki_ay` | Önceki ay · Sonraki ay *(sınırda: "… yok")* |

> "Biriken"in **formülü** tokens §14.4'tedir. Arayüz **"biriken"** der;
> "tasarruf ettin" ya da "kazandın" yazılmaz.

---

## 25. E-22 Oturum aç · E-23 Hesap oluştur · E-19 Hesap bölümü

> **Sözcük (K-057/6):** kimlik doğrulama **"Oturum aç"**tır. Ekran kodları
> E-22/E-23 ve dosya adları değişmedi; değişen **arayüz metnidir**.
> Hesap hiçbir akışın önkoşulu değildir (K-052): "Hesapsız devam et" her
> iki ekranda 44pt tam genişlikte durur.

### 25.1 Ortak

| Anahtar | Metin |
|---|---|
| `hesap.mahremiyet` | Harcamaların sende kalır. Hesap yalnız seni tanır. |
| `hesap.mahremiyet.ek` | Yedekleme sonraki sürümlerde. |
| `giris.ayirac` | ya da |
| `giris.hesapsiz` | Hesapsız devam et |
| `giris.sosyal.apple` | Apple ile Devam Et *(Apple'ın yerelleştirmesi — değiştirilemez)* |
| `giris.sosyal.google` | Google ile devam et *(Google'ın yerelleştirmesi — değiştirilemez)* |
| `alan.eposta` / `.eposta_ph` | E-posta · ornek@eposta.com |
| `alan.sifre` / `.sifre_ph.giris` / `.sifre_ph.kayit` | Şifre · Şifreni yaz · Şifre belirle |
| `alan.sifre.gorunur` / `.gizli` | Şifreyi göster · Şifreyi gizle *(a11y)* |

> Sağlayıcı kümesi platforma göre değişir (K-058): **iOS** Apple + Google,
> **Android** yalnız Google. Metin ikisinde de aynıdır.

### 25.2 E-22 Oturum aç

| Anahtar | Metin |
|---|---|
| `giris.baslik` | Oturum aç |
| `giris.eylem` / `.mesgul` | Oturum aç · Oturum açılıyor |
| `giris.unuttum` | Şifremi unuttum |
| `giris.kayit_kapisi` | Hesap oluştur |
| `hata.eposta_bicim` | Geçerli bir e-posta yaz. |
| `hata.kimlik` | E-posta ya da şifre yanlış. Yeniden dene. |
| `hata.eposta_bos` | Önce e-postanı yaz. |
| `hata.baglanti.giris` | Oturum açmak için bağlantı gerekir. Kayıtların bağlantısız çalışır. |
| `sifirla.baslik` / `.govde` / `.ipucu` | Bağlantıyı gönderdik · {eposta} adresine şifre bağlantısı gitti. · Gelmediyse istenmeyen klasörüne bak. |
| `sifirla.yeniden` / `.bekle` | Yeniden gönder · 60 saniye sonra yeniden gönderebilirsin. |
| `sifirla.geri` | Oturum açmaya dön |

> Kimlik hatası bilerek **genel**: hangi adreslerin kayıtlı olduğu
> sızdırılmaz. Şifre sıfırlama **ayrı ekran değil**, E-22'nin bir durumudur.

### 25.3 E-23 Hesap oluştur

| Anahtar | Metin |
|---|---|
| `kayit.baslik` | Hesap oluştur |
| `kayit.eylem` / `.mesgul` | Hesap oluştur · Hesap oluşturuluyor |
| `kayit.sifre_kural` / `.sifre_kural_tamam` | En az 8 karakter. · Uzunluk yeterli. |
| `kayit.yasal` | Hesap oluşturarak **Kullanım şartları** ve **Gizlilik politikasını** kabul ediyorsun. |
| `kayit.giris_kapisi` | Hesabın var mı · Oturum aç |
| `hata.eposta_kayitli` | Bu e-posta ile hesap var. Oturum aç. |
| `hata.baglanti.kayit` | Hesap açmak için bağlantı gerekir. Kayıtların bağlantısız çalışır. |

> ⏸️ `kayit.yasal`'ın iki bağlantısı **yer tutucudur**: gizlilik politikası
> ve kullanım şartları metinleri henüz yazılmadı (K-057/7 · yayın
> bloklayıcısı).

### 25.4 E-19 · Hesap bölümü

| Anahtar | Metin |
|---|---|
| `ayar.hesap.baslik` | Hesap |
| `ayar.hesap.aciklama` | Hesap yalnız seni tanımak için. |
| `ayar.hesap.eposta` | E-posta |
| `ayar.hesap.saglayici` | Google ile bağlı. *(varyant: Apple ile bağlı. · Şifre ile bağlı.)* |
| `ayar.hesap.cikis` / `.cikis_not` | Çıkış yap · Çıkınca kayıtların sende kalır. |
| `ayar.hesap.sil` | Hesabı sil |
| `ayar.hesap.kapali` / `.kapali_kapi` | Hesap isteğe bağlı. Kayıtların sende kalır. · Oturum aç ya da hesap oluştur |
| `hesapsil.baslik` / `.govde` | Hesabın silinecek · Geri alınamaz. Bu e-posta ile bir daha oturum açamazsın. |
| `hesapsil.veri` | {n} kayıt sende kalır. Silmek istersen Veri bölümünü kullan. |
| `hesapsil.eylem` | Hesabı sil |

> Çıkış için onay diyaloğu **yok**, hesap silme için **var** (K-029 ölçütü:
> yüksek etkili + geri alınamaz). Hesap silmek yerel veriyi silmez.

---

## 26. Katman 2 (E-25 Seni tanıyalım) · E-26 Planın hazır · Ayarlar

### 26.1 E-25 — Seni tanıyalım (8 kart, hepsi atlanabilir)

| Anahtar | Metin |
|---|---|
| `tan.baslik` | Seni tanıyalım |
| `tan.aciklama` | Sekiz kart. Her birini atlayabilirsin. |
| `tan.fiyat_vaadi` / `.alt` | Fiyatları biz tahmin etmiyoruz. · Ne kadar ödediğini sen yazıyorsun. |
| `tan.atla` | Bu kartı atla |
| `tan.sabit.baslik` / `.aciklama` | Sabit giderler · Her ay kesin çıkan tutarlar. Bilmediğini boş bırak. |
| `tan.sabit.kira` / `.fatura` / `.ulasim` / `.kredi` | Kira ve aidat · Faturalar · Ulaşım ve yakıt · Kredi ve taksit |
| `tan.siklik.etiket` | Ne sıklıkla |
| `tan.siklik.*` | Günde 1 · Günde 2 · Haftada 2-3 · Haftada 1 · Ayda 1-2 · Hiç · Kendim yazayım |
| `tan.kahve.baslik` / `.aciklama` / `.fiyat` | Kahve · Dışarıda aldığın kahve. Evde yaptığın sayılmaz. · Bir fincan kaç lira |
| `tan.sigara.baslik` / `.aciklama` / `.fiyat` | Sigara · Sıklığı ve kendi ödediğin fiyatı yazıyorsun. · Bir paket kaç lira |
| `tan.yemek.baslik` / `.aciklama` | Dışarıda yemek · Öğle yemeği, akşam yemeği, paket sipariş. |
| `tan.yemek.fiyat` / `.birim` | Bir yemek kaç lira · yemek *(serbest sayıda "Günde kaç yemek")* |
| `tan.hic.not` | Hiç dedin. Bu kart planda görünmez. |
| `tan.yatirim.baslik` / `.aciklama` | Yatırım · Cevabın yalnız birikimini adlandırmak için. |
| `tan.yatirim.*` | Yapıyorum · Yapmayı düşünüyorum · İlgilenmiyorum |
| `tan.yatirim.sinir` / `.sinir.alt` | Yatırım tavsiyesi vermiyoruz. · Birikimin bir kısmını yatırım payı diye etiketleriz. |
| `tan.birikim.baslik` / `.aciklama` | Birikim hedefi · Sabit giderlerinden sonra kalanın içinden ayrılır. |
| `tan.birikim.etiket` | Gelirin yüzdesi |
| `tan.birikim.sinir` / `.sinir.alt` | Üst sınıra geldin. Kaydırıcı burada durur. · Sosyal ve keyfi payı 0 ₺ kalır. |
| `tan.donus.baslik` / `.aciklama` | Kaldığın yerden · Dört kart cevapladın. Dördü bekliyor. |
| `tan.donus.cevaplanmadi` | Cevaplanmadı |
| `tan.donus.plan` | Planı şimdi gör |
| `tan.fiyat.bos` | Fiyatını yaz |

> **"öğün" sözcüğü kullanılmaz** (K-051 · K-061/4). Sigara ve alkol
> kartları diğerlerinin birebir kopyasıdır: uyarı rengi, sağlık mesajı,
> "azaltmayı düşündün mü" yok.

### 26.2 E-26 — Planın hazır

| Anahtar | Metin |
|---|---|
| `plan.baslik` / `.aciklama` | Planın hazır · Cevaplarından çıkardık. Değiştirebilirsin. |
| `plan.pay.zorunlu` / `.zorunlu.alt` | Zorunlu · Kira, fatura, ulaşım, kredi taksiti. |
| `plan.pay.sosyal` / `.sosyal.alt` | Sosyal ve keyfi · Günlük limitin buradan çıkar. |
| `plan.pay.birikim` / `plan.pay.yatirim` | Birikim · Bunun {tutar}'si yatırım payı. |
| `plan.limit.baslik` | Günlük limit |
| `plan.limit.pano` / `.pano.alt` | Panodaki büyük sayı bu olur. · Her maaş döneminde yeniden bölünür. |
| `plan.nasil` | Nasıl hesaplandı |
| `plan.nasil.1` … `.4` | Sabit giderlerini topladık · Birikim hedefini ayırdık · Kalanı sosyal ve keyfi paya yazdık · Dönemde kalan güne böldük |
| `plan.nasil.yuvarlama` / `.yuvarlama.alt` | Hesap kuruş üzerinden yapılır. · Günlük limit tam liraya aşağı yuvarlanır. Yüzdeler tam sayıya yuvarlanır, toplamı 100'e tamamlanır. |
| `plan.aliskanlik.baslik` / `.sag` | Alışkanlık maliyeti · Kendi fiyatlarınla |
| `plan.aliskanlik.toplam_not` | Sosyal ve keyfi payının {tutar}'si. Yasak değil, görünür. |
| `plan.aliskanlik.bos` / `.bos.alt` | Alışkanlık kartlarını cevaplamadın. · Sıklığı ve kendi fiyatını yazarsan aylık tutarı burada görürsün. |
| `plan.ayar.baslik` / `.not` | Payları ayarla · Zorunlu pay sabit kalır. O senin girdiğin sabit giderlerin toplamı. |
| `plan.ayar.degisim` | Sosyal ve keyfi pay {tutar} azaldı. Zorunlu pay değişmedi. |
| `plan.gelirsiz.baslik` / `.aciklama` | Limitini yazalım · Gelirini paylaşmadın. Yüzde planı kurulmadı. |
| `plan.gelirsiz.eldeki` / `.sonra` | Alışkanlık maliyeti gelirsiz de çalışır. · Gelirini sonra da ekleyebilirsin. |
| `plan.eksi.baslik` / `.aciklama` | Plan bu ay kurulamadı · Sabit giderlerin gelirinden fazla. |
| `plan.eksi.tutar` / `.kalan` | Sabit giderlerin gelirini {tutar} aşıyor. · {tutar} eksik |
| `plan.eksi.normalize` | Bu çok rastlanan bir durum. Ölçülebilir olması iyi haber. |
| `plan.eksi.yol1` / `.yol2` / `.yol3` / `.yol3.alt` | Giderleri gözden geçir · Limiti elle yaz · Limitsiz devam et · Takip etmek için plana ihtiyacın yok. Kayıt tutmak tek başına işe yarar. |
| `plan.yarim.baslik` / `.aciklama` | Plan yarım hazır · Dört kart boş. Eldekiyle böldük. |
| `plan.yarim.birikim` | Birikim hedefi girmedin. Şimdilik kalanın tamamı sosyal ve keyfi payında. |
| `plan.kur` | Planı kur |

> Negatif tutar yazılmaz: "{tutar} eksik" (§0). Plan ekranı bir **başarı
> ekranı değil, bir dökümdür** — kutlama, rozet, puan, "finansal sağlık
> skoru" yoktur (K-048 · K-050 · K-053). Formüller: tokens §14.2.

### 26.3 Ayarlar > Plan ve profil

| Anahtar | Metin |
|---|---|
| `ayar.plan.baslik` / `.aciklama` | Plan ve profil · Plan cevaplarından çıkar. İstediğin an değiştir. |
| `ayar.plan.gelirsiz` | Gelirini girmedin. Plan onsuz kurulmuyor. |
| `ayar.plan.kalan` / `.bekliyor` | {n} kart kaldı · 8 kart bekliyor |
| `ayar.plan.gor` | Planı gör |

---

## 27. E-11 ürün arama · Katman 1 limit önerisi

### 27.1 Ürün arama (E-11)

| Anahtar | Metin |
|---|---|
| `ekle.arama.placeholder` | Ne aldın? (isteğe bağlı) |
| `ekle.arama.grup.gecmis` / `.katalog` | Son kullandıkların · Ürünler |
| `ekle.arama.satir.gecen` | {kategori} · geçen sefer {tutar} |
| `ekle.arama.yeni.baslik` / `.alt` | "{arama}" olarak ekle · Kategoriyi ve tutarı sen seç. |
| `ekle.tutar.oneri.cip` | Geçen sefer {tutar} |
| `ekle.tutar.alt.gecmisten` | Tutar geçen seferkinden geldi. Değiştirebilirsin. |
| `ekle.tutar.alt.katalogdan` | Tutarı sen yaz. Fiyat tahmini yapmıyoruz. |
| `ekle.tutar.alt.kategori` | Kategori üründen geldi. Değiştirebilirsin. |
| `ekle.tutar.alt.ikisi` | Tutar ve kategori son kaydından geldi. Değiştirebilirsin. |
| `ekle.gun.serit` | Bu kayıt {gün}'e yazılacak. |
| `ekle.hata.tutar` / `.kategori` | Tutar sıfırdan büyük olmalı. · Bir kategori seç. |
| `ekle.limit.onizleme` | Bu harcama günlük limitin {tutar} üzerine çıkarır. |
| `ekle.hata.yazilamadi` | Kayıt yazılamadı. Yeniden dene. |

**Erişilebilirlik etiketleri (ekranda görünmez):**

| Anahtar | Metin |
|---|---|
| `a11y.ekle.arama` | Ürün ara, isteğe bağlı |
| `a11y.ekle.aramaTemizle` / `.urunKaldir` | Aramayı temizle · Ürünü kaldır |
| `a11y.ekle.gun` | Gün seç, şu an {gün} |
| `a11y.ekle.kategoriDeger` | Kategori {ad}, değiştirmek için dokun |
| `a11y.ekle.oneriCip` | Geçen sefer ödediğin {tutar} tutarını kullan |
| `a11y.ekle.sonKullanilan` | {ad}, geçen sefer {tutar} |

> **Katalogda fiyat yoktur** (K-050 · K-060/1): katalog ne aldığını
> isimlendirir, ne kadar ödediğini **yalnız kullanıcı** söyler. Katalog
> jeneriktir (marka adı taşımaz); marka adı kullanıcının kendi geçmişinden
> gelir. Ürün seçmek **zorunlu değildir**.

### 27.2 Günlük limit önerisi (Katman 1 çıkışı · K-059/5)

| Anahtar | Metin |
|---|---|
| `oneri.baslik` | Günlük limit önerimiz |
| `oneri.pul` | Öneri |
| `oneri.alt` | Sen onaylamadan limit olmaz. |
| `oneri.nasil.baslik` | Nasıl hesaplandı |
| `oneri.nasil.1` | Aylık net gelirin {tutar}. |
| `oneri.nasil.2` | Yaygın bir varsayılan dağılım kullandık: %50 zorunlu, %30 sosyal ve keyfi, %20 birikim. |
| `oneri.nasil.3` | Sosyal ve keyfi pay {tutar} oldu, maaş döneminde kalan {n} güne bölündü. |
| `oneri.serit.1` | Bu sayı senin cevaplarından değil, varsayılan dağılımdan çıktı. |
| `oneri.serit.2` | Sekiz kartı doldurursan plan kendi giderlerinle kurulur. |
| `oneri.btn.kabul` / `.degistir` / `.red` | Limiti kabul et · Başka bir sayı yaz · Limitsiz devam et |

> Öneri **gelir girildiyse** açılır; girilmediyse yüzey hiç görünmez ve
> limitsiz kip devam eder. Formül: tokens §14.3.

