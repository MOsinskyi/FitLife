from typing import Annotated

from fastapi import Depends

from fitlife.coaches.repositories import CoachRepository
from fitlife.database import SessionDep
from fitlife.members.repositories import MemberRepository
from fitlife.training_sessions.repositories import TrainingSessionRepository
from fitlife.training_sessions.services import TrainingSessionService


async def get_training_session_repository(session: SessionDep) -> TrainingSessionRepository:
    return TrainingSessionRepository(session)


async def get_training_session_service(
    session: SessionDep,
    training_session_repository: Annotated[TrainingSessionRepository, Depends(get_training_session_repository)],
) -> TrainingSessionService:
    coach_repository = CoachRepository(session)
    member_repository = MemberRepository(session)
    return TrainingSessionService(training_session_repository, coach_repository, member_repository)


TrainingSessionServiceDep = Annotated[TrainingSessionService, Depends(get_training_session_service)]
