import { StyleSheet, View } from 'react-native';

import { ClaySurface } from '@/components/ClaySurface';
import { IconButton } from '@/components/IconButton';
import { LimitGauge } from '@/components/LimitGauge';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { sayiyaCevir, SIMGE } from '@/lib/para';
import { color, gauge, radius, rhythm } from '@/theme/tokens';

/**
 * E-10 kahraman kart (v4 — K-049 sayfalama). Tek ağırlık merkezi korunur:
 * mavi panel → beyaz kil topak → çukur oluk → kabarık yay → kabarık topuz.
 * Bugün sayfasında yay CANLI (kalan/taşma); geçmiş sayfada KAPANMIŞ
 * (o günün toplam harcaması, `gunluk.hero.gecmis`). `limitKurus === null`
 * iken yay hiç çizilmez — `HeroPlain` dalına düşer (bağlayıcı kural,
 * tokens.md §3.2b / LimitGauge.tsx üst notu).
 */
type Props = {
  gunFarki: number;
  harcananKurus: number;
  limitKurus: number | null;
  /** §7.8 — bu günün hiç kaydı yok (gauge dolgu/topuz/taşma yok) */
  bos: boolean;
  oncekiPasif: boolean;
  onOnceki: () => void;
  onSonraki: () => void;
  altMetin: string;
};

export function HeroCard({
  gunFarki,
  harcananKurus,
  limitKurus,
  bos,
  oncekiPasif,
  onOnceki,
  onSonraki,
  altMetin,
}: Props) {
  const bugunMu = gunFarki === 0;
  const limitDisi = limitKurus !== null && harcananKurus > limitKurus;

  return (
    <ClaySurface
      level="raisedLg"
      borderRadius={radius.hero}
      background={color.primarySoft}
      style={stil.kart}>
      <View style={stil.merkezSatiri}>
        <IconButton
          icon="chevron-left"
          accessibilityLabel={t['gunluk.onceki_gun']}
          onPress={onOnceki}
          disabled={oncekiPasif}
        />
        {limitKurus === null ? (
          <HeroPlain
            harcananKurus={harcananKurus}
            etiket={bugunMu ? t['pano.hero.limitsiz'] : t['gunluk.hero.gecmis']}
          />
        ) : (
          <LimitGauge
            harcananKurus={harcananKurus}
            limitKurus={limitKurus}
            bos={bos}
            merkezTutarKurus={bugunMu ? undefined : harcananKurus}
            etiket={
              bugunMu
                ? limitDisi
                  ? t['pano.hero.limit_disi']
                  : t['pano.hero.takip']
                : t['gunluk.hero.gecmis']
            }
          />
        )}
        <IconButton
          icon="chevron-right"
          accessibilityLabel={t['gunluk.sonraki_gun']}
          onPress={onSonraki}
          disabled={bugunMu}
        />
      </View>

      <View style={{ height: bugunMu ? rhythm.blockInCard : rhythm.section }} />

      <Txt role="body" style={stil.ortaMetin}>
        {altMetin}
      </Txt>
    </ClaySurface>
  );
}

/**
 * `HeroPlain` — günlük limit TANIMSIZKEN çizilen ayrı dal (tokens.md §3.2b,
 * LimitGauge.tsx üst notu). Yay/oluk/topuz yok; ölçülecek bir eşik yoktur.
 * §7.5 "uzun tutar" kuralıyla aynı basamak-düşürme mantığı korunur.
 */
function HeroPlain({ harcananKurus, etiket }: { harcananKurus: number; etiket: string }) {
  const sayi = sayiyaCevir(harcananKurus);
  const uzun = sayi.length >= gauge.heroDigitLimit;
  return (
    <View style={stil.duzMerkez}>
      <View style={stil.paraSatiri}>
        <Txt
          role={uzun ? 'display' : 'hero'}
          numberOfLines={1}
          adjustsFontSizeToFit
          minimumFontScale={0.55}
          style={stil.esnekSayi}>
          {sayi}
        </Txt>
        <View style={{ width: rhythm.sameObject }} />
        <Txt role={uzun ? 'amount' : 'display'}>{SIMGE}</Txt>
      </View>
      <Txt role="label" tone={color.text2}>
        {etiket}
      </Txt>
    </View>
  );
}

const stil = StyleSheet.create({
  // §3.1 / §7.2 — kart iç boşluğu 16, istisnasız
  kart: { padding: rhythm.pad, alignItems: 'center' },
  merkezSatiri: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '100%',
  },
  duzMerkez: { alignItems: 'center' },
  paraSatiri: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center', width: gauge.innerWidth },
  esnekSayi: { flexShrink: 1, minWidth: 0 },
  ortaMetin: { textAlign: 'center' },
});
