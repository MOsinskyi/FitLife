from sqlalchemy.orm import relationship

from fitlife.models import UserBase


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    sessions = relationship(
        'TrainingSessionModel',
        back_populates='coach',
    )
