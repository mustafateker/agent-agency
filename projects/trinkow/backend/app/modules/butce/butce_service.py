"""Calendar-day budgets preserve historical intent and keep cash separate from plans."""
from __future__ import annotations
from calendar import monthrange
from datetime import date
from hashlib import sha256
from typing import Any
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.butce.butce_dto import ButceIstegi, RutinIstegi, FavoriIstegi
from app.modules.butce.butce_model import KOLEKSIYONLAR


def gun_dogrula(gun: str) -> date:
    try:
        parsed = date.fromisoformat(gun)
        if parsed.isoformat() != gun:
            raise ValueError
        return parsed
    except ValueError:
        raise HTTPException(422, 'Geçerli tarih gerekli.') from None


def kimlik_dogrula(kimlik: str) -> None:
    if not kimlik or len(kimlik) > 100 or any(c in kimlik for c in '/.$:'):
        raise HTTPException(422, 'Geçersiz kayıt kimliği.')


def dis_gorunum(belge: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in belge.items() if k not in ('_id', 'kullanici_id')}


def gunluk_pay(aylik: int, gun: str) -> int:
    tarih = gun_dogrula(gun)
    adet = monthrange(tarih.year, tarih.month)[1]
    return aylik // adet + (aylik % adet if tarih.day == adet else 0)


def butce_hesapla(surum: dict[str, Any], gun: str) -> dict[str, Any]:
    gorunum = dis_gorunum(surum)
    gelir = surum.get('gelir_kurus')
    net = None if gelir is None else gelir - sum(surum['sabit_giderler'].values()) - surum['hedef_birikim_kurus']
    pay = None if net is None else gunluk_pay(max(0, net), gun)
    limit = surum['manuel_limit_kurus'] if surum['limit_modu'] == 'manuel' else pay
    kategoriler = surum.get('kategori_limitleri', {})
    # A shorter/longer month must not make automatic categories invalid. Keep the
    # explicitly selected amounts; show excess for editing rather than rescale.
    gorunum.update(gunluk_limit_kurus=limit, gunluk_gelir_payi_kurus=pay,
                   dagitilmamis_kurus=None if limit is None else limit - sum(kategoriler.values()),
                   butce_acigi_kurus=0 if net is None else max(0, -net))
    return gorunum


class ButceService:
    def __init__(self, veritabani: AsyncIOMotorDatabase) -> None:
        self.db = veritabani

    async def hesap_verilerini_sil(self, kullanici_id: str) -> None:
        for ad in KOLEKSIYONLAR:
            await self.db[ad].delete_many({'kullanici_id': kullanici_id})

    async def gocu_garanti_et(self, kullanici_id: str, bugun: str) -> None:
        gun_dogrula(bugun)
        mevcut = await self.db.butce_gocleri.find_one({'_id': kullanici_id})
        if mevcut:
            return
        profil = await self.db.kullanici_profilleri.find_one({'kullanici_id': kullanici_id}) or {}
        eski = await self.db.kategori_limitleri.find({'kullanici_id': kullanici_id}).to_list(None)
        await self.db.butce_gocleri.update_one({'_id': kullanici_id}, {'$setOnInsert': {
            'kullanici_id': kullanici_id, 'takip_baslangic_gunu': bugun,
            'eski_aylik_kategori_limitleri': [dis_gorunum(x) for x in eski],
        }}, upsert=True)
        if not profil:
            return
        limit = profil.get('gunluk_limit_kurus')
        gelir = profil.get('gelir_kurus')
        hedef = profil.get('birikim_kurus') or 0
        istek = ButceIstegi(gelir_kurus=gelir, sabit_giderler={
            'kira': profil.get('kira_aidat_kurus') or 0, 'fatura': profil.get('faturalar_kurus') or 0,
            'ulasim': profil.get('ulasim_yakit_kurus') or 0, 'kredi': profil.get('kredi_taksit_kurus') or 0,
        }, hedef_birikim_kurus=hedef, limit_modu='manuel' if limit and limit > 0 else 'otomatik',
            manuel_limit_kurus=limit if limit and limit > 0 else None)
        belge = istek.model_dump() | {'kullanici_id': kullanici_id, 'yururluk_gunu': bugun}
        await self.db.butce_surumleri.update_one({'_id': f'{kullanici_id}:{bugun}'}, {'$setOnInsert': belge}, upsert=True)

    async def surumler(self, kullanici_id: str) -> list[dict[str, Any]]:
        return await self.db.butce_surumleri.find({'kullanici_id': kullanici_id}).sort('yururluk_gunu', 1).to_list(None)

    async def getir(self, kullanici_id: str, bugun: str, gun: str | None = None) -> dict[str, Any]:
        await self.gocu_garanti_et(kullanici_id, bugun)
        gun = gun or bugun
        gun_dogrula(gun)
        surum = await self.db.butce_surumleri.find_one({'kullanici_id': kullanici_id, 'yururluk_gunu': {'$lte': gun}}, sort=[('yururluk_gunu', -1)])
        goc = await self.db.butce_gocleri.find_one({'_id': kullanici_id})
        return {'gun': gun, 'butce': butce_hesapla(surum, gun) if surum else None,
                'eski_aylik_kategori_limitleri': goc['eski_aylik_kategori_limitleri']}

    async def yaz(self, kullanici_id: str, bugun: str, istek: ButceIstegi) -> dict[str, Any]:
        await self.gocu_garanti_et(kullanici_id, bugun)
        belge = istek.model_dump() | {'kullanici_id': kullanici_id, 'yururluk_gunu': bugun}
        if belge['limit_modu'] == 'otomatik':
            belge['manuel_limit_kurus'] = None
        # Validate against ordinary days, excluding the last-day rounding residue.
        ilk = bugun[:8] + '01'
        limit = butce_hesapla(belge, ilk)['gunluk_limit_kurus']
        if sum(istek.kategori_limitleri.values()) > (limit or 0):
            raise HTTPException(422, 'Kategori payları günlük limiti aşamaz.')
        await self.db.butce_surumleri.replace_one({'_id': f'{kullanici_id}:{bugun}'}, belge, upsert=True)
        guncel = butce_hesapla(belge, bugun)['gunluk_limit_kurus']
        await self.db.kullanici_profilleri.update_one({'kullanici_id': kullanici_id}, {'$set': {
            'gelir_kurus': istek.gelir_kurus, 'gunluk_limit_kurus': guncel, 'gunluk_limit_onerisi_kurus': None,
            'kira_aidat_kurus': istek.sabit_giderler.kira, 'faturalar_kurus': istek.sabit_giderler.fatura,
            'ulasim_yakit_kurus': istek.sabit_giderler.ulasim, 'kredi_taksit_kurus': istek.sabit_giderler.kredi,
            'birikim_kurus': istek.hedef_birikim_kurus,
        }}, upsert=True)
        if guncel is not None:
            await self.db.limit_gecmisleri.update_one({'kullanici_id': kullanici_id, 'yururluk_tarihi': bugun},
                {'$set': {'kurus': guncel}}, upsert=True)
        return await self.getir(kullanici_id, bugun)

    async def manuel_limit_yaz(self, kullanici_id: str, bugun: str, limit: int) -> None:
        mevcut = (await self.getir(kullanici_id, bugun))['butce'] or {}
        girdi = {k: v for k, v in mevcut.items() if k in ButceIstegi.model_fields}
        girdi.update(limit_modu='manuel', manuel_limit_kurus=limit)
        await self.yaz(kullanici_id, bugun, ButceIstegi(**girdi))

    async def rutinler(self, kullanici_id: str, bugun: str, gun: str | None = None) -> list[dict[str, Any]]:
        await self.gocu_garanti_et(kullanici_id, bugun)
        gun = gun or bugun
        gun_dogrula(gun)
        kayitlar = await self.db.rutin_surumleri.find({'kullanici_id': kullanici_id, 'yururluk_gunu': {'$lte': gun}}).sort('yururluk_gunu', 1).to_list(None)
        son = {x['id']: dis_gorunum(x) for x in kayitlar}
        return list(son.values())

    async def rutin_yaz(self, kullanici_id: str, bugun: str, kimlik: str, istek: RutinIstegi) -> dict[str, Any]:
        kimlik_dogrula(kimlik)
        await self.gocu_garanti_et(kullanici_id, bugun)
        belge = istek.model_dump() | {'kullanici_id': kullanici_id, 'id': kimlik, 'yururluk_gunu': bugun}
        await self.db.rutin_surumleri.replace_one({'_id': f'{kullanici_id}:{kimlik}:{bugun}'}, belge, upsert=True)
        return dis_gorunum(belge)

    async def vazgecme_yaz(self, kullanici_id: str, bugun: str, kimlik: str, gun: str, adet: int) -> dict[str, Any]:
        gun_dogrula(gun)
        if gun > bugun:
            raise HTTPException(422, 'Gelecek güne vazgeçme eklenemez.')
        rutin = next((r for r in await self.rutinler(kullanici_id, bugun, gun) if r['id'] == kimlik and r['aktif']), None)
        if rutin is None:
            raise HTTPException(404, 'O gün için rutin bulunamadı.')
        alinan = await self.db.harcamalar.find({'kullanici_id': kullanici_id, 'gun': gun, 'rutin_id': kimlik}).to_list(None)
        kalan = max(0, rutin['gunluk_adet'] - sum(x.get('adet', 1) for x in alinan))
        if adet > kalan:
            raise HTTPException(422, 'Vazgeçilen adet, kalan rutin adedini aşamaz.')
        belge = {'kullanici_id': kullanici_id, 'rutin_id': kimlik, 'gun': gun, 'adet': adet,
                 'birim_fiyat_kurus': rutin['birim_fiyat_kurus'], 'kategori': rutin['kategori'], 'ad': rutin['ad']}
        await self.db.rutin_vazgecmeleri.replace_one({'_id': f'{kullanici_id}:{kimlik}:{gun}'}, belge, upsert=True)
        return {'rutin_id': kimlik, 'gun': gun, 'adet': adet, 'tasarruf_kurus': adet * rutin['birim_fiyat_kurus']}

    async def vazgecmeler(self, kullanici_id: str, baslangic: str, bitis: str) -> list[dict[str, Any]]:
        kayitlar = await self.db.rutin_vazgecmeleri.find({'kullanici_id': kullanici_id, 'gun': {'$gte': baslangic, '$lte': bitis}}).to_list(None)
        rutin_sur = await self.db.rutin_surumleri.find({'kullanici_id': kullanici_id, 'yururluk_gunu': {'$lte': bitis}}).sort('yururluk_gunu', 1).to_list(None)
        harcamalar = await self.db.harcamalar.find({'kullanici_id': kullanici_id, 'gun': {'$gte': baslangic, '$lte': bitis}, 'rutin_id': {'$ne': None}}).to_list(None)
        sonuc = []
        for kayit in kayitlar:
            rutin = next((r for r in reversed(rutin_sur) if r['id'] == kayit['rutin_id'] and r['yururluk_gunu'] <= kayit['gun']), None)
            alinan = sum(x.get('adet', 1) for x in harcamalar if x.get('rutin_id') == kayit['rutin_id'] and x['gun'] == kayit['gun'])
            adet = min(kayit['adet'], max(0, rutin['gunluk_adet'] - alinan)) if rutin and rutin['aktif'] else 0
            sonuc.append(dis_gorunum(kayit) | {'adet': adet, 'tasarruf_kurus': adet * kayit['birim_fiyat_kurus']})
        return sonuc

    async def favori_yaz(self, kullanici_id: str, kimlik: str, istek: FavoriIstegi) -> dict[str, Any]:
        kimlik_dogrula(kimlik)
        belge = istek.model_dump() | {'kullanici_id': kullanici_id, 'id': kimlik, 'sabitlenmis': True, 'kullanim_sayisi': 0}
        await self.db.favori_kalemler.replace_one({'_id': f'{kullanici_id}:{kimlik}'}, belge, upsert=True)
        return dis_gorunum(belge)

    async def favori_sil(self, kullanici_id: str, kimlik: str) -> None:
        await self.db.favori_kalemler.delete_one({'_id': f'{kullanici_id}:{kimlik}', 'kullanici_id': kullanici_id})

    async def sik_kullanilanlar(self, kullanici_id: str, bugun: str) -> list[dict[str, Any]]:
        gun_dogrula(bugun)
        sabit = await self.db.favori_kalemler.find({'kullanici_id': kullanici_id}).to_list(None)
        kayitlar = await self.db.harcamalar.find({'kullanici_id': kullanici_id, 'gun': {'$lte': bugun}, 'urun_adi': {'$nin': [None, '']}}).sort([('gun', -1), ('zaman', -1), ('_id', -1)]).to_list(None)
        gruplar: dict[tuple[str, str], dict[str, Any]] = {}
        for x in kayitlar:
            anahtar = (x['kategori'], x['urun_adi'].strip().casefold())
            if anahtar not in gruplar:
                kimlik = sha256(('|'.join(anahtar)).encode()).hexdigest()[:24]
                gruplar[anahtar] = {'id': kimlik, 'ad': x['urun_adi'], 'kategori': x['kategori'], 'tutar_kurus': x['tutar_kurus'], 'sabitlenmis': False, 'kullanim_sayisi': 0}
            gruplar[anahtar]['kullanim_sayisi'] += 1
        sonuc = []
        for x in sabit:
            anahtar = (x['kategori'], x['ad'].strip().casefold())
            x['kullanim_sayisi'] = gruplar.pop(anahtar, {}).get('kullanim_sayisi', 0)
            sonuc.append(dis_gorunum(x))
        sonuc.extend(sorted(gruplar.values(), key=lambda x: -x['kullanim_sayisi']))
        return sonuc[:12]
