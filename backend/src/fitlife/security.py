from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from fitlife.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(settings.security.hash_encoding), bcrypt.gensalt()).decode(
            settings.security.hash_encoding
        )

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(settings.security.hash_encoding), hashed_password.encode(settings.security.hash_encoding)
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=settings.security.access_token_expire_minutes)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.algorithm)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            return payload
        except JWTError:
            return {}


async def get_security_service() -> Security:
    return Security()


SecurityDep = Annotated[Security, Depends(get_security_service)]
