from functools import wraps

from flask_login import current_user

from app.schemas.films import FilmsQuerySchema, FilmSchema, FilmWithUserIdBodySchema, FilmBodySchema
from app.database.cruds.films import FilmsCRUD
from app.database.cruds.base import AbstractCRUD

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        film_id = args[1]
        film = FilmsCRUD().read_one(film_id)

        if film.user.id != current_user.id and not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_films(crud: AbstractCRUD, data: FilmsQuerySchema) -> list[FilmSchema]:
    films = crud.read(data)
    return films


def get_one_film(crud: AbstractCRUD, film_id: int) -> FilmSchema:
    film = crud.read_one(film_id)
    return film


def create_film(crud: AbstractCRUD, data: FilmWithUserIdBodySchema) -> FilmSchema:
    film = crud.create(data)
    return film


@check_access
def update_film(crud: AbstractCRUD, film_id: int, data: FilmBodySchema) -> FilmSchema:
    film = crud.update(film_id, data)
    return film


@check_access
def delete_film(crud: AbstractCRUD, film_id: int):
    crud.delete(film_id)

