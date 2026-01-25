from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fitlife.models import Base
from fitlife.schemas import OkResponse

router = APIRouter()

engine = create_async_engine('sqlite+aiosqlite:///fitlife.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    '/setup-database',
    summary='Setup database',
    tags=['📊 Database'],
    description='Recreate all tables in the database',
    response_model=OkResponse,
)
async def setup_database(request: Request):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    request.state.logger.info('Database setup successfully')
    return OkResponse(msg='Database setup successfully')
