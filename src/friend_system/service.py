from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models import user


class UserService:

    @staticmethod
    def get_specific_user(user_id: int, session: AsyncSession):
        query = select(user).filter(user.c.id == user_id)
        result = session.execute(query)

        return result
