from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from src.friend_system.models import friendship
from src.auth.models import user


class FriendService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def add_friend(self, friend_id: int, session: AsyncSession) -> None:
        stmt = insert(friendship).values(user_id=self.user_id, friend_id=friend_id)
        await session.execute(stmt)
        await session.commit()

    async def delete_friend(self, friend_id: int, session: AsyncSession) -> None:
        stmt = delete(friendship).where(friendship.c.user_id == self.user_id, friendship.c.friend_id == friend_id)
        await session.execute(stmt)
        await session.commit()

    # async def get_friends_list(self, session: AsyncSession) -> List[Dict]:
    #     fetch_ids_query = select(friendship).where(friendship.c.user_id == self.user_id)
    #     result = await session.execute(fetch_ids_query)
    #     friends = [{"id": row[1]} for row in result.fetchall()]
    #     return friends
    async def get_friends_list(self, session: AsyncSession):

        fetch_friends_query = (
            select(user.c.id, user.c.username, user.c.email)
            .join(friendship, friendship.c.friend_id == user.c.id)
            .where(friendship.c.user_id == self.user_id)
        )

        # Execute the query
        result = await session.execute(fetch_friends_query)

        # Extract friend data from the result
        friends = [
            {
                "user_id": row.user_id,
                "username": row.username,
                "email": row.email
            }
            for row in result.fetchall()
        ]

        return friends

    async def is_friend(self, friend_id: int, session: AsyncSession) -> bool:
        fetch_friend_query = select(friendship).where(friendship.c.user_id == self.user_id,
                                                      friendship.c.friend_id == friend_id)
        result = await session.execute(fetch_friend_query)
        friend = result.scalar()
        return friend is not None
