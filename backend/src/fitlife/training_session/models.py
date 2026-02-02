from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from fitlife.models import Base

session_participants = Table(
    'session_participants',
    Base.metadata,
    Column('session_id', ForeignKey('training_sessions.id'), primary_key=True),
    Column('member_id', ForeignKey('members.id'), primary_key=True),
)


class TrainingSession(Base):
    __tablename__ = 'training_sessions'

    title = Column(
        String,
        nullable=False,
    )
    description = Column(
        String,
    )
    max_participants = Column(
        Integer,
        default=4,
        nullable=False,
    )
    price = Column(
        Integer,
        default=0,
        nullable=False,
    )
    duration_minutes = Column(
        Integer,
        default=60,
        nullable=False,
    )

    coach_id = Column(
        UUID,
        ForeignKey('coaches.id'),
        nullable=False,
    )
    coach = relationship(
        'CoachModel',
        back_populates='sessions',
    )

    members = relationship(
        'MemberModel',
        secondary=session_participants,
        back_populates='sessions',
    )
