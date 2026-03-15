from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

PHONE_PATTERN = r'^\+380\d{9}$'


class OkResponse(BaseModel):
    success: bool = True
    msg: str


class BadResponse(BaseModel):
    success: bool = False
    msg: str


class UserCredentialsSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)


class UserRegisterSchema(UserCredentialsSchema):
    password: str


class UserSchema(UserCredentialsSchema):
    id: UUID = Field(default_factory=uuid4)
    role: str


Response = OkResponse | BadResponse
