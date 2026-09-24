import { router } from 'expo-router';
import { useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button } from '@/components/Button';
import { InfoStrip } from '@/components/InfoStrip';
import { OrDivider } from '@/components/OrDivider';
import { PasswordField } from '@/components/PasswordField';
import { PushHeader } from '@/components/PushHeader';
import { SettingRow } from '@/components/SettingRow';
import { SocialAuthButton } from '@/components/SocialAuthButton';
import { TextField } from '@/components/TextField';
import { Txt } from '@/components/Txt';
import { ApiHatasi, GELISTIRME_GIRISI, benKimim, girisYap } from '@/lib/api';
import { oturumYaz } from '@/lib/oturumDeposu';
import { appleIleDevamEt, googleIleDevamEt, sosyalSaglayicilar } from '@/lib/sosyalGiris';
import { color, layout, rhythm } from '@/theme/tokens';

export default function GirisEkrani() {
  const insets = useSafeAreaInsets();
  const [eposta, setEposta] = useState('');
  const [sifre, setSifre] = useState('');
  const [hatirla, setHatirla] = useState(true);
  const [demo, setDemo] = useState(false);
  const [hata, setHata] = useState<string | null>(null);
  const [mesgul, setMesgul] = useState(false);
  async function gonder() {
    if (mesgul) return;
    if (!demo && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(eposta.trim())) { setHata('Geçerli bir e-posta adresi gir.'); return; }
    setHata(null); setMesgul(true);
    try {
      const cift = await girisYap(eposta.trim(), sifre, demo);
      const ben = await benKimim(cift.erisimTokeni);
      await oturumYaz({ ...cift, kullaniciId: ben.id, email: ben.email, kimlikSaglayici: ben.kimlikSaglayici }, hatirla);
    } catch (e) {
      setHata(e instanceof ApiHatasi && e.durum === 401 ? 'E-posta ya da şifre yanlış.' : 'Oturum açılamadı. Bağlantını kontrol edip yeniden dene.');
    } finally { setMesgul(false); }
  }
  return <View style={[stil.ekran, { paddingTop: insets.top }]}>
    <PushHeader baslik="Oturum aç" onGeri={() => { if (router.canGoBack()) router.back(); }} />
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScrollView keyboardShouldPersistTaps="handled" contentContainerStyle={[stil.icerik, { paddingBottom: insets.bottom + 24 }]}>
        {hata ? <InfoStrip variant="warning" icon="info" metin={hata} /> : null}
        <TextField label={demo ? 'Test adı' : 'E-posta'} value={eposta} onChangeText={setEposta} keyboardType="email-address" autoCapitalize="none" autoComplete="email" textContentType="emailAddress" />
        <PasswordField label="Şifre" value={sifre} onChangeText={setSifre} autoComplete="current-password" textContentType="password" />
        <SettingRow baslik="Beni hatırla" aciklama="Bu cihazda oturumun açık kalsın." anahtarDegeri={hatirla} onAnahtarDegistir={() => setHatirla(!hatirla)} />
        <Button label="Şifremi unuttum" variant="ghost" onPress={() => router.push('/sifremi-unuttum')} />
        <Button label="Giriş yap" loadingLabel="Giriş yapılıyor…" variant="primary" loading={mesgul} disabled={!eposta.trim() || !sifre} onPress={() => void gonder()} />
        <Button label="Hesap oluştur" variant="ghost" onPress={() => router.replace('/kayit')} />
        <OrDivider />
        {sosyalSaglayicilar().map((provider) => <SocialAuthButton key={provider} provider={provider} disabled onPress={() => void (provider === 'apple' ? appleIleDevamEt() : googleIleDevamEt())} />)}
        <Txt role="micro">Apple ve Google ile giriş henüz kullanıma açılmadı.</Txt>
        {GELISTIRME_GIRISI ? <SettingRow baslik="Geliştirme test girişi" aciklama="Yalnız test hesabıyla giriş yapar." anahtarDegeri={demo} onAnahtarDegistir={() => setDemo(!demo)} /> : null}
        <Button label="Gizlilik ve kullanım şartları" variant="ghost" onPress={() => router.push('/legal')} />
      </ScrollView>
    </KeyboardAvoidingView>
  </View>;
}
const stil = StyleSheet.create({ ekran: { flex: 1, backgroundColor: color.bg }, icerik: { paddingHorizontal: layout.screenPaddingX, gap: rhythm.blockInCard } });
