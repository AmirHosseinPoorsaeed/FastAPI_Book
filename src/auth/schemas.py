import uuid
from pydantic import BaseModel, Field


class UserCreationSchema(BaseModel):
    username: str = Field(max_length=40)
    email: str = Field(max_length=50)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=40)
    password: str = Field(min_length=8, exclude=True)


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserBaseSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserDetailSchema(UserBaseSchema):
    uid: uuid.UUID


class UserChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
    confirm_new_password: str = Field(min_length=8)
