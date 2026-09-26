import { router } from 'expo-router';
import { useEffect, useState } from 'react';
import { Button } from '@/components/Button';
import { MoneyInput } from '@/components/MoneyInput';
import { Card, LoadState, RevScreen, money, useRevLoad } from '@/components/RevScreen';
import { Txt } from '@/components/Txt';
import { kurustanTutarGirisi, tutarGirisindenKurus } from '@/lib/para';
import { budgetBody, budgetGet, budgetPut, emptyBudget, type BudgetInput } from '@/lib/revApi';
import { veriDegisti } from '@/lib/veriBus';

type Alan = 'gelir'|'kira'|'fatura'|'ulasim'|'kredi'|'hedef'|'borc';
const alanlar: [Alan,string][] = [['gelir','Aylık gelir · ₺'],['kira','Kira · ₺'],['fatura','Faturalar · ₺'],['ulasim','Zorunlu ulaşım · ₺'],['kredi','Aylık kredi ödemesi · ₺'],['hedef','Aylık hedef birikim · ₺'],['borc','Kalan toplam borç · ₺']];

export default function Butce() {
  const load = useRevLoad(budgetGet);
  const [fields,setFields] = useState<Record<Alan,string>>({gelir:'',kira:'',fatura:'',ulasim:'',kredi:'',hedef:'',borc:''});
  const [busy,setBusy] = useState(false); const [message,setMessage] = useState('');
  useEffect(()=>{ const b=load.data?.butce; if(!b)return; setFields({gelir:b.gelir_kurus==null?'':kurustanTutarGirisi(b.gelir_kurus),borc:b.borc_kurus==null?'':kurustanTutarGirisi(b.borc_kurus),hedef:kurustanTutarGirisi(b.hedef_birikim_kurus),kira:kurustanTutarGirisi(b.sabit_giderler.kira),fatura:kurustanTutarGirisi(b.sabit_giderler.fatura),ulasim:kurustanTutarGirisi(b.sabit_giderler.ulasim),kredi:kurustanTutarGirisi(b.sabit_giderler.kredi)}); },[load.data]);
  async function save(){ if(busy)return; setBusy(true);setMessage(''); try { const base=budgetBody(load.data?.butce??null); const body:BudgetInput={...base,gelir_kurus:fields.gelir?tutarGirisindenKurus(fields.gelir):null,borc_kurus:fields.borc?tutarGirisindenKurus(fields.borc):null,hedef_birikim_kurus:tutarGirisindenKurus(fields.hedef),sabit_giderler:{kira:tutarGirisindenKurus(fields.kira),fatura:tutarGirisindenKurus(fields.fatura),ulasim:tutarGirisindenKurus(fields.ulasim),kredi:tutarGirisindenKurus(fields.kredi)}}; const result=await budgetPut(body);load.setData(result);veriDegisti();setMessage('Bütçen bugünden itibaren güncellendi.'); } catch {setMessage('Kaydedilemedi. Geliri ve kategori paylarını kontrol et.');} finally {setBusy(false);} }
  const b=load.data?.butce;
  return <RevScreen title="Bütçem"><LoadState {...load}/>{load.data&&!load.loading&&!load.error?<><Txt role="body">Değişiklikler bugünden itibaren geçerli olur; geçmiş günlerin hesabı değişmez.</Txt><Card>{alanlar.map(([key,label])=><MoneyInput key={key} label={label} value={fields[key]} onChangeText={value=>setFields(old=>({...old,[key]:value}))}/>) }<Txt role="caption">Gelir veya borç bilinmiyorsa boş bırakabilirsin. Hedef birikim, gerçekleşmiş birikim sayılmaz.</Txt></Card><Card><Txt role="h2">Otomatik günlük limit</Txt><Txt role="h1">{money(b?.gunluk_limit_kurus)}</Txt>{b?.butce_acigi_kurus?<Txt role="body">Aylık bütçe açığı: {money(b.butce_acigi_kurus)}</Txt>:null}<Txt role="caption">Gelir − sabit ödemeler − hedef birikim, ayın günlerine dağıtılır.</Txt></Card>{message?<Txt role="body" accessibilityLiveRegion="polite">{message}</Txt>:null}<Button variant="primary" label={b?'Kaydet':'Bütçemi oluştur'} loading={busy} onPress={()=>void save()}/><Button variant="secondary" label="Günlük ve kategori limitleri" disabled={!b} onPress={()=>router.push('/limitler')}/><Button variant="secondary" label="Rutinlerim" onPress={()=>router.push('/rutinler')}/></>:null}</RevScreen>;
}
