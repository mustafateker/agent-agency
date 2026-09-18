# Durum

Son güncelleme: 2026-09-18 (3. oturum)
Proje: **Trinkow** — harcama takip uygulaması (davranışsal finans / "kalori sayacı")
Mevcut aşama: **2 — UI/UX Tasarım (YENİDEN AÇILDI)** 🔄 · Aşama 3 duraklatıldı
Neden: 2026-09-17'de Mustafa kapsamı genişletti (K-047…K-058). Detay en altta.

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
