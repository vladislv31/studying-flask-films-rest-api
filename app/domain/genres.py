from functools import wraps

from flask_login import current_user

from app.database.cruds.genres import GenresCRUD
from app.database.schemas.genres import GenreSchema, GenreCreateSchema, GenreUpdateSchema

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_genres():
    genres = GenresCRUD().read()

    return {
        "count": len(genres),
        "result": [
            GenreSchema.from_orm(genre).dict() for genre in genres
        ]
    }


def get_one_genre(genre_id: int):
    genre = GenresCRUD().read_one(genre_id)

    return GenreSchema.from_orm(genre).dict()


@check_access
def create_genre(data: GenreCreateSchema):
    genre = GenresCRUD().create(data)

    return GenreSchema.from_orm(genre).dict()


@check_access
def update_genre(genre_id: int, data: GenreUpdateSchema):
    genre = GenresCRUD().update(genre_id, data)

    return GenreSchema.from_orm(genre).dict()


@check_access
def delete_genre(genre_id: int):
    GenresCRUD().delete(genre_id)

