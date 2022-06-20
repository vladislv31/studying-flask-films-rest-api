"""Genres pydantic schemas."""

from pydantic import BaseModel


class GenreBaseSchema(BaseModel):
    name: str


class GenreSchema(GenreBaseSchema):
    id: int

    class Config:
        orm_mode = True


class GenreCreateSchema(GenreBaseSchema):
    pass


class GenreUpdateSchema(GenreBaseSchema):
    pass
