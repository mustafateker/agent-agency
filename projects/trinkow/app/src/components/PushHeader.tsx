import { StyleSheet, View } from 'react-native';

import { IconButton } from '@/components/IconButton';
import type { IconName } from '@/components/Icon';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { layout, size } from '@/theme/tokens';

/**
 * Bileşen envanteri §4 `PushHeader` — itilen ekranlar (E-15 · E-17 · E-18).
 * `.ekran-basi` ile aynı ölçü (üst/alt 8/16): solda geri `IconButton`,
 * ortada `h1` tek satır, sağda isteğe bağlı eylem ya da 44pt denge kutusu.
 */
export function PushHeader({
  baslik,
  onGeri,
  sagIkon,
  sagEtiket,
  onSagPress,
}: {
  baslik: string;
  onGeri: () => void;
  sagIkon?: IconName;
  sagEtiket?: string;
  onSagPress?: () => void;
}) {
  return (
    <View style={stil.kutu}>
      <IconButton icon="chevron-left" accessibilityLabel={t['eylem.geri']} onPress={onGeri} />
      <View style={stil.orta}>
        <Txt role="h1" numberOfLines={1}>
          {baslik}
        </Txt>
      </View>
      {sagIkon && sagEtiket ? (
        <IconButton icon={sagIkon} accessibilityLabel={sagEtiket} onPress={onSagPress} />
      ) : (
        <View style={stil.denge} />
      )}
    </View>
  );
}

const stil = StyleSheet.create({
  kutu: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: layout.headerPadTop,
    paddingBottom: layout.headerPadBottom,
    paddingHorizontal: layout.screenPaddingX,
  },
  orta: { flex: 1, minWidth: 0, alignItems: 'center' },
  denge: { width: size.iconButton, height: size.iconButton },
});
