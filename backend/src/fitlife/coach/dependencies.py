from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.coach.repositories import CoachSqlAlchemyRepository
from fitlife.coach.services import CoachService
from fitlife.database import SessionDep


async def get_coach_service(
    session: SessionDep, background_tasks: BackgroundTasks, security: SessionDep
) -> CoachService:
    return CoachService(CoachSqlAlchemyRepository(session), background_tasks, security)


CoachServiceDep = Annotated[CoachService, Depends(get_coach_service)]
