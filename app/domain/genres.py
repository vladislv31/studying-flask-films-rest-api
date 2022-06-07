from functools import wraps

from flask_login import current_user

from app.database.cruds.genres import GenresCRUD
from app.schemas.genres import GenreSchema, GenreCreateSchema, GenreUpdateSchema

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_genres() -> list[GenreSchema]:
    genres = GenresCRUD().read()
    return [GenreSchema.from_orm(genre) for genre in genres]


def get_one_genre(genre_id: int) -> GenreSchema:
    genre = GenresCRUD().read_one(genre_id)
    return GenreSchema.from_orm(genre)


@check_access
def create_genre(data: GenreCreateSchema) -> GenreSchema:
    genre = GenresCRUD().create(data)
    return GenreSchema.from_orm(genre)


@check_access
def update_genre(genre_id: int, data: GenreUpdateSchema) -> GenreSchema:
    genre = GenresCRUD().update(genre_id, data)
    return GenreSchema.from_orm(genre)


@check_access
def delete_genre(genre_id: int):
    GenresCRUD().delete(genre_id)
