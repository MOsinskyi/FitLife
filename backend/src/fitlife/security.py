from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


async def get_security_service() -> Security:
    return Security()


SecurityDep = Annotated[Security, Depends(get_security_service)]
