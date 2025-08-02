import uuid
from src.db.main import Base
from sqlalchemy import (
    Column, String, DateTime, Date, Integer, ForeignKey
)
from sqlalchemy.sql import func
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    uid = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    datetime_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    datetime_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    books = relationship(
        'Book', 
        back_populates='user', 
        lazy='selectin'
    )

    def __repr__(self):
        return f'<{type(self).__name__} {self.username}>'
    

class Book(Base):
    __tablename__ = 'books'

    uid = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )
    title = Column(String, nullable=False, unique=True)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    page_count = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    datetime_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    datetime_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    user_uid = Column(
        pg.UUID(as_uuid=True), 
        ForeignKey('users.uid'),
        nullable=False
    )

    user = relationship(
        'User', 
        back_populates='books', 
        lazy='selectin'
    )

    def __repr__(self):
        return f'<{type(self).__name__} {self.title}>'
