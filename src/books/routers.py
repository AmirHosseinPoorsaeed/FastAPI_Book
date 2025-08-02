from fastapi import APIRouter


book_router = APIRouter()


@book_router.get('/')
async def get_all_books():
    return {'hello'}
