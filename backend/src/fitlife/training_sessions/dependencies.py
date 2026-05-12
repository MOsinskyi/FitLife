from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.coaches.dependencies import CoachRepositoryDep
from fitlife.config import settings
from fitlife.database import SessionDep
from fitlife.members.dependencies import MemberRepositoryDep
from fitlife.training_sessions.repositories import TrainingSessionRepository
from fitlife.training_sessions.services import TrainingSessionService


async def get_training_session_repository(
    session: SessionDep,
) -> TrainingSessionRepository:
    return TrainingSessionRepository(session)


TrainingSessionRepositoryDep = Annotated[
    TrainingSessionRepository, Depends(get_training_session_repository)
]


async def get_training_session_service(
    training_session_repository: TrainingSessionRepositoryDep,
    coach_repository: CoachRepositoryDep,
    member_repository: MemberRepositoryDep,
    background_tasks: BackgroundTasks,
) -> TrainingSessionService:
    cache_namespace: str = settings.cache.namespace.training_session

    return TrainingSessionService(
        training_session_repository,
        coach_repository,
        member_repository,
        background_tasks,
        cache_namespace,
    )


TrainingSessionServiceDep = Annotated[
    TrainingSessionService, Depends(get_training_session_service)
]
