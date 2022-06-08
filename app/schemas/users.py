from pydantic import BaseModel

from app.schemas.roles import RoleSchema


class UserBaseSchema(BaseModel):
    id: int
    username: str


class UserSchema(UserBaseSchema):

    class Config:
        orm_mode = True


class UserWithRoleSchema(UserBaseSchema):
    role: RoleSchema

    class Config:
        orm_mode = True
