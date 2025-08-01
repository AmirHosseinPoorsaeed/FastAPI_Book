from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.db.main import get_db_session
from src.auth.schemas import UserCreationSchema


auth_router = APIRouter()


@auth_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreationSchema,
    session: AsyncSession = Depends(get_db_session)
):
    email = user_data.email
    user_exists = await UserService(session).user_exists(email)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with this email already exists.'
        )

    new_user = await UserService(session).create_user(user_data)
    return new_user
