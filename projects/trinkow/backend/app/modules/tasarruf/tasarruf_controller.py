"""Savings reporting and explicit cash-ledger HTTP contracts."""
from typing import Any
from fastapi import APIRouter, Depends, Response
from app.core.database import get_database
from app.modules.auth.auth_controller import gecerli_kullanici_id
from app.modules.tasarruf.tasarruf_service import TasarrufService
from app.modules.tasarruf.tasarruf_dto import BirikimIstegi
router = APIRouter(prefix='/tasarruf', tags=['tasarruf'])

def servis() -> TasarrufService:
    return TasarrufService(get_database())

@router.get('/ay')
async def ay_getir(ay: str, bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: TasarrufService = Depends(servis)) -> dict[str, Any]:
    return await svc.ay_getir(uid, ay, bugun)

@router.get('/birikimler')
async def birikimler(ay: str | None = None, uid: str = Depends(gecerli_kullanici_id), svc: TasarrufService = Depends(servis)) -> dict[str, Any]:
    return await svc.birikimler(uid, ay)

@router.put('/birikimler/{kimlik}')
async def birikim_yaz(kimlik: str, istek: BirikimIstegi, bugun: str, uid: str = Depends(gecerli_kullanici_id), svc: TasarrufService = Depends(servis)) -> dict[str, Any]:
    return await svc.birikim_yaz(uid, kimlik, bugun, istek)

@router.delete('/birikimler/{kimlik}', status_code=204)
async def birikim_sil(kimlik: str, uid: str = Depends(gecerli_kullanici_id), svc: TasarrufService = Depends(servis)) -> Response:
    await svc.birikim_sil(uid, kimlik)
    return Response(status_code=204)
