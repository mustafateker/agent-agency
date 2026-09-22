// §2.1 — TOPLAM 4 FONT DOSYASI, artırılamaz. Paket kökünden (barrel) import
// edilirse Google Fonts paketinin BÜTÜN ağırlıkları paketlenir; bu yüzden
// yalnız ilgili alt yollar import edilir.
import { Montserrat_400Regular } from '@expo-google-fonts/montserrat/400Regular';
import { Montserrat_600SemiBold } from '@expo-google-fonts/montserrat/600SemiBold';
import { Montserrat_700Bold } from '@expo-google-fonts/montserrat/700Bold';
import { Poppins_600SemiBold } from '@expo-google-fonts/poppins/600SemiBold';
import { useFonts } from 'expo-font';
import { router, Stack } from 'expo-router';
import { SQLiteProvider, useSQLiteContext } from 'expo-sqlite';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';

import { DB_ADI, semayiKur } from '@/db';
import { onboardingTamamlandiMi } from '@/db/profil';
import { gunSiniriOku, kurulumGunuBaslat } from '@/db/ayarTercihleri';
import { katalogTazele } from '@/db/katalog';
import { ProfilingHost } from '@/components/ProfilingHost';
import { ToastHost } from '@/components/ToastHost';
import { benKimim } from '@/lib/api';
import { oturumDegisimineAbone, oturumOku, oturumSil } from '@/lib/oturumDeposu';
import { gunSiniriSaatiniAyarla } from '@/lib/tarih';
import { girisEkraninaDon } from '@/lib/yonlendirme';
import { color } from '@/theme/tokens';

/**
 * İlk açılış yönlendirmesi — TEK yer burasıdır (D-2d-3a / D-2c-3 ile
 * genişletildi). Sıra (K-080 — hesap ZORUNLU): açılış → (oturum yoksa)
 * `/giris` → (onboarding tamamlanmadıysa) `/onboarding` → uygulama.
 *
 * Oturum durumu değiştiğinde (giriş/kayıt başarılı, çıkış, hesap silme,
 * `api.ts`'in token yenileme başarısızlığı) `oturumDeposu`'nun mevcut
 * yayın/abone mekanizması (`oturumDegisimineAbone`) bu koruyucuyu yeniden
 * tetikler — ikinci bir yönlendirme mekanizması KURULMADI, tek yer burası.
 */
function OnboardingYonlendirici() {
  const db = useSQLiteContext();
  const [tetik, setTetik] = useState(0);

  useEffect(() => oturumDegisimineAbone(() => setTetik((n) => n + 1)), []);

  useEffect(() => {
    let iptal = false;
    (async () => {
      const kayit = await oturumOku();
      if (!kayit) {
        if (!iptal) girisEkraninaDon();
        return;
      }
      try {
        await benKimim(); // 401 ise api.ts zaten tek seferlik yenilemeyi dener
      } catch {
        if (!iptal) {
          await oturumSil(); // pub/sub bu efekti yeniden tetikler
          girisEkraninaDon();
        }
        return;
      }
      // K-084/2 — kurulum günü write-once: sunucuda zaten varsa sessizce yok
      // sayılır, bu yüzden her açılışta çağrılabilir (bkz. `ayarTercihleri.ts`).
      kurulumGunuBaslat(db).catch(() => {
        // Ağ hatası — bir sonraki açılışta tekrar denenir, akışı bloklamaz.
      });
      // BE-6c Madde 4 — katalog ETag ile tazelenir; gömülü 80 kalem varsayılan kalır.
      katalogTazele(db).catch(() => {
        // bkz. `db/katalog.ts` — sessiz kalınır.
      });
      try {
        const tamam = await onboardingTamamlandiMi(db);
        if (!iptal && !tamam) router.replace('/onboarding');
      } catch {
        // Okuma başarısızsa onboarding'i zorlamak yerine mevcut ekranda kal.
      }
    })();
    return () => {
      iptal = true;
    };
  }, [db, tetik]);

  // D-2c-1b — F-15 gün sınırı tercihini `gunAnahtari`nin senkron önbelleğine
  // yükler; TEK yer (app açılışı). Ayarlar ekranında değişince
  // `gunSiniriKaydet` zaten anında günceller (bkz. `db/ayarTercihleri.ts`).
  useEffect(() => {
    let iptal = false;
    gunSiniriOku(db)
      .then((saat) => {
        if (!iptal) gunSiniriSaatiniAyarla(saat);
      })
      .catch(() => {
        // Okunamazsa varsayılan (gece yarısı) kalır.
      });
    return () => {
      iptal = true;
    };
  }, [db]);

  return null;
}

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
            <OnboardingYonlendirici />
            <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: color.bg } }}>
              <Stack.Screen name="harcama-ekle" options={{ presentation: 'modal' }} />
              <Stack.Screen name="harcama/[id]" options={{ presentation: 'modal' }} />
              <Stack.Screen name="onboarding" options={{ gestureEnabled: false }} />
              <Stack.Screen name="tanisma" options={{ gestureEnabled: false }} />
              <Stack.Screen name="plan" options={{ gestureEnabled: false }} />
            </Stack>
            <ProfilingHost />
            <ToastHost />
          </SQLiteProvider>
        </View>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
