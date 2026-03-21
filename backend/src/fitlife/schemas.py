from uuid import UUID, uuid4

from pydantic import BaseModel, Field

MOBILE_PHONE_PATTERN = (
    r'/\+38\s\(0(39|50|63|66|67|68|70|73|90|91|92|93|94|95|96|97|98|99)\)\s[\d]{3}-[\d]{2}-[\d]{2}/g'  # noqa
)
EMAIL_PATTERN = r'/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/'


class UserCreateSchema(BaseModel):
    first_name: str = Field(default='John')
    last_name: str = Field(default='Doe')
    phone_number: str = Field(pattern=MOBILE_PHONE_PATTERN)
    email: str | None = Field(pattern=EMAIL_PATTERN, default='john.doe@example.com')


class UserRegisterSchema(UserCreateSchema):
    password: str = Field(min_length=8, default='', description='Password must be at least 8 characters long')


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    password: str | None = None


class UserSchema(UserCreateSchema):
    id: UUID = Field(default=uuid4)
    role: str = Field(default='member', examples=['member', 'coach'])
