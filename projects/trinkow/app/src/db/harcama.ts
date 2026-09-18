import type { SQLiteBindValue, SQLiteDatabase } from 'expo-sqlite';

import { ayEkle, gunAnahtari } from '@/lib/tarih';

/**
 * Harcama veri modeli — backlog Ü-5'e hazır: ürün adı / tutar / tarih
 * AYRI alanlardır, tek serbest metin değil.
 *
 * PARA: `tutarKurus` DAİMA kuruş cinsinden integer. Float ile para tutmak
 * sessiz kuruş hatası üretir; SQLite kolonu da INTEGER.
 */
export type OdemeTipi = 'nakit' | 'kart';

/** §7 / K-036 — ödeme tipinde tek varsayılan: Kart. */
export const ODEME_VARSAYILAN: OdemeTipi = 'kart';

export type Harcama = {
  id: number;
  /** kuruş integer */
  tutarKurus: number;
  kategori: string;
  /** Ü-5 — ayrı alan; yoksa kategori adı gösterilir */
  urunAdi: string | null;
  /** ISO 8601 yerel damga */
  zaman: string;
  /** 'YYYY-MM-DD' yerel gün anahtarı */
  gun: string;
  odeme: OdemeTipi;
  /** E-12 "Not" alanı — isteğe bağlı, tek satır */
  notMetni: string | null;
  /** Taksit serisi grubu — null ise tek harcama */
  taksitId: string | null;
  /** 1 tabanlı taksit sırası (3/12 → 3) */
  taksitNo: number | null;
  /** Serideki toplam taksit sayısı (3/12 → 12) */
  taksitToplam: number | null;
};

type HarcamaSatiri = {
  id: number;
  tutar_kurus: number;
  kategori: string;
  urun_adi: string | null;
  zaman: string;
  gun: string;
  odeme: OdemeTipi;
  not_metni: string | null;
  taksit_id: string | null;
  taksit_no: number | null;
  taksit_toplam: number | null;
};

function cevir(r: HarcamaSatiri): Harcama {
  return {
    id: r.id,
    tutarKurus: r.tutar_kurus,
    kategori: r.kategori,
    urunAdi: r.urun_adi,
    zaman: r.zaman,
    gun: r.gun,
    odeme: r.odeme,
    notMetni: r.not_metni,
    taksitId: r.taksit_id,
    taksitNo: r.taksit_no,
    taksitToplam: r.taksit_toplam,
  };
}

const SATIR_SUTUNLARI = `id, tutar_kurus, kategori, urun_adi, zaman, gun, odeme, not_metni, taksit_id, taksit_no, taksit_toplam`;

export async function gununHarcamalari(db: SQLiteDatabase, gun: string): Promise<Harcama[]> {
  const satirlar = await db.getAllAsync<HarcamaSatiri>(
    `SELECT ${SATIR_SUTUNLARI} FROM harcama WHERE gun = ? ORDER BY zaman ASC`,
    gun,
  );
  return satirlar.map(cevir);
}

/** Bir ayın TÜM kayıtları — E-14 gün gruplama burada, `src/lib/gruplama.ts` ile. */
export async function ayHarcamalari(db: SQLiteDatabase, ay: string): Promise<Harcama[]> {
  const satirlar = await db.getAllAsync<HarcamaSatiri>(
    `SELECT ${SATIR_SUTUNLARI} FROM harcama WHERE substr(gun, 1, 7) = ? ORDER BY zaman ASC`,
    ay,
  );
  return satirlar.map(cevir);
}

export type AySpecifiOzeti = { adet: number; toplamKurus: number };

/** `kayitlar.ay_ozet` — "{adet} kayıt · {tutar}" (E-14 ay değiştirici). */
export async function ayOzeti(db: SQLiteDatabase, ay: string): Promise<AySpecifiOzeti> {
  const r = await db.getFirstAsync<{ adet: number; toplam: number | null }>(
    'SELECT COUNT(*) AS adet, SUM(tutar_kurus) AS toplam FROM harcama WHERE substr(gun, 1, 7) = ?',
    ay,
  );
  return { adet: r?.adet ?? 0, toplamKurus: r?.toplam ?? 0 };
}

/** E-14 — hiç kayıt yok mu (tüm zamanlar)? Ay değiştiricinin gösterilip gösterilmeyeceğini belirler. */
export async function herhangiKayitVarMi(db: SQLiteDatabase): Promise<boolean> {
  const r = await db.getFirstAsync<{ adet: number }>('SELECT COUNT(*) AS adet FROM harcama LIMIT 1');
  return (r?.adet ?? 0) > 0;
}

export async function gunToplami(db: SQLiteDatabase, gun: string): Promise<number> {
  const r = await db.getFirstAsync<{ toplam: number | null }>(
    'SELECT SUM(tutar_kurus) AS toplam FROM harcama WHERE gun = ?',
    gun,
  );
  return r?.toplam ?? 0;
}

/** Ayın limit aşılan gün sayısı — imza kartının sayısı (`pano.limit_sorgu.baslik`). */
export async function ayAsimSayisi(
  db: SQLiteDatabase,
  ay: string,
  gunlukLimitKurus: number,
): Promise<number> {
  const r = await db.getFirstAsync<{ adet: number }>(
    `SELECT COUNT(*) AS adet FROM (
       SELECT gun, SUM(tutar_kurus) AS toplam FROM harcama
       WHERE substr(gun, 1, 7) = ? GROUP BY gun HAVING toplam > ?
     )`,
    ay,
    gunlukLimitKurus,
  );
  return r?.adet ?? 0;
}

export type KategoriDurumu = {
  kategori: string;
  harcananKurus: number;
  limitKurus: number;
  /** v4 E-10 — o günün (bugünün) kategori toplamı, K-056 ikincil satır. `gun` verilmezse 0. */
  bugunKurus: number;
};

/**
 * Aylık kategori limitleri + o ayın kategori toplamı. Limiti olmayan kategori
 * listelenmez. `gun` verilirse (v4 E-10 Günlük kartı) o günün toplamı da
 * döner — K-056: kart satırının birincil ölçeği DAİMA aylık/aylık, günün
 * tutarı yalnız ikincil satırda görünür.
 */
export async function kategoriDurumlari(
  db: SQLiteDatabase,
  ay: string,
  gun?: string,
): Promise<KategoriDurumu[]> {
  return db.getAllAsync<KategoriDurumu>(
    `SELECT kl.kategori AS kategori,
            kl.limit_kurus AS limitKurus,
            COALESCE((SELECT SUM(h.tutar_kurus) FROM harcama h
                      WHERE h.kategori = kl.kategori AND substr(h.gun, 1, 7) = ?), 0) AS harcananKurus,
            COALESCE((SELECT SUM(h.tutar_kurus) FROM harcama h
                      WHERE h.kategori = kl.kategori AND h.gun = ?), 0) AS bugunKurus
     FROM kategori_limiti kl
     ORDER BY kl.sira ASC`,
    ay,
    gun ?? '',
  );
}

/** v4 K-049 — ilk kaydın günü (tüm zamanlar MIN). Hiç kayıt yoksa `null`. */
export async function ilkKayitGunu(db: SQLiteDatabase): Promise<string | null> {
  const r = await db.getFirstAsync<{ gun: string | null }>('SELECT MIN(gun) AS gun FROM harcama');
  return r?.gun ?? null;
}

export type GunToplami = { gun: string; toplamKurus: number; kayitAdedi: number };

/**
 * Bir tarih aralığındaki (dahil) günlük toplamlar — tek sorguda toplu okuma.
 * E-21 (son 4 hafta) ve E-24 (ay ızgarası) bu fonksiyonu paylaşır; gün başına
 * ayrı sorgu atmak yerine `GROUP BY gun` ile tek seferde okunur.
 */
export async function gunAraligiToplamlari(
  db: SQLiteDatabase,
  baslangicGun: string,
  bitisGun: string,
): Promise<Map<string, GunToplami>> {
  const satirlar = await db.getAllAsync<{ gun: string; toplam: number; adet: number }>(
    `SELECT gun, SUM(tutar_kurus) AS toplam, COUNT(*) AS adet FROM harcama
     WHERE gun BETWEEN ? AND ? GROUP BY gun`,
    baslangicGun,
    bitisGun,
  );
  const harita = new Map<string, GunToplami>();
  for (const s of satirlar) {
    harita.set(s.gun, { gun: s.gun, toplamKurus: s.toplam, kayitAdedi: s.adet });
  }
  return harita;
}

export async function ayarOku(db: SQLiteDatabase, anahtar: string): Promise<string | null> {
  const r = await db.getFirstAsync<{ deger: string }>(
    'SELECT deger FROM ayar WHERE anahtar = ?',
    anahtar,
  );
  return r?.deger ?? null;
}

export async function ayarYaz(db: SQLiteDatabase, anahtar: string, deger: string): Promise<void> {
  await db.runAsync('INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES (?, ?)', anahtar, deger);
}

/** Günlük limit — kuruş integer. Tanımsızsa null (`HeroPlain` varyantı). */
export async function gunlukLimit(db: SQLiteDatabase): Promise<number | null> {
  const d = await ayarOku(db, 'gunluk_limit_kurus');
  return d === null ? null : Number.parseInt(d, 10);
}

/** Tek kayıt — E-12 detay ekranı. Bulunamazsa `null` (`detay.bulunamadi.*`). */
export async function harcamaGetir(db: SQLiteDatabase, id: number): Promise<Harcama | null> {
  const r = await db.getFirstAsync<HarcamaSatiri>(
    `SELECT ${SATIR_SUTUNLARI} FROM harcama WHERE id = ?`,
    id,
  );
  return r ? cevir(r) : null;
}

/** Tek harcama yazma — tutar kuruş integer olarak gelir. */
export async function harcamaEkle(
  db: SQLiteDatabase,
  h: Omit<Harcama, 'id'>,
): Promise<number> {
  const sonuc = await db.runAsync(
    `INSERT INTO harcama
       (tutar_kurus, kategori, urun_adi, zaman, gun, odeme, not_metni, taksit_id, taksit_no, taksit_toplam)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    Math.round(h.tutarKurus),
    h.kategori,
    h.urunAdi,
    h.zaman,
    h.gun,
    h.odeme,
    h.notMetni,
    h.taksitId,
    h.taksitNo,
    h.taksitToplam,
  );
  return sonuc.lastInsertRowId;
}

export type HarcamaGuncelleme = Partial<
  Pick<Harcama, 'tutarKurus' | 'kategori' | 'urunAdi' | 'odeme' | 'notMetni' | 'zaman' | 'gun'>
>;

/** E-12 "Kaydet" — yalnız verilen alanları günceller. Taksitli kayıtta tutar/tarih önerilmez (UI katmanında engellenir). */
export async function harcamaGuncelle(
  db: SQLiteDatabase,
  id: number,
  degisiklik: HarcamaGuncelleme,
): Promise<void> {
  const alanlar: string[] = [];
  const degerler: SQLiteBindValue[] = [];
  const eslesme: Record<string, SQLiteBindValue | undefined> = {
    tutar_kurus: degisiklik.tutarKurus !== undefined ? Math.round(degisiklik.tutarKurus) : undefined,
    kategori: degisiklik.kategori,
    urun_adi: degisiklik.urunAdi,
    odeme: degisiklik.odeme,
    not_metni: degisiklik.notMetni,
    zaman: degisiklik.zaman,
    gun: degisiklik.gun,
  };
  for (const [sutun, deger] of Object.entries(eslesme)) {
    if (deger !== undefined) {
      alanlar.push(`${sutun} = ?`);
      degerler.push(deger);
    }
  }
  if (alanlar.length === 0) return;
  await db.runAsync(`UPDATE harcama SET ${alanlar.join(', ')} WHERE id = ?`, ...degerler, id);
}

/** K-029 — tek harcama silme: onaysız, anında. Geri alma çağıranın sorumluluğunda (6 sn toast). */
export async function harcamaSil(db: SQLiteDatabase, id: number): Promise<void> {
  await db.runAsync('DELETE FROM harcama WHERE id = ?', id);
}

/** Aynı `taksitId`'ye sahip TÜM satırlar — E-12 taksit bilgi şeridi + E-13 özet satırı. */
export async function taksitSerisi(db: SQLiteDatabase, taksitId: string): Promise<Harcama[]> {
  const satirlar = await db.getAllAsync<HarcamaSatiri>(
    `SELECT ${SATIR_SUTUNLARI} FROM harcama WHERE taksit_id = ? ORDER BY taksit_no ASC`,
    taksitId,
  );
  return satirlar.map(cevir);
}

/** E-13 — taksit serisini TAMAMEN siler (K-029: onaylıdır, geri alma yoktur). */
export async function taksitSerisiSil(db: SQLiteDatabase, taksitId: string): Promise<void> {
  await db.runAsync('DELETE FROM harcama WHERE taksit_id = ?', taksitId);
}

type TaksitSerisiGirdi = {
  tutarKurusToplam: number;
  taksitSayisi: number;
  kategori: string;
  urunAdi: string | null;
  odeme: OdemeTipi;
  notMetni: string | null;
  ilkZaman: Date;
};

/**
 * K-023 taksit serisi — her ay için ayrı satır (E-18 "ay yükü" bunlardan
 * kurulur). Tutar kuruş-hassas dağıtılır: kalan kuruşlar İLK taksitlere
 * eklenir (12 × 833,33 gibi bölünemeyen tutarlarda kuruş kaybolmasın diye).
 */
export async function taksitSerisiOlustur(
  db: SQLiteDatabase,
  girdi: TaksitSerisiGirdi,
): Promise<{ taksitId: string; ilkId: number }> {
  const { tutarKurusToplam, taksitSayisi, kategori, urunAdi, odeme, notMetni, ilkZaman } = girdi;
  const taksitId = `t${Date.now()}${Math.random().toString(36).slice(2, 8)}`;
  const taban = Math.floor(tutarKurusToplam / taksitSayisi);
  const kalan = tutarKurusToplam - taban * taksitSayisi;

  let ilkId = -1;
  for (let i = 0; i < taksitSayisi; i += 1) {
    const tutar = taban + (i < kalan ? 1 : 0);
    const zaman = ayEkle(ilkZaman, i);
    const id = await harcamaEkle(db, {
      tutarKurus: tutar,
      kategori,
      urunAdi,
      zaman: zaman.toISOString(),
      gun: gunAnahtari(zaman),
      odeme,
      notMetni,
      taksitId,
      taksitNo: i + 1,
      taksitToplam: taksitSayisi,
    });
    if (i === 0) ilkId = id;
  }
  return { taksitId, ilkId };
}

export type SikAlinan = {
  urunAdi: string;
  kategori: string;
  tutarKurus: number;
  sonZaman: string;
};

/**
 * E-11 "Sık alınanlar" — kullanıcının kendi geçmişinden gelir, tahminden
 * değil: her satır gerçekten yazılmış bir kayıttır (prototip notu).
 * Ürün adı olmayan kayıtlar (yalnız kategoriyle girilenler) burada geçmez.
 */
export async function sikAlinanlar(db: SQLiteDatabase, limit = 3): Promise<SikAlinan[]> {
  const satirlar = await db.getAllAsync<{
    urun_adi: string;
    kategori: string;
    tutar_kurus: number;
    zaman: string;
  }>(
    `SELECT urun_adi, kategori, tutar_kurus, zaman FROM (
       SELECT urun_adi, kategori, tutar_kurus, zaman,
              ROW_NUMBER() OVER (PARTITION BY urun_adi ORDER BY zaman DESC) AS rn
       FROM harcama WHERE urun_adi IS NOT NULL AND urun_adi <> ''
     ) WHERE rn = 1 ORDER BY zaman DESC LIMIT ?`,
    limit,
  );
  return satirlar.map((r) => ({
    urunAdi: r.urun_adi,
    kategori: r.kategori,
    tutarKurus: r.tutar_kurus,
    sonZaman: r.zaman,
  }));
}

/** Ürün adına göre serbest arama (E-11 "Ne aldın" alanı) — Türkçe küçük harfe göre `includes`. */
export async function urunAra(db: SQLiteDatabase, sorgu: string, limit = 5): Promise<SikAlinan[]> {
  const hepsi = await sikAlinanlar(db, 200);
  const anahtar = sorgu.toLocaleLowerCase('tr');
  return hepsi.filter((s) => s.urunAdi.toLocaleLowerCase('tr').includes(anahtar)).slice(0, limit);
}

/* --------------------------------------------------------- E-15 kategori */

/** Bir kategorinin bir aydaki TÜM kayıtları, en yeni önce (prototip sırası). */
export async function kategoriAyHarcamalari(
  db: SQLiteDatabase,
  kategoriKodu: string,
  ay: string,
): Promise<Harcama[]> {
  const satirlar = await db.getAllAsync<HarcamaSatiri>(
    `SELECT ${SATIR_SUTUNLARI} FROM harcama WHERE kategori = ? AND substr(gun, 1, 7) = ? ORDER BY zaman DESC`,
    kategoriKodu,
    ay,
  );
  return satirlar.map(cevir);
}

/** Bir kategorinin bir aydaki toplamı + kayıt adedi. */
export async function kategoriAyOzeti(
  db: SQLiteDatabase,
  kategoriKodu: string,
  ay: string,
): Promise<AySpecifiOzeti> {
  const r = await db.getFirstAsync<{ adet: number; toplam: number | null }>(
    'SELECT COUNT(*) AS adet, SUM(tutar_kurus) AS toplam FROM harcama WHERE kategori = ? AND substr(gun, 1, 7) = ?',
    kategoriKodu,
    ay,
  );
  return { adet: r?.adet ?? 0, toplamKurus: r?.toplam ?? 0 };
}

/* -------------------------------------------------------- E-18 taksitler */

export type TaksitAySatiri = { ay: string; toplamKurus: number };

/** Bugünden başlayarak `aySayisi` ayın taksit toplamı (§7.12 `LoadBar`). */
export async function taksitAylikYuk(db: SQLiteDatabase, aySayisiler: string[]): Promise<TaksitAySatiri[]> {
  if (aySayisiler.length === 0) return [];
  const yerTutucular = aySayisiler.map(() => '?').join(', ');
  const satirlar = await db.getAllAsync<{ ay: string; toplam: number }>(
    `SELECT substr(gun, 1, 7) AS ay, SUM(tutar_kurus) AS toplam FROM harcama
     WHERE taksit_id IS NOT NULL AND substr(gun, 1, 7) IN (${yerTutucular})
     GROUP BY ay`,
    ...aySayisiler,
  );
  const eslesme = new Map(satirlar.map((s) => [s.ay, s.toplam]));
  return aySayisiler.map((ay) => ({ ay, toplamKurus: eslesme.get(ay) ?? 0 }));
}

/** Bu ayın taksit toplamı (E-18 kahraman kartı). */
export async function taksitBuAyToplam(db: SQLiteDatabase, buAy: string): Promise<number> {
  const r = await db.getFirstAsync<{ toplam: number | null }>(
    "SELECT SUM(tutar_kurus) AS toplam FROM harcama WHERE taksit_id IS NOT NULL AND substr(gun, 1, 7) = ?",
    buAy,
  );
  return r?.toplam ?? 0;
}

/** Bu ay dahil kalan TÜM taksit yükü — "Kalan toplam" (6 aylık pencereyle sınırlı değil). */
export async function taksitKalanToplamKurus(db: SQLiteDatabase, buAyBaslangicGunu: string): Promise<number> {
  const r = await db.getFirstAsync<{ toplam: number | null }>(
    'SELECT SUM(tutar_kurus) AS toplam FROM harcama WHERE taksit_id IS NOT NULL AND gun >= ?',
    buAyBaslangicGunu,
  );
  return r?.toplam ?? 0;
}

/** En geç biten serinin son ay anahtarı ("2027-05") — yoksa null. */
export async function taksitSonAy(db: SQLiteDatabase, buAyBaslangicGunu: string): Promise<string | null> {
  const r = await db.getFirstAsync<{ sonGun: string | null }>(
    'SELECT MAX(gun) AS sonGun FROM harcama WHERE taksit_id IS NOT NULL AND gun >= ?',
    buAyBaslangicGunu,
  );
  return r?.sonGun ? r.sonGun.slice(0, 7) : null;
}

export type SurenSeri = {
  taksitId: string;
  kategori: string;
  taksitNo: number;
  taksitToplam: number;
  tutarKurus: number;
  /** "2027-05" — serinin son taksidinin ay anahtarı */
  sonAy: string;
};

/** Bu ayda ödemesi düşen (hâlâ süren) taksit serileri — E-18 "Süren seriler". */
export async function surenSeriler(db: SQLiteDatabase, buAy: string): Promise<SurenSeri[]> {
  const satirlar = await db.getAllAsync<{
    taksit_id: string;
    kategori: string;
    taksit_no: number;
    taksit_toplam: number;
    tutar_kurus: number;
  }>(
    `SELECT taksit_id, kategori, taksit_no, taksit_toplam, tutar_kurus FROM harcama
     WHERE taksit_id IS NOT NULL AND substr(gun, 1, 7) = ? ORDER BY tutar_kurus DESC`,
    buAy,
  );
  if (satirlar.length === 0) return [];
  const idler = satirlar.map((s) => s.taksit_id);
  const yerTutucular = idler.map(() => '?').join(', ');
  const sonlar = await db.getAllAsync<{ taksit_id: string; sonGun: string }>(
    `SELECT taksit_id, MAX(gun) AS sonGun FROM harcama WHERE taksit_id IN (${yerTutucular}) GROUP BY taksit_id`,
    ...idler,
  );
  const sonEslesme = new Map(sonlar.map((s) => [s.taksit_id, s.sonGun.slice(0, 7)]));
  return satirlar.map((s) => ({
    taksitId: s.taksit_id,
    kategori: s.kategori,
    taksitNo: s.taksit_no,
    taksitToplam: s.taksit_toplam,
    tutarKurus: s.tutar_kurus,
    sonAy: sonEslesme.get(s.taksit_id) ?? buAy,
  }));
}

/** Geçen ay biten (bu ay artık görünmeyen) tek bir seri — "seri bitti" bilgi şeridi. */
export async function gecenAyBitenSeri(
  db: SQLiteDatabase,
  gecenAy: string,
): Promise<{ kategori: string; tutarKurus: number } | null> {
  const r = await db.getFirstAsync<{ kategori: string; tutar_kurus: number }>(
    `SELECT kategori, tutar_kurus FROM harcama
     WHERE taksit_id IS NOT NULL AND taksit_no = taksit_toplam AND substr(gun, 1, 7) = ?
     LIMIT 1`,
    gecenAy,
  );
  return r ? { kategori: r.kategori, tutarKurus: r.tutar_kurus } : null;
}
