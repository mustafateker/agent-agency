import { router } from 'expo-router';
import { useCallback } from 'react';

import { Button } from '@/components/Button';
import { Card, LoadState, RevScreen, useRevLoad } from '@/components/RevScreen';
import { Txt } from '@/components/Txt';
import { oturumOku } from '@/lib/oturumDeposu';

export default function ProfilEkrani() {
  const oturum = useRevLoad(useCallback(oturumOku, []));

  return (
    <RevScreen title="Profil" tab="profil">
      <LoadState {...oturum} />
      {!oturum.loading && !oturum.error ? (
        <>
          <Card>
            <Txt role="h2">Hesabın</Txt>
            <Txt role="body">{oturum.data?.email ?? 'Oturum bilgisi bulunamadı'}</Txt>
            <Txt role="caption">Hesap, güvenlik, çıkış ve hesap silme işlemlerini ayarlardan yönetebilirsin.</Txt>
            <Button variant="secondary" label="Hesap ve uygulama ayarları" onPress={() => router.push('/ayarlar')} />
          </Card>
          <Card>
            <Txt role="h2">Planın</Txt>
            <Button variant="secondary" label="Maaş ve bütçem" onPress={() => router.push('/butce')} />
            <Button variant="secondary" label="Günlük ve kategori limitleri" onPress={() => router.push('/limitler')} />
            <Button variant="secondary" label="Rutinlerim" onPress={() => router.push('/rutinler')} />
            <Button variant="secondary" label="Favorilerim" onPress={() => router.push('/favoriler')} />
          </Card>
          <Card>
            <Txt role="h2">Analiz</Txt>
            <Button variant="secondary" label="Aylık özeti aç" onPress={() => router.push('/ozet')} />
          </Card>
        </>
      ) : null}
    </RevScreen>
  );
}
