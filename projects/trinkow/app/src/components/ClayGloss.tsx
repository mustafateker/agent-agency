import { StyleSheet } from 'react-native';
import Svg, { Defs, LinearGradient, Rect, Stop } from 'react-native-svg';

import { CLAY_FACE_STOP, gradient, rgbaAyir } from '@/theme/tokens';

let sayac = 0;

/**
 * §5.3 — kabarık yüzeyin üst %45'indeki parlama (`grad.clay-face`).
 * Gölge + parlama birlikte "3B kabarık" hissi verir; biri eksikse yüzey
 * düz görünür. Kapsayıcı View `overflow: 'hidden'` + borderRadius ile
 * köşeleri kırpar, bu yüzden dikdörtgen doldurmak yeterli.
 *
 * Not: `expo-linear-gradient` onaylı bağımlılık listesinde yok, bu yüzden
 * gradyanlar `react-native-svg` ile çiziliyor (§1.8 iki seçeneği de sayar).
 *
 * Alfa `stopOpacity` ile verilir: `stop-color` alfa taşımaz, rgba dizesi
 * doğrudan verilince parlama opak beyaza döner ve zemin tonunu (ör. kahraman
 * kartın `primary-soft`u) tamamen örter.
 */
const UST = rgbaAyir(gradient.clayFace[0]);
const ALT = rgbaAyir(gradient.clayFace[1]);

export function ClayGloss() {
  // Aynı sayfada çok sayıda gradyan olabilir → id çakışması yasak (§12 no.29)
  const id = `clayFace${++sayac}`;
  return (
    <Svg style={StyleSheet.absoluteFill} pointerEvents="none">
      <Defs>
        <LinearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor={UST.renk} stopOpacity={UST.opaklik} />
          <Stop offset={String(CLAY_FACE_STOP)} stopColor={ALT.renk} stopOpacity={ALT.opaklik} />
        </LinearGradient>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill={`url(#${id})`} />
    </Svg>
  );
}
