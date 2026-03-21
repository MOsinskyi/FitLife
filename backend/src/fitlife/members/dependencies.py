from typing import Annotated

from fastapi import Depends

from fitlife.database import SessionDep

from .repositories import MemberRepository
from .services import MemberService


def get_member_repository(session: SessionDep):
    return MemberRepository(session)


MemberRepositoryDep = Annotated[MemberRepository, Depends(get_member_repository)]


def get_member_service(repository: MemberRepositoryDep):
    return MemberService(repository)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
