from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.coach.models import CoachModel
from fitlife.repositories import BaseRepository, BaseSqlAlchemyRepository


class CoachRepository(BaseRepository, ABC):
    pass


class CoachSqlAlchemyRepository(CoachRepository, BaseSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=CoachModel, session=session)
