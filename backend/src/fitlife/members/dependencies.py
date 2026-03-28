from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.config import settings
from fitlife.database import SessionDep
from fitlife.security import SecurityDep

from .repositories import MemberRepository
from .services import MemberService


def get_member_repository(session: SessionDep) -> MemberRepository:
    return MemberRepository(session)


MemberRepositoryDep = Annotated[MemberRepository, Depends(get_member_repository)]


def get_member_service(
    repository: MemberRepositoryDep,
    security: SecurityDep,
    background_tasks: BackgroundTasks,
) -> MemberService:
    cache_namespace: str = settings.cache.namespace.member

    return MemberService(repository, security, background_tasks, cache_namespace)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
