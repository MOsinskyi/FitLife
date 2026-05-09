from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, relationship

from fitlife.models import UserBase
from fitlife.training_sessions.models import TrainingSession


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    specializations = Column(
        ARRAY(String),
        nullable=False,
        default=list,
    )
    emoji = Column(
        String,
        nullable=False,
        default='',
    )
    experience = Column(
        Integer,
        nullable=False,
        default=0,
    )
    experience_label = Column(
        String,
        nullable=False,
        default='',
    )

    sessions: Mapped[list['TrainingSession']] = relationship(back_populates='coach')

    def __str__(self):
        return f'{self.emoji} {self.first_name} {self.last_name}'
