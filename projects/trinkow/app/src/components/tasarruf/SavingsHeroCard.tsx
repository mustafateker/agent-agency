import { StyleSheet, View } from 'react-native';

import { Chip } from '@/components/Chip';
import { ClaySurface } from '@/components/ClaySurface';
import { Icon } from '@/components/Icon';
import { IconButton } from '@/components/IconButton';
import { Button } from '@/components/Button';
import { LimitGauge } from '@/components/LimitGauge';
import { Txt } from '@/components/Txt';
import {
  a11yTasarrufButceCip,
  a11yTasarrufGostergeDisinda,
  t,
  tasarrufButceCip,
  tasarrufGostergeCumleBuAy,
  tasarrufGostergeCumleGecmisAy,
  tasarrufGostergeDisindaBuAy,
  tasarrufGostergeDisindaGecmisAy,
} from '@/content/metinler';
import { paraYaz } from '@/lib/para';
import { color, radius, rhythm } from '@/theme/tokens';

/** rev2-tasarruf-profil.md §3.2/§3.10 — ekranın beş gösterge durumu. */
export type HeroDurum =
  | { tur: 'default'; hesaplananTasarrufKurus: number; harcanabilirKurus: number; tamamlananGun: number }
  | { tur: 'overflow'; hesaplananTasarrufKurus: number; harcanabilirKurus: number }
  | { tur: 'empty' }
  | { tur: 'no-budget' };

/**
 * rev2-tasarruf-profil.md §3.2 — E-27 kahraman kart. Tek kahraman gösterge
 * (`LimitGauge mod="birikim"`); bütçe dışında ana yay/topuz ÇİZİLMEZ (aynı
 * bileşenin formülü, bkz. `LimitGauge.tsx`). Ay gezinmesi göstergenin iki
 * yanında (E-10 gün sayfalamasıyla aynı dil).
 */
export function SavingsHeroCard({
  durum,
  butceTutari,
  guncelAyMi,
  ayLokatifDeger,
  oncekiPasif,
  sonrakiPasif,
  onOnceki,
  onSonraki,
  onKipPress,
  onButcePress,
}: {
  durum: HeroDurum;
  /** `null` → "Bütçe yok" çipi. */
  butceTutari: string | null;
  guncelAyMi: boolean;
  ayLokatifDeger: string;
  oncekiPasif: boolean;
  sonrakiPasif: boolean;
  onOnceki: () => void;
  onSonraki: () => void;
  onKipPress: () => void;
  onButcePress: () => void;
}) {
  return (
    <ClaySurface level="raisedLg" borderRadius={radius.hero} background={color.primarySoft} style={stil.kart}>
      <View style={stil.aralik}>
        <Chip
          ad={t['tasarruf.kip.cip']}
          selected
          dotColor={color.primary}
          onPress={onKipPress}
          accessibilityLabel={t['a11y.tasarruf.kipCip']}
        />
        <Chip
          ad={tasarrufButceCip(butceTutari)}
          trailingIcon="chevron-right"
          onPress={onButcePress}
          accessibilityLabel={a11yTasarrufButceCip(butceTutari)}
        />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <View style={stil.pagerSatiri}>
        <IconButton
          icon="chevron-left"
          accessibilityLabel={t['a11y.tasarruf.oncekiAy']}
          onPress={onOnceki}
          disabled={oncekiPasif}
        />
        <Gosterge durum={durum} />
        <IconButton
          icon="chevron-right"
          accessibilityLabel={t['a11y.tasarruf.sonrakiAy']}
          onPress={onSonraki}
          disabled={sonrakiPasif}
        />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      {durum.tur === 'no-budget' ? (
        <NoBudgetAlt onButcePress={onButcePress} />
      ) : (
        <Txt role="body" style={stil.cumle}>
          {cumleMetni(durum, guncelAyMi, ayLokatifDeger)}
        </Txt>
      )}
    </ClaySurface>
  );
}

function Gosterge({ durum }: { durum: HeroDurum }) {
  if (durum.tur === 'empty') {
    return (
      <LimitGauge
        mod="birikim"
        bos
        harcananKurus={0}
        limitKurus={0}
        merkezTutarKurus={0}
        etiket={t['tasarruf.gosterge.etiket']}
        accessibilityLabel={t['a11y.tasarruf.gosterge']}
      />
    );
  }
  if (durum.tur === 'no-budget') {
    return (
      <LimitGauge
        mod="birikim"
        bos
        harcananKurus={0}
        limitKurus={0}
        etiket=""
        accessibilityLabel="Bütçe tanımlı değil"
        centerOverride={<Icon name="landmark" size={32} color={color.text2} />}
      />
    );
  }
  const asiriMi = durum.tur === 'overflow';
  return (
    <LimitGauge
      mod="birikim"
      harcananKurus={durum.hesaplananTasarrufKurus}
      limitKurus={durum.harcanabilirKurus}
      etiket={asiriMi ? t['tasarruf.gosterge.etiketDisinda'] : t['tasarruf.gosterge.etiket']}
      accessibilityLabel={asiriMi ? a11yTasarrufGostergeDisinda(paraYaz(Math.abs(durum.hesaplananTasarrufKurus))) : t['a11y.tasarruf.gosterge']}
    />
  );
}

function NoBudgetAlt({ onButcePress }: { onButcePress: () => void }) {
  return (
    <View style={stil.noBudget}>
      <Txt role="h2">{t['tasarruf.gelirYok.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" style={stil.cumle}>
        {t['tasarruf.gelirYok.alt']}
      </Txt>
      <View style={{ height: rhythm.blockInCard }} />
      <Button variant="primary" label={t['tasarruf.gelirYok.btn']} onPress={onButcePress} />
    </View>
  );
}

/** `no-budget` çağırılmaz — o dal `NoBudgetAlt`e düşer (bkz. `SavingsHeroCard`). */
function cumleMetni(durum: Exclude<HeroDurum, { tur: 'no-budget' }>, guncelAyMi: boolean, ayLokatifDeger: string): string {
  if (durum.tur === 'empty') return t['tasarruf.gosterge.ayYeni'];
  if (durum.tur === 'overflow') {
    const tutar = paraYaz(Math.abs(durum.hesaplananTasarrufKurus));
    return guncelAyMi ? tasarrufGostergeDisindaBuAy(tutar) : tasarrufGostergeDisindaGecmisAy(ayLokatifDeger, tutar);
  }
  return guncelAyMi
    ? tasarrufGostergeCumleBuAy(durum.tamamlananGun)
    : tasarrufGostergeCumleGecmisAy(ayLokatifDeger, durum.tamamlananGun);
}

const stil = StyleSheet.create({
  kart: { padding: rhythm.pad, alignItems: 'center', width: '100%' },
  aralik: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%' },
  pagerSatiri: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%' },
  cumle: { textAlign: 'center' },
  noBudget: { alignItems: 'center', width: '100%' },
});
