from passlib.context import CryptContext

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
