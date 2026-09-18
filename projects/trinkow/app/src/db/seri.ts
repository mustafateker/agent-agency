import type { SQLiteDatabase } from 'expo-sqlite';

import { ayarOku, gunAraligiToplamlari, ilkKayitGunu } from '@/db/harcama';
import { ayBasligi, ayAnahtari, gunAnahtari, gunEkle, tarihtenGun } from '@/lib/tarih';

/**
 * K-048 — seri (streak) hesabı. Kaynak: tokens.md §14.5 + DECISIONS K-048.
 *
 * BİLİNÇLİ BASİTLEŞTİRME (rapora işlendi): günlük limit geçmişte
 * değiştiyse şema bunu saklamıyor — geçmiş günler DAİMA güncel günlük
 * limitle değerlendirilir. Prototipin "O gün limiti 250 ₺" gibi farklı
 * tarihsel değer gösteren kareleri bu yüzden MVP'de tek bir güncel
 * limitle çizilir; limit geçmişi Faz 1 kapsamı dışında.
 */

/** K-048 — milestone dizisi. Artırılamaz/uydurulmaz (bağlayıcı liste). */
export const MILESTONES = [3, 7, 14, 30, 60, 100, 180, 365] as const;

export async function gunHarcamasizIsaretle(db: SQLiteDatabase, gun: string): Promise<void> {
  await db.runAsync(
    'INSERT INTO gun_durumu (gun, harcamasiz) VALUES (?, 1) ON CONFLICT(gun) DO UPDATE SET harcamasiz = 1',
    gun,
  );
}

export async function gunHarcamasizMi(db: SQLiteDatabase, gun: string): Promise<boolean> {
  const r = await db.getFirstAsync<{ harcamasiz: number }>(
    'SELECT harcamasiz FROM gun_durumu WHERE gun = ?',
    gun,
  );
  return r?.harcamasiz === 1;
}

/** Aralıktaki harcamasız-işaretli günler — toplu okuma (bkz. `gunAraligiToplamlari`). */
async function harcamasizGunler(
  db: SQLiteDatabase,
  baslangicGun: string,
  bitisGun: string,
): Promise<Set<string>> {
  const satirlar = await db.getAllAsync<{ gun: string }>(
    'SELECT gun FROM gun_durumu WHERE harcamasiz = 1 AND gun BETWEEN ? AND ?',
    baslangicGun,
    bitisGun,
  );
  return new Set(satirlar.map((s) => s.gun));
}

/**
 * K-049 sol sınırı: kayıt varsa ilk kaydın günü, yoksa kurulum günü — ikisinin
 * DE ERKEN olanı (örnek veri bugünden "N gün önce" tarihlerle üretildiği için
 * ilk kayıt kurulum gününden önce olabilir; gerçek kullanıcıda ikisi eşittir).
 */
export async function ilkSinirGunu(db: SQLiteDatabase): Promise<string> {
  const kurulum = (await ayarOku(db, 'kurulum_gunu')) ?? gunAnahtari(new Date());
  const ilkKayit = await ilkKayitGunu(db);
  if (!ilkKayit) return kurulum;
  return ilkKayit < kurulum ? ilkKayit : kurulum;
}

/**
 * Bir günün veriye dayalı durumu. "pasif" (dokunulamaz — ilk kayıt öncesi/
 * gelecek) BUNUN parçası değildir; ayrı bir alan (`GunSeciciGunu.pasif`),
 * çünkü bir gün AYNI ANDA hem "bos" hem "pasif" olabilir (K-040 — iki dil
 * aynı elemanda birleşmez, tek bir "durum" alanına sıkıştırılmaz).
 */
export type GunSeriDurumu = 'altinda' | 'disinda' | 'bos';

/** Tek bir günün ızgara/seri durumu — E-21/E-24 ortak sınıflandırma. */
export function gunSeriDurumu(
  harcananKurus: number,
  kayitAdedi: number,
  limitKurus: number | null,
): GunSeriDurumu {
  if (kayitAdedi === 0) return 'bos';
  if (limitKurus !== null && harcananKurus > limitKurus) return 'disinda';
  return 'altinda';
}

/** Bir günün seriye sayılıp sayılmadığı (K-048 hile kapısı). `limitKurus` yoksa `null`. */
function gunSeriyeSayilirMi(
  harcananKurus: number,
  kayitAdedi: number,
  harcamasizIsaretli: boolean,
  limitKurus: number,
): boolean {
  const kayitliYaDaIsaretli = kayitAdedi > 0 || harcamasizIsaretli;
  return kayitliYaDaIsaretli && harcananKurus <= limitKurus;
}

export type SeriDurumu = {
  /** Bugün dahil, geriye doğru kesintisiz seriye sayılan gün sayısı. */
  mevcutSeri: number;
  enUzunSeri: number;
  /** "Temmuz 2026" — en uzun serinin bittiği ay. Hiç yoksa `null`. */
  enUzunSeriEtiketi: string | null;
  /** Limitsiz mod — seri işlemez (K-048). */
  kapali: boolean;
  /** `mevcutSeri === 0` ama daha önce bir seri vardıysa (suçlayıcı olmayan dil). */
  kirildiMi: boolean;
  sonrakiDurak: number | null;
  oncekiDurak: number;
  /** `sonrakiDurak - mevcutSeri` — yalnız `mevcutSeri > 0`. */
  kalanGun: number | null;
  /** Önceki↔sonraki durak arasındaki ilerleme oranı, 0..1. */
  aralikYuzde: number;
  /** Bugün YENİ geçilen ve daha önce hiç gösterilmemiş milestone — kutlama tetiği. */
  kutlanacakMilestone: number | null;
};

/** Tek bir günün seri/UI durumu — E-10 geçmiş sayfa şeridi için. */
export type GunSeriBilgisi = {
  harcananKurus: number;
  kayitAdedi: number;
  harcamasizIsaretli: boolean;
  /** `limitKurus` tanımsızsa `null` (seri hiç değerlendirilmez). */
  seriyeSayildiMi: boolean | null;
};

export async function gunSeriBilgisi(
  db: SQLiteDatabase,
  gun: string,
  limitKurus: number | null,
): Promise<GunSeriBilgisi> {
  const [toplamlar, harcamasiz] = await Promise.all([
    gunAraligiToplamlari(db, gun, gun),
    gunHarcamasizMi(db, gun),
  ]);
  const g = toplamlar.get(gun);
  const harcananKurus = g?.toplamKurus ?? 0;
  const kayitAdedi = g?.kayitAdedi ?? 0;
  return {
    harcananKurus,
    kayitAdedi,
    harcamasizIsaretli: harcamasiz,
    seriyeSayildiMi:
      limitKurus === null
        ? null
        : gunSeriyeSayilirMi(harcananKurus, kayitAdedi, harcamasiz, limitKurus),
  };
}

function sonrakiDurak(n: number): number | null {
  return MILESTONES.find((m) => m > n) ?? null;
}

function oncekiDurak(n: number): number {
  let onceki = 0;
  for (const m of MILESTONES) {
    if (m <= n) onceki = m;
    else break;
  }
  return onceki;
}

/**
 * Seri durumunu baştan hesaplar (K-048/§14.5). `bugun` test edilebilirlik
 * için parametredir; üretimde `new Date()` verilir.
 */
export async function seriDurumuHesapla(
  db: SQLiteDatabase,
  bugun: Date,
  limitKurus: number | null,
): Promise<SeriDurumu> {
  const bugunGun = gunAnahtari(bugun);
  const gosterilenDonum = Number((await ayarOku(db, 'seri_en_yuksek_gosterilen_donum')) ?? '0');

  if (limitKurus === null) {
    const persistedEnUzun = Number((await ayarOku(db, 'seri_en_uzun_gun')) ?? '0');
    const etiketGun = await ayarOku(db, 'seri_en_uzun_bitis_gun');
    return {
      mevcutSeri: 0,
      enUzunSeri: persistedEnUzun,
      enUzunSeriEtiketi: etiketGun ? ayBasligi(ayAnahtari(tarihtenGun(etiketGun))) : null,
      kapali: true,
      kirildiMi: false,
      sonrakiDurak: null,
      oncekiDurak: 0,
      kalanGun: null,
      aralikYuzde: 0,
      kutlanacakMilestone: null,
    };
  }

  const ilkGun = await ilkSinirGunu(db);
  const [toplamlar, harcamasizSet] = await Promise.all([
    gunAraligiToplamlari(db, ilkGun, bugunGun),
    harcamasizGunler(db, ilkGun, bugunGun),
  ]);

  // Gün gün nitelik dizisi (ilk gün → bugün).
  const gunler: string[] = [];
  for (let g = ilkGun; g <= bugunGun; ) {
    gunler.push(g);
    if (g === bugunGun) break;
    g = gunAnahtari(gunEkle(tarihtenGun(g), 1));
  }
  const nitelikler = gunler.map((g) => {
    const t = toplamlar.get(g);
    return gunSeriyeSayilirMi(
      t?.toplamKurus ?? 0,
      t?.kayitAdedi ?? 0,
      harcamasizSet.has(g),
      limitKurus,
    );
  });

  // Mevcut seri: bugünden geriye kesintisiz "true" sayısı.
  let mevcutSeri = 0;
  for (let i = nitelikler.length - 1; i >= 0; i -= 1) {
    if (!nitelikler[i]) break;
    mevcutSeri += 1;
  }

  // En uzun seri: tüm zamanların en uzun kesintisiz koşusu + bittiği gün.
  let calisanKosu = 0;
  let enUzunKosu = 0;
  let enUzunBitisIndeksi = -1;
  for (let i = 0; i < nitelikler.length; i += 1) {
    if (nitelikler[i]) {
      calisanKosu += 1;
      if (calisanKosu > enUzunKosu) {
        enUzunKosu = calisanKosu;
        enUzunBitisIndeksi = i;
      }
    } else {
      calisanKosu = 0;
    }
  }

  const persistedEnUzun = Number((await ayarOku(db, 'seri_en_uzun_gun')) ?? '0');
  const persistedEtiketGun = await ayarOku(db, 'seri_en_uzun_bitis_gun');

  let enUzunSeri = persistedEnUzun;
  let enUzunBitisGun = persistedEtiketGun;
  if (enUzunKosu > persistedEnUzun) {
    enUzunSeri = enUzunKosu;
    enUzunBitisGun = gunler[enUzunBitisIndeksi];
    await db.runAsync(
      "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('seri_en_uzun_gun', ?)",
      String(enUzunSeri),
    );
    await db.runAsync(
      "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('seri_en_uzun_bitis_gun', ?)",
      enUzunBitisGun,
    );
  }

  const kirildiMi = mevcutSeri === 0 && enUzunSeri > 0;
  const sonraki = sonrakiDurak(mevcutSeri);
  const onceki = oncekiDurak(mevcutSeri);
  const aralikYuzde = sonraki ? (mevcutSeri - onceki) / (sonraki - onceki) : 1;

  const kutlanacakMilestone =
    (MILESTONES as readonly number[]).includes(mevcutSeri) && mevcutSeri > gosterilenDonum
      ? mevcutSeri
      : null;

  return {
    mevcutSeri,
    enUzunSeri,
    enUzunSeriEtiketi: enUzunBitisGun ? ayBasligi(ayAnahtari(tarihtenGun(enUzunBitisGun))) : null,
    kapali: false,
    kirildiMi,
    sonrakiDurak: sonraki,
    oncekiDurak: onceki,
    kalanGun: mevcutSeri > 0 && sonraki ? sonraki - mevcutSeri : null,
    aralikYuzde,
    kutlanacakMilestone,
  };
}

/** Kutlama gösterildikten sonra kalıcı işaretle — uygulama yeniden açılınca tekrar oynamaz. */
export async function milestoneGosterildiIsaretle(db: SQLiteDatabase, milestone: number): Promise<void> {
  const mevcut = Number((await ayarOku(db, 'seri_en_yuksek_gosterilen_donum')) ?? '0');
  if (milestone <= mevcut) return;
  await db.runAsync(
    "INSERT OR REPLACE INTO ayar (anahtar, deger) VALUES ('seri_en_yuksek_gosterilen_donum', ?)",
    String(milestone),
  );
}
