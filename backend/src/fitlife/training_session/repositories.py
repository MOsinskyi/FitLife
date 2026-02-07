from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.repositories import BaseRepository, BaseSqlAlchemyRepository

from .models import TrainingSessionModel


class TrainingSessionRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_by_title(self, title: str) -> TrainingSessionModel:
        pass


class TrainingSessionSqlAlchemyRepository(TrainingSessionRepository, BaseSqlAlchemyRepository):
    def __init__(self, model: type[TrainingSessionModel], session: AsyncSession):
        super().__init__(
            model=model,
            session=session,
        )
        self.model = model

    async def get_by_title(self, title: str) -> TrainingSessionModel:
        query = select(self.model).where(self.model.title == title)
        response = await self.session.execute(query)
        return response.scalars().first()
