from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user


class UserService:

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def get_specific_user(self, session: AsyncSession):
        query = select(user).filter(user.c.id == self.user_id)
        result = await session.execute(query)
        user_data = [row for row in result.fetchall()[0]]
        return user_data




