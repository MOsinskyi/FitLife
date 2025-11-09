from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from fitlife.config import settings
from fitlife.database import get_db
from fitlife.user.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: dict = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_coach(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "coach":
        raise HTTPException(status_code=403, detail="Not authorized as coach")
    return current_user


async def get_current_customer(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Not authorized as customer")
    return current_user


async def get_current_manager(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Not authorized as manager")
    return current_user
