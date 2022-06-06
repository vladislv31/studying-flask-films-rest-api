from typing import Generic, TypeVar, Type, Any, Optional

from sqlalchemy.orm import Session, declarative_base
from pydantic import BaseModel

from app.utils.exceptions import EntityIdError


Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, data: CreateSchemaType) -> ModelType:
        obj = self.model(**(data.dict()))

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def read(self, db: Session, page: Optional[int] = None, page_limit: int = 10, order: int = 1) -> list[ModelType]:
        query = db.query(self.model)
        
        if order == 1:
            query = query.order_by(self.model.id.asc())
        elif order == -1:
            query = query.order_by(self.model.id.desc())

        if page and page > 0:
            objs = query.paginate(page, page_limit, False).items
        else:
            objs = query.all()

        return objs

    def read_one(self, db: Session, id_: int) -> ModelType:
        obj =  db.query(self.model).filter(self.model.id == id_).first()

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        return obj

    def update(self, db: Session, id_: int, data: UpdateSchemaType) -> ModelType:
        obj = db.query(self.model).get(id_)

        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        for key, value in vars(data).items():
            setattr(obj, key, value) if value else None

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def delete(self, db: Session, id_: int) -> None: 
        obj = db.query(self.model).filter_by(id=id_).first()
        
        if not obj:
            raise EntityIdError("{} with such id not found: {}.".format(self.model.__name__, id_))

        db.delete(obj)
        db.commit()

