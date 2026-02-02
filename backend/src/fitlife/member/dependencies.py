from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.database import SessionDep
from fitlife.member.repositories import MemberSqlAlchemyRepository
from fitlife.member.services import MemberService
from fitlife.security import SecurityDep


async def get_member_service(
    session: SessionDep,
    background_tasks: BackgroundTasks,
    security: SecurityDep,
) -> MemberService:
    return MemberService(MemberSqlAlchemyRepository(session), background_tasks, security)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
