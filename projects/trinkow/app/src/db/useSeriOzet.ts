import { useSQLiteContext } from 'expo-sqlite';
import { useCallback, useEffect, useState } from 'react';

import { gunlukLimit } from '@/db/harcama';
import { seriDurumuHesapla, type SeriDurumu } from '@/db/seri';
import { veriDegisimineAbone } from '@/lib/veriBus';

/**
 * Günlük ekranının başlığında (her sayfada aynı) gösterilen seri özeti +
 * milestone kutlama tetiği. `app/index.tsx` bunu bir kez okur, tüm gün
 * sayfalarına prop olarak geçirir (her sayfa aynı sorguyu tekrarlamasın).
 */
export function useSeriOzet(): { yukleniyor: boolean; hata: boolean; durum: SeriDurumu | null; yenile: () => void } {
  const db = useSQLiteContext();
  const [veri, setVeri] = useState<{ yukleniyor: boolean; hata: boolean; durum: SeriDurumu | null }>({
    yukleniyor: true,
    hata: false,
    durum: null,
  });

  const oku = useCallback(async () => {
    try {
      const limitKurus = await gunlukLimit(db);
      const durum = await seriDurumuHesapla(db, new Date(), limitKurus);
      setVeri({ yukleniyor: false, hata: false, durum });
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
