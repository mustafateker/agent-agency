import type { ReactNode } from 'react';
import { View, type StyleProp, type ViewProps, type ViewStyle } from 'react-native';

import { ClayGloss } from '@/components/ClayGloss';
import { clay, color, radius } from '@/theme/tokens';

/**
 * Clay yüzey seviyeleri — tokens.md §5.1.
 * Kabarık yüzeyler `grad.clay-face` parlamasını da taşır (§5.3).
 */
export type ClayLevel = 'raised' | 'raisedLg' | 'pressed' | 'sunken';

const zemin: Record<ClayLevel, string> = {
  raised: color.surface,
  raisedLg: color.surface,
  pressed: color.groove,
  sunken: color.well,
};

const parlakMi: Record<ClayLevel, boolean> = {
  raised: true,
  raisedLg: true,
  // basılı ve çukur yüzeyde üst parlama yoktur (prototip: background-image: none)
  pressed: false,
  sunken: false,
};

type Props = ViewProps & {
  level: ClayLevel;
  /** tokens.md §4 — eleman tipinden türer, serbest değer verilmez. */
  borderRadius?: number;
  /** Zemin tonu gerekiyorsa (ör. kahraman kart `primary-soft`). */
  background?: string;
  style?: StyleProp<ViewStyle>;
  children?: ReactNode;
};

export function ClaySurface({
  level,
  borderRadius = radius.card,
  background,
  style,
  children,
  ...rest
}: Props) {
  return (
    <View
      {...rest}
      style={[
        {
          backgroundColor: background ?? zemin[level],
          borderRadius,
          boxShadow: clay[level],
          // parlama dikdörtgeni köşelerden taşmasın
          overflow: 'hidden',
        },
        style,
      ]}>
      {parlakMi[level] ? <ClayGloss /> : null}
      {children}
    </View>
  );
}
