"""Module implements genres domain."""

from app.database.cruds.base import AbstractCRUD
from app.schemas.genres import GenreSchema, GenreCreateSchema, GenreUpdateSchema

from app.domain.utils import admin_required


def get_all_genres(crud: AbstractCRUD) -> list[GenreSchema]:
    """Returns from crud genres."""
    genres = crud.read()
    return genres


def get_one_genre(crud: AbstractCRUD, genre_id: int) -> GenreSchema:
    """Returns from crud a specific genre."""
    genre = crud.read_one(genre_id)
    return genre


@admin_required
def create_genre(crud: AbstractCRUD, data: GenreCreateSchema) -> GenreSchema:
    """Creates a genre by crud."""
    genre = crud.create(data)
    return genre


@admin_required
def update_genre(crud: AbstractCRUD, genre_id: int, data: GenreUpdateSchema) -> GenreSchema:
    """Updates a genre by crud."""
    genre = crud.update(genre_id, data)
    return genre


@admin_required
def delete_genre(crud: AbstractCRUD, genre_id: int):
    """Deletes a genre by crud."""
    crud.delete(genre_id)
