import { StyleSheet, View } from 'react-native';

import { Txt } from '@/components/Txt';
import { clay, color, radius, rhythm, size } from '@/theme/tokens';

/**
 * Bileşen envanteri §3 `DayBox` (E-15) — `SpendRow`'un sol sütununda
 * kategori kabının YERİNE geçer: kategori sabitken değişen gündür.
 * 44×44, radius 16, zemin `well` + `clay.sunken`.
 */
export function DayBox({ gun, ayKisa }: { gun: number; ayKisa: string }) {
  return (
    <View style={stil.kutu}>
      <Txt role="label">{gun}</Txt>
      <View style={{ height: rhythm.sameObject }} />
      <Txt role="micro" tone={color.text2}>
        {ayKisa}
      </Txt>
    </View>
  );
}

const stil = StyleSheet.create({
  kutu: {
    width: size.catBox,
    height: size.catBox,
    borderRadius: radius.tile,
    backgroundColor: color.well,
    boxShadow: clay.sunken,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
