"""Database models for the book API.

This module defines the SQLAlchemy models used in the application.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from db_config import Base


class Book(Base):
    """Book model representing a book in the database.

    Attributes:
        title: The book' title.
        author: The book' author.
        year: The publication year.
    """

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    year: Mapped[int] = mapped_column(nullable=True, index=True)
