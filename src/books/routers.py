from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer
from src.books.schemas import BookBaseSchema, BookCreationSchema, BookDetailSchema
from src.books.service import BookService
from src.db.main import get_db_session


book_router = APIRouter()


@book_router.get(
    '/',
    response_model=list[BookBaseSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_books(
    session: AsyncSession = Depends(get_db_session)
):
    books = await BookService(session).get_all_books()
    return books


@book_router.get(
    '/{book_uid}',
    response_model=BookDetailSchema,
    status_code=status.HTTP_200_OK
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_db_session)
):
    book = await BookService(session).get_book_by_uid(book_uid)

    if book is not None:
        return book
    else:
        raise HTTPException(
            detail='Book Not Found.',
            status_code=status.HTTP_404_NOT_FOUND
        )


@book_router.post(
    '/',
    response_model=BookBaseSchema,
    status_code=status.HTTP_201_CREATED
)
async def book_create(
    book_data: BookCreationSchema,
    session: AsyncSession = Depends(get_db_session),
    token_detail: dict = Depends(AccessTokenBearer())
):
    user_uid = token_detail['user']['user_uid']
    new_book = await BookService(session).create_book(user_uid, book_data)
    return new_book
