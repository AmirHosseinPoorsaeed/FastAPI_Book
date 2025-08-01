from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.auth.utils import authenticate_user, create_access_token
from src.config import Config
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
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                expires_delta=timedelta(
                    minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
                )
            )
            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                expires_delta=timedelta(
                    days=Config.REFRESH_TOKEN_EXPIRE_DAYS
                ),
                refresh=True
            )
            return JSONResponse(
                content={
                    'message': 'Login Successfully.',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'uid': str(user.uid)
                    }
                },
            )

        raise HTTPException(
            detail='Invalid Password or Email',
            status_code=status.HTTP_403_FORBIDDEN
        )

    raise HTTPException(
        detail='User with this email does not exists.',
        status_code=status.HTTP_403_FORBIDDEN
    )
