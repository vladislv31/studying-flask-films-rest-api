from app import db

from app.database.cruds.base import BaseCRUD
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema, GenreSchema
from app.database.models import Genre

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError


class GenresCRUD(BaseCRUD[Genre, GenreCreateSchema, GenreUpdateSchema, GenreSchema]):

    def __init__(self):
        super().__init__(Genre, GenreSchema, db.session)

    def create(self, data: GenreCreateSchema) -> GenreSchema:
        if Genre.query.filter_by(name=data.name).first():
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))
        
        genre = Genre(name=data.name)

        db.session.add(genre)
        db.session.commit()

        return GenreSchema.from_orm(genre)

    def update(self, id_: int, data: GenreUpdateSchema) -> GenreSchema:
        genre = Genre.query.filter_by(id=id_).first()

        if not genre:
            raise EntityIdError("Genre with such id not found: {}.".format(id_))

        if Genre.query.filter_by(name=data.name).first() and genre.name != data.name:
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))

        genre.name = data.name

        db.session.add(genre)
        db.session.commit()

        return GenreSchema.from_orm(genre)
