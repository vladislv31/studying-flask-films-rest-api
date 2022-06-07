from functools import wraps

from flask_login import current_user

from app.database.cruds.directors import DirectorsCRUD
from app.schemas.directors import DirectorSchema, DirectorCreateSchema, DirectorUpdateSchema

from app.utils.exceptions import UnauthorizedError


def check_access(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper


def get_all_directors() -> list[DirectorSchema]:
    directors = DirectorsCRUD().read()
    return [DirectorSchema.from_orm(director) for director in directors]


def get_one_director(director_id: int) -> DirectorSchema:
    director = DirectorsCRUD().read_one(director_id)
    return DirectorSchema.from_orm(director)


@check_access
def create_director(data: DirectorCreateSchema) -> DirectorSchema:
    director = DirectorsCRUD().create(data)
    return DirectorSchema.from_orm(director)


@check_access
def update_director(director_id: int, data: DirectorUpdateSchema) -> DirectorSchema:
    director = DirectorsCRUD().update(director_id, data)
    return DirectorSchema.from_orm(director)


@check_access
def delete_director(director_id: int):
    DirectorsCRUD().delete(director_id)
