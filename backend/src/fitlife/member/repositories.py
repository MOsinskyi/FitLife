from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.member import models
from fitlife.repositories import BaseRepository, BaseSqlAlchemyRepository


class MemberRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_member_by_phone_number(self, phone_number: str) -> models.MemberModel:
        """
        Асинхронна функція, яка повертає користувача за номером телефону
        :param phone_number: Номер телефону користувача
        """
        pass


class MemberSqlAlchemyRepository(MemberRepository, BaseSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=models.MemberModel, session=session)

    async def get_member_by_phone_number(self, phone_number: str):
        query = select(models.MemberModel).where(models.MemberModel.phone == phone_number)
        response = await self.session.execute(query)
        return response.scalars().first()
