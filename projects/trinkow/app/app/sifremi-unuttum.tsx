import { useState } from 'react';
import { useLocalSearchParams } from 'expo-router';
import { SettingsPage } from '@/components/SettingsPage';
import { TextField } from '@/components/TextField';
import { Button } from '@/components/Button';
import { Txt } from '@/components/Txt';
import { InfoStrip } from '@/components/InfoStrip';
import { ApiHatasi, sifirlamaIste } from '@/lib/api';
export default function SifremiUnuttum() {
  const params = useLocalSearchParams<{ email?: string }>();
  const [email, setEmail] = useState(params.email ?? '');
  const [mesgul, setMesgul] = useState(false);
  const [bitti, setBitti] = useState(false);
  const [hata, setHata] = useState<string | null>(null);
  async function gonder() {
    if (mesgul) return;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) { setHata('Geçerli bir e-posta adresi gir.'); return; }
    setMesgul(true); setHata(null);
    try { await sifirlamaIste(email.trim()); setBitti(true); }
    catch (e) { setHata(e instanceof ApiHatasi && e.durum === 503 ? 'Şifre kurtarma şu anda kullanılamıyor. Daha sonra yeniden dene.' : 'İstek gönderilemedi. Bağlantını kontrol edip yeniden dene.'); }
    finally { setMesgul(false); }
  }
  return <SettingsPage baslik="Şifremi unuttum">
    <Txt role="body">E-posta adresine 30 dakika geçerli bir şifre yenileme bağlantısı göndereceğiz.</Txt>
    {hata ? <InfoStrip variant="warning" icon="info" metin={hata} /> : null}
    {bitti ? <InfoStrip variant="info" icon="info" metin="Bu e-posta ile bir hesabın varsa şifre yenileme bağlantısı gönderilecek. Gelen kutunu ve spam klasörünü kontrol et." /> : <>
      <TextField label="E-posta" value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" autoComplete="email" />
      <Button label="Bağlantı gönder" variant="primary" loading={mesgul} disabled={!email.trim()} onPress={() => void gonder()} />
    </>}
  </SettingsPage>;
}
