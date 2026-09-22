/**
 * D-2c-2 — oturum deposu. Erişim + yenileme token'ı ve kullanıcı kimliği
 * TEK YERDEN okunur/yazılır; `src/lib/api.ts` ve ekranlar bu modülün
 * DIŞINDA hiçbir yerde token okumaz/yazmaz.
 *
 * ⚠️ Güvenli saklama (`expo-secure-store`) YENİ BAĞIMLILIK olduğu için
 * onay bekliyor (bkz. görev brifi). Bu yüzden bu tur `expo-sqlite` ile
 * ayrı, izole bir `oturum` tablosuna yazar (uygulamanın harcama
 * veritabanıyla aynı dosya, `db/semasi.ts`'e DOKUNULMADI — bilerek: bu
 * tablo `expo-secure-store` onaylanınca buradan tamamen silinip modülün
 * İÇİ değişecek, `db/semasi.ts`'in sürüm geçmişini kirletmesin).
 * Çağıranlar (`api.ts`, `hesapEylemleri.ts`, ekranlar) yalnız bu dosyanın
 * dışa açtığı fonksiyonları çağırır — o gün tek dosya değişir, çağıranlar
 * DEĞİŞMEZ.
 *
 * NOT (güvenlik sınırı, bilerek kabul edildi): SQLite şifrelenmemiştir;
 * bu yalnız `expo-secure-store` onaylanana kadarki GEÇİCİ bir çözümdür.
 */
import { openDatabaseAsync, type SQLiteDatabase } from 'expo-sqlite';

import { DB_ADI } from '@/db';

export type Oturum = {
  erisimTokeni: string;
  yenilemeTokeni: string;
  kullaniciId: string;
  email: string;
  /** `google` · `apple` · `sifre` — bkz. backend `kimlik_saglayici`. */
  kimlikSaglayici: string;
};

let dbSozu: Promise<SQLiteDatabase> | null = null;

function db(): Promise<SQLiteDatabase> {
  if (!dbSozu) {
    dbSozu = openDatabaseAsync(DB_ADI).then(async (d) => {
      await d.execAsync(
        `CREATE TABLE IF NOT EXISTS oturum (
          id                INTEGER PRIMARY KEY CHECK (id = 1),
          erisim_tokeni     TEXT NOT NULL,
          yenileme_tokeni   TEXT NOT NULL,
          kullanici_id      TEXT NOT NULL,
          email             TEXT NOT NULL,
          kimlik_saglayici  TEXT NOT NULL
        )`,
      );
      return d;
    });
  }
  return dbSozu;
}

type Satir = {
  erisim_tokeni: string;
  yenileme_tokeni: string;
  kullanici_id: string;
  email: string;
  kimlik_saglayici: string;
};

export async function oturumOku(): Promise<Oturum | null> {
  const d = await db();
  const satir = await d.getFirstAsync<Satir>('SELECT * FROM oturum WHERE id = 1');
  if (!satir) return null;
  return {
    erisimTokeni: satir.erisim_tokeni,
    yenilemeTokeni: satir.yenileme_tokeni,
    kullaniciId: satir.kullanici_id,
    email: satir.email,
    kimlikSaglayici: satir.kimlik_saglayici,
  };
}

export async function oturumYaz(oturum: Oturum): Promise<void> {
  const d = await db();
  await d.runAsync(
    `INSERT INTO oturum (id, erisim_tokeni, yenileme_tokeni, kullanici_id, email, kimlik_saglayici)
     VALUES (1, ?, ?, ?, ?, ?)
     ON CONFLICT(id) DO UPDATE SET
       erisim_tokeni = excluded.erisim_tokeni,
       yenileme_tokeni = excluded.yenileme_tokeni,
       kullanici_id = excluded.kullanici_id,
       email = excluded.email,
       kimlik_saglayici = excluded.kimlik_saglayici`,
    oturum.erisimTokeni,
    oturum.yenilemeTokeni,
    oturum.kullaniciId,
    oturum.email,
    oturum.kimlikSaglayici,
  );
  oturumDegisti();
}

/** Yalnız `token/yenile` sonrası — yenileme token'ı sabit kalır. */
export async function oturumErisimTokeniGuncelle(erisimTokeni: string): Promise<void> {
  const d = await db();
  await d.runAsync('UPDATE oturum SET erisim_tokeni = ? WHERE id = 1', erisimTokeni);
}

export async function oturumSil(): Promise<void> {
  const d = await db();
  await d.runAsync('DELETE FROM oturum WHERE id = 1');
  oturumDegisti();
}

/**
 * Ekranlar arası "oturum değişti" sinyali (bkz. `lib/veriBus.ts` deseni) —
 * `AccountSection`/Ayarlar bunu dinleyip yeniden okur.
 */
type Dinleyici = () => void;
const dinleyiciler = new Set<Dinleyici>();

export function oturumDegisti(): void {
  for (const d of dinleyiciler) d();
}

export function oturumDegisimineAbone(dinleyici: Dinleyici): () => void {
  dinleyiciler.add(dinleyici);
  return () => dinleyiciler.delete(dinleyici);
}
