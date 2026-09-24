"""Savings analytics distinguish unused budget, routine choices and actual cash."""
from __future__ import annotations
from calendar import monthrange
from datetime import date, timedelta
from typing import Any
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from app.modules.butce.butce_service import ButceService, gun_dogrula, gunluk_pay, butce_hesapla, kimlik_dogrula
from app.modules.tasarruf.tasarruf_dto import BirikimIstegi


def ay_gunleri(ay: str) -> list[str]:
    ilk = gun_dogrula(ay + '-01')
    return [date(ilk.year, ilk.month, n).isoformat() for n in range(1, monthrange(ilk.year, ilk.month)[1] + 1)]


def efektif_surum(surumler: list[dict[str, Any]], gun: str) -> dict[str, Any] | None:
    return next((s for s in reversed(surumler) if s['yururluk_gunu'] <= gun), None)


def ay_hesapla(ay: str, bugun: str, surumler: list[dict[str, Any]], harcamalar: list[dict[str, Any]], takip: str) -> dict[str, Any]:
    """Only tracked, completed calendar days earn calculated (not actual) savings."""
    gunler = ay_gunleri(ay)
    paylar: dict[str, int | None] = {}
    sabit_paylar = {k: 0 for k in ('kira', 'fatura', 'ulasim', 'kredi')}
    for gun in gunler:
        s = efektif_surum(surumler, gun) if gun >= takip else None
        paylar[gun] = butce_hesapla(s, gun)['gunluk_gelir_payi_kurus'] if s else None
        if s:
            for kod, tutar in s['sabit_giderler'].items():
                sabit_paylar[kod] += gunluk_pay(tutar, gun)
    toplam = 0
    harcanan = 0
    tamamlanan_harcama = 0
    kategoriler: dict[str, int] = {}
    for h in sorted(harcamalar, key=lambda x: (x['gun'], x.get('zaman', ''))):
        if not h['gun'].startswith(ay) or h['gun'] > bugun:
            continue
        toplam += h['tutar_kurus']
        tutar = h['tutar_kurus']
        kod = h.get('sabit_gider_kodu')
        if kod and kod in sabit_paylar and h['gun'] >= takip:
            karsilanan = min(sabit_paylar[kod], tutar)
            sabit_paylar[kod] -= karsilanan
            tutar -= karsilanan
        # Pre-tracking entries remain visible in total history, but cannot consume
        # a budget that did not exist then.
        if h['gun'] < takip:
            continue
        harcanan += tutar
        kategoriler[h['kategori']] = kategoriler.get(h['kategori'], 0) + tutar
        if h['gun'] < bugun:
            tamamlanan_harcama += tutar
    takipli = [g for g in gunler if g >= takip]
    tamamlanan = [g for g in takipli if g < bugun]
    butce_biliniyor = bool(takipli) and all(paylar[g] is not None for g in takipli)
    kapanmis_biliniyor = all(paylar[g] is not None for g in tamamlanan)
    butce = sum(paylar[g] or 0 for g in takipli) if butce_biliniyor else None
    tasarruf = sum(paylar[g] or 0 for g in tamamlanan) - tamamlanan_harcama if kapanmis_biliniyor else None
    return {'harcanabilir_kurus': butce, 'harcanan_kurus': harcanan, 'toplam_harcama_kurus': toplam,
            'kalan_kurus': None if butce is None else butce - harcanan,
            'hesaplanan_tasarruf_kurus': tasarruf, 'bilinmeyen_gun_sayisi': sum(v is None for v in paylar.values()),
            'tamamlanan_gun_sayisi': len(tamamlanan),
            'kategoriler': [{'kategori': k, 'harcanan_kurus': v, 'rutin_tasarruf_kurus': 0} for k, v in kategoriler.items()]}


class TasarrufService:
    def __init__(self, veritabani: AsyncIOMotorDatabase) -> None:
        self.db = veritabani
        self.butce = ButceService(veritabani)

    async def birikimler(self, kullanici_id: str, ay: str | None = None) -> dict[str, Any]:
        if ay:
            ay_gunleri(ay)
        defter = await self.db.birikim_defterleri.find_one({'_id': kullanici_id}) or {}
        tum = defter.get('hareketler', [])
        hareketler = [x for x in tum if not ay or x['gun'].startswith(ay)]
        return {'hareketler': sorted(hareketler, key=lambda x: (x['gun'], x['id']), reverse=True),
                'toplam_kurus': sum(x['tutar_kurus'] for x in tum)}

    async def _defteri_degistir(self, kullanici_id: str, kimlik: str, hareket: dict[str, Any] | None) -> None:
        kimlik_dogrula(kimlik)
        for _ in range(10):
            mevcut = await self.db.birikim_defterleri.find_one({'_id': kullanici_id})
            eski = mevcut.get('hareketler', []) if mevcut else []
            yeni = [x for x in eski if x['id'] != kimlik]
            if hareket:
                yeni.append(hareket)
            if sum(x['tutar_kurus'] for x in yeni) < 0:
                raise HTTPException(422, 'Birikim bakiyesi sıfırın altına inemez.')
            rev = mevcut.get('surum', 0) if mevcut else 0
            belge = {'_id': kullanici_id, 'kullanici_id': kullanici_id, 'surum': rev + 1, 'hareketler': yeni}
            if mevcut:
                sonuc = await self.db.birikim_defterleri.replace_one({'_id': kullanici_id, 'surum': rev}, belge)
                if sonuc.modified_count:
                    return
            else:
                try:
                    await self.db.birikim_defterleri.insert_one(belge)
                    return
                except DuplicateKeyError:
                    continue
        raise HTTPException(409, 'Birikim kaydı değişti; yeniden deneyin.')

    async def birikim_yaz(self, kullanici_id: str, kimlik: str, bugun: str, istek: BirikimIstegi) -> dict[str, Any]:
        gun_dogrula(istek.gun)
        gun_dogrula(bugun)
        if istek.gun > bugun:
            raise HTTPException(422, 'Gelecek güne gerçekleşmiş birikim eklenemez.')
        hareket = istek.model_dump() | {'id': kimlik}
        await self._defteri_degistir(kullanici_id, kimlik, hareket)
        return hareket

    async def birikim_sil(self, kullanici_id: str, kimlik: str) -> None:
        await self._defteri_degistir(kullanici_id, kimlik, None)

    async def ay_getir(self, kullanici_id: str, ay: str, bugun: str) -> dict[str, Any]:
        gun_dogrula(bugun)
        gunler = ay_gunleri(ay)
        if ay > bugun[:7]:
            raise HTTPException(422, 'Gelecek ayın tasarrufu henüz oluşmadı.')
        await self.butce.gocu_garanti_et(kullanici_id, bugun)
        goc = await self.db.butce_gocleri.find_one({'_id': kullanici_id})
        takip = goc['takip_baslangic_gunu']
        surumler = await self.butce.surumler(kullanici_id)
        kayitlar = await self.db.harcamalar.find({'kullanici_id': kullanici_id, 'gun': {'$lte': min(gunler[-1], bugun)}}).to_list(None)
        sonuc = ay_hesapla(ay, bugun, surumler, kayitlar, takip)
        kumulatif: int | None = 0
        tarih = date.fromisoformat(takip[:7] + '-01')
        while tarih.isoformat()[:7] <= ay:
            deger = ay_hesapla(tarih.isoformat()[:7], bugun, surumler, kayitlar, takip)['hesaplanan_tasarruf_kurus']
            if deger is None:
                kumulatif = None
                break
            kumulatif += deger
            tarih = (tarih.replace(day=28) + timedelta(days=4)).replace(day=1)
        ledger = await self.birikimler(kullanici_id)
        # Past monthly screens show the balance at the selected month's end.
        hareketler = [x for x in ledger['hareketler'] if x['gun'] <= min(bugun, gunler[-1])]
        gercek = sum(x['tutar_kurus'] for x in hareketler)
        ay_birikim = sum(x['tutar_kurus'] for x in hareketler if x['gun'].startswith(ay))
        vazgecmeler = await self.butce.vazgecmeler(kullanici_id, gunler[0], min(bugun, gunler[-1]))
        rutinler: dict[str, dict[str, Any]] = {}
        kat = {x['kategori']: x for x in sonuc['kategoriler']}
        for x in vazgecmeler:
            kod = x['kategori']
            kat.setdefault(kod, {'kategori': kod, 'harcanan_kurus': 0, 'rutin_tasarruf_kurus': 0})['rutin_tasarruf_kurus'] += x['tasarruf_kurus']
            rutinler.setdefault(x['rutin_id'], {'rutin_id': x['rutin_id'], 'ad': x['ad'], 'tasarruf_kurus': 0})['tasarruf_kurus'] += x['tasarruf_kurus']
        secili = efektif_surum(surumler, min(bugun, gunler[-1])) or {}
        borc = secili.get('borc_kurus')
        oran = min(100, gercek * 100 // borc) if borc and gercek > 0 else (0 if borc else None)
        mesaj = f'Gerçek birikimin borcunun %{oran} tutarına denk geliyor. Adım adım devam edebilirsin.' if borc else 'Küçük adımlar birikimine dönüşebilir.'
        return sonuc | {'ay': ay, 'takip_baslangic_gunu': takip, 'kumulatif_tasarruf_kurus': kumulatif,
            'gercek_birikim_kurus': gercek, 'ay_birikim_kurus': ay_birikim,
            'hedef_birikim_kurus': secili.get('hedef_birikim_kurus', 0),
            'rutin_tasarruf_kurus': sum(x['tasarruf_kurus'] for x in vazgecmeler),
            'kategoriler': list(kat.values()), 'rutinler': list(rutinler.values()),
            'motivasyon': {'tur': 'borc' if borc else 'birikim', 'mesaj': mesaj, 'borc_kurus': borc, 'borc_yuzde': oran}}
