from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

PHONE_PATTERN = r'^+380(50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$'


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
