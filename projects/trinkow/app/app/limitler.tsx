import { router } from 'expo-router';
import { useEffect, useState } from 'react';
import { Button } from '@/components/Button';
import { CategoryPicker } from '@/components/CategoryPicker';
import { MoneyInput } from '@/components/MoneyInput';
import { Card, LoadState, RevScreen, money, useRevLoad } from '@/components/RevScreen';
import { Txt } from '@/components/Txt';
import { kategori as kategoriGetir, type KategoriKodu } from '@/lib/kategoriler';
import { kurustanTutarGirisi, tutarGirisindenKurus } from '@/lib/para';
import { budgetBody, budgetGet, budgetPut } from '@/lib/revApi';
import { veriDegisti } from '@/lib/veriBus';

export default function Limitler() {
  const load = useRevLoad(budgetGet);
  const [mode, setMode] = useState<'otomatik'|'manuel'>('otomatik');
  const [amount, setAmount] = useState('');
  const [cats, setCats] = useState<Record<string,string>>({});
  const [cat, setCat] = useState<KategoriKodu|null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  useEffect(() => {
    const b=load.data?.butce; if(!b)return;
    setMode(b.limit_modu); setAmount(b.manuel_limit_kurus==null?'':kurustanTutarGirisi(b.manuel_limit_kurus));
    setCats(Object.fromEntries(Object.entries(b.kategori_limitleri).map(([k,v])=>[k,kurustanTutarGirisi(v)])));
  }, [load.data]);
  const b=load.data?.butce;
  const total=Object.values(cats).reduce((a,v)=>a+tutarGirisindenKurus(v),0);
  const limit=mode==='manuel'?tutarGirisindenKurus(amount):b?.gunluk_gelir_payi_kurus??null;
  async function save(){
    if(!b||busy)return; setBusy(true); setMessage('');
    try { const result=await budgetPut({...budgetBody(b),limit_modu:mode,manuel_limit_kurus:mode==='manuel'?tutarGirisindenKurus(amount):null,kategori_limitleri:Object.fromEntries(Object.entries(cats).map(([k,v])=>[k,tutarGirisindenKurus(v)]))}); load.setData(result); veriDegisti(); setMessage('Limitler bugünden itibaren kaydedildi.'); }
    catch { setMessage('Kaydedilemedi. Kategori toplamı günlük limiti aşmamalı.'); }
    finally { setBusy(false); }
  }
  return <RevScreen title="Limitler">
    <LoadState {...load}/>
    {load.data&&!b?<Card><Txt role="h2">Önce bütçeni oluştur</Txt><Txt role="body">Günlük limit için maaş veya manuel tutar bilgisi gerekli.</Txt><Button variant="primary" label="Bütçeme git" onPress={()=>router.replace('/butce')}/></Card>:null}
    {b?<>
      <Txt role="body">Düzenleme bugün ve sonraki günlere uygulanır. Önceki günler değişmez.</Txt>
      <Card><Button variant={mode==='otomatik'?'primary':'secondary'} label="Maaşa göre otomatik" onPress={()=>setMode('otomatik')}/><Button variant={mode==='manuel'?'primary':'secondary'} label="Günlük limiti ben belirleyeceğim" onPress={()=>setMode('manuel')}/>{mode==='manuel'?<MoneyInput label="Günlük limit · ₺" value={amount} onChangeText={setAmount}/>:<Txt role="body">Gelirine göre günlük pay: {money(b.gunluk_gelir_payi_kurus)}</Txt>}</Card>
      <Card><Txt role="h2">Kategori payları</Txt><Txt role="body">Bu paylar günlük limitin içindedir. Dağıtılmayan tutarı diğer harcamalarda kullanabilirsin.</Txt>
        {Object.entries(cats).map(([k,v])=><Card key={k}><MoneyInput label={`${kategoriGetir(k).ad} · günlük ₺`} value={v} onChangeText={n=>setCats(old=>({...old,[k]:n}))}/><Button variant="ghost" label="Payı kaldır" onPress={()=>setCats(old=>{const next={...old};delete next[k];return next;})}/></Card>)}
        <CategoryPicker value={cat} onChange={setCat}/><Button variant="secondary" label="Kategori payı ekle" disabled={!cat} onPress={()=>{if(cat)setCats(old=>({...old,[cat]:old[cat]||''}));setCat(null);}}/><Txt role="body">Kategori toplamı: {money(total)}</Txt><Txt role="body">Dağıtılmamış: {money(limit==null?null:limit-total)}</Txt>
      </Card>
      {load.data?.eski_aylik_kategori_limitleri.length?<Txt role="caption">Önceki aylık kategori limitlerin arşivlendi; günlük tutara çevrilmedi.</Txt>:null}
      {message?<Txt role="body" accessibilityLiveRegion="polite">{message}</Txt>:null}
      <Button variant="primary" label="Limitleri kaydet" loading={busy} disabled={limit==null||limit<=0||total>limit} onPress={()=>void save()}/>
    </>:null}
  </RevScreen>;
}
