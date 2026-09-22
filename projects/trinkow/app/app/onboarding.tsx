import { router } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { BottomSheet } from '@/components/BottomSheet';
import { Button } from '@/components/Button';
import { Chip } from '@/components/Chip';
import { ClayKeypad } from '@/components/ClayKeypad';
import { ClaySurface } from '@/components/ClaySurface';
import { DayBox } from '@/components/DayBox';
import { EquationRow } from '@/components/EquationRow';
import { Icon } from '@/components/Icon';
import { IconButton } from '@/components/IconButton';
import { InfoStrip } from '@/components/InfoStrip';
import { OptionCard } from '@/components/OptionCard';
import { StepIndicator } from '@/components/StepIndicator';
import { SuggestionTag } from '@/components/SuggestionTag';
import { Txt } from '@/components/Txt';
import {
  a11yObGun,
  obMaasDonem,
  obOzetMaasGunu,
  oneriDenklemKalanGun,
  oneriNasil1,
  oneriNasil3,
  t,
} from '@/content/metinler';
import { onboardingKaydet, oneriKabulEt, oneriReddet, type Niyet } from '@/db/profil';
import { kalanGun, oneriLimitKurus, oneriSosyalKurus } from '@/lib/plan';
import { paraYaz, tutarGirisiEkle, tutarGirisindenKurus, tutarGirisiSil, tutarGosterimi } from '@/lib/para';
import { gunBulunmaEki, gunIyelikEki } from '@/lib/tarih';
import { toastGoster } from '@/lib/toastBus';
import { clay, color, layout, radius, rhythm, v4 } from '@/theme/tokens';

type Adim = 1 | 2 | 3;

type OneriDetay = {
  gelirKurus: number;
  sosyalKurus: number;
  gunSayisi: number;
  oneriKurus: number;
};

const NIYET_KART: { id: Niyet; icon: 'target' | 'landmark' | 'trending-up'; baslik: string; alt: string }[] = [
  { id: 'takip', icon: 'target', baslik: t['ob.niyet.takip'], alt: t['ob.niyet.takip.alt'] },
  { id: 'tasarruf', icon: 'landmark', baslik: t['ob.niyet.tasarruf'], alt: t['ob.niyet.tasarruf.alt'] },
  { id: 'borc', icon: 'trending-up', baslik: t['ob.niyet.borc'], alt: t['ob.niyet.borc.alt'] },
];

const NIYET_ONIZLEME: Record<Niyet, string> = {
  takip: t['pano.hero.takip'],
  tasarruf: t['pano.hero.tasarruf'],
  borc: t['pano.hero.borc'],
};

const NIYET_OZET: Record<Niyet, string> = {
  takip: t['pano.kip.takip'],
  tasarruf: t['pano.kip.tasarruf'],
  borc: t['pano.kip.borc'],
};

const ADIM_ETIKET: Record<Adim, string> = { 1: t['ob.adim'], 2: t['ob.adim2'], 3: t['ob.adim3'] };

/**
 * E-01…E-03 · Katman 1 onboarding (K-053, 3 zorunlu soru) + K-059/5 günlük
 * limit önerisi sheet'i. Tek ekran, üç iç adım (`limitler.tsx`'teki
 * "iç görünüm" desenini izler) — router stack'i büyütmeden geri/ileri.
 */
export default function OnboardingEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [adim, setAdim] = useState<Adim>(1);
  const [niyet, setNiyet] = useState<Niyet | null>(null);
  const [gelirBuffer, setGelirBuffer] = useState('');
  const [maasGunu, setMaasGunu] = useState<number | null>(null);
  const [maasDuzensiz, setMaasDuzensiz] = useState(false);
  const [kaydediliyor, setKaydediliyor] = useState(false);

  const [oneriGoster, setOneriGoster] = useState(false);
  const [oneriDetay, setOneriDetay] = useState<OneriDetay | null>(null);

  const gelirKurusGuncel = tutarGirisindenKurus(gelirBuffer);
  const gunSecili = maasGunu !== null || maasDuzensiz;

  function gunSec(n: number) {
    setMaasGunu(n);
    setMaasDuzensiz(false);
  }

  function duzensizSec() {
    setMaasDuzensiz(true);
    setMaasGunu(null);
  }

  async function kapatVeGit(hedef: '/' | '/limitler') {
    router.replace('/');
    if (hedef === '/limitler') router.push('/limitler');
  }

  /**
   * Başlıktaki "Şimdi değil" — Katman 1'in TAMAMINDAN çıkar (bir adımı
   * atlamaz): 3 sorudan biri disabled-Devam ile zorunlu kılınmışken aynı
   * ekranda hep açık bir "Devam" alternatifi olması, bunun soru bazlı bir
   * atlama değil genel bir çıkış kapısı olduğunu gösteriyor (prototipte
   * yazılı değil, PM'e bildirildi). O ana kadar cevaplanan alanlar
   * KORUNUR — yalnız gelir önerisi (K-059/5) bu yoldan hiç sunulmaz.
   */
  async function simdiDegil() {
    if (kaydediliyor) return;
    setKaydediliyor(true);
    try {
      const gelirKurus = gelirKurusGuncel;
      await onboardingKaydet(db, {
        niyet,
        gelirKurus: gelirKurus > 0 ? gelirKurus : null,
        maasGunu: maasDuzensiz ? null : maasGunu,
        maasDuzensiz,
        gunlukLimitOnerisiKurus: null,
      });
      await kapatVeGit('/');
    } catch {
      // Ağ/sunucu hatası — sessizce başarılı gösterilmez (K-029), ekranda kalınır.
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    } finally {
      setKaydediliyor(false);
    }
  }

  async function basla() {
    if (kaydediliyor || !gunSecili) return;
    setKaydediliyor(true);
    try {
      const gelirKurus = tutarGirisindenKurus(gelirBuffer);
      const gelirVar = gelirKurus > 0;
      const gun = maasDuzensiz ? null : maasGunu;
      const gunSayisi = kalanGun(new Date(), gun);
      const sosyalKurus = gelirVar ? oneriSosyalKurus(gelirKurus) : 0;
      const oneriKurus = gelirVar ? oneriLimitKurus(gelirKurus, gunSayisi) : null;

      await onboardingKaydet(db, {
        niyet,
        gelirKurus: gelirVar ? gelirKurus : null,
        maasGunu: gun,
        maasDuzensiz,
        gunlukLimitOnerisiKurus: oneriKurus,
      });

      if (gelirVar && oneriKurus !== null) {
        setOneriDetay({ gelirKurus, sosyalKurus, gunSayisi, oneriKurus });
        setOneriGoster(true);
      } else {
        await kapatVeGit('/');
      }
    } catch {
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    } finally {
      setKaydediliyor(false);
    }
  }

  async function oneriKabul() {
    if (!oneriDetay) return;
    try {
      await oneriKabulEt(db, oneriDetay.oneriKurus);
      setOneriGoster(false);
      await kapatVeGit('/');
    } catch {
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    }
  }

  async function oneriBaskaSayi() {
    try {
      await oneriReddet(db);
      setOneriGoster(false);
      await kapatVeGit('/limitler');
    } catch {
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    }
  }

  async function oneriLimitsiz() {
    try {
      await oneriReddet(db);
      setOneriGoster(false);
      await kapatVeGit('/');
    } catch {
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    }
  }

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <View style={stil.basSatiri}>
        {adim > 1 ? (
          <IconButton
            icon="chevron-left"
            accessibilityLabel={t['eylem.geri']}
            onPress={() => setAdim((a) => (a - 1) as Adim)}
          />
        ) : (
          <View style={stil.basDenge} />
        )}
        <Txt role="micro" tone={color.text2}>
          {ADIM_ETIKET[adim]}
        </Txt>
        <Button label={t['eylem.simdi_degil']} variant="ghost" auto onPress={() => void simdiDegil()} />
      </View>
      <View style={stil.pad}>
        <StepIndicator adim={adim} />
      </View>

      <ScrollView style={stil.kaydir} contentContainerStyle={stil.pad} showsVerticalScrollIndicator={false}>
        <View style={{ height: rhythm.section }} />

        {adim === 1 ? (
          <>
            <Txt role="h1">{t['ob.niyet.baslik']}</Txt>
            <View style={{ height: rhythm.group }} />
            <Txt role="body" tone={color.text2}>
              {t['ob.niyet.aciklama']}
            </Txt>
            <View style={{ height: rhythm.section }} />
            {NIYET_KART.map((k, i) => (
              <View key={k.id}>
                {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
                <OptionCard
                  icon={k.icon}
                  title={k.baslik}
                  caption={k.alt}
                  selected={niyet === k.id}
                  onPress={() => setNiyet(k.id)}
                />
              </View>
            ))}
            {niyet ? (
              <>
                <View style={{ height: rhythm.section }} />
                <View style={stil.serit}>
                  <Icon name="gauge" size={20} color={color.primaryText} />
                  <View style={{ width: rhythm.blockInCard }} />
                  <View style={stil.esnek}>
                    <Txt role="label" tone={color.text2}>
                      {t['ob.onizleme.etiket']}
                    </Txt>
                    <View style={{ height: rhythm.sameObject }} />
                    <Txt role="bodyStrong">{NIYET_ONIZLEME[niyet]}</Txt>
                  </View>
                </View>
              </>
            ) : null}
          </>
        ) : null}

        {adim === 2 ? (
          <>
            <Txt role="h1">{t['ob.gelir.baslik']}</Txt>
            <View style={{ height: rhythm.group }} />
            <Txt role="body" tone={color.text2}>
              {t['ob.gelir.aciklama']}
            </Txt>
            <View style={{ height: rhythm.section }} />
            <Txt role="label" tone={color.text2}>
              {t['ob.gelir.etiket']}
            </Txt>
            <View style={{ height: rhythm.group }} />
            <ClaySurface level="sunken" borderRadius={radius.tile} style={stil.gelirKuyu}>
              <View style={stil.gelirSatir}>
                <Txt role="hero" tone={gelirBuffer ? undefined : color.text3}>
                  {tutarGosterimi(gelirBuffer)}
                </Txt>
                {gelirBuffer ? <View style={stil.imlec} /> : null}
                <View style={{ width: rhythm.group }} />
                <Txt role="display" tone={color.text2}>
                  ₺
                </Txt>
              </View>
            </ClaySurface>
            <View style={{ height: rhythm.group }} />
            <Txt role="caption">{gelirBuffer ? t['ob.gelir.net'] : t['ob.gelir.bos']}</Txt>
            <View style={{ height: rhythm.blockInCard }} />
            <View style={stil.serit}>
              <Icon name="info" size={20} color={color.primaryText} />
              <View style={{ width: rhythm.blockInCard }} />
              <View style={stil.esnek}>
                <Txt role="caption" tone={color.text}>
                  {t['ob.gelir.mahremiyet']}
                </Txt>
                <View style={{ height: rhythm.sameObject }} />
                <Txt role="caption">{t['ob.gelir.atlarsan']}</Txt>
              </View>
            </View>
          </>
        ) : null}

        {adim === 3 ? (
          <>
            <Txt role="h1">{t['ob.maas.baslik']}</Txt>
            <View style={{ height: rhythm.group }} />
            <Txt role="body" tone={color.text2}>
              {t['ob.maas.aciklama']}
            </Txt>
            <View style={{ height: rhythm.section }} />
            <View style={stil.gunIzgara}>
              {Array.from({ length: 31 }, (_, i) => i + 1).map((n) => (
                <View key={n} style={stil.gunHucre}>
                  <DayBox gun={n} selected={maasGunu === n} onPress={() => gunSec(n)} accessibilityLabel={a11yObGun(n)} />
                </View>
              ))}
            </View>
            <View style={{ height: rhythm.blockInCard }} />
            <Chip ad={t['ob.maas.duzensiz']} selected={maasDuzensiz} onPress={duzensizSec} />
            {gunSecili ? (
              <>
                <View style={{ height: rhythm.group }} />
                <Txt role="caption">
                  {maasDuzensiz ? t['ob.maas.duzensiz.not'] : obMaasDonem(gunBulunmaEki(maasGunu ?? 1))}
                </Txt>
              </>
            ) : null}
            <View style={{ height: rhythm.section }} />
            <ClaySurface level="raised" borderRadius={radius.card} style={stil.ozetKart}>
              <Txt role="label" tone={color.text2}>
                {t['ob.ozet.baslik']}
              </Txt>
              <View style={{ height: rhythm.group }} />
              <OzetSatir sol={t['ob.ozet.niyet_label']} sag={niyet ? NIYET_OZET[niyet] : t['ob.ozet.limit_yok']} />
              <View style={{ height: rhythm.group }} />
              <OzetSatir
                sol={t['ob.gelir.etiket']}
                sag={gelirKurusGuncel > 0 ? paraYaz(gelirKurusGuncel) : t['ob.ozet.limit_yok']}
                amount={gelirKurusGuncel > 0}
              />
              <View style={{ height: rhythm.group }} />
              <OzetSatir
                sol={t['ob.ozet.maas_label']}
                sag={
                  maasDuzensiz
                    ? t['ob.ozet.maas_duzensiz']
                    : maasGunu !== null
                      ? obOzetMaasGunu(gunIyelikEki(maasGunu))
                      : t['ob.ozet.limit_yok']
                }
              />
              <View style={{ height: rhythm.group }} />
              <OzetSatir sol={t['ob.ozet.limit_label']} sag={t['ob.ozet.limit_yok']} />
            </ClaySurface>
            <View style={{ height: rhythm.group }} />
            <Txt role="caption">{gelirKurusGuncel > 0 ? t['onboarding.ozet.limitSatiri'] : t['ob.ozet.limit_not']}</Txt>
          </>
        ) : null}

        <View style={{ height: rhythm.section }} />
      </ScrollView>

      <View style={[stil.altSabit, { paddingBottom: insets.bottom }]}>
        {adim === 2 ? (
          <>
            <View style={stil.pad}>
              <ClayKeypad
                onDigit={(d) => setGelirBuffer((b) => tutarGirisiEkle(b, d))}
                onComma={() => setGelirBuffer((b) => tutarGirisiEkle(b, ','))}
                onBackspace={() => setGelirBuffer((b) => tutarGirisiSil(b))}
              />
            </View>
            <View style={{ height: rhythm.blockInCard }} />
            <View style={stil.pad}>
              <Button
                label={t['eylem.devam']}
                variant="primary"
                disabled={gelirKurusGuncel <= 0}
                onPress={() => setAdim(3)}
              />
              <View style={{ height: rhythm.group }} />
              <Button
                label={t['ob.gelir.atla']}
                variant="ghost"
                accessibilityLabel={t['a11y.ob.gelir_atla']}
                onPress={() => {
                  setGelirBuffer('');
                  setAdim(3);
                }}
              />
            </View>
          </>
        ) : (
          <View style={stil.pad}>
            <Button
              label={adim === 1 ? t['eylem.devam'] : t['ob.bitir']}
              variant="primary"
              disabled={adim === 1 ? !niyet : !gunSecili}
              loading={kaydediliyor}
              onPress={() => (adim === 1 ? setAdim(2) : void basla())}
            />
          </View>
        )}
      </View>

      <BottomSheet visible={oneriGoster} onClose={() => void oneriLimitsiz()}>
        {oneriDetay ? (
          <OneriSheetIcerik
            detay={oneriDetay}
            onKabul={() => void oneriKabul()}
            onDegistir={() => void oneriBaskaSayi()}
            onRed={() => void oneriLimitsiz()}
          />
        ) : null}
      </BottomSheet>
    </View>
  );
}

function OzetSatir({ sol, sag, amount = false }: { sol: string; sag: string; amount?: boolean }) {
  return (
    <View style={stil.ozetSatir}>
      <Txt role="body">{sol}</Txt>
      <Txt role={amount ? 'amount' : 'bodyStrong'}>{sag}</Txt>
    </View>
  );
}

function OneriSheetIcerik({
  detay,
  onKabul,
  onDegistir,
  onRed,
}: {
  detay: OneriDetay;
  onKabul: () => void;
  onDegistir: () => void;
  onRed: () => void;
}) {
  return (
    <ScrollView showsVerticalScrollIndicator={false}>
      <View style={stil.sheetBaslikSatiri}>
        <Txt role="h2" style={stil.esnek}>
          {t['oneri.baslik']}
        </Txt>
        <View style={{ width: rhythm.blockInCard }} />
        <SuggestionTag label={t['oneri.pul']} />
      </View>
      <View style={{ height: rhythm.group }} />
      <Txt role="caption">{t['oneri.alt']}</Txt>
      <View style={{ height: rhythm.pad }} />
      <EquationRow
        items={[
          { value: paraYaz(detay.sosyalKurus), label: t['oneri.denklem.sosyal'] },
          { value: oneriDenklemKalanGun(detay.gunSayisi), label: t['oneri.denklem.kalan_gun'] },
          { value: paraYaz(detay.oneriKurus), label: t['oneri.denklem.gunluk'] },
        ]}
      />
      <View style={{ height: rhythm.pad }} />
      <Txt role="label" tone={color.text2}>
        {t['oneri.nasil.baslik']}
      </Txt>
      <View style={{ height: rhythm.blockInCard }} />
      <NumaraliSatir n={1} metin={oneriNasil1(paraYaz(detay.gelirKurus))} />
      <View style={{ height: rhythm.group }} />
      <NumaraliSatir n={2} metin={t['oneri.nasil.2']} />
      <View style={{ height: rhythm.group }} />
      <NumaraliSatir n={3} metin={oneriNasil3(paraYaz(detay.sosyalKurus), detay.gunSayisi)} />
      <View style={{ height: rhythm.pad }} />
      <InfoStrip variant="info" metin={`${t['oneri.serit.1']}\n${t['oneri.serit.2']}`} />
      <View style={{ height: rhythm.pad }} />
      <Button label={t['oneri.btn.kabul']} variant="primary" icon="check" onPress={onKabul} />
      <View style={{ height: rhythm.group }} />
      <Button label={t['oneri.btn.degistir']} variant="secondary" icon="pencil" onPress={onDegistir} />
      <View style={{ height: rhythm.group }} />
      <Button label={t['oneri.btn.red']} variant="ghost" onPress={onRed} />
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
  serit: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    paddingVertical: rhythm.blockInCard,
    paddingHorizontal: rhythm.pad,
    borderRadius: radius.tile,
    backgroundColor: color.primarySoft,
    boxShadow: clay.sunken,
  },
  gelirKuyu: { padding: rhythm.pad, alignItems: 'center' },
  gelirSatir: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center' },
  imlec: { width: 3, height: 44, borderRadius: radius.pill, backgroundColor: color.primary, marginLeft: rhythm.sameObject },
  gunIzgara: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -v4.gridGap / 2 },
  gunHucre: { width: '14.2857%', alignItems: 'center', marginBottom: v4.gridGap },
  ozetKart: { padding: rhythm.pad },
  ozetSatir: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  altSabit: { paddingTop: rhythm.group, backgroundColor: color.bg },
  sheetBaslikSatiri: { flexDirection: 'row', alignItems: 'center' },
  numaraSatir: { flexDirection: 'row', alignItems: 'flex-start' },
  numaraKutu: { width: 12, alignItems: 'flex-start' },
});
