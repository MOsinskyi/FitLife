from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(
    DeclarativeBase,
):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(
            UTC,
        ),
    )
    updated_on: Mapped[datetime] = mapped_column(
        default=datetime.now(
            UTC,
        ),
        onupdate=datetime.now(
            UTC,
        ),
    )


class UserBase(
    Base,
):
    __abstract__ = True

    first_name = Column(
        String,
        nullable=False,
    )
    last_name = Column(
        String,
        nullable=False,
    )
    phone_number = Column(
        String,
        nullable=False,
    )
    email = Column(
        String,
    )
    password = Column(
        String(
            255,
        ),
        nullable=False,
    )
    role = Column(
        String,
        nullable=False,
        default='member',
    )
