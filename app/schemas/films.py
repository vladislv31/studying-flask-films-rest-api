from typing import Optional, Any
from datetime import date

from pydantic import BaseModel, validator 

from app.utils.helpers import validate_date
from app.schemas.enums import SortByEnum, SortOrderEnum
from app.schemas.users import UserSchema
from app.schemas.directors import DirectorSchema
from app.schemas.genres import GenreSchema

from app.models import Film, Director, User, Genre


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

    @validator("start_premiere_date", "end_premiere_date")
    def premiere_dates_validator(cls, value: str) -> str:
        if not validate_date(value):
            raise ValueError("date should be specified in format: YYYY-m-d.")
        return value
    
    @validator("rating")
    def rating_validator(cls, value: int) -> int:
        if not (0 <= value <= 10):
            raise ValueError("rating should be specified in range 0-10.")
        return value

    @validator("genres_ids")
    def genres_ids_validator(cls, value: str) -> str:
        try:
            genres = value.split(",")

            for genre in genres:
                int(genre)

        except ValueError:
            raise ValueError("genres_ids should be specified like string in format: 1,2,3.")

        return value

    @validator("page")
    def page_validator(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("page should be specified like positive integer.")

        return value


class FilmBodySchema(BaseModel):
    title: str
    premiere_date: Optional[str]
    director_id: Optional[int]
    description: Optional[str]
    rating: int
    poster_url: Optional[str]
    genres_ids: Optional[list[int]]

    @validator("premiere_date")
    def premiere_dates_validator(cls, value: str) -> str:
        if not validate_date(value):
            raise ValueError("date should be specified in format: YYYY-m-d.")
        return value
    
    @validator("rating")
    def rating_validator(cls, value: int) -> int:
        if not (0 <= value <= 10):
            raise ValueError("rating should be specified in range 0-10.")
        return value


class FilmWithUserIdBodySchema(FilmBodySchema):
    user_id: int


class FilmSchema(BaseModel):
    id: int
    title: str
    premiere_date: Optional[date]
    director: Optional[DirectorSchema]
    genres: Optional[list[GenreSchema]]
    description: Optional[str]
    rating: int
    poster_url: Optional[str]
    user: UserSchema

    class Config:
        orm_mode = True
    
    @validator("premiere_date")
    def premiere_date_to_string(cls, value):
        return str(value)

