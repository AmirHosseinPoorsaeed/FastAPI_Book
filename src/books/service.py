from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, desc

from src.db.models import Book


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        books = await self.session.execute(
            select(Book).order_by(desc(Book.datetime_created))
        )
        return books.scalars().all()
