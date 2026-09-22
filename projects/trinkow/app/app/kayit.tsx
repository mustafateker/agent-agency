import { router } from 'expo-router';
import { useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button } from '@/components/Button';
import { InfoStrip } from '@/components/InfoStrip';
import { LegalConsentText } from '@/components/LegalConsentText';
import { OrDivider } from '@/components/OrDivider';
import { PasswordField } from '@/components/PasswordField';
import { PasswordRuleLine } from '@/components/PasswordRuleLine';
import { PushHeader } from '@/components/PushHeader';
import { SocialAuthButton } from '@/components/SocialAuthButton';
import { TextField } from '@/components/TextField';
import { Txt } from '@/components/Txt';
import { t } from '@/content/metinler';
import { ApiAgHatasi, ApiHatasi, benKimim, kayitOl } from '@/lib/api';
import { oturumYaz } from '@/lib/oturumDeposu';
import { appleIleDevamEt, googleIleDevamEt, sosyalSaglayicilar } from '@/lib/sosyalGiris';
import { color, layout, rhythm } from '@/theme/tokens';

const EPOSTA_BICIMI = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const SIFRE_MIN_UZUNLUK = 8;

/**
 * D-2c-3 · E-23 Hesap oluştur — referans: prototip-v4/16-kayit.html (7 yüzey).
 * K-080 ile "Hesapsız devam et" KALKTI — hesap zorunlu. Sosyal düğmeler
 * tasarımdaki hâliyle DURUR, dikişleri boş; yasal bağlantılar yer
 * tutucudur (delta-v4 çelişki #7, belge metinleri henüz yazılmadı).
 * Başarılı kayıt sonrası `router.replace('/')` — bkz. giris.tsx aynı not.
 */
export default function KayitEkrani() {
  const insets = useSafeAreaInsets();
  const [eposta, setEposta] = useState('');
  const [sifre, setSifre] = useState('');
  const [epostaHata, setEpostaHata] = useState<string | null>(null);
  const [agHatasi, setAgHatasi] = useState(false);
  const [gonderiliyor, setGonderiliyor] = useState(false);

  const kuralKarsilandi = sifre.length >= SIFRE_MIN_UZUNLUK;

  function epostaBicimDogrula() {
    if (eposta.trim().length === 0) return;
    setEpostaHata(EPOSTA_BICIMI.test(eposta.trim()) ? null : t['hata.eposta_bicim']);
  }

  async function gonder() {
    if (eposta.trim().length === 0 || !kuralKarsilandi || gonderiliyor) return;
    if (!EPOSTA_BICIMI.test(eposta.trim())) {
      setEpostaHata(t['hata.eposta_bicim']);
      return;
    }
    setEpostaHata(null);
    setAgHatasi(false);
    setGonderiliyor(true);
    try {
      const cift = await kayitOl(eposta.trim(), sifre);
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
        // bkz. giris.tsx aynı not — oturum açık kalır.
      }
      router.replace('/');
    } catch (hata) {
      if (hata instanceof ApiAgHatasi) {
        setAgHatasi(true);
      } else if (hata instanceof ApiHatasi && hata.durum === 409) {
        setEpostaHata(t['hata.eposta_kayitli']);
      } else {
        setAgHatasi(true);
      }
    } finally {
      setGonderiliyor(false);
    }
  }

  const gonderPasif = eposta.trim().length === 0 || !kuralKarsilandi;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <PushHeader baslik={t['kayit.baslik']} onGeri={() => router.back()} />
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={insets.top}>
        <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false}>
          <View style={{ height: rhythm.section }} />

          {agHatasi ? (
            <>
              <InfoStrip variant="warning" icon="wifi-off" metin={t['hata.baglanti.kayit']} />
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
            placeholder={t['alan.sifre_ph.kayit']}
            value={sifre}
            onChangeText={setSifre}
            autoComplete="new-password"
            textContentType="newPassword"
            accessibilityLabel={t['alan.sifre']}
          />
          <View style={{ height: rhythm.group }} />
          <PasswordRuleLine met={kuralKarsilandi} />

          <View style={{ height: rhythm.section }} />
          <InfoStrip variant="info" icon="info" metin={`${t['hesap.mahremiyet']} ${t['hesap.mahremiyet.ek']}`} />

          <View style={{ height: rhythm.section }} />
          <LegalConsentText metin={t['kayit.yasal']} />

          <View style={{ height: rhythm.blockInCard }} />
          <View style={stil.aralik}>
            <Txt role="caption">{t['kayit.giris_kapisi.soru']}</Txt>
            <Button label={t['kayit.giris_kapisi.aksiyon']} variant="ghost" auto onPress={() => router.replace('/giris')} />
          </View>
          <View style={{ height: rhythm.section }} />
        </ScrollView>

        <View style={[stil.altSabit, { paddingBottom: insets.bottom + rhythm.pad }]}>
          <Button
            label={t['kayit.eylem']}
            loadingLabel={t['kayit.mesgul']}
            variant="primary"
            disabled={gonderPasif}
            loading={gonderiliyor}
            onPress={() => void gonder()}
          />
        </View>
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
