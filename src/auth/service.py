from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.schemas import UserCreationSchema
from src.auth.utils import get_password_hash
from src.db.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str):
        user = await self.session.execute(
            select(User).where(User.email == email)
        )

        return user.scalars().first()

    async def user_exists(self, email):
        user = await self.get_user_by_email(email)
        
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreationSchema):
        new_user = User(
            **user_data.model_dump(),
            password_hash=get_password_hash(user_data.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def update_user(self, user: User, user_data: dict):
        for key, value in user_data.items():
            setattr(user, key, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        return user
