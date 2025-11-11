from datetime import timedelta
from typing import Any

from fastapi import HTTPException, status

from fitlife.config import settings
from fitlife.security import create_access_token, verify_password
from fitlife.user.repositories import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> dict[Any, Any]:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_result: dict[Any, Any] = user
        return user_result

    def create_token(self, user: dict[str, Any]) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token: str = create_access_token(
            data={"sub": user["email"], "role": user["role"]}, expires_delta=access_token_expires
        )
        return token
