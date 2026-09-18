import { StyleSheet, View } from 'react-native';

import { CategoryIconBox } from '@/components/CategoryIconBox';
import { ClaySurface } from '@/components/ClaySurface';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { kategori } from '@/lib/kategoriler';
import { color, radius, rhythm, size } from '@/theme/tokens';

/**
 * Bileşen envanteri §3 `SeriesRow` (E-18) — kategori kabı ·
 * "{kategori} · {mevcut}/{toplam}" · bitiş tarihi · sağda aylık tutar +
 * "her ay". `last` durumunda alt satır "Son taksit bu ay" (`warning-ink`).
 */
export function SeriesRow({
  kategoriKodu,
  ustSatir,
  altSatir,
  tutar,
  last = false,
}: {
  kategoriKodu: string;
  ustSatir: string;
  altSatir: string;
  tutar: string;
  last?: boolean;
}) {
  const kat = kategori(kategoriKodu);
  return (
    <ClaySurface level="raised" borderRadius={radius.tile} style={stil.satir}>
      <CategoryIconBox kategori={kat} />
      <View style={{ width: rhythm.blockInCard }} />
      <View style={stil.orta}>
        <Txt role="body" numberOfLines={1}>
          {ustSatir}
        </Txt>
        <Txt role="caption" tone={last ? color.warningInk : color.text2} numberOfLines={1}>
          {altSatir}
        </Txt>
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      <View style={stil.sag}>
        <Txt role="amount">{tutar}</Txt>
        <Txt role="caption" tone={color.text2}>
          {t['taksit.her_ay']}
        </Txt>
      </View>
    </ClaySurface>
  );
}

const stil = StyleSheet.create({
  satir: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: size.rowMinHeight,
    paddingVertical: size.rowPadY,
    paddingHorizontal: size.rowPadX,
  },
  orta: { flex: 1, minWidth: 0 },
  sag: { alignItems: 'flex-end', flexShrink: 0 },
});
