from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SpecializationBase(BaseModel):
    name: str
    emoji: str = "⚡"


class SpecializationResponse(SpecializationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
