import { StyleSheet, View } from 'react-native';

import { Button } from '@/components/Button';
import { ClayPressable } from '@/components/ClayPressable';
import { ClaySurface } from '@/components/ClaySurface';
import { FactStrip } from '@/components/FactStrip';
import { Icon } from '@/components/Icon';
import { Skeleton } from '@/components/Skeleton';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { clay, color, radius, rhythm } from '@/theme/tokens';

type Olgu = { icon: 'trending-up'; olgu: string; baglam: string };

/**
 * Bileşen envanteri §5 `IdentityPanel` (yeni) — rev2-tasarruf-profil.md
 * §4.2/§4.2.1: kahraman panel (`primary-soft` · r32 · `clay.raised-lg`).
 * Dört durumun DÖRDÜ de aynı panel — aksan durum değiştirince kaybolmaz.
 * `signed-in`de içine `FactStrip` girer (Ö7 takviyesi, panel 156pt);
 * `signed-out`/`error`de şerit ÇİZİLMEZ (panelin tek mesajı bölünmez).
 */
export function IdentityPanel(
  props:
    | { variant: 'signed-in'; eposta: string; saglayiciEtiketi: string; olgu: Olgu; onPress: () => void }
    | { variant: 'signed-out'; onOturumAc: () => void }
    | { variant: 'error'; onRetry: () => void }
    | { variant: 'skeleton' },
) {
  if (props.variant === 'skeleton') {
    return (
      <ClaySurface level="raisedLg" borderRadius={radius.hero} background={color.primarySoft} style={stil.panel}>
        <View style={stil.satir}>
          <Skeleton width={48} height={48} borderRadius={radius.tile} />
          <View style={{ width: rhythm.blockInCard }} />
          <View style={stil.esnek}>
            <Skeleton width={208} height={16} />
            <View style={{ height: rhythm.sameObject }} />
            <Skeleton width={136} height={13} />
          </View>
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <Skeleton width="100%" height={64} borderRadius={radius.tile} />
      </ClaySurface>
    );
  }

  if (props.variant === 'signed-out') {
    return (
      <ClaySurface level="raisedLg" borderRadius={radius.hero} background={color.primarySoft} style={stil.panel}>
        <Txt role="bodyStrong">{t['profil.kimlik.hesapsiz.baslik']}</Txt>
        <View style={{ height: rhythm.sameObject }} />
        <Txt role="caption">{t['profil.kimlik.hesapsiz.alt']}</Txt>
        <View style={{ height: rhythm.blockInCard }} />
        <Button variant="secondary" label={t['profil.kimlik.hesapsiz.btn']} auto onPress={props.onOturumAc} />
      </ClaySurface>
    );
  }

  if (props.variant === 'error') {
    return (
      <ClaySurface level="raisedLg" borderRadius={radius.hero} background={color.primarySoft} style={stil.panel}>
        <View style={stil.hataBaslik}>
          <Icon name="wifi-off" size={20} color={color.text2} />
          <View style={{ width: rhythm.group }} />
          <Txt role="bodyStrong">{t['profil.kimlik.hata.baslik']}</Txt>
        </View>
        <View style={{ height: rhythm.sameObject }} />
        <Txt role="caption">{t['profil.kimlik.hata.alt']}</Txt>
        <View style={{ height: rhythm.blockInCard }} />
        <Button variant="secondary" label={t['profil.kimlik.hata.btn']} auto onPress={props.onRetry} />
      </ClaySurface>
    );
  }

  const { eposta, saglayiciEtiketi, olgu, onPress } = props;
  const etiket = `Hesabını aç. ${eposta}, ${saglayiciEtiketi}. ${olgu.olgu}, ${olgu.baglam}`;

  return (
    <ClayPressable
      onPress={onPress}
      accessibilityLabel={etiket}
      borderRadius={radius.hero}
      background={color.primarySoft}
      pressedBackground={color.groove}
      shadow={clay.raisedLg}
      pressedShadow={clay.pressed}
      gloss
      style={stil.panel}>
      <View style={stil.satir}>
        <ClaySurface level="sunken" borderRadius={radius.tile} background={color.groove} style={stil.ikonKutu}>
          <Icon name="user" size={24} color={color.primaryText} />
        </ClaySurface>
        <View style={{ width: rhythm.blockInCard }} />
        <View style={stil.esnek}>
          <Txt role="bodyStrong" numberOfLines={1} ellipsizeMode="tail">
            {eposta}
          </Txt>
          <View style={{ height: rhythm.sameObject }} />
          <Txt role="caption" numberOfLines={1}>
            {saglayiciEtiketi}
          </Txt>
        </View>
        <View style={{ width: rhythm.blockInCard }} />
        <Icon name="chevron-right" size={20} color={color.text2} />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <FactStrip icon={olgu.icon} olgu={olgu.olgu} baglam={olgu.baglam} />
    </ClayPressable>
  );
}

const stil = StyleSheet.create({
  panel: { padding: rhythm.pad, borderRadius: radius.hero },
  satir: { flexDirection: 'row', alignItems: 'center' },
  esnek: { flex: 1, minWidth: 0 },
  ikonKutu: { width: 48, height: 48, alignItems: 'center', justifyContent: 'center' },
  hataBaslik: { flexDirection: 'row', alignItems: 'center' },
});
