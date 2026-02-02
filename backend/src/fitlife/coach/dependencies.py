from fastapi import BackgroundTasks, Depends
from sqlalchemy.sql.annotation import Annotated

from fitlife.coach.repositories import CoachSqlAlchemyRepository
from fitlife.coach.services import CoachService
from fitlife.database import SessionDep


async def get_coach_service(session: SessionDep, background_tasks: BackgroundTasks):
    return CoachService(CoachSqlAlchemyRepository(session), background_tasks)


CoachServiceDep = Annotated[CoachService, Depends(get_coach_service)]
