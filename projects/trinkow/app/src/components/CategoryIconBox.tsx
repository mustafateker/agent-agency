import { StyleSheet, View } from 'react-native';

import { Icon } from '@/components/Icon';
import { aileRenkleri, type Kategori } from '@/lib/kategoriler';
import { clay, radius, size } from '@/theme/tokens';

/** §7.3 — 44×44, radius 16, zemin `cat.*.soft`, `clay.sunken`, 20pt ikon. */
export function CategoryIconBox({ kategori }: { kategori: Kategori }) {
  const renk = aileRenkleri(kategori.aile);
  return (
    <View style={[stil.kutu, { backgroundColor: renk.soft }]}>
      <Icon name={kategori.ikon} size={size.iconSm} color={renk.solid} />
    </View>
  );
}

const stil = StyleSheet.create({
  kutu: {
    width: size.catBox,
    height: size.catBox,
    borderRadius: radius.tile,
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: clay.sunken,
  },
});
