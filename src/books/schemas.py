from datetime import datetime
from pydantic import BaseModel


class BookBaseSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    language: str
