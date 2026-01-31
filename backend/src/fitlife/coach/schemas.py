from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from fitlife.schemas import EMAIL_PATTERN, PHONE_PATTERN


class CoachAuthSchema(BaseModel):
    phone_number: str = Field(pattern=PHONE_PATTERN)
    email: str | None = Field(pattern=EMAIL_PATTERN)
    password: str


class CoachAddSchema(CoachAuthSchema):
    first_name: str
    last_name: str


class CoachSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    phone_number: str = Field(pattern=PHONE_PATTERN)
    email: str = Field(pattern=EMAIL_PATTERN)
