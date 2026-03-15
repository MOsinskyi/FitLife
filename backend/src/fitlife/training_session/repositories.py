import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fitlife.repositories import BaseRepository, BaseSqlAlchemyRepository

from ..member.models import MemberModel
from .models import TrainingSessionModel


class TrainingSessionRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_by_title(self, title: str) -> TrainingSessionModel:
        pass

    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID) -> TrainingSessionModel:
        pass

    @abstractmethod
    async def create(self, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def add_member_to_training_session(self, training_session_uuid, member_uuid):
        pass

    @abstractmethod
    async def is_member_in_training_session(self, training_session_uuid, member_uuid):
        pass

    @abstractmethod
    async def get_all(self):
        pass


class TrainingSessionSqlAlchemyRepository(TrainingSessionRepository, BaseSqlAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(
            model=TrainingSessionModel,
            session=session,
        )

    async def get_all(self):
        query = select(self.model).options(selectinload(self.model.members))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id_: uuid.UUID) -> TrainingSessionModel:
        query = select(self.model).where(self.model.id == id_).options(selectinload(self.model.members))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def is_member_in_training_session(self, training_session_uuid: uuid.UUID, member_uuid: uuid.UUID):
        query = select(self.model).where(
            self.model.id == training_session_uuid, self.model.members.any(MemberModel.id == member_uuid)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def add_member_to_training_session(self, training_session_uuid, member_uuid):
        training_session = await self.get_by_id(training_session_uuid)

        query = select(MemberModel).where(MemberModel.id == member_uuid)
        result = await self.session.execute(query)
        member: MemberModel = result.scalars().first()

        training_session.members.append(member)
        await self.session.commit()
        await self.session.refresh(training_session)

        return training_session

    async def get_by_title(self, title: str) -> TrainingSessionModel:
        query = select(self.model).where(self.model.title == title)
        response = await self.session.execute(query)
        return response.scalars().first()

    async def create(self, data: BaseModel) -> None:
        data_dict = data.model_dump()
        member_ids: list[UUID] = data_dict.pop('member_ids', [])

        new_session = self.model(**data_dict)

        if member_ids:
            query = select(MemberModel).where(MemberModel.id.in_(member_ids))
            result = await self.session.execute(query)
            members = result.scalars().all()
            new_session.members = list(members)

        self.session.add(new_session)
        await self.session.commit()

    async def update(self, id_: uuid.UUID, data: BaseModel) -> None:
        query = select(self.model).where(self.model.id == id_).options(selectinload(TrainingSessionModel.members))
        result = await self.session.execute(query)
        existing_training_session: TrainingSessionModel = result.scalars().first()

        data_dict = data.model_dump()
        member_ids: list[UUID] = data_dict.pop('member_ids', [])

        for k, v in data_dict.items():
            setattr(existing_training_session, k, v)

        if member_ids:
            query = select(MemberModel).where(MemberModel.id.in_(member_ids))
            result = await self.session.execute(query)
            existing_training_session.members = list(result.scalars().all())
        else:
            existing_training_session.members = []

        await self.session.commit()
        await self.session.refresh(existing_training_session)
