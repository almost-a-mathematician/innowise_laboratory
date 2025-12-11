"""This module provides service layer for database operations on books."""

from sqlalchemy import Sequence, select
from sqlalchemy.sql.elements import OperatorExpression
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from api.models import Book
from api.schemas import BookSchema, PaginationQuery, SearchBookQuery


class BookDoesNotExistException(BaseException):
    """Exception raised when a book does not exist in the database."""


class BookService:
    """Service class for managing book database operations.

    Provides methods for CRUD operations and search functionality for books.
    """

    def build_search_query(
        self, search_text: str, column: InstrumentedAttribute[str]
    ) -> OperatorExpression:
        """Build a search query for partial text matching.

        Creates a query that matches the full search text and individual words
        against a specified column using SQL LIKE operator.

        Args:
            search_text: The text to search for.
            column: The database column to search in.

        Returns:
            A SQLAlchemy query expression for partial matching.
        """
        subquery = column.like(f"%{search_text}%")

        search_words_list = search_text.split(" ")

        for search_word in search_words_list:
            subquery |= column.like(f"%{search_word}%")

        return subquery

    async def get(
        self, session: AsyncSession, pagination: PaginationQuery
    ) -> Sequence[Book]:
        """Get a paginated list of books.

        Args:
            session: Database session.
            pagination: Pagination parameters (cursor and limit).

        Returns:
            A sequence of Book objects.
        """
        query = select(Book).order_by(Book.id).limit(pagination.limit)

        if pagination.cursor:
            query = query.where(Book.id > pagination.cursor)

        books = (await session.scalars(query)).all()

        return books

    async def search(
        self,
        session: AsyncSession,
        search_params: SearchBookQuery,
        pagination: PaginationQuery,
    ) -> Sequence[Book]:
        """Search for books by title, author, or year with pagination.

        Supports partial matching for title and author fields.

        Args:
            session: Database session.
            search_params: title, author, and/or year.
            pagination: Pagination parameters (cursor and limit).

        Returns:
            A sequence of matching Book objects.
        """
        query = select(Book)

        if search_params.title is not None:
            subquery = self.build_search_query(search_params.title, Book.title)
            query = query.where(subquery)

        if search_params.author is not None:
            subquery = self.build_search_query(search_params.author, Book.author)
            query = query.where(subquery)

        if search_params.year is not None:
            query = query.where(Book.year == search_params.year)

        query = query.limit(pagination.limit)

        if pagination.cursor:
            query = query.where(Book.id > pagination.cursor)

        books = (await session.scalars(query)).all()

        return books

    async def create(self, session: AsyncSession, payload: BookSchema) -> Book:
        """Create a new book in the database.

        Args:
            session: Database session.
            payload: Book data to create.

        Returns:
            The created Book object with assigned ID.
        """
        book = Book(title=payload.title, author=payload.author, year=payload.year)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    async def update(
        self, session: AsyncSession, book_id: int, payload: BookSchema
    ) -> Book:
        """Update an existing book's details.

        Args:
            session: Database session.
            book_id: The ID of the book to update.
            payload: Updated book data.

        Returns:
            The updated Book object.

        Raises:
            BookDoesNotExistException: If the book with given ID does not exist.
        """
        book = await session.get(Book, book_id)

        if book is None:
            raise BookDoesNotExistException

        book.title = payload.title
        book.author = payload.author
        book.year = payload.year

        await session.commit()
        await session.refresh(book)

        return book

    async def delete(self, session: AsyncSession, book_id: int) -> None:
        """Delete a book from the database.

        Args:
            session: Database session.
            book_id: The ID of the book to delete.

        Raises:
            BookDoesNotExistException: If the book with given ID does not exist.
        """
        book = await session.get(Book, book_id)

        if book is None:
            raise BookDoesNotExistException

        await session.delete(book)
        await session.commit()


book_service = BookService()
