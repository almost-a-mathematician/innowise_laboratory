"""Pydantic schemas for the book API.

This module defines request and response schemas used for data validation and serialization.
"""

from typing import Annotated, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ConfigDict


class YearField:
    """Mixin class providing year field validation.

    Ensures that the year value is not in the future.
    """

    year: Annotated[int, Field(ge=1, examples=[2025])] | None = None

    @field_validator("year")
    @classmethod
    def check_not_future(cls, year_value: int | None) -> int | None:
        """Validate that the year is not in the future.

        Args:
            year_value: The year to validate.

        Returns:
            The validated year value.

        Raises:
            ValueError: If the year is in the future.
        """
        if year_value is not None and year_value > datetime.now().year:
            raise ValueError("Year cannot be in the future")
        return year_value


class BookSchema(BaseModel, YearField):
    """Schema for creating or updating a book.

    Attributes:
        title: The book' title (1-50 characters).
        author: The book' author (1-50 characters).
        year: Optional publication year (inherited from YearField).
    """

    title: Annotated[str, Field(min_length=1, max_length=50, examples=["Book Title"])]
    author: Annotated[str, Field(min_length=1, max_length=50, examples=["Book Author"])]


class BookSerializer(BookSchema):
    """Schema for serializing a book with its ID.

    Extends BookSchema with the database ID field.
    """

    id: int


class SearchBookQuery(BaseModel, YearField):
    """Schema for the book' search query parameters.

    At least one search parameter (title, author, or year) must be provided.
    Whitespace in strings is automatically stripped.
    """

    model_config = ConfigDict(str_strip_whitespace=True)
    title: Annotated[str, Field(min_length=1, examples=["Book Title"])] = None
    author: Annotated[str, Field(min_length=1, examples=["Book Author"])] = None

    @model_validator(mode="after")
    def check_search_parameter(self):
        """Validate that at least one search parameter is provided.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If no search parameters are provided.
        """
        if self.author is None and self.title is None and self.year is None:
            raise ValueError("Enter at least one search parameter")

        return self


class PaginationQuery(BaseModel):
    """Schema for pagination query parameters.

    Attributes:
        cursor: Optional cursor for pagination (ID of the last item from previous page).
        limit: Maximum number of items to return (default: 12, minimum: 1).
    """

    cursor: int | None = None
    limit: Annotated[int, Field(ge=1, default=12)]


class BooksListSerializer(BaseModel):
    """Schema for serializing a list of books.

    Attributes:
        items: List of serialized book objects.
    """

    items: List[BookSerializer]
