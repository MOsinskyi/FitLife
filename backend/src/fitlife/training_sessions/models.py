import enum
from datetime import datetime, time
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from fitlife.coaches.models import CoachModel
from fitlife.members.models import MemberModel
from fitlife.models import Base


class SessionStatus(enum.StrEnum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class TrainingSession(Base):
    __tablename__ = 'training_sessions'

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    status: Mapped[SessionStatus] = mapped_column(SQLEnum(SessionStatus), default=SessionStatus.SCHEDULED)
    max_participants: Mapped[int] = mapped_column(Integer, default=10)

    coach_id: Mapped[UUID | None] = mapped_column(ForeignKey('coaches.id', ondelete='SET NULL'), nullable=True)

    coach: Mapped[Optional['CoachModel']] = relationship(back_populates='sessions')
    participants: Mapped[list['SessionParticipant']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )


class SessionParticipant(Base):
    __tablename__ = 'session_participants'

    member_id: Mapped[UUID] = mapped_column(ForeignKey('members.id', ondelete='CASCADE'), primary_key=True)
    session_id: Mapped[UUID] = mapped_column(ForeignKey('training_sessions.id', ondelete='CASCADE'), primary_key=True)

    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    member: Mapped['MemberModel'] = relationship(back_populates='participations')
    session: Mapped['TrainingSession'] = relationship(back_populates='participants')
