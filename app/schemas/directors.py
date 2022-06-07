from pydantic import BaseModel


class DirectorBaseSchema(BaseModel):
    first_name: str
    last_name: str


class DirectorSchema(DirectorBaseSchema):
    id: int

    class Config:
        orm_mode = True


class DirectorCreateSchema(DirectorBaseSchema):
    pass


class DirectorUpdateSchema(DirectorBaseSchema):
    pass
