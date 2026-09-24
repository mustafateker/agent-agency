"""Authenticated HTTP boundary for versioned budgets and routine choices."""
from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Depends, Response
from app.core.database import get_database
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.butce.butce_dto import ButceIstegi, RutinIstegi, VazgecmeIstegi, FavoriIstegi
from app.modules.butce.butce_service import ButceService

router = APIRouter(prefix='/butce', tags=['butce'])

def servis() -> ButceService:
    return ButceService(get_database())

@router.get('')
async def getir(bugun: str, gun: str | None = None, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return await svc.getir(uid, bugun, gun)

@router.put('')
async def yaz(istek: ButceIstegi, bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return await svc.yaz(uid, bugun, istek)

@router.get('/rutinler')
async def rutinler(bugun: str, gun: str | None = None, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return {'rutinler': await svc.rutinler(uid, bugun, gun)}

@router.put('/rutinler/{kimlik}')
async def rutin_yaz(kimlik: str, istek: RutinIstegi, bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return await svc.rutin_yaz(uid, bugun, kimlik, istek)

@router.put('/rutinler/{kimlik}/vazgecme')
async def vazgec(kimlik: str, istek: VazgecmeIstegi, bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return await svc.vazgecme_yaz(uid, bugun, kimlik, istek.gun, istek.adet)

@router.get('/sik-kullanilanlar')
async def favoriler(bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return {'kalemler': await svc.sik_kullanilanlar(uid, bugun)}

@router.put('/sik-kullanilanlar/{kimlik}')
async def favori_yaz(kimlik: str, istek: FavoriIstegi, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> dict[str, Any]:
    return await svc.favori_yaz(uid, kimlik, istek)

@router.delete('/sik-kullanilanlar/{kimlik}', status_code=204)
async def favori_sil(kimlik: str, uid: str = Depends(gecerli_kullanici_id), svc: ButceService = Depends(servis)) -> Response:
    await svc.favori_sil(uid, kimlik)
    return Response(status_code=204)
