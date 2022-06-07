from app import db

from app.database.cruds.base import BaseCRUD
from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema
from app.models import Director


class DirectorsCRUD(BaseCRUD[Director, DirectorCreateSchema, DirectorUpdateSchema]):

    def __init__(self):
        super().__init__(Director, db.session)
