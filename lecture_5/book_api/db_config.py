"""Database configuration module for the book API.

This module sets up the SQLAlchemy async engine, session maker, and base model class.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Base(DeclarativeBase):
    """Base class for all database models.

    Provides a common id primary key field for all the models.
    """

    id: Mapped[int] = mapped_column(primary_key=True)


DB_NAME: str = "book_collection.db"

DB_URL: str = f"sqlite+aiosqlite:///{DB_NAME}"

engine = create_async_engine(DB_URL, echo=True)

# pylint: disable=<invalid-name>
Session = async_sessionmaker(engine)
