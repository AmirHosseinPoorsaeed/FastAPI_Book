import uuid
from src.db.main import Base
from sqlalchemy import (
    Column, String, DateTime
)
from sqlalchemy.sql import func
import sqlalchemy.dialects.postgresql as pg

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

    def __repr__(self):
        return f'<{type(self).__name__} {self.username}>'
