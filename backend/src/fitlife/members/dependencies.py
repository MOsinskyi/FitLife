from typing import Annotated

from fastapi import Depends

from fitlife.database import SessionDep
from fitlife.security import SecurityDep

from .repositories import MemberRepository
from .services import MemberService


def get_member_repository(session: SessionDep) -> MemberRepository:
    return MemberRepository(session)


MemberRepositoryDep = Annotated[MemberRepository, Depends(get_member_repository)]


def get_member_service(repository: MemberRepositoryDep, security: SecurityDep) -> MemberService:
    return MemberService(repository, security)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
