from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.member import models
from fitlife.repositories import UserRepository, UserSqlAlchemyRepository


class MemberRepository(UserRepository, ABC):
    pass


class MemberSqlAlchemyRepository(MemberRepository, UserSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=models.MemberModel, session=session)
