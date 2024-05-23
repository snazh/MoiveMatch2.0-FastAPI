from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (MetaData, Column, Integer, String,
                        ForeignKey, Table, JSON, Boolean, TIMESTAMP)
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("avatar", String, default=None, nullable=True)
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(length=64), nullable=False
    )

    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    avatar: Mapped[str] = mapped_column(
        String, default=None, nullable=True
    )
