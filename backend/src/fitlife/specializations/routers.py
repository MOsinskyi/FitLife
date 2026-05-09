from fastapi import APIRouter
from fitlife.specializations.dependencies import SpecializationServiceDep
from fitlife.specializations.schemas import SpecializationResponse

specialization_router = APIRouter(prefix='/specializations', tags=['specializations'])

@specialization_router.get('', response_model=list[SpecializationResponse])
async def get_specializations(service: SpecializationServiceDep):
    return await service.get_all_specializations()
