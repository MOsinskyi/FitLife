from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.database import get_session
from .repositories import AdminRepository

async def get_admin_repository(session: AsyncSession = Depends(get_session)):
    return AdminRepository(session)

AdminRepositoryDep = Annotated[AdminRepository, Depends(get_admin_repository)]
