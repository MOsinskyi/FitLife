import enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Specialities(enum.Enum):
    CARDIO = 'Cardio'
    STRENGTH = 'Strength'
    CROSSFIT = 'CrossFit'
    MASSAGE_THERAPIST = 'Massage Therapist'
    SWIMMER = 'Swimmer'


class TrainersAddSchema(BaseModel):
    name: str
    speciality: Specialities


class TrainersSchema(TrainersAddSchema):
    id: UUID = Field(default_factory=uuid4)
