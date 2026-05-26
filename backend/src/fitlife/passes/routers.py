from fastapi import APIRouter
from .schemas import PassSchema
from .dependencies import PassServiceDep

pass_router = APIRouter(prefix="/passes", tags=["💰 Passes"])

@pass_router.get("/", response_model=list[PassSchema])
async def get_passes(service: PassServiceDep):
    return await service.get_active_passes()
