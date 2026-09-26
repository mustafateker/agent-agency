import { router } from 'expo-router';
import { Fragment } from 'react';
import { StyleSheet, View } from 'react-native';

import { Accordion } from '@/components/Accordion';
import { Chip } from '@/components/Chip';
import { ClaySurface } from '@/components/ClaySurface';
import { IconButton } from '@/components/IconButton';
import { LimitGauge } from '@/components/LimitGauge';
import { Skeleton } from '@/components/Skeleton';
import { Txt } from '@/components/Txt';
import { a11yBolumYukleniyor, t } from '@/content/metinler';
import { color, radius, rhythm } from '@/theme/tokens';

const BOLUM_BASLIKLARI = [
  'tasarruf.bolum.butce',
  'tasarruf.bolum.birikim',
  'tasarruf.bolum.kategori',
  'tasarruf.bolum.rutin',
] as const;

/**
 * rev2-tasarruf-profil.md §3.10/§3.12.5 (loading) — "başlıklar gerçek,
 * özetlerin yeri iskelet; A'nın içeriği iskelet". Gerçek `Accordion`
 * bileşeni kullanılır (aynı ölçüler, tek kaynak): A açık + iskelet içerik,
 * B/C/D kapalı + 104×18 özet yer tutucu (`loadingSummary`).
 */
export function SavingsSkeleton() {
  return (
    <View>
      <ClaySurface level="raisedLg" borderRadius={radius.hero} background={color.primarySoft} style={stil.heroKart}>
        <View style={stil.aralik}>
          <Chip
            ad={t['tasarruf.kip.cip']}
            selected
            dotColor={color.primary}
            onPress={() => router.push('/ayarlar')}
            accessibilityLabel={t['a11y.tasarruf.kipCip']}
          />
          <Skeleton width={132} height={40} />
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <View style={stil.aralik}>
          <IconButton icon="chevron-left" accessibilityLabel={t['a11y.tasarruf.oncekiAy']} disabled />
          <LimitGauge
            mod="birikim"
            harcananKurus={-1}
            limitKurus={0}
            etiket=""
            accessibilityLabel={t['tasarruf.gosterge.hesaplaniyor']}
            centerOverride={
              <View style={stil.gostergeOrta}>
                <Skeleton width={140} height={38} />
                <View style={{ height: rhythm.sameObject }} />
                <Skeleton width={88} height={18} />
              </View>
            }
          />
          <IconButton icon="chevron-right" accessibilityLabel={t['a11y.tasarruf.sonrakiAy']} disabled />
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <Txt role="caption">{t['tasarruf.gosterge.hesaplaniyor']}</Txt>
      </ClaySurface>

      <View style={{ height: rhythm.group }} />

      <Accordion
        title={t[BOLUM_BASLIKLARI[0]]}
        loadingSummary
        expanded
        onToggle={() => {}}
        accessibilityLabel={a11yBolumYukleniyor(t[BOLUM_BASLIKLARI[0]])}>
        <View style={stil.denklem}>
          {[0, 1, 2].map((i) => (
            <Fragment key={i}>
              {i > 0 ? <View style={{ width: 16 }} /> : null}
              <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.denklemKutu}>
                <Skeleton width="64%" height={12} />
                <View style={{ height: rhythm.sameObject }} />
                <Skeleton width="100%" height={24} />
              </ClaySurface>
            </Fragment>
          ))}
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <Skeleton width="100%" height={18} />
        <View style={{ height: rhythm.blockInCard }} />
        <Skeleton width="60%" height={18} />
      </Accordion>

      {BOLUM_BASLIKLARI.slice(1).map((anahtar) => (
        <Fragment key={anahtar}>
          <View style={{ height: rhythm.group }} />
          <Accordion
            title={t[anahtar]}
            loadingSummary
            expanded={false}
            onToggle={() => {}}
            accessibilityLabel={a11yBolumYukleniyor(t[anahtar])}
          />
        </Fragment>
      ))}
    </View>
  );
}

const stil = StyleSheet.create({
  heroKart: { padding: rhythm.pad, alignItems: 'center' },
  aralik: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%' },
  gostergeOrta: { alignItems: 'center', justifyContent: 'center' },
  denklem: { flexDirection: 'row', alignItems: 'stretch', width: '100%' },
  denklemKutu: { flex: 1, minWidth: 0, padding: rhythm.group, alignItems: 'center', justifyContent: 'center' },
});
