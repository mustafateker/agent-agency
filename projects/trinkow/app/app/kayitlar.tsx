import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { FlatList, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ClaySurface } from '@/components/ClaySurface';
import { EmptyState } from '@/components/EmptyState';
import { ErrorState } from '@/components/ErrorState';
import { ExpenseRow } from '@/components/ExpenseRow';
import { Icon } from '@/components/Icon';
import { IconButton } from '@/components/IconButton';
import { ScreenHeader } from '@/components/ScreenHeader';
import { Skeleton } from '@/components/Skeleton';
import { TabBar } from '@/components/TabBar';
import { Txt } from '@/components/Txt';
import { gunToplamEtiketi, kayitlarAyOzeti, kayitlarGunToplamLimitDisi, kayitlarYerTutucuBasligi, t } from '@/content/metinler';
import { ayHarcamalari, ayOzeti, gunlukLimit, herhangiKayitVarMi, type Harcama } from '@/db/harcama';
import { duzListeOlustur, gunGruplariOlustur, type ListeOgesi } from '@/lib/gruplama';
import { paraYaz } from '@/lib/para';
import { ayAnahtari, ayBasligi, ayEkle, gunBasligi } from '@/lib/tarih';
import { veriDegisimineAbone } from '@/lib/veriBus';
import { clay, color, layout, radius, rhythm, size } from '@/theme/tokens';

/**
 * E-14 · Kayıtlar (sekme 2). Referans: prototip-v3/04-kayitlar.html.
 * Mood: "defter" — hiç kart yok, sık dikey ritim (§6 ekran karakteri).
 * Gün gruplaması hazır `lib/gruplama.ts` ile kurulur.
 */
export default function KayitlarEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [ayGosterge, setAyGosterge] = useState(() => new Date());
  const ay = useMemo(() => ayAnahtari(ayGosterge), [ayGosterge]);

  const [yukleniyor, setYukleniyor] = useState(true);
  const [skeletonGoster, setSkeletonGoster] = useState(false);
  const [hata, setHata] = useState(false);
  const [harcamalar, setHarcamalar] = useState<Harcama[]>([]);
  const [ozet, setOzet] = useState({ adet: 0, toplamKurus: 0 });
  const [limitKurus, setLimitKurus] = useState<number | null>(null);
  const [genelBos, setGenelBos] = useState<boolean | null>(null);

  const oku = useCallback(async () => {
    setYukleniyor(true);
    setHata(false);
    try {
      const [liste, ozetSonuc, limit, varMi] = await Promise.all([
        ayHarcamalari(db, ay),
        ayOzeti(db, ay),
        gunlukLimit(db),
        herhangiKayitVarMi(db),
      ]);
      setHarcamalar(liste);
      setOzet(ozetSonuc);
      setLimitKurus(limit);
      setGenelBos(!varMi);
    } catch {
      setHata(true);
    } finally {
      setYukleniyor(false);
    }
  }, [db, ay]);

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

  const ogeler: ListeOgesi[] = useMemo(() => {
    const gruplar = gunGruplariOlustur(harcamalar);
    return duzListeOlustur(gruplar, limitKurus);
  }, [harcamalar, limitKurus]);

  const bugun = useMemo(() => new Date(), []);
  const ayDegistir = (fark: number) => setAyGosterge((d) => ayEkle(d, fark));

  const ayDegistiriciGizli = genelBos === true;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <ScreenHeader
        baslik={t['kayitlar.baslik']}
        actionIcon="repeat"
        actionLabel={t['kayitlar.taksitleri_ac']}
        onActionPress={() => router.push('/taksitler')}
      />

      <FlatList
        style={stil.liste}
        contentContainerStyle={[stil.pad, { paddingBottom: layout.scrollPadBottom }]}
        showsVerticalScrollIndicator={false}
        data={skeletonGoster || hata || genelBos === null ? [] : ogeler}
        keyExtractor={(oge) => (oge.tip === 'baslik' ? `b-${oge.gun}` : `s-${oge.harcama.id}`)}
        ListHeaderComponent={
          <>
            {!ayDegistiriciGizli ? (
              <>
                <AyDegistirici
                  skeleton={skeletonGoster}
                  baslik={ayBasligi(ay)}
                  ozetMetin={ozet.adet === 0 ? t['kayitlar.ay_ozet_bos'] : kayitlarAyOzeti(ozet.adet, paraYaz(ozet.toplamKurus))}
                  onOnceki={() => ayDegistir(-1)}
                  onSonraki={() => ayDegistir(1)}
                />
                <View style={{ height: rhythm.section }} />
              </>
            ) : null}

            {skeletonGoster ? (
              <ListeSkeleton />
            ) : hata ? (
              <>
                <ErrorState onRetry={oku} />
                <View style={{ height: rhythm.section }} />
                <PlaceholderSatiri ay={ayBasligi(ay)} />
              </>
            ) : genelBos === null ? (
              // İlk okuma 150ms'den kısa sürdü — henüz boş/dolu bilinmiyor, hiçbir şey çizilmez.
              null
            ) : genelBos ? (
              <EmptyState
                icon="notebook"
                baslik={t['bos.kayitlar.baslik']}
                govde={t['bos.kayitlar.govde']}
                butonEtiketi={t['eylem.harcama_ekle']}
                onButonPress={() => router.push('/harcama-ekle')}
              />
            ) : ozet.adet === 0 ? (
              <AyBosDurumu />
            ) : null}
          </>
        }
        renderItem={({ item, index }) => {
          if (item.tip === 'baslik') {
            return (
              <View>
                {index > 0 ? <View style={{ height: rhythm.section }} /> : null}
                <View style={stil.gunBasligi}>
                  <Txt role="bodyStrong">{gunBasligi(item.gun, bugun)}</Txt>
                  <Txt role="label" tone={item.limitDisi ? color.warningInk : color.text2}>
                    {item.limitDisi
                      ? kayitlarGunToplamLimitDisi(paraYaz(item.toplamKurus))
                      : gunToplamEtiketi(paraYaz(item.toplamKurus))}
                  </Txt>
                </View>
                <View style={{ height: rhythm.group }} />
              </View>
            );
          }
          return (
            <View style={{ paddingBottom: rhythm.group }}>
              <ExpenseRow
                harcama={item.harcama}
                limitDisi={item.limitDisi}
                kaydirilabilir
                onPress={() => router.push(`/harcama/${item.harcama.id}`)}
              />
            </View>
          );
        }}
      />

      <View style={[stil.pad, { paddingBottom: layout.tabBarLift + insets.bottom }]}>
        <TabBar
          active="kayitlar"
          onSelect={(key) => {
            if (key === 'gunluk') router.replace('/');
            else if (key === 'ozet') router.push('/ozet');
          }}
          onAdd={() => router.push('/harcama-ekle')}
        />
      </View>
    </View>
  );
}

function AyDegistirici({
  skeleton,
  baslik,
  ozetMetin,
  onOnceki,
  onSonraki,
}: {
  skeleton: boolean;
  baslik: string;
  ozetMetin: string;
  onOnceki: () => void;
  onSonraki: () => void;
}) {
  return (
    <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.aySarma}>
      {skeleton ? (
        <View style={stil.aySatiri}>
          <Skeleton width={44} height={44} borderRadius={radius.pill} />
          <View style={stil.ayOrta}>
            <Skeleton width={104} height={20} />
            <View style={{ height: rhythm.sameObject }} />
            <Skeleton width={136} height={16} />
          </View>
          <Skeleton width={44} height={44} borderRadius={radius.pill} />
        </View>
      ) : (
        <View style={stil.aySatiri}>
          <IconButton icon="chevron-left" accessibilityLabel={t['kayitlar.onceki_ay']} onPress={onOnceki} />
          <View style={stil.ayOrta}>
            <Txt role="bodyStrong">{baslik}</Txt>
            <View style={{ height: rhythm.sameObject }} />
            <Txt role="caption" tone={color.text2}>
              {ozetMetin}
            </Txt>
          </View>
          <IconButton icon="chevron-right" accessibilityLabel={t['kayitlar.sonraki_ay']} onPress={onSonraki} />
        </View>
      )}
    </ClaySurface>
  );
}

function ListeSkeleton() {
  return (
    <View>
      <Skeleton width={140} height={18} />
      <View style={{ height: rhythm.group }} />
      {[62, 48, 55].map((w, i) => (
        <View key={i} style={stil.satirKart}>
          <Skeleton width={44} height={44} borderRadius={radius.tile} />
          <View style={stil.esnek}>
            <Skeleton width={`${w}%`} height={16} />
            <View style={{ height: rhythm.group }} />
            <Skeleton width={`${w - 20}%`} height={12} />
          </View>
          <Skeleton width={72} height={20} />
        </View>
      ))}
    </View>
  );
}

/**
 * "Bu ayda kayıt yok" — E-14'ün ikinci boş durumu. Global boş durumdan
 * FARKLI illüstrasyon ölçeği (96pt, `ErrorState` ile aynı kap) — ay
 * değiştirici burada kalır, çözüm zaten orada.
 */
function AyBosDurumu() {
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.bosKart}>
      <View style={stil.hataDaire}>
        <Icon name="calendar" size={32} color={color.text2} />
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <Txt role="h2">{t['bos.kayitlar_ay.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" style={stil.ortaMetin}>
        {t['bos.kayitlar_ay.govde']}
      </Txt>
    </ClaySurface>
  );
}

/** Hata durumunda listenin nereye geleceğini gösteren kapalı yer tutucu. */
function PlaceholderSatiri({ ay }: { ay: string }) {
  return (
    <View style={stil.satirKart}>
      <View style={stil.placeholderIkon}>
        <Icon name="circle-dashed" size={20} color={color.text2} />
      </View>
      <View style={stil.esnek}>
        <Txt role="body" tone={color.text2}>
          {kayitlarYerTutucuBasligi(ay)}
        </Txt>
        <Txt role="caption">{t['kayitlar.yer_tutucu.govde']}</Txt>
      </View>
    </View>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  liste: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  aySarma: { padding: rhythm.pad },
  aySatiri: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  ayOrta: { alignItems: 'center' },
  gunBasligi: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  esnek: { flex: 1, minWidth: 0, paddingHorizontal: rhythm.blockInCard },
  satirKart: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: size.rowMinHeight,
    paddingVertical: size.rowPadY,
    paddingHorizontal: size.rowPadX,
    marginBottom: rhythm.group,
    borderRadius: radius.tile,
    backgroundColor: color.surface,
  },
  placeholderIkon: { width: size.catBox, height: size.catBox, alignItems: 'center', justifyContent: 'center' },
  bosKart: { padding: rhythm.pad, alignItems: 'center' },
  hataDaire: {
    width: 96,
    height: 96,
    borderRadius: radius.pill,
    backgroundColor: color.groove,
    boxShadow: clay.sunken,
    alignItems: 'center',
    justifyContent: 'center',
  },
  ortaMetin: { textAlign: 'center' },
});
