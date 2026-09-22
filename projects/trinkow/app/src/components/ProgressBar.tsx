import { StyleSheet, View } from 'react-native';

import { GradFill } from '@/components/GradFill';
import { Txt } from '@/components/Txt';
import { clay, color, gradient, radius, rhythm } from '@/theme/tokens';

/**
 * Bileşen envanteri `ProgressBar` (Katman 2, E-25) — RN inşa notu 9: 8 segment
 * ÇİZİLMEZ (390px'te 38px'lik parçalara bölünür, ilerleme okunmaz olur).
 * Tek oluk + dolgu (`grad.action`, metinsiz) + yanında `n/8`.
 */
export function ProgressBar({ mevcut, toplam, accessibilityLabel }: { mevcut: number; toplam: number; accessibilityLabel: string }) {
  const oran = toplam > 0 ? Math.min(1, mevcut / toplam) : 0;
  return (
    <View
      style={stil.satir}
      accessible
      accessibilityRole="progressbar"
      accessibilityLabel={accessibilityLabel}
      accessibilityValue={{ min: 1, max: toplam, now: mevcut }}>
      <View style={stil.oluk}>
        <View style={[stil.dolguKirp, { width: `${oran * 100}%` }]}>
          <GradFill colors={gradient.action} />
        </View>
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      <Txt role="micro" tone={color.text2}>
        {mevcut}/{toplam}
      </Txt>
    </View>
  );
}

const stil = StyleSheet.create({
  satir: { flexDirection: 'row', alignItems: 'center' },
  oluk: {
    flex: 1,
    height: 8,
    borderRadius: radius.pill,
    backgroundColor: color.well,
    boxShadow: clay.sunken,
    overflow: 'hidden',
  },
  dolguKirp: { height: 8, borderRadius: radius.pill, overflow: 'hidden' },
});
