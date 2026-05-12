from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.config import settings
from fitlife.database import SessionDep
from fitlife.security import SecurityDep
from fitlife.specializations.dependencies import SpecializationRepositoryDep

from .repositories import CoachRepository
from .services import CoachService


def get_coach_repository(session: SessionDep) -> CoachRepository:
    return CoachRepository(session)


CoachRepositoryDep = Annotated[CoachRepository, Depends(get_coach_repository)]


def get_coach_service(
    repository: CoachRepositoryDep,
    specialization_repository: SpecializationRepositoryDep,
    security: SecurityDep,
    background_tasks: BackgroundTasks,
) -> CoachService:
    cache_namespace: str = settings.cache.namespace.coach

    return CoachService(
        repository,
        specialization_repository,
        security,
        background_tasks,
        cache_namespace,
    )


CoachServiceDep = Annotated[CoachService, Depends(get_coach_service)]
