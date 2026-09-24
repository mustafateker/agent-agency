import { router, useFocusEffect } from 'expo-router';
import { useCallback, useEffect, useState, type ReactNode } from 'react';
import { Keyboard, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button } from '@/components/Button';
import { Txt } from '@/components/Txt';
import { TabBar, type TabKey } from '@/components/TabBar';
import { clay,color,radius,layout } from '@/theme/tokens';
import { paraYaz } from '@/lib/para';
export const money = (n:number|null|undefined) => n == null ? 'Henüz bilinmiyor' : paraYaz(n,true);
export function Card({children}:{children:ReactNode}) { return <View style={s.card}>{children}</View>; }
export function RevScreen({title,children,tab}:{title:string;children:ReactNode;tab?:TabKey}) {
  const i=useSafeAreaInsets();
  const [klavyeAcik, setKlavyeAcik] = useState(false);

  useEffect(() => {
    const acildi = Keyboard.addListener(Platform.OS === 'ios' ? 'keyboardWillShow' : 'keyboardDidShow', () => setKlavyeAcik(true));
    const kapandi = Keyboard.addListener(Platform.OS === 'ios' ? 'keyboardWillHide' : 'keyboardDidHide', () => setKlavyeAcik(false));
    return () => { acildi.remove(); kapandi.remove(); };
  }, []);

  return <KeyboardAvoidingView
    style={[s.screen,{paddingTop:i.top,paddingBottom:i.bottom}]}
    behavior={Platform.OS==='ios'?'padding':'height'}>
    <View style={s.header}>
      {tab ? null : <Button auto variant="ghost" label="Geri" onPress={()=>router.canGoBack()?router.back():router.replace('/')} />}
      <Txt role="h1" style={{flex:1}}>{title}</Txt>
      {tab ? null : <Button auto variant="ghost" label="Ayarlar" onPress={()=>router.push('/ayarlar')}/>}
    </View>
    <ScrollView style={s.scroll} keyboardShouldPersistTaps="handled" contentContainerStyle={s.content}>{children}</ScrollView>
    {tab && !klavyeAcik ? <View style={s.tabAlani}>
      <TabBar active={tab} onSelect={k=>router.replace(k==='gunluk'?'/':k==='tasarruflar'?'/tasarruflar':'/profil')} onAdd={()=>router.push('/harcama-ekle')}/>
    </View>:null}
  </KeyboardAvoidingView>;
}
export function useRevLoad<T>(fetcher:()=>Promise<T>) { const [data,setData]=useState<T|null>(null),[error,setError]=useState(''),[loading,setLoading]=useState(true);const reload=useCallback(async()=>{setLoading(true);setError('');try{setData(await fetcher());}catch{setError('Bilgiler yüklenemedi. Bağlantını kontrol edip yeniden deneyebilirsin.');}finally{setLoading(false);}},[fetcher]);useFocusEffect(useCallback(()=>{void reload();},[reload]));return {data,error,loading,reload,setData}; }
export function LoadState({loading,error,reload}:{loading:boolean;error:string;reload:()=>void}) { return loading?<Txt role="body">Yükleniyor…</Txt>:error?<Card><Txt role="body">{error}</Txt><Button variant="secondary" label="Yeniden dene" onPress={reload}/></Card>:null; }
export const s=StyleSheet.create({screen:{flex:1,backgroundColor:color.bg},header:{flexDirection:'row',alignItems:'center',paddingHorizontal:12,gap:8,paddingBottom:12},scroll:{flex:1,minHeight:0},content:{padding:layout.screenPaddingX,gap:24,paddingBottom:32},tabAlani:{paddingHorizontal:layout.screenPaddingX,paddingBottom:layout.tabBarLift},card:{padding:24,borderRadius:radius.card,backgroundColor:color.surface,boxShadow:clay.raised,gap:12},row:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',gap:12}});
