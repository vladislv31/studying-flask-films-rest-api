"""Module implements BaseCRUD class."""

from abc import ABC

from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session, declarative_base
from pydantic import BaseModel

from app.utils.exceptions import EntityIdError

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)


class AbstractCRUD(ABC):
    """Abstract CRUD class."""

    def create(self, data: CreateSchemaType) -> ReturnSchemaType:
        pass

    def read(self, *args, **kwargs) -> list[ReturnSchemaType]:
        pass

    def read_one(self, id_: int) -> ReturnSchemaType:
        pass

    def update(self, id_: int, data: UpdateSchemaType) -> ReturnSchemaType:
        pass

    def delete(self, id_: int) -> None:
        pass


class BaseCRUD(AbstractCRUD, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]):
    """Base CRUD class."""

    def __init__(self, model: Type[ModelType], schema: Type[ReturnSchemaType], db: Session):
        self.model = model
        self.schema = schema
        self.db = db

    def create(self, data: CreateSchemaType) -> ReturnSchemaType:
        """Creates entity and returns it."""
        obj = self.model(**(data.dict()))

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return self.schema.from_orm(obj)

    def read(self, *args, **kwargs) -> list[ReturnSchemaType]:
        """Returns entities."""
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

        return [self.schema.from_orm(obj) for obj in objs]

    def read_one(self, id_: int) -> ReturnSchemaType:
        """Returns a specific entity."""
        obj = self.db.query(self.model).filter(self.model.id == id_).first()

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        return self.schema.from_orm(obj)

    def update(self, id_: int, data: UpdateSchemaType) -> ReturnSchemaType:
        """Updates entity and returns it."""
        obj = self.db.query(self.model).get(id_)

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        for key, value in vars(data).items():
            setattr(obj, key, value) if value else None

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return self.schema.from_orm(obj)

    def delete(self, id_: int) -> None:
        """Deletes entity."""
        obj = self.db.query(self.model).filter_by(id=id_).first()

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        self.db.delete(obj)
        self.db.commit()
