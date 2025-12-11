from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from api.models import Book
from api.schemas import BookSchema, PaginationQuery, SearchBookQuery


class BookDoesNotExistException(BaseException): ...


class BookService:

    def build_search_query(self, search_text: str, column: InstrumentedAttribute[str]):
        subquery = column.like(f"%{search_text}%")

        search_words_list = search_text.split(" ")

        for search_word in search_words_list:
            subquery |= column.like(f"%{search_word}%")

        return subquery

    async def get(
        self, session: AsyncSession, pagination: PaginationQuery
    ) -> Sequence[Book]:
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
        book = Book(title=payload.title, author=payload.author, year=payload.year)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    async def update(
        self, session: AsyncSession, book_id: int, payload: BookSchema
    ) -> Book:
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
        book = await session.get(Book, book_id)

        if book is None:
            raise BookDoesNotExistException

        await session.delete(book)
        await session.commit()


book_service = BookService()
