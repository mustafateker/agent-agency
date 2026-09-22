import { StyleSheet, View } from 'react-native';

import { GradFill } from '@/components/GradFill';
import { t } from '@/content/metinler';
import { clay, color, gradient, radius, rhythm } from '@/theme/tokens';

/**
 * Bileşen envanteri `StepIndicator` — "Adım n/3" + 3 oluk. Metnin kendisi
 * ekran başlığında ayrı bir `Txt` olarak durur (prototip: `.t-micro` header
 * içinde, groove satırı SALT görsel); bu yüzden burada yalnız erişilebilir
 * `progressbar` + doldurulmuş oluklar var. Yüzde yazılmaz (K-040).
 */
export function StepIndicator({ adim, toplam = 3 }: { adim: number; toplam?: number }) {
  return (
    <View
      accessible
      accessibilityRole="progressbar"
      accessibilityLabel={t['a11y.kurulum_ilerlemesi']}
      accessibilityValue={{ min: 1, max: toplam, now: adim }}
      style={stil.satir}>
      {Array.from({ length: toplam }, (_, i) => (
        <View key={i} style={stil.oluk}>
          {i < adim ? <GradFill colors={gradient.action} /> : null}
        </View>
      ))}
    </View>
  );
}

const stil = StyleSheet.create({
  satir: { flexDirection: 'row', gap: rhythm.group },
  oluk: {
    flex: 1,
    height: 8,
    borderRadius: radius.pill,
    backgroundColor: color.well,
    boxShadow: clay.sunken,
    overflow: 'hidden',
  },
});
