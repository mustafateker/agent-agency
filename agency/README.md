# agency/ — Otomasyon Sistemi

Burası **ajansın kendisi**: ajan tanımları, operasyon kuralları, ortak
varlıklar ve projelerin doküman/durum kayıtları. Çalışan ürün kodu bu
klasöre girmez; repo kökündeki `../mobile/` ve `../backend/` altında yaşar.

```
agency/
├── CLAUDE.md   ← ajans talimatları ve onay kuralları
├── .claude/   ← uzman ajan tanımları ve ayarları
├── templates/   ← her projede kurulan iskeletler
├── reference/   ← her projede uyulan kurallar ve kaynak listeleri
├── vendor/      ← dışarıdan alınan, bizim yazmadığımız kaynaklar
└── projects/    ← proje bağlamı, tasarım belgeleri ve operasyon durumu
```

## Çalıştırma

```bash
cd agency
claude
```

`.claude/settings.json` oturumu `pm-orchestrator` ile açar. Aktif proje
`projects/trinkow/`; uygulama kodu sırasıyla `../mobile/` ve `../backend/`dedir.

## templates/
| Dosya | Ne işe yarar |
|---|---|
| `proje-kurulum-checklist.md` | Her yeni projede kurulması gereken 8 varlık (P-1…P-8): bağlam paketi, marka tokenları, devir-teslim günlüğü, gerçek metinler, referans seti, varlık kilidi, bileşen envanteri, repo hijyeni. Her maddede sahibi, zamanlaması, kazanç gerekçesi ve DoD var. |
| `brandbook-template.md` | `brand-strategist`in dolduracağı marka iskeleti. |

## reference/
| Dosya | Ne işe yarar |
|---|---|
| `jenerik-ai-ui-anti-pattern-listesi.md` | "AI yapmış gibi duran" arayüzden kaçınma listesi. `design-reviewer`in ana kontrol listesi. **Proje bazında gevşetilebilir** — gevşetme o projenin `CONTEXT.md`'sine yazılır, buraya değil. |
| `referans-repolar.md` | 54 doğrulanmış GitHub reposu, 10 kategori. **Kural: sistematik alınır, görsel stil alınmaz.** |
| `rn-tasarim-kisitlari.md` | React Native'de neyin çalışmadığı (hover yok, CSS Grid yok, gölge platforma göre değişir, 44pt dokunma hedefi). Mobil projede bağlayıcı. |
| `open-design-entegrasyon.md` | `vendor/open-design` skill'inin nasıl kullanılacağı + **çerçeve/içerik ayrımı** kuralı. |

## vendor/
Dışarıdan alınan kaynaklar. **Bu dosyaları biz düzenlemeyiz** — güncellemek
gerekirse kaynağından yeniden çekilir.

| Klasör | Kaynak | Lisans |
|---|---|---|
| `open-design/` | `github.com/nexu-io/open-design` — mobil ekran skill'i: iPhone çerçevesi, 6 arketip, P0 kontrol listesi | Apache-2.0 |
| `design-systems/` | 138 design system spesifikasyonu + `interop-protocol.md` + `crosswalk.md` | (kaynağıyla birlikte geldi) |

---

## Bir dosya nereye ait?

> **"İkinci bir proje başlasa bu dosyayı kopyalar mıydım?"**
> Evet → ajansın `templates/`, `reference/` veya `vendor/` alanı ·
> Hayır → `projects/<ad>/`

Örnekler:
- RN kısıtları → **agency** (her mobil projede aynı)
- Trinkow'un brandbook'u → **projects** (yalnız Trinkow'un)
- 138 design system kütüphanesi → **agency** (kaynak havuzu)
- Trinkow'un seçtiği claymorphism → **projects** (o projenin kararı)
- Anti-pattern listesi → **agency** (kural)
- Emoji yasağı → **projects** (Trinkow'a özel karar, `CONTEXT.md`'de)

## Değiştirmeden önce
`agency/` altındaki bir dosyayı değiştirmek **bütün projeleri** etkiler.
Proje-özel bir ihtiyaç varsa kuralı burada değiştirme — o projenin
`CONTEXT.md`'sine **geçersiz kılma** olarak yaz. Bu yöntemin örnekleri:
Trinkow'da emoji yasağı (K-004), gölge/gradyan serbestliği (K-019),
Poppins/Montserrat izni (K-024).
