from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

PHONE_PATTERN = r'^(\+?380|0)(50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$'


class OkResponse(BaseModel):
    success: bool = True
    msg: str


class BadResponse(BaseModel):
    success: bool = False
    msg: str


class UserAuthSchema(BaseModel):
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)
    password: str


class UserAddSchema(UserAuthSchema):
    first_name: str
    last_name: str
    role: str


class UserSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)


Response = OkResponse | BadResponse
