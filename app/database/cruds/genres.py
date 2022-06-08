from app import db

from app.database.cruds.base import BaseCRUD
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema
from app.models import Genre

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError


class GenresCRUD(BaseCRUD[Genre, GenreCreateSchema, GenreUpdateSchema]):

    def __init__(self):
        super().__init__(Genre, db.session)

    def create(self, data: GenreCreateSchema) -> Genre:
        if Genre.query.filter_by(name=data.name).first():
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))
        
        genre = Genre(name=data.name)

        db.session.add(genre)
        db.session.commit()

        return genre

    def update(self, id_: int, data: GenreUpdateSchema) -> Genre:
        genre = Genre.query.filter_by(id=id_).first()

        if not genre:
            raise EntityIdError("Genre with such id not found: {}.".format(id_))

        if Genre.query.filter_by(name=data.name).first() and genre.name != data.name:
            raise GenreAlreadyExistsError("Genre with such name already exists: {}.".format(data.name))

        genre.name = data.name

        db.session.add(genre)
        db.session.commit()

        return genre
