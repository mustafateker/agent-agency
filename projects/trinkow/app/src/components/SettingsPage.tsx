import type { ReactNode } from 'react';
import { router } from 'expo-router';
import { KeyboardAvoidingView, Platform, ScrollView, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { PushHeader } from '@/components/PushHeader';
import { color, layout, rhythm } from '@/theme/tokens';
export function SettingsPage({ baslik, children }: { baslik: string; children: ReactNode }) {
  const insets = useSafeAreaInsets();
  return <View style={{ flex: 1, backgroundColor: color.bg, paddingTop: insets.top }}>
    <PushHeader baslik={baslik} onGeri={() => router.canGoBack() ? router.back() : router.replace('/giris')} />
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={{ paddingHorizontal: layout.screenPaddingX, paddingBottom: insets.bottom + 24, gap: rhythm.blockInCard }}>{children}</ScrollView>
    </KeyboardAvoidingView>
  </View>;
}
