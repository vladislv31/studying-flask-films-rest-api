from app import db

from app.database.cruds.base import BaseCRUD
from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema, DirectorSchema
from app.database.models import Director


class DirectorsCRUD(BaseCRUD[Director, DirectorCreateSchema, DirectorUpdateSchema, DirectorSchema]):

    def __init__(self):
        super().__init__(Director, DirectorSchema, db.session)
