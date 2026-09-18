import { StyleSheet, View } from 'react-native';

import { ClayPressable } from '@/components/ClayPressable';
import { Txt } from '@/components/Txt';
import { clay, color, radius, rhythm, size } from '@/theme/tokens';

/**
 * §7.6 — çip. BAĞLAYICI kurallar:
 *  · Tek satır, sarmaz (`numberOfLines={1}`), maks. genişlik 240, `flexShrink: 0`.
 *  · Ad bölümü maks. 120, `ellipsizeMode="tail"`.
 *  · Tutar bölümü `flexShrink: 0` ile HİÇ kırpılmaz — `₺` asla kırpılmaz.
 *  · `accessibilityLabel` DAİMA tam adı taşır.
 *  · Seçili durum çukurlukla anlaşılır; onay ikonu yok.
 */
type Props = {
  /** Kırpılabilen bölüm */
  ad: string;
  /** Kırpılmayan bölüm — `₺` burada durur */
  tutar?: string;
  selected?: boolean;
  /** Seçili çipin solundaki 8pt nokta rengi */
  dotColor?: string;
  onPress?: () => void;
  /** Tam ad + tutar; verilmezse ad/tutar'dan kurulur */
  accessibilityLabel?: string;
};

export function Chip({ ad, tutar, selected = false, dotColor, onPress, accessibilityLabel }: Props) {
  const etiket = accessibilityLabel ?? (tutar ? `${ad}, ${tutar}` : ad);
  return (
    <ClayPressable
      onPress={onPress}
      selected={selected}
      accessibilityLabel={etiket}
      borderRadius={radius.pill}
      background={selected ? color.primarySoft : color.surface}
      pressedBackground={color.well}
      shadow={selected ? clay.sunken : clay.raised}
      gloss={!selected}
      style={stil.cip}>
      {selected && dotColor ? (
        <>
          <View style={[stil.nokta, { backgroundColor: dotColor }]} />
          <View style={{ width: rhythm.group }} />
        </>
      ) : null}
      <Txt
        role="label"
        tone={selected ? color.text : color.text2}
        numberOfLines={1}
        ellipsizeMode="tail"
        style={stil.ad}>
        {ad}
      </Txt>
      {tutar ? (
        <>
          <View style={{ width: rhythm.group }} />
          <Txt role="label" tone={selected ? color.text : color.text2} numberOfLines={1} style={stil.tutar}>
            {tutar}
          </Txt>
        </>
      ) : null}
    </ClayPressable>
  );
}

const stil = StyleSheet.create({
  cip: {
    flexDirection: 'row',
    alignItems: 'center',
    height: size.chipHeight,
    maxWidth: size.chipMaxWidth,
    paddingHorizontal: size.chipPadX,
    // yatay şeritte asla daralmaz
    flexShrink: 0,
    flexGrow: 0,
  },
  ad: { maxWidth: size.chipNameMaxWidth, flexShrink: 1 },
  // `₺` kırpılamaz
  tutar: { flexShrink: 0 },
  nokta: { width: 8, height: 8, borderRadius: radius.pill },
});
