from typing import Generic, TypeVar, Type, Any, Optional

from sqlalchemy.orm import Session, declarative_base
from pydantic import BaseModel

from app.utils.exceptions import EntityIdError


Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, data: CreateSchemaType) -> ModelType:
        obj = self.model(**(data.dict()))

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def read(self, *args, **kwargs) -> list[ModelType]:
        query = self.db.query(self.model)

        page = kwargs.get("page", None)
        page_limit = kwargs.get("page_limit", 10)
        order = kwargs.get("order", 1)

        if order == 1:
            query = query.order_by(self.model.id.asc())
        elif order == -1:
            query = query.order_by(self.model.id.desc())

        if page and page > 0:
            objs = query.paginate(page, page_limit, False).items
        else:
            objs = query.all()

        return objs

    def read_one(self, id_: int) -> ModelType:
        obj = self.db.query(self.model).filter(self.model.id == id_).first()

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        return obj

    def update(self, id_: int, data: UpdateSchemaType) -> ModelType:
        obj = self.db.query(self.model).get(id_)

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        for key, value in vars(data).items():
            setattr(obj, key, value) if value else None

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(self, id_: int) -> None:
        obj = self.db.query(self.model).filter_by(id=id_).first()
        
        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        self.db.delete(obj)
        self.db.commit()
