import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { ClaySwitch } from '@/components/ClaySwitch';
import { Txt } from '@/components/Txt';
import { clay, color, radius, rhythm, size } from '@/theme/tokens';

/**
 * Bileşen envanteri §2 `SettingRow` — kabarık tek karar satırı. Solda
 * başlık + `caption` açıklama, sağda kontrol (`ClaySwitch` ya da serbest
 * `deger`). İç boşluk 12/16, minimum 68 (§7.3/§7.12 ile aynı ölçek).
 *
 * Anahtar varsa satırın TAMAMI dokunma hedefidir (tokens §7.12 `ClaySwitch`
 * notu) — anahtarın kendisi ayrı bir dokunma alanı DEĞİLDİR.
 */
export function SettingRow({
  baslik,
  aciklama,
  anahtarDegeri,
  anahtarKapali,
  onAnahtarDegistir,
  deger,
  disabled = false,
  accessibilityLabel,
}: {
  baslik: string;
  aciklama?: string;
  /** Verilirse satır bir `ClaySwitch` çizer. */
  anahtarDegeri?: boolean;
  /** §6 — izin yokken anahtar pasif ama GİZLENMEZ. */
  anahtarKapali?: boolean;
  onAnahtarDegistir?: () => void;
  /** `anahtarDegeri` verilmezse sağda serbest içerik (ör. yalnız metin). */
  deger?: ReactNode;
  disabled?: boolean;
  accessibilityLabel?: string;
}) {
  const anahtarVar = anahtarDegeri !== undefined;
  const gorunum = (
    <>
      <View style={stil.esnek}>
        <Txt role="bodyStrong">{baslik}</Txt>
        {aciklama ? (
          <>
            <View style={{ height: rhythm.sameObject }} />
            <Txt role="caption">{aciklama}</Txt>
          </>
        ) : null}
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      {anahtarVar ? <ClaySwitch value={anahtarDegeri} disabled={disabled || anahtarKapali} /> : deger}
    </>
  );

  if (!anahtarVar) {
    return <View style={stil.satir}>{gorunum}</View>;
  }

  return (
    <Pressable
      onPress={disabled || anahtarKapali ? undefined : onAnahtarDegistir}
      disabled={disabled || anahtarKapali}
      accessibilityRole="switch"
      accessibilityState={{ checked: anahtarDegeri, disabled: disabled || anahtarKapali }}
      accessibilityLabel={accessibilityLabel ?? baslik}
      style={({ pressed }) => [
        stil.satir,
        pressed && !disabled && !anahtarKapali ? { backgroundColor: color.groove, boxShadow: clay.pressed } : null,
      ]}>
      {gorunum}
    </Pressable>
  );
}

const stil = StyleSheet.create({
  satir: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: size.rowMinHeight,
    paddingVertical: size.rowPadY,
    paddingHorizontal: size.rowPadX,
    borderRadius: radius.tile,
  },
  esnek: { flex: 1, minWidth: 0 },
});
