import { StyleSheet, View } from 'react-native';

import { Button } from '@/components/Button';
import { ClaySurface } from '@/components/ClaySurface';
import { Icon } from '@/components/Icon';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { clay, color, radius, rhythm } from '@/theme/tokens';

/**
 * Bileşen envanteri §5 `ErrorState`. 96pt çukur daire — boş durumdan
 * FARKLI illüstrasyon. Teknik hata kodu / depolama açıklaması yok.
 */
export function ErrorState({ onRetry }: { onRetry?: () => void }) {
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
      <View style={stil.disk}>
        <Icon name="refresh-cw" size={32} color={color.text2} />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <Txt role="h2">{t['hata.okuma.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" style={stil.metin}>
        {t['hata.okuma.govde']}
      </Txt>
      <View style={{ height: rhythm.blockInCard }} />
      <Button
        label={t['hata.okuma.eylem']}
        variant="primary"
        icon="refresh-cw"
        onPress={onRetry}
        auto
      />
    </ClaySurface>
  );
}

const stil = StyleSheet.create({
  kart: { padding: rhythm.pad, alignItems: 'center' },
  disk: {
    width: 96,
    height: 96,
    borderRadius: radius.pill,
    backgroundColor: color.groove,
    boxShadow: clay.sunken,
    alignItems: 'center',
    justifyContent: 'center',
  },
  metin: { textAlign: 'center' },
});
