# Trinkow REV3 — 2026-09-26 (kapandı)

Mustafa'nın 5 maddelik direktifi uygulandı. Tasarım iki grup hâlinde
`design-reviewer` PASS'i aldı (Günlük+Tasarruf 2 turda, Taksitler 4 turda),
kod indi, QA kapanış kapısı **GEÇTİ**: tsc 0 · mobil **95/95** ·
backend **144/144** · iOS+Android export · `git diff --check` temiz.

| İş | Sonuç |
|---|---|
| Günlük'te rutin bölümü (açılır, "Aldım"/"Almadım" hızlı eylem) | tamam |
| Rutin yönetimi `/rutinler`de kaldı, Günlük'e yalnız günlük eylem taşındı | tamam |
| Tasarruf ekranı akordiyon (ilk bölüm açık, diğerleri katlı) | tamam |
| Menülerde "Geri"/"Ayarlar" yazıları → ikon | tamam |
| Taksitler: toplam + kategori + **ürün bazlı** kırılım | tamam |
| "Seni tanıyalım" kartları | kodda hata yok; Mustafa'nın cihaz denemesi bekliyor |

Bu turda bulunup düzeltilen gerçek hatalar:
- **Seri kuralı metinleri yalan söylüyordu:** dört yerde "günü limit altında
  kapatırsan seri sürer" yazıyordu; kural zaten kayıt temelliydi. Metinler
  düzeltildi, regex testiyle kilitlendi.
- **"Almadım" işareti kalıcı değildi** (yalnız oturum içi). Backend'e
  `vazgecilen_adet` eklendi; kural: gerçek satın alma vazgeçmeyi geçersiz kılar.
- **Rutin verisi geçmiş güne bakarken de "bugün" için sorgulanıyordu.**
- **`taksitKalanToplamKurus` içinde bulunulan ayı sayıyordu** → kalan borç
  olduğundan fazla görünüyordu. Tek çağrı yeri var, izole düzeltildi.
- Ay adı bulunma eki sabitlenmişti ("Eylül'ta") — 12 ayın 8'i bozuktu.

Tasarım denetiminin yakaladığı en kritik kusur: ilk ekran yüksekliği **yanlış
pencere** üzerine ölçülmüştü (766 yerine sekmeli ekranlarda 693, itilen
ekranlarda 769). Tasarruf'ta bir kart 7px kesilecekti.

Test sayısı 14 → **95** (backend 139 → 144).

Sonraki adım: Mustafa'nın cihaz turu + K-093…K-097 kararları. Yayın kapısı
açılmadı.

---
# Trinkow REV2 — 2026-09-26 (kapandı)

Mustafa'nın 11 maddelik oturum direktifi uygulandı. Tasarım iki ekran grubu için
`design-reviewer` PASS'i aldı (her biri bir revizyon turundan sonra), kod indi,
QA kapanış kapısı **GEÇTİ**: tsc 0 · mobil 38/38 · backend 139/139 ·
iOS+Android export · `git diff --check` temiz.

## 2026-09-26 — Seri kuralı: limit aşımı seriyi bozmuyor

Mustafa'nın direktifi: "Seri günlük limiti aşsın ya da aşmasın kayıt girdiği
müddetçe devam etsin."

**Nihai kural:** Bir gün, o gün en az bir harcama kaydı varsa YA DA "harcamasız
gün" işaretlenmişse seriyi sürdürür. Limitin aşılıp aşılmaması seriye etki
etmez; seriyi kıran tek şey o güne hiç kayıt girilmemiş olmasıdır.

- Backend'de kural zaten doğruydu (commit `e92c45a`). Bu turda ölü
  `limit_kurus`/`limitsiz_mi` parametreleri temizlendi, yanlış docstring'ler
  düzeltildi, eksik testler yazıldı.
- İstemcide kopya/eski hesap YOKTU — seri tamamen sunucudan geliyor (K-068).
- **Asıl kusur metinlerdeydi:** dört yerde kullanıcıya "günü limit altında
  kapatırsan seri sürer" deniyordu. Düzeltildi (`seri.kural.1`,
  `gunluk.seri_baslar.govde`, `seri.bos.govde`, `seriAktifGovde`).
- Izgara durumları (`altinda`/`disinda`/`bos`) ve limit karşılaştırması kasıtlı
  olarak KORUNDU: kullanıcı limiti aştığı günleri görmeye devam ediyor.
- Kanıt: backend 141/141 · mobil 45/45 · tsc 0 hata.

| İş | Sonuç |
|---|---|
| Açılışta hata ekranı → giriş ekranı | tamam |
| Kayıt: şifre tekrar · mahremiyet notu kaldırıldı · iki yasal onay checkbox'ı | tamam |
| Kurulum: SetupShell + sabit adım göstergesi, seçenek kartları, animasyonlu geçiş | tamam |
| Kurulum metinleri motive edici tona çekildi ("Hadi başlayalım!") | tamam |
| Adım 2 "Gelir ve Gider" + analiz/plan açıklaması + niyete göre hedef etiketi | tamam |
| "maaş" dili tüm ekranlarda "gelir"e çevrildi ("maaş günü" kavramı korundu) | tamam |
| Navigasyon: `+` FAB kaldırıldı, 3 sekme | tamam |
| Harcama ekle: kategori seçimi ve sabit ödeme bölümü kaldırıldı | tamam |
| Günlük boş durum CTA'sı → kategori listesi (kategorisiz kayıt yolu kapandı) | tamam |
| Tasarruf + Profil baştan tasarlandı ve kodlandı | tamam |
| Canlılık: Profil aksan oranı %3 → %21,9 | tamam |

Turda bulunup düzeltilen iki gerçek hata: Profil ekranı ağ hatasında sessizce
"bütçen/limitin/rutinin yok" gösteriyordu (yanlış finansal bilgi) · `/birikimler`
rotası oturum korumasına eklenmemişti. İkisi de regresyon testiyle kilitlendi.

Test sayısı 14 → 38. Bileşen envanteri 70 → 81, ekran envanteri 21 → 25 yüzey.

Sonraki adım: Mustafa'nın cihaz turu (aşağıdaki doğrulama listesi) + K-093…K-096
kararları. Yayın kapısı hâlâ açılmadı.

---
# Trinkow Rev — 2026-09-23

## 2026-09-24 — Onboarding rutin akışı sadeleştirmesi

- Amaç ve maaş/aylık plan adımlarının ana eylemi `Sonraki` oldu.
- Onboarding rutin adımında hazır Kahve/Sigara/Yemek kısayolları kaldırıldı; doğrudan `Rutin ekle` formu gösteriliyor.
- Kurulum içindeki rutin kartında yalnız `Düzenle` ve `Rutini kaldır` var. Harcama ekleme ve günlük vazgeçme kontrolleri normal Rutinler ekranında kalıyor.
- Kanıt: mobil 14/14, TypeScript, iOS+Android export ve `git diff --check` temiz.

## 2026-09-24 — Günlük harcamaları kategori altında gruplama

- Günlük hareketler ürün adı, saat ve tutarla ilgili kategorinin altında gösteriliyor; hareket satırı düzenleme ekranına açılıyor.
- Günlük hızlı listeden `Abonelik`, `Fatura`, `Kira ve ev` çıkarıldı. Mevcut kayıtları kaybetmemek için bu üç kategori Günlük'te ayrı `Planlı ödemeler` listesinde görünür.
- Kanıt: mobil 14/14, TypeScript, iOS+Android export ve `git diff --check` temiz.

## 2026-09-24 — Günlük kahraman tutar düzeltmesi

- Dört haneli tutarlar (`1.000` ve üzeri) gösterge iç alanına göre `hero`dan `display` ölçeğine iner; daha uzun tutarlar tek satırda otomatik küçülür.
- Günlük kartın sol üstündeki niyet çipi (`Takip` vb.) ve sağ üstündeki günlük limit çipi kaldırıldı.
- Kanıt: mobil 14/14, TypeScript, iOS+Android export, backend sağlık 200 ve `git diff --check` temiz.

## 2026-09-24 — Profil sekmesi ve hızlı kategori harcaması

- Ana navigasyon `Günlük / Tasarruf / Profil` olarak güncellendi; Özet, Profil içindeki analiz bağlantısından açılıyor.
- Profil ana sekmesi hesap, uygulama ayarları, bütçe, limit, rutin ve favori girişlerini topluyor.
- Günlük ekranı kategori limiti olmasa da 13 varsayılan kategorinin tamamını gösteriyor. Her satırdaki `+`, harcama formunu ilgili kategori seçili açıyor; satır aynı günün kategori toplamını gösteriyor.
- Kanıt: mobil 14/14, TypeScript, iOS+Android export, backend sağlık 200 ve `git diff --check` temiz.

## 2026-09-23 — Çalışan backend ve navigasyon düzeltmesi

- Eski 8000 süreci yeni `/butce` ve `/tasarruf` router'larını yüklemiyordu; güncel backend yerel MongoDB ile yeniden başlatıldı.
- `backend/requirements.txt` oluşturuldu ve `pyproject.toml` ile eşlendi.
- Alt çubuk etiketi `Tasarruf` oldu; küçük ekran esnekliği, tek satır etiket, sekmelerde `replace`, safe-area ve klavye davranışı düzeltildi.
- Kanıt: sağlık 200, OpenAPI 43 yol, backend 139/139, mobil 14/14, TypeScript, iOS+Android export ve `git diff --check` temiz.

Kullanıcı planı açıkça uygulama için onayladı. Önceki değişiklikler korunacak.
Aktif aşama: Revizyon uygulandı; yayın dışı bağımlılıklar ve cihaz dokunma QA'sı izleniyor.
Kararlar: ayrı tasarruf/birikim; günlük kategori payları; takip serisi; maaş−sabit−hedef birikim takvim ayına bölünür; rutin tasarrufu açık doğrulama; e-posta öncelikli; yerel posta+SMTP; legal taslaklar; push/AI/prod kapsam dışı.

| Görev | Sahip | Durum | Kabul |
|---|---|---|---|
| REV-01 tasarım delta/prototip | UI/UX | tamamlandı | `trinkow-rev.md/html`, 390×844 durumlar |
| REV-02 tasarım denetimi | design-reviewer/root | PASS | tasarruf ve gerçek birikim ayrımı düzeltildi |
| REV-03 bütçe/rutin/favori/tasarruf/seri API | Python finans | tamamlandı | tarihli sözleşme + Mongo kabul testleri |
| REV-04 gerçek auth/reset/rotation/mail | Python auth | tamamlandı | tek kullanım, iptal, rate limit, outbox/SMTP |
| REV-05 native girdiler | frontend ortak | tamamlandı | özel keypad kullanımda yok; native decimal/paste |
| REV-06 tasarruf/onboarding/limit/favori ekranları | frontend finans | tamamlandı | gerçek API + aylık/günlük hesaplar |
| REV-07 auth/ayarlar/legal/hesap ekranları | frontend hesap | tamamlandı | hatırla/reset/export/silme |
| REV-08 QA entegrasyon | QA/root | otomasyon tamamlandı | 139 backend + 14 mobil + doctor + iki bundle |

Dış bağımlılıklar: gerçek SMTP/gönderici; legal işletmeci bilgileri/hukuki kontrol. Yerel outbox akışı uçtan uca geçti; prod/yayın yapılmadı. App Store/Play öncesi gerçek iOS ve Android cihazda dokunma, klavye ve küçük ekran matrisi manuel çalıştırılmalı.
Kanıt: backend 139/139; mobil 14/14; `tsc`; Expo Doctor 21/21; iOS ve Android export; ayrı `trinkow_smoke` DB'de auth→bütçe→rutin→harcama→tasarruf→reset→oturum iptali→hesap silme PASS.
Sonraki adım: gerçek SMTP bilgilerini bağla, legal işletmeci alanlarını hukuk incelemesiyle tamamla ve cihaz kabul matrisini çalıştır.

---
Önceki kayıtlar (tarihsel):

# Durum

Son güncelleme: 2026-09-22 (çalışma zamanı düzeltmeleri)
Proje: **Trinkow** — harcama takip uygulaması (davranışsal finans / "kalori sayacı")
Mevcut aşama: **3 — Geliştirme** · **arayüz TAMAMLANDI**, backend başladı

## 2026-09-22 — güncel çalışma durumu
Önceki oturum notları tarihseldir. Gerçek mimari Expo + Python/FastAPI + MongoDB;
veri sunucudadır. Backend ve API bağlantısı tamamlanmış, QA bu tur yeniden çalıştırılmıştır.
- Atlas TLS el sıkışması başarısız; Atlas verisi/ayarları değiştirilmedi.
- `app/` içinde `npm run dev`: yerel MongoDB (27018) + API (8000) + Expo.
- Mustafa'nın bu oturumdaki talebiyle rastgele ad/şifre girişi eklendi.
  Demo hesaplar gerçek hesaplardan ayrıdır; normal auth şifre doğrulamaya devam eder.
- Açılışta oturum doğrulama, gün sınırı ve onboarding sırası düzeltildi.
  Ağ hatasında oturum korunur; 401 yenileme tekilleştirildi ve ikinci 401 kapatılır.
- Yakalanmayan async hatalar için ilgili ekranlarda hata/yeniden deneme davranışı eklendi.
- 128 backend testi + 8 istemci testi geçti; TypeScript ve iOS/Android export temiz.
- Sosyal giriş / gerçek şifre sıfırlama / bildirim izni / secure-store işleri hâlâ açık;
  bağlı olmayan giriş yöntemleri artık başarılı olmuş gibi davranmaz.
Kurulum: `app/README.md`. Teknik kanıt ve kapsam: `docs/qa-raporu.md` son bölüm.


## 4. oturumun özeti (en üstte — eski notlar tarihseldir)
**Arayüz bitti.** Kodlanan turlar: D-2d-1 (Günlük + seri + gün seçici) · D-2d-2
(ürün arama + 80 kalemlik katalog + `limit_gecmisi`) · D-2d-3a (onboarding Katman 1
+ limit önerisi) · D-2d-3b (Katman 2 + "Planın hazır" + kategori tohumlama + F-11) ·
D-2c-1/1b (Ayarlar + profilleme sheet + Ayarlar'a giriş) · D-2c-2 (oturum aç /
hesap oluştur + API istemcisi + oturum deposu). Şema sürümü **5**. Her turda
`tsc` 0 hata + iOS export temiz, **hiç yeni bağımlılık eklenmedi**.

**Backend başladı** (Mustafa direktifi K-067/K-068): `projects/trinkow/backend/`,
Python + FastAPI + MongoDB, modüler yapı (`modules/<ad>/{controller,service,dto,model}`).
`auth` modülü yazıldı: kayıt · giriş · token yenile · çıkış · ben · hesap sil.

**Temel değişti:** artık "offline-first, veri cihazda" DEĞİL — **veri sunucuda**,
kimlik kendi backend'imizde JWT ile (Supabase düştü). `CONTEXT.md` güncellendi.

### 🔵 Mustafa'da bekleyen kararlar (hepsi ilerlemeyi yavaşlatıyor)
1. **Yerel MongoDB yok** (BE-2a/K-069) — brew kurulumu / Docker / mevcut bağlantı?
   Backend testleri gerçek veritabanına karşı **hiç çalıştırılamadı**.
2. **K-073** — "Hesapsız devam et" K-068 ile çelişiyor: hesap zorunlu mu, misafir
   hesabı mı? PM eğilimi: misafir hesabı.
3. **Bağımlılık onayı:** `expo-notifications` (bildirim izni) · `expo-secure-store`
   (token'lar şu an SQLite'ta, yayın öncesi şart) · Google/Apple giriş kütüphaneleri.
4. Eskiden beri bekleyen: gizlilik politikası + kullanım şartları (K-057/7) ·
   tütün fiyatları (K-037) · IG/X hesabı (K-010).

### 🔴 Yayın bloklayıcıları (teknik)
- "Şifremi unuttum" **sahte** — backend'de sıfırlama ucu yok (K-074/3).
- Yenileme token'ı rotasyonu yok (K-069/1).
- Token'lar güvenli depoda değil.
- E-00 açılış ekranı yapılmadı.

### Sıradaki iş (karar gelince)
BE-3 `kullanici` + BE-4 `harcama` modülleri → **BE-6: istemcinin `src/db/*`
katmanının API'ye bağlanması** (K-068'in asıl işi) → D-3 QA (Aşama 4) →
T-5 doküman senkronu (tasarım dokümanları koddan geride kaldı, 12+ madde birikti).

---

## Genel özet
Ürün: harcamaları kalori sayar gibi takip ettiren, günlük limit çubuğuyla
"ödeme acısını" geri getiren **offline-first** mobil uygulama. Sunucu yok,
hesap yok, ücretli servis yok. MVP'de oyunlaştırma/fiş okuma/açık bankacılık
YOK — sadece çekirdek davranışsal döngü.

Stack: **React Native (Expo) + TypeScript**, `expo-sqlite`, `expo-router`,
`react-native-svg`. Faz 1'de backend yok → `python-developer` devrede değil (K-003).

## Tamamlanan aşamalar
- **Aşama 0 — Keşif ✅** `docs/CONTEXT.md` (P-1) üretildi, Faz 1 MVP F-1…F-15'e kırıldı.
- **Aşama 1 — Marka ✅** (K-006, sonra K-021 ile v2.0). Ürün adı **Trinkow**.
  Görsel dil **claymorphism** (K-024/K-027) — üç yön denendi, ilk ikisi reddedildi.
- **Aşama 2 — UI/UX Tasarım ✅** (K-035 onaylandı). `docs/design/prototip-v3/`:
  12 ekran + index, **62 yüzey**, design-reviewer PASS + Mustafa görsel onayı.
  `tokens.md` v3.1 · `bilesen-envanteri.md` v3.1 (33 bileşen) · `varliklar.md` v3.1.
- **Aşama 6 — Büyüme (paralel)** İçerik takvimi hazır (4 hafta, 16 içerik, IG+X).
  Yayın zamanlaması ve hesap açma **Mustafa'da** (K-010).

## 🔄 ŞU AN: Aşama 3 — Geliştirme
Strateji: **yürüyen iskelet önce** (K-036) — önce tek ekran gerçekten çalışsın,
sonra seri üretim. Bu strateji kendini ödedi (aşağıya bak).

- **D-1 ✅ Yürüyen iskelet çalışıyor** (K-039). `app/` · 31 dosya · tsc temiz ·
  simülatörde PM tarafından gözle doğrulandı. Dört bilinmezin dördü de kapandı:
  clay inset RN'de tutuyor · kahraman gösterge prototiple ayırt edilemiyor ·
  `₺`+Montserrat tabular sorunsuz · 4/8/12/16/24 ritmi kaymıyor.
  **Tasarım dili değişmiyor → kalan ekranların önü açık.**
- **D-2a ✅ Günlük döngü KODLANDI** (K-041). E-11 harcama ekle · E-12 detay/
  düzenle · E-13 taksit silme onayı · E-14 kayıtlar · sekme navigasyonu ·
  **Akış C** (sola kaydır → Tekrarla, sağa kaydır → Sil). 51 dosya, tsc 0 hata,
  yeni bağımlılık yok. **Uygulama artık günlük kullanım için tam.**
  ⏳ Mustafa'nın simülatörde gözle doğrulaması bekleniyor.
- **D-1b ✅** — doküman senkronu TAMAM. `tokens.md` §7.6 (seçili çipte halka
  yok) + §7.11 (8+ karakterde tutar `hero`→`display`) kuralları yazıldı,
  `stil.css` + prototip üreteci düzeltildi, üretecin denetimi 12 sayfada 0 bulgu.
- **D-2b ✅** — anlama ekranları KODLANDI: E-16 özet · E-15 kategori detayı ·
  E-17 limitler · E-18 taksitler. 8 yeni bileşen + `db/limitler.ts`/`db/ozet.ts`.
  tsc 0 hata, iOS bundle temiz, yeni bağımlılık yok. K-043 renk devri uygulandı.
- **D-2c 🔴 BLOKLU (K-044)** — çevre ekranları: E-00 açılış, E-01/02/03
  onboarding, E-19 ayarlar, E-20 profilleme. Açılış+onboarding giriş/kayıt
  kararına bağlı. Devirler: K-045 (seçim kartında halka yok), K-046 (metinler.md
  çift tanım temizliği).
- **D-3** — qa-engineer (Aşama 4): tsc + Vitest/Jest, para/tarih/offline riskleri.
  ⚠️ **Aşama kapısı:** Aşama 3'ün çıkış kriteri "planlanan özellikler kodlanmış".
  D-2c bloklu olduğu için kriter KARŞILANMADI → PM qa-engineer'ı kendi başına
  çağırmaz. Mustafa "QA'yı erken başlat" derse istisna olarak açılır.

## ⏳ Mustafa'da: simülatör gözle doğrulaması
D-2a (günlük döngü) + D-2b (anlama ekranları) kodlandı ama henüz gözle
görülmedi. `cd projects/trinkow/app && npx expo start --ios`

## 🔴 Açık bloklayıcı: K-044 — Mustafa'da
Giriş/kayıt ekranı + Google/Apple ile oturum açma isteği, `CONTEXT.md` ve F-13'teki
**"sunucu yok, hesap yok"** temeliyle çelişiyor. Ayrıca Apple Developer ($99/yıl)
ücretli bağımlılığı doğuruyor (K-009 kapısı). Seçenekler DECISIONS.md K-044'te:
**A** hesapsız onaylı akış (PM önerisi) · **B** hesap Faz 3'te, yalnız yedekleme · **C** tam auth + backend.
→ **D-2c (E-00 açılış + E-01/02/03 onboarding) bu karar gelene kadar kodlanmıyor.**

Mustafa'da bekleyen, acil olmayan iki iş:
- **K-037** — Ü-2 için 20-30 tütün markasının güncel fiyatı (Faz 2.5, acil değil).
- **K-010** — IG/X hesabı açma + bekleme listesi formu (Aşama 6).

## Bu projede pahalıya mal olan üç hata (tekrarlamasın)
1. **Sessiz sapma** (K-032): tasarımcı onaylı bir kararı bildirmeden tersine
   çevirdi. Kural: çelişki bulunca sessizce çözme, **bildir**.
2. **Doküman↔kod ayrışması** (K-040): prototip ile `tokens.md` çelişti.
   Kural: **`tokens.md` tek otoritedir**, prototip onu geçersiz kılamaz.
3. **Kesilen oturumun kayıp bulguları** (K-042): 12 Eylül'de oturum ölünce
   ajanın bildirmek üzere tuttuğu bir çelişki rapora hiç ulaşmadı; kodda
   yorum olarak kaldığı için şansa yakalandı. Kural: **PM bir oturumu
   devralırken `src/` içinde çelişki işaretlerini tarar** (🔴 / "çelişki" /
   "rapora bildirildi").

## Teknik hafıza — sonraki geliştiricinin bilmesi gerekenler
- `react-native-svg`'de `stopColor` **alfa taşımaz** → saydamlık `stopOpacity` ile.
  Tarayıcıda görünmez, RN'de opak çıkar. D-1'de tam olarak bu patladı.
- Clay gölgeleri `tokens.md §5`'te hazır `boxShadow` dizesi; `elevation` kullanılmaz.
  Expo New Architecture **şart** (inset gölge buna bağlı; Android 10+).
- **Para kuruş cinsinden integer.** Float yasak.
- Silme (K-029): tek harcama → onaysız + 6 sn geri al toast'ı; taksit serisi → diyalog.
- Sil/Tekrarla mantığı tek yerde: `src/lib/harcamaEylemleri.ts`. Kaydırma
  `gesture-handler`'ın `Swipeable`'ı ile; `_layout.tsx`'te `GestureHandlerRootView` şart.
- **Taksitli kayıtta tutar düzenlenemez** (seri toplamıyla tutarsızlaşır);
  kilit nedeni kullanıcıya `InfoStrip` ile söyleniyor.
- Emoji yasak (K-004). Örnek veri `ORNEK_VERI_SURUMU` ile sürümlü; kullanıcı
  verisi varsa dokunulmuyor.

## Çalıştırma
`cd projects/trinkow/app && npx expo start --ios` · ekran görüntüleri `app/.onizleme/`

## Not
Değişiklikler commit EDİLMEDİ.


---

## 2026-09-17/18 — 3. OTURUM: kapsam genişlemesi + Aşama 2 yeniden açıldı

Mustafa beş yeni istek verdi → yeni yüzeyler doğdu → tasarım kapısı yeniden açıldı.
Kodlama (Aşama 3) bu yüzeyler onaylanana kadar duraklatıldı. **D-1…D-2b kodu sağlam,
değişmedi.**

### Yeni kararlar (DECISIONS.md)
- **K-047/K-052** — Giriş/kayıt ve **Google + Apple oturum açma ONAYLANDI.** Kapsam
  daraltıldı: harcama verisi cihazda kalır, sunucuya senkron YOK, hesap yalnız kimlik.
  "Hesapsız devam et" duruyor → giriş duvarı yok. Kimlik: **Supabase Auth** (ücretsiz katman).
  Apple Developer $99/yıl zaten mağaza şartı. K-044 kapandı.
- **K-048** — **Seri (streak) + milestone MVP'ye alındı** (CONTEXT.md'deki "Faz 2"
  geçersiz). Seri = limit altında kapatılan üst üste gün; gün ancak kayıt varsa ya da
  "Harcamasız gün" işaretlendiyse sayılır. Milestone 3/7/14/30/60/100/180/365.
  Puan/seviye/rozet/lig **kalıcı olarak kapsam dışı**.
- **K-049 + K-055** — Sekme 1 **"Günlük"**, yatay tarih sayfalama. **Bugün en sağdaki
  sayfa, geçmiş sola doğru** (Mustafa "çevir" dedi → takvim konvansiyonu).
  Sınırlar: gelecek yok, ilk kayıt gününden geriye yok.
- **K-050** — Kalori-app uyarlama yasakları: kcal/porsiyon/barkod dili yok, ürün
  kataloğu **fiyat göstermez** (kullanıcı girer, "geçen sefer ₺45"), ürün seçmek zorunlu değil.
- **K-051** — Referans görsel uyarlama haritası (ALINAN / ALINMAYAN).
  Görseller: `docs/design/referans-gorseller/kalori-app-referans/` 01-09.
- **K-053** — Profilleme genişlemesi + **F-9 "3 soru" çelişkisinin çözümü**:
  Katman 1 zorunlu 3 soru · Katman 2 "Seni tanıyalım" atlanabilir ~8 kart ·
  çıktı "Planın hazır" → **günlük limit sosyal pay ÷ kalan gün** formülüyle türetilir.
  **Yatırım tavsiyesi YASAK** (SPK).
- **K-054 / K-056 / K-057 / K-058** — tasarım delta bulgularının karara bağlanması:
  seçili günde halka yok · "Seri 12 gün" · kategori çubuğu aylık/aylık · "Oturum aç"
  sözcüğü · iOS'ta Apple+Google, Android'de yalnız Google · Apple hesabının Android'de
  "şifremi unuttum" ile kurtarılması.

### Tasarım durumu — `docs/design/prototip-v4/`
**16 ekran · 94 yüzey · `denetim.py` 0 bulgu** (v3'e dokunulmadı, tar yedeği alındı).
- T-1 ✅ Günlük (12 durum, tarih sayfalama, milestone kutlaması) + E-21 Seri (5 durum)
- T-1b ✅ E-24 Gün seçici (5 durum, ay ızgarası + Aktif/Limit altı/Tasarruf)
- T-2 ✅ E-22 Oturum aç (8 durum) + E-23 Hesap oluştur (7 durum) + Ayarlar Hesap bölümü
  (çıkış/hesabı sil) + platform kuralı + 4 düzeltme
- T-3 🔄 Profilleme (Katman 1+2) + "Planın hazır" — ÇALIŞIYOR
- T-4 ⏳ E-11 ürün arama revizyonu (F-18)
- T-5 ⏳ `delta-v4.md` → tokens.md / bilesen-envanteri.md / metinler.md / varliklar.md birleştirme
- T-6 ⏳ **design-reviewer delta denetimi (PASS bloklayıcı)** → sonra Mustafa görsel onayı
- B-1 🔄 brandbook mahremiyet + seri dili revizyonu — ÇALIŞIYOR

### ⏳ Mustafa'da bekleyen
- **K-057/7 — gizlilik politikası + kullanım şartları metni YOK → yayın bloklayıcısı.**
  Seçenekler: (A) sade taslağı biz yazalım, sen gözden geçir (PM önerisi) ·
  (B) hazır şablon/servis · (C) avukat.
- K-051 — Pro/paywall + Profil sekmesi: monetizasyon kararı yok, tasarlanmadı.
- K-048 — "Seri dondurma hakkı" Faz 1'de yok; istenirse eklenir.
- Eski bekleyenler: K-037 (tütün fiyatları), K-010 (IG/X hesabı).

### Bu oturumun operasyonel dersi
Aynı dizine **iki ajan** verildi (kazara) → `stil.css` bir kez karşılıklı üzerine
yazıldı, ajanlar fark edip geri koydu. Zarar yok ama kural netleşti: **bir dizin,
bir ajan.** Bu oturumda çalışan ajana müdahale aracı (SendMessage) kapalı olduğu için
brief ilk seferde eksiksiz verilmeli. İki ajan da oturum limitine takılıp kesildi;
brandbook işi kısmen tamamlanmış hâlde bulundu ve tamamlatıldı.
