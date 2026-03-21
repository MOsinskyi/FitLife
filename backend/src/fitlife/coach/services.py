from fastapi import BackgroundTasks

from fitlife.coach.repositories import CoachRepository
from fitlife.coach.schemas import CoachRegisterSchema, CoachRegisterWithRoleSchema
from fitlife.config import settings
from fitlife.security import SecurityDep
from fitlife.services import UserService


class CoachService(UserService):
    def __init__(self, repository: CoachRepository, background_tasks: BackgroundTasks, security: SecurityDep):
        super().__init__(
            repository=repository,
            background_tasks=background_tasks,
            cache_namespace=settings.cache.namespace.coach,
            security=security,
        )

    async def create_coach(self, data: CoachRegisterSchema):
        data_dict = data.model_dump()
        data_dict['role'] = 'coach'
        data = CoachRegisterWithRoleSchema(**data_dict)

        return await super().create_user(data, self.security)
