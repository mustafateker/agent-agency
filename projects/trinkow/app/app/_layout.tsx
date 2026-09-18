// §2.1 — TOPLAM 4 FONT DOSYASI, artırılamaz. Paket kökünden (barrel) import
// edilirse Google Fonts paketinin BÜTÜN ağırlıkları paketlenir; bu yüzden
// yalnız ilgili alt yollar import edilir.
import { Montserrat_400Regular } from '@expo-google-fonts/montserrat/400Regular';
import { Montserrat_600SemiBold } from '@expo-google-fonts/montserrat/600SemiBold';
import { Montserrat_700Bold } from '@expo-google-fonts/montserrat/700Bold';
import { Poppins_600SemiBold } from '@expo-google-fonts/poppins/600SemiBold';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { SQLiteProvider } from 'expo-sqlite';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';

import { DB_ADI, semayiKur } from '@/db';
import { ToastHost } from '@/components/ToastHost';
import { color } from '@/theme/tokens';

SplashScreen.preventAutoHideAsync().catch(() => {
  // Splash zaten kapanmışsa sorun değil.
});

export default function RootLayout() {
  const [fontHazir, fontHatasi] = useFonts({
    Montserrat_400Regular,
    Montserrat_600SemiBold,
    Montserrat_700Bold,
    Poppins_600SemiBold,
  });

  useEffect(() => {
    if (fontHazir || fontHatasi) SplashScreen.hideAsync().catch(() => {});
  }, [fontHazir, fontHatasi]);

  if (!fontHazir && !fontHatasi) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        {/* Faz 1: tek tema (açık). useColorScheme kullanılmaz. */}
        <StatusBar style="dark" />
        <View style={{ flex: 1, backgroundColor: color.bg }}>
          <SQLiteProvider databaseName={DB_ADI} onInit={semayiKur}>
            <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: color.bg } }}>
              <Stack.Screen name="harcama-ekle" options={{ presentation: 'modal' }} />
              <Stack.Screen name="harcama/[id]" options={{ presentation: 'modal' }} />
            </Stack>
            <ToastHost />
          </SQLiteProvider>
        </View>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
