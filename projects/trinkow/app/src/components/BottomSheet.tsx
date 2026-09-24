import type { ReactNode } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, Modal, Pressable, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { color, radius } from '@/theme/tokens';

/**
 * tokens.md §"BottomSheet" — üst köşeler 32, zemin `bg`, gölge
 * `clay.raised-lg`, scrim `rgba(28,57,142,0.38)`. Ekranın tamamını
 * KAPLAMAZ — arkadaki yüzey (RN `Modal` altındaki ekran) görünür kalır.
 * Üstte 44×4 tutamak.
 */
export function BottomSheet({
  visible,
  onClose,
  children,
}: {
  visible: boolean;
  onClose: () => void;
  children: ReactNode;
}) {
  const insets = useSafeAreaInsets();
  return (
    <Modal
      visible={visible}
      transparent
      animationType="slide"
      statusBarTranslucent
      onRequestClose={onClose}>
      <KeyboardAvoidingView style={stil.katman} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        <Pressable
          style={[StyleSheet.absoluteFill, stil.scrim]}
          accessibilityRole="button"
          accessibilityLabel="Kapat"
          onPress={onClose}
        />
        <View style={[stil.sheet, { paddingBottom: insets.bottom + 16 }]}>
          <View style={stil.tutamacSatiri}>
            <View style={stil.tutamac} />
          </View>
          <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={{ paddingBottom: 8 }}>{children}</ScrollView>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const stil = StyleSheet.create({
  katman: { flex: 1, justifyContent: 'flex-end' },
  scrim: { backgroundColor: color.scrim },
  sheet: {
    backgroundColor: color.bg,
    borderTopLeftRadius: radius.hero,
    borderTopRightRadius: radius.hero,
    paddingHorizontal: 16,
    maxHeight: '90%',
    boxShadow: '0 -16px 32px -8px rgba(28,57,142,0.22)',
  },
  tutamacSatiri: { alignItems: 'center', paddingVertical: 12 },
  tutamac: { width: 44, height: 4, borderRadius: radius.pill, backgroundColor: color.line },
});
