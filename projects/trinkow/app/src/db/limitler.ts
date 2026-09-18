import type { SQLiteDatabase } from 'expo-sqlite';

import { TUM_KATEGORILER, type KategoriKodu } from '@/lib/kategoriler';

/**
 * E-17 — günlük limit + kategori limitleri yazma/okuma. Ayrı dosya:
 * `db/harcama.ts` harcama TABLOSUNU sorgular, bu dosya AYAR/limit
 * tablolarını yazar (farklı sorumluluk).
 */

/** Tüm kategori limitleri — yalnız DEĞERİ OLANLAR (Record: kod → kuruş). */
export async function tumKategoriLimitleri(db: SQLiteDatabase): Promise<Record<string, number>> {
  const satirlar = await db.getAllAsync<{ kategori: string; limit_kurus: number }>(
    'SELECT kategori, limit_kurus FROM kategori_limiti',
  );
  const sonuc: Record<string, number> = {};
  for (const s of satirlar) sonuc[s.kategori] = s.limit_kurus;
  return sonuc;
}

/** Kategori limiti yaz/güncelle. `sira` kategori listesindeki sabit sıradan gelir. */
export async function kategoriLimitiKaydet(
  db: SQLiteDatabase,
  kod: KategoriKodu,
  limitKurus: number,
): Promise<void> {
  const sira = TUM_KATEGORILER.indexOf(kod) + 1;
  await db.runAsync(
    'INSERT OR REPLACE INTO kategori_limiti (kategori, limit_kurus, sira) VALUES (?, ?, ?)',
    kod,
    Math.round(limitKurus),
    sira,
  );
}

/** Kategori limitini kaldır — veri (harcama) SİLİNMEZ, yalnız takip durur (K-029). */
export async function kategoriLimitiSil(db: SQLiteDatabase, kod: KategoriKodu): Promise<void> {
  await db.runAsync('DELETE FROM kategori_limiti WHERE kategori = ?', kod);
}

/** Günlük limiti yaz/güncelle — `ayar.gunluk_limit_kurus`. */
export async function gunlukLimitKaydet(db: SQLiteDatabase, limitKurus: number): Promise<void> {
  await db.runAsync(
    "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('gunluk_limit_kurus', ?)",
    String(Math.round(limitKurus)),
  );
}
