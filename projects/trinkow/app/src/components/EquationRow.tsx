import { StyleSheet, View } from 'react-native';

import { ClaySurface } from '@/components/ClaySurface';
import { Txt } from '@/components/Txt';
import { color, radius, rhythm } from '@/theme/tokens';

export type EquationItem = { value: string; label: string };

/**
 * Bileşen envanteri `EquationRow` (E-26 için yazıldı, K-059/5 günlük limit
 * önerisi sheet'inde de kullanılıyor — RN inşa notu 8: tek hesap, tek
 * görsel bileşen). Üç çukur kutu + `÷` `=` + kabarık sonuç kutusu.
 */
export function EquationRow({
  items,
}: {
  items: readonly [EquationItem, EquationItem, EquationItem];
}) {
  return (
    <View style={stil.satir}>
      <Kutu item={items[0]} />
      <Islec sembol="÷" />
      <Kutu item={items[1]} />
      <Islec sembol="=" />
      <Kutu item={items[2]} sonuc />
    </View>
  );
}

function Kutu({ item, sonuc = false }: { item: EquationItem; sonuc?: boolean }) {
  return (
    <ClaySurface
      level={sonuc ? 'raised' : 'sunken'}
      borderRadius={radius.tile}
      background={sonuc ? color.primarySoft : undefined}
      style={stil.kutu}>
      <Txt role="amount" numberOfLines={1}>
        {item.value}
      </Txt>
      <View style={{ height: rhythm.sameObject }} />
      <Txt role="micro" tone={color.text2} numberOfLines={1}>
        {item.label}
      </Txt>
    </ClaySurface>
  );
}

function Islec({ sembol }: { sembol: string }) {
  return (
    <View style={stil.islec}>
      <Txt role="body" tone={color.text2}>
        {sembol}
      </Txt>
    </View>
  );
}

const stil = StyleSheet.create({
  satir: { flexDirection: 'row', alignItems: 'stretch' },
  kutu: {
    flex: 1,
    minWidth: 0,
    padding: rhythm.group,
    alignItems: 'center',
    justifyContent: 'center',
  },
  islec: { width: 16, alignItems: 'center', justifyContent: 'center' },
});
