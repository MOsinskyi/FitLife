from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
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


async def get_all_entities(model: type[Base], session: SessionDep):
    query = select(model)
    result = await session.execute(query)
    return result.scalars().all()


async def get_entity_by_uuid(model: type[Base], uuid: UUID, session: SessionDep, error_detail: str):
    query = select(model).where(model.id == uuid)
    try:
        result = await session.execute(query)
        return result.scalars().one()
    except NoResultFound:
        raise HTTPException(detail=error_detail, status_code=status.HTTP_404_NOT_FOUND) from None


async def add_entity(new_entity: Base, session: SessionDep, error_message: str, *inspections):
    if any(inspections):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_message)
    else:
        session.add(new_entity)
        await session.commit()


async def update_entity(exiting_entity: Base, session: SessionDep):
    session.add(exiting_entity)
    await session.commit()
    await session.refresh(exiting_entity)


async def delete_entity(exiting_entity: Base, session: SessionDep):
    await session.delete(exiting_entity)
    await session.commit()


@router.post(
    '/setup-database',
    summary='Setup database',
    tags=['📊 Database'],
    description='Recreate all tables in the database',
    response_model=OkResponse,
)
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    return OkResponse(msg='Database setup successfully')
