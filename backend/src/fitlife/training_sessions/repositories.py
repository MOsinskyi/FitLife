from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fitlife.training_sessions.models import SessionParticipant, TrainingSession
from fitlife.training_sessions.schemas import TrainingSessionUpdateSchema


class TrainingSessionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_training_session_by_id(self, id_: UUID) -> TrainingSession:
        stmt = (
            select(TrainingSession)
            .where(TrainingSession.id == id_)
            .options(
                selectinload(TrainingSession.coach),
                selectinload(TrainingSession.participants).joinedload(
                    SessionParticipant.member
                ),
            )
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_training_session(
        self, training_session: TrainingSession
    ) -> TrainingSession:
        self._session.add(training_session)
        await self._session.flush()
        return training_session

    async def get_training_sessions(self) -> list[TrainingSession]:
        stmt = select(TrainingSession).options(
            selectinload(TrainingSession.coach),
            selectinload(TrainingSession.participants).joinedload(
                SessionParticipant.member
            ),
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_training_session(
        self, id_: UUID, data: TrainingSessionUpdateSchema
    ) -> TrainingSession | None:
        stmt = (
            update(TrainingSession)
            .where(TrainingSession.id == id_)
            .values(
                **data.model_dump(
                    exclude_unset=True, exclude_none=True, exclude_defaults=True
                )
            )
            .returning(TrainingSession)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_training_session(self, id_: UUID) -> None:
        stmt = delete(TrainingSession).where(TrainingSession.id == id_)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
