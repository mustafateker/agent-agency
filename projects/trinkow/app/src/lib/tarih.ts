/** Tarih biçimleri — prototipteki "10 Eylül Perşembe" ve "08.20" düzeni. */

const AYLAR = [
  'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
  'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık',
];

export const GUNLER = ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'];

/** "Pt · Sa · Ça …" — E-24 ay ızgarası hafta başlığı (Pazartesi başlangıçlı). */
export const HAFTA_GUN_MIKRO = ['Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct', 'Pa'];

const AYLAR_KISA = [
  'Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara',
];

/** "Eyl" — `DayBox` ay kısaltması (E-15). */
export function ayKisaAdi(d: Date): string {
  return AYLAR_KISA[d.getMonth()];
}

/** "Pzt" · "Sal" · … — E-16 sütun grafiği gün etiketleri (Pazartesi başlangıçlı). */
export const HAFTA_GUN_KISA = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];

/** "10 Eylül Perşembe" */
export function uzunTarih(d: Date): string {
  return `${d.getDate()} ${AYLAR[d.getMonth()]} ${GUNLER[d.getDay()]}`;
}

/** Yerel gün anahtarı: "2026-09-12" (SQLite'ta gün bazlı sorgu için) */
export function gunAnahtari(d: Date): string {
  const ay = String(d.getMonth() + 1).padStart(2, '0');
  const gun = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${ay}-${gun}`;
}

/** Yerel ay anahtarı: "2026-09" */
export function ayAnahtari(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
}

/** "08.20" — prototipteki saat düzeni (iki nokta değil nokta) */
export function saatYaz(isoDamga: string): string {
  const d = new Date(isoDamga);
  return `${String(d.getHours()).padStart(2, '0')}.${String(d.getMinutes()).padStart(2, '0')}`;
}

/** Bugünden `fark` gün ötesi/berisi */
export function gunEkle(d: Date, fark: number): Date {
  const y = new Date(d);
  y.setDate(y.getDate() + fark);
  return y;
}

/** `ay` ay ötesi/berisi — gün-sabiti korunur (E-14 ay değiştirici, taksit serisi). */
export function ayEkle(d: Date, ay: number): Date {
  const y = new Date(d);
  const gun = y.getDate();
  y.setDate(1);
  y.setMonth(y.getMonth() + ay);
  // Ay taşması telafisi: 31 Ocak + 1 ay → 28/29 Şubat (31 değil).
  const ayinSonGunu = new Date(y.getFullYear(), y.getMonth() + 1, 0).getDate();
  y.setDate(Math.min(gun, ayinSonGunu));
  return y;
}

/** "YYYY-MM-DD" gün anahtarını yerel `Date`'e çevirir (öğlen saatine sabitler — TZ kaymasını önler). */
export function tarihtenGun(gunAnahtariDeger: string): Date {
  const [yil, ay, gun] = gunAnahtariDeger.split('-').map(Number);
  return new Date(yil, ay - 1, gun, 12, 0, 0);
}

/** "Eylül 2026" — ay değiştirici başlığı (E-14). */
export function ayBasligi(ayAnahtariDeger: string): string {
  const [yil, ay] = ayAnahtariDeger.split('-').map(Number);
  return `${AYLAR[ay - 1]} ${yil}`;
}

/** "Eylül" — yıl olmadan yalnız ay adı (E-18 ay yükü çubuğu etiketi). */
export function ayAdiTek(ayAnahtariDeger: string): string {
  const ay = Number(ayAnahtariDeger.split('-')[1]);
  return AYLAR[ay - 1];
}

/** "Bugün" · "Dün" · "8 Eylül Salı" — gün grubu başlığı (E-14). */
export function gunBasligi(gunAnahtariDeger: string, bugun: Date): string {
  const bugunAnahtari = gunAnahtari(bugun);
  const dunAnahtari = gunAnahtari(gunEkle(bugun, -1));
  if (gunAnahtariDeger === bugunAnahtari) return 'Bugün';
  if (gunAnahtariDeger === dunAnahtari) return 'Dün';
  return uzunTarih(tarihtenGun(gunAnahtariDeger));
}

/** "10 Eylül" — kısa tarih (E-11 tarih çipi, E-12 eklenme satırı). */
export function kisaTarih(d: Date): string {
  return `${d.getDate()} ${AYLAR[d.getMonth()]}`;
}

/** Haftanın Pazartesi'si (E-16 hafta değiştirici). Yerel gün, saat sıfırlanmaz. */
export function haftaBaslangici(d: Date): Date {
  const gun = (d.getDay() + 6) % 7; // Pazartesi=0 … Pazar=6
  return gunEkle(d, -gun);
}

/** "31 Ağustos – 6 Eylül" — `ozet.hafta_araligi` (E-16). */
export function haftaAraligi(baslangic: Date, bitis: Date): string {
  return `${kisaTarih(baslangic)} – ${kisaTarih(bitis)}`;
}

/** "10 Eylül · 21.30 eklendi" (E-12 alt bilgi). */
export function eklenmeEtiketi(isoDamga: string): string {
  const d = new Date(isoDamga);
  return `${kisaTarih(d)} · ${saatYaz(isoDamga)} eklendi`;
}

/* ------------------------------------------------------- v4 · E-10 sayfalama */

/**
 * E-10 gün başlığı (K-049/metinler.md §23.1). `gunFarki` 0=bugün, -1=dün,
 * daha eskisi tarihli başlığa döner: h1 "17/09 Perşembe", üst satır "N gün önce".
 * Bugün/dün sayfasında üst satır tam tarihtir (`uzunTarih`), h1 "Bugün"/"Dün".
 */
export function gunlukBaslik(gunFarki: number, tarih: Date): { h1: string; ustSatir: string } {
  if (gunFarki === 0) return { h1: 'Bugün', ustSatir: uzunTarih(tarih) };
  if (gunFarki === -1) return { h1: 'Dün', ustSatir: uzunTarih(tarih) };
  const gg = String(tarih.getDate()).padStart(2, '0');
  const ay = String(tarih.getMonth() + 1).padStart(2, '0');
  return { h1: `${gg}/${ay} ${GUNLER[tarih.getDay()]}`, ustSatir: `${Math.abs(gunFarki)} gün önce` };
}

/** İki günün arasındaki gün farkı (saat/TZ'den bağımsız, öğlene sabitlenmiş). */
export function gunFarkiHesapla(hedef: Date, bugun: Date): number {
  const h = new Date(hedef.getFullYear(), hedef.getMonth(), hedef.getDate(), 12, 0, 0);
  const b = new Date(bugun.getFullYear(), bugun.getMonth(), bugun.getDate(), 12, 0, 0);
  return Math.round((h.getTime() - b.getTime()) / 86_400_000);
}

/* ---------------------------------------------------- v4 · E-24 ay ızgarası */

/** Ayın gün sayısı — "2026-09" → 30. */
export function ayGunSayisi(ayAnahtariDeger: string): number {
  const [yil, ay] = ayAnahtariDeger.split('-').map(Number);
  return new Date(yil, ay, 0).getDate();
}

/** Ayın 1'inin haftadaki yeri — Pazartesi=0 … Pazar=6 (ay ızgarası baş boşluğu). */
export function ayIlkGununHaftaIndeksi(ayAnahtariDeger: string): number {
  const [yil, ay] = ayAnahtariDeger.split('-').map(Number);
  return (new Date(yil, ay - 1, 1).getDay() + 6) % 7;
}

/** `ay` ay ötesi/berisi ay anahtarı — "2026-09" + 1 → "2026-10" (E-24 ay değiştirici). */
export function ayAnahtariFarkli(ayAnahtariDeger: string, fark: number): string {
  const [yil, ay] = ayAnahtariDeger.split('-').map(Number);
  return ayAnahtari(ayEkle(new Date(yil, ay - 1, 1), fark));
}
