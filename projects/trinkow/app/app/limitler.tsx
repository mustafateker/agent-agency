import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button } from '@/components/Button';
import { CategoryIconBox } from '@/components/CategoryIconBox';
import { ClayKeypad } from '@/components/ClayKeypad';
import { ClayPressable } from '@/components/ClayPressable';
import { ClaySurface } from '@/components/ClaySurface';
import { ErrorState } from '@/components/ErrorState';
import { Icon } from '@/components/Icon';
import { InfoStrip } from '@/components/InfoStrip';
import { PushHeader } from '@/components/PushHeader';
import { Skeleton } from '@/components/Skeleton';
import { Txt } from '@/components/Txt';
import { ValueWell } from '@/components/ValueWell';
import {
  a11yKategoriLimitDegistir,
  a11yKategoriLimitKaldir,
  limitlerSuAnki,
  limitlerToplamNotu,
  t,
  toastLimitGuncellendi,
  toastLimitKaldirildi,
} from '@/content/metinler';
import { gunlukLimit } from '@/db/harcama';
import { gunlukLimitKaydet, kategoriLimitiKaydet, kategoriLimitiSil, tumKategoriLimitleri } from '@/db/limitler';
import { kategori, TUM_KATEGORILER, type KategoriKodu } from '@/lib/kategoriler';
import {
  paraYaz,
  sayiyaCevir,
  tutarGirisiEkle,
  tutarGirisiSil,
  tutarGirisindenKurus,
  tutarGosterimi,
  kurustanTutarGirisi,
} from '@/lib/para';
import { toastGoster } from '@/lib/toastBus';
import { veriDegisimineAbone, veriDegisti } from '@/lib/veriBus';
import { clay, color, layout, radius, rhythm, size } from '@/theme/tokens';

type LimitMap = Partial<Record<KategoriKodu, number>>;

/**
 * E-17 · Limitler. Referans: prototip-v3/09-limitler.html.
 * Mood: "ayar masası" — tek karar/satır. Günlük limit `pencil` ile AYRI bir
 * alt görünüme geçer (tam ekran kil tuş takımı); kategori limitleri aynı
 * ekranda AKORDEON açılır (K-029: kaldırma anında + geri al, değer
 * değişikliği yalnız alttaki genel "Kaydet" ile yazılır — bkz. PM raporu).
 */
export default function LimitlerEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [yukleniyor, setYukleniyor] = useState(true);
  const [skeletonGoster, setSkeletonGoster] = useState(false);
  const [hata, setHata] = useState(false);
  const [kaydediliyor, setKaydediliyor] = useState(false);

  const [gunlukOrijinal, setGunlukOrijinal] = useState<number | null>(null);
  const [gunlukDraft, setGunlukDraft] = useState<number | null>(null);
  const [kategoriOrijinal, setKategoriOrijinal] = useState<LimitMap>({});
  const [kategoriDraft, setKategoriDraft] = useState<LimitMap>({});
  const [kategoriHata, setKategoriHata] = useState<Partial<Record<KategoriKodu, string>>>({});

  const [aktifKategori, setAktifKategori] = useState<KategoriKodu | null>(null);
  const [kategoriBuffer, setKategoriBuffer] = useState('');

  const [gunlukDuzenleAcik, setGunlukDuzenleAcik] = useState(false);
  const [gunlukBuffer, setGunlukBuffer] = useState('');

  const [listeyiZorlaGoster, setListeyiZorlaGoster] = useState(false);

  const oku = useCallback(async () => {
    setYukleniyor(true);
    setHata(false);
    try {
      const [limit, limitler] = await Promise.all([gunlukLimit(db), tumKategoriLimitleri(db)]);
      const kategoriMap = limitler as LimitMap;
      setGunlukOrijinal(limit);
      setGunlukDraft(limit);
      setKategoriOrijinal(kategoriMap);
      setKategoriDraft(kategoriMap);
      setKategoriHata({});
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

  const kirli = useMemo(() => {
    if (gunlukDraft !== gunlukOrijinal) return true;
    return TUM_KATEGORILER.some((k) => (kategoriDraft[k] ?? null) !== (kategoriOrijinal[k] ?? null));
  }, [gunlukDraft, gunlukOrijinal, kategoriDraft, kategoriOrijinal]);

  const herhangiHataVar = Object.values(kategoriHata).some(Boolean);
  const kaydetKapali = !kirli || herhangiHataVar || kaydediliyor;

  const kategoriToplamKurus = useMemo(
    () => TUM_KATEGORILER.reduce((s, k) => s + (kategoriDraft[k] ?? 0), 0),
    [kategoriDraft],
  );

  const listeVarMi = listeyiZorlaGoster || Object.keys(kategoriOrijinal).length > 0 || Object.keys(kategoriDraft).length > 0;

  function kategoriAc(kod: KategoriKodu) {
    if (aktifKategori === kod) {
      kategoriKapat();
      return;
    }
    if (aktifKategori) kategoriKapat();
    setAktifKategori(kod);
    const mevcut = kategoriDraft[kod];
    setKategoriBuffer(mevcut ? kurustanTutarGirisi(mevcut) : '');
  }

  function kategoriKapat() {
    const kod = aktifKategori;
    if (!kod) return;
    const kurus = tutarGirisindenKurus(kategoriBuffer);
    if (kurus <= 0) {
      setKategoriHata((h) => ({ ...h, [kod]: t['hata.limit_sifir'] }));
      setKategoriDraft((d) => ({ ...d, [kod]: 0 }));
    } else {
      setKategoriHata((h) => ({ ...h, [kod]: undefined }));
      setKategoriDraft((d) => ({ ...d, [kod]: kurus }));
    }
    setAktifKategori(null);
  }

  async function kategoriKaldir(kod: KategoriKodu) {
    const eskiKurus = kategoriOrijinal[kod];
    await kategoriLimitiSil(db, kod);
    setKategoriOrijinal((o) => {
      const n = { ...o };
      delete n[kod];
      return n;
    });
    setKategoriDraft((d) => {
      const n = { ...d };
      delete n[kod];
      return n;
    });
    setKategoriHata((h) => ({ ...h, [kod]: undefined }));
    setAktifKategori(null);
    veriDegisti();
    const katAdi = kategori(kod).ad;
    toastGoster({
      tur: 'undoInfo',
      metin: toastLimitKaldirildi(katAdi),
      eylemEtiketi: t['toast.geri_al'],
      onEylem: async () => {
        if (eskiKurus === undefined) return;
        await kategoriLimitiKaydet(db, kod, eskiKurus);
        setKategoriOrijinal((o) => ({ ...o, [kod]: eskiKurus }));
        setKategoriDraft((d) => ({ ...d, [kod]: eskiKurus }));
        veriDegisti();
        toastGoster({ tur: 'info', metin: t['toast.geri_alindi'] });
      },
    });
  }

  function gunlukAc() {
    setGunlukBuffer(gunlukDraft ? kurustanTutarGirisi(gunlukDraft) : '');
    setGunlukDuzenleAcik(true);
  }

  function gunlukUygula() {
    const kurus = tutarGirisindenKurus(gunlukBuffer);
    if (kurus > 0) setGunlukDraft(kurus);
    setGunlukDuzenleAcik(false);
  }

  async function tumunuKaydet() {
    if (kaydetKapali) return;
    setKaydediliyor(true);
    try {
      if (gunlukDraft !== gunlukOrijinal && gunlukDraft !== null) {
        await gunlukLimitKaydet(db, gunlukDraft);
      }
      for (const kod of TUM_KATEGORILER) {
        const yeni = kategoriDraft[kod];
        const eski = kategoriOrijinal[kod];
        if (yeni !== undefined && yeni !== eski) {
          await kategoriLimitiKaydet(db, kod, yeni);
        }
      }
      veriDegisti();
      setGunlukOrijinal(gunlukDraft);
      setKategoriOrijinal({ ...kategoriDraft });
      if (gunlukDraft !== null && gunlukDraft !== gunlukOrijinal) {
        toastGoster({ tur: 'info', metin: toastLimitGuncellendi(paraYaz(gunlukDraft)) });
      }
    } finally {
      setKaydediliyor(false);
    }
  }

  if (gunlukDuzenleAcik) {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <PushHeader baslik={t['limitler.gunluk']} onGeri={() => setGunlukDuzenleAcik(false)} />
        <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false}>
          <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
            <Txt role="caption">{t['limitler.gunluk_aciklama']}</Txt>
            <View style={{ height: rhythm.blockInCard }} />
            <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.buyukKuyu}>
              <View style={stil.buyukSatir}>
                <Txt role="hero">{tutarGosterimi(gunlukBuffer)}</Txt>
                <View style={{ width: rhythm.sameObject }} />
                <Txt role="display" tone={color.text2}>
                  ₺
                </Txt>
                <View style={{ width: rhythm.group }} />
                <View style={stil.imlec} />
              </View>
            </ClaySurface>
            <View style={{ height: rhythm.blockInCard }} />
            <Txt role="caption">{limitlerSuAnki(paraYaz(gunlukOrijinal ?? 0))}</Txt>
          </ClaySurface>
        </ScrollView>
        <View style={[stil.altSabit, { paddingBottom: insets.bottom }]}>
          <View style={stil.pad}>
            <ClayKeypad
              onDigit={(d) => setGunlukBuffer((b) => tutarGirisiEkle(b, d))}
              onComma={() => setGunlukBuffer((b) => tutarGirisiEkle(b, ','))}
              onBackspace={() => setGunlukBuffer((b) => tutarGirisiSil(b))}
            />
          </View>
          <View style={{ height: rhythm.blockInCard }} />
          <View style={stil.pad}>
            <Button label={t['eylem.kaydet']} variant="primary" onPress={gunlukUygula} />
          </View>
        </View>
      </View>
    );
  }

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <PushHeader baslik={t['limitler.baslik']} onGeri={() => router.back()} />

      <ScrollView
        style={stil.kaydir}
        contentContainerStyle={[stil.pad, { paddingBottom: rhythm.section }]}
        showsVerticalScrollIndicator={false}>
        {skeletonGoster ? (
          <LimitlerSkeleton />
        ) : hata ? (
          <ErrorState onRetry={oku} />
        ) : (
          <>
            <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
              <Txt role="h2">{t['limitler.gunluk']}</Txt>
              <View style={{ height: rhythm.group }} />
              <Txt role="caption">{t['limitler.gunluk_aciklama']}</Txt>
              <View style={{ height: rhythm.blockInCard }} />
              <ClayPressable
                onPress={gunlukAc}
                accessibilityLabel={t['a11y.gunluk_limit_degistir']}
                borderRadius={radius.tile}
                background={color.well}
                pressedBackground={color.groove}
                shadow={clay.sunken}
                pressedShadow={clay.pressed}
                gloss={false}
                style={stil.gunlukKuyu}>
                <View style={stil.gunlukSatir}>
                  <Txt role="display">{sayiyaCevir(gunlukDraft ?? 0)}</Txt>
                  <View style={{ width: rhythm.sameObject }} />
                  <Txt role="amount" tone={color.text2}>
                    ₺
                  </Txt>
                </View>
                <Icon name="pencil" size={size.iconSm} color={color.text2} />
              </ClayPressable>
            </ClaySurface>

            <View style={{ height: rhythm.section }} />
            <View style={stil.bolumBasligi}>
              <Txt role="h2">{t['limitler.kategori_baslik']}</Txt>
              <Txt role="label" tone={color.text2}>
                {t['limitler.kategori_periyot']}
              </Txt>
            </View>
            <View style={{ height: rhythm.group }} />

            {listeVarMi ? (
              <>
                {TUM_KATEGORILER.map((kod, i) => {
                  const kat = kategori(kod);
                  const deger = kategoriDraft[kod];
                  const odaklandi = aktifKategori === kod;
                  const hataVar = Boolean(kategoriHata[kod]);
                  const kaldirilabilir = odaklandi && (kategoriOrijinal[kod] !== undefined || (deger ?? 0) > 0);
                  return (
                    <View key={kod}>
                      {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
                      <ValueWell
                        sol={<CategoryIconBox kategori={kat} />}
                        etiket={kat.ad}
                        deger={
                          odaklandi
                            ? `${tutarGosterimi(kategoriBuffer)} ₺`
                            : deger
                              ? paraYaz(deger)
                              : t['limitler.limit_yok']
                        }
                        degerSoluk={!odaklandi && !deger}
                        focused={odaklandi}
                        hata={hataVar}
                        onPress={() => kategoriAc(kod)}
                        accessibilityLabel={a11yKategoriLimitDegistir(kat.ad)}
                      />
                      {hataVar ? (
                        <>
                          <View style={{ height: rhythm.sameObject }} />
                          <Txt role="caption" tone={color.dangerInk}>
                            {kategoriHata[kod]}
                          </Txt>
                        </>
                      ) : null}
                      {odaklandi ? (
                        <>
                          <View style={{ height: rhythm.group }} />
                          <ClayKeypad
                            onDigit={(d) => setKategoriBuffer((b) => tutarGirisiEkle(b, d))}
                            onComma={() => setKategoriBuffer((b) => tutarGirisiEkle(b, ','))}
                            onBackspace={() => setKategoriBuffer((b) => tutarGirisiSil(b))}
                          />
                          {kaldirilabilir ? (
                            <>
                              <View style={{ height: rhythm.group }} />
                              <Button
                                label={t['limitler.limit_kaldir']}
                                variant="ghost"
                                icon="limit-kaldir"
                                auto
                                onPress={() => void kategoriKaldir(kod)}
                                accessibilityLabel={a11yKategoriLimitKaldir(kat.ad)}
                              />
                            </>
                          ) : null}
                        </>
                      ) : null}
                    </View>
                  );
                })}

                <View style={{ height: rhythm.section }} />
                <InfoStrip
                  variant="info"
                  metin={`${limitlerToplamNotu(paraYaz(kategoriToplamKurus))}\n${t['limitler.bos_takip']}`}
                />
              </>
            ) : (
              <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
                <Txt role="body">{t['limitler.kategori_bos']}</Txt>
                <View style={{ height: rhythm.blockInCard }} />
                <Button
                  label={t['limitler.kategori_ekle']}
                  variant="secondary"
                  icon="plus"
                  auto
                  onPress={() => setListeyiZorlaGoster(true)}
                />
              </ClaySurface>
            )}
          </>
        )}
      </ScrollView>

      <View style={[stil.altSabit, { paddingBottom: layout.tabBarLift + insets.bottom }]}>
        <View style={stil.pad}>
          <Button
            label={t['eylem.kaydet']}
            variant="primary"
            disabled={kaydetKapali && !kaydediliyor}
            loading={kaydediliyor}
            onPress={() => void tumunuKaydet()}
          />
        </View>
      </View>
    </View>
  );
}

function LimitlerSkeleton() {
  return (
    <>
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
        <Skeleton width={112} height={18} />
        <View style={{ height: rhythm.group }} />
        <Skeleton width={214} height={18} />
        <View style={{ height: rhythm.blockInCard }} />
        <Skeleton width="100%" height={64} borderRadius={radius.tile} />
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
        <Skeleton width={148} height={25} />
        <View style={{ height: rhythm.group }} />
        {[0, 1, 2].map((i) => (
          <View key={i}>
            {i > 0 ? <View style={{ height: rhythm.blockInCard }} /> : null}
            <Skeleton width="100%" height={68} borderRadius={radius.tile} />
          </View>
        ))}
      </ClaySurface>
    </>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  kart: { padding: rhythm.pad },
  bolumBasligi: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  altSabit: { paddingTop: rhythm.group, backgroundColor: color.bg },
  buyukKuyu: { padding: rhythm.pad, alignItems: 'center' },
  buyukSatir: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center' },
  imlec: { width: 3, height: 44, borderRadius: radius.pill, backgroundColor: color.primary },
  gunlukKuyu: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: rhythm.pad,
  },
  gunlukSatir: { flexDirection: 'row', alignItems: 'baseline' },
});
