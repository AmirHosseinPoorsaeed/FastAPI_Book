from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.auth.utils import authenticate_user
from src.db.main import get_db_session
from src.auth.schemas import UserCreationSchema, UserLoginSchema


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


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login_user(
    login_data: UserLoginSchema,
    session: AsyncSession = Depends(get_db_session)
):
    email = login_data.email
    password = login_data.password

    user = await UserService(session).get_user_by_email(email)

    if user is not None:
        if authenticate_user(user, password):
            return {'Authenticate successfully.'}
        
        raise HTTPException(
            detail='Invalid Password or Email',
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    raise HTTPException(
        detail='User with this email does not exists.',
        status_code=status.HTTP_403_FORBIDDEN
    )
    
