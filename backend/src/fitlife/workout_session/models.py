from datetime import date, time

from sqlalchemy.orm import Mapped

from fitlife.models import Base


class WorkoutSessionModel(Base):
    __tablename__ = 'workout_sessions'

    date: Mapped[date]
    time: Mapped[time]
