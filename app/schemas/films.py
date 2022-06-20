"""Films pydantic schemas."""

from typing import Optional

import datetime

from pydantic import BaseModel, validator

from app.schemas.genres import GenreSchema
from app.schemas.directors import DirectorSchema
from app.schemas.users import UserSchema
from app.schemas.enums import SortByEnum, SortOrderEnum


class FilmSchema(BaseModel):
    id: int
    title: str
    premiere_date: datetime.date
    description: Optional[str]
    rating: int
    poster_url: str
    director: Optional[DirectorSchema]
    user: UserSchema
    genres: list[GenreSchema]

    class Config:
        orm_mode = True

    @validator("director")
    def director_none_then_unknown(cls, value):
        if not value:
            return "unknown"

        return value

    @validator("premiere_date")
    def premiere_date_to_string(cls, value):
        return str(value)


class FilmsQuerySchema(BaseModel):
    search: Optional[str]
    director_id: Optional[int]
    sort_by: Optional[SortByEnum]
    sort_order: Optional[SortOrderEnum]
    start_premiere_date: Optional[str]
    end_premiere_date: Optional[str]
    rating: Optional[int]
    genres_ids: Optional[str]
    page: Optional[int]


class FilmBodySchema(BaseModel):
    title: str
    premiere_date: str
    director_id: int
    description: Optional[str]
    rating: int
    poster_url: str
    genres_ids: Optional[list[int]]


class FilmWithUserIdBodySchema(FilmBodySchema):
    user_id: int

