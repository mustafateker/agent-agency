import type { SQLiteDatabase } from 'expo-sqlite';

import { ayarOku, harcamaEkle, ODEME_VARSAYILAN, type OdemeTipi } from '@/db/harcama';
import { lira } from '@/lib/para';
import { ayAnahtari, gunAnahtari, gunEkle } from '@/lib/tarih';

export const SEMA_SURUMU = 1;

/**
 * Örnek veri sürümü. Faz 1'de veritabanındaki her kayıt bu dosyadan gelir
 * (harcama ekleme akışı henüz kodlanmadı), bu yüzden sürüm değişince örnek
 * kayıtlar tazelenir — yoksa simülatördeki eski kurulum prototiple
 * uyuşmayan sayıları göstermeye devam eder.
 *
 * TODO(Ü-5): Kullanıcı ilk kaydını yazdığında `ayar.kullanici_verisi = '1'`
 * konmalı; aşağıdaki tazeleme o bayrak varken ÇALIŞMAZ.
 */
export const ORNEK_VERI_SURUMU = 2;

/**
 * Şema — Faz 1 iskeleti.
 * PARA: tüm tutar kolonları INTEGER ve KURUŞ cinsinden. REAL kullanılmaz.
 */
const SEMA = `
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS harcama (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  tutar_kurus INTEGER NOT NULL,
  kategori    TEXT    NOT NULL,
  urun_adi    TEXT,
  zaman       TEXT    NOT NULL,
  gun         TEXT    NOT NULL,
  odeme       TEXT    NOT NULL CHECK (odeme IN ('nakit', 'kart'))
);
CREATE INDEX IF NOT EXISTS harcama_gun ON harcama (gun);

CREATE TABLE IF NOT EXISTS kategori_limiti (
  kategori    TEXT    PRIMARY KEY,
  limit_kurus INTEGER NOT NULL,
  sira        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ayar (
  anahtar TEXT PRIMARY KEY,
  deger   TEXT NOT NULL
);

-- v4 · K-048 seri hesabı: kayıt yazılmamış bir günün "harcamasız" işareti.
-- Harcama satırı DEĞİLDİR — hile kapısının (b) şıkkı burada tutulur.
CREATE TABLE IF NOT EXISTS gun_durumu (
  gun         TEXT PRIMARY KEY,
  harcamasiz  INTEGER NOT NULL DEFAULT 0
);
`;

/**
 * D-2 (E-11…E-14) eklentileri: not metni + taksit serisi alanları.
 * `ALTER TABLE ADD COLUMN` — mevcut veriyi SİLMEZ, yalnız eksik kolonu
 * ekler. `PRAGMA table_info` ile önce kontrol edilir (SQLite'ta
 * `ADD COLUMN IF NOT EXISTS` yok, ikinci kez eklemek hataya düşer).
 */
const EK_KOLONLAR: { tablo: string; kolon: string; tip: string }[] = [
  { tablo: 'harcama', kolon: 'not_metni', tip: 'TEXT' },
  { tablo: 'harcama', kolon: 'taksit_id', tip: 'TEXT' },
  { tablo: 'harcama', kolon: 'taksit_no', tip: 'INTEGER' },
  { tablo: 'harcama', kolon: 'taksit_toplam', tip: 'INTEGER' },
];

async function eksikKolonlariEkle(db: SQLiteDatabase): Promise<void> {
  for (const { tablo, kolon, tip } of EK_KOLONLAR) {
    const kolonlar = await db.getAllAsync<{ name: string }>(`PRAGMA table_info(${tablo})`);
    if (!kolonlar.some((k) => k.name === kolon)) {
      await db.execAsync(`ALTER TABLE ${tablo} ADD COLUMN ${kolon} ${tip}`);
    }
  }
}

export async function semayiKur(db: SQLiteDatabase): Promise<void> {
  const { user_version: surum = 0 } =
    (await db.getFirstAsync<{ user_version: number }>('PRAGMA user_version')) ?? {};
  await db.execAsync(SEMA);
  await eksikKolonlariEkle(db);
  if (surum < SEMA_SURUMU) {
    await db.execAsync(`PRAGMA user_version = ${SEMA_SURUMU}`);
  }
  // v4 · seri/gün sayfalama geriye sınırı (K-049): ilk kez kuruluyorsa bugünü
  // "kurulum günü" olarak sabitler — örnek veri silinse/tazelense bile bu
  // sınır DEĞİŞMEZ (gerçek kullanıcıda "uygulamayı ilk açtığın gün" budur).
  const kurulumGunu = await db.getFirstAsync<{ deger: string }>(
    "SELECT deger FROM ayar WHERE anahtar = 'kurulum_gunu'",
  );
  if (!kurulumGunu) {
    await db.runAsync(
      "INSERT INTO ayar (anahtar, deger) VALUES ('kurulum_gunu', ?)",
      gunAnahtari(new Date()),
    );
  }
  await ornekVeriYaz(db);
}

/**
 * İlk açılışta örnek veri yazılır, sonra panoda okunur — veri akışının
 * çalıştığının kanıtı. TÜM sayılar onaylı prototipten alındı, uydurulmadı:
 * projects/trinkow/docs/design/prototip-v3/01-bugun.html
 *
 *   · günlük limit          300 ₺
 *   · bugün (limit altı)    95 + 42 + 43 = 180 ₺ → kalan 120 ₺
 *   · Market  ay toplamı  2.180 / 3.000 ₺
 *   · Kafe    ay toplamı    940 / 1.200 ₺
 *   · ay içindeki limit aşımı gün sayısı: 6 (imza kartının sayısı)
 *
 * Kategori ay toplamları AYIN TAMAMININ toplamıdır; bu yüzden geçmiş
 * kayıtlar aşağıdaki plana göre güne dağıtılır ve toplamları tutar.
 */

/** Bir günün örnek kayıtları: [kategori, tutar (₺), ödeme, saat, dakika] */
type Kayit = [string, number, OdemeTipi, number, number];

/**
 * Gün planı — anahtar: kaç gün önce. Toplamlar prototiple birebir:
 * Market 2.180 · Kafe 940 · aşım günü 6 (1, 3, 4, 5, 6, 7 gün önce).
 * 2 gün önce bilerek boştur: boş durum yüzeyi (`?gun=-2`) gerçek veriyle görülür.
 */
const GUN_PLANI: Record<number, Kayit[]> = {
  // bugün · 180 ₺ · limit altı (varsayılan yüzey)
  0: [
    ['kafe', 95, 'nakit', 8, 20],
    ['ulasim', 42, ODEME_VARSAYILAN, 9, 5],
    ['market', 43, ODEME_VARSAYILAN, 18, 40],
  ],
  // dün · 360 ₺ · limit dışı yüzeyi (`?gun=-1`) — "Limitin 60 ₺ üzerindesin."
  1: [
    ['market', 210, ODEME_VARSAYILAN, 12, 30],
    ['restoran', 150, ODEME_VARSAYILAN, 21, 30],
  ],
  // 2 gün önce: kayıt yok — boş durum
  3: [['market', 380, ODEME_VARSAYILAN, 11, 15]],
  4: [
    ['market', 275, ODEME_VARSAYILAN, 13, 40],
    ['kafe', 90, 'nakit', 16, 0],
  ],
  5: [['market', 410, ODEME_VARSAYILAN, 10, 5]],
  6: [
    ['market', 300, ODEME_VARSAYILAN, 12, 0],
    ['kafe', 120, ODEME_VARSAYILAN, 15, 30],
  ],
  7: [
    ['market', 350, ODEME_VARSAYILAN, 19, 20],
    ['kafe', 65, 'nakit', 9, 45],
  ],
  // buradan sonrası limit altı günler — yalnız ay toplamlarını tamamlar
  8: [
    ['kafe', 185, ODEME_VARSAYILAN, 14, 10],
    ['market', 60, ODEME_VARSAYILAN, 18, 5],
  ],
  9: [
    ['kafe', 160, 'nakit', 11, 0],
    ['market', 72, ODEME_VARSAYILAN, 17, 25],
  ],
  10: [
    ['kafe', 125, ODEME_VARSAYILAN, 10, 30],
    ['market', 80, ODEME_VARSAYILAN, 20, 0],
  ],
  11: [['kafe', 100, 'nakit', 9, 15]],
};

/**
 * Planlanan günü İÇİNDE BULUNULAN AYA sabitler. Ayın ilk günlerinde
 * uygulama ilk kez açılırsa `bugün - 11` bir önceki aya taşar ve kategori
 * ay toplamları prototiple tutmaz; bu durumda kayıt ayın ilerisine alınır —
 * toplamlar ay bazlı olduğu için sayılar bozulmaz.
 */
function ayIciGun(bugun: Date, gunOnce: number): Date {
  const geri = gunEkle(bugun, -gunOnce);
  if (ayAnahtari(geri) === ayAnahtari(bugun)) return geri;
  const ileri = gunEkle(bugun, gunOnce - (bugun.getDate() - 1));
  return ayAnahtari(ileri) === ayAnahtari(bugun) ? ileri : geri;
}

async function ornekVeriYaz(db: SQLiteDatabase): Promise<void> {
  const kullaniciVerisi = await ayarOku(db, 'kullanici_verisi');
  const surum = await ayarOku(db, 'ornek_veri_surumu');
  const mevcut = await db.getFirstAsync<{ adet: number }>('SELECT COUNT(*) AS adet FROM harcama');
  const doluMu = (mevcut?.adet ?? 0) > 0;

  if (doluMu) {
    // Kullanıcı verisi varsa asla dokunulmaz.
    if (kullaniciVerisi === '1') return;
    if (surum === String(ORNEK_VERI_SURUMU)) return;
    await db.execAsync('DELETE FROM harcama; DELETE FROM kategori_limiti;');
  }

  await db.runAsync(
    "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('ornek_veri_surumu', ?)",
    String(ORNEK_VERI_SURUMU),
  );

  await db.runAsync(
    "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('gunluk_limit_kurus', ?)",
    String(lira(300)),
  );

  // Aylık kategori limitleri — prototipteki değerler (Market 3.000 · Kafe 1.200)
  const limitler: [string, number, number][] = [
    ['market', lira(3000), 1],
    ['kafe', lira(1200), 2],
  ];
  for (const [kod, limitKurus, sira] of limitler) {
    await db.runAsync(
      'INSERT OR REPLACE INTO kategori_limiti (kategori, limit_kurus, sira) VALUES (?, ?, ?)',
      kod,
      limitKurus,
      sira,
    );
  }

  const bugun = new Date();
  for (const [gunOnceMetin, kayitlar] of Object.entries(GUN_PLANI)) {
    const g = ayIciGun(bugun, Number(gunOnceMetin));
    for (const [kategori, tutarLira, odeme, saat, dakika] of kayitlar) {
      const zaman = new Date(g);
      zaman.setHours(saat, dakika, 0, 0);
      await harcamaEkle(db, {
        tutarKurus: lira(tutarLira),
        kategori,
        urunAdi: null,
        zaman: zaman.toISOString(),
        gun: gunAnahtari(zaman),
        odeme,
        notMetni: null,
        taksitId: null,
        taksitNo: null,
        taksitToplam: null,
      });
    }
  }
}
