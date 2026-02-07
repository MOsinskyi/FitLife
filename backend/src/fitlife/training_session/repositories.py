from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.repositories import BaseRepository, BaseSqlAlchemyRepository

from .models import TrainingSessionModel


class TrainingSessionRepository(BaseRepository, ABC):
    pass


class TrainingSessionSqlAlchemyRepository(TrainingSessionRepository, BaseSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            model=TrainingSessionModel,
            session=session,
        )
