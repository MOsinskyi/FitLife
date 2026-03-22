from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4(),
    )
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )


class UserBase(Base):
    __abstract__ = True

    first_name = Column(
        String,
        nullable=False,
        default='',
    )
    last_name = Column(
        String,
        nullable=False,
        default='',
    )
    phone_number = Column(
        String,
        nullable=False,
        default='',
    )
    email = Column(
        String,
        default='',
    )
    password = Column(
        String,
        nullable=False,
        default='',
    )
    role = Column(
        String,
        nullable=False,
        default='member',
    )
