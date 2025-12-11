from typing import Annotated, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ConfigDict


class YearField:
    year: Annotated[int, Field(ge=1, examples=[2025])] | None = None

    @field_validator("year")
    @classmethod
    def check_not_future(cls, year_value: int | None) -> int | None:
        if year_value is not None and year_value > datetime.now().year:
            raise ValueError("Year cannot be in the future")
        return year_value


class BookSchema(BaseModel, YearField):
    title: Annotated[str, Field(min_length=1, max_length=50, examples=["Book Title"])]
    author: Annotated[str, Field(min_length=1, max_length=50, examples=["Book Author"])]


class BookSerializer(BookSchema):
    id: int


class SearchBookQuery(BaseModel, YearField):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: Annotated[str, Field(min_length=1, examples=["Book Title"])] = None
    author: Annotated[str, Field(min_length=1, examples=["Book Author"])] = None

    @model_validator(mode="after")
    def check_search_parameter(self):
        if self.author is None and self.title is None and self.year is None:
            raise ValueError("Enter at least one search parameter")

        return self


class PaginationQuery(BaseModel):
    cursor: int | None = None
    limit: Annotated[int, Field(ge=1, default=12)]


class BooksListSerializer(BaseModel):
    items: List[BookSerializer]
