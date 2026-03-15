from fastapi import BackgroundTasks

from fitlife.config import settings
from fitlife.member.repositories import MemberRepository
from fitlife.schemas import UserRegisterSchema
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

    async def create_member(self, data: UserRegisterSchema):
        data_dict = data.model_dump()
        data_dict['role'] = 'member'
        data = UserRegisterSchema(**data_dict)

        return await super().create_user(data, self.security)
