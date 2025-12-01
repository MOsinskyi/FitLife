from uuid import UUID, uuid4

from pydantic import BaseModel, Field

PHONE_PATTERN = r'^(\+?380|0)(50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$'


class MemberAddSchema(BaseModel):
    name: str
    phone: str = Field(pattern=PHONE_PATTERN)


class MemberSchema(MemberAddSchema):
    id: UUID = Field(default_factory=uuid4)
