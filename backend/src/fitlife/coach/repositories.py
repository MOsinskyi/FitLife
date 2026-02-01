from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.coach.models import CoachModel
from fitlife.repositories import UserRepository, UserSqlAlchemyRepository


class CoachRepository(UserRepository, ABC):
    pass


class CoachSqlAlchemyRepository(CoachRepository, UserSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=CoachModel, session=session)
