from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.database import get_session
from .repositories import PassRepository, PassFeatureRepository
from .services import PassService

async def get_pass_service(session: Annotated[AsyncSession, Depends(get_session)]) -> PassService:
    repository = PassRepository(session)
    feature_repository = PassFeatureRepository(session)
    return PassService(repository, feature_repository)

PassServiceDep = Annotated[PassService, Depends(get_pass_service)]
