from functools import wraps

from flask_login import current_user

from app.database.cruds.base import AbstractCRUD
from app.schemas.genres import GenreSchema, GenreCreateSchema, GenreUpdateSchema

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_genres(crud: AbstractCRUD) -> list[GenreSchema]:
    genres = crud.read()
    return genres


def get_one_genre(crud: AbstractCRUD, genre_id: int) -> GenreSchema:
    genre = crud.read_one(genre_id)
    return genre


@check_access
def create_genre(crud: AbstractCRUD, data: GenreCreateSchema) -> GenreSchema:
    genre = crud.create(data)
    return genre


@check_access
def update_genre(crud: AbstractCRUD, genre_id: int, data: GenreUpdateSchema) -> GenreSchema:
    genre = crud.update(genre_id, data)
    return genre


@check_access
def delete_genre(crud: AbstractCRUD, genre_id: int):
    crud.delete(genre_id)
