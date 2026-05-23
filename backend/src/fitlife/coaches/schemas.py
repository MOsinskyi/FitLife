from typing import Annotated
from pydantic import ConfigDict, Field
from fitlife import schemas as base
from fitlife.specializations.schemas import SpecializationResponse
from uuid import UUID


class CoachCreateSchema(base.UserCreateSchema):
    specialization_ids: list[UUID] = Field(default_factory=list)
    image_url: str = Field(default="")
    experience: Annotated[int, Field(default=1, ge=1)]
    experience_label: Annotated[str, Field(default="рік")]

    model_config = ConfigDict(use_enum_values=True)


class CoachRegisterSchema(base.UserRegisterSchema, CoachCreateSchema):
    pass


class CoachUpdateSchema(base.UserUpdateSchema):
    specialization_ids: list[UUID] | None = None
    image_url: str | None = None
    experience: int | None = None
    experience_label: str | None = None


class CoachSchema(base.UserSchema):
    specializations: list[SpecializationResponse] = Field(default_factory=list)
    image_url: str
    experience: int
    experience_label: str
    role: str = "coach"

    model_config = ConfigDict(from_attributes=True)
