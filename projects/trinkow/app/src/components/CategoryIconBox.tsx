import { StyleSheet, View } from 'react-native';

import { Icon } from '@/components/Icon';
import { aileRenkleri, type Kategori } from '@/lib/kategoriler';
import { clay, color, radius, size } from '@/theme/tokens';

/** §7.3 — 44×44, radius 16, zemin `cat.*.soft`, `clay.sunken`, 20pt ikon. */
export function CategoryIconBox({ kategori }: { kategori: Kategori }) {
  const renk = aileRenkleri(kategori.aile);
  return (
    <View style={[stil.kutu, { backgroundColor: renk.soft }]}>
      <Icon name={kategori.ikon} size={size.iconSm} color={renk.solid} />
    </View>
  );
}

/**
 * F-18 `kat-kab.notr` (delta-v4.md tokens eklentileri) — "Kendi kalemini
 * ekle" satırı bir kategori DEĞİLDİR; kategori renkleri yalnız kategori
 * bilgisi taşır (tokens §1.4). Kap `primary-soft`, çizgi `primary-text`.
 */
export function NeutralIconBox() {
  return (
    <View style={[stil.kutu, { backgroundColor: color.primarySoft }]}>
      <Icon name="plus" size={size.iconSm} color={color.primaryText} />
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
