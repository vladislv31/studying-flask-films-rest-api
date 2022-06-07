from app import db

from app.database.cruds.base import BaseCRUD
from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema
from app.models import Director


class DirectorsCRUD(BaseCRUD[Director, DirectorCreateSchema, DirectorUpdateSchema]):

    def __init__(self):
        super().__init__(Director)

    def create(self, data: DirectorCreateSchema) -> Director:
        return super().create(db.session, data)

    def read(self) -> list[Director]:
        return super().read(db.session)

    def read_one(self, id_: int) -> Director:
        return super().read_one(db.session, id_)

    def update(self, id_: int, data: DirectorUpdateSchema) -> Director:
        return super().update(db.session, id_, data)

    def delete(self, id_: int) -> None:
        super().delete(db.session, id_)

