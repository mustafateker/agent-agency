# Trinkow REV3 — 2026-09-26

Mevcut aşama: **REV3 revizyon turu KAPANDI.** Aşama 2 → 3 → 4 döngüsü bu tur
için tamamlandı; **Aşama 5 (DevOps/Yayın) hâlâ açılmadı.**

REV3 kapıları: design-reviewer PASS ×2 (Günlük+Tasarruf r2'de · Taksitler r4'te) ·
QA kapanış **GEÇTİ** (tsc 0 · mobil 95/95 · backend 144/144 · iOS+Android export).

Cihazda doğrulanacaklar (otomasyon kapsamı dışı): Taksitler'in 9 durumu ·
tek→çok kategori `LayoutAnimation` geçişi · uzun ürün adı kırpması · rutin
satırında kazara dokunma · akordiyon açılış animasyonu · `LimitGauge mod="birikim"` ·
`SavingsSheet` klavye · `DateField` kaydırma · kurulum kaydırma kesmesi ·
`fontScale > 1.3` · "Seni tanıyalım" kartlarının çıkması.

---
# Trinkow REV2 — 2026-09-26

Mevcut aşama: **REV2 revizyon turu KAPANDI.** Aşama 2 (tasarım) → 3 (geliştirme)
→ 4 (kalite) döngüsü bu tur için tamamlandı; **Aşama 5 (DevOps/Yayın) hâlâ
açılmadı.**

REV2 kapıları: design-reviewer PASS ×2 (onboarding+kayıt, tasarruf+profil) ·
QA kapanış GEÇTİ (tsc 0 · mobil 38/38 · backend 139/139 · iOS+Android export).

Bekleyen: Mustafa'nın cihaz/simülatör doğrulaması ve K-093…K-096 kararları.
Cihazda doğrulanacaklar (otomasyonun kapsamı dışında): `LimitGauge mod="birikim"`
yay baskılama · `SavingsSheet` klavye+footer · hareket satırında sağdan sola
silme jesti · `DateField` yatay kaydırma · kurulum formunda kaydırma kesmesi ·
`fontScale > 1.3` görünümü.

---
# Trinkow Rev — 2026-09-23

Kullanıcı planı açıkça uygulama için onayladı. Önceki değişiklikler korunacak.
Aktif aşama: Revizyon uygulaması ve otomatik QA tamamlandı; yayın kapısı açılmadı.
Kararlar: ayrı tasarruf/birikim; günlük kategori payları; takip serisi; maaş−sabit−hedef birikim takvim ayına bölünür; rutin tasarrufu açık doğrulama; e-posta öncelikli; yerel posta+SMTP; legal taslaklar; push/AI/prod kapsam dışı.

| Görev | Sahip | Durum | Kabul |
|---|---|---|---|
| REV-01 tasarım delta/prototip | UI/UX | tamamlandı | marka + yeni durumlar |
| REV-02 tasarım denetimi | design-reviewer/root | PASS | tasarruf/birikim ayrımı |
| REV-03 bütçe/rutin/favori/tasarruf/seri API | Python finans | tamamlandı | sözleşme + Mongo testleri |
| REV-04 gerçek auth/reset/rotation/mail | Python auth | tamamlandı | reset/rotation/outbox |
| REV-05 native girdiler | frontend ortak | tamamlandı | özel keypad kaldırıldı |
| REV-06 finans ekranları | frontend finans | tamamlandı | gerçek API akışları |
| REV-07 hesap/ayarlar/legal | frontend hesap | tamamlandı | güvenli oturum + hesap işlemleri |
| REV-08 QA entegrasyon | QA/root | otomasyon tamamlandı | 139 + 14 test, iki bundle |

Dış bağımlılıklar: gerçek SMTP/gönderici; legal işletmeci bilgileri/hukuki kontrol. Yerel testleri durdurmaz, prod tamamlandı sayılmaz.
Sonraki adım: prod kapsamı açılırsa SMTP/legal bilgileri ve gerçek cihaz matrisi tamamlanır.

---
Önceki kayıtlar (tarihsel):

# Aşama Takibi

Mevcut aşama: **4 ✅ KAPANDI → 5 (DevOps/Yayın) kapısında, Mustafa kararı bekleniyor**
QA delta: BLOCKER yok (K-092). Backend 123/123 · istemci tsc 0 hata.
Aşama 5 açılmadan önce yayın öncesi borç listesi önceliklendirilmeli.
Aşama 3 ✅ KAPANDI (2026-09-20, K-088): arayüz + 5 modüllük Python/MongoDB backend +
istemcinin tamamen sunucuya bağlanması. Backend 118/118 test geçiyor (Atlas).
Aşama 2 ✅ KAPANDI: design-reviewer PASS + Mustafa onayı (K-063).
Tasarım: `docs/design/prototip-v4/` — **18 ekran · 122 yüzey · 0 bulgu**, anti-pattern 20/20 temiz.
Kaynak dokümanlar senkron: `tokens.md` **v4.0** · bileşen envanteri · metinler · varlıklar · ekran envanteri.

**Kodlama sırası (K-063, hız önceliği):**
D-1 ✅ · D-2a ✅ · D-1b ✅ · D-2b ✅ · D-2d-1 ✅ (Günlük + seri + gün seçici) ·
D-2d-2 ✅ · D-2d-3a ✅ · D-2d-3b ✅ · D-2c-1 ✅ · D-2c-1b ✅ · D-2c-2 ✅
→ **ARAYÜZ TAMAMLANDI** (2026-09-19).
Kalan: E-00 açılış ekranı · "şifremi unuttum" sahte (yayın bloklayıcı) ·
**BE-6 istemcinin API'ye bağlanması** · D-3 QA (Aşama 4) · T-5 doküman senkronu.
Açık PM kararları: K-065 · K-066. Arayüz bitince T-5 doküman birleştirmesi yapılır.

Yayın öncesi bloklayıcılar (Mustafa'da): gizlilik politikası + kullanım şartları
metni (K-057/7) · hesap silme Edge Function (K-057/4).

Backend: Mustafa 2026-09-19'da **Python + modüler + MongoDB** backend direktifi verdi (K-067).
`../backend/` kuruldu. **Kural: arayüz bitmeden backend kodu yazılmaz**
→ `python-developer` sıraya girdi ama henüz çağrılmadı; önce K-067'nin 4 sorusu cevaplanmalı.
Aşama 6 (Büyüme): içerik takvimi hazır, yayın zamanlaması Mustafa'da (K-010).
Aşama 1 ✅ (K-006/K-021, brandbook 2026-09-17'de K-052/K-048'e göre revize edildi).
Proje: Trinkow · Bağlam: `projects/trinkow/docs/CONTEXT.md` · Stack: RN (Expo) + TypeScript.

Kural: PM, mevcut aşamanın "çıkış kriteri" karşılanmadan ve gerekiyorsa
Mustafa'nın onayı `projects/trinkow/status/DECISIONS.md`'ye işlenmeden bir SONRAKİ aşamaya
GEÇMEZ. Bir aşamada listelenmeyen ajanı PM o aşamada çağırmaz.

Her aşamanın "Kurulum" satırı `templates/proje-kurulum-checklist.md`'deki
P-serisine, "Girdi" satırı ise PM'in alt-ajana vereceği brief'te geçmesi
gereken dosya yollarıdır (bkz. CLAUDE.md → Token ekonomisi).

## Aşama 0 — Keşif
- Aktif ajan: pm-orchestrator (sadece okur/netleştirir, üretim yapmaz)
- Girdi: `projects/trinkow/docs/` altındaki proje dökümanı
- Kurulum: **P-1** (`projects/trinkow/docs/CONTEXT.md` tek sayfalık bağlam paketi), **P-8**
  (repo hijyeni) — bkz. `templates/proje-kurulum-checklist.md`
- Çıkış kriteri: projects/trinkow/docs/ içindeki proje dökümanı okunmuş, BACKLOG.md'de net
  bir MVP tanımı var, P-1 üretilmiş.

## Aşama 1 — Marka
- Aktif ajan: brand-strategist
- Girdi: proje dökümanı, `templates/brandbook-template.md`,
  `reference/jenerik-ai-ui-anti-pattern-listesi.md`
- Çıktı: `projects/trinkow/docs/brand/brandbook.md`
- Kurulum (onaydan hemen sonra): **P-2** (marka token dosyası),
  **P-3** (`projects/trinkow/status/HANDOFF.md` başlat)
- Çıkış kriteri: Mustafa brandbook'u onayladı (DECISIONS.md'de kayıtlı).

## Aşama 2 — UI/UX Tasarım
- Aktif ajanlar: ui-ux-designer, design-reviewer
- Ön koşul: Aşama 1 tamamlanmış olmalı (brandbook onaylı).
- Girdi: `projects/trinkow/docs/brand/brandbook.md`,
  `reference/jenerik-ai-ui-anti-pattern-listesi.md`,
  `reference/referans-repolar.md`,
  **`reference/rn-tasarim-kisitlari.md`** (RN'de inşa edilebilirlik — bağlayıcı)
- Kurulum (tasarım başlamadan ÖNCE): **P-4** gerçek metinler, **P-5**
  projeye özel referans seti, **P-6** varlık kilidi (tek ikon seti + fontlar),
  **P-7** bileşen envanteri + state listesi
- Çıktı: `projects/trinkow/docs/design/` altında tasarım/prototip
- Döngü: ui-ux-designer üretir → design-reviewer denetler → REVİZE ise
  somut maddelerle tasarımcıya geri döner. İkinci turdan itibaren denetim
  DELTA'dır (sadece açık maddeler + yeni sorunlar).
- Çıkış kriteri: design-reviewer PASS verdi VE Mustafa son görsel onayı
  verdi (DECISIONS.md). PASS tek başına yeterli değildir.

## Aşama 3 — Geliştirme
- Aktif ajanlar: frontend-developer (UI kodu), python-developer (backend/
  iş mantığı)
- Ön koşul: Aşama 2 tamamlanmış olmalı.
- Girdi: onaylı tasarım (`projects/trinkow/docs/design/`), `projects/trinkow/docs/brand/brandbook.md`
- Çıkış kriteri: Planlanan özellikler kodlanmış, BACKLOG.md'de işaretli.

## Aşama 4 — Kalite
- Aktif ajan: qa-engineer
- Girdi: `src/`, `tests/`
- Çıkış kriteri: Testler geçiyor, kritik/blocker hata yok.
- Not: BLOCKER bulgular `python-developer`/`frontend-developer`'a geri
  döner; QA düzeltme yapmaz.

## Aşama 5 — DevOps / Yayın
- Aktif ajan: devops-engineer
- Ön koşul: Aşama 4 tamamlanmış olmalı.
- Çıkış kriteri: Yayın planı DECISIONS.md'de onaylı (prod/deploy/domain/
  ücretli servis kararları CLAUDE.md'deki onay kuralına tabidir).

## Aşama 6 — Büyüme / Sosyal Medya (PARALEL aşama)
- Aktif ajanlar: social-media-strategist, social-media-analyst
- Ön koşul: SADECE Aşama 1 (brandbook onayı) tamamlanmış olmalı — marka
  sesi olmadan içerik üretilmez. Bu aşama Aşama 2-5 ile PARALEL
  ilerleyebilir, sıralı beklemez.
- Girdi: `projects/trinkow/docs/brand/brandbook.md`, proje dökümanı,
  (varsa) `projects/trinkow/docs/social/analiz-raporu.md`
- Sıra: analyst önce veri üretir → strategist o veriyle takvimi kurar.

## Sonraki aşamalar (henüz kurulmadı, ihtiyaç oldukça agency-agents'tan
eklenecek): Satış, Müşteri Destek, Finans/Operasyon, Hukuk/Uyumluluk.
Bunlar için şu an ajan yok — iş bu noktaya geldiğinde PM'e/Mustafa'ya
haber verilip birlikte eklenecek.
