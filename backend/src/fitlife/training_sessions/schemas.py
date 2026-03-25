from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from fitlife.training_sessions.models import SessionStatus


class UserSchema(BaseModel):
    id: Annotated[UUID, Field(default_factory=uuid4)]
    first_name: Annotated[str, Field(default='John')]
    last_name: Annotated[str, Field(default='Doe')]

    model_config = ConfigDict(from_attributes=True)


class CoachSchema(UserSchema):
    specialization: Annotated[str, Field(default='Yoga')]


class ParticipantSchema(BaseModel):
    joined_at: Annotated[datetime, Field(default=datetime.now(UTC))]
    member: UserSchema

    model_config = ConfigDict(from_attributes=True)


class TrainingSessionCreateSchema(BaseModel):
    title: Annotated[str, Field(default='Кросфіт для початківців')]
    description: Annotated[
        str, Field(default="Інтенсивне кругове тренування на всі групи м'язів. Підходить для новачків.")
    ]
    start_time: Annotated[datetime, Field(default=datetime.now(UTC))]
    end_time: Annotated[datetime, Field(default=datetime.now(UTC) + timedelta(hours=1))]
    status: Annotated[SessionStatus, Field(default=SessionStatus.SCHEDULED)]
    max_participants: Annotated[int, Field(default=12, ge=1, le=12)]
    coach: UUID
    participants: Annotated[list[UUID], Field(default=[])]


class TrainingSessionUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: SessionStatus | None = None
    max_participants: int | None = None
    coach: UUID | None = None
    participants: list[UUID] | None = []


class TrainingSessionSchema(TrainingSessionCreateSchema):
    id: Annotated[UUID, Field(default_factory=uuid4)]
    coach: CoachSchema | None
    participants: list[ParticipantSchema]

    model_config = ConfigDict(from_attributes=True)
