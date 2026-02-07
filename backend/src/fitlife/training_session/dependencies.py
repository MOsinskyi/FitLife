from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.database import SessionDep

from .repositories import TrainingSessionSqlAlchemyRepository
from .services import TrainingSessionService


async def get_training_session_service(
    session: SessionDep,
    background_tasks: BackgroundTasks,
) -> TrainingSessionService:
    return TrainingSessionService(
        TrainingSessionSqlAlchemyRepository(session),
        background_tasks,
    )


TrainingSessionServiceDep = Annotated[TrainingSessionService, Depends(get_training_session_service)]
