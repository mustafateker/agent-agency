import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ClaySurface } from '@/components/ClaySurface';
import { ErrorState } from '@/components/ErrorState';
import { Icon } from '@/components/Icon';
import { InfoStrip } from '@/components/InfoStrip';
import { MonthLoadRow, MonthLoadRowSkeleton } from '@/components/MonthLoadRow';
import { PushHeader } from '@/components/PushHeader';
import { SeriesRow } from '@/components/SeriesRow';
import { Skeleton } from '@/components/Skeleton';
import { Txt } from '@/components/Txt';
import { t, taksitBitis, taksitKalanToplam, taksitSeri, taksitSeriBitti } from '@/content/metinler';
import {
  gecenAyBitenSeri,
  surenSeriler,
  taksitAylikYuk,
  taksitBuAyToplam,
  taksitKalanToplamKurus,
  taksitSonAy,
  type SurenSeri,
} from '@/db/harcama';
import { kategori } from '@/lib/kategoriler';
import { paraYaz, sayiyaCevir } from '@/lib/para';
import { ayAdiTek, ayAnahtari, ayBasligi, ayEkle } from '@/lib/tarih';
import { veriDegisimineAbone } from '@/lib/veriBus';
import { clay, color, layout, radius, rhythm } from '@/theme/tokens';

const GELECEK_AY_SAYISI = 6;

type Veri = {
  buAyToplamKurus: number;
  aylar: { ay: string; toplamKurus: number }[];
  kalanToplamKurus: number;
  sonAy: string | null;
  seriler: SurenSeri[];
  bitenSeri: { kategori: string; tutarKurus: number } | null;
};

/**
 * E-18 · Taksitler. Referans: prototip-v3/10-taksitler.html.
 * Mood: "yük haritası" — merkezde altı aylık `MonthLoadRow` çubuğu.
 */
export default function TaksitlerEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [yukleniyor, setYukleniyor] = useState(true);
  const [skeletonGoster, setSkeletonGoster] = useState(false);
  const [hata, setHata] = useState(false);
  const [veri, setVeri] = useState<Veri | null>(null);

  const oku = useCallback(async () => {
    setYukleniyor(true);
    setHata(false);
    try {
      const bugun = new Date();
      const buAy = ayAnahtari(bugun);
      const buAyBaslangicGunu = `${buAy}-01`;
      const gecenAy = ayAnahtari(ayEkle(bugun, -1));
      const aySayisiler = Array.from({ length: GELECEK_AY_SAYISI }, (_, i) => ayAnahtari(ayEkle(bugun, i)));

      const [buAyToplamKurus, aylar, kalanToplamKurus, sonAy, seriler, bitenSeri] = await Promise.all([
        taksitBuAyToplam(db, buAy),
        taksitAylikYuk(db, aySayisiler),
        taksitKalanToplamKurus(db, buAyBaslangicGunu),
        taksitSonAy(db, buAyBaslangicGunu),
        surenSeriler(db, buAy),
        gecenAyBitenSeri(db, gecenAy),
      ]);
      setVeri({ buAyToplamKurus, aylar, kalanToplamKurus, sonAy, seriler, bitenSeri });
    } catch {
      setHata(true);
    } finally {
      setYukleniyor(false);
    }
  }, [db]);

  useEffect(() => {
    void oku();
  }, [oku]);

  useEffect(() => veriDegisimineAbone(() => void oku()), [oku]);

  useEffect(() => {
    if (!yukleniyor) {
      setSkeletonGoster(false);
      return;
    }
    const zamanlayici = setTimeout(() => setSkeletonGoster(true), 150);
    return () => clearTimeout(zamanlayici);
  }, [yukleniyor]);

  const maxAyToplami = useMemo(
    () => Math.max(1, ...(veri?.aylar.map((a) => a.toplamKurus) ?? [1])),
    [veri],
  );

  const bosMu = !skeletonGoster && !hata && veri !== null && veri.buAyToplamKurus === 0 && veri.seriler.length === 0;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <PushHeader baslik={t['taksit.baslik']} onGeri={() => router.back()} />

      <ScrollView
        style={stil.kaydir}
        contentContainerStyle={[stil.pad, { paddingBottom: layout.scrollPadBottom }]}
        showsVerticalScrollIndicator={false}>
        {skeletonGoster ? (
          <Skeletonlar />
        ) : hata ? (
          <ErrorState onRetry={oku} />
        ) : bosMu ? (
          <BosDurum />
        ) : veri ? (
          <>
            <ClaySurface level="raisedLg" borderRadius={radius.hero} style={stil.kart}>
              <Txt role="label" tone={color.text2}>
                {t['taksit.bu_ay_etiket']}
              </Txt>
              <View style={{ height: rhythm.sameObject }} />
              <View style={stil.paraSatiri}>
                <Txt role="display">{sayiyaCevir(veri.buAyToplamKurus)}</Txt>
                <View style={{ width: rhythm.sameObject }} />
                <Txt role="amount" tone={color.text2}>
                  ₺
                </Txt>
              </View>
              <View style={{ height: rhythm.blockInCard }} />
              <Txt role="caption">{t['taksit.aciklama']}</Txt>
            </ClaySurface>

            <View style={{ height: rhythm.section }} />
            <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
              <Txt role="h2">{t['taksit.gelecek_baslik']}</Txt>
              <View style={{ height: rhythm.group }} />
              {veri.aylar.map((a, i) => (
                <View key={a.ay}>
                  {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
                  <MonthLoadRow
                    ay={ayAdiTek(a.ay)}
                    tutar={paraYaz(a.toplamKurus)}
                    oran={a.toplamKurus / maxAyToplami}
                    current={i === 0}
                  />
                </View>
              ))}
              {veri.kalanToplamKurus > 0 && veri.sonAy ? (
                <>
                  <View style={{ height: rhythm.blockInCard }} />
                  <Txt role="caption">
                    {taksitKalanToplam(paraYaz(veri.kalanToplamKurus), ayBasligi(veri.sonAy))}
                  </Txt>
                </>
              ) : null}
            </ClaySurface>

            <View style={{ height: rhythm.section }} />
            <View style={stil.bolumBasligi}>
              <Txt role="h2">{t['taksit.seriler_baslik']}</Txt>
              <Txt role="label" tone={color.text2}>
                {seriAdet(veri.seriler.length)}
              </Txt>
            </View>
            <View style={{ height: rhythm.group }} />
            {veri.seriler.map((s, i) => {
              const kat = kategori(s.kategori);
              const son = s.taksitNo === s.taksitToplam;
              return (
                <View key={s.taksitId}>
                  {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
                  <SeriesRow
                    kategoriKodu={s.kategori}
                    ustSatir={taksitSeri(kat.ad, s.taksitNo, s.taksitToplam)}
                    altSatir={son ? t['taksit.son_taksit'] : taksitBitis(ayBasligi(s.sonAy))}
                    tutar={paraYaz(s.tutarKurus)}
                    last={son}
                  />
                </View>
              );
            })}

            {veri.bitenSeri ? (
              <>
                <View style={{ height: rhythm.section }} />
                <InfoStrip
                  variant="info"
                  metin={taksitSeriBitti(
                    kategori(veri.bitenSeri.kategori).ad,
                    ayAdiTek(ayAnahtari(ayEkle(new Date(), -1))),
                    paraYaz(veri.bitenSeri.tutarKurus),
                  )}
                />
              </>
            ) : null}
          </>
        ) : null}
      </ScrollView>
    </View>
  );
}

function seriAdet(adet: number): string {
  return `${adet} seri`;
}

function BosDurum() {
  return (
    <ClaySurface level="raisedLg" borderRadius={radius.hero} style={stil.bosKart}>
      <View style={stil.bosDisk}>
        <Icon name="calendar-clock" size={32} color={color.text2} />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <Txt role="h2">{t['bos.taksit.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" style={stil.ortaMetin}>
        {t['bos.taksit.govde']}
      </Txt>
    </ClaySurface>
  );
}

function Skeletonlar() {
  return (
    <>
      <ClaySurface level="raisedLg" borderRadius={radius.hero} style={stil.kart}>
        <Skeleton width={52} height={18} />
        <View style={{ height: rhythm.sameObject }} />
        <Skeleton width={152} height={38} />
        <View style={{ height: rhythm.blockInCard }} />
        <Skeleton width="100%" height={18} />
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
        <Skeleton width={176} height={25} />
        <View style={{ height: rhythm.group }} />
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <View key={i}>
            {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
            <MonthLoadRowSkeleton />
          </View>
        ))}
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
      <Skeleton width={140} height={25} />
      <View style={{ height: rhythm.group }} />
      {[0, 1].map((i) => (
        <View key={i}>
          {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
          <View style={stil.satirIskelet}>
            <Skeleton width={44} height={44} borderRadius={radius.tile} />
            <View style={stil.satirIskeletOrta}>
              <Skeleton width={128} height={24} />
              <View style={{ height: rhythm.sameObject }} />
              <Skeleton width={168} height={18} />
            </View>
            <Skeleton width={72} height={24} />
          </View>
        </View>
      ))}
    </>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  kart: { padding: rhythm.pad },
  paraSatiri: { flexDirection: 'row', alignItems: 'baseline' },
  bolumBasligi: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  bosKart: { padding: rhythm.pad, alignItems: 'center' },
  bosDisk: {
    width: 176,
    height: 176,
    borderRadius: radius.pill,
    backgroundColor: color.groove,
    boxShadow: clay.sunken,
    alignItems: 'center',
    justifyContent: 'center',
  },
  ortaMetin: { textAlign: 'center' },
  satirIskelet: { flexDirection: 'row', alignItems: 'center', minHeight: 68, paddingHorizontal: 16 },
  satirIskeletOrta: { flex: 1, minWidth: 0, paddingHorizontal: rhythm.blockInCard },
});
