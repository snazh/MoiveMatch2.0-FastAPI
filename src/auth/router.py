from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.auth.models import user
from src.movie_algo.service import GetUserMovie
from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session
from src.friend_system.models import friendship

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/own-profile", status_code=status.HTTP_200_OK)
async def get_profile(session: AsyncSession = Depends(get_async_session),
                      curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user

        user_movies = await GetUserMovie(curr_user.id).get_movies(session)

        return {
            "status": "success",
            "data": {
                "movies": user_movies,
                "username": curr_user.username,
                "email": curr_user.email},
            "details": "The profile has been fetched"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while removing movie"
        })


@router.get("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def get_another_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user_movies = await GetUserMovie(user_id).get_movies(session)
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        user_data = result.fetchall()[0]

        return {
            "status": "success",
            "data": {
                "movies": user_movies,
                "username": user_data[2],
                "email": user_data[1]
            },
            "details": "The profile has been fetched"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while fetching profile  {e}"
        })
