from sqlalchemy.orm import Mapped

from fitlife.models import Base
from fitlife.trainer.schemas import Specialities


class TrainerModel(Base):
    __tablename__ = 'trainers'

    name: Mapped[str]
    speciality: Mapped[Specialities]
