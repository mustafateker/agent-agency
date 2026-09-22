import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button } from '@/components/Button';
import { ClaySurface } from '@/components/ClaySurface';
import { ErrorState } from '@/components/ErrorState';
import { Icon } from '@/components/Icon';
import { IconButton } from '@/components/IconButton';
import { InfoStrip } from '@/components/InfoStrip';
import { ScreenHeader } from '@/components/ScreenHeader';
import { Skeleton } from '@/components/Skeleton';
import { TabBar } from '@/components/TabBar';
import { Txt } from '@/components/Txt';
import { WeekStrip, type WeekStripGun } from '@/components/WeekStrip';
import { LimitReviewCard } from '@/components/pano/LimitReviewCard';
import {
  ozetDagilimGun,
  ozetEnCok,
  ozetGecenGunOrtalama,
  ozetKucukHarcamaAlt,
  ozetLimitAltiGun,
  ozetLimitCizgisi,
  ozetLimitDisiGun,
  ozetLimitSorguBasligi,
  ozetPay,
  ozetTaksitYuku,
  t,
  taksitYukuAltMetni,
} from '@/content/metinler';
import { gunlukLimit, surenSeriler, taksitSonAy } from '@/db/harcama';
import { haftaGunToplamlari, haftaKategoriDagilimi, haftaKucukHarcamaOzeti, type KategoriPayi } from '@/db/ozet';
import { aileRenkleri, kategori } from '@/lib/kategoriler';
import { paraYaz, sayiyaCevir } from '@/lib/para';
import { ayAnahtari, ayBasligi, ayEkle, gunAnahtari, gunEkle, haftaAraligi, haftaBaslangici } from '@/lib/tarih';
import { veriDegisimineAbone } from '@/lib/veriBus';
import { clay, color, layout, radius, rhythm } from '@/theme/tokens';

const KUCUK_HARCAMA_ESIK_KURUS = 5000;

type Veri = {
  gunToplamlari: Map<string, number>;
  kategoriDagilimi: KategoriPayi[];
  kucukHarcama: { adet: number; toplamKurus: number };
  limitKurus: number | null;
  // taksit yükü (gelecek ay)
  gelecekAyTutarKurus: number;
  gelecekAySeriAdet: number;
  gelecekAySonAy: string | null;
};

/**
 * E-16 · Özet. Referans: prototip-v3/05-ozet.html.
 * Mood: "ölçüm sayfası" — yorum yok, sayı var (hairline ayraçlı liste).
 */
export default function OzetEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [haftaFarki, setHaftaFarki] = useState(0);
  const [yukleniyor, setYukleniyor] = useState(true);
  const [skeletonGoster, setSkeletonGoster] = useState(false);
  const [hata, setHata] = useState(false);
  const [veri, setVeri] = useState<Veri | null>(null);
  const [kartKapatildi, setKartKapatildi] = useState(false);

  const bugun = useMemo(() => new Date(), []);
  const haftaBasi = useMemo(
    () => gunEkle(haftaBaslangici(bugun), haftaFarki * 7),
    [bugun, haftaFarki],
  );
  const haftaSonu = useMemo(() => gunEkle(haftaBasi, 6), [haftaBasi]);
  const buHaftaMi = haftaFarki === 0;
  const haftaTamamlandiMi = haftaFarki < 0;

  useEffect(() => setKartKapatildi(false), [haftaFarki]);

  const oku = useCallback(async () => {
    setYukleniyor(true);
    setHata(false);
    try {
      const gecekAy = ayAnahtari(ayEkle(bugun, 1));
      const gelecekAyBaslangicGunu = `${gecekAy}-01`;
      const [gunToplamlari, kategoriDagilimi, kucukHarcama, limitKurus, gelecekAySeriler, gelecekAySonAy] =
        await Promise.all([
          haftaGunToplamlari(db, gunAnahtari(haftaBasi), gunAnahtari(haftaSonu)),
          haftaKategoriDagilimi(db, gunAnahtari(haftaBasi), gunAnahtari(haftaSonu)),
          haftaKucukHarcamaOzeti(db, gunAnahtari(haftaBasi), gunAnahtari(haftaSonu), KUCUK_HARCAMA_ESIK_KURUS),
          gunlukLimit(db),
          surenSeriler(db, gecekAy),
          taksitSonAy(db, gelecekAyBaslangicGunu),
        ]);
      const gecekAyToplam = gelecekAySeriler.reduce((s, ser) => s + ser.tutarKurus, 0);
      setVeri({
        gunToplamlari: new Map(gunToplamlari.map((g) => [g.gun, g.toplamKurus])),
        kategoriDagilimi,
        kucukHarcama,
        limitKurus,
        gelecekAyTutarKurus: gecekAyToplam,
        gelecekAySeriAdet: gelecekAySeriler.length,
        gelecekAySonAy,
      });
    } catch {
      setHata(true);
    } finally {
      setYukleniyor(false);
    }
  }, [db, bugun, haftaBasi, haftaSonu]);

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

  const gunler: WeekStripGun[] = useMemo(() => {
    if (!veri) return [];
    return Array.from({ length: 7 }, (_, i) => {
      const g = gunEkle(haftaBasi, i);
      const gelecek = buHaftaMi && g.getTime() > bugun.getTime();
      return { toplamKurus: veri.gunToplamlari.get(gunAnahtari(g)) ?? 0, gelecek };
    });
  }, [veri, haftaBasi, buHaftaMi, bugun]);

  const elapsedGunSayisi = buHaftaMi ? ((bugun.getDay() + 6) % 7) + 1 : 7;
  const aktifIndex = buHaftaMi ? elapsedGunSayisi - 1 : undefined;

  const haftaToplamKurus = useMemo(
    () => gunler.reduce((s, g) => s + g.toplamKurus, 0),
    [gunler],
  );
  const limitDisiGunSayisi = useMemo(() => {
    if (!veri?.limitKurus) return 0;
    return gunler.slice(0, elapsedGunSayisi).filter((g) => g.toplamKurus > (veri.limitKurus as number)).length;
  }, [gunler, elapsedGunSayisi, veri]);
  const tumHaftaLimitDisi = veri?.limitKurus != null && elapsedGunSayisi > 0 && limitDisiGunSayisi === elapsedGunSayisi;

  const gunlukOrtalamaKurus = elapsedGunSayisi > 0 ? Math.round(haftaToplamKurus / elapsedGunSayisi) : 0;

  const enCokKategori = veri && veri.kategoriDagilimi.length > 0 ? veri.kategoriDagilimi[0] : null;
  const dagilimToplam = veri ? veri.kategoriDagilimi.reduce((s, k) => s + k.toplamKurus, 0) : 0;

  const haftaBosMu = !skeletonGoster && !hata && veri !== null && haftaToplamKurus === 0 && veri.kategoriDagilimi.length === 0;

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <ScreenHeader
        baslik={t['ozet.baslik']}
        actionIcon="limitler"
        actionLabel={t['ozet.limitleri_ac']}
        onActionPress={() => router.push('/limitler')}
        ikinciActionIcon="ayarlar"
        ikinciActionLabel={t['ayar.baslik']}
        onIkinciActionPress={() => router.push('/ayarlar')}
      />

      <ScrollView
        style={stil.kaydir}
        contentContainerStyle={[stil.pad, { paddingBottom: layout.scrollPadBottom }]}
        showsVerticalScrollIndicator={false}>
        <HaftaDegistirici
          skeleton={skeletonGoster}
          strong={buHaftaMi ? t['ozet.hafta_bu'] : haftaAraligi(haftaBasi, haftaSonu)}
          caption={buHaftaMi ? haftaAraligi(haftaBasi, haftaSonu) : t['ozet.hafta_tamamlanan']}
          sonrakiKapali={haftaFarki >= 0}
          onOnceki={() => setHaftaFarki((f) => f - 1)}
          onSonraki={() => setHaftaFarki((f) => Math.min(0, f + 1))}
        />

        <View style={{ height: rhythm.section }} />

        {skeletonGoster ? (
          <OzetKartiSkeleton />
        ) : hata ? (
          <ErrorState onRetry={oku} />
        ) : haftaBosMu ? (
          <BosHafta gunler={gunler} onEkle={() => router.push('/harcama-ekle')} />
        ) : veri ? (
          <>
            <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
              <View style={stil.aralik}>
                <View>
                  <Txt role="label" tone={color.text2}>
                    {t['ozet.hafta_toplam']}
                  </Txt>
                  <View style={{ height: rhythm.sameObject }} />
                  <Txt role="display" tone={tumHaftaLimitDisi ? color.warningInk : color.text}>
                    {paraYaz(haftaToplamKurus)}
                  </Txt>
                </View>
                <View style={stil.sagHiza}>
                  <Txt role="label" tone={color.text2}>
                    {buHaftaMi ? ozetGecenGunOrtalama(elapsedGunSayisi) : t['ozet.gunluk_ortalama']}
                  </Txt>
                  <View style={{ height: rhythm.sameObject }} />
                  <Txt role="amount">{paraYaz(gunlukOrtalamaKurus)}</Txt>
                </View>
              </View>
              <View style={{ height: rhythm.blockInCard }} />
              <View style={stil.aralik}>
                <Txt role="label" tone={color.text2}>
                  {t['ozet.gunluk_toplam']}
                </Txt>
                {veri.limitKurus !== null ? (
                  <View style={stil.limitEtiket}>
                    <View style={stil.cizgiOrnegi} />
                    <View style={{ width: rhythm.sameObject }} />
                    <Txt role="micro">{ozetLimitCizgisi(paraYaz(veri.limitKurus))}</Txt>
                  </View>
                ) : null}
              </View>
              <View style={{ height: rhythm.group }} />
              <WeekStrip gunler={gunler} limitKurus={veri.limitKurus} aktifIndex={aktifIndex} />
              <View style={{ height: rhythm.blockInCard }} />
              <InfoStrip
                variant={tumHaftaLimitDisi ? 'warning' : 'info'}
                metin={
                  tumHaftaLimitDisi
                    ? ozetLimitDisiGun(limitDisiGunSayisi)
                    : ozetLimitAltiGun(elapsedGunSayisi - limitDisiGunSayisi)
                }
              />
            </ClaySurface>

            {tumHaftaLimitDisi && !kartKapatildi && veri.limitKurus !== null ? (
              <>
                <View style={{ height: rhythm.section }} />
                <LimitReviewCard
                  asimSirasi={limitDisiGunSayisi}
                  baslikOverride={ozetLimitSorguBasligi(paraYaz(veri.limitKurus))}
                  onReview={() => router.push('/limitler')}
                  onDismiss={() => setKartKapatildi(true)}
                />
              </>
            ) : null}

            {veri.kategoriDagilimi.length > 0 ? (
              <>
                <View style={{ height: rhythm.section }} />
                <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
                  <View style={stil.aralik}>
                    <Txt role="h2">{t['ozet.kategori_dagilimi']}</Txt>
                    <Txt role="label" tone={color.text2}>
                      {ozetDagilimGun(elapsedGunSayisi)}
                    </Txt>
                  </View>
                  <View style={{ height: rhythm.group }} />
                  <View style={stil.segmentOluk}>
                    {veri.kategoriDagilimi.map((k) => (
                      <View
                        key={k.kategori}
                        style={[
                          stil.segmentDolgu,
                          {
                            width: `${(k.toplamKurus / Math.max(dagilimToplam, 1)) * 100}%`,
                            backgroundColor: aileRenkleri(kategori(k.kategori).aile).solid,
                          },
                        ]}
                      />
                    ))}
                  </View>
                  <View style={{ height: rhythm.blockInCard }} />
                  {veri.kategoriDagilimi.map((k, i) => (
                    <KategoriSatiri
                      key={k.kategori}
                      kategoriKodu={k.kategori}
                      pay={Math.round((k.toplamKurus / Math.max(dagilimToplam, 1)) * 100)}
                      tutarKurus={k.toplamKurus}
                      son={i === veri.kategoriDagilimi.length - 1}
                    />
                  ))}
                  <View style={{ height: rhythm.blockInCard }} />
                  <View style={stil.satir}>
                    <View style={stil.ikonKutu}>
                      <Icon name="trending-up" size={20} color={color.text2} />
                    </View>
                    <View style={{ width: rhythm.blockInCard }} />
                    <Txt role="caption" style={stil.esnek}>
                      {enCokKategori ? ozetEnCok(kategori(enCokKategori.kategori).ad) : ''}
                    </Txt>
                  </View>
                </ClaySurface>
              </>
            ) : null}

            {veri.kucukHarcama.adet > 0 ? (
              <>
                <View style={{ height: rhythm.section }} />
                <ClaySurface level="raised" borderRadius={radius.card} style={[stil.kart, stil.satirUst]}>
                  <View style={stil.esnek}>
                    <Txt role="label" tone={color.text2}>
                      {t['ozet.kucuk_harcama_baslik']}
                    </Txt>
                    <View style={{ height: rhythm.sameObject }} />
                    <Txt role="display">{sayiyaCevir(veri.kucukHarcama.toplamKurus)}</Txt>
                    <View style={{ height: rhythm.group }} />
                    <Txt role="caption">
                      {ozetKucukHarcamaAlt(
                        veri.kucukHarcama.adet,
                        paraYaz(Math.round(veri.kucukHarcama.toplamKurus / veri.kucukHarcama.adet)),
                      )}
                    </Txt>
                  </View>
                  <View style={{ width: rhythm.blockInCard }} />
                  <View style={[stil.katKab, { backgroundColor: aileRenkleri('amber').soft }]}>
                    <Icon name="coffee" size={20} color={aileRenkleri('amber').solid} />
                  </View>
                </ClaySurface>
              </>
            ) : null}

            {veri.gelecekAyTutarKurus > 0 ? (
              <>
                <View style={{ height: rhythm.section }} />
                <ClaySurface level="raised" borderRadius={radius.card} style={[stil.kart, stil.satirUst]}>
                  <View style={stil.esnek}>
                    <Txt role="bodyStrong">{ozetTaksitYuku(paraYaz(veri.gelecekAyTutarKurus, true))}</Txt>
                    <View style={{ height: rhythm.group }} />
                    <Txt role="caption">
                      {veri.gelecekAySonAy
                        ? taksitYukuAltMetni(veri.gelecekAySeriAdet, ayBasligi(veri.gelecekAySonAy))
                        : ''}
                    </Txt>
                    <View style={{ height: rhythm.blockInCard }} />
                    <Button
                      label={t['ozet.taksitleri_gor']}
                      variant="secondary"
                      auto
                      onPress={() => router.push('/taksitler')}
                    />
                  </View>
                  <View style={{ width: rhythm.blockInCard }} />
                  <View style={[stil.katKab, { backgroundColor: aileRenkleri('lacivert').soft }]}>
                    <Icon name="repeat" size={20} color={aileRenkleri('lacivert').solid} />
                  </View>
                </ClaySurface>
              </>
            ) : null}
          </>
        ) : null}
      </ScrollView>

      <View style={[stil.pad, { paddingBottom: layout.tabBarLift + insets.bottom }]}>
        <TabBar
          active="ozet"
          onSelect={(key) => {
            if (key === 'gunluk') router.replace('/');
            else if (key === 'kayitlar') router.push('/kayitlar');
          }}
          onAdd={() => router.push('/harcama-ekle')}
        />
      </View>
    </View>
  );
}

function HaftaDegistirici({
  skeleton,
  strong,
  caption,
  sonrakiKapali,
  onOnceki,
  onSonraki,
}: {
  skeleton: boolean;
  strong: string;
  caption: string;
  sonrakiKapali: boolean;
  onOnceki: () => void;
  onSonraki: () => void;
}) {
  return (
    <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.haftaSarma}>
      {skeleton ? (
        <View style={stil.haftaSatiri}>
          <Skeleton width={44} height={44} borderRadius={radius.pill} />
          <View style={stil.haftaOrta}>
            <Skeleton width={104} height={20} />
            <View style={{ height: rhythm.sameObject }} />
            <Skeleton width={136} height={16} />
          </View>
          <Skeleton width={44} height={44} borderRadius={radius.pill} />
        </View>
      ) : (
        <View style={stil.haftaSatiri}>
          <IconButton icon="chevron-left" accessibilityLabel={t['ozet.onceki_hafta']} onPress={onOnceki} />
          <View style={stil.haftaOrta}>
            <Txt role="bodyStrong">{strong}</Txt>
            <View style={{ height: rhythm.sameObject }} />
            <Txt role="caption" tone={color.text2}>
              {caption}
            </Txt>
          </View>
          <IconButton
            icon="chevron-right"
            accessibilityLabel={t['ozet.sonraki_hafta']}
            onPress={sonrakiKapali ? undefined : onSonraki}
          />
        </View>
      )}
    </ClaySurface>
  );
}

function KategoriSatiri({
  kategoriKodu,
  pay,
  tutarKurus,
  son,
}: {
  kategoriKodu: string;
  pay: number;
  tutarKurus: number;
  son: boolean;
}) {
  const kat = kategori(kategoriKodu);
  const renk = aileRenkleri(kat.aile);
  return (
    <Pressable
      onPress={() => router.push(`/kategori/${kategoriKodu}`)}
      accessibilityRole="button"
      accessibilityLabel={`${kat.ad}, ${ozetPay(pay)}, ${paraYaz(tutarKurus)}`}
      style={({ pressed }) => [
        stil.katSatiri,
        pressed && stil.katSatiriBasili,
        !son && !pressed ? stil.katSatiriAyrac : null,
      ]}>
      <View style={[stil.nokta, { backgroundColor: renk.solid }]} />
      <View style={{ width: rhythm.blockInCard }} />
      <Txt role="body" style={stil.esnek} numberOfLines={1}>
        {kat.ad}
      </Txt>
      <Txt role="caption" style={stil.payMetin}>
        {ozetPay(pay)}
      </Txt>
      <View style={{ width: rhythm.blockInCard }} />
      <Txt role="amount" style={stil.tutarMetin}>
        {paraYaz(tutarKurus)}
      </Txt>
    </Pressable>
  );
}

function BosHafta({ gunler, onEkle }: { gunler: WeekStripGun[]; onEkle: () => void }) {
  const bosGunler: WeekStripGun[] = gunler.length === 7 ? gunler : Array.from({ length: 7 }, () => ({ toplamKurus: 0, gelecek: true }));
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
      <WeekStrip gunler={bosGunler} limitKurus={null} />
      <View style={{ height: rhythm.blockInCard }} />
      <Txt role="h2">{t['bos.ozet.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body">{t['bos.ozet.govde']}</Txt>
      <View style={{ height: rhythm.blockInCard }} />
      <Button label={t['eylem.harcama_ekle']} variant="primary" icon="plus" onPress={onEkle} auto />
    </ClaySurface>
  );
}

function OzetKartiSkeleton() {
  return (
    <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
      <View style={stil.aralik}>
        <View>
          <Skeleton width={112} height={18} />
          <View style={{ height: rhythm.sameObject }} />
          <Skeleton width={136} height={32} />
        </View>
        <View style={stil.sagHiza}>
          <Skeleton width={104} height={18} />
          <View style={{ height: rhythm.sameObject }} />
          <Skeleton width={72} height={24} />
        </View>
      </View>
      <View style={{ height: rhythm.blockInCard }} />
      <Skeleton width="100%" height={104} borderRadius={radius.tile} />
    </ClaySurface>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  kart: { padding: rhythm.pad },
  satirUst: { flexDirection: 'row', alignItems: 'flex-start' },
  aralik: { flexDirection: 'row', alignItems: 'flex-start', justifyContent: 'space-between' },
  sagHiza: { alignItems: 'flex-end' },
  esnek: { flex: 1, minWidth: 0 },
  limitEtiket: { flexDirection: 'row', alignItems: 'center' },
  cizgiOrnegi: { width: 16, height: 2, borderRadius: radius.pill, backgroundColor: color.text2 },
  haftaSarma: { padding: rhythm.pad },
  haftaSatiri: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  haftaOrta: { alignItems: 'center' },
  segmentOluk: {
    flexDirection: 'row',
    height: 12,
    borderRadius: radius.pill,
    backgroundColor: color.groove,
    boxShadow: clay.sunken,
    overflow: 'hidden',
  },
  segmentDolgu: { height: 12 },
  katSatiri: { flexDirection: 'row', alignItems: 'center', minHeight: 44, paddingVertical: rhythm.sameObject },
  katSatiriBasili: { backgroundColor: color.groove, borderRadius: radius.tile, marginHorizontal: -8, paddingHorizontal: 8 },
  katSatiriAyrac: { borderBottomWidth: 1, borderBottomColor: color.line },
  nokta: { width: 8, height: 8, borderRadius: radius.pill },
  payMetin: { width: 40, textAlign: 'right' },
  tutarMetin: { width: 88, textAlign: 'right' },
  satir: { flexDirection: 'row', alignItems: 'flex-start' },
  ikonKutu: { width: 20, height: 20 },
  katKab: { width: 44, height: 44, borderRadius: radius.tile, alignItems: 'center', justifyContent: 'center' },
});
