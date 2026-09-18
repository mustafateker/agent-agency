import { router, useLocalSearchParams } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useEffect, useMemo, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { AmountWell } from '@/components/AmountWell';
import { Button } from '@/components/Button';
import { CategoryPicker } from '@/components/CategoryPicker';
import { Chip } from '@/components/Chip';
import { ClayKeypad } from '@/components/ClayKeypad';
import { InfoStrip } from '@/components/InfoStrip';
import { ScreenHeader } from '@/components/ScreenHeader';
import { SegmentedControl } from '@/components/SegmentedControl';
import { TextField } from '@/components/TextField';
import { Txt } from '@/components/Txt';
import { ekleLimitDisiUyari, ekleTaksitOnizleme, t, toastKaydedildi, toastKaydedildiLimitDisi } from '@/content/metinler';
import {
  ODEME_VARSAYILAN,
  gunToplami,
  gunlukLimit,
  harcamaEkle,
  sikAlinanlar,
  taksitSerisiOlustur,
  type OdemeTipi,
  type SikAlinan,
} from '@/db/harcama';
import { aileRenkleri, kategori as kategoriGetir, type KategoriKodu } from '@/lib/kategoriler';
import {
  TUTAR_BUYUK_ESIK_KURUS,
  paraYaz,
  tutarGirisiEkle,
  tutarGirisiSil,
  tutarGirisindenKurus,
  tutarGosterimi,
  kurustanTutarGirisi,
} from '@/lib/para';
import { gunAnahtari, gunEkle, kisaTarih } from '@/lib/tarih';
import { toastGoster } from '@/lib/toastBus';
import { veriDegisti } from '@/lib/veriBus';
import { color, layout, rhythm } from '@/theme/tokens';

/**
 * E-11 · Harcama ekle. Referans: prototip-v3/02-harcama-ekle.html.
 * Dokunuş bütçesi (ekran-envanteri §4): 1) Harcama ekle 2) Kategori 3) Kaydet.
 * Tarih/ödeme/taksit/not varsayılanları bu sayıyı korumak için seçildi.
 *
 * K-032: kategori önceden seçili GELMEZ (yalnız v4 K-049 "geçmiş güne geç
 * kayıt" ve K-051 kategori kartı "+" hızlı eklemesi istisna — `kategori`
 * route param'ıyla önceden dolar, kullanıcı isterse değiştirir).
 * Nakite dönülürse taksit sessizce sıfırlanır (K-023). Kaydet yalnız
 * tutar>0 iken etkin; kategori eksikse gönderim anında hata gösterilir.
 */
const TAKSIT_SECENEKLERI = [3, 6, 9, 12];

export default function HarcamaEkleEkrani() {
  const db = useSQLiteContext();
  const insets = useSafeAreaInsets();
  const params = useLocalSearchParams<{ gunFarki?: string; kategori?: string }>();

  // v4 K-049 — Günlük'ün geçmiş sayfasından açılınca tarih o güne SABİTLENİR
  // (0/-1 dışındaki bir gün farkı geldiyse Bugün/Dün seçici gizlenir).
  const gunFarkiParam = params.gunFarki !== undefined ? Number.parseInt(params.gunFarki, 10) : null;
  const sabitGunFarki =
    gunFarkiParam !== null && Number.isFinite(gunFarkiParam) && gunFarkiParam !== 0 && gunFarkiParam !== -1;

  const [buffer, setBuffer] = useState('');
  const [urunAdi, setUrunAdi] = useState('');
  const [kategoriKodu, setKategoriKodu] = useState<KategoriKodu | null>(() =>
    params.kategori ? kategoriGetir(params.kategori).kod : null,
  );
  const [odeme, setOdeme] = useState<OdemeTipi>(ODEME_VARSAYILAN);
  const [taksitliAcik, setTaksitliAcik] = useState(false);
  const [taksitSayisi, setTaksitSayisi] = useState<number | null>(null);
  const [dun, setDun] = useState(gunFarkiParam === -1);
  const [notAcik, setNotAcik] = useState(false);
  const [notMetni, setNotMetni] = useState('');

  const [kategoriHata, setKategoriHata] = useState<string | undefined>();
  const [tutarHata, setTutarHata] = useState<string | undefined>();
  const [yazmaHata, setYazmaHata] = useState<string | undefined>();
  const [kaydediliyor, setKaydediliyor] = useState(false);

  const [sikAlinanlarListesi, setSikAlinanlarListesi] = useState<SikAlinan[]>([]);
  const [gununToplamiKurus, setGununToplamiKurus] = useState(0);
  const [limitKurus, setLimitKurus] = useState<number | null>(null);

  useEffect(() => {
    let canli = true;
    void sikAlinanlar(db, 3).then((l) => canli && setSikAlinanlarListesi(l));
    void gunlukLimit(db).then((l) => canli && setLimitKurus(l));
    return () => {
      canli = false;
    };
  }, [db]);

  const seciliTarih = useMemo(
    () => gunEkle(new Date(), sabitGunFarki ? gunFarkiParam! : dun ? -1 : 0),
    [dun, sabitGunFarki, gunFarkiParam],
  );
  const seciliGun = useMemo(() => gunAnahtari(seciliTarih), [seciliTarih]);

  useEffect(() => {
    let canli = true;
    void gunToplami(db, seciliGun).then((v) => canli && setGununToplamiKurus(v));
    return () => {
      canli = false;
    };
  }, [db, seciliGun]);

  const tutarKurus = tutarGirisindenKurus(buffer);
  const tutarGosterim = tutarGosterimi(buffer);
  const limitDisiFarkKurus =
    limitKurus !== null && tutarKurus > 0 && gununToplamiKurus + tutarKurus > limitKurus
      ? gununToplamiKurus + tutarKurus - limitKurus
      : 0;

  function tutarDegistir(guncelle: (b: string) => string) {
    if (tutarHata) setTutarHata(undefined);
    setBuffer(guncelle);
  }

  function odemeSec(v: OdemeTipi) {
    setOdeme(v);
    if (v === 'nakit') {
      // K-023 — nakite dönülürse taksit sessizce sıfırlanır.
      setTaksitliAcik(false);
      setTaksitSayisi(null);
    }
  }

  function sikAlinanSec(s: SikAlinan) {
    setBuffer(kurustanTutarGirisi(s.tutarKurus));
    setKategoriKodu(kategoriGetir(s.kategori).kod);
    setUrunAdi(s.urunAdi);
    setKategoriHata(undefined);
  }

  async function kaydet() {
    if (!kategoriKodu) {
      setKategoriHata(t['hata.kategori_yok']);
      return;
    }
    if (tutarKurus > TUTAR_BUYUK_ESIK_KURUS) {
      setTutarHata(t['hata.tutar_buyuk']);
      return;
    }
    setKaydediliyor(true);
    setYazmaHata(undefined);
    try {
      if (taksitliAcik && taksitSayisi) {
        await taksitSerisiOlustur(db, {
          tutarKurusToplam: tutarKurus,
          taksitSayisi,
          kategori: kategoriKodu,
          urunAdi: urunAdi.trim() || null,
          odeme: 'kart',
          notMetni: notMetni.trim() || null,
          ilkZaman: seciliTarih,
        });
      } else {
        await harcamaEkle(db, {
          tutarKurus,
          kategori: kategoriKodu,
          urunAdi: urunAdi.trim() || null,
          zaman: seciliTarih.toISOString(),
          gun: seciliGun,
          odeme,
          notMetni: notMetni.trim() || null,
          taksitId: null,
          taksitNo: null,
          taksitToplam: null,
        });
      }
      veriDegisti();
      toastGoster({
        tur: limitDisiFarkKurus > 0 ? 'warning' : 'info',
        metin:
          limitDisiFarkKurus > 0
            ? toastKaydedildiLimitDisi(paraYaz(tutarKurus), paraYaz(limitDisiFarkKurus))
            : toastKaydedildi(paraYaz(tutarKurus)),
      });
      router.back();
    } catch {
      setYazmaHata(t['hata.yazma']);
    } finally {
      setKaydediliyor(false);
    }
  }

  return (
    <View style={stil.ekran}>
      <View style={{ height: insets.top }} />
      <ScrollView
        style={stil.kaydir}
        contentContainerStyle={stil.kaydirIcerik}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled">
        <ScreenHeader
          baslik={t['ekle.baslik']}
          actionIcon="x"
          actionLabel={t['eylem.kapat']}
          onActionPress={() => router.back()}
        />

        <View style={stil.pad}>
          <AmountWell
            tutarGosterim={tutarGosterim}
            ustSol={t['ekle.tutar.etiket']}
            ustSag={sabitGunFarki ? kisaTarih(seciliTarih) : dun ? t['ekle.tarih.dun'] : t['ekle.tarih.bugun']}
            hata={tutarHata}
          />
        </View>

        {limitDisiFarkKurus > 0 ? (
          <>
            <View style={{ height: rhythm.group }} />
            <View style={stil.pad}>
              <InfoStrip
                variant="warning"
                metin={ekleLimitDisiUyari(paraYaz(limitDisiFarkKurus))}
              />
            </View>
          </>
        ) : null}

        <View style={{ height: rhythm.group }} />
        <View style={stil.pad}>
          <TextField
            value={urunAdi}
            onChangeText={setUrunAdi}
            placeholder={t['ekle.urun.placeholder']}
            clearable
            accessibilityLabel="Ürün adı, isteğe bağlı"
          />
        </View>

        {sikAlinanlarListesi.length > 0 ? (
          <>
            <View style={{ height: rhythm.section }} />
            <View style={stil.pad}>
              <Txt role="label" tone={color.text2}>
                {t['ekle.sik_alinanlar']}
              </Txt>
            </View>
            <View style={{ height: rhythm.group }} />
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={[stil.yatayKaydir, { paddingHorizontal: layout.screenPaddingX }]}>
              {sikAlinanlarListesi.map((s) => (
                <Chip
                  key={s.urunAdi}
                  ad={s.urunAdi}
                  tutar={paraYaz(s.tutarKurus)}
                  dotColor={aileRenkleri(kategoriGetir(s.kategori).aile).solid}
                  onPress={() => sikAlinanSec(s)}
                />
              ))}
            </ScrollView>
          </>
        ) : null}

        <View style={{ height: rhythm.section }} />
        <View style={stil.pad}>
          <Txt role="label" tone={color.text2}>
            {t['ekle.kategori.etiket']}
          </Txt>
        </View>
        <View style={{ height: rhythm.group }} />
        <CategoryPicker
          value={kategoriKodu}
          onChange={(k) => {
            setKategoriKodu(k);
            setKategoriHata(undefined);
          }}
          error={kategoriHata}
        />

        <View style={{ height: rhythm.section }} />
        <View style={stil.pad}>
          <Txt role="label" tone={color.text2}>
            {t['ekle.odeme.etiket']}
          </Txt>
          <View style={{ height: rhythm.group }} />
          <View style={stil.odemeSatiri}>
            <View style={stil.segmentEsnek}>
              <SegmentedControl
                secenekler={[
                  { value: 'nakit' as OdemeTipi, label: t['ekle.odeme.nakit'], icon: 'banknote' },
                  { value: 'kart' as OdemeTipi, label: t['ekle.odeme.kart'], icon: 'credit-card' },
                ]}
                deger={odeme}
                onChange={odemeSec}
              />
            </View>
            {odeme === 'kart' ? (
              <>
                <View style={{ width: rhythm.blockInCard }} />
                <Chip
                  ad={t['ekle.taksit.baglanti']}
                  selected={taksitliAcik}
                  dotColor={color.primary}
                  onPress={() => setTaksitliAcik((a) => !a)}
                />
              </>
            ) : null}
          </View>
        </View>

        {taksitliAcik ? (
          <>
            <View style={{ height: rhythm.blockInCard }} />
            <View style={stil.pad}>
              <Txt role="label" tone={color.text2}>
                {t['ekle.taksit.baslik']}
              </Txt>
            </View>
            <View style={{ height: rhythm.group }} />
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={[stil.yatayKaydir, { paddingHorizontal: layout.screenPaddingX }]}>
              {TAKSIT_SECENEKLERI.map((n) => (
                <Chip
                  key={n}
                  ad={`${n} taksit`}
                  selected={taksitSayisi === n}
                  dotColor={color.primary}
                  onPress={() => setTaksitSayisi(n)}
                />
              ))}
            </ScrollView>
            {taksitSayisi ? (
              <>
                <View style={{ height: rhythm.group }} />
                <View style={stil.pad}>
                  <Txt role="caption" tone={color.text2}>
                    {ekleTaksitOnizleme(paraYaz(Math.round(tutarKurus / taksitSayisi), true), taksitSayisi)}
                  </Txt>
                </View>
              </>
            ) : null}
          </>
        ) : null}

        <View style={{ height: rhythm.section }} />
        <View style={[stil.pad, stil.satir]}>
          {sabitGunFarki ? null : (
            <>
              <Chip
                ad={t['ekle.tarih.dun']}
                selected={dun}
                dotColor={color.primary}
                onPress={() => setDun((d) => !d)}
                accessibilityLabel={dun ? 'Tarihi bugüne al' : 'Tarihi dün yap'}
              />
              <View style={{ width: rhythm.group }} />
            </>
          )}
          <Chip
            ad={t['ekle.not.ac']}
            selected={notAcik}
            dotColor={color.primary}
            onPress={() => setNotAcik((a) => !a)}
            accessibilityLabel="Not ekle"
          />
        </View>

        {notAcik ? (
          <>
            <View style={{ height: rhythm.group }} />
            <View style={stil.pad}>
              <TextField
                label={t['ekle.not.etiket']}
                value={notMetni}
                onChangeText={setNotMetni}
                placeholder={t['ekle.not.placeholder']}
                maxLength={60}
              />
            </View>
          </>
        ) : null}

        <View style={{ height: rhythm.section }} />
      </ScrollView>

      <View style={[stil.altSabit, { paddingBottom: insets.bottom + rhythm.group }]}>
        <View style={stil.pad}>
          <ClayKeypad
            onDigit={(d) => tutarDegistir((b) => tutarGirisiEkle(b, d))}
            onComma={() => tutarDegistir((b) => tutarGirisiEkle(b, ','))}
            onBackspace={() => tutarDegistir(tutarGirisiSil)}
          />
        </View>
        <View style={{ height: rhythm.blockInCard }} />
        <View style={stil.pad}>
          {yazmaHata ? (
            <>
              <Txt role="caption" tone={color.dangerInk}>
                {yazmaHata}
              </Txt>
              <View style={{ height: rhythm.group }} />
            </>
          ) : null}
          <Button
            label={t['eylem.kaydet']}
            variant="primary"
            disabled={tutarKurus <= 0}
            loading={kaydediliyor}
            onPress={kaydet}
          />
        </View>
      </View>
    </View>
  );
}

const stil = StyleSheet.create({
  ekran: { flex: 1, backgroundColor: color.bg },
  kaydir: { flex: 1 },
  kaydirIcerik: { paddingBottom: rhythm.section },
  pad: { paddingHorizontal: layout.screenPaddingX },
  satir: { flexDirection: 'row', alignItems: 'center' },
  odemeSatiri: { flexDirection: 'row', alignItems: 'center' },
  segmentEsnek: { flex: 1 },
  yatayKaydir: { flexDirection: 'row', alignItems: 'center', gap: rhythm.group },
  // §3.1 sabit alt blok üst boşluğu 8
  altSabit: { paddingTop: rhythm.group },
});
