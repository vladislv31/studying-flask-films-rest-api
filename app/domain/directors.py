"""Module implements directors domain."""

from app.database.cruds.base import AbstractCRUD
from app.schemas.directors import DirectorSchema, DirectorCreateSchema, DirectorUpdateSchema

from app.domain.utils import admin_required


def get_all_directors(crud: AbstractCRUD) -> list[DirectorSchema]:
    """Returns from crud all directors."""
    directors = crud.read()
    return directors


def get_one_director(crud: AbstractCRUD, director_id: int) -> DirectorSchema:
    """Returns from crud a specific director."""
    director = crud.read_one(director_id)
    return director


@admin_required
def create_director(crud: AbstractCRUD, data: DirectorCreateSchema) -> DirectorSchema:
    """Creates a director by crud."""
    director = crud.create(data)
    return director


@admin_required
def update_director(crud: AbstractCRUD, director_id: int, data: DirectorUpdateSchema) -> DirectorSchema:
    """Updates a director by crud."""
    director = crud.update(director_id, data)
    return director


@admin_required
def delete_director(crud: AbstractCRUD, director_id: int):
    """Deletes a director by crud."""
    crud.delete(director_id)
