"""Module implements Directors CRUD class."""

from app import db

from app.database.cruds.base import BaseCRUD
from app.database.models import Director
from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema, DirectorSchema


class DirectorsCRUD(BaseCRUD[Director, DirectorCreateSchema, DirectorUpdateSchema, DirectorSchema]):
    """Directors CRUD class."""

    def __init__(self):
        super().__init__(Director, DirectorSchema, db.session)
