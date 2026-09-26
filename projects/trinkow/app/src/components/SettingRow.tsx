import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { ClaySwitch } from '@/components/ClaySwitch';
import { Icon, type IconName } from '@/components/Icon';
import { NeutralIconBox } from '@/components/CategoryIconBox';
import { Txt } from '@/components/Txt';
import { clay, color, radius, rhythm, size } from '@/theme/tokens';

/**
 * Bileşen envanteri §2 `SettingRow` — kabarık tek karar satırı. Solda
 * başlık + `caption` açıklama, sağda kontrol (`ClaySwitch` ya da serbest
 * `deger`). İç boşluk 12/16, minimum 68 (§7.3/§7.12 ile aynı ölçek).
 *
 * Anahtar varsa satırın TAMAMI dokunma hedefidir (tokens §7.12 `ClaySwitch`
 * notu) — anahtarın kendisi ayrı bir dokunma alanı DEĞİLDİR.
 *
 * `icon` + `onPress` — rev2-tasarruf-profil.md §4.3 **gezinme varyantı**:
 * solda 44 `kat-kab.notr` ikon kabı, sağda `chevron-right`, ikincil satır
 * (`aciklama`) satırın gerçek değerini taşır. Anahtar/gezinme aynı anda
 * verilmez; ikisi de yoksa satır dokunulamaz (eski davranış korunur).
 */
export function SettingRow({
  baslik,
  aciklama,
  icon,
  onPress,
  anahtarDegeri,
  anahtarKapali,
  onAnahtarDegistir,
  deger,
  disabled = false,
  accessibilityLabel,
}: {
  baslik: string;
  aciklama?: string;
  /** Gezinme varyantı — sol ikon kabı (§4.3). */
  icon?: IconName;
  /** Gezinme varyantı — verilirse satır `Pressable` olur, sağda `chevron-right` görünür. */
  onPress?: () => void;
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
  const gezinmeMi = !anahtarVar && onPress !== undefined;
  const gorunum = (
    <>
      {icon ? (
        <>
          <NeutralIconBox icon={icon} />
          <View style={{ width: rhythm.blockInCard }} />
        </>
      ) : null}
      <View style={stil.esnek}>
        <Txt role="bodyStrong" numberOfLines={gezinmeMi ? 1 : undefined} ellipsizeMode="tail">
          {baslik}
        </Txt>
        {aciklama ? (
          <>
            <View style={{ height: rhythm.sameObject }} />
            <Txt role="caption" numberOfLines={gezinmeMi ? 1 : undefined} ellipsizeMode="tail">
              {aciklama}
            </Txt>
          </>
        ) : null}
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      {anahtarVar ? (
        <ClaySwitch value={anahtarDegeri} disabled={disabled || anahtarKapali} />
      ) : gezinmeMi ? (
        (deger ?? <Icon name="chevron-right" size={size.iconSm} color={color.text2} />)
      ) : (
        deger
      )}
    </>
  );

  if (anahtarVar) {
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

  if (gezinmeMi) {
    return (
      <Pressable
        onPress={disabled ? undefined : onPress}
        disabled={disabled}
        accessibilityRole="button"
        accessibilityState={{ disabled }}
        accessibilityLabel={accessibilityLabel ?? baslik}
        style={({ pressed }) => [
          stil.satir,
          { backgroundColor: color.surface, boxShadow: clay.raised },
          pressed && !disabled ? { backgroundColor: color.groove, boxShadow: clay.pressed } : null,
        ]}>
        {gorunum}
      </Pressable>
    );
  }

  return <View style={stil.satir}>{gorunum}</View>;
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
