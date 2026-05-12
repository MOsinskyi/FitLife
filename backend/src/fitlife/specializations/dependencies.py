from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.database import get_session
from fitlife.specializations.repositories import SpecializationRepository
from fitlife.specializations.services import SpecializationService


async def get_specialization_repository(
    session: AsyncSession = Depends(get_session),
) -> SpecializationRepository:
    return SpecializationRepository(session)


async def get_specialization_service(
    repository: SpecializationRepository = Depends(get_specialization_repository),
) -> SpecializationService:
    return SpecializationService(repository)


SpecializationServiceDep = Annotated[
    SpecializationService, Depends(get_specialization_service)
]
SpecializationRepositoryDep = Annotated[
    SpecializationRepository, Depends(get_specialization_repository)
]
