import enum
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

MOBILE_PHONE_PATTERN = r'^\+380\d{9}$'  # noqa
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class UserRoles(enum.Enum):
    MEMBER = 'member'
    COACH = 'coach'
    ADMIN = 'admin'


class UserCreateSchema(BaseModel):
    first_name: str = Field(default='John')
    last_name: str = Field(default='Doe')
    phone_number: str = Field(pattern=MOBILE_PHONE_PATTERN)
    email: str | None = Field(pattern=EMAIL_PATTERN, default='john.doe@example.com')


class UserRegisterSchema(UserCreateSchema):
    password: str = Field(min_length=8, default='', description='Password must be at least 8 characters long')


class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    phone_number: str | None = Field(default=None, pattern=MOBILE_PHONE_PATTERN)
    email: str | None = Field(default=None)


class UserSchema(UserCreateSchema):
    id: UUID = Field(examples=[uuid4().hex])
    role: Annotated[UserRoles, Field(examples=['member', 'coach'])]
    created_at: datetime = Field(examples=[datetime.now(UTC)])
    updated_at: datetime = Field(examples=[datetime.now(UTC)])
