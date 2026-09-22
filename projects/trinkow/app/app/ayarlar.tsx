import { router, useFocusEffect } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { AccountSection } from '@/components/AccountSection';
import { BottomSheet } from '@/components/BottomSheet';
import { Button } from '@/components/Button';
import { Chip } from '@/components/Chip';
import { ClayKeypad } from '@/components/ClayKeypad';
import { ClaySurface } from '@/components/ClaySurface';
import { DayBox } from '@/components/DayBox';
import { Dialog } from '@/components/Dialog';
import { ErrorState } from '@/components/ErrorState';
import { InfoStrip } from '@/components/InfoStrip';
import { OptionCard } from '@/components/OptionCard';
import { PushHeader } from '@/components/PushHeader';
import { SegmentedControl } from '@/components/SegmentedControl';
import { SettingRow } from '@/components/SettingRow';
import { Skeleton } from '@/components/Skeleton';
import { Txt } from '@/components/Txt';
import { ValueWell } from '@/components/ValueWell';
import {
  a11yDegerDegistir,
  a11yObGun,
  ayarPlanBekliyor,
  ayarPlanKalan,
  ayarSurum,
  ayarVeriSilOzet,
  hesapsilVeri,
  obOzetMaasGunu,
  t,
} from '@/content/metinler';
import { bildirimIzniVarMi } from '@/lib/bildirimIzni';
import {
  bildirimAksamOzetKaydet,
  bildirimAksamOzetOku,
  bildirimSaatiKaydet,
  bildirimSaatiOku,
  gunSiniriKaydet,
  gunSiniriOku,
  varsayilanOdemeKaydet,
  varsayilanOdemeOku,
  type GunSiniriSaat,
} from '@/db/ayarTercihleri';
import { ilkKayitGunu, tumKayitSayisi, tumVeriyiSil, type OdemeTipi } from '@/db/harcama';
import {
  gelirKaydet,
  katman2DolanKartSayisi,
  maasGunuKaydet,
  niyetKaydet,
  profilDetayOku,
  profilOku,
  type Niyet,
} from '@/db/profil';
import { hesabiSil, oturumuKapat } from '@/lib/hesapEylemleri';
import { type Oturum, oturumOku } from '@/lib/oturumDeposu';
import { toastGoster } from '@/lib/toastBus';
import { girisEkraninaDon } from '@/lib/yonlendirme';
import { paraYaz, tutarGirisiEkle, tutarGirisiSil, tutarGirisindenKurus, tutarGosterimi, kurustanTutarGirisi } from '@/lib/para';
import { ayAnahtari, ayBasligi, gunIyelikEki, tarihtenGun } from '@/lib/tarih';
import { veriDegisti } from '@/lib/veriBus';
import { color, layout, radius, rhythm, v4 } from '@/theme/tokens';

/**
 * D-2c-1 · E-19 Ayarlar. Referans: prototip-v4/11-ayarlar.html (4 yüzey).
 * Arka oda — **Kaydet yok**: her anahtar dokunulduğu an yazılır, ekranda
 * birincil buton ve alt sabit blok bulunmaz (bkz. prototip not-kutusu).
 *
 * Hesap bölümü D-2c-2'de gerçek oturuma bağlandı (bkz. `src/lib/api.ts` ·
 * `src/lib/oturumDeposu.ts`). `oturum` yerel depodan okunur — Ayarlar her
 * odaklandığında (`useFocusEffect`) tazelenir, bu yüzden giriş/kayıt/çıkış
 * sonrası buraya dönüldüğünde satır güncel görünür.
 */
const SAGLAYICI_ETIKETI: Record<string, string> = {
  google: t['ayar.hesap.saglayici.google'],
  apple: t['ayar.hesap.saglayici.apple'],
  eposta: t['ayar.hesap.saglayici.sifre'],
};

const KIP_META: { id: Niyet; icon: 'target' | 'landmark' | 'trending-up'; baslik: string; alt: string }[] = [
  { id: 'takip', icon: 'target', baslik: t['ob.niyet.takip'], alt: t['ob.niyet.takip.alt'] },
  { id: 'tasarruf', icon: 'landmark', baslik: t['ob.niyet.tasarruf'], alt: t['ob.niyet.tasarruf.alt'] },
  { id: 'borc', icon: 'trending-up', baslik: t['ob.niyet.borc'], alt: t['ob.niyet.borc.alt'] },
];

const KIP_ETIKET: Record<Niyet, string> = {
  takip: t['pano.kip.takip'],
  tasarruf: t['pano.kip.tasarruf'],
  borc: t['pano.kip.borc'],
};

const BILDIRIM_SAAT_SECENEKLERI = ['19.00', '19.30', '20.00', '20.30', '21.00', '21.30', '22.00', '22.30', '23.00'];

const GUN_SINIRI_SECENEKLERI: { value: `${GunSiniriSaat}`; label: string }[] = [
  { value: '0', label: t['ayar.gun_siniri.0'] },
  { value: '3', label: t['ayar.gun_siniri.3'] },
  { value: '6', label: t['ayar.gun_siniri.6'] },
];

const ODEME_SECENEKLERI: { value: OdemeTipi; label: string; icon: 'banknote' | 'credit-card' }[] = [
  { value: 'nakit', label: t['ekle.odeme.nakit'], icon: 'banknote' },
  { value: 'kart', label: t['ekle.odeme.kart'], icon: 'credit-card' },
];

const MAAS_GUNLERI = Array.from({ length: 31 }, (_, i) => i + 1);

export default function AyarlarEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();

  const [yukleniyor, setYukleniyor] = useState(true);
  const [hata, setHata] = useState(false);
  const [izinVarMi, setIzinVarMi] = useState(true);
  const [bildirimAcik, setBildirimAcik] = useState(true);
  const [bildirimSaati, setBildirimSaati] = useState('21.00');
  const [gunSiniri, setGunSiniri] = useState<GunSiniriSaat>(0);
  const [odeme, setOdeme] = useState<OdemeTipi>('kart');
  const [niyet, setNiyet] = useState<Niyet>('takip');
  const [gelirKurus, setGelirKurus] = useState<number | null>(null);
  const [maasGunu, setMaasGunu] = useState<number | null>(null);
  const [maasDuzensiz, setMaasDuzensiz] = useState(false);
  const [katman2Kalan, setKatman2Kalan] = useState(8);
  const [kayitAdedi, setKayitAdedi] = useState(0);
  const [ilkKayitAyYil, setIlkKayitAyYil] = useState<string | null>(null);

  const [saatSheetAcik, setSaatSheetAcik] = useState(false);
  const [kipSheetAcik, setKipSheetAcik] = useState(false);
  const [gelirDuzenleAcik, setGelirDuzenleAcik] = useState(false);
  const [gelirBuffer, setGelirBuffer] = useState('');
  const [maasDuzenleAcik, setMaasDuzenleAcik] = useState(false);
  const [veriSilAcik, setVeriSilAcik] = useState(false);
  const [veriSiliniyor, setVeriSiliniyor] = useState(false);
  const [hesapSilAcik, setHesapSilAcik] = useState(false);
  const [hesapSiliniyor, setHesapSiliniyor] = useState(false);
  const [oturum, setOturum] = useState<Oturum | null>(null);

  const oku = useCallback(async () => {
    setYukleniyor(true);
    setHata(false);
    try {
      const [izin, acik, saat, sinir, odemeD, profil, detay, adet, ilkGun, oturumKaydi] = await Promise.all([
        bildirimIzniVarMi(),
        bildirimAksamOzetOku(db),
        bildirimSaatiOku(db),
        gunSiniriOku(db),
        varsayilanOdemeOku(db),
        profilOku(db),
        profilDetayOku(db),
        tumKayitSayisi(db),
        ilkKayitGunu(db),
        oturumOku(),
      ]);
      setOturum(oturumKaydi);
      setIzinVarMi(izin);
      setBildirimAcik(acik);
      setBildirimSaati(saat);
      setGunSiniri(sinir);
      setOdeme(odemeD);
      setNiyet(profil.niyet ?? 'takip');
      setGelirKurus(profil.gelirKurus);
      setMaasGunu(profil.maasGunu);
      setMaasDuzensiz(profil.maasDuzensiz);
      setKatman2Kalan(8 - katman2DolanKartSayisi(detay));
      setKayitAdedi(adet);
      setIlkKayitAyYil(ilkGun ? ayBasligi(ayAnahtari(tarihtenGun(ilkGun))) : null);
    } catch {
      setHata(true);
    } finally {
      setYukleniyor(false);
    }
  }, [db]);

  useFocusEffect(
    useCallback(() => {
      void oku();
    }, [oku]),
  );

  async function bildirimAcikDegistir() {
    const yeni = !bildirimAcik;
    setBildirimAcik(yeni);
    await bildirimAksamOzetKaydet(db, yeni);
  }

  async function bildirimSaatiSec(saat: string) {
    setBildirimSaati(saat);
    setSaatSheetAcik(false);
    await bildirimSaatiKaydet(db, saat);
  }

  async function gunSiniriSec(deger: `${GunSiniriSaat}`) {
    const saat = Number(deger) as GunSiniriSaat;
    setGunSiniri(saat);
    await gunSiniriKaydet(db, saat);
  }

  async function odemeSec(deger: OdemeTipi) {
    setOdeme(deger);
    await varsayilanOdemeKaydet(db, deger);
  }

  async function kipSec(id: Niyet) {
    setNiyet(id);
    setKipSheetAcik(false);
    await niyetKaydet(db, id);
    veriDegisti();
  }

  function gelirDuzenleAc() {
    setGelirBuffer(gelirKurus ? kurustanTutarGirisi(gelirKurus) : '');
    setGelirDuzenleAcik(true);
  }

  async function gelirDuzenleKapat() {
    const kurus = tutarGirisindenKurus(gelirBuffer);
    const yeni = kurus > 0 ? kurus : null;
    setGelirKurus(yeni);
    setGelirDuzenleAcik(false);
    await gelirKaydet(db, yeni);
    veriDegisti();
  }

  async function maasGunuSec(gun: number) {
    setMaasGunu(gun);
    setMaasDuzensiz(false);
    setMaasDuzenleAcik(false);
    await maasGunuKaydet(db, gun, false);
    veriDegisti();
  }

  async function maasDuzensizSec() {
    setMaasGunu(null);
    setMaasDuzensiz(true);
    setMaasDuzenleAcik(false);
    await maasGunuKaydet(db, null, true);
    veriDegisti();
  }

  async function veriyiSil() {
    setVeriSiliniyor(true);
    try {
      await tumVeriyiSil(db);
      setVeriSilAcik(false);
      veriDegisti();
      await oku();
    } finally {
      setVeriSiliniyor(false);
    }
  }

  async function oturumuKapatVeGirisEkraninaDon() {
    await oturumuKapat();
    // K-080 — hesapsız kullanım yok; çıkış sonrası giriş ekranına düşer.
    // K-082/2 — üstteki yığın da kapatılır (geri tuşuyla eskiye dönülemez).
    girisEkraninaDon();
  }

  async function hesabiSilOnayla() {
    setHesapSiliniyor(true);
    try {
      await hesabiSil();
      setHesapSilAcik(false);
      // K-080 — hesap silinince uygulama kullanılamaz, giriş ekranına düşer.
      girisEkraninaDon();
    } catch {
      // Ağ/sunucu hatası — hesap yerelde "silinmiş" gösterilmez, diyalog
      // açık kalır (K-029: geri alınamaz işlemde sessiz başarısızlık yok).
      toastGoster({ tur: 'warning', metin: t['hata.okuma.govde'] });
    } finally {
      setHesapSiliniyor(false);
    }
  }

  const maasGunuDegeri = maasDuzensiz ? t['ob.maas.duzensiz'] : maasGunu !== null ? obOzetMaasGunu(gunIyelikEki(maasGunu)) : t['tan.girilmedi'];
  const katman2Deger = katman2Kalan === 8 ? ayarPlanBekliyor(8) : ayarPlanKalan(katman2Kalan);

  if (hata) {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <PushHeader baslik={t['ayar.baslik']} onGeri={() => router.back()} />
        <View style={stil.pad}>
          <ErrorState onRetry={() => void oku()} />
        </View>
      </View>
    );
  }

  if (yukleniyor) {
    return (
      <View style={stil.ekran}>
        <View style={{ height: insets.top }} />
        <PushHeader baslik={t['ayar.baslik']} onGeri={() => router.back()} />
        <View style={stil.pad}>
          <Skeleton width="100%" height={140} borderRadius={radius.card} />
          <View style={{ height: rhythm.section }} />
          <Skeleton width="100%" height={100} borderRadius={radius.card} />
          <View style={{ height: rhythm.section }} />
          <Skeleton width="100%" height={220} borderRadius={radius.card} />
        </View>
      </View>
    );
  }

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <PushHeader baslik={t['ayar.baslik']} onGeri={() => router.back()} />

      <ScrollView style={stil.kaydir} contentContainerStyle={[stil.pad, { paddingBottom: layout.scrollPadBottom + insets.bottom }]} showsVerticalScrollIndicator={false}>
        {/* Bildirim */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.bildirim']}</Txt>
          <View style={{ height: rhythm.group }} />
          <SettingRow
            baslik={t['ayar.bildirim']}
            aciklama={izinVarMi ? t['ayar.bildirim_aciklama'] : t['ayar.bildirim_izni_kapali_not']}
            anahtarDegeri={bildirimAcik}
            anahtarKapali={!izinVarMi}
            onAnahtarDegistir={() => void bildirimAcikDegistir()}
            accessibilityLabel={`${t['ayar.bildirim']}, ${bildirimAcik ? 'açık' : 'kapalı'}`}
          />
          {izinVarMi ? (
            <>
              <View style={{ height: rhythm.blockInCard }} />
              <ValueWell
                etiket={t['ayar.bildirim_saat']}
                deger={bildirimSaati}
                onPress={() => setSaatSheetAcik(true)}
                accessibilityLabel={a11yDegerDegistir(t['ayar.bildirim_saat'], bildirimSaati)}
              />
            </>
          ) : (
            <>
              <View style={{ height: rhythm.blockInCard }} />
              <InfoStrip variant="info" icon="bell" metin={t['ayar.bildirim_kapali_not']} />
            </>
          )}
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Gün sınırı */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.gun_siniri']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{t['ayar.gun_siniri_aciklama']}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <SegmentedControl secenekler={GUN_SINIRI_SECENEKLERI} deger={`${gunSiniri}` as `${GunSiniriSaat}`} onChange={(v) => void gunSiniriSec(v)} />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Varsayılan ödeme */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.varsayilan_odeme']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{t['ayar.odeme_aciklama']}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <SegmentedControl secenekler={ODEME_SECENEKLERI} deger={odeme} onChange={(v) => void odemeSec(v)} />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Kip */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.kip']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{t['ayar.kip_aciklama']}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <ValueWell
            etiket={t['ayar.kip']}
            deger={KIP_ETIKET[niyet]}
            onPress={() => setKipSheetAcik(true)}
            accessibilityLabel={a11yDegerDegistir(t['ayar.kip'], KIP_ETIKET[niyet])}
          />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Plan ve profil */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.plan.baslik']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="caption">{gelirKurus === null ? t['ayar.plan.gelirsiz'] : t['ayar.plan.aciklama']}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <ValueWell
            etiket={t['ayar.plan.gelir']}
            deger={gelirDuzenleAcik ? `${tutarGosterimi(gelirBuffer)} ₺` : gelirKurus ? paraYaz(gelirKurus) : t['ayar.plan.gelir_girilmedi']}
            degerSoluk={!gelirDuzenleAcik && !gelirKurus}
            focused={gelirDuzenleAcik}
            onPress={() => (gelirDuzenleAcik ? void gelirDuzenleKapat() : gelirDuzenleAc())}
            accessibilityLabel={
              gelirKurus ? a11yDegerDegistir(t['ayar.plan.gelir'], paraYaz(gelirKurus)) : t['ayar.plan.gelir']
            }
          />
          {gelirDuzenleAcik ? (
            <>
              <View style={{ height: rhythm.group }} />
              <ClayKeypad
                onDigit={(d) => setGelirBuffer((b) => tutarGirisiEkle(b, d))}
                onComma={() => setGelirBuffer((b) => tutarGirisiEkle(b, ','))}
                onBackspace={() => setGelirBuffer((b) => tutarGirisiSil(b))}
              />
            </>
          ) : null}
          <View style={{ height: rhythm.blockInCard }} />
          <ValueWell
            etiket={t['ayar.plan.maas_gunu']}
            deger={maasGunuDegeri}
            degerSoluk={maasGunu === null && !maasDuzensiz}
            onPress={() => setMaasDuzenleAcik((a) => !a)}
            accessibilityLabel={a11yDegerDegistir(t['ayar.plan.maas_gunu'], maasGunuDegeri)}
          />
          {maasDuzenleAcik ? (
            <>
              <View style={{ height: rhythm.group }} />
              <View style={stil.gunIzgara}>
                {MAAS_GUNLERI.map((n) => (
                  <View key={n} style={stil.gunHucre}>
                    <DayBox gun={n} selected={maasGunu === n} onPress={() => void maasGunuSec(n)} accessibilityLabel={a11yObGun(n)} />
                  </View>
                ))}
              </View>
              <View style={{ height: rhythm.blockInCard }} />
              <Chip ad={t['ob.maas.duzensiz']} selected={maasDuzensiz} onPress={() => void maasDuzensizSec()} />
            </>
          ) : null}
          <View style={{ height: rhythm.blockInCard }} />
          <ValueWell
            etiket={t['ayar.plan.tanit']}
            deger={katman2Deger}
            degerSoluk
            onPress={() => router.push('/tanisma')}
            accessibilityLabel={t['ayar.plan.tanit']}
          />
          <View style={{ height: rhythm.blockInCard }} />
          <ValueWell etiket={t['ayar.plan.gor']} deger="" onPress={() => router.push('/plan')} accessibilityLabel={t['ayar.plan.gor']} />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Hesap — D-2c-2: gerçek oturuma bağlandı; D-2c-3/K-080: hesap
            zorunlu, çıkış/silme sonrası `_layout.tsx`'in giriş duvarı
            devreye girer (bkz. src/lib/hesapEylemleri.ts). */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.hesap.baslik']}</Txt>
          <View style={{ height: rhythm.group }} />
          {oturum ? (
            <AccountSection
              variant="signed-in"
              eposta={oturum.email}
              saglayiciEtiketi={SAGLAYICI_ETIKETI[oturum.kimlikSaglayici] ?? t['ayar.hesap.saglayici.sifre']}
              onCikisYap={() => void oturumuKapatVeGirisEkraninaDon()}
              onHesabiSil={() => setHesapSilAcik(true)}
            />
          ) : (
            <AccountSection variant="signed-out" onOturumAcKapisi={() => router.push('/giris')} />
          )}
        </ClaySurface>

        <View style={{ height: rhythm.section }} />

        {/* Veri */}
        <ClaySurface level="raised" borderRadius={radius.card} style={stil.kart}>
          <Txt role="h2">{t['ayar.veri']}</Txt>
          <View style={{ height: rhythm.group }} />
          <Txt role="body">{t['ayar.veri_aciklama']}</Txt>
          <View style={{ height: rhythm.blockInCard }} />
          <Button
            label={t['ayar.veri_sil']}
            variant="ghost"
            icon="trash"
            auto
            disabled={kayitAdedi === 0}
            onPress={() => setVeriSilAcik(true)}
          />
        </ClaySurface>

        <View style={{ height: rhythm.section }} />
        <Txt role="micro" tone={color.text2}>
          {ayarSurum('1.0.0')}
        </Txt>
      </ScrollView>

      {/* Bildirim saati sheet */}
      <BottomSheet visible={saatSheetAcik} onClose={() => setSaatSheetAcik(false)}>
        <Txt role="h2">{t['ayar.bildirim_saat']}</Txt>
        <View style={{ height: rhythm.blockInCard }} />
        <View style={stil.cipAgi}>
          {BILDIRIM_SAAT_SECENEKLERI.map((s) => (
            <View key={s} style={stil.cipOge}>
              <Chip ad={s} selected={s === bildirimSaati} onPress={() => void bildirimSaatiSec(s)} />
            </View>
          ))}
        </View>
        <View style={{ height: rhythm.pad }} />
      </BottomSheet>

      {/* Kip sheet */}
      <BottomSheet visible={kipSheetAcik} onClose={() => setKipSheetAcik(false)}>
        <Txt role="h2">{t['ayar.kip_degistir']}</Txt>
        <View style={{ height: rhythm.blockInCard }} />
        {KIP_META.map((k, i) => (
          <View key={k.id}>
            {i > 0 ? <View style={{ height: rhythm.group }} /> : null}
            <OptionCard icon={k.icon} title={k.baslik} caption={k.alt} selected={niyet === k.id} onPress={() => void kipSec(k.id)} />
          </View>
        ))}
        <View style={{ height: rhythm.pad }} />
      </BottomSheet>

      <Dialog
        visible={veriSilAcik}
        baslik={t['ayar.veri_sil_baslik']}
        govde={t['ayar.veri_sil_govde']}
        ozet={
          <InfoStrip
            variant="danger"
            icon="notebook"
            metin={ilkKayitAyYil ? ayarVeriSilOzet(kayitAdedi, ilkKayitAyYil) : `${kayitAdedi}`}
          />
        }
        silEtiketi={t['ayar.veri_sil']}
        vazgecEtiketi={t['eylem.vazgec']}
        siliniyor={veriSiliniyor}
        onSil={() => void veriyiSil()}
        onVazgec={() => setVeriSilAcik(false)}
      />

      <Dialog
        visible={hesapSilAcik}
        baslik={t['hesapsil.baslik']}
        govde={t['hesapsil.govde']}
        ozet={<InfoStrip variant="danger" icon="notebook" metin={hesapsilVeri(kayitAdedi)} />}
        silEtiketi={t['hesapsil.eylem']}
        vazgecEtiketi={t['eylem.vazgec']}
        siliniyor={hesapSiliniyor}
        onSil={() => void hesabiSilOnayla()}
        onVazgec={() => setHesapSilAcik(false)}
      />
    </View>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  pad: { paddingHorizontal: layout.screenPaddingX },
  kart: { padding: rhythm.pad },
  gunIzgara: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -v4.gridGap / 2 },
  gunHucre: { width: '14.2857%', alignItems: 'center', marginBottom: v4.gridGap },
  cipAgi: { flexDirection: 'row', flexWrap: 'wrap', marginRight: -rhythm.group, marginBottom: -rhythm.group },
  cipOge: { marginRight: rhythm.group, marginBottom: rhythm.group },
});
