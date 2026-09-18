import type { SQLiteDatabase } from 'expo-sqlite';

/**
 * E-16 — haftalık özet sorguları. `db/harcama.ts`'teki gün/ay bazlı
 * fonksiyonlardan ayrı: burada aralık (hafta) bazlı gruplama var.
 */

export type GunToplami = { gun: string; toplamKurus: number };

/** Hafta aralığındaki (dahil) günlük toplamlar — veri olmayan günler listede yok. */
export async function haftaGunToplamlari(
  db: SQLiteDatabase,
  baslangicGunu: string,
  bitisGunu: string,
): Promise<GunToplami[]> {
  const satirlar = await db.getAllAsync<{ gun: string; toplam: number }>(
    'SELECT gun, SUM(tutar_kurus) AS toplam FROM harcama WHERE gun BETWEEN ? AND ? GROUP BY gun',
    baslangicGunu,
    bitisGunu,
  );
  return satirlar.map((s) => ({ gun: s.gun, toplamKurus: s.toplam }));
}

export type KategoriPayi = { kategori: string; toplamKurus: number };

/** Hafta aralığında kategoriye göre toplam — büyükten küçüğe. */
export async function haftaKategoriDagilimi(
  db: SQLiteDatabase,
  baslangicGunu: string,
  bitisGunu: string,
): Promise<KategoriPayi[]> {
  const satirlar = await db.getAllAsync<{ kategori: string; toplam: number }>(
    `SELECT kategori, SUM(tutar_kurus) AS toplam FROM harcama
     WHERE gun BETWEEN ? AND ? GROUP BY kategori ORDER BY toplam DESC`,
    baslangicGunu,
    bitisGunu,
  );
  return satirlar.map((s) => ({ kategori: s.kategori, toplamKurus: s.toplam }));
}

export type KucukHarcamaOzeti = { adet: number; toplamKurus: number };

/** "50 ₺ altı" harcamaların adedi + toplamı (Latte Faktörü — ürünün varlık sebebi). */
export async function haftaKucukHarcamaOzeti(
  db: SQLiteDatabase,
  baslangicGunu: string,
  bitisGunu: string,
  esikKurus = 5000,
): Promise<KucukHarcamaOzeti> {
  const r = await db.getFirstAsync<{ adet: number; toplam: number | null }>(
    'SELECT COUNT(*) AS adet, SUM(tutar_kurus) AS toplam FROM harcama WHERE gun BETWEEN ? AND ? AND tutar_kurus < ?',
    baslangicGunu,
    bitisGunu,
    esikKurus,
  );
  return { adet: r?.adet ?? 0, toplamKurus: r?.toplam ?? 0 };
}

/** Hafta aralığında hiç kayıt var mı — boş durum kararı. */
export async function haftaKayitVarMi(
  db: SQLiteDatabase,
  baslangicGunu: string,
  bitisGunu: string,
): Promise<boolean> {
  const r = await db.getFirstAsync<{ adet: number }>(
    'SELECT COUNT(*) AS adet FROM harcama WHERE gun BETWEEN ? AND ? LIMIT 1',
    baslangicGunu,
    bitisGunu,
  );
  return (r?.adet ?? 0) > 0;
}
