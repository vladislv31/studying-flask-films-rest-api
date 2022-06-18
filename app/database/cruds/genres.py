"""Module implements Genres CRUD class."""

from app import db

from app.database.cruds.base import BaseCRUD
from app.database.models import Genre
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema, GenreSchema

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError


class GenresCRUD(BaseCRUD[Genre, GenreCreateSchema, GenreUpdateSchema, GenreSchema]):
    """Genres CRUD class."""

    def __init__(self):
        super().__init__(Genre, GenreSchema, db.session)

    def create(self, data: GenreCreateSchema) -> GenreSchema:
        """Creates genre with checking for unique genre name and returns it."""
        if Genre.query.filter_by(name=data.name).first():
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))

        genre = Genre(name=data.name)

        db.session.add(genre)
        db.session.commit()

        return GenreSchema.from_orm(genre)

    def update(self, id_: int, data: GenreUpdateSchema) -> GenreSchema:
        """Updates genre with checking for unique genre name and returns it."""
        genre = Genre.query.filter_by(id=id_).first()

        if not genre:
            raise EntityIdError("Genre with such id not found: {}.".format(id_))

        if Genre.query.filter_by(name=data.name).first() and genre.name != data.name:
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))

        genre.name = data.name

        db.session.add(genre)
        db.session.commit()

        return GenreSchema.from_orm(genre)
