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
