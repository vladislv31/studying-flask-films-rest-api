from functools import wraps

from flask_login import current_user

from app.database.cruds.base import AbstractCRUD
from app.schemas.directors import DirectorSchema, DirectorCreateSchema, DirectorUpdateSchema

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_directors(crud: AbstractCRUD) -> list[DirectorSchema]:
    directors = crud.read()
    return directors


def get_one_director(crud: AbstractCRUD, director_id: int) -> DirectorSchema:
    director = crud.read_one(director_id)
    return director


@check_access
def create_director(crud: AbstractCRUD, data: DirectorCreateSchema) -> DirectorSchema:
    director = crud.create(data)
    return director


@check_access
def update_director(crud: AbstractCRUD, director_id: int, data: DirectorUpdateSchema) -> DirectorSchema:
    director = crud.update(director_id, data)
    return director


@check_access
def delete_director(crud: AbstractCRUD, director_id: int):
    crud.delete(director_id)
