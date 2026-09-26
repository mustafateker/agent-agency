import { router } from 'expo-router';
import { useCallback, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Accordion } from '@/components/Accordion';
import { ErrorState } from '@/components/ErrorState';
import { IconButton } from '@/components/IconButton';
import { InfoStrip } from '@/components/InfoStrip';
import { RevScreen, useRevLoad } from '@/components/RevScreen';
import { SavingsSheet, type BirikimGirdisi } from '@/components/SavingsSheet';
import { BudgetCard } from '@/components/tasarruf/BudgetCard';
import { CategoryDistributionCard } from '@/components/tasarruf/CategoryDistributionCard';
import { MovementsSection } from '@/components/tasarruf/MovementsSection';
import { RealSavingsCard } from '@/components/tasarruf/RealSavingsCard';
import { RoutineSavingsCard } from '@/components/tasarruf/RoutineSavingsCard';
import { SavingsHeroCard, type HeroDurum } from '@/components/tasarruf/SavingsHeroCard';
import { SavingsSkeleton } from '@/components/tasarruf/SavingsSkeleton';
import { Txt } from '@/components/Txt';
import {
  a11yTasarrufBolum,
  ayLokatif,
  t,
  tasarrufButceTakipBasi,
  tasarrufHareketKaydedildiToast,
  tasarrufHareketSilindiToast,
  tasarrufMotivasyonBorc,
  tasarrufOzetBirikim,
  tasarrufOzetBirikimAyYokBuAy,
  tasarrufOzetBirikimAyYokGecmisAy,
  tasarrufOzetBirikimHedefYok,
  tasarrufOzetButce,
  tasarrufOzetButceDisinda,
  tasarrufOzetKategori,
  tasarrufOzetRutin,
  tasarrufUstSatir,
} from '@/content/metinler';
import {
  bugun,
  movementDelete,
  movementPut,
  routinesGet,
  savingsGet,
  movementsGet,
  yeniId,
  type Movement,
  type Savings,
} from '@/lib/revApi';
import { paraYaz } from '@/lib/para';
import { ayAnahtari, ayAnahtariFarkli, ayBasligi, ayGunSayisi, tarihtenGun } from '@/lib/tarih';
import { toastGoster } from '@/lib/toastBus';
import { veriDegisti } from '@/lib/veriBus';
import { color, layout, rhythm } from '@/theme/tokens';

/**
 * rev2-tasarruf-profil.md §3.12 — E-27 Tasarruf. Kahraman gösterge + DÖRT
 * akordiyon bölümü (A bütçe · B gerçek birikim+hareketler · C kategori ·
 * D rutin tasarrufu). Sözlük ayrımı korunur: *hesaplanan tasarruf* (A) ·
 * *gerçek birikim* (B) · *rutin tasarrufu* (D) — üçü hiçbir yerde toplanmaz.
 */
type BolumAnahtari = 'butce' | 'birikim' | 'kategori' | 'rutin';

export default function TasarruflarEkrani() {
  const [ay, setAy] = useState(() => bugun().slice(0, 7));
  const guncelAyMi = ay === bugun().slice(0, 7);

  const fetcher = useCallback(async () => {
    const [savings, ledger, rutinYaniti] = await Promise.all([savingsGet(ay), movementsGet(ay), routinesGet()]);
    return { savings, ledger, toplamRutinSayisi: rutinYaniti.rutinler.length };
  }, [ay]);
  const load = useRevLoad(fetcher);
  const d = load.data?.savings;
  const ledger = load.data?.ledger;
  const toplamRutinSayisi = load.data?.toplamRutinSayisi;

  // §3.12.3 (Hafıza) — yalnız ekranın ÖMRÜ boyunca: ay değiştirince korunur,
  // ekrandan çıkıp dönünce (bileşen yeniden mount olunca) varsayılana döner.
  const [acikBolum, setAcikBolum] = useState<Partial<Record<BolumAnahtari, boolean>>>({ butce: true });
  function bolumAc(anahtar: BolumAnahtari) {
    setAcikBolum((onceki) => ({ ...onceki, [anahtar]: !onceki[anahtar] }));
  }

  const [sheetAcik, setSheetAcik] = useState(false);
  const [duzenlenen, setDuzenlenen] = useState<Movement | null>(null);
  const [sheetYeniId, setSheetYeniId] = useState(yeniId);
  const [sheetBusy, setSheetBusy] = useState(false);
  const [sheetHata, setSheetHata] = useState<string>();

  function ayDegistir(fark: number) {
    setAy((onceki) => ayAnahtariFarkli(onceki, fark));
  }

  const ayAdiYil = ayBasligi(ay);
  const ayLokatifDeger = ayLokatif(Number(ay.split('-')[1]));

  function ekleAc() {
    setDuzenlenen(null);
    setSheetYeniId(yeniId());
    setSheetHata(undefined);
    setSheetAcik(true);
  }
  function duzenleAc(m: Movement) {
    setDuzenlenen(m);
    setSheetHata(undefined);
    setSheetAcik(true);
  }
  function sheetKapat() {
    if (sheetBusy) return;
    setSheetAcik(false);
  }

  async function kaydet(girdi: BirikimGirdisi) {
    setSheetBusy(true);
    setSheetHata(undefined);
    try {
      await movementPut(girdi);
      veriDegisti();
      await load.reload();
      setSheetAcik(false);
      toastGoster({ tur: 'info', metin: tasarrufHareketKaydedildiToast(paraYaz(Math.abs(girdi.tutar_kurus))) });
    } catch {
      setSheetHata(t['birikimSheet.hata.ag']);
    } finally {
      setSheetBusy(false);
    }
  }

  function silBaslat(m: Movement) {
    void silVeGeriAlSun(m);
    setSheetAcik(false);
  }

  async function silVeGeriAlSun(m: Movement) {
    await movementDelete(m.id);
    veriDegisti();
    await load.reload();
    toastGoster({
      tur: 'undo',
      metin: tasarrufHareketSilindiToast(paraYaz(Math.abs(m.tutar_kurus))),
      eylemEtiketi: t['toast.geri_al'],
      onEylem: async () => {
        await movementPut({ id: m.id, gun: m.gun, tutar_kurus: m.tutar_kurus, not_metni: m.not_metni });
        veriDegisti();
        await load.reload();
      },
    });
  }

  const header = (
    <View style={stil.ekranBasi}>
      <View style={stil.esnek}>
        <Txt role="caption">{load.error ? t['tasarruf.ustSatir.hata'] : load.loading ? ayAdiYil : tasarrufUstSatir(ayAdiYil, !guncelAyMi)}</Txt>
        <Txt role="h1" numberOfLines={1}>
          {t['tasarruf.baslik']}
        </Txt>
      </View>
    </View>
  );

  return (
    <RevScreen title={t['tasarruf.baslik']} tab="tasarruflar" header={header} contentGap={0}>
      {load.loading ? <SavingsSkeleton /> : null}

      {load.error ? (
        <>
          <View style={stil.hataPagerSatiri}>
            <IconButton icon="chevron-left" accessibilityLabel={t['a11y.tasarruf.oncekiAy']} onPress={() => ayDegistir(-1)} />
            <Txt role="label">{ayAdiYil}</Txt>
            <IconButton
              icon="chevron-right"
              accessibilityLabel={t['a11y.tasarruf.sonrakiAy']}
              onPress={() => ayDegistir(1)}
              disabled={guncelAyMi}
            />
          </View>
          <View style={{ height: rhythm.section }} />
          <ErrorState
            icon="wifi-off"
            baslik={t['tasarruf.hata.baslik']}
            govde={t['tasarruf.hata.alt']}
            butonEtiketi={t['tasarruf.hata.btn']}
            buttonVariant="secondary"
            onRetry={load.reload}
          />
        </>
      ) : null}

      {d && ledger && toplamRutinSayisi !== undefined && !load.loading && !load.error ? (
        <>
          <SavingsHeroCard
            durum={heroDurum(d)}
            butceTutari={d.harcanabilir_kurus === null ? null : paraYaz(d.harcanabilir_kurus)}
            guncelAyMi={guncelAyMi}
            ayLokatifDeger={ayLokatifDeger}
            oncekiPasif={ayAnahtari(tarihtenGun(d.takip_baslangic_gunu)) >= ay}
            sonrakiPasif={guncelAyMi}
            onOnceki={() => ayDegistir(-1)}
            onSonraki={() => ayDegistir(1)}
            onKipPress={() => router.push('/ayarlar')}
            onButcePress={() => router.push('/butce')}
          />

          {/* REV3-r1 §2.1 — kahraman kart ↔ akordiyon grubu 8 (aynı grubun devamı, eskiden 24). */}
          <View style={{ height: rhythm.group }} />

          <Accordion
            title={guncelAyMi ? t['tasarruf.bolum.butce'] : t['tasarruf.bolum.butceGecmis']}
            summary={butceOzeti(d)}
            expanded={!!acikBolum.butce}
            onToggle={() => bolumAc('butce')}
            accessibilityLabel={a11yTasarrufBolum(guncelAyMi ? t['tasarruf.bolum.butce'] : t['tasarruf.bolum.butceGecmis'], butceOzeti(d))}>
            {d.harcanabilir_kurus === null ? (
              <InfoStrip variant="info" icon="info" textTone={color.text} metin={takipBasiMetni(d.takip_baslangic_gunu, ay)} />
            ) : (
              <BudgetCard
                harcanabilirKurus={d.harcanabilir_kurus}
                harcananKurus={d.harcanan_kurus}
                kalanKurus={d.kalan_kurus ?? 0}
                toplamHarcamaKurus={d.toplam_harcama_kurus}
                tamamlananGun={d.tamamlanan_gun_sayisi}
                ayGunSayisi={ayGunSayisi(ay)}
                kumulatifKurus={d.kumulatif_tasarruf_kurus}
                bilinmeyenGunSayisi={d.bilinmeyen_gun_sayisi}
                overflowMi={(d.hesaplanan_tasarruf_kurus ?? 0) < 0}
              />
            )}
          </Accordion>

          <View style={{ height: rhythm.group }} />

          <Accordion
            title={t['tasarruf.bolum.birikim']}
            summary={birikimOzeti(d, guncelAyMi, ayLokatifDeger)}
            expanded={!!acikBolum.birikim}
            onToggle={() => bolumAc('birikim')}
            accessibilityLabel={a11yTasarrufBolum(t['tasarruf.bolum.birikim'], birikimOzeti(d, guncelAyMi, ayLokatifDeger))}>
            <RealSavingsCard
              guncelAyMi={guncelAyMi}
              ayLokatifDeger={ayLokatifDeger}
              gercekBirikimKurus={d.gercek_birikim_kurus}
              ayBirikimKurus={d.ay_birikim_kurus}
              hedefBirikimKurus={d.hedef_birikim_kurus}
              onEklePress={ekleAc}
              onHedefPress={() => router.push('/butce')}
              motivasyonStrip={
                <InfoStrip
                  variant="info"
                  icon="target"
                  textTone={color.text}
                  metin={d.motivasyon.tur === 'borc' ? tasarrufMotivasyonBorc(d.motivasyon.borc_yuzde ?? 0) : t['tasarruf.motivasyon.birikim']}
                />
              }
            />
            <View style={{ height: rhythm.blockInCard }} />
            <MovementsSection
              guncelAyMi={guncelAyMi}
              ayLokatifDeger={ayLokatifDeger}
              hareketler={ledger.hareketler}
              toplamKayit={ledger.hareketler.length}
              onRowPress={duzenleAc}
              onSwipeDelete={silBaslat}
              onTumuPress={() => router.push({ pathname: '/birikimler', params: { ay } })}
            />
          </Accordion>

          <View style={{ height: rhythm.group }} />

          <Accordion
            title={t['tasarruf.bolum.kategori']}
            summary={d.kategoriler.length === 0 ? t['tasarruf.ozet.kategoriYok'] : tasarrufOzetKategori(paraYaz(d.harcanan_kurus))}
            expanded={!!acikBolum.kategori}
            onToggle={() => bolumAc('kategori')}
            accessibilityLabel={a11yTasarrufBolum(
              t['tasarruf.bolum.kategori'],
              d.kategoriler.length === 0 ? t['tasarruf.ozet.kategoriYok'] : tasarrufOzetKategori(paraYaz(d.harcanan_kurus)),
            )}>
            <CategoryDistributionCard
              guncelAyMi={guncelAyMi}
              ayLokatifDeger={ayLokatifDeger}
              kategoriler={d.kategoriler}
              harcananToplam={d.harcanan_kurus}
              onTumunuGorPress={() => router.push('/ozet')}
            />
          </Accordion>

          <View style={{ height: rhythm.group }} />

          <Accordion
            title={t['tasarruf.bolum.rutin']}
            summary={toplamRutinSayisi === 0 ? t['tasarruf.ozet.rutinYok'] : tasarrufOzetRutin(paraYaz(d.rutin_tasarruf_kurus), toplamRutinSayisi)}
            expanded={!!acikBolum.rutin}
            onToggle={() => bolumAc('rutin')}
            accessibilityLabel={a11yTasarrufBolum(
              t['tasarruf.bolum.rutin'],
              toplamRutinSayisi === 0 ? t['tasarruf.ozet.rutinYok'] : tasarrufOzetRutin(paraYaz(d.rutin_tasarruf_kurus), toplamRutinSayisi),
            )}>
            <RoutineSavingsCard
              guncelAyMi={guncelAyMi}
              ayLokatifDeger={ayLokatifDeger}
              rutinler={d.rutinler}
              toplamKurus={d.rutin_tasarruf_kurus}
              toplamRutinSayisi={toplamRutinSayisi}
              onRutinleriAcPress={() => router.push('/rutinler')}
            />
          </Accordion>
        </>
      ) : null}

      <SavingsSheet
        visible={sheetAcik}
        editing={duzenlenen}
        yeniId={sheetYeniId}
        busy={sheetBusy}
        hata={sheetHata}
        mevcutBakiyeKurus={d?.gercek_birikim_kurus ?? 0}
        onKaydet={(girdi) => void kaydet(girdi)}
        onSil={duzenlenen ? () => silBaslat(duzenlenen) : undefined}
        onClose={sheetKapat}
      />
    </RevScreen>
  );
}

function heroDurum(d: Savings): HeroDurum {
  if (d.harcanabilir_kurus === null) return { tur: 'no-budget' };
  if (d.tamamlanan_gun_sayisi === 0) return { tur: 'empty' };
  const hesaplanan = d.hesaplanan_tasarruf_kurus ?? 0;
  if (hesaplanan < 0) return { tur: 'overflow', hesaplananTasarrufKurus: hesaplanan, harcanabilirKurus: d.harcanabilir_kurus };
  return {
    tur: 'default',
    hesaplananTasarrufKurus: hesaplanan,
    harcanabilirKurus: d.harcanabilir_kurus,
    tamamlananGun: d.tamamlanan_gun_sayisi,
  };
}

/** §3.12.4 — A bölümünün kapalı özeti: "Kalan {tutar}" · "Bütçe dışı {tutar}" · "Gelir eksik". */
function butceOzeti(d: Savings): string {
  if (d.harcanabilir_kurus === null) return t['tasarruf.ozet.butceGelirYok'];
  const overflowMi = (d.hesaplanan_tasarruf_kurus ?? 0) < 0;
  const tutar = paraYaz(Math.abs(d.kalan_kurus ?? 0));
  return overflowMi ? tasarrufOzetButceDisinda(tutar) : tasarrufOzetButce(tutar);
}

/** §3.12.4 — B bölümünün kapalı özeti: "{tutar} · hedefin %{n}'i" · "… kayıt yok" · "… hedef koymadın". */
function birikimOzeti(d: Savings, guncelAyMi: boolean, ayLokatifDeger: string): string {
  const tutar = paraYaz(d.gercek_birikim_kurus);
  if (d.hedef_birikim_kurus <= 0) return tasarrufOzetBirikimHedefYok(tutar);
  // İçerik satırının eşiğiyle AYNI (`RealSavingsCard`'daki `birikimAySatiri`) — tek kaynak.
  if (d.ay_birikim_kurus === 0) {
    return guncelAyMi ? tasarrufOzetBirikimAyYokBuAy(tutar) : tasarrufOzetBirikimAyYokGecmisAy(tutar, ayLokatifDeger);
  }
  const yuzde = Math.round(Math.min(1, d.gercek_birikim_kurus / d.hedef_birikim_kurus) * 100);
  return tasarrufOzetBirikim(tutar, yuzde);
}

/** `tasarruf.butce.takipBasi` — yalnız takip görüntülenen ayda başladıysa anlamlı (§3.4 no-budget). */
function takipBasiMetni(takipBaslangicGunu: string, gorunenAy: string): string {
  const tarih = tarihtenGun(takipBaslangicGunu);
  const ayinSonGunu = new Date(tarih.getFullYear(), tarih.getMonth() + 1, 0).getDate();
  const hesaplanacakGun = ayAnahtari(tarih) === gorunenAy ? ayinSonGunu - tarih.getDate() + 1 : ayinSonGunu;
  return tasarrufButceTakipBasi(tarih.getDate(), ayLokatif(tarih.getMonth() + 1), hesaplanacakGun);
}

const stil = StyleSheet.create({
  ekranBasi: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: layout.headerPadTop,
    paddingBottom: layout.headerPadBottom,
    paddingHorizontal: layout.screenPaddingX,
  },
  esnek: { flex: 1, minWidth: 0 },
  hataPagerSatiri: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
});
