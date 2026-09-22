import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { BottomSheet } from '@/components/BottomSheet';
import { Button } from '@/components/Button';
import { ClayKeypad } from '@/components/ClayKeypad';
import { ClaySurface } from '@/components/ClaySurface';
import { EquationRow } from '@/components/EquationRow';
import { ErrorState } from '@/components/ErrorState';
import { IconButton } from '@/components/IconButton';
import { InfoStrip } from '@/components/InfoStrip';
import { ShareBar } from '@/components/ShareBar';
import { ShareRow } from '@/components/ShareRow';
import { Skeleton } from '@/components/Skeleton';
import { Slider } from '@/components/Slider';
import { Txt } from '@/components/Txt';
import {
  abonelikFormulMetni,
  planAliskanlikSatirAlt,
  planAralikEnCok,
  planAliskanlikToplamNot,
  planAyarAltMetin,
  planAyarDegisim,
  planDenklemKalanGun,
  planEksiKalan,
  planEksiTutar,
  planGelirEtiketi,
  planGelirsizAylikTahmin,
  planNasil1,
  planNasil2,
  planNasil3,
  planNasil4,
  planPayYatirim,
  planYuzde,
  t,
} from '@/content/metinler';
import { siklikEtiketi } from '@/components/FrequencyChips';
import { ApiAgHatasi, ApiHatasi } from '@/lib/api';
import { gunlukLimitKaydet } from '@/db/limitler';
import {
  abonelikSatiriKurus,
  aliskanlikSatiriKurus,
  planKur,
  profilDetayAlanKaydet,
  profilDetayOku,
  profilOku,
  type ProfilDetay,
} from '@/db/profil';
import {
  birikimKurus,
  birikimYuzdeUstSiniri,
  dagitimYuzdeleri,
  eksikKurus,
  gunlukLimitKurus,
  kalanGun,
  planNegatifMi,
  sosyalKurus,
  yatirimPayiKurus,
  yatirimYuzdeVarsayimi,
  zorunluKurus,
} from '@/lib/plan';
import { paraYaz, tutarGirisiEkle, tutarGirisindenKurus, tutarGirisiSil, tutarGosterimi } from '@/lib/para';
import { toastGoster } from '@/lib/toastBus';
import { color, layout, radius, rhythm, share } from '@/theme/tokens';

type Durum =
  | { tip: 'yukleniyor' }
  | { tip: 'hata' }
  | { tip: 'gelirsiz'; detay: ProfilDetay }
  | { tip: 'eksi'; detay: ProfilDetay; gelirKurus: number; zorunlu: number }
  | { tip: 'plan'; detay: ProfilDetay; gelirKurus: number; gunSayisi: number };

export default function PlanEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();
  const [durum, setDurum] = useState<Durum>({ tip: 'yukleniyor' });
  const [nasilGoster, setNasilGoster] = useState(false);
  const [limitBuffer, setLimitBuffer] = useState('');
  const [kaydediliyor, setKaydediliyor] = useState(false);

  const yukle = useCallback(() => {
    let iptal = false;
    setDurum({ tip: 'yukleniyor' });
    Promise.all([profilDetayOku(db), profilOku(db)])
      .then(([detay, profil]) => {
        if (iptal) return;
        if (!profil.gelirKurus || profil.gelirKurus <= 0) {
          setDurum({ tip: 'gelirsiz', detay });
          return;
        }
        const zorunlu = zorunluKurus({
          kiraAidatKurus: detay.kiraAidatKurus,
          faturalarKurus: detay.faturalarKurus,
          ulasimYakitKurus: detay.ulasimYakitKurus,
          krediTaksitKurus: detay.krediTaksitKurus,
        });
        if (planNegatifMi(profil.gelirKurus, zorunlu)) {
          setDurum({ tip: 'eksi', detay, gelirKurus: profil.gelirKurus, zorunlu });
          return;
        }
        const gunSayisi = kalanGun(new Date(), profil.maasDuzensiz ? null : profil.maasGunu);
        setDurum({ tip: 'plan', detay, gelirKurus: profil.gelirKurus, gunSayisi });
      })
      .catch(() => {
        if (!iptal) setDurum({ tip: 'hata' });
      });
    return () => {
      iptal = true;
    };
  }, [db]);

  useEffect(() => yukle(), [yukle]);

  /** Ağ/sunucu hatasında sessizce başarısız OLMAZ (K-029): kaydediliyor biter, ekranda kalınır. */
  function hataMetniGoster() {
    toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
  }

  function habitToplamlari(detay: ProfilDetay) {
    return {
      kafe: aliskanlikSatiriKurus(detay.kahve),
      restoran: aliskanlikSatiriKurus(detay.yemek),
      abonelik: abonelikSatiriKurus(detay),
      aliskanliklar: aliskanlikSatiriKurus(detay.sigara) + aliskanlikSatiriKurus(detay.alkol),
    };
  }

  async function limitiKaydet(detay: ProfilDetay) {
    const kurus = tutarGirisindenKurus(limitBuffer);
    if (kurus <= 0 || kaydediliyor) return;
    setKaydediliyor(true);
    try {
      await gunlukLimitKaydet(db, kurus);
      router.replace('/');
    } catch {
      // Ağ/sunucu hatası — sessizce başarılı gösterilmez (K-029), ekranda kalınır.
      hataMetniGoster();
    } finally {
      setKaydediliyor(false);
    }
  }

  async function planiKur(detay: ProfilDetay, gunlukLimit: number) {
    if (kaydediliyor) return;
    setKaydediliyor(true);
    try {
      await planKur(db, gunlukLimit, habitToplamlari(detay));
      router.replace('/');
    } catch (e) {
      if (e instanceof ApiHatasi || e instanceof ApiAgHatasi) hataMetniGoster();
      else throw e;
    } finally {
      setKaydediliyor(false);
    }
  }

  if (durum.tip === 'yukleniyor') {
    return <YukleniyorEkrani insetTop={insets.top} />;
  }

  if (durum.tip === 'hata') {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <View style={stil.basSatiri}>
          <IconButton icon="chevron-left" accessibilityLabel={t['eylem.geri']} onPress={() => router.back()} />
          <Txt role="micro" tone={color.text2}>
            {t['plan.ustbaslik']}
          </Txt>
          <View style={stil.basDenge} />
        </View>
        <View style={stil.pad}>
          <ErrorState onRetry={yukle} />
        </View>
      </View>
    );
  }

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <View style={stil.basSatiri}>
        <IconButton icon="chevron-left" accessibilityLabel={t['eylem.geri']} onPress={() => router.back()} />
        <Txt role="micro" tone={color.text2}>
          {t['plan.ustbaslik']}
        </Txt>
        <View style={stil.basDenge} />
      </View>

      {durum.tip === 'gelirsiz' ? (
        <GelirsizIcerik
          detay={durum.detay}
          insetBottom={insets.bottom}
          buffer={limitBuffer}
          onDigit={(d) => setLimitBuffer((b) => tutarGirisiEkle(b, d))}
          onComma={() => setLimitBuffer((b) => tutarGirisiEkle(b, ','))}
          onBackspace={() => setLimitBuffer((b) => tutarGirisiSil(b))}
          onKaydet={() => void limitiKaydet(durum.detay)}
          kaydediliyor={kaydediliyor}
        />
      ) : null}

      {durum.tip === 'eksi' ? <EksiIcerik gelirKurus={durum.gelirKurus} zorunlu={durum.zorunlu} /> : null}

      {durum.tip === 'plan' ? (
        <PlanIcerik
          db={db}
          detay={durum.detay}
          setDetay={(d) => setDurum({ ...durum, detay: d })}
          gelirKurus={durum.gelirKurus}
          gunSayisi={durum.gunSayisi}
          insetBottom={insets.bottom}
          nasilGoster={nasilGoster}
          onNasilAc={() => setNasilGoster(true)}
          onNasilKapat={() => setNasilGoster(false)}
          onPlaniKur={(limit) => void planiKur(durum.detay, limit)}
          kaydediliyor={kaydediliyor}
        />
      ) : null}
    </View>
  );
}

function YukleniyorEkrani({ insetTop }: { insetTop: number }) {
  return (
    <View style={stil.ekran}>
      <View style={{ height: insetTop }} />
      <View style={[stil.pad, { paddingTop: layout.headerPadTop }]}>
        <Skeleton width="70%" height={28} />
        <View style={{ height: rhythm.group }} />
        <Skeleton width="100%" height={16} />
        <View style={{ height: rhythm.section }} />
        <Skeleton width="100%" height={180} borderRadius={radius.card} />
        <View style={{ height: rhythm.section }} />
        <Skeleton width="100%" height={140} borderRadius={radius.card} />
      </View>
    </View>
  );
}

function GelirsizIcerik({
  detay,
  insetBottom,
  buffer,
  onDigit,
  onComma,
  onBackspace,
  onKaydet,
  kaydediliyor,
}: {
  detay: ProfilDetay;
  insetBottom: number;
  buffer: string;
  onDigit: (d: string) => void;
  onComma: () => void;
  onBackspace: () => void;
  onKaydet: () => void;
  kaydediliyor: boolean;
}) {
  const aylikToplam =
    aliskanlikSatiriKurus(detay.kahve) +
    aliskanlikSatiriKurus(detay.sigara) +
    aliskanlikSatiriKurus(detay.alkol) +
    aliskanlikSatiriKurus(detay.yemek) +
    abonelikSatiriKurus(detay);
  const gunlukKurus = tutarGirisindenKurus(buffer);
  return (
    <>
      <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
        <View style={{ height: rhythm.section }} />
        <Txt role="h1">{t['plan.gelirsiz.baslik']}</Txt>
        <View style={{ height: rhythm.group }} />
        <Txt role="body" tone={color.text2}>
          {t['plan.gelirsiz.aciklama']}
        </Txt>
        <View style={{ height: rhythm.section }} />
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <Txt role="label" tone={color.text2}>
            {t['plan.gelirsiz.limit_etiket']}
          </Txt>
          <View style={{ height: rhythm.group }} />
          <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.gelirKuyu}>
            <View style={stil.gelirSatir}>
              <Txt role="hero" tone={buffer ? undefined : color.text3}>
                {tutarGosterimi(buffer)}
              </Txt>
              <View style={{ width: rhythm.group }} />
              <Txt role="display" tone={color.text2}>
                ₺
              </Txt>
            </View>
          </ClaySurface>
          {gunlukKurus > 0 ? (
            <>
              <View style={{ height: rhythm.group }} />
              <Txt role="caption">{planGelirsizAylikTahmin(paraYaz(gunlukKurus * 30))}</Txt>
            </>
          ) : null}
        </ClaySurface>
        <View style={{ height: rhythm.section }} />
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <Txt role="h2">{t['plan.gelirsiz.elimizde_baslik']}</Txt>
          <View style={{ height: rhythm.sameObject }} />
          <Txt role="label" tone={color.text2}>
            {t['plan.gelirsiz.elimizde_alt']}
          </Txt>
          <View style={{ height: rhythm.pad }} />
          <Txt role="body">{t['plan.gelirsiz.eldeki']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{t['plan.gelirsiz.eldeki_alt']}</Txt>
          {aylikToplam > 0 ? (
            <>
              <View style={{ height: rhythm.pad }} />
              <View style={stil.aralikSatiri}>
                <Txt role="bodyStrong">{t['plan.gelirsiz.aylik_toplam']}</Txt>
                <Txt role="amount">{paraYaz(aylikToplam)}</Txt>
              </View>
              <View style={{ height: rhythm.blockInCard }} />
              <Txt role="caption">{t['plan.gelirsiz.limit_not']}</Txt>
            </>
          ) : null}
        </ClaySurface>
        <View style={{ height: rhythm.section }} />
        <InfoStrip variant="info" metin={`${t['plan.gelirsiz.sonra']} ${t['plan.gelirsiz.sonra_alt']}`} />
        <View style={{ height: rhythm.section }} />
      </ScrollView>
      <View style={[stil.altSabit, { paddingBottom: insetBottom }]}>
        <View style={stil.pad}>
          <ClayKeypad onDigit={onDigit} onComma={onComma} onBackspace={onBackspace} />
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <View style={stil.pad}>
          <Button label={t['plan.gelirsiz.kaydet']} variant="primary" disabled={gunlukKurus <= 0} loading={kaydediliyor} onPress={onKaydet} />
        </View>
      </View>
    </>
  );
}

function EksiIcerik({ gelirKurus, zorunlu }: { gelirKurus: number; zorunlu: number }) {
  const eksik = eksikKurus(gelirKurus, zorunlu);
  return (
    <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false}>
      <View style={{ height: rhythm.section }} />
      <Txt role="h1">{t['plan.eksi.baslik']}</Txt>
      <View style={{ height: rhythm.group }} />
      <Txt role="body" tone={color.text2}>
        {t['plan.eksi.aciklama']}
      </Txt>
      <View style={{ height: rhythm.section }} />
      <InfoStrip variant="warning" metin={`${planEksiTutar(paraYaz(eksik))} ${t['plan.eksi.normalize']}`} />
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
        <View style={stil.aralikSatiri}>
          <Txt role="h2">{t['plan.eksi.hesap']}</Txt>
          <Txt role="label" tone={color.text2}>
            {t['plan.eksi.bu_ay']}
          </Txt>
        </View>
        <View style={{ height: rhythm.pad }} />
        <View style={stil.aralikSatiri}>
          <Txt role="body">{t['plan.eksi.net_gelir']}</Txt>
          <Txt role="amount">{paraYaz(gelirKurus)}</Txt>
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <View style={stil.aralikSatiri}>
          <Txt role="body">{t['plan.eksi.sabit_giderler']}</Txt>
          <Txt role="amount">{paraYaz(zorunlu)}</Txt>
        </View>
        <View style={{ height: rhythm.pad }} />
        <View style={stil.aralikSatiri}>
          <Txt role="bodyStrong">{t['plan.eksi.kalan_etiket']}</Txt>
          <Txt role="amount" tone={color.warningInk}>
            {planEksiKalan(paraYaz(eksik))}
          </Txt>
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <Txt role="caption">{t['plan.eksi.yuzde_yok']}</Txt>
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
      <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
        <View style={stil.aralikSatiri}>
          <Txt role="h2">{t['plan.eksi.cikis_baslik']}</Txt>
          <Txt role="label" tone={color.text2}>
            {t['plan.eksi.cikis_alt']}
          </Txt>
        </View>
        <View style={{ height: rhythm.pad }} />
        <Txt role="body">{t['plan.eksi.uc_yol']}</Txt>
        <View style={{ height: rhythm.pad }} />
        <Button label={t['plan.eksi.yol1']} variant="primary" onPress={() => router.push({ pathname: '/tanisma', params: { kart: '1' } })} />
        <View style={{ height: rhythm.group }} />
        <Txt role="caption">{t['plan.eksi.yol1.alt']}</Txt>
        <View style={{ height: rhythm.pad }} />
        <Button label={t['plan.eksi.yol2']} variant="secondary" onPress={() => router.push('/limitler')} />
        <View style={{ height: rhythm.group }} />
        <Txt role="caption">{t['plan.eksi.yol2.alt']}</Txt>
        <View style={{ height: rhythm.pad }} />
        <Button label={t['plan.eksi.yol3']} variant="ghost" onPress={() => router.replace('/')} />
        <View style={{ height: rhythm.group }} />
        <Txt role="caption">{t['plan.eksi.yol3.alt']}</Txt>
      </ClaySurface>
      <View style={{ height: rhythm.section }} />
    </ScrollView>
  );
}

function PlanIcerik({
  db,
  detay,
  setDetay,
  gelirKurus,
  gunSayisi,
  insetBottom,
  nasilGoster,
  onNasilAc,
  onNasilKapat,
  onPlaniKur,
  kaydediliyor,
}: {
  db: ReturnType<typeof useSQLiteContext>;
  detay: ProfilDetay;
  setDetay: (d: ProfilDetay) => void;
  gelirKurus: number;
  gunSayisi: number;
  insetBottom: number;
  nasilGoster: boolean;
  onNasilAc: () => void;
  onNasilKapat: () => void;
  onPlaniKur: (gunlukLimitKurus: number) => void;
  kaydediliyor: boolean;
}) {
  const zorunlu = zorunluKurus({
    kiraAidatKurus: detay.kiraAidatKurus,
    faturalarKurus: detay.faturalarKurus,
    ulasimYakitKurus: detay.ulasimYakitKurus,
    krediTaksitKurus: detay.krediTaksitKurus,
  });
  const birikimVar = detay.birikimYuzde !== null;
  const birikimYuzdeGosterim = detay.birikimYuzde ?? 0;
  const birikim = birikimVar ? birikimKurus(gelirKurus, birikimYuzdeGosterim) : 0;
  const sosyal = sosyalKurus(gelirKurus, zorunlu, birikim);
  const yuzdeler = dagitimYuzdeleri(gelirKurus, zorunlu, sosyal, birikim);
  const gunlukLimit = gunlukLimitKurus(sosyal, gunSayisi);

  const [oncekiLimit, setOncekiLimit] = useState<number | null>(null);
  const max = birikimYuzdeUstSiniri(gelirKurus, zorunlu);

  const yatirimYuzde = yatirimYuzdeVarsayimi(detay.yatirimNiyet);
  const yatirimPayi = birikimVar ? yatirimPayiKurus(birikim, yatirimYuzde) : 0;

  const kahveSatiri = aliskanlikSatiriKurus(detay.kahve);
  const sigaraSatiri = aliskanlikSatiriKurus(detay.sigara);
  const alkolSatiri = aliskanlikSatiriKurus(detay.alkol);
  const yemekSatiri = aliskanlikSatiriKurus(detay.yemek);
  const abonelikSatiri = abonelikSatiriKurus(detay);
  const aliskanlikToplam = kahveSatiri + sigaraSatiri + alkolSatiri + yemekSatiri + abonelikSatiri;

  function birikimDegistir(yuzde: number) {
    setOncekiLimit(gunlukLimit);
    setDetay({ ...detay, birikimYuzde: yuzde });
    void profilDetayAlanKaydet(db, 'birikim_yuzde', yuzde);
  }

  const basligBaslik = birikimVar ? t['plan.baslik'] : t['plan.yarim.baslik'];
  const basligAciklama = birikimVar ? t['plan.aciklama'] : t['plan.yarim.aciklama'];

  return (
    <>
      <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false}>
        <View style={{ height: rhythm.section }} />
        <Txt role="h1">{basligBaslik}</Txt>
        <View style={{ height: rhythm.group }} />
        <Txt role="body" tone={color.text2}>
          {basligAciklama}
        </Txt>
        <View style={{ height: rhythm.section }} />

        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <View style={stil.aralikSatiri}>
            <Txt role="h2">{t['plan.aylik_planin']}</Txt>
            <Txt role="label" tone={color.text2}>
              {planGelirEtiketi(paraYaz(gelirKurus))}
            </Txt>
          </View>
          <View style={{ height: rhythm.pad }} />
          <ShareBar
            segments={[
              { color: share.zorunlu, kurus: zorunlu },
              { color: share.sosyal, kurus: Math.max(0, sosyal) },
              { color: share.birikim, kurus: birikim },
            ]}
            toplamKurus={gelirKurus}
          />
          <View style={{ height: rhythm.pad }} />
          <ShareRow
            dotColor={share.zorunlu}
            ad={t['plan.pay.zorunlu']}
            aciklama={t['plan.pay.zorunlu.alt']}
            tutarYazi={paraYaz(zorunlu)}
            yuzdeYazi={planYuzde(yuzdeler.zorunlu)}
          />
          <View style={{ height: rhythm.blockInCard }} />
          <ShareRow
            dotColor={share.sosyal}
            ad={t['plan.pay.sosyal']}
            aciklama={t['plan.pay.sosyal.alt']}
            tutarYazi={paraYaz(Math.max(0, sosyal))}
            yuzdeYazi={planYuzde(yuzdeler.sosyal)}
          />
          <View style={{ height: rhythm.blockInCard }} />
          <ShareRow
            dotColor={share.birikim}
            ad={t['plan.pay.birikim']}
            aciklama={birikimVar ? (yatirimPayi > 0 ? planPayYatirim(paraYaz(yatirimPayi)) : '') : t['plan.yarim.birikim']}
            tutarYazi={birikimVar ? paraYaz(birikim) : null}
            yuzdeYazi={birikimVar ? planYuzde(yuzdeler.birikim) : null}
          />
          {!birikimVar ? (
            <>
              <View style={{ height: rhythm.pad }} />
              <Txt role="caption">{t['plan.yarim.not']}</Txt>
            </>
          ) : null}
        </ClaySurface>

        <View style={{ height: rhythm.section }} />
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <View style={stil.aralikSatiri}>
            <Txt role="h2">{t['plan.limit.baslik']}</Txt>
            <Txt role="label" tone={color.text2}>
              {t['plan.turetildi']}
            </Txt>
          </View>
          <View style={{ height: rhythm.pad }} />
          <EquationRow
            items={[
              { value: paraYaz(Math.max(0, sosyal)), label: t['plan.denklem.sosyal'] },
              { value: planDenklemKalanGun(gunSayisi), label: t['plan.denklem.kalan_gun'] },
              { value: paraYaz(gunlukLimit), label: t['plan.denklem.gunluk'] },
            ]}
          />
          <View style={{ height: rhythm.pad }} />
          <InfoStrip variant="info" metin={`${t['plan.limit.pano']} ${t['plan.limit.pano.alt']}`} />
          {!birikimVar ? (
            <>
              <View style={{ height: rhythm.blockInCard }} />
              <Txt role="caption">{t['plan.yarim.limit_not']}</Txt>
            </>
          ) : oncekiLimit !== null && oncekiLimit !== gunlukLimit ? (
            <>
              <View style={{ height: rhythm.blockInCard }} />
              <Txt role="caption">{planAyarDegisim(paraYaz(Math.abs(oncekiLimit - gunlukLimit)), gunlukLimit < oncekiLimit)}</Txt>
            </>
          ) : null}
          <View style={{ height: rhythm.blockInCard }} />
          <Button label={t['plan.nasil']} variant="ghost" auto icon="info" onPress={onNasilAc} />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <View style={stil.aralikSatiri}>
            <Txt role="h2">{t['plan.aliskanlik.baslik']}</Txt>
            <Txt role="label" tone={color.text2}>
              {t['plan.aliskanlik.sag']}
            </Txt>
          </View>
          <View style={{ height: rhythm.pad }} />
          {aliskanlikToplam > 0 ? (
            <>
              {kahveSatiri > 0 ? (
                <AliskanlikSatiri baslik={t['tan.kahve.baslik']} alt={planAliskanlikSatirAlt(siklikEtiketi(detay.kahve.siklik!), paraYaz(detay.kahve.fiyatKurus ?? 0))} tutar={kahveSatiri} />
              ) : null}
              {yemekSatiri > 0 ? (
                <AliskanlikSatiri baslik={t['tan.yemek.baslik']} alt={planAliskanlikSatirAlt(siklikEtiketi(detay.yemek.siklik!), paraYaz(detay.yemek.fiyatKurus ?? 0))} tutar={yemekSatiri} />
              ) : null}
              {alkolSatiri > 0 ? (
                <AliskanlikSatiri baslik={t['tan.alkol.baslik']} alt={planAliskanlikSatirAlt(siklikEtiketi(detay.alkol.siklik!), paraYaz(detay.alkol.fiyatKurus ?? 0))} tutar={alkolSatiri} />
              ) : null}
              {sigaraSatiri > 0 ? (
                <AliskanlikSatiri baslik={t['tan.sigara.baslik']} alt={planAliskanlikSatirAlt(siklikEtiketi(detay.sigara.siklik!), paraYaz(detay.sigara.fiyatKurus ?? 0))} tutar={sigaraSatiri} />
              ) : null}
              {abonelikSatiri > 0 ? (
                <AliskanlikSatiri
                  baslik={t['tan.abonelik.baslik']}
                  alt={abonelikFormulMetni(detay.abonelikAdet ?? 0, paraYaz(detay.abonelikOrtalamaKurus ?? 0))}
                  tutar={abonelikSatiri}
                />
              ) : null}
              <View style={{ height: rhythm.pad }} />
              <View style={stil.aralikSatiri}>
                <Txt role="bodyStrong">{t['tan.sabit.toplam']}</Txt>
                <Txt role="amount">{paraYaz(aliskanlikToplam)}</Txt>
              </View>
              <View style={{ height: rhythm.blockInCard }} />
              <Txt role="caption">{planAliskanlikToplamNot(paraYaz(aliskanlikToplam))}</Txt>
            </>
          ) : (
            <>
              <Txt role="body">{t['plan.aliskanlik.bos']}</Txt>
              <View style={{ height: rhythm.group }} />
              <Txt role="caption">{t['plan.aliskanlik.bos.alt']}</Txt>
              <View style={{ height: rhythm.pad }} />
              <Button label={t['plan.aliskanlik.kartlara_don']} variant="secondary" auto onPress={() => router.push('/tanisma')} />
            </>
          )}
        </ClaySurface>

        <View style={{ height: rhythm.section }} />
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kartIc}>
          <View style={stil.aralikSatiri}>
            <Txt role="h2">{t['plan.ayar.baslik']}</Txt>
            <Txt role="label" tone={color.text2}>
              {t['plan.ayar.tek_kaydirici']}
            </Txt>
          </View>
          <View style={{ height: rhythm.pad }} />
          <View style={stil.aralikSatiri}>
            <Txt role="label" tone={color.text2}>
              {t['plan.ayar.etiket']}
            </Txt>
            <Txt role="display">%{birikimYuzdeGosterim}</Txt>
          </View>
          <View style={{ height: rhythm.group }} />
          <Slider value={birikimYuzdeGosterim} max={max} onChange={birikimDegistir} accessibilityLabel={t['plan.ayar.etiket']} />
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{planAyarAltMetin(paraYaz(birikim))}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <View style={stil.aralikSatiri}>
            <Txt role="micro" tone={color.text2}>
              {t['plan.ayar.aralik_en_az']}
            </Txt>
            <Txt role="micro" tone={color.text2}>
              {planAralikEnCok(max)}
            </Txt>
          </View>
          <View style={{ height: rhythm.blockInCard }} />
          <Txt role="caption">{t['plan.ayar.not']}</Txt>
        </ClaySurface>

        <View style={{ height: rhythm.section }} />
      </ScrollView>

      <View style={[stil.altSabit, { paddingBottom: insetBottom }]}>
        <View style={stil.pad}>
          <Button label={t['plan.kur']} variant="primary" loading={kaydediliyor} onPress={() => onPlaniKur(gunlukLimit)} />
          <View style={{ height: rhythm.group }} />
          <Button label={t['eylem.simdi_degil']} variant="ghost" onPress={() => router.back()} />
        </View>
      </View>

      <BottomSheet visible={nasilGoster} onClose={onNasilKapat}>
        <NasilHesaplandiIcerik
          detay={detay}
          gelirKurus={gelirKurus}
          zorunlu={zorunlu}
          birikimVar={birikimVar}
          birikimYuzde={birikimYuzdeGosterim}
          birikim={birikim}
          sosyal={sosyal}
          gunSayisi={gunSayisi}
          gunlukLimit={gunlukLimit}
          onKapat={onNasilKapat}
        />
      </BottomSheet>
    </>
  );
}

function AliskanlikSatiri({ baslik, alt, tutar }: { baslik: string; alt: string; tutar: number }) {
  return (
    <View style={stil.aliskanlikSatiri}>
      <View style={stil.esnek}>
        <Txt role="bodyStrong">{baslik}</Txt>
        <View style={{ height: rhythm.sameObject }} />
        <Txt role="caption">{alt}</Txt>
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      <Txt role="amount">{paraYaz(tutar)}</Txt>
    </View>
  );
}

function NasilHesaplandiIcerik({
  detay,
  gelirKurus,
  zorunlu,
  birikimVar,
  birikimYuzde,
  birikim,
  sosyal,
  gunSayisi,
  gunlukLimit,
  onKapat,
}: {
  detay: ProfilDetay;
  gelirKurus: number;
  zorunlu: number;
  birikimVar: boolean;
  birikimYuzde: number;
  birikim: number;
  sosyal: number;
  gunSayisi: number;
  gunlukLimit: number;
  onKapat: () => void;
}) {
  const kalemler = [detay.kiraAidatKurus, detay.faturalarKurus, detay.ulasimYakitKurus, detay.krediTaksitKurus]
    .filter((k): k is number => k !== null && k > 0)
    .map((k) => paraYaz(k));
  return (
    <ScrollView showsVerticalScrollIndicator={false}>
      <View style={stil.sheetBaslikSatiri}>
        <Txt role="micro" tone={color.text2} style={stil.esnek}>
          {t['plan.nasil.hesap']}
        </Txt>
        <IconButton icon="x" accessibilityLabel={t['eylem.kapat']} onPress={onKapat} />
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="h1">{t['plan.nasil']}</Txt>
      <View style={{ height: rhythm.section }} />
      <NumaraliSatir n={1} metin={planNasil1(kalemler.length > 0 ? kalemler : [paraYaz(0)], paraYaz(zorunlu))} />
      <View style={{ height: rhythm.pad }} />
      <NumaraliSatir n={2} metin={birikimVar ? planNasil2(paraYaz(gelirKurus), birikimYuzde, paraYaz(birikim)) : t['plan.yarim.birikim']} />
      <View style={{ height: rhythm.pad }} />
      <NumaraliSatir n={3} metin={planNasil3(paraYaz(gelirKurus), paraYaz(zorunlu), paraYaz(birikim), paraYaz(Math.max(0, sosyal)))} />
      <View style={{ height: rhythm.pad }} />
      <NumaraliSatir n={4} metin={planNasil4(paraYaz(Math.max(0, sosyal)), gunSayisi, paraYaz(gunlukLimit))} />
      <View style={{ height: rhythm.section }} />
      <InfoStrip variant="info" metin={`${t['plan.nasil.yuvarlama']} ${t['plan.nasil.yuvarlama.alt']}`} />
      <View style={{ height: rhythm.section }} />
      <Button label={t['plan.nasil.anladim']} variant="secondary" onPress={onKapat} />
    </ScrollView>
  );
}

function NumaraliSatir({ n, metin }: { n: number; metin: string }) {
  return (
    <View style={stil.numaraSatir}>
      <View style={stil.numaraKutu}>
        <Txt role="label" tone={color.text2}>
          {n}
        </Txt>
      </View>
      <View style={{ width: rhythm.blockInCard }} />
      <Txt role="caption" style={stil.esnek}>
        {metin}
      </Txt>
    </View>
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
  aralikSatiri: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  aliskanlikSatiri: { flexDirection: 'row', alignItems: 'flex-start', marginBottom: rhythm.blockInCard },
  gelirKuyu: { padding: rhythm.pad, alignItems: 'center' },
  gelirSatir: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center' },
  altSabit: { paddingTop: rhythm.group, backgroundColor: color.bg },
  sheetBaslikSatiri: { flexDirection: 'row', alignItems: 'center' },
  numaraSatir: { flexDirection: 'row', alignItems: 'flex-start' },
  numaraKutu: { width: 12, alignItems: 'flex-start' },
});
