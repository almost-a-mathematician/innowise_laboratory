from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List
from datetime import datetime


class BookSchema(BaseModel):
    title: str
    author: str
    year: Annotated[int, Field(ge=1)] | None = None

    @field_validator('year')
    @classmethod
    def check_not_future(cls, year_value: int | None) -> int | None:
        if year_value is not None and year_value > datetime.now().year:
            raise ValueError(f'Year cannot be in the future')
        return year_value
    

class UpdateBook(BaseModel):
    title: str
    author: str
    year: Annotated[int, Field(ge=1)] | None
    

class BooksListSerializer(BaseModel):
    items: List[BookSchema]
