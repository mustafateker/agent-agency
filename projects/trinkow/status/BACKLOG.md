# Trinkow REV3 — 2026-09-26

Mustafa'nın direktifi: rutinlerin Günlük'e taşınması · geri/ayarlar ikonları ·
Tasarruf'un akordiyona çevrilmesi · Taksitler'de ürün bazlı takip ·
"Seni tanıyalım" kartlarının çıkmaması.

| Görev | Sahip | Durum | Kabul |
|---|---|---|---|
| REV3-01 seri kuralı: limit aşımı seriyi bozmaz + yanlış metinler | python + frontend | tamamlandı | 4 metin düzeltildi, regex testi kilitledi |
| REV3-02 geri/ayarlar ikonları | frontend | tamamlandı | a11y etiketleri korundu |
| REV3-03 "Seni tanıyalım" teşhisi | frontend | kodda hata yok | 10 test eklendi; cihaz denemesi Mustafa'da |
| REV3-04 Günlük rutin + Tasarruf akordiyon tasarımı | ui-ux-designer | tamamlandı | r1 revizyonu sonrası PASS |
| REV3-05 Taksitler tasarımı | ui-ux-designer | tamamlandı | r3 revizyonu sonrası PASS (4 tur) |
| REV3-06 tasarım denetimleri | design-reviewer | tamamlandı | 9 bloklayıcı yakalandı, hepsi kapandı |
| REV3-07 Günlük rutin + Tasarruf akordiyon kodlaması | frontend | tamamlandı | +17 test |
| REV3-08 rutin vazgeçme kalıcılığı (`vazgecilen_adet`) | python + frontend | tamamlandı | backend 144/144, +10 test |
| REV3-09 Taksitler kodlaması | frontend | tamamlandı | +13 test, kalan borç hatası da düzeltildi |
| REV3-10 doküman artıkları + Profil aksan ölçümü | ui-ux-designer | tamamlandı | 4 prototip 0 bulgu |
| REV3-11 QA kapanış | qa-engineer | **GEÇTİ** | tsc 0 · 95/95 · 144/144 · iOS+Android export |
| REV3-12 cihaz doğrulama turu (11 madde, bkz. STAGE.md) | Mustafa | bekliyor | simülatör/gerçek cihaz |
| REV3-13 odak halkası (`:focus-visible`) tüm prototiplerde | ui-ux-designer | bekliyor | tek ekranda çözülmemeli |
| REV3-14 Tasarruf'ta bölüm bazlı yeniden deneme | frontend | bekliyor | tek istek/tek hata modeli değişmeli |
| REV3-15 geçmiş ay taksitleri: Özet'e süzgeç | ui-ux-designer | bekliyor | ay seçici değil, süzgeç (K-T0) |
| REV3-16 `vazgecmeler()` ile `rutinler()` capping mantığının birleştirilmesi | python | bekliyor | iki yerde küçük varyasyon |
| REV3-17 tek kategori dalında 19px oturma | QA | cihaz turunda | animasyonla yumuşatıldı, görsel doğrulama |

---

# Trinkow REV2 — 2026-09-24

Mustafa'nın oturum direktifi: açılış/kayıt akışı düzeltmeleri, onboarding yeniden
tasarımı, navigasyon sadeleştirmesi, harcama ekle temizliği, Tasarruf + Profil
modernizasyonu ve genel "canlılık" turu.

| Görev | Sahip | Durum | Kabul |
|---|---|---|---|
| REV2-01 açılışta hata ekranı yerine giriş · FAB kaldırma · harcama ekle sadeleştirme | frontend | tamamlandı | tsc + 14/14 test temiz |
| REV2-02 onboarding + kayıt tasarımı | ui-ux-designer | tamamlandı | r1 revizyonu sonrası PASS, 20 yüzey · 0 bulgu |
| REV2-03 Tasarruf + Profil tasarımı + canlılık reçetesi | ui-ux-designer | tamamlandı | r1 revizyonu sonrası PASS, 12 yüzey · 0 bulgu |
| REV2-04 tasarım denetimi (2 ekran × 2 tur) | design-reviewer | tamamlandı | ikisi de PASS |
| REV2-05 onboarding + kayıt kodlaması | frontend | tamamlandı | tsc + 14/14, 6 yeni bileşen |
| REV2-08 Günlük boş durum CTA'sı → kategori listesi | frontend | tamamlandı | kategorisiz çağrı tip düzeyinde imkansız |
| REV2-11 denetim şartları + "bütçe dışı" sözlük + Profil aksan takviyesi | ui-ux-designer | tamamlandı | aksan %13,1 → %21,9 |
| REV2-06 Tasarruf + Profil kodlaması | frontend | tamamlandı | 15 yeni bileşen, tsc temiz |
| REV2-12 eksik testler | frontend | tamamlandı | 14 → 38 test |
| REV2-09 ölü dosyalar (`CategoryValueRow`, `LegalConsentText`, `ClayKeypad`) — silme onayı → K-093 | Mustafa | bekliyor | onay sonrası silinir |
| REV2-17 birikim tarih girişi: 21 günlük şerit mi, tarih seçici bağımlılığı mı → K-094 | Mustafa | bekliyor | geçmişe kayıt yolu geri gelir |
| REV2-18 `/birikimler` ekranının kapsama alınması → K-095 | Mustafa | bekliyor | bilgi + onay |
| REV2-19 doküman ekran numarası çakışması → K-096 | PM/tasarımcı | bekliyor | tek numara uzayı |
| REV2-20 cihaz doğrulama turu (6 madde, bkz. STAGE.md) | Mustafa | bekliyor | simülatör/gerçek cihaz |
| REV2-13 doküman senkronu | ui-ux-designer | tamamlandı | 48 düzeltme; bileşen 70→81, ekran 21→25 |
| REV2-15 "maaş" → "gelir" dil tutarlılığı (bütçe/limitler/ayarlar) | frontend | tamamlandı | "maaş günü" kavramı korundu |
| REV2-16 QA bulgu düzeltmeleri (Profil hata durumu · `/birikimler` guard) | frontend | tamamlandı | +5 regresyon testi |
| REV2-07 QA ara regresyon | qa-engineer | tamamlandı (2026-09-25) | BLOCKER 0 · tsc 0 · 14/14 · 139/139 · iOS+Android export |
| REV2-21 seri kuralı: limit aşımı seriyi bozmaz (backend temizlik + istemci metinleri) | python + frontend | tamamlandı (2026-09-26) | 141/141 · 45/45 · tsc 0 |
| REV2-14 QA kapanış + delta | qa-engineer | **GEÇTİ** (2026-09-26) | tsc 0 · 38/38 · 139/139 · iOS+Android export |

---

# Trinkow Rev — 2026-09-23

Kullanıcı planı açıkça uygulama için onayladı. Önceki değişiklikler korunacak.
Aktif aşama: Revizyon kodu ve otomatik QA tamamlandı.
Kararlar: ayrı tasarruf/birikim; günlük kategori payları; takip serisi; maaş−sabit−hedef birikim takvim ayına bölünür; rutin tasarrufu açık doğrulama; e-posta öncelikli; yerel posta+SMTP; legal taslaklar; push/AI/prod kapsam dışı.

| Görev | Sahip | Durum | Kabul |
|---|---|---|---|
| REV-01…07 | ilgili ajanlar + root | tamamlandı | tasarım, backend ve mobil akışlar kodlandı |
| REV-08 otomatik QA | QA/root | tamamlandı | 139 backend, 14 mobil, doctor, iOS/Android bundle |
| REV-09 gerçek cihaz kabul matrisi | QA | yayın öncesi | iOS/Android odak, klavye, küçük ekran, sheet |
| REV-10 SMTP ve legal yayına hazırlık | dış bağımlılık | bekliyor | gönderici bilgisi + işletmeci/hukuk metinleri |

Dış bağımlılıklar: gerçek SMTP/gönderici; legal işletmeci bilgileri/hukuki kontrol. Yerel testleri durdurmaz, prod tamamlandı sayılmaz.
Sonraki adım: yayın kapsamı açıldığında REV-09 ve REV-10.

---
Önceki kayıtlar (tarihsel):

# Backlog

## PROJE: Harcama Takip Uygulaması ("kalori sayacı" mantığı)
Bağlam: `projects/trinkow/docs/CONTEXT.md` (P-1) · Kapsam: **Faz 1 MVP**

### Stack (kesinleşti)
**React Native (Expo) + TypeScript**, offline-first `expo-sqlite`,
`expo-router`, `react-native-svg`. Sunucu yok, backend yok, ücretli servis yok.
Karar: K-002 + K-005. ✅ Açık bloklayıcı yok.

### Sıradaki adım
### ✅ Bloklayıcı yok — Aşama 3 (Geliştirme) sürüyor, Aşama 6 paralel
Ürün adı: **Trinkow** · Görsel dil: **claymorphism** (K-024/K-027).
Not: Yön A "Defter" ve Yön C "Gün Işığı" denendi ve REDDEDİLDİ — geçerli olan
claymorphism'dir. Tasarım onayı K-035.

### F-serisi — Faz 1 MVP özellik kırılımı
Aşama 2'de tasarlanır, Aşama 3'te kodlanır. K-002 kesinleşince stack'e göre
detaylandırılır.

**Çekirdek döngü (ürünün kalbi — bunlar olmadan ürün yok)**
- [ ] **F-1** — Günlük harcama limiti belirleme (kurulum + sonradan değiştirme)
- [ ] **F-2** — Hızlı manuel harcama girişi. **Sürtünme kritik:** tutar +
      kategori en az adımda girilebilmeli. Bu ekran ürünün en çok kullanılan
      ekranı; her fazladan tık kullanıcı kaybı.
- [ ] **F-3** — Kalan limit ilerleme çubuğu ("kalori çubuğu"). Anında
      güncellenir, ana ekranın merkezinde.
- [ ] **F-4** — Kategori bazlı takip + kategori limitleri (zihinsel muhasebe)
- [ ] **F-5** — Günlük/haftalık özet: para nereye gitti?

**Giriş çeşitliliği**
- [ ] **F-6** — Nakit / kart ayrımı
- [ ] **F-7** — Taksitli işlem: tutar aylara yayılır, her ay ilgili taksit
      o günün bütçesine yansır
- [ ] **F-8** — Harcama düzenleme / silme (yanlış giriş kaçınılmaz)

**Onboarding (rapordaki kurallara birebir)**
- [ ] **F-9** — **Zorunlu katmanda** en fazla **3 soru** (K-053: Katman 2 atlanabilir,
      sınır bozulmadı). Ana niyet: Takip / Tasarruf / Borç
- [ ] **F-10** — "Adım 1/3" ilerleme göstergesi
- [ ] **F-11** — Niyete göre **anında kişiselleşen** pano (ör. Borç Avcısı
      Modu). Kullanıcı verdiği bilginin karşılığını hemen görmeli.
- [ ] **F-12** — Aşamalı profilleme: gelir/taksit/bildirim tercihi 1. günde
      DEĞİL, 2-3. günde bağlama uygun sorulur

**Veri**
- [ ] **F-13** — Offline-first yerel veritabanı, sunucu yok, hesap yok
- [ ] **F-14** — Para birimi TL; **para float ile tutulmaz** (kuruş hatası)
- [ ] **F-15** — Gün sınırı/saat dilimi mantığı ("bugün" ne zaman biter?)

**Kapsam DIŞI — MVP'ye sokma:** XP/seviye/streak (Faz 2), fiş okuma (Faz 3),
açık bankacılık (Faz 3), Live Activities, bulut senkron, aile paylaşımı.

---

## P-serisi — Her proje için standart kurulum
Kaynak: `agency/templates/proje-kurulum-checklist.md`
Bu bölüm HER yeni projede aynen tekrarlanır. PM projeye özel notunu ekler.
Bir madde atlanacaksa **gerekçesiyle** "atlandı" olarak işaretlenir, sessizce
silinmez.

### A. Token tasarrufu varlıkları
- [x] **P-1** ✅ (2026-09-10) — `projects/trinkow/docs/CONTEXT.md`: tek sayfalık bağlam paketi (PM, Aşama 0→1).
      Sistemdeki en büyük tek tasarruf kalemi: 9 ajan 20 sayfa yerine 1 sayfa okur.
- [x] **P-2** ✅ (2026-09-10) — `projects/trinkow/docs/brand/tokens.md` + `src/theme/tokens.ts`: brandbook'un
      makine okunur özeti (ui-ux-designer + frontend-developer, Aşama 1→2).
      design-reviewer'ın mekanik denetimi bu dosyaya karşı grep ile çalışır.
- [x] **P-3** ✅ (2026-09-10) — `projects/trinkow/status/HANDOFF.md`: aşama başına 3-5 satır devir-teslim (PM,
      her aşama sonu). PM brief'lerinin "Bağlam" maddesi buradan kopyalanır.
- [x] **P-4** ✅ (2026-09-10) — `projects/trinkow/docs/content/metinler.md`: gerçek ekran metinleri
      (ui-ux-designer, Aşama 2 başı). Lorem ipsum yasağının tek kaynağı.

### B. Tasarım referans varlıkları
- [x] **P-5** ✅ (2026-09-10) — Projeye özel `referans-repolar.md`: global listeden buda +
      alan-bazlı ekle + 5-8 gerçek ilham linki (ui-ux-designer, PM onaylar).
      KURAL: sistematik alınır, görsel stil ALINMAZ.
- [x] **P-6** ✅ (2026-09-10) — `projects/trinkow/docs/design/varliklar.md`: ikon seti (TEK set), fontlar,
      görsel kaynağı, lisanslar — sürümleriyle kilitlenir (ui-ux-designer).
- [x] **P-7** ✅ (2026-09-10) — `projects/trinkow/docs/design/bilesen-envanteri.md`: bileşen listesi + her
      birinin zorunlu state'leri (ui-ux-designer). Revizyon turlarını kapatır.

### C. Hijyen
- [x] **P-8** ✅ (2026-09-10) — Repo hijyeni: `.gitignore`, klasör yapısı, `.env.example`
      (devops-engineer veya PM). grep/glob sonuçlarını temiz tutar.

---

## Devam edenler
### 🔴 Bloklayıcı — Mustafa'da
✅ K-018'in üç sorusu da kapandı: (a) görsel dil gevşetildi (K-019),
(b) yeni palet piyasaya uygun seçilecek, referans moru kopyalanmayacak,
(c) repo geldi ve entegre edildi (K-020).
✅ K-021 onaylandı — Yön C "Gün Işığı".
✅ **Aşama 2 KAPANDI** — tasarım onaylandı (K-035).

### Aşama 3 — Geliştirme
- [x] **D-1** — ✅ Yürüyen iskelet ÇALIŞIYOR. 31 dosya, tsc temiz,
      simülatörde doğrulandı. **Dört bilinmez de kapandı (K-039):** clay inset
      tutuyor, gösterge birebir, `₺`+tabular sorunsuz, ritim kaymıyor.
      SVG alfa hatası bulunup düzeltildi. (2026-09-12)
- [x] **D-1b** — ✅ Doküman↔kod senkronu TAMAM (2026-09-17). `tokens.md` §7.6
      (halka yok) + §7.11 (8+ kar. `hero`→`display`) kuralları yazıldı,
      `stil.css` + `_uret/s02` düzeltildi, `02-harcama-ekle.html` yeniden
      üretildi, `AmountWell.tsx` yorumu sadeleşti. `_uret/denetim.py`:
      12 sayfa, **0 bulgu**. Kapsam dışı bulgu → K-045.
      <details>Orijinal madde:
      (a) **K-040:** `tokens.md §7.6`'ya "seçili çipte halka YOKTUR" yazılsın,
      prototip üreteci halkayı bıraksın. Aynı kural kategori ızgarası
      (`kat-sec-kutu`) için de geçerli — kodda zaten uygulandı (K-041).
      (b) **K-042:** `tokens.md §7.11`'e "8+ karakterde tutar `hero`→`display`
      iner; prototip bunu göstermiyor, **kural geçerlidir**" notu düşülsün,
      prototip üreteci düzeltilsin.</details>
- [x] **D-2a** — ✅ Günlük döngü KODLANDI (K-041 + düzeltme turu). E-11 ekle ·
      E-12 detay/düzenle · E-13 taksit silme onayı · E-14 kayıtlar · sekme
      navigasyonu bağlandı · Akış C kaydırma (Tekrarla/Sil). 51 dosya,
      tsc 0 hata, **yeni bağımlılık yok**. Düzeltme turunda kapatılanlar:
      E-12'de tutar düzenleme (F-8) + Akış C + metin senkronu.
      ⏳ **Mustafa'nın simülatörde gözle doğrulaması bekleniyor.** (2026-09-17)
- [x] **D-2b** — ✅ Anlama ekranları KODLANDI (2026-09-17). E-16 özet ·
      E-15 kategori detayı · E-17 limitler · E-18 taksitler. 8 yeni bileşen,
      `db/limitler.ts` + `db/ozet.ts` veri katmanı. K-043 devri uygulandı
      (`ExpenseRow` sil zemini `danger-soft` / `danger-ink`).
      `tsc --noEmit` 0 hata · `expo export --platform ios` 1778 modül temiz ·
      **yeni bağımlılık yok** (doğrulandı). 5 sapma bildirildi, hepsi kabul;
      biri doküman hatası çıktı → K-046.
      ⏳ **Mustafa'nın simülatörde gözle doğrulaması bekleniyor** (D-2a ile birlikte).
- [ ] **D-2c** — Çevre ekranları: E-00 açılış · E-01/02/03 onboarding ·
      E-19 ayarlar · E-20 profilleme sorusu.
      🔴 **BLOKLU: K-044** (giriş/kayıt kararı Mustafa'da) — açılış ve
      onboarding akışı o karara bağlı.
      **+ Devir (K-045):** `.secim-kart.secili`'den halka kalkar (seçili durum
      yüzey tonu + metin rengiyle). `tokens.md §7.6` + `stil.css` birlikte.
      **+ Devir (K-046):** `docs/content/metinler.md` E-15'i iki kez tanımlıyor
      (§7 vs §22.1). §22.1 geçerli; §7 arşivlenir. Dosyanın tamamı
      çift-tanımlı ekran için taranır.
- [ ] **D-3** — qa-engineer: Vitest/Jest + tsc, para/tarih/offline riskleri.
      **+ Bakılacak (K-043):** yalnız-kaydırmayla erişilen eylemlerin
      VoiceOver/TalkBack erişilebilirliği (`accessibilityActions` yaması yeterli mi?).
- [ ] **K-037** — Mustafa: 20-30 tütün markası güncel fiyat (Ü-2 için).
- [x] **G-010b** — TUR B kalan ekranlar: Aşama 2'de tamamlandı, tasarım
      onaylandı (K-035). Madde kapandı. (2026-09-12)



## Sırada (bunlar bitince)

- [x] **G-006** — design-reviewer denetimi PASS + Mustafa onayı → Aşama 2
      kapandı (K-035). (2026-09-12)
- [ ] **G-008** — Mustafa: IG + X hesabı açma, bekleme listesi formu (K-010)


## Tamamlananlar
- [x] **G-000/G-001** — Proje dökümanı eklendi ve okundu; `projects/trinkow/docs/CONTEXT.md`
      (P-1) üretildi, MVP Faz 1 kapsamı F-serisi olarak kırıldı.
      **Aşama 0 çıkış kriteri karşılandı.** (2026-09-10)
- [x] **P-1** — `projects/trinkow/docs/CONTEXT.md` bağlam paketi. (2026-09-10)
- [x] **P-3** — `projects/trinkow/status/HANDOFF.md` devir-teslim günlüğü başlatıldı. (2026-09-10)
- [x] **G-007** — social-media-strategist: `projects/trinkow/docs/social/icerik-takvimi.md`
      (4 hafta, 16 içerik, IG+X). PM denetimi geçti. 5 madde Mustafa'da
      (K-010): hesap açma, bekleme listesi formu, kart şablonu, profil
      görseli, rakip adı anmama onayı. (2026-09-10)
- [x] **G-005d / G-006c** — Son düzeltme turu + **design-reviewer PASS**.
      TabItem 48pt (tasarımcının gerekçeli itirazı haklıydı, K-016),
      §2.5 kuralı dürüstleştirildi. tokens.md §7.7'ye sekme ölçüleri ve
      RN kodlama notu eklendi. **Aşama 2 teknik olarak tamam.** (2026-09-10)
- [x] **G-005c** — Revizyon turu: B1/B3/Ö1/Ö2 kapandı, B2 kısmen.
      Ayrıca kapsam dışı gerçek bir hata bulundu ve düzeltildi: 7 sayfa
      `index.html`'e bağlanıyordu ama dosya yoktu — tüm gezinme bağlantıları
      ölüydü. `s00_index.py` eklendi, HTML 7→8. (2026-09-10)
- [x] **G-006b** — design-reviewer DELTA denetim: 1 blocker + 1 önemli kaldı.
      `index.html` temiz geçti. PM aritmetiği bağımsız doğruladı. (2026-09-10)
- [x] **G-006** — design-reviewer 1. tur denetimi: **REVİZE GEREKİYOR**.
      3 blocker + 2 önemli, hepsi konum belirtilmiş. PM bağımsız doğruladı.
      Anti-pattern 17/19 temiz, kapsam 15/15 yüzey. (2026-09-10)
- [x] **G-005b** — ui-ux-designer TUR 2: prototip üretildi —
      7 HTML (~370KB) + `stil.css` + 4 gömülü font. Ekranlar Python
      üreteçle (`_uret/`) üretildi. Sosyal kart şablonu + monogram profil
      görseli dahil. İki API kesintisine rağmen tamamlandı. (2026-09-10)
- [x] **P-8** — repo hijyeni: `__pycache__/` .gitignore'a eklendi
      ve temizlendi. (2026-09-10)
- [x] **K-012** — "Sigara" → "Alışkanlıklar" (Mustafa: B seçeneği).
      PM'in önerdiği C seçeneği Faz 1'de uygulanamazdı (kullanıcı kategorisi
      ekleme Faz 2); Mustafa'nın kararı isabetliydi. (2026-09-10)
- [x] **G-005a / P-4,P-5,P-6,P-7** — ui-ux-designer TUR 1 tasarım temeli:
      5 dosya, 1185 satır. 27 bileşen + durum tabloları, Lucide 1.43.0 kilidi,
      452 satır gerçek Türkçe metin, 15 yüzey + 7 akış. Harcama girişi
      3 dokunuşa indirildi. PM doğruladı, ikon iddiası düzeltildi. (2026-09-10)
- [x] **P-2** — `projects/trinkow/docs/brand/tokens.md`: 46 aktif token, 13 kontrast çifti,
      9 bileşen ölçüsü, design-reviewer için grep denetim listesi. (2026-09-10)
- [x] **G-003** — Brandbook v1.0 NİHAİ: Trinkow adı işlendi, §5 Logo sistemi
      sıfırdan yazıldı (wordmark + "T"/çentik monogramı), Yön B arşivlendi,
      iki kontrast sayısı düzeltildi. Fontlar OFL → ücretsiz. (2026-09-10)
- [x] **G-002** — brand-strategist brandbook TASLAĞI üretti; PM denetiminden
      geçti (15 kontrast çifti bağımsız doğrulandı). Onaylandı. (2026-09-10)
- [x] **G-004** — social-media-analyst pazar analizi → `projects/trinkow/docs/social/analiz-raporu.md`.
      n=2 rakip doğrulandı (Bütçem gerçek, PM ayrıca URL doğruladı); kalan
      veri erişilemez olduğu için "[veri yok]" olarak bırakıldı, uydurulmadı.
      Çıktı kabul edildi (K-008). (2026-09-10)
- [x] **K-004** — Emoji yasağı: uygulamada emoji kullanılmayacak; ayırt
      edicilik gereken yerde ikon seti. CONTEXT.md'ye bağlayıcı yazıldı. (2026-09-10)
- [x] **K-002/K-005** — Stack kararı: React Native (Expo). CONTEXT + STAGE +
      BACKLOG güncellendi. (2026-09-10)
- [x] **S-010** — `agency/reference/rn-tasarim-kisitlari.md` üretildi ve 4 ajana
      bağlandı (ui-ux-designer, design-reviewer, frontend-developer,
      devops-engineer). design-reviewer'a "Geçiş 5: RN uygulanabilirliği"
      denetimi eklendi. Amaç: web alışkanlığıyla inşa edilemez tasarım
      üretilip revizyon turu yakılmasın. (2026-09-10)
- [x] **S-009** — `qa-engineer` çok dilli hale getirildi (pytest + Vitest/Jest
      + tsc). Ayrıca projeye özel risk alanları eklendi: para/float, tarih-gün
      sınırı, offline veri kaybı. Gerekçe: DECISIONS K-003. (2026-09-10)
- [x] **S-001** — 10 alt-ajan preprompt'u ortak profesyonel iskelete
      oturtuldu; her ajana çıktı sözleşmesi, token disiplini ve "Sınırlar"
      (ne YAPMAYACAĞI) bölümü eklendi. (2026-09-09)
- [x] **S-002** — `agency/reference/referans-repolar.md` kuruldu: küratörlü,
      HTTP 200 ile doğrulanmış GitHub repo kayıt defteri +
      "sistematik al, görsel stil alma" kuralı. (2026-09-09)
- [x] **S-003** — Token ekonomisi politikası CLAUDE.md'ye yazıldı. (2026-09-09)
- [x] **S-004** — STAGE.md'ye aşama başına "Girdi" dosya yolları,
      Aşama 2 revizyon döngüsü ve delta-denetim kuralı eklendi. (2026-09-09)
- [x] **S-005** — README ve CLAUDE.md güncellendi. (2026-09-09)
- [x] **S-006** — Sistem tutarlılık doğrulaması. (2026-09-09)
- [x] **S-007** — `agency/templates/proje-kurulum-checklist.md` kuruldu:
      her proje için 8 maddelik standart kurulum (token tasarrufu +
      tasarım referansları), her maddede kazanç ve DoD tanımlı. (2026-09-10)
- [x] **S-008** — Referans kayıt defterine "Alan-bazlı" bölüm eklendi
      (dashboard/tablo/form/editör/takvim/harita) — 54 doğrulanmış repo.
      Projeye göre seçilir, hepsi birden taşınmaz. (2026-09-10)

## ÜRÜN BACKLOG'U — Faz 2+ (K-030, araştırması yapıldı)
- [ ] **Ü-1 (Faz 2)** — **"Sık alınanlar"**: kullanıcı ürün adı + tutar
      girer, uygulama hatırlar; ikinci kez tek dokunuşla eklenir, fiyat
      önceki kayıttan gelir. **Maliyet 0, offline, API yok.** Latte
      Faktörü'nün doğası tekrar olduğu için değerin çoğunu bu verir.
- [ ] **Ü-2 (Faz 2.5)** — **Tütün fiyat listesi**: TR'de tütün ülke
      genelinde tek fiyat olduğu için küçük yerel liste yeterli; API gerekmez.
      Raporun amiral senaryosunu ("günde 125 TL sigara") çözer.
- [ ] **Ü-3 (ERTELENDİ)** — **Barkod tarama**: tarama bedava (`expo-camera`)
      ama barkod→isim verisi **güvenilmez**. PM testi: uydurma barkod
      `8691234567890` → OFF "riso basmati raja" döndürdü (TR önekine atanmış
      İtalyan pirinci). Yanlış ürün adı göstermek güveni bitirir. K-031.
- [ ] **Ü-5 (Faz 3)** — **Kendi fiyat verimiz**: kullanıcıların girdiği
      ürün+fiyat verisini toplayıp paylaşmak. Ölçekteki tek gerçek çözüm;
      üçüncü taraf API'sinden daha güncel olur. Kendi altyapımız (küçük db +
      toplama servisi), ücretli üçüncü taraf değil. Gelir sonrası.
      **Şimdi yapılacak hazırlık:** Ü-1'in veri modeli buna uygun olsun —
      ürün adı, tutar, tarih **ayrı alanlar**, serbest metin değil.
- [ ] **Ü-4** — Reddedildi: ücretli perakende fiyat API'si. K-009'a aykırı
      ve TR fiyat verisi zaten güvenilir/ücretsiz değil (Open Prices'ta
      TRY cinsinden yalnız 27 kayıt).

## Sistem backlog'u (ileride)
- [ ] **S-010** — Yeni ajanlar (Satış, Müşteri Destek, Finans, Hukuk)
      ihtiyaç doğduğunda, aynı preprompt iskeletiyle eklenecek.
- [ ] **S-011** — `referans-repolar.md` ölü link taraması: ajanlar 404
      bildirdikçe güncelle.
- [ ] **S-012** — İlk proje bitince: P-serisinin hangi maddeleri gerçekten
      işe yaradı, hangileri tören oldu? Checklist'i buna göre buda.

---

## 🆕 Kapsam genişlemesi — 2026-09-17 (Mustafa direktifi)
Kararlar: K-047 (giriş/kayıt) · K-048 (seri/oyunlaştırma) · K-049 (Günlük
sekmesi tarih sayfalama) · K-050 (kalori-app uyarlaması + ürün arama).
Aşama 2 yeniden açıldı; bu maddeler tasarım → denetim → onay → kod sırasıyla.

### F-16 — Seri (streak) sistemi
- [ ] F-16a Seri hesabı: limit altında kapatılan üst üste gün. Gün ancak kayıt
      VARSA ya da "Harcamasız gün" işaretlenmişse sayılır (hile kapısı, K-048)
- [ ] F-16b Milestone'lar: 3/7/14/30/60/100/180/365
- [ ] F-16c Milestone kutlama animasyonu (≤1.2 sn, atlanabilir, emoji/konfeti yok)
- [ ] F-16d Seri yüzeyi (E-21): mevcut seri · en uzun seri · 30 günlük ızgara
- [ ] F-16e Limitsiz modda seri kapalı + "Seri için günlük limit gerekir"
- [ ] F-16f Seri kırılması: suçlayıcı olmayan dil, "en uzun seri" saklanır

### F-17 — Günlük sekmesi (E-10 revizyonu, K-049)
- [ ] F-17a En sol sekme etiketi "Günlük"; sekme sayısı 3'te kalır
- [ ] F-17b Yatay tarih sayfalama: sola kaydır = önceki gün
- [ ] F-17c Başlık: Bugün / Dün / "17/09 Çarşamba"
- [ ] F-17d Sınırlar: gelecek yok; ilk kayıt gününden geriye yok
- [ ] F-17e Geçmiş güne harcama ekleme (geç kayıt)

### F-18 — Ürün arama ile hızlı giriş (E-11 revizyonu, K-050)
- [ ] F-18a Yerel ürün kataloğu (~60-80 kalem), her kalem bir kategoriye bağlı
- [ ] F-18b Arama → ürün seç → fiyat gir → ekle
- [ ] F-18c "Geçen sefer ₺X" (kullanıcının kendi son fiyatı). Katalog fiyat GÖSTERMEZ
- [ ] F-18d Kategori dropdown ile ekleme (ürün seçmek zorunlu değil, 2 adım korunur)
- [ ] F-18e Son kullanılanlar kısayolu

### F-19 — Giriş / Kayıt (K-047)
- [ ] F-19a E-22 Giriş, E-23 Kayıt tasarımı (e-posta + şifre)
- [ ] F-19b "Hesapsız devam et" çıkışı her iki ekranda (giriş duvarı YOK)
- [ ] F-19c Faz 1 kodu: hesap YEREL, sunucuya veri gitmez
- [ ] F-19d ⏸️ Google/Apple + backend → Mustafa onayı bekliyor (ücretli: $99/yıl)

### Tasarım görevleri (Aşama 2, sırayla)
- [x] T-1 prototip-v4 + Günlük sekmesi + seri yüzeyleri → ui-ux-designer (çalışıyor)
- [ ] T-2 E-11 ürün arama revizyonu + E-22/E-23 giriş/kayıt → ui-ux-designer
- [ ] T-3 delta denetimi → design-reviewer (PASS şart)
- [ ] T-4 delta-v4.md'nin tokens.md / bilesen-envanteri.md / metinler.md'ye
      birleştirilmesi (PM koordine eder, tek otorite tokens.md — K-040)

### F-19 güncellendi — Giriş/Kayıt + Google/Apple (K-052 ONAYLI)
- [ ] F-19a E-22 Giriş · E-23 Kayıt tasarımı (e-posta + şifre)
- [ ] F-19b "Hesapsız devam et" her iki ekranda (giriş duvarı YOK)
- [ ] F-19c Google ile giriş + Apple ile giriş (App Store 4.8 → ikisi birlikte)
- [ ] F-19d Kimlik doğrulama: Supabase Auth (ücretsiz katman) · harcama verisi
      cihazda kalır, Faz 1'de senkron YOK
- [ ] F-19e Gizlilik politikası + kullanım şartları metni (App Store şartı)
- [ ] F-19f Hesap silme akışı (App Store zorunluluğu — hesap varsa şart)

### F-20 — Profilleme anketi + para yönetim modeli (K-053)
- [ ] F-20a Katman 1: 3 zorunlu soru (niyet · gelir(atlanabilir) · maaş günü)
- [ ] F-20b Katman 2 "Seni tanıyalım": atlanabilir ~8 kart, ilerleme göstergeli,
      ayarlardan sonra tamamlanabilir
- [ ] F-20c Sabit giderler girişi: kira/aidat · faturalar · ulaşım · kredi-taksit
- [ ] F-20d Alışkanlık kartları: kahve · sigara · alkol · dışarıda yemek ·
      abonelikler → **sıklık + kullanıcının kendi fiyatı**
- [ ] F-20e Yatırım niyeti sorusu (tavsiye YOK, yalnız "yatırım payı" etiketi)
- [ ] F-20f "Planın hazır" ekranı: Zorunlu / Sosyal / Birikim dağılımı ₺ ve %
- [ ] F-20g **Günlük limit türetme:** sosyal pay ÷ maaş döngüsünde kalan gün
- [ ] F-20h "Alışkanlık maliyeti" kartı (sıklık × kendi fiyatı → aylık ₺)
- [ ] F-20i Yüzde kaydırıcıları + %100 kilidi + "Nasıl hesaplandı?" açıklaması
- [ ] F-20j Gelir yoksa zarif küçülme: yüzde modeli kapanır, limit elle girilir

### Marka görevi
- [ ] B-1 brandbook + CONTEXT.md mahremiyet ifadesi revizyonu → brand-strategist
      ("hesap yok" → "harcama verin cihazında kalır, hesap yalnız kimlik için").
      K-052 nedeniyle zorunlu. Tasarımcılar bitince başlatılacak (dosya sahipliği).

### Tasarım görevleri (güncel sıra)
- [x] T-1 prototip-v4 + Günlük (12 durum) + E-21 Seri (5 durum) → ✅ 0 bulgu
- [x] T-1b E-24 Gün seçici (5 durum) + Günlük referans uyarlaması → ✅ 0 bulgu
      (kazara paralel başlatılan ajan; çıktı kullanıldı, 78 yüzey / 14 sayfa)
- [ ] T-2 E-22/E-23 giriş+kayıt (Google/Apple) + E-19 Hesap bölümü + 4 düzeltme
      (K-055 yön çevirisi · K-054/7 çip birimi · K-056 kategori ölçeği ·
      Tasarruf tanımı) → ui-ux-designer (çalışıyor)
- [ ] T-3 Profilleme anketi (F-20) + "Planın hazır" ekranı → ui-ux-designer
- [ ] T-4 E-11 ürün arama revizyonu (F-18) → ui-ux-designer
- [ ] T-4 delta denetimi → design-reviewer (PASS şart, bloklayıcı)
- [ ] T-5 delta-v4 birleştirme: tokens.md / bilesen-envanteri.md / metinler.md

### T-5 birleştirme kalemleri (biriktirilen)
- [ ] `delta-v4.md` → `tokens.md` (T-1: 7 · T-2: 12-18 madde) sürüm notlu işlenmesi
- [ ] `bilesen-envanteri.md`: +15 bileşen (34→49 civarı) · §6'daki "takvim ızgarası
      Faz 1'de üretilmez" maddesi K-054/3'e göre yeniden yazılacak (ızgara MVP'de,
      rozet/başarım hâlâ yok)
- [ ] `metinler.md`: T-1/T-2/T-3 metin anahtarları + "Limit altı günlerde biriken"
      (Tasarruf) formülünün yazıya geçmesi
- [ ] `varliklar.md`: **"üçüncü taraf marka varlıkları"** bölümü (Google/Apple
      logoları, izinli renk/biçim, dosya yolları) — K-057/2
- [ ] `ekran-envanteri.md`: E-21 Seri · E-22 Oturum aç · E-23 Hesap oluştur ·
      E-24 Gün seçici · profilleme/plan ekranları + sekme 1 "Günlük" etiketi
- [ ] brandbook §6.6 süre tablosuna milestone kutlama hareket spesifikasyonu
      (≤1.2 sn, atlanabilir) işlenecek — B-1'de görsel dil kapsam dışıydı
- [ ] brandbook §8.2 S-1…S-8 "açık sorular" listesi **bayat**: palet/yön soruları
      K-024/K-027 (claymorphism) ve K-035 ile kapandı, kod da o tokenlarla yazıldı.
      Liste "kapandı" işaretiyle temizlenecek — yeni karar gerekmiyor.

---

## 🚀 Aşama 3 — Kodlama sırası (K-063 onayı sonrası, 2026-09-18)
Mustafa: "frontend olarak sen bunu kodla, bir an önce ürüne ulaşalım."
Sıra hız önceliğine göre: önce ürün değeri, auth en sonda.

- [x] **D-2d-1** ✅ Günlük sekmesi + yatay tarih sayfalama + seri sistemi (F-16) +
      gün seçici (E-24). Yeni bağımlılık yok. 2 PM kararı doğurdu → **K-064**.
      (2026-09-19)
- [x] **D-2d-2** ✅ (2026-09-19) — E-11 ürün arama + 80 kalemlik yerel katalog (F-18)
      **+ K-064/1** `limit_gecmisi` tablosu (seri geçmişi güncel limitle
      değerlendirilmesin) **+ K-064/2** `gunsec.alt.acik_gun` metin düzeltmesi
      **+ K-062** metin taşıyan yüzeylerde gradyan → düz `primary-deep`
      (Button.tsx vd., erişilebilirlik zorunluluğu). (2026-09-19)
      Kapsam dışı bırakıldı → D-2d-3: limit önerisi sheet'i (Katman 1'e bağlı).
      Sonuç: 8 yeni dosya (`urunKatalogu.ts` 80 kalem · `urunArama.ts` ·
      `urunKategori.ts` öğrenme tablosu · 5 bileşen), şema 1→2, tsc 0 hata,
      iOS export temiz, yeni bağımlılık yok. Düzeltme turu: `gun-btn` artık
      E-24 Gün seçici'yi **seçim kipinde** açıyor (sapma K-065/1).
      PM hükümleri: **K-065**.
- [x] **D-2d-3a** ✅ (2026-09-19, K-070) — Onboarding Katman 1 (E-01 niyet · E-02 gelir
      (atlanabilir) · E-03 maaş günü) + günlük limit önerisi sheet'i (K-059/5) +
      profil veri katmanı (şema 2→3) + `kalan_gun`/`gunluk_limit` formül modülü
      (tek tanım, 3b bunu kullanacak).
- [x] **D-2d-3b** ✅ (2026-09-19, K-071) — Katman 2 "Seni tanıyalım" (E-25, ~8 kart) + sabit giderler +
      alışkanlık kartları + "Planın hazır" (E-26) + yüzde kaydırıcıları +
      kategori limiti tohumlama + **F-11 niyete göre kişiselleşen pano** (K-070 devri).
      Renk kararı hazır: **K-066** (`share.birikim` = `success`, iki sınırla).
- [ ] **D-2c** — E-22 Oturum aç · E-23 Hesap oluştur · Supabase Auth ·
      E-19 Ayarlar hesap bölümü (çıkış / hesabı sil) · E-00 açılış · onboarding.
      Tek yeni bağımlılık kümesi burada; ürün onsuz da çalışsın diye en sonda.
- [ ] **D-3** — qa-engineer (Aşama 4). QA notu (K-064): 300+ günlük geçmişte
      `FlatList` pencereleme senaryosu denenecek.

## 🆕 BACKEND (Mustafa direktifi, 2026-09-19 — K-067)
Python · modüler (`modul/{dto,service,controller,model,repository}`) · MongoDB (yerel)
**Sıra kuralı: arayüz geliştirmesi bitmeden backend KODU yazılmaz.** Modüller tek tek tasarlanır.

- [x] **BE-0** ✅ `projects/trinkow/backend/` + `README.md` (klasör yapısı ve kurallar)
- [x] **BE-1** ✅ K-067'nin 4 sorusu cevaplandı → **K-068** (veri sunucuda ·
      kendi JWT auth'umuz · klasörleme aynen · prod barındırma yok).
- [x] **BE-2** ✅ (2026-09-19) — `auth` modülü + FastAPI/Motor iskeleti.
      6 uç nokta, 2 koleksiyon (unique + TTL index), pytest yazıldı.
      ⚠️ Testler **gerçek Mongo'ya karşı çalıştırılamadı** (yerel sunucu yok) → K-069.
- [ ] **BE-2a** 🔵 Mustafa: yerel MongoDB kurulumu (K-069) — onay gerekiyor,
      sonra `pytest` gerçek veritabanına karşı doğrulanır.
- [ ] **BE-2b** Yenileme token'ı rotasyonu (K-069/1) — her yenilemede eski jti iptal.
- [ ] **BE-2c** Şifre sıfırlama akışı — e-posta gönderimi gerektirir (dış servis,
      onay kapısı). K-058 buna bağlı, yayın öncesi gerekli.
- [ ] **BE-2d** Google / Apple ile giriş — sağlayıcı token'ının `auth` modülünde
      doğrulanması (K-057: iOS'ta ikisi, Android'de yalnız Google).
- [x] **BE-3** ✅ (2026-09-19) — `kullanici` modülü: profil oku · Katman 1 · Katman 2
      (kısmi) · plan kur (sunucuda hesaplanıyor, K-075) · günlük limit. 19 test yazıldı,
      Mongo yokluğundan koşamadı. Eksikler BE-4 Madde 0'a devredildi.
- [x] **BE-4** ✅ (2026-09-19, K-076) — `harcama` modülü (harcama · taksit serisi · kategori
      limiti · gün durumu · limit geçmişi · ürün öğrenme) + Madde 0: pytest fixture
      düzeltmesi (formül testleri Mongo'suz koşsun) · `gunluk_limit_onerisi_kurus` ve
      `son_kart` alanları · uygulama tercihleri uç noktası.
- [x] **BE-5** ✅ (2026-09-19, K-077) — `ozet` modülü: günlük pano · özet · kategori dağılımı ·
      **seri hesabı** (K-048 + K-064/1). Toplama sunucuda, gösterim istemcide (K-076/3).
- [x] **BE-5b** ✅ (2026-09-19) — seri düzeltmeleri: en uzun seri kalıcı (ratchet) ·
      sınır günü ilk kayda göre · limit geçmişi toplu çekim (O(gün) → O(1) sorgu).
- [x] **BE-7** ✅ (2026-09-19) — `katalog` modülü: 80 kalem tohumlama · ETag/sürüm ile
      listeleme · tekil okuma. Fiyat/marka/görsel yok (K-050). Arama istemcide kalıyor. — 80 kalemlik ürün kataloğunun sunucudan güncellenmesi
      (uygulama sürümü çıkmadan katalog güncellenebilsin).
- [ ] **BE-9** `bildirim` modülü — acelesi yok, önce dil ve tetikleyici tasarımı.
      Mustafa: "ona bir şeyler düşün, sonrasında karar veririz"
- [ ] **BE-6** 🔒 Mobil istemcinin backend'e bağlanması — **MongoDB kurulana kadar
      BAŞLATILMIYOR** (K-079). Bugün uygulama SQLite ile çalışıyor; çalışmayan bir
      sunucuya bağlamak onu tamamen kullanılamaz hâle getirir.
- [ ] **BE-7** Gizlilik politikası metninin backend kapsamına göre güncellenmesi
      (K-057/7 zaten açık; backend kapsamı büyürse metin de büyür)
- [ ] **BE-8** brand-strategist: brandbook mahremiyet dili **yeniden** revize —
      "verin cihazında kalır" K-068 ile geçersiz. Gizlilik politikası metni (K-057/7)
      bu revizyondan sonra yazılır; sosyal içerik takviminde de mahremiyet vaadi var.
- [ ] **D-2c sıra değişti** — oturum aç / hesap oluştur ekranları artık **BE-2'den
      SONRA** kodlanır (Supabase'e göre yazılıp atılacak kod üretilmesin).
- [ ] **F-11b** — "Borç" niyetinin gerçek sayıya bağlanması: Katman 2'ye toplam borç
      kartı (K-071 açık boşluğu). D-2c sonrası karara bağlanacak.
- [x] **D-2c-1** ✅ (2026-09-19, K-072) — E-19 Ayarlar + E-20 bağlamsal profilleme
      sheet'i. Şema 4→5.
- [x] **D-2c-1b** ✅ (2026-09-19) — Özet başlığına Ayarlar girişi (K-072) +
      varsayılan ödeme ön seçimi + gün sınırı tercihinin gün hesabına bağlanması
      (tek yerde: `lib/tarih.ts`). Sapma: `ScreenHeader`'a ikinci ikon eklendi
      (envanterdeki "sağda tek IconButton" kuralı → T-5'te güncellenecek).
- [x] **D-2c-2** ✅ (2026-09-19, K-074) — E-22/E-23 + API istemcisi + oturum deposu.
      ⚠️ E-00 açılış ekranı yapılmadı (aşağıda). **ARAYÜZ TAMAMLANDI.**
- [ ] **D-2c-3** — E-00 açılış ekranı (marka + topuz), yayın öncesi.
- [ ] 🔴 **D-2c-4** — "Şifremi unuttum" şu an sahte (K-074/3): BE-2c yazılana kadar
      bağlantı gizlenir. **Yayın bloklayıcısı.**
- [ ] ~~eski D-2c-2 satırı~~ — E-00 açılış + E-22 oturum aç + E-23 hesap oluştur +
      `lib/api.ts` + `lib/oturumDeposu.ts` + Ayarlar hesap eylemlerinin bağlanması.
      Açık dikişler: "Hesapsız devam et" (K-073) · Google/Apple (BE-2d) ·
      güvenli token saklama (`expo-secure-store` onayı).
- [ ] **S-013** — `design-reviewer` denetim listesine **erişilebilirlik grafiği**
      maddesi: her ekrana uygulama içinden bir yoldan gidilebiliyor mu? K-072'de
      Ayarlar'ın kapısız kaldığı PASS'ten sonra fark edildi.
- [ ] **D-2c-1c** — `prof.degisti` sonrası "Taksit yükü" kartının panoya eklenmesi
      (K-072/3, küçük).
- [ ] 🔵 **Mustafa: `expo-notifications` onayı** (ücretsiz, Expo paketi) — bildirim
      izni satırının gerçekten çalışması için. K-072.

## 🆕 K-080/K-081/K-082 sonrası (2026-09-19)
- [x] **D-2c-3** ✅ Hesap zorunlu: giriş duvarı · "Hesapsız devam et" kaldırıldı ·
      çıkış/hesap silme giriş ekranına düşürüyor (K-080).
- [ ] 🔵 **Mustafa: Atlas veritabanı KULLANICI ADI** — bağlantı dizesinde `<db_username>`
      yer tutucu. Bu gelmeden 47 test gerçek veritabanına karşı koşamıyor.
- [ ] 🔴 **Mustafa (öneri): Atlas şifresini yenile** — şifre sohbete düz metin girdi.
- [ ] 🔴 **C-1** `hesap.mahremiyet` metni yanıltıcı ("Harcamaların sende kalır" ama veri
      sunucuda) → `metinler.md` + `metinler.ts` + brandbook birlikte düzeltilecek (K-082/1).
      **Yayın bloklayıcısı.**
- [ ] **BE-9 iptal/ertelendi** — bildirim Expo ile yapılmayacak (K-081/2); Mustafa
      kendisi çözecek. Dil/kural taslağı (K-078) geçerli kalıyor.
- [ ] **D-2c-4'e ek** — Ayarlar'daki bildirim anahtarı gerçek izin isteyemiyor
      (çalışmayan anahtar). Yayın öncesi bağlanır ya da gizlenir.
- [x] **BE-6a** ✅ profil/plan/tercihler API'ye bağlandı (K-084)
- [x] **BE-6b** ✅ harcama/taksit/limit/ürün öğrenme API'ye bağlandı (K-085)
- [x] **BE-4b** ✅ backend 6 eksik kapandı; hesap silme artık tüm veriyi siliyor (K-086)
- [ ] **BE-6c** 🔄 ÇALIŞIYOR — pano/özet/seri + katalog + Ayarlar'ın kalan 2 eylemi +
      yerel şema temizliği. **Veri taşımanın son turu.**
- [ ] **BE-10** `backend/README.md` bayat bölümler: "yerel MongoDB" → Atlas (K-086 notu)
- [x] **BE-6c/6d** ✅ veri taşıma tamamlandı (K-087/K-088)
- [x] **D-3 QA** ✅ tur yapıldı → **GEÇMEDİ**, 2 bloklayıcı (K-089) · `docs/qa-raporu.md`
- [x] **QA-2** ✅ 8 yanıltıcı metin düzeltildi (hesap silme onayı dahil)
- [ ] **QA-1** 🔄 `plani_kur` gün parametresi + backend genelinde saat dilimi taraması
- [ ] **Q-1** 🔵 İstemci test altyapısı YOK (Vitest) — QA'nın yapısal bulgusu.
      Öncelikli 6 modül belirlendi. **Mustafa'ya sorulacak:** şimdi mi, yayından sonra mı?
- [ ] **T-5 ek** `metinler.md` §25'teki "hesap önkoşul değildir / Hesapsız devam et"
      doküman notu temizlensin (K-080 ile geçersiz, prose notu).

## 🟢 QA GEÇTİ (2026-09-20, K-092) — yayın öncesi borç listesi
Uygulama + backend çalışıyor, testler yeşil. Aşağıdakiler **kararı Mustafa'da**:
- [ ] **R-1** 🔴 "Şifremi unuttum" sahte — backend'de sıfırlama ucu yok. Ya yazılır
      (e-posta servisi gerekir → yeni bağımlılık) ya da bağlantı gizlenir.
- [ ] **R-2** 🔴 Token'lar güvenli depoda değil (SQLite) → `expo-secure-store` (ücretsiz).
- [ ] **R-3** 🔴 Yenileme token'ı rotasyonu yok (çalınan token süresi dolana kadar geçerli).
- [ ] **R-4** Gizlilik politikası + kullanım şartları metni (App Store şartı) — Mustafa'da.
- [ ] **R-5** Brandbook mahremiyet dili revizyonu (BE-8) — "veri cihazda" artık geçersiz.
- [ ] **R-6** Ayarlar'daki bildirim anahtarı gerçek izin isteyemiyor → bağla ya da gizle.
      (Mustafa bildirim işini kendisi çözecek — K-081/2.)
- [ ] **R-7** E-00 açılış ekranı (marka + topuz) yapılmadı.
- [ ] **R-8** Google / Apple ile giriş (BE-2d) — kütüphane onayı gerekiyor.
- [ ] **Q-1** İstemci test altyapısı yok (Vitest) — öncelikli 6 modül belirlendi.
- [ ] **QA-1e kalıntısı** Ölü kod temizliği (`gunlukLimitGecmisiKaydet`, `limitGecmisiYazIstegi`
      + `profil.ts:40` docstring) — küçük.
- [ ] 🔵 **Commit** — bu oturumdaki tüm iş (arayüz + backend + bağlama) **commit edilmedi.**
- [ ] 🔵 Atlas'ta kalan test kullanıcısı silinsin mi? · Atlas şifresi yenilensin mi?
