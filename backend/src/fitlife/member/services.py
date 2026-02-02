from fastapi import BackgroundTasks

from fitlife.config import settings
from fitlife.member.repositories import MemberRepository
from fitlife.security import SecurityDep
from fitlife.services import UserService


class MemberService(UserService):
    def __init__(self, repository: MemberRepository, background_tasks: BackgroundTasks, security: SecurityDep):
        super().__init__(
            repository=repository,
            background_tasks=background_tasks,
            security=security,
            cache_namespace=settings.cache.namespace.member,
        )
