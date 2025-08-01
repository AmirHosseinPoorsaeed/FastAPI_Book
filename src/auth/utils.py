import uuid
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.config import Config
from src.db.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: User, password: str):
    if not verify_password(password, user.password_hash):
        return False
    return True


def create_access_token(
    user_data: dict,
    expires_delta: timedelta | None = None,
    refresh: bool = False
):
    to_encode = {}

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({
        'user': user_data,
        'exp': expire,
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    })

    encoded_jwt = jwt.encode(
        to_encode, Config.JWT_SECRET, Config.JWT_ALGORITHM
    )
    return encoded_jwt
