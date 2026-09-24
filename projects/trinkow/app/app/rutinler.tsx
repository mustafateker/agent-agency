import { router } from 'expo-router';
import { useState } from 'react';
import { View } from 'react-native';

import { Button } from '@/components/Button';
import { CategoryPicker } from '@/components/CategoryPicker';
import { MoneyInput } from '@/components/MoneyInput';
import { Card, LoadState, RevScreen, money, useRevLoad } from '@/components/RevScreen';
import { TextField } from '@/components/TextField';
import { Txt } from '@/components/Txt';
import { kategori as kategoriGetir, type KategoriKodu } from '@/lib/kategoriler';
import { kurustanTutarGirisi, tutarGirisindenKurus } from '@/lib/para';
import { routinePut, routineSkip, routinesGet, yeniId, type Routine } from '@/lib/revApi';
import { veriDegisti } from '@/lib/veriBus';

const HAZIR_RUTINLER: [string, KategoriKodu][] = [
  ['Kahve', 'kafe'],
  ['Sigara', 'aliskanliklar'],
  ['Yemek', 'restoran'],
  ['Ulaşım', 'ulasim'],
  ['Atıştırmalık', 'market'],
];

export function RoutinePanel({ onboarding = false }: { onboarding?: boolean }) {
  const load = useRevLoad(routinesGet);
  const [ad, setAd] = useState('');
  const [amount, setAmount] = useState('');
  const [count, setCount] = useState('1');
  const [cat, setCat] = useState<KategoriKodu | null>(null);
  const [id, setId] = useState(yeniId);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [skip, setSkip] = useState<Record<string, string>>({});

  function edit(rutin: Routine) {
    setId(rutin.id);
    setAd(rutin.ad);
    setCat(rutin.kategori as KategoriKodu);
    setAmount(kurustanTutarGirisi(rutin.birim_fiyat_kurus));
    setCount(String(rutin.gunluk_adet));
  }

  function clear() {
    setId(yeniId());
    setAd('');
    setCat(null);
    setAmount('');
    setCount('1');
  }

  async function run(fn: () => Promise<unknown>, success = 'Kaydedildi.') {
    if (busy) return;
    setBusy(true);
    setMessage('');
    try {
      await fn();
      veriDegisti();
      await load.reload();
      setMessage(success);
    } catch {
      setMessage('İşlem tamamlanamadı. Bilgileri kontrol edip yeniden dene.');
    } finally {
      setBusy(false);
    }
  }

  const active = load.data?.rutinler.filter((rutin) => rutin.aktif) ?? [];
  const duzenleniyor = active.some((rutin) => rutin.id === id);

  return (
    <>
      <LoadState {...load} />
      {!onboarding ? (
        <>
          <Txt role="body">Günlük rutinlerini seç, kendi adet ve fiyatını yaz. Birden fazla rutin ekleyebilirsin.</Txt>
          <View style={{ gap: 12 }}>
            {HAZIR_RUTINLER.map(([name, kategori]) => (
              <Button
                key={name}
                variant="secondary"
                label={`${active.some((rutin) => rutin.ad === name) ? 'Seçili · ' : ''}${name}`}
                onPress={() => {
                  const existing = active.find((rutin) => rutin.ad === name);
                  if (existing) edit(existing);
                  else {
                    clear();
                    setAd(name);
                    setCat(kategori);
                  }
                }}
              />
            ))}
            <Button variant="ghost" label="Kendim ekleyeyim" onPress={clear} />
          </View>
        </>
      ) : null}

      <Card>
        <Txt role="h2">{duzenleniyor ? 'Rutini düzenle' : 'Rutin ekle'}</Txt>
        <TextField label="Harcamanın adı" value={ad} onChangeText={setAd} />
        <CategoryPicker value={cat} onChange={setCat} />
        <TextField
          label="Günlük adet"
          value={count}
          onChangeText={(value) => setCount(value.replace(/\D/g, ''))}
          keyboardType="number-pad"
        />
        <MoneyInput label="Birim fiyat · ₺" value={amount} onChangeText={setAmount} />
        <Button
          variant="primary"
          label={duzenleniyor ? 'Değişiklikleri kaydet' : 'Rutini kaydet'}
          loading={busy}
          disabled={!ad.trim() || !cat || Number(count) <= 0 || !Number.isSafeInteger(Number(count)) || tutarGirisindenKurus(amount) <= 0}
          onPress={() => void run(async () => {
            await routinePut({
              id,
              ad: ad.trim(),
              kategori: cat!,
              gunluk_adet: Number(count),
              birim_fiyat_kurus: tutarGirisindenKurus(amount),
              aktif: true,
            });
            clear();
          })}
        />
      </Card>

      {message ? <Txt role="body" accessibilityLiveRegion="polite">{message}</Txt> : null}

      {active.map((rutin) => (
        <Card key={rutin.id}>
          <Txt role="h2">{rutin.ad}</Txt>
          <Txt role="body">{kategoriGetir(rutin.kategori).ad} · Günde {rutin.gunluk_adet} × {money(rutin.birim_fiyat_kurus)}</Txt>
          {!onboarding ? (
            <>
              <Button
                variant="secondary"
                label="+ Harcama ekle"
                onPress={() => router.push({
                  pathname: '/harcama-ekle',
                  params: {
                    kategori: rutin.kategori,
                    ad: rutin.ad,
                    tutarKurus: String(rutin.birim_fiyat_kurus),
                    rutinId: rutin.id,
                  },
                })}
              />
              <TextField
                label="Bugün vazgeçtiğim adet"
                value={skip[rutin.id] ?? '1'}
                keyboardType="number-pad"
                onChangeText={(value) => setSkip((old) => ({ ...old, [rutin.id]: value.replace(/\D/g, '') }))}
              />
              <Button
                variant="secondary"
                label="Bugün almadım"
                disabled={busy || Number(skip[rutin.id] ?? 1) <= 0}
                onPress={() => void run(
                  () => routineSkip(rutin.id, Number(skip[rutin.id] ?? 1)),
                  'Bugünkü vazgeçişin kaydedildi. Bu işlem birikim hesabına para eklemez.',
                )}
              />
              <Button
                variant="ghost"
                label="Bugünkü vazgeçişi geri al"
                disabled={busy}
                onPress={() => void run(() => routineSkip(rutin.id, 0))}
              />
            </>
          ) : null}
          <Button variant="ghost" label="Düzenle" onPress={() => edit(rutin)} />
          <Button
            variant="ghost"
            label="Rutini kaldır"
            disabled={busy}
            onPress={() => void run(() => routinePut({ ...rutin, aktif: false }))}
          />
        </Card>
      ))}

      {!onboarding ? (
        <Txt role="caption">Rutin değişiklikleri bugünden itibaren geçerlidir. Harcama girmemek otomatik tasarruf sayılmaz.</Txt>
      ) : null}
    </>
  );
}

export default function Rutinler() {
  return <RevScreen title="Rutinlerim"><RoutinePanel /></RevScreen>;
}
