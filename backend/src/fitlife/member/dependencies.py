from typing import Annotated

from fastapi import Depends

from fitlife.database import SessionDep
from fitlife.member.repositories import MemberSqlAlchemyRepository
from fitlife.member.services import MemberService


async def get_member_service(session: SessionDep):
    return MemberService(MemberSqlAlchemyRepository(session))


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
