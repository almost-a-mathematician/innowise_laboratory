from typing import Annotated, Literal
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from api.schemas import BooksListSerializer, BookSchema, BookSerializer
from api.session_dep import SessionDep
from api.db_service import book_service, BookDoesNotExistException
import api.schemas

router = APIRouter(prefix="/books", tags=["Books"])

PaginationQuery = Annotated[api.schemas.PaginationQuery, Query()]


@router.get(path="/", name="Get all books")
async def get(session: SessionDep, pagination: PaginationQuery) -> BooksListSerializer:
    books = await book_service.get(session=session, pagination=pagination)

    return JSONResponse(
        BooksListSerializer.model_validate(
            {"items": books}, from_attributes=True
        ).model_dump()
    )


class SearchRouteQueryParams(
    api.schemas.PaginationQuery, api.schemas.SearchBookQuery
): ...


@router.get(path="/search/", name="Search books by title, author, or year")
async def search(
    session: SessionDep, query_params: Annotated[SearchRouteQueryParams, Query()]
) -> BooksListSerializer:
    books = await book_service.search(
        session=session, search_params=query_params, pagination=query_params
    )

    return JSONResponse(
        BooksListSerializer.model_validate(
            {"items": books}, from_attributes=True
        ).model_dump()
    )


@router.post(path="/", name="Add a new book")
async def create(session: SessionDep, payload: BookSchema) -> BookSerializer:
    book = await book_service.create(session, payload)

    return JSONResponse(
        BookSerializer.model_validate(book, from_attributes=True).model_dump()
    )


@router.put(
    path="/{book_id}",
    responses={404: {"description": "in case if book does not exist"}},
    name="Update book details",
)
async def update(
    session: SessionDep, book_id: int, payload: BookSchema
) -> BookSerializer:
    try:
        book = await book_service.update(session, book_id, payload)
    except BookDoesNotExistException as exc:
        raise HTTPException(status_code=404) from exc

    return JSONResponse(
        BookSerializer.model_validate(book, from_attributes=True).model_dump()
    )


@router.delete(
    path="/{book_id}",
    responses={404: {"description": "in case if book does not exist"}},
    name="Delete a book by ID",
)
async def delete(session: SessionDep, book_id: int) -> Literal[True]:
    try:
        await book_service.delete(session=session, book_id=book_id)
    except BookDoesNotExistException as exc:
        raise HTTPException(status_code=404) from exc

    return True
