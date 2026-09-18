# Proje Kurulum Checklist'i (her yeni proje için standart)

Bu sistem **birden fazla proje** üretecek. Her projede sıfırdan
"nasıl kuruyorduk?" diye düşünmemek için, her proje başında kurulması
gereken varlıklar burada sabitlenmiştir.

PM, yeni bir proje başlarken bu listeyi **`projects/trinkow/status/BACKLOG.md`'ye P-serisi
görevler olarak kopyalar** ve aşama sırasına göre tamamlatır.

Her maddenin bir **kazanç** satırı var — neden var olduğu belli olsun,
tören olsun diye yapılmasın.

---

## Neden bu liste var?

Çok-ajanlı sistemde en pahalı iki şey:
1. **Alt-ajanın bağlamı yeniden keşfetmesi** — her ajan soğuk başlar. Aynı
   dökümanı 6 ajan ayrı ayrı okursa, aynı token 6 kez ödenir.
2. **Revizyon turu** — tasarımcı yanlış varsayımla üretir, denetçi REVİZE
   verir, baştan üretilir. Bir revizyon turu, tüm bu kurulumdan pahalıdır.

Aşağıdaki varlıklar bu ikisini birden azaltır: bilgiyi **bir kez, makine
okunur ve tek kaynak** halinde üretip herkesin oradan okumasını sağlar.

---

# A. Token tasarrufu varlıkları

## P-1 — Bağlam paketi · `projects/trinkow/docs/CONTEXT.md`
- **Ne zaman:** Aşama 0 çıkışında (proje dökümanı okunur okunmaz)
- **Kim:** pm-orchestrator
- **Ne:** Projenin **tek sayfalık** özeti. Proje dökümanı 20 sayfa da olsa
  bu 1 sayfa olacak: ürün nedir, kim kullanır, MVP kapsamı (ve kapsam DIŞI),
  ürün tipi/stack, kısıtlar, proje sözlüğü (alan terimleri).
- **Kazanç:** PM her brief'te bunu referans verir. 9 ajanın her biri 20
  sayfalık dökümanı okumak yerine 1 sayfa okur. Sistemdeki **en büyük tek
  tasarruf kalemi budur.**
- **DoD:** 1 sayfayı geçmiyor · "kapsam DIŞI" bölümü dolu · alan terimleri
  tanımlı · proje dökümanıyla çelişmiyor.

## P-2 — Marka token dosyası · `projects/trinkow/docs/brand/tokens.md` + kod karşılığı
  (web: `src/web/tokens.css` · React Native: `src/theme/tokens.ts`)
- **Ne zaman:** Brandbook ONAYLANDIKTAN hemen sonra (Aşama 1→2 geçişinde)
- **Kim:** ui-ux-designer üretir, frontend-developer koda çevirir
- **Ne:** Brandbook düzyazıdır; bu onun **makine okunur** özeti:
  renkler (HEX + kullanım), font stack'leri, type scale, spacing scale,
  radius kuralı, gölge kuralı, breakpoint/ekran boyutları, katman sırası.
- **Kazanç (iki yönlü):**
  - Ajanlar düzyazı brandbook'u ayrıştırmak yerine değeri doğrudan okur.
  - `design-reviewer` mekanik denetimi (Geçiş 1) bu dosyaya karşı `grep`
    ile çalışır → "brandbook'ta olmayan renk var mı?" sorusu saniyeler
    sürer, sayfalarca CSS okumaya gerek kalmaz.
- **DoD:** Brandbook'taki HER görsel değer burada · değerler **tek yerde**
  tanımlı (bileşenlere dağıtılmamış) · tasarım ve kod aynı değeri kullanıyor.

## P-3 — Devir-teslim günlüğü · `projects/trinkow/status/HANDOFF.md`
- **Ne zaman:** Her aşama bitiminde güncellenir
- **Kim:** pm-orchestrator
- **Ne:** Aşama başına **3-5 satır**: ne üretildi, hangi kritik karar
  verildi, sonraki aşamanın bilmesi gereken ne var.
- **Kazanç:** PM'in alt-ajana vereceği brief'in "Bağlam" maddesi (bkz.
  CLAUDE.md → Delegasyon sözleşmesi) buradan kopyalanır. Ajan geçmişi
  kazmak zorunda kalmaz.
- **DoD:** Aşama başına 5 satırı geçmiyor · karar var, anlatı yok.

## P-4 — Gerçek metin kaynağı · `projects/trinkow/docs/content/metinler.md`
- **Ne zaman:** Tasarım başlamadan önce (Aşama 2 başı)
- **Kim:** ui-ux-designer (marka tonuna göre), gerekirse
  social-media-strategist destekler
- **Ne:** Ekranlarda geçecek **gerçek** metinler: başlıklar, buton
  etiketleri, boş durum mesajları, hata mesajları, form yardım metinleri.
- **Kazanç:** Lorem ipsum yasağı (anti-pattern listesi) tek kaynaktan
  çözülür. Tasarımcı ve frontend aynı metni kullanır — metin iki kez
  yazılmaz, uyuşmazlık yüzünden revizyon turu çıkmaz.
- **DoD:** Placeholder yok · hata/boş durum metinleri dahil · marka ses
  tonuna uygun · uzun metin örnekleri var (taşma testi için).

---

# B. Tasarım referans varlıkları

## P-5 — Projeye özel referans seti · `agency/reference/referans-repolar.md` (proje kopyası)
- **Ne zaman:** Aşama 2 başlamadan önce
- **Kim:** ui-ux-designer, PM onaylar
- **Ne:** Bu repodaki **global** `agency/reference/referans-repolar.md`'den
  başla, projeye göre **buda ve genişlet**:
  - Alakasız kategorileri çıkar (ör. pazarlama sitesinde veri-viz gerekmez)
  - Alan-bazlı repoları ekle (global listenin "Alan-bazlı" bölümünden)
  - Projeye özel 5-8 gerçek marka/ilham linki ekle (rakip analizinden)
- **Kazanç:** Ajan 54 repoluk genel liste içinde dolaşmaz; 8-10 alakalı
  kaynağa bakar. Arama yerine adres → fetch başına ciddi tasarruf.
- **DoD:** Linkler doğrulanmış (404 yok) · her kaynağın "ne için bakılır"
  satırı var · liste 12 kalemi geçmiyor.
- **KURAL (değişmez):** Bu repolardan **sistematik** alınır (token mimarisi,
  erişilebilirlik, state/edge case), **görsel stil ALINMAZ.** Hazır design
  system temasını kopyalamak, kaçındığımız jenerik AI görünümünün birebir
  kaynağıdır. Renk ve font sadece brandbook'tan gelir.

## P-6 — Varlık kilidi · `projects/trinkow/docs/design/varliklar.md`
- **Ne zaman:** Aşama 2 başı
- **Kim:** ui-ux-designer
- **Ne:** Projede kullanılacak varlıklar **kilitlenir**:
  - **İkon seti: TEK set.** Hangisi, hangi sürüm, çizgi kalınlığı kaç?
  - **Fontlar:** hangileri, nereden (self-host mu, hangi ağırlıklar?)
  - Görsel/illüstrasyon kaynağı ve lisans durumu
  - Varsa animasyon kütüphanesi
- **Kazanç:** İkon setlerini karıştırmak amatörlüğün **en görünür**
  işaretidir (çizgi kalınlıkları tutmaz). Ayrıca her ekranda "hangi ikonu
  kullansam?" araştırması yapılmaz.
- **DoD:** Tek ikon seti · font ağırlıkları sınırlı (2-3) · lisanslar
  ticari kullanıma uygun · sürümler yazılı.

## P-7 — Bileşen envanteri · `projects/trinkow/docs/design/bilesen-envanteri.md`
- **Ne zaman:** Ekran tasarımı başlamadan önce
- **Kim:** ui-ux-designer
- **Ne:** Hangi bileşenler gerekli (buton, input, kart, tablo, modal,
  bildirim…) ve her biri için **zorunlu state listesi**: varsayılan,
  disabled, loading, hata, boş + platforma göre:
  **web** → hover, focus-visible, active · **mobil** → pressed
  (dokunmatikte hover YOKTUR; pressed kullanıcının tek geri bildirimidir).
- **Kazanç:** Tasarımcı ve frontend **aynı listeden** çalışır. Eksik state
  yüzünden çıkan revizyon turu (`design-reviewer` Geçiş 4) büyük ölçüde
  kapanır — ki bir revizyon turu bu listeyi yazmaktan çok daha pahalıdır.
- **DoD:** Her bileşenin state listesi tam · boş/hata durumları dahil ·
  tasarımda ve kodda aynı isimler kullanılıyor.

---

# C. Hijyen

## P-8 — Repo hijyeni
- **Ne zaman:** Proje başında
- **Kim:** devops-engineer (veya PM, basitse)
- **Ne:** `.gitignore` (sırlar, build çıktıları, `node_modules`, `.env`),
  klasör yapısı (stack'e uygun: web `src/web/`, RN `app/` + `src/`),
  `tests/`, `.env.example`.
- **Kazanç:** Ajanlar `grep`/`glob` yaparken build artıklarına ve
  bağımlılık klasörlerine takılmaz — hem gürültü hem token.
- **DoD:** Sır repoda değil · `grep` sonuçları temiz · yapı CLAUDE.md'deki
  klasör şemasına uygun.

---

## PM için özet akış

| Aşama | Kurulacaklar |
|---|---|
| 0 → 1 | P-1 (CONTEXT), P-8 (hijyen) |
| 1 → 2 | P-2 (tokens), P-3 (handoff başlat) |
| 2 başı | P-4 (metinler), P-5 (referans seti), P-6 (varlık kilidi), P-7 (bileşen envanteri) |
| Her aşama sonu | P-3 güncelle |

**Stack'e göre ek kurulum:** Proje web dışı bir hedefe (React Native,
masaüstü vb.) gidiyorsa, o platformun **inşa edilebilirlik kısıtları** ayrı
bir dosyaya yazılır ve tasarım ajanlarına bağlanır.
Örnek: `agency/reference/rn-tasarim-kisitlari.md` (React Native — CSS yok, hover
yok, grid yok). Tasarımcı web alışkanlığıyla inşa edilemez bir şey üretirse
sonuç doğrudan revizyon turudur.

**Atlama kuralı:** Bir madde bu proje için gereksizse (ör. tek ekranlık iç
araçta P-7 fazla gelebilir) PM bunu `projects/trinkow/status/BACKLOG.md`'de **"atlandı +
gerekçe"** olarak yazar. Sessizce atlanmaz — sonraki projede aynı kararı
yeniden tartışmamak için gerekçe kalır.
