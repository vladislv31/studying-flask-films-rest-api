from pydantic import BaseModel


class GenreSchema(BaseModel):
    id: int
    name: str
 
    class Config:
        orm_mode = True

