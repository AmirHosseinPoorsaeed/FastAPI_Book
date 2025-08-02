from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.books.schemas import BookBaseSchema
from src.books.service import BookService
from src.db.main import get_db_session


book_router = APIRouter()


@book_router.get(
    '/',
    response_model=list[BookBaseSchema]
)
async def get_all_books(
    session: AsyncSession = Depends(get_db_session)
):
    books = await BookService(session).get_all_books()
    return books
