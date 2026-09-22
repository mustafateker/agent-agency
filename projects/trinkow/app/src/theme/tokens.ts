import type { TextStyle } from 'react-native';

/**
 * Trinkow tasarım tokenları — tek kaynak.
 * Türetildiği yer: projects/trinkow/docs/brand/tokens.md v3.1 (Claymorphism).
 * Buradaki değerler bileşenlere KOPYALANMAZ; bileşen daima buradan okur.
 *
 * Faz 1: tek tema (açık). Karanlık mod tokenı üretilmez (tokens.md §11).
 */

/* ---------------------------------------------------------------- §1 RENK */

export const color = {
  // §1.1 zemin ve yüzey
  bg: '#E6EFFE',
  surface: '#FFFFFF',
  groove: '#F2F7FE',
  well: '#E6EFFE',
  line: '#DCE6F9',
  disabledBg: '#DCE6F9',
  scrim: 'rgba(28,57,142,0.38)',

  // §1.2 metin
  text: '#1C398E',
  text2: '#4961A5',
  text3: '#556AAA',
  onPrimary: '#FFFFFF',

  // §1.3 eylem ve durum
  primary: '#3B82F6',
  primaryDeep: '#2F68C5',
  primaryPress: '#295BAC',
  primaryText: '#2C62B8',
  primarySoft: '#E4EEFE',
  warning: '#D97706',
  warningDeep: '#B45309',
  warningInk: '#8A4B04',
  warningSoft: '#FAECDC',
  /** §1.3 — yalnız dört bağlam: taksit serisi silme · tüm veriyi silme · form hatası kenarlığı · silme toast göstergesi */
  danger: '#DC2626',
  dangerInk: '#C62222',
  dangerSoft: '#FAE1E1',
  success: '#16A34A',
  successInk: '#12823B',
  successSoft: '#DEF2E6',
} as const;

/**
 * §7.13 / §1.3 · K-059/4 — plan pay çubuğunun (E-26 `ShareBar`/`ShareRow`)
 * ÜÇ segment rengi. Mevcut hex değerlerin YENİDEN ADLANDIRILMASI — yeni
 * renk değeri değil. `success` yalnız bu grafik bağlamda kullanılır ve
 * ÜSTÜNDE METİN TAŞIMAZ (K-066 · pay adları çubuğun dışındaki `ShareRow`da).
 */
export const share = {
  zorunlu: color.primaryDeep,
  sosyal: color.primary,
  birikim: color.success,
} as const;

/** §7.13 `Slider` (E-25/E-26) — oluk/topuz/satır. Yeni ölçü ailesi açılmadı (12/32/44 mevcut, satır = §6 `a11y.minTarget`). */
export const slider = {
  track: 12,
  knob: 32,
  row: 44,
} as const;

/** §1.4 kategori aileleri — 6 aile. Kategoriyi ayıran şey ikon + ad. */
export const catColor = {
  mavi: { solid: '#306BCA', soft: '#E4EEFE' },
  lacivert: { solid: '#172F74', soft: '#DFE3EF' },
  yesil: { solid: '#12863D', soft: '#DEF2E6' },
  amber: { solid: '#B26205', soft: '#FAECDC' },
  kiremit: { solid: '#B41F1F', soft: '#FAE1E1' },
  duman: { solid: '#2E3A5C', soft: '#DEDFE5' },
} as const;

export type CatFamily = keyof typeof catColor;

/** §1.8 izinli gradyanlar — dört tane, artırılamaz. */
export const gradient = {
  /** Kahraman yay dolgusu (yay boyunca) */
  arc: ['#3B82F6', '#2F68C5'] as const,
  /** Taşma yayı — yalnız limit dışı */
  arcOver: ['#D97706', '#B45309'] as const,
  /** Birincil buton, FAB — dikey, koyu uçlu */
  action: ['#3B82F6', '#2F68C5'] as const,
  actionPressed: ['#2F68C5', '#295BAC'] as const,
  /** Kabarık yüzeyin üst parlaması — dikey, üst %45 */
  clayFace: ['rgba(255,255,255,0.90)', 'rgba(255,255,255,0)'] as const,
} as const;

/** §5.3 — grad.clay-face'in bittiği oran. Yüzeyin üst %45'i. */
export const CLAY_FACE_STOP = 0.45;

/**
 * `rgba(...)` tokenini renk + opaklık olarak ayırır.
 * SVG `stop-color` alfa taşımaz; saydamlık `stop-opacity` ile verilir —
 * rgba dizesi doğrudan verilirse alfa düşer ve gradyan OPAK çıkar
 * (kabarık yüzeylerin üst parlaması bütün kartı beyaza boyar).
 */
export function rgbaAyir(deger: string): { renk: string; opaklik: number } {
  const e = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/.exec(deger);
  if (!e) return { renk: deger, opaklik: 1 };
  return {
    renk: `rgb(${e[1]}, ${e[2]}, ${e[3]})`,
    opaklik: e[4] === undefined ? 1 : Number(e[4]),
  };
}

/* ----------------------------------------------------------- §2 TİPOGRAFİ */

/** §2.1 — dört dosya. Artırılamaz. Ağırlık dosya seçimiyle gelir. */
export const fontFamily = {
  /** Montserrat 400 */
  uiRegular: 'Montserrat_400Regular',
  /** Montserrat 600 */
  uiSemibold: 'Montserrat_600SemiBold',
  /** Montserrat 700 — tüm rakamlar (tek `₺` glifi taşıyan tabular font) */
  numBold: 'Montserrat_700Bold',
  /** Poppins 600 — yalnız h1/h2, rakam içeremez */
  display: 'Poppins_600SemiBold',
} as const;

/** Montserrat tabular rakam. `₺` ve tutarlar daima bununla dizilir (§2.3). */
export const TABULAR = ['tabular-nums'] as NonNullable<TextStyle['fontVariant']>;

/**
 * §2.2 — 10 tip rolü. Ara değer üretilemez.
 * İzinli punto: 12 · 13 · 16 · 17 · 19 · 26 · 32 · 56
 */
export const type = {
  hero: {
    fontFamily: fontFamily.numBold,
    fontSize: 56,
    lineHeight: 60,
    letterSpacing: -2,
    fontVariant: TABULAR,
  },
  display: {
    fontFamily: fontFamily.numBold,
    fontSize: 32,
    lineHeight: 38,
    letterSpacing: -1,
    fontVariant: TABULAR,
  },
  amount: {
    fontFamily: fontFamily.numBold,
    fontSize: 17,
    lineHeight: 24,
    letterSpacing: -0.2,
    fontVariant: TABULAR,
  },
  h1: {
    fontFamily: fontFamily.display,
    fontSize: 26,
    lineHeight: 32,
    letterSpacing: -0.6,
  },
  h2: {
    fontFamily: fontFamily.display,
    fontSize: 19,
    lineHeight: 25,
    letterSpacing: -0.3,
  },
  body: { fontFamily: fontFamily.uiRegular, fontSize: 16, lineHeight: 24, letterSpacing: 0 },
  bodyStrong: { fontFamily: fontFamily.uiSemibold, fontSize: 16, lineHeight: 24, letterSpacing: 0 },
  label: { fontFamily: fontFamily.uiSemibold, fontSize: 13, lineHeight: 18, letterSpacing: 0.2 },
  caption: { fontFamily: fontFamily.uiRegular, fontSize: 13, lineHeight: 18, letterSpacing: 0 },
  micro: { fontFamily: fontFamily.uiRegular, fontSize: 12, lineHeight: 16, letterSpacing: 0.2 },
} satisfies Record<string, TextStyle>;

/* ------------------------------------------------------------ §3 SPACING */

/** §3 — taban 4pt. Bu altı değerin dışında boşluk kullanılamaz. */
export const space = {
  1: 4,
  2: 8,
  3: 12,
  4: 16,
  5: 24,
  6: 32,
} as const;

/**
 * §3.1 dikey ritim seti — her değerin TEK bir işi vardır.
 * Kodda `space[n]` yerine bu adları kullan; hangi işi yaptığı okunsun.
 */
export const rhythm = {
  /** 4 — aynı nesnenin iki satırı */
  sameObject: space[1],
  /** 8 — başlık↔gövde · etiket↔girdi · aynı grubun tekrarlayan öğeleri */
  group: space[2],
  /** 12 — kartın İÇİNDE iki bağımsız blok */
  blockInCard: space[3],
  /** 16 — iç boşluk (padding), dikey ritim değil */
  pad: space[4],
  /** 24 — ekran düzeyinde iki bağımsız blok · içerik alt boşluğu */
  section: space[5],
} as const;

export const layout = {
  /** §3 — tüm ekranlarda sabit */
  screenPaddingX: space[4],
  /** §3.1 .ekran-basi → üst 8 / alt 16 */
  headerPadTop: space[2],
  headerPadBottom: space[4],
  /** §3.1 kaydırılan içeriğin sonu */
  scrollPadBottom: space[5],
  /** §7.7 yüzen sekme çubuğu yan boşluğu */
  tabBarInsetX: space[4],
  /** §7.7 çubuk alttan `insets.bottom + 8` */
  tabBarLift: space[2],
} as const;

/* ------------------------------------------------------------- §4 RADIUS */

/** §4 — izinli: 16 · 24 · 32 · 999 · 0 (+ odak halkası 20/28/36) */
export const radius = {
  hero: 32,
  card: 24,
  tile: 16,
  pill: 999,
  none: 0,
} as const;

/** §4 — odak halkası = eleman radius + 4 */
export const focusRing = {
  width: 2,
  color: color.primaryText,
  /** koyu zeminde */
  colorOnDark: '#FFFFFF',
  offset: 2,
} as const;

/* ---------------------------------------------- §5 CLAY ELEVATION (gölge) */

/**
 * §5.1 — `boxShadow` dizeleri tokens.md'den BİREBİR.
 * Yeniden yorumlanmaz, `elevation` (eski Android API) kullanılmaz (§5.2).
 * Inset gölge yalnız New Architecture'da çalışır — app.json'da açık.
 */
export const clay = {
  /** 4 katman — kart, liste satırı, kategori kutusu, çip */
  raised:
    '0 8px 16px -4px rgba(28,57,142,0.16), 0 2px 4px -1px rgba(28,57,142,0.10), inset 0 -5px 8px -4px rgba(28,57,142,0.14), inset 0 5px 8px -4px rgba(255,255,255,0.95)',
  /** 4 katman — kahraman kart, bottom sheet, yüzen sekme çubuğu, toast */
  raisedLg:
    '0 16px 32px -8px rgba(28,57,142,0.22), 0 4px 8px -2px rgba(28,57,142,0.12), inset 0 -8px 12px -6px rgba(28,57,142,0.16), inset 0 8px 12px -6px rgba(255,255,255,0.98)',
  /** 3 katman — HER basılı etkileşimli yüzey */
  pressed:
    '0 1px 2px 0 rgba(28,57,142,0.10), inset 0 3px 6px -2px rgba(28,57,142,0.20), inset 0 -2px 4px -2px rgba(255,255,255,0.60)',
  /** 2 katman — oluk, metin girişi kuyusu, segment track, ilerleme oluğu */
  sunken:
    'inset 0 3px 6px -2px rgba(28,57,142,0.18), inset 0 -2px 3px -2px rgba(255,255,255,0.80)',
  /** 4 katman — birincil buton, FAB. Gölge zeminin rengini alır. */
  action:
    '0 8px 16px -4px rgba(47,104,197,0.42), 0 2px 4px -1px rgba(47,104,197,0.28), inset 0 -4px 8px -3px rgba(28,57,142,0.34), inset 0 4px 8px -3px rgba(255,255,255,0.42)',
  /** 3 katman — birincil buton / FAB pressed */
  actionPressed:
    '0 2px 4px -2px rgba(47,104,197,0.30), inset 0 4px 8px -2px rgba(28,57,142,0.42), inset 0 -2px 4px -2px rgba(255,255,255,0.22)',
} as const;

/* ------------------------------------------------ §6 DOKUNMA / ERİŞİM */

export const a11y = {
  /** §6 — minimum dokunma hedefi */
  minTarget: 44,
} as const;

/* -------------------------------------------------- §7 BİLEŞEN ÖLÇÜLERİ */

export const size = {
  /** §7.1 buton yükseklikleri */
  buttonPrimary: 56,
  buttonSecondary: 52,
  buttonGhost: 44,
  buttonPadX: space[5],
  buttonGhostPadX: space[4],
  /** §7.1 ikon: buton içi 20, varsayılan 24, FAB 28 (§9) */
  iconSm: 20,
  icon: 24,
  iconFab: 28,
  /** §7.3 liste satırı */
  rowMinHeight: 68,
  rowPadY: space[3],
  rowPadX: space[4],
  /** §7.3 sol kategori kabı */
  catBox: 44,
  /** §7.4 metin girişi */
  input: 56,
  /** §7.6 çip */
  chipHeight: 40,
  chipPadX: space[4],
  chipMaxWidth: 240,
  chipNameMaxWidth: 120,
  /** §7.7 yüzen sekme çubuğu */
  tabBarHeight: 68,
  tabBarPadX: space[2],
  tabItemWidth: 64,
  tabItemHeight: 56,
  tabIconBox: 40,
  tabIconBoxHeight: 24,
  tabIconBoxHeightActive: 32,
  /** §7.7 FAB — bar üstünden 16 taşar, sağdan 8 */
  fab: 64,
  fabOverhang: space[4],
  fabRight: space[2],
  /** §7.7 alan yüksekliği = 68 + 16 */
  tabAreaHeight: 68 + space[4],
  /** ikon butonu (44) */
  iconButton: 44,
  iconButtonGlyph: 22,
  /** §7.5 kategori çubuğu */
  catBarHeight: 12,
  /** §7.12 `ClaySwitch` — track 56×32, iç boşluk 4, topuz 24 */
  switchTrackW: 56,
  switchTrackH: 32,
  switchTrackPad: 4,
  switchKnob: 24,
} as const;

/** §7.5 kahraman gösterge geometrisi — prototipteki ölçüler birebir. */
export const gauge = {
  /** dış kabarık disk çapı */
  diameter: 224,
  /** oluk merkez yarıçapı (78..94) */
  trackRadius: 86,
  /** oluk + dolgu kalınlığı */
  trackWidth: 16,
  /** çukurluk kenar yayları */
  edgeOuterRadius: 92.5,
  edgeInnerRadius: 79.5,
  edgeWidth: 2.5,
  edgeOuterColor: 'rgba(28,57,142,0.13)',
  edgeInnerColor: 'rgba(255,255,255,0.95)',
  /** dolgu parlaması */
  fillGlossWidth: 5,
  fillGlossColor: 'rgba(255,255,255,0.30)',
  /** yay açıklığı 270°, boşluk altta, başlangıç saat 7 */
  sweepDegrees: 270,
  startAngleDeg: 135,
  /** topuz (§7.5) */
  knobRadius: 13,
  knobRingWidth: 4,
  knobRingRadius: 11,
  knobShadowRadius: 13.5,
  knobShadowColor: 'rgba(28,57,142,0.18)',
  knobGlossRadius: 8,
  knobGlossWidth: 1.5,
  knobGlossColor: 'rgba(255,255,255,0.55)',
  /** taşma yayı — merkez yarıçapı 102, 8pt, saat 12'den saat yönünde */
  overRadius: 102,
  overWidth: 8,
  overGlossWidth: 3,
  overGlossColor: 'rgba(255,255,255,0.32)',
  /** iç alan genişliği — uzun tutar kuralının ölçüldüğü yer */
  innerWidth: 156,
  /** §7.5 — sayı 6+ karakterse rol bir basamak iner */
  heroDigitLimit: 6,
  /** §7.8 boş durum illüstrasyonu */
  emptyDiameter: 176,
  emptyTrackRadius: 70,
  emptyTrackWidth: 12,
  emptyEdgeOuterRadius: 75,
  emptyEdgeInnerRadius: 65,
} as const;

/* ------------------------------------------------------------ §8 HAREKET */

/** §8 — 150–250ms, ease-out. Reduce motion açıkken tüm süreler 0ms. */
export const motion = {
  press: 150,
  arc: 250,
  count: 250,
  sheet: 250,
} as const;

/** §9 — Lucide, çizgi kalınlığı 2.0 (FAB 2.5, prototipte böyle) */
export const icon = {
  strokeWidth: 2,
  strokeWidthFab: 2.5,
} as const;

/**
 * §7.13 v4 bileşenleri (E-10 sayfalama · E-21 seri · E-24 gün seçici).
 * Yeni ölçü ailesi AÇILMAZ — hepsi mevcut 8/24/44/96 değerlerinden.
 */
export const v4 = {
  /** `MilestoneRail` durağı — 44 dairesi (a11y.minTarget), 24×8 bağlantı yolu */
  durakDiameter: a11y.minTarget,
  durakTrackWidth: space[5],
  durakTrackHeight: space[2],
  /** `StreakDayGrid` / `MonthGrid` kutusu — mevcut `DayBox` (44), lejant karesi 24 */
  dayBox: a11y.minTarget,
  legendSwatch: space[5],
  /** Kutlama kartı (`MilestoneOverlay`) diski — mevcut hata dairesi ölçüsü */
  milestoneDisk: 96,
  /** `MonthGrid` bugün noktası */
  monthTodayDot: space[2],
  /** Hücreler arası boşluk (§3.3 negatif oluk telafisi) */
  gridGap: space[2],
} as const;
