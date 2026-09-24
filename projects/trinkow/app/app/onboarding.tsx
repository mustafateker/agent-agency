import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useState } from 'react';

import { Button } from '@/components/Button';
import { MoneyInput } from '@/components/MoneyInput';
import { Card, RevScreen, money } from '@/components/RevScreen';
import { Txt } from '@/components/Txt';
import { onboardingKaydet, type Niyet } from '@/db/profil';
import { tutarGirisindenKurus } from '@/lib/para';
import { budgetPut, emptyBudget } from '@/lib/revApi';
import { veriDegisti } from '@/lib/veriBus';
import { RoutinePanel } from './rutinler';

type Alan = 'gelir' | 'kira' | 'fatura' | 'ulasim' | 'kredi' | 'hedef' | 'borc';
const alanlar: [Alan, string][] = [
  ['gelir', 'Aylık net maaş · ₺'], ['kira', 'Kira / aidat · ₺'],
  ['fatura', 'Sabit faturalar · ₺'], ['ulasim', 'Zorunlu ulaşım · ₺'],
  ['kredi', 'Kredi ödemeleri · ₺'], ['hedef', 'Aylık hedef birikim · ₺'],
  ['borc', 'Kalan toplam borç (isteğe bağlı) · ₺'],
];

export default function Onboarding() {
  const db = useSQLiteContext();
  const [adim, setAdim] = useState(1);
  const [niyet, setNiyet] = useState<Niyet>('tasarruf');
  const [degerler, setDegerler] = useState<Record<Alan, string>>({ gelir:'', kira:'', fatura:'', ulasim:'', kredi:'', hedef:'', borc:'' });
  const [kayitliLimit, setKayitliLimit] = useState<number | null>(null);
  const [mesgul, setMesgul] = useState(false);
  const [hata, setHata] = useState('');

  async function butceyiKaydet() {
    if (!degerler.gelir || mesgul) return;
    setMesgul(true); setHata('');
    try {
      const temel = emptyBudget();
      const sonuc = await budgetPut({ ...temel,
        gelir_kurus: tutarGirisindenKurus(degerler.gelir),
        sabit_giderler: { kira:tutarGirisindenKurus(degerler.kira), fatura:tutarGirisindenKurus(degerler.fatura), ulasim:tutarGirisindenKurus(degerler.ulasim), kredi:tutarGirisindenKurus(degerler.kredi) },
        hedef_birikim_kurus: tutarGirisindenKurus(degerler.hedef),
        borc_kurus: degerler.borc ? tutarGirisindenKurus(degerler.borc) : null,
      });
      setKayitliLimit(sonuc.butce?.gunluk_limit_kurus ?? null);
      setAdim(3);
    } catch { setHata('Bütçe kaydedilemedi. Maaş ve sabit ödemeleri kontrol edip yeniden dene.'); }
    finally { setMesgul(false); }
  }

  async function bitir() {
    if (mesgul) return;
    setMesgul(true); setHata('');
    try {
      await onboardingKaydet(db, { niyet, gelirKurus:tutarGirisindenKurus(degerler.gelir), maasGunu:null, maasDuzensiz:true, gunlukLimitOnerisiKurus:null });
      veriDegisti(); setAdim(4);
    } catch { setHata('Kurulum tamamlanamadı. Yeniden deneyebilirsin.'); }
    finally { setMesgul(false); }
  }

  return <RevScreen title={`Kurulum · ${adim}/4`}>
    {adim === 1 ? <>
      <Txt role="h2">Amacın ne?</Txt><Txt role="body">Bunu motivasyon metinlerini sana uygun göstermek için kullanacağız.</Txt>
      {([['takip','Harcamalarımı görmek'],['tasarruf','Tasarruf etmek'],['borc','Borcumu azaltmak']] as [Niyet,string][]).map(([k,etiket]) => <Button key={k} variant={niyet===k?'primary':'secondary'} label={etiket} onPress={()=>setNiyet(k)} />)}
      <Button variant="primary" label="Sonraki" onPress={()=>setAdim(2)} />
    </> : null}
    {adim === 2 ? <>
      <Txt role="h2">Maaş ve aylık plan</Txt><Txt role="body">Otomatik günlük limit, maaşından sabit ödemeler ve hedef birikim çıkarılıp ayın günlerine bölünerek hesaplanır.</Txt>
      <Card>{alanlar.map(([alan, etiket]) => <MoneyInput key={alan} label={etiket} value={degerler[alan]} onChangeText={v=>setDegerler(d=>({...d,[alan]:v}))} />)}</Card>
      <Button variant="primary" label="Sonraki" loading={mesgul} disabled={tutarGirisindenKurus(degerler.gelir)<=0} onPress={()=>void butceyiKaydet()} /><Button variant="ghost" label="Geri" onPress={()=>setAdim(1)} />
    </> : null}
    {adim === 3 ? <>
      <Txt role="h2">Günlük rutinlerin</Txt><Txt role="body">Rutinlerini ad, kategori, günlük adet ve fiyat bilgisiyle ekleyebilirsin.</Txt><RoutinePanel onboarding />
      <Button variant="primary" label="Plan özetine geç" loading={mesgul} onPress={()=>void bitir()} /><Button variant="ghost" label="Rutinim yok, devam et" disabled={mesgul} onPress={()=>void bitir()} /><Button variant="ghost" label="Gelir planına dön" onPress={()=>setAdim(2)} />
    </> : null}
    {adim === 4 ? <>
      <Txt role="h2">Planın hazır</Txt><Card><Txt role="body">Amaç: {niyet === 'borc' ? 'Borcumu azaltmak' : niyet === 'tasarruf' ? 'Tasarruf etmek' : 'Harcamalarımı görmek'}</Txt><Txt role="body">Aylık maaş: {money(tutarGirisindenKurus(degerler.gelir))}</Txt><Txt role="h2">Günlük limit: {money(kayitliLimit)}</Txt><Txt role="caption">Bu değeri Ayarlar → Limitler bölümünden değiştirebilir veya maaşa göre otomatiğe dönebilirsin.</Txt></Card>
      <Button variant="primary" label="Trinkow’u kullanmaya başla" onPress={()=>router.replace('/')} />
    </> : null}
    {hata ? <Txt role="body" accessibilityLiveRegion="polite">{hata}</Txt> : null}
  </RevScreen>;
}
