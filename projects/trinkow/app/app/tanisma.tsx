import { router, useLocalSearchParams } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button } from '@/components/Button';
import { ClayKeypad } from '@/components/ClayKeypad';
import { ClayPressable } from '@/components/ClayPressable';
import { ClaySurface } from '@/components/ClaySurface';
import { ErrorState } from '@/components/ErrorState';
import { FrequencyChips, siklikEtiketi } from '@/components/FrequencyChips';
import type { IconName } from '@/components/Icon';
import { IconButton } from '@/components/IconButton';
import { InfoStrip } from '@/components/InfoStrip';
import { MirrorWell } from '@/components/MirrorWell';
import { NeutralIconBox } from '@/components/NeutralIconBox';
import { ProgressBar } from '@/components/ProgressBar';
import { Skeleton } from '@/components/Skeleton';
import { Slider } from '@/components/Slider';
import { Txt } from '@/components/Txt';
import { ValueWell } from '@/components/ValueWell';
import {
  a11yTanKart,
  abonelikFormulMetni,
  planAralikEnCok,
  t,
  tanBirikimHedef,
  tanBirikimUstSinirNotu,
  tanDonusAciklama,
  tanFormulMetni,
  tanGundeKac,
} from '@/content/metinler';
import {
  DETAY_VARSAYILAN,
  profilDetayAlanKaydet,
  profilDetayOku,
  profilOku,
  sonKartKaydet,
  aliskanlikSatiriKurus,
  abonelikSatiriKurus,
  type AliskanlikCevabi,
  type ProfilDetay,
  type ProfilDetayKolonu,
} from '@/db/profil';
import { birikimYuzdeUstSiniri, zorunluKurus, zorunluYuzdeYuvarlanmis, type Siklik, type YatirimNiyet } from '@/lib/plan';
import { paraYaz, tutarGirisiEkle, tutarGirisindenKurus, tutarGirisiSil, tutarGosterimi, kurustanTutarGirisi } from '@/lib/para';
import { clay, color, layout, radius, rhythm } from '@/theme/tokens';

type HabitKey = 'kahve' | 'sigara' | 'alkol' | 'yemek';
type Asama = 'yukleniyor' | 'kapi' | 'donus' | number;

/** Sabit + habit + abonelik editörünün ele aldığı alanlar — para (kuruş) ya da sayı (adet/serbest). */
type AlanId =
  | 'sabit.kira'
  | 'sabit.fatura'
  | 'sabit.ulasim'
  | 'sabit.kredi'
  | 'kahve.fiyat'
  | 'kahve.serbest'
  | 'sigara.fiyat'
  | 'sigara.serbest'
  | 'alkol.fiyat'
  | 'alkol.serbest'
  | 'yemek.fiyat'
  | 'yemek.serbest'
  | 'abonelik.adet'
  | 'abonelik.ortalama';

const SAYI_ALANLARI = new Set<AlanId>(['kahve.serbest', 'sigara.serbest', 'alkol.serbest', 'yemek.serbest', 'abonelik.adet']);

const KOLON: Record<AlanId, ProfilDetayKolonu> = {
  'sabit.kira': 'kira_aidat_kurus',
  'sabit.fatura': 'faturalar_kurus',
  'sabit.ulasim': 'ulasim_yakit_kurus',
  'sabit.kredi': 'kredi_taksit_kurus',
  'kahve.fiyat': 'kahve_fiyat_kurus',
  'kahve.serbest': 'kahve_serbest_sayi',
  'sigara.fiyat': 'sigara_fiyat_kurus',
  'sigara.serbest': 'sigara_serbest_sayi',
  'alkol.fiyat': 'alkol_fiyat_kurus',
  'alkol.serbest': 'alkol_serbest_sayi',
  'yemek.fiyat': 'yemek_fiyat_kurus',
  'yemek.serbest': 'yemek_serbest_sayi',
  'abonelik.adet': 'abonelik_adet',
  'abonelik.ortalama': 'abonelik_ortalama_kurus',
};

const KOLON_SIKLIK: Record<HabitKey, ProfilDetayKolonu> = {
  kahve: 'kahve_siklik',
  sigara: 'sigara_siklik',
  alkol: 'alkol_siklik',
  yemek: 'yemek_siklik',
};

const HABIT_META: Record<HabitKey, { icon: IconName; baslik: string; aciklama: string; fiyatEtiket: string; birim: string }> = {
  kahve: { icon: 'coffee', baslik: t['tan.kahve.baslik'], aciklama: t['tan.kahve.aciklama'], fiyatEtiket: t['tan.kahve.fiyat'], birim: t['tan.kahve.birim'] },
  // Sigara/alkol aynı kategori kabını (footprints — "Alışkanlıklar" ailesi) paylaşır: onaylı
  // sette özel bir sigara/alkol ikonu yok (§9 "yeni ikon eklenmedi"), prototip de sigara
  // kartında bilerek AYNI şekli kullanıyor (bkz. rapor).
  sigara: { icon: 'footprints', baslik: t['tan.sigara.baslik'], aciklama: t['tan.sigara.aciklama'], fiyatEtiket: t['tan.sigara.fiyat'], birim: t['tan.sigara.birim'] },
  alkol: { icon: 'footprints', baslik: t['tan.alkol.baslik'], aciklama: t['tan.alkol.aciklama'], fiyatEtiket: t['tan.alkol.fiyat'], birim: t['tan.alkol.birim'] },
  yemek: { icon: 'utensils', baslik: t['tan.yemek.baslik'], aciklama: t['tan.yemek.aciklama'], fiyatEtiket: t['tan.yemek.fiyat'], birim: t['tan.yemek.birim'] },
};

const KART_BASLIK: Record<number, string> = {
  1: t['tan.sabit.baslik'],
  2: t['tan.kahve.baslik'],
  3: t['tan.sigara.baslik'],
  4: t['tan.alkol.baslik'],
  5: t['tan.yemek.baslik'],
  6: t['tan.abonelik.baslik'],
  7: t['tan.yatirim.baslik'],
  8: t['tan.birikim.baslik'],
};

/** Sayı alanları için sade tamsayı tampon (para değil — virgül yok, 3 hane sınırı). */
function sayiEkle(buffer: string, d: string): string {
  const yeni = (buffer + d).replace(/^0+(?=\d)/, '');
  return yeni.length > 3 ? buffer : yeni;
}

export default function TanismaEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();
  const { kart: kartParam } = useLocalSearchParams<{ kart?: string }>();

  const [asama, setAsama] = useState<Asama>('yukleniyor');
  const [hata, setHata] = useState(false);
  const [detay, setDetay] = useState<ProfilDetay>(DETAY_VARSAYILAN);
  const [gelirKurus, setGelirKurus] = useState<number | null>(null);

  const [aktifAlan, setAktifAlan] = useState<AlanId | null>(null);
  const [buffer, setBuffer] = useState('');

  const yukle = useCallback(() => {
    let iptal = false;
    setHata(false);
    setAsama('yukleniyor');
    Promise.all([profilDetayOku(db), profilOku(db)])
      .then(([d, p]) => {
        if (iptal) return;
        setDetay(d);
        setGelirKurus(p.gelirKurus);
        const istenenKart = kartParam ? Number(kartParam) : null;
        if (istenenKart && istenenKart >= 1 && istenenKart <= 8) {
          setAsama(istenenKart);
        } else if (d.sonKart > 1 && !d.planKuruldu) {
          setAsama('donus');
        } else {
          setAsama('kapi');
        }
      })
      .catch(() => {
        if (!iptal) setHata(true);
      });
    return () => {
      iptal = true;
    };
    // `kartParam` yalnız ilk yüklemede okunur — sonraki gezinme ekranın kendi state'iyle yönetilir.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [db]);

  useEffect(() => yukle(), [yukle]);

  useEffect(() => {
    if (typeof asama === 'number') void sonKartKaydet(db, asama);
  }, [asama, db]);

  function alanTipi(id: AlanId): 'para' | 'sayi' {
    return SAYI_ALANLARI.has(id) ? 'sayi' : 'para';
  }

  function yazAlan(id: AlanId, deger: number | null) {
    setDetay((d) => {
      const nd: ProfilDetay = { ...d };
      switch (id) {
        case 'sabit.kira':
          nd.kiraAidatKurus = deger;
          break;
        case 'sabit.fatura':
          nd.faturalarKurus = deger;
          break;
        case 'sabit.ulasim':
          nd.ulasimYakitKurus = deger;
          break;
        case 'sabit.kredi':
          nd.krediTaksitKurus = deger;
          break;
        case 'kahve.fiyat':
          nd.kahve = { ...d.kahve, fiyatKurus: deger };
          break;
        case 'kahve.serbest':
          nd.kahve = { ...d.kahve, serbestSayi: deger };
          break;
        case 'sigara.fiyat':
          nd.sigara = { ...d.sigara, fiyatKurus: deger };
          break;
        case 'sigara.serbest':
          nd.sigara = { ...d.sigara, serbestSayi: deger };
          break;
        case 'alkol.fiyat':
          nd.alkol = { ...d.alkol, fiyatKurus: deger };
          break;
        case 'alkol.serbest':
          nd.alkol = { ...d.alkol, serbestSayi: deger };
          break;
        case 'yemek.fiyat':
          nd.yemek = { ...d.yemek, fiyatKurus: deger };
          break;
        case 'yemek.serbest':
          nd.yemek = { ...d.yemek, serbestSayi: deger };
          break;
        case 'abonelik.adet':
          nd.abonelikAdet = deger;
          break;
        case 'abonelik.ortalama':
          nd.abonelikOrtalamaKurus = deger;
          break;
      }
      return nd;
    });
    void profilDetayAlanKaydet(db, KOLON[id], deger);
  }

  /** Aktif alanı tamponundan kalıcıya yazar (RN inşa notu 4 — "Devam" beklemez). */
  function alaniKapat() {
    if (!aktifAlan) return;
    const tip = alanTipi(aktifAlan);
    const deger = buffer === '' ? null : tip === 'para' ? tutarGirisindenKurus(buffer) : Number(buffer);
    yazAlan(aktifAlan, deger);
    setAktifAlan(null);
    setBuffer('');
  }

  function alaniAc(id: AlanId, mevcut: number | null) {
    if (aktifAlan === id) {
      alaniKapat();
      return;
    }
    if (aktifAlan) alaniKapat();
    setAktifAlan(id);
    setBuffer(mevcut !== null ? (alanTipi(id) === 'para' ? kurustanTutarGirisi(mevcut) : String(mevcut)) : '');
  }

  function siklikSec(h: HabitKey, s: Siklik) {
    if (aktifAlan) alaniKapat();
    setDetay((d) => ({ ...d, [h]: { ...d[h], siklik: s } }));
    void profilDetayAlanKaydet(db, KOLON_SIKLIK[h], s);
  }

  function yatirimSec(v: YatirimNiyet) {
    setDetay((d) => ({ ...d, yatirimNiyet: v }));
    void profilDetayAlanKaydet(db, 'yatirim_niyet', v);
  }

  function birikimSec(yuzde: number) {
    setDetay((d) => ({ ...d, birikimYuzde: yuzde }));
    void profilDetayAlanKaydet(db, 'birikim_yuzde', yuzde);
  }

  function kartDolduMu(n: number, d: ProfilDetay): boolean {
    switch (n) {
      case 1:
        return d.kiraAidatKurus !== null || d.faturalarKurus !== null || d.ulasimYakitKurus !== null || d.krediTaksitKurus !== null;
      case 2:
        return d.kahve.siklik !== null;
      case 3:
        return d.sigara.siklik !== null;
      case 4:
        return d.alkol.siklik !== null;
      case 5:
        return d.yemek.siklik !== null;
      case 6:
        return d.abonelikAdet !== null || d.abonelikOrtalamaKurus !== null;
      case 7:
        return d.yatirimNiyet !== null;
      case 8:
        return d.birikimYuzde !== null;
      default:
        return false;
    }
  }

  async function kapat() {
    alaniKapat();
    router.replace('/');
  }

  function geri() {
    alaniKapat();
    if (asama === 'donus') {
      router.replace('/');
      return;
    }
    if (typeof asama === 'number') {
      if (asama === 1) setAsama('kapi');
      else setAsama(asama - 1);
    }
  }

  function basla() {
    setAsama(1);
  }

  function ileriGit() {
    alaniKapat();
    if (typeof asama !== 'number') return;
    if (asama >= 8) {
      router.push('/plan');
      return;
    }
    setAsama((asama + 1) as Asama);
  }

  const zorunlu = zorunluKurus({
    kiraAidatKurus: detay.kiraAidatKurus,
    faturalarKurus: detay.faturalarKurus,
    ulasimYakitKurus: detay.ulasimYakitKurus,
    krediTaksitKurus: detay.krediTaksitKurus,
  });
  const birikimMax = gelirKurus !== null && gelirKurus > 0 ? birikimYuzdeUstSiniri(gelirKurus, zorunlu) : 0;
  const zorunluYuzdeGosterim = gelirKurus && gelirKurus > 0 ? zorunluYuzdeYuvarlanmis(gelirKurus, zorunlu) : 0;

  if (hata) {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <View style={stil.pad}>
          <View style={{ height: rhythm.section }} />
          <ErrorState onRetry={yukle} />
        </View>
      </View>
    );
  }

  if (asama === 'yukleniyor') {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <View style={stil.pad}>
          <View style={{ height: rhythm.section }} />
          <Skeleton width="60%" height={28} />
          <View style={{ height: rhythm.group }} />
          <Skeleton width="100%" height={16} />
          <View style={{ height: rhythm.section }} />
          <Skeleton width="100%" height={220} borderRadius={radius.card} />
        </View>
      </View>
    );
  }

  const gosterKeypad = aktifAlan !== null;
  const devamAktif = typeof asama === 'number' ? kartDolduMu(asama, detay) : false;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <View style={stil.basSatiri}>
        <IconButton icon="chevron-left" accessibilityLabel={t['a11y.tan.geri']} onPress={geri} />
        <Txt role="micro" tone={color.text2}>
          {t['tan.baslik']}
        </Txt>
        {asama === 'donus' ? (
          <View style={stil.basDenge} />
        ) : (
          <IconButton icon="x" accessibilityLabel={t['a11y.tan.kapat']} onPress={() => void kapat()} />
        )}
      </View>

      <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
        <View style={{ height: rhythm.section }} />

        {asama === 'kapi' ? <KapiIcerik /> : null}
        {asama === 'donus' ? (
          <DonusIcerik detay={detay} kartDolduMu={(n) => kartDolduMu(n, detay)} onKartaGit={(n) => setAsama(n)} />
        ) : null}

        {typeof asama === 'number' ? (
          <>
            <ProgressBar mevcut={asama} toplam={8} accessibilityLabel={a11yTanKart(asama)} />
            <View style={{ height: rhythm.section }} />

            {asama === 1 ? (
              <SabitCard detay={detay} aktifAlan={aktifAlan} buffer={buffer} onAc={alaniAc} />
            ) : null}
            {asama === 2 ? <HabitCard k="kahve" cevap={detay.kahve} aktifAlan={aktifAlan} buffer={buffer} onSiklik={siklikSec} onAc={alaniAc} /> : null}
            {asama === 3 ? <HabitCard k="sigara" cevap={detay.sigara} aktifAlan={aktifAlan} buffer={buffer} onSiklik={siklikSec} onAc={alaniAc} /> : null}
            {asama === 4 ? <HabitCard k="alkol" cevap={detay.alkol} aktifAlan={aktifAlan} buffer={buffer} onSiklik={siklikSec} onAc={alaniAc} /> : null}
            {asama === 5 ? <HabitCard k="yemek" cevap={detay.yemek} aktifAlan={aktifAlan} buffer={buffer} onSiklik={siklikSec} onAc={alaniAc} /> : null}
            {asama === 6 ? <AbonelikCard detay={detay} aktifAlan={aktifAlan} buffer={buffer} onAc={alaniAc} /> : null}
            {asama === 7 ? <YatirimCard secili={detay.yatirimNiyet} onSec={yatirimSec} /> : null}
            {asama === 8 ? (
              <BirikimCard
                gelirKurus={gelirKurus}
                zorunluGiderKurus={zorunlu}
                zorunluYuzde={zorunluYuzdeGosterim}
                birikimYuzde={detay.birikimYuzde}
                max={birikimMax}
                onSec={birikimSec}
              />
            ) : null}
          </>
        ) : null}

        <View style={{ height: rhythm.section }} />
      </ScrollView>

      <View style={[stil.altSabit, { paddingBottom: insets.bottom }]}>
        {gosterKeypad ? (
          <>
            <View style={stil.pad}>
              <ClayKeypad
                onDigit={(d) =>
                  setBuffer((b) => (aktifAlan && alanTipi(aktifAlan) === 'sayi' ? sayiEkle(b, d) : tutarGirisiEkle(b, d)))
                }
                onComma={() => setBuffer((b) => (aktifAlan && alanTipi(aktifAlan) === 'sayi' ? b : tutarGirisiEkle(b, ',')))}
                onBackspace={() => setBuffer((b) => (aktifAlan && alanTipi(aktifAlan) === 'sayi' ? b.slice(0, -1) : tutarGirisiSil(b)))}
              />
            </View>
            <View style={{ height: rhythm.blockInCard }} />
            <View style={stil.pad}>
              <Button label={t['eylem.devam']} variant="secondary" onPress={alaniKapat} />
            </View>
          </>
        ) : asama === 'kapi' ? (
          <View style={stil.pad}>
            <Button label={t['ob.bitir']} variant="primary" onPress={basla} />
            <View style={{ height: rhythm.group }} />
            <Button label={t['eylem.simdi_degil']} variant="ghost" onPress={() => void kapat()} />
          </View>
        ) : asama === 'donus' ? (
          <View style={stil.pad}>
            <Button label={t['tan.donus.devam']} variant="primary" onPress={() => setAsama(detay.sonKart)} />
            <View style={{ height: rhythm.group }} />
            <Button label={t['tan.donus.plan']} variant="ghost" onPress={() => router.push('/plan')} />
          </View>
        ) : (
          <View style={stil.pad}>
            <Button label={asama === 8 ? t['tan.gor.plan'] : t['eylem.devam']} variant="primary" disabled={!devamAktif} onPress={ileriGit} />
            <View style={{ height: rhythm.group }} />
            <Button label={t['tan.atla']} variant="ghost" onPress={ileriGit} />
          </View>
        )}
      </View>
    </View>
  );
}

function KapiIcerik() {
  return (
    <>
      <Txt role="h1">{t['tan.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" tone={color.text2}>
        {t['tan.aciklama']}
      </Txt>
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
        <Txt role="label" tone={color.text2}>
          {t['tan.kapi.neler']}
        </Txt>
        <View style={{ height: rhythm.blockInCard }} />
        <KapiSatir icon="house" baslik={t['tan.sabit.baslik']} aciklama={t['plan.pay.zorunlu.alt']} />
        <View style={{ height: rhythm.blockInCard }} />
        <KapiSatir icon="coffee" baslik={t['tan.kapi.aliskanlik.baslik']} aciklama={t['tan.kapi.aliskanlik.alt']} />
        <View style={{ height: rhythm.blockInCard }} />
        <KapiSatir icon="target" baslik={t['tan.birikim.baslik']} aciklama={t['tan.kapi.birikim.alt']} />
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
      <InfoStrip variant="info" metin={`${t['tan.fiyat_vaadi']} ${t['tan.fiyat_vaadi.alt']}`} />
    </>
  );
}

function KapiSatir({ icon, baslik, aciklama }: { icon: IconName; baslik: string; aciklama: string }) {
  return (
    <View style={stil.satir}>
      <NeutralIconBox icon={icon} />
      <View style={{ width: rhythm.pad }} />
      <View style={stil.esnek}>
        <Txt role="bodyStrong">{baslik}</Txt>
        <View style={{ height: rhythm.sameObject }} />
        <Txt role="caption">{aciklama}</Txt>
      </View>
    </View>
  );
}

function DonusIcerik({
  detay,
  kartDolduMu,
  onKartaGit,
}: {
  detay: ProfilDetay;
  kartDolduMu: (n: number) => boolean;
  onKartaGit: (n: number) => void;
}) {
  const bekleyenler = [1, 2, 3, 4, 5, 6, 7, 8].filter((n) => !kartDolduMu(n));
  const cevaplanan = 8 - bekleyenler.length;
  return (
    <>
      <Txt role="h1">{t['tan.donus.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" tone={color.text2}>
        {tanDonusAciklama(cevaplanan, bekleyenler.length)}
      </Txt>
      <View style={{ height: rhythm.section }} />
      <ProgressBar mevcut={detay.sonKart} toplam={8} accessibilityLabel={t['tan.donus.baslik']} />
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
        <Txt role="label" tone={color.text2}>
          {t['tan.donus.bekleyen']}
        </Txt>
        <View style={{ height: rhythm.blockInCard }} />
        {bekleyenler.map((n, i) => (
          <View key={n}>
            {i > 0 ? <View style={{ height: rhythm.blockInCard }} /> : null}
            <ValueWell
              etiket={KART_BASLIK[n]}
              deger={t['tan.donus.cevaplanmadi']}
              degerSoluk
              accessibilityLabel={KART_BASLIK[n]}
              onPress={() => onKartaGit(n)}
            />
          </View>
        ))}
      </ClaySurface>
    </>
  );
}

function SabitCard({
  detay,
  aktifAlan,
  buffer,
  onAc,
}: {
  detay: ProfilDetay;
  aktifAlan: AlanId | null;
  buffer: string;
  onAc: (id: AlanId, mevcut: number | null) => void;
}) {
  const toplam = zorunluKurus({
    kiraAidatKurus: detay.kiraAidatKurus,
    faturalarKurus: detay.faturalarKurus,
    ulasimYakitKurus: detay.ulasimYakitKurus,
    krediTaksitKurus: detay.krediTaksitKurus,
  });
  const satirlar: [AlanId, string, number | null][] = [
    ['sabit.kira', t['tan.sabit.kira'], detay.kiraAidatKurus],
    ['sabit.fatura', t['tan.sabit.fatura'], detay.faturalarKurus],
    ['sabit.ulasim', t['tan.sabit.ulasim'], detay.ulasimYakitKurus],
    ['sabit.kredi', t['tan.sabit.kredi'], detay.krediTaksitKurus],
  ];
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
      <View style={stil.satir}>
        <NeutralIconBox icon="house" />
        <View style={{ width: rhythm.pad }} />
        <Txt role="h2" style={stil.esnek}>
          {t['tan.sabit.baslik']}
        </Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{t['tan.sabit.aciklama']}</Txt>
      <View style={{ height: rhythm.pad }} />
      {satirlar.map(([id, etiket, deger], i) => {
        const odakli = aktifAlan === id;
        return (
          <View key={id}>
            {i > 0 ? <View style={{ height: rhythm.blockInCard }} /> : null}
            <ValueWell
              etiket={etiket}
              deger={odakli ? tutarGosterimi(buffer) : deger !== null ? paraYaz(deger) : t['tan.girilmedi']}
              degerSoluk={!odakli && deger === null}
              focused={odakli}
              accessibilityLabel={etiket}
              onPress={() => onAc(id, deger)}
            />
          </View>
        );
      })}
      {toplam > 0 ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <View style={stil.aralikSatiri}>
            <Txt role="bodyStrong">{t['tan.sabit.toplam']}</Txt>
            <Txt role="amount">{paraYaz(toplam)}</Txt>
          </View>
        </>
      ) : null}
    </ClaySurface>
  );
}

function HabitCard({
  k,
  cevap,
  aktifAlan,
  buffer,
  onSiklik,
  onAc,
}: {
  k: HabitKey;
  cevap: AliskanlikCevabi;
  aktifAlan: AlanId | null;
  buffer: string;
  onSiklik: (h: HabitKey, s: Siklik) => void;
  onAc: (id: AlanId, mevcut: number | null) => void;
}) {
  const meta = HABIT_META[k];
  const fiyatId = `${k}.fiyat` as AlanId;
  const serbestId = `${k}.serbest` as AlanId;
  const fiyatOdakli = aktifAlan === fiyatId;
  const serbestOdakli = aktifAlan === serbestId;
  const gosterFiyat = cevap.siklik !== null && cevap.siklik !== 'hic';
  const aylik = aliskanlikSatiriKurus(cevap);

  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
      <View style={stil.satir}>
        <NeutralIconBox icon={meta.icon} />
        <View style={{ width: rhythm.pad }} />
        <Txt role="h2" style={stil.esnek}>
          {meta.baslik}
        </Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{meta.aciklama}</Txt>
      <View style={{ height: rhythm.pad }} />
      <Txt role="label" tone={color.text2}>
        {t['tan.siklik.etiket']}
      </Txt>
      <View style={{ height: rhythm.group }} />
      <FrequencyChips deger={cevap.siklik} onSecim={(s) => onSiklik(k, s)} />

      {cevap.siklik === 'serbest' ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <Txt role="label" tone={color.text2}>
            {tanGundeKac(meta.birim)}
          </Txt>
          <View style={{ height: rhythm.group }} />
          <ValueWell
            etiket={tanGundeKac(meta.birim)}
            deger={serbestOdakli ? buffer || '0' : cevap.serbestSayi !== null ? String(cevap.serbestSayi) : t['tan.girilmedi']}
            degerSoluk={!serbestOdakli && cevap.serbestSayi === null}
            focused={serbestOdakli}
            accessibilityLabel={tanGundeKac(meta.birim)}
            onPress={() => onAc(serbestId, cevap.serbestSayi)}
          />
        </>
      ) : null}

      {gosterFiyat ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <ValueWell
            etiket={meta.fiyatEtiket}
            deger={fiyatOdakli ? tutarGosterimi(buffer) : cevap.fiyatKurus !== null ? paraYaz(cevap.fiyatKurus) : t['tan.fiyat.bos']}
            degerSoluk={!fiyatOdakli && cevap.fiyatKurus === null}
            focused={fiyatOdakli}
            accessibilityLabel={meta.fiyatEtiket}
            onPress={() => onAc(fiyatId, cevap.fiyatKurus)}
          />
        </>
      ) : null}

      {gosterFiyat && aylik > 0 ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <MirrorWell
            baslik={t['tan.ayda']}
            tutarYazi={paraYaz(aylik)}
            formulYazi={tanFormulMetni(
              siklikEtiketi(cevap.siklik as Siklik),
              paraYaz(cevap.fiyatKurus ?? 0),
              cevap.siklik === 'hafta1' || cevap.siklik === 'hafta2_3',
              cevap.siklik === 'ay1_2',
            )}
          />
        </>
      ) : null}

      {cevap.siklik === 'hic' ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <InfoStrip variant="info" metin={t['tan.hic.not']} />
        </>
      ) : null}
    </ClaySurface>
  );
}

function AbonelikCard({
  detay,
  aktifAlan,
  buffer,
  onAc,
}: {
  detay: ProfilDetay;
  aktifAlan: AlanId | null;
  buffer: string;
  onAc: (id: AlanId, mevcut: number | null) => void;
}) {
  const adetOdakli = aktifAlan === 'abonelik.adet';
  const ortalamaOdakli = aktifAlan === 'abonelik.ortalama';
  const aylik = abonelikSatiriKurus(detay);
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
      <View style={stil.satir}>
        <NeutralIconBox icon="repeat" />
        <View style={{ width: rhythm.pad }} />
        <Txt role="h2" style={stil.esnek}>
          {t['tan.abonelik.baslik']}
        </Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{t['tan.abonelik.aciklama']}</Txt>
      <View style={{ height: rhythm.pad }} />
      <ValueWell
        etiket={t['tan.abonelik.adet']}
        deger={adetOdakli ? buffer || '0' : detay.abonelikAdet !== null ? String(detay.abonelikAdet) : t['tan.girilmedi']}
        degerSoluk={!adetOdakli && detay.abonelikAdet === null}
        focused={adetOdakli}
        accessibilityLabel={t['tan.abonelik.adet']}
        onPress={() => onAc('abonelik.adet', detay.abonelikAdet)}
      />
      <View style={{ height: rhythm.blockInCard }} />
      <ValueWell
        etiket={t['tan.abonelik.ortalama']}
        deger={ortalamaOdakli ? tutarGosterimi(buffer) : detay.abonelikOrtalamaKurus !== null ? paraYaz(detay.abonelikOrtalamaKurus) : t['tan.fiyat.bos']}
        degerSoluk={!ortalamaOdakli && detay.abonelikOrtalamaKurus === null}
        focused={ortalamaOdakli}
        accessibilityLabel={t['tan.abonelik.ortalama']}
        onPress={() => onAc('abonelik.ortalama', detay.abonelikOrtalamaKurus)}
      />
      {aylik > 0 ? (
        <>
          <View style={{ height: rhythm.pad }} />
          <MirrorWell
            baslik={t['tan.ayda']}
            tutarYazi={paraYaz(aylik)}
            formulYazi={abonelikFormulMetni(detay.abonelikAdet ?? 0, paraYaz(detay.abonelikOrtalamaKurus ?? 0))}
          />
        </>
      ) : null}
    </ClaySurface>
  );
}

const YATIRIM_SECENEK: { v: YatirimNiyet; etiket: string }[] = [
  { v: 'yapiyorum', etiket: t['tan.yatirim.yapiyorum'] },
  { v: 'dusunuyorum', etiket: t['tan.yatirim.dusunuyorum'] },
  { v: 'ilgilenmiyorum', etiket: t['tan.yatirim.ilgilenmiyorum'] },
];

function YatirimCard({ secili, onSec }: { secili: YatirimNiyet | null; onSec: (v: YatirimNiyet) => void }) {
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
      <View style={stil.satir}>
        <NeutralIconBox icon="landmark" />
        <View style={{ width: rhythm.pad }} />
        <Txt role="h2" style={stil.esnek}>
          {t['tan.yatirim.baslik']}
        </Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{t['tan.yatirim.aciklama']}</Txt>
      <View style={{ height: rhythm.pad }} />
      {YATIRIM_SECENEK.map((s, i) => (
        <View key={s.v}>
          {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
          <ClayPressable
            onPress={() => onSec(s.v)}
            selected={secili === s.v}
            accessibilityLabel={s.etiket}
            borderRadius={radius.tile}
            background={secili === s.v ? color.primarySoft : color.surface}
            shadow={secili === s.v ? clay.sunken : clay.raised}
            gloss={secili !== s.v}
            style={stil.secimSatiri}>
            <Txt role="bodyStrong">{s.etiket}</Txt>
          </ClayPressable>
        </View>
      ))}
      <View style={{ height: rhythm.pad }} />
      <InfoStrip variant="info" metin={`${t['tan.yatirim.sinir']} ${t['tan.yatirim.sinir.alt']}`} />
    </ClaySurface>
  );
}

function BirikimCard({
  gelirKurus,
  zorunluGiderKurus,
  zorunluYuzde,
  birikimYuzde,
  max,
  onSec,
}: {
  gelirKurus: number | null;
  zorunluGiderKurus: number;
  zorunluYuzde: number;
  birikimYuzde: number | null;
  max: number;
  onSec: (yuzde: number) => void;
}) {
  if (!gelirKurus || gelirKurus <= 0) {
    return (
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
        <View style={stil.satir}>
          <NeutralIconBox icon="target" />
          <View style={{ width: rhythm.pad }} />
          <Txt role="h2" style={stil.esnek}>
            {t['tan.birikim.baslik']}
          </Txt>
        </View>
        <View style={{ height: rhythm.group }} />
        <Txt role="caption">{t['tan.birikim.aciklama']}</Txt>
        <View style={{ height: rhythm.pad }} />
        <InfoStrip variant="info" metin={t['tan.birikim.gelirsiz']} />
      </ClaySurface>
    );
  }
  const yuzde = birikimYuzde ?? 0;
  const tutar = Math.round((gelirKurus * yuzde) / 100);
  const sinirda = max > 0 && yuzde >= max;
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
      <View style={stil.satir}>
        <NeutralIconBox icon="target" />
        <View style={{ width: rhythm.pad }} />
        <Txt role="h2" style={stil.esnek}>
          {t['tan.birikim.baslik']}
        </Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{t['tan.birikim.aciklama']}</Txt>
      <View style={{ height: rhythm.pad }} />
      <View style={stil.aralikSatiri}>
        <Txt role="label" tone={color.text2}>
          {t['tan.birikim.etiket']}
        </Txt>
        <Txt role="display">%{yuzde}</Txt>
      </View>
      <View style={{ height: rhythm.group }} />
      <Slider value={yuzde} max={max} onChange={onSec} accessibilityLabel={t['tan.birikim.etiket']} />
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{tanBirikimHedef(paraYaz(tutar))}</Txt>
      <View style={{ height: rhythm.blockInCard }} />
      <View style={stil.aralikSatiri}>
        <Txt role="micro" tone={color.text2}>
          {t['plan.ayar.aralik_en_az']}
        </Txt>
        <Txt role="micro" tone={color.text2}>
          {planAralikEnCok(max)}
        </Txt>
      </View>
      {sinirda ? (
        <>
          <View style={{ height: rhythm.blockInCard }} />
          <InfoStrip variant="warning" metin={`${t['tan.birikim.sinir']} ${t['tan.birikim.sinir.alt']}`} />
        </>
      ) : null}
      <View style={{ height: rhythm.blockInCard }} />
      <Txt role="caption">{tanBirikimUstSinirNotu(zorunluYuzde)}</Txt>
    </ClaySurface>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  basSatiri: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: layout.headerPadTop,
    paddingBottom: layout.headerPadBottom,
    paddingHorizontal: layout.screenPaddingX,
  },
  basDenge: { width: 44, height: 44 },
  esnek: { flex: 1, minWidth: 0 },
  kartIc: { padding: rhythm.pad },
  satir: { flexDirection: 'row', alignItems: 'center' },
  aralikSatiri: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  secimSatiri: { width: '100%', padding: rhythm.pad },
  altSabit: { paddingTop: rhythm.group, backgroundColor: color.bg },
});
