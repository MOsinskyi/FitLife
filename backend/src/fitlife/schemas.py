from uuid import UUID, uuid4

from pydantic import BaseModel, Field

MOBILE_PHONE_PATTERN = r'^(?:\+38)?(?:\(044\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[0-9]{7})$'  # noqa
EMAIL_PATTERN = r'/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/'


class UserCreateSchema(BaseModel):
    first_name: str = Field(default='John')
    last_name: str = Field(default='Doe')
    phone_number: str = Field(pattern=MOBILE_PHONE_PATTERN)
    email: str | None = Field(pattern=EMAIL_PATTERN, default='john.doe@example.com')


class UserRegisterSchema(UserCreateSchema):
    password: str = Field(min_length=8, default='', description='Password must be at least 8 characters long')


class UserUpdateSchema:
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    password: str | None = None


class UserSchema(UserCreateSchema):
    id: UUID = Field(default=uuid4)
    role: str = Field(default='member', examples=['member', 'coach'])
