from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, desc

from src.books.schemas import BookCreationSchema
from src.db.models import Book


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        books = await self.session.execute(
            select(Book).order_by(desc(Book.datetime_created))
        )
        return books.scalars().all()

    async def get_book_by_uid(
        self, 
        book_uid: str
    ):
        book = await self.session.execute(
            select(Book).where(Book.uid == book_uid)
        )
        
        return book.scalars().first()
    
    async def create_book(
        self, 
        user_uid: str, 
        book_data: BookCreationSchema
    ):
        new_book = Book(
            **book_data.model_dump(),
            user_uid=user_uid
        )
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book
