"""Module implements films domain."""

from functools import wraps

from flask_login import current_user

from app.schemas.films import FilmsQuerySchema, FilmSchema, FilmWithUserIdBodySchema, FilmBodySchema
from app.database.cruds.films import FilmsCRUD
from app.database.cruds.base import AbstractCRUD

from app.utils.exceptions import UnauthorizedError


def check_access(func):
    """Checks for auth and if a user is author of film or is admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        film_id = args[1]
        film = FilmsCRUD().read_one(film_id)

        if film.user.id != current_user.id and not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_films(crud: AbstractCRUD, data: FilmsQuerySchema) -> list[FilmSchema]:
    """Returns from crud films."""
    films = crud.read(data)
    return films


def get_one_film(crud: AbstractCRUD, film_id: int) -> FilmSchema:
    """Returns from crud a specific film."""
    film = crud.read_one(film_id)
    return film


def create_film(crud: AbstractCRUD, data: FilmWithUserIdBodySchema) -> FilmSchema:
    """Creates a film by crud."""
    film = crud.create(data)
    return film


@check_access
def update_film(crud: AbstractCRUD, film_id: int, data: FilmBodySchema) -> FilmSchema:
    """Updates a film by crud."""
    film = crud.update(film_id, data)
    return film


@check_access
def delete_film(crud: AbstractCRUD, film_id: int):
    """Deletes a film by crud."""
    crud.delete(film_id)
