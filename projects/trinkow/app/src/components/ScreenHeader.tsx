import { StyleSheet, View } from 'react-native';

import { IconButton } from '@/components/IconButton';
import type { IconName } from '@/components/Icon';
import { Txt } from '@/components/Txt';
import { layout } from '@/theme/tokens';

/** §3.1 `.ekran-basi` — üst 8 / alt 16, yatay 16. */
export function ScreenHeader({
  ustSatir,
  baslik,
  actionIcon = 'limitler',
  actionLabel = 'Limitleri aç',
  onActionPress,
}: {
  ustSatir?: string;
  baslik: string;
  actionIcon?: IconName;
  actionLabel?: string;
  onActionPress?: () => void;
}) {
  return (
    <View style={stil.kutu}>
      <View>
        {ustSatir ? <Txt role="caption">{ustSatir}</Txt> : null}
        <Txt role="h1">{baslik}</Txt>
      </View>
      <IconButton icon={actionIcon} accessibilityLabel={actionLabel} onPress={onActionPress} />
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
});
