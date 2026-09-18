import { StyleSheet, View } from 'react-native';

import { ClaySurface } from '@/components/ClaySurface';
import { Txt } from '@/components/Txt';
import { SIMGE } from '@/lib/para';
import { clay, color, radius, rhythm } from '@/theme/tokens';

/**
 * tokens.md §7.4/§7.11 — tutar kuyusu. Sistem klavyesi açılmaz; sayı
 * `ClayKeypad`'den gelir. Uzun tutar kuralı (tokens.md §7.11, K-042):
 * gösterim 7 karakteri AŞARSA (8+) `hero` (56pt) → `display` (32pt)
 * rolüne iner, `₺` de bir basamak iner (`display` → `amount`). Kuyu
 * yüksekliği sabit kalır. Prototip üreteci de aynı kurala göre düzeltildi.
 */
export function AmountWell({
  tutarGosterim,
  ustSol,
  ustSag,
  hata,
  cursorGoster = true,
}: {
  tutarGosterim: string;
  ustSol: string;
  ustSag: string;
  hata?: string;
  cursorGoster?: boolean;
}) {
  const uzun = tutarGosterim.length > 7;
  const sayiRolu = uzun ? 'display' : 'hero';
  const simgeRolu = uzun ? 'amount' : 'display';

  return (
    <View>
      <ClaySurface
        level="sunken"
        borderRadius={radius.tile}
        style={[stil.kuyu, hata ? { boxShadow: `${clay.sunken}, 0 0 0 2px ${color.danger}` } : null]}>
        <View style={stil.ustSatir}>
          <Txt role="label" tone={color.text2}>
            {ustSol}
          </Txt>
          <Txt role="caption">{ustSag}</Txt>
        </View>
        <View style={{ height: rhythm.group }} />
        <View style={stil.paraSatiri}>
          <Txt role={sayiRolu} numberOfLines={1}>
            {tutarGosterim}
          </Txt>
          {cursorGoster ? <View style={stil.imlec} /> : null}
          <View style={{ width: rhythm.group }} />
          <Txt role={simgeRolu} tone={color.text2}>
            {SIMGE}
          </Txt>
        </View>
      </ClaySurface>
      {hata ? (
        <>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption" tone={color.dangerInk}>
            {hata}
          </Txt>
        </>
      ) : null}
    </View>
  );
}

const stil = StyleSheet.create({
  kuyu: { padding: rhythm.pad },
  ustSatir: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  paraSatiri: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center' },
  imlec: { width: 3, height: 44, borderRadius: radius.pill, backgroundColor: color.primary, marginLeft: 2 },
});
