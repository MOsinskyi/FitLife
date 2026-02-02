from sqlalchemy.orm import relationship

from fitlife.models import UserBase


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    sessions = relationship(
        'TrainingSession',
        back_populates='coach',
    )
