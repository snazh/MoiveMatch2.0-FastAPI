from sqlalchemy import select, distinct
from typing import Set
from sqlalchemy.ext.asyncio import AsyncSession
from src.movie_algo.models import user_movie, movie
from src.auth.models import user

class GetUserMovie:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def get_ids(self, session: AsyncSession) -> Set[int]:
        stmt = select(user_movie.c.movie_id).where(user_movie.c.user_id == self.user_id)
        result = await session.execute(stmt)
        movie_ids = {row[0] for row in result.fetchall()}
        return movie_ids

    async def get_movies(self, session: AsyncSession):
        stmt = (select(movie).
                join(user_movie, movie.c.movie_id == user_movie.c.movie_id).
                where(user_movie.c.user_id == self.user_id))
        result = await session.execute(stmt)

        return [{"id": row[0], **row[1]} for row in result.fetchall()]


async def get_users_data(session: AsyncSession):
    result = await session.execute(select(distinct(user_movie.c.user_id)))
    user_ids = result.scalars().all()

    users_data = {}
    for user_id in user_ids:
        result = await session.execute(
            select(user_movie.c.movie_id).where(user_movie.c.user_id == user_id)
        )
        movie_ids = [movie_id for (movie_id,) in result.all()]
        users_data[user_id] = movie_ids

    return users_data


def calculate_jaccard_similarity(set_target, set_other):
    intersection_size = len(set_target.intersection(set_other))
    union_size = len(set_target.union(set_other))
    return intersection_size / union_size if union_size > 0 else 0


async def find_similar_users(target_user_id: int, users_dict: dict, k: int):
    target_items = set(users_dict.get(target_user_id, []))
    similarities = [(user_id, calculate_jaccard_similarity(target_items, set(items))) for user_id, items in
                    users_dict.items() if user_id != target_user_id]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]


async def search_algo(user_id: int, session: AsyncSession):
    users_dict = await get_users_data(session)
    k_neighbors = 10
    similar_users = await find_similar_users(user_id, users_dict, k_neighbors)

    if not similar_users:
        return {
            'soulmate': 'Not Found',
            'percentage': 0,
            'recommendations': []
        }

    soulmate_user_id, soulmate_similarity = similar_users[0]
    target_user_ids = await GetUserMovie(user_id).get_ids(session)

    if len(similar_users) > 3:
        soulmates_list = similar_users[:3]
    else:
        soulmates_list = similar_users[:len(similar_users)]

    unique_soulmate_movie_ids = set()
    for soulmate_id, _ in soulmates_list:
        unique_soulmate_movie_ids.update(await GetUserMovie(soulmate_id).get_ids(session))

    select_ids_query = select(movie).where(movie.c.movie_id.in_(unique_soulmate_movie_ids),
                                           ~movie.c.movie_id.in_(target_user_ids))
    result = await session.execute(select_ids_query)
    rec_movies = [{"id": row[0], **row[1]} for row in result.fetchall()]

    select_soulmate = select(user.c.username).where(user.c.id == soulmate_user_id)
    result1 = await session.execute(select_soulmate)
    username = result1.scalar()
    return {
        'soulmate': [soulmate_user_id, username],
        'percentage': round(soulmate_similarity * 100, 3),
        'recommendations': rec_movies
    }
