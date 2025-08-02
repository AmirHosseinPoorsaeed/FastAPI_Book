from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.auth.utils import decode_token
from src.db.main import get_db_session


class JWTBearer(HTTPBearer):
    def init(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)

        token = credentials.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                detail='Invalid or expired token',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError(
            'Please override this method in child classes'
        )
    

class RefreshTokenBearer(JWTBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Please Provide a refresh token'
            )
        

class AccessTokenBearer(JWTBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Please Provide an access token'
            )


async def get_current_user(
    token_detail: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_db_session)
):
    user_email = token_detail['user']['email']
    user = await UserService(session).get_user_by_email(user_email)
    return user
