import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useState } from 'react';

import { gunAraligiToplamlari, gunlukLimit } from '@/db/harcama';
import { gunSeriDurumu, seriDurumuHesapla, type GunSeriDurumu, type SeriDurumu } from '@/db/seri';
import { gunAnahtari, gunEkle, haftaAraligi } from '@/lib/tarih';
import { veriDegisimineAbone } from '@/lib/veriBus';

const PENCERE_GUN = 28;

export type SeriIzgaraGunu = { gun: number; anahtar: string; durum: GunSeriDurumu };

export type SeriEkraniVerisi = {
  yukleniyor: boolean;
  hata: boolean;
  durum: SeriDurumu | null;
  izgara: SeriIzgaraGunu[];
  pencereEtiketi: string;
};

/** E-21 Seri ekranı — seri durumu + "son 4 hafta" ızgarası (kapanmış günler, bugün hariç). */
export function useSeriEkrani(): SeriEkraniVerisi & { yenile: () => void } {
  const db = useSQLiteContext();
  const [veri, setVeri] = useState<SeriEkraniVerisi>({
    yukleniyor: true,
    hata: false,
    durum: null,
    izgara: [],
    pencereEtiketi: '',
  });

  const oku = useCallback(async () => {
    try {
      const bugun = new Date();
      const limitKurus = await gunlukLimit(db);
      const bitis = gunEkle(bugun, -1);
      const baslangic = gunEkle(bugun, -PENCERE_GUN);
      const [durum, toplamlar] = await Promise.all([
        seriDurumuHesapla(db, bugun, limitKurus),
        gunAraligiToplamlari(db, gunAnahtari(baslangic), gunAnahtari(bitis)),
      ]);
      const izgara: SeriIzgaraGunu[] = [];
      for (let i = 0; i < PENCERE_GUN; i += 1) {
        const tarih = gunEkle(baslangic, i);
        const anahtar = gunAnahtari(tarih);
        const t = toplamlar.get(anahtar);
        izgara.push({
          gun: tarih.getDate(),
          anahtar,
          durum: gunSeriDurumu(t?.toplamKurus ?? 0, t?.kayitAdedi ?? 0, limitKurus),
        });
      }
      setVeri({
        yukleniyor: false,
        hata: false,
        durum,
        izgara,
        pencereEtiketi: haftaAraligi(baslangic, bitis),
      });
    } catch {
      setVeri((o) => ({ ...o, yukleniyor: false, hata: true }));
    }
  }, [db]);

  useEffect(() => {
    void oku();
  }, [oku]);
  useEffect(() => veriDegisimineAbone(() => void oku()), [oku]);

  return { ...veri, yenile: () => void oku() };
}
