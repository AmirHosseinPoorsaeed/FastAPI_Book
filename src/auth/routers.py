from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RefreshTokenBearer, get_current_user
from src.auth.service import UserService
from src.auth.utils import authenticate_user, create_access_token
from src.config import Config
from src.db.main import get_db_session
from src.auth.schemas import UserBaseSchema, UserCreationSchema, UserDetailSchema, UserLoginSchema
from src.db.models import User


auth_router = APIRouter()


@auth_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=UserBaseSchema
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
                ),
                refresh=False
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


@auth_router.get(
    '/refresh_token'
)
async def get_new_access_token(
    token_detail: dict = Depends(RefreshTokenBearer())
):
    expiry_timestamp = token_detail['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_detail['user']
        )
        return JSONResponse(
            content={
                'access_token': new_access_token
            }
        )

    raise HTTPException(
        detail='Invalid or Expired Token.',
        status_code=status.HTTP_403_FORBIDDEN
    )


@auth_router.get(
    '/me',
    response_model=UserDetailSchema
)
async def get_user(
    user: User = Depends(get_current_user)
):
    return user
