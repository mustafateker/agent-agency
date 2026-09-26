import { forwardRef, useImperativeHandle, useRef, type ReactNode } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { IconButton } from '@/components/IconButton';
import { StepIndicator } from '@/components/StepIndicator';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { color, layout, rhythm, size } from '@/theme/tokens';

export type SetupShellHandle = { scrollToTop: () => void };

/**
 * rev2-onboarding-kayit.md §2 — kurulumun kendi kabuğu. `RevScreen`
 * KULLANILMAZ (h1 başlık basıyor, iç boşluğu 24 yapıyor — ikisi de bu
 * akışta tokens'a aykırı, bkz. spesifikasyon giriş bölümü).
 *
 * B2 (düzeltilmiş bulgu, en kritik): başlık çubuğu + adım oluğu
 * `ScrollView`ın KARDEŞİDİR, çocuğu değil — 2/4 formu aşağı kaydırıldığında
 * ilerleme göstergesi ekrandan ÇIKMAZ. Alt-sabit blok da aynı nedenle
 * `ScrollView`ın dışında: birincil düğme parmağın altından kaçmaz.
 */
export const SetupShell = forwardRef<
  SetupShellHandle,
  {
    adim: number;
    toplam?: number;
    /** `null` → sol üstte 44×44 denge kutusu (1/4'te geri yolu yok). */
    onGeri: (() => void) | null;
    children: ReactNode;
    altSabit: ReactNode;
  }
>(function SetupShell({ adim, toplam = 4, onGeri, children, altSabit }, ref) {
  const insets = useSafeAreaInsets();
  const scrollRef = useRef<ScrollView>(null);

  useImperativeHandle(ref, () => ({
    scrollToTop: () => scrollRef.current?.scrollTo({ y: 0, animated: false }),
  }));

  return (
    <View style={[stil.ekran, { paddingTop: insets.top }]}>
      <View style={stil.ekranBasi}>
        {onGeri ? (
          <IconButton icon="chevron-left" accessibilityLabel={t['a11y.onceki_adim']} onPress={onGeri} />
        ) : (
          <View style={stil.denge} />
        )}
        <Txt role="micro" tone={color.text2}>
          {`${adim}/${toplam}`}
        </Txt>
        <View style={stil.denge} />
      </View>
      <View style={stil.adimCubugu}>
        <StepIndicator adim={adim} toplam={toplam} />
      </View>
      <KeyboardAvoidingView
        style={stil.esnek}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={insets.top}>
        <ScrollView
          ref={scrollRef}
          style={stil.esnek}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
          contentContainerStyle={stil.icerik}>
          {children}
        </ScrollView>
        <View style={[stil.altSabit, { paddingBottom: Math.max(insets.bottom, rhythm.group) }]}>{altSabit}</View>
      </KeyboardAvoidingView>
    </View>
  );
});

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  esnek: { flex: 1, minHeight: 0 },
  ekranBasi: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: layout.headerPadTop,
    paddingBottom: layout.headerPadBottom,
    paddingHorizontal: layout.screenPaddingX,
  },
  denge: { width: size.iconButton, height: size.iconButton },
  adimCubugu: { paddingHorizontal: layout.screenPaddingX },
  icerik: { paddingHorizontal: layout.screenPaddingX, paddingTop: rhythm.section, paddingBottom: rhythm.section },
  altSabit: { paddingHorizontal: layout.screenPaddingX, paddingTop: rhythm.group },
});
