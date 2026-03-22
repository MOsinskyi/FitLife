from typing import Annotated

from fastapi import Depends

from fitlife.database import SessionDep
from fitlife.security import SecurityDep

from .repositories import CoachRepository
from .services import CoachService


def get_member_repository(session: SessionDep) -> CoachRepository:
    return CoachRepository(session)


CoachRepositoryDep = Annotated[CoachRepository, Depends(get_member_repository)]


def get_member_service(repository: CoachRepositoryDep, security: SecurityDep) -> CoachService:
    return CoachService(repository, security)


CoachServiceDep = Annotated[CoachService, Depends(get_member_service)]
