from functools import wraps

from flask_login import current_user

from app.schemas.films import FilmsQuerySchema, FilmSchema, FilmWithUserIdBodySchema, FilmBodySchema
from app.database.cruds.films import FilmsCRUD

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        film_id = args[0]
        film = FilmsCRUD().read_one(film_id)

        if film.user_id != current_user.id and not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_films(data: FilmsQuerySchema):
    films = FilmsCRUD().read(data)

    return {
        "count": len(films),
        "result": [
            FilmSchema.from_orm(film).dict() for film in films
        ]
    }


def get_one_film(film_id: int):
    film = FilmsCRUD().read_one(film_id)

    return FilmSchema.from_orm(film).dict()


def create_film(data: FilmWithUserIdBodySchema):
    film = FilmsCRUD().create(data)

    return FilmSchema.from_orm(film).dict()


@check_access
def update_film(film_id: int, data: FilmBodySchema):
    film = FilmsCRUD().update(film_id, data)

    return FilmSchema.from_orm(film).dict()


@check_access
def delete_film(film_id: int):
    FilmsCRUD().delete(film_id)
