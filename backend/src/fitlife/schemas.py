from pydantic import BaseModel


class OkResponse(BaseModel):
    success: bool = True
    msg: str


class BadResponse(BaseModel):
    success: bool = False
    msg: str


PHONE_PATTERN = r'^(\+?380|0)(50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
