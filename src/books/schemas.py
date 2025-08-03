from datetime import datetime
import uuid
from pydantic import BaseModel

from src.auth.schemas import UserBaseSchema


class BookBaseSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    language: str

    class Config:
        orm_mode = True


class BookDetailSchema(BookBaseSchema):
    user: UserBaseSchema
    datetime_created: datetime
    datetime_updated: datetime


class BookCreationSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
