import { router } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button } from '@/components/Button';
import { InfoStrip } from '@/components/InfoStrip';
import { OrDivider } from '@/components/OrDivider';
import { PasswordField } from '@/components/PasswordField';
import { PushHeader } from '@/components/PushHeader';
import { ResetSentCard } from '@/components/ResetSentCard';
import { SocialAuthButton } from '@/components/SocialAuthButton';
import { TextField } from '@/components/TextField';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { ApiAgHatasi, ApiHatasi, benKimim, girisYap } from '@/lib/api';
import { oturumYaz } from '@/lib/oturumDeposu';
import { appleIleDevamEt, googleIleDevamEt, sosyalSaglayicilar } from '@/lib/sosyalGiris';
import { color, layout, rhythm } from '@/theme/tokens';

const EPOSTA_BICIMI = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * D-2c-3 · E-22 Oturum aç — referans: prototip-v4/15-giris.html (8 yüzey).
 * K-080 ile "Hesapsız devam et" KALKTI — hesap zorunlu. Sosyal düğmeler
 * (K-057/BE-2d) tasarımdaki hâliyle DURUR, dikişleri boş; yalnız
 * e-posta/şifre backend'e gerçekten bağlıdır. Başarılı giriş sonrası
 * `router.back()` DEĞİL `router.replace('/')` kullanılır — açılışta bu
 * ekrana `_layout.tsx`'in giriş duvarı `replace` ile düşer, geri gidecek
 * bir ekran YOKTUR.
 */
export default function GirisEkrani() {
  const insets = useSafeAreaInsets();
  const [eposta, setEposta] = useState('');
  const [sifre, setSifre] = useState('');
  const [epostaHata, setEpostaHata] = useState<string | null>(null);
  const [sifreHata, setSifreHata] = useState<string | null>(null);
  const [agHatasi, setAgHatasi] = useState(false);
  const [gonderiliyor, setGonderiliyor] = useState(false);

  const [sifirlaGonderildi, setSifirlaGonderildi] = useState(false);
  const [sifirlaBekliyor, setSifirlaBekliyor] = useState(true);
  const bekleZamanlayici = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (bekleZamanlayici.current) clearTimeout(bekleZamanlayici.current);
    };
  }, []);

  function epostaBicimDogrula() {
    if (eposta.trim().length === 0) return;
    setEpostaHata(EPOSTA_BICIMI.test(eposta.trim()) ? null : t['hata.eposta_bicim']);
  }

  function sifremiUnuttum() {
    if (eposta.trim().length === 0) {
      setEpostaHata(t['hata.eposta_bos']);
      return;
    }
    if (!EPOSTA_BICIMI.test(eposta.trim())) {
      setEpostaHata(t['hata.eposta_bicim']);
      return;
    }
    setEpostaHata(null);
    setSifirlaGonderildi(true);
    setSifirlaBekliyor(true);
    bekleZamanlayici.current = setTimeout(() => setSifirlaBekliyor(false), 60000);
  }

  function yenidenGonder() {
    setSifirlaBekliyor(true);
    bekleZamanlayici.current = setTimeout(() => setSifirlaBekliyor(false), 60000);
  }

  async function gonder() {
    if (eposta.trim().length === 0 || sifre.length === 0 || gonderiliyor) return;
    if (!EPOSTA_BICIMI.test(eposta.trim())) {
      setEpostaHata(t['hata.eposta_bicim']);
      return;
    }
    setEpostaHata(null);
    setSifreHata(null);
    setAgHatasi(false);
    setGonderiliyor(true);
    try {
      const cift = await girisYap(eposta.trim(), sifre);
      await oturumYaz({
        erisimTokeni: cift.erisimTokeni,
        yenilemeTokeni: cift.yenilemeTokeni,
        kullaniciId: '',
        email: eposta.trim(),
        kimlikSaglayici: 'eposta',
      });
      try {
        const ben = await benKimim();
        await oturumYaz({
          erisimTokeni: cift.erisimTokeni,
          yenilemeTokeni: cift.yenilemeTokeni,
          kullaniciId: ben.id,
          email: ben.email,
          kimlikSaglayici: ben.kimlikSaglayici,
        });
      } catch {
        // "ben kimim" başarısız olsa bile oturum açık kalır — Ayarlar
        // bir sonraki açılışta yeniden okumayı dener.
      }
      router.replace('/');
    } catch (hata) {
      if (hata instanceof ApiAgHatasi) {
        setAgHatasi(true);
      } else if (hata instanceof ApiHatasi && hata.durum === 401) {
        setSifreHata(t['hata.kimlik']);
      } else {
        setAgHatasi(true);
      }
    } finally {
      setGonderiliyor(false);
    }
  }

  const gonderPasif = eposta.trim().length === 0 || sifre.length === 0;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <PushHeader baslik={t['giris.baslik']} onGeri={() => router.back()} />
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={insets.top}>
        {sifirlaGonderildi ? (
          <ScrollView
            keyboardShouldPersistTaps="handled"
            contentContainerStyle={[stil.pad, { paddingBottom: layout.scrollPadBottom + insets.bottom }]}
            showsVerticalScrollIndicator={false}>
            <View style={{ height: rhythm.section }} />
            <ResetSentCard eposta={eposta.trim()} yenidenGonderPasif={sifirlaBekliyor} onYenidenGonder={yenidenGonder} />
            <View style={{ height: rhythm.section }} />
            <Button label={t['sifirla.geri']} variant="ghost" onPress={() => setSifirlaGonderildi(false)} />
          </ScrollView>
        ) : (
          <>
            <ScrollView
              keyboardShouldPersistTaps="handled"
              contentContainerStyle={stil.pad}
              showsVerticalScrollIndicator={false}>
              <Txt role="caption">{t['hesap.mahremiyet']}</Txt>
              <View style={{ height: rhythm.section }} />

              {agHatasi ? (
                <>
                  <InfoStrip variant="warning" icon="wifi-off" metin={t['hata.baglanti.giris']} />
                  <View style={{ height: rhythm.section }} />
                </>
              ) : null}

              {sosyalSaglayicilar().map((saglayici, i) => (
                <View key={saglayici}>
                  {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
                  <SocialAuthButton
                    provider={saglayici}
                    onPress={() => void (saglayici === 'apple' ? appleIleDevamEt() : googleIleDevamEt())}
                  />
                </View>
              ))}
              <View style={{ height: rhythm.blockInCard }} />
              <OrDivider />
              <View style={{ height: rhythm.blockInCard }} />

              <TextField
                label={t['alan.eposta']}
                placeholder={t['alan.eposta_ph']}
                value={eposta}
                onChangeText={(v) => {
                  setEposta(v);
                  if (epostaHata) setEpostaHata(null);
                }}
                onBlur={epostaBicimDogrula}
                error={epostaHata ?? undefined}
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                textContentType="emailAddress"
                accessibilityLabel={t['alan.eposta']}
              />
              <View style={{ height: rhythm.blockInCard }} />
              <PasswordField
                label={t['alan.sifre']}
                placeholder={t['alan.sifre_ph.giris']}
                value={sifre}
                onChangeText={(v) => {
                  setSifre(v);
                  if (sifreHata) setSifreHata(null);
                }}
                error={sifreHata ?? undefined}
                autoComplete="current-password"
                textContentType="password"
                accessibilityLabel={t['alan.sifre']}
              />
              <View style={{ height: rhythm.blockInCard }} />
              <View style={stil.aralik}>
                <Button label={t['giris.unuttum']} variant="ghost" auto onPress={sifremiUnuttum} />
                <Button label={t['giris.kayit_kapisi']} variant="ghost" auto onPress={() => router.replace('/kayit')} />
              </View>
              <View style={{ height: rhythm.section }} />
            </ScrollView>

            <View style={[stil.altSabit, { paddingBottom: insets.bottom + rhythm.pad }]}>
              <Button
                label={t['giris.eylem']}
                loadingLabel={t['giris.mesgul']}
                variant="primary"
                disabled={gonderPasif}
                loading={gonderiliyor}
                onPress={() => void gonder()}
              />
            </View>
          </>
        )}
      </KeyboardAvoidingView>
    </View>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  pad: { paddingHorizontal: layout.screenPaddingX },
  aralik: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  altSabit: { paddingHorizontal: layout.screenPaddingX, paddingTop: rhythm.pad },
});
