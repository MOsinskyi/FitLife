from datetime import date, time
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkoutSessionAddSchema(BaseModel):
    date: date
    time: time


class WorkoutSessionSchema(WorkoutSessionAddSchema):
    id: UUID = Field(default_factory=uuid4)
