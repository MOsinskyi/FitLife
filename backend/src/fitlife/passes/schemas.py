from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PassFeatureBase(BaseModel):
    name: str

class PassFeatureCreate(PassFeatureBase):
    pass

class PassFeatureSchema(PassFeatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID

class PassBase(BaseModel):
    title: str
    price: int
    duration_days: int
    is_active: bool = True

class PassCreate(PassBase):
    feature_ids: list[UUID] = []

class PassUpdate(BaseModel):
    title: str | None = None
    price: int | None = None
    duration_days: int | None = None
    feature_ids: list[UUID] | None = None
    is_active: bool | None = None

class PassSchema(PassBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    features: list[PassFeatureSchema] = []
    created_at: datetime
    updated_at: datetime
