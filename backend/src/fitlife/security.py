from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from fitlife.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

REFRESH_TOKEN_EXPIRE_DAYS = 7
_REFRESH_SUBJECT = "refresh"


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode(settings.security.hash_encoding), bcrypt.gensalt()
        ).decode(settings.security.hash_encoding)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(settings.security.hash_encoding),
            hashed_password.encode(settings.security.hash_encoding),
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta
            or timedelta(minutes=settings.security.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.security.secret_key,
            algorithm=settings.security.algorithm,
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        to_encode.update({"exp": expire, "type": _REFRESH_SUBJECT})
        return jwt.encode(
            to_encode,
            settings.security.secret_key,
            algorithm=settings.security.algorithm,
        )

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm],
            )
            if payload.get("type") == _REFRESH_SUBJECT:
                return {}
            return payload
        except JWTError:
            return {}

    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm],
            )
            if payload.get("type") != _REFRESH_SUBJECT:
                return {}
            return payload
        except JWTError:
            return {}


async def get_security_service() -> Security:
    return Security()


SecurityDep = Annotated[Security, Depends(get_security_service)]
