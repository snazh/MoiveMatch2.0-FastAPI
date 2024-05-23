from collections import defaultdict
from typing import Dict, List
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session
from src.movie_algo.models import user_movie, comment, movie
from src.movie_algo.schemas import Comment
from src.movie_algo.service import search_algo
from src.movie_api.service import TMDB

router = APIRouter(
    prefix="/movie-algo",
    tags=["Movie Algo"]
)


@router.post("/add-to-favorite/{movie_id}", status_code=status.HTTP_201_CREATED)
async def add_to_favorite(movie_id: int,
                          session: AsyncSession = Depends(get_async_session),
                          curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        # Check if the movie_id is already in the movie table
        existing_movie = await session.execute(select(movie).where(movie.c.movie_id == movie_id))
        existing_movie = existing_movie.scalar_one_or_none()

        if existing_movie is None:
            details = await TMDB.get_movie_brief_data(movie_id)

            add_movie_stmt = insert(movie).values(movie_id=movie_id, details=details)
            await session.execute(add_movie_stmt)
            await session.commit()

        # Add the movie to the user's favorites
        add_to_favorite_stmt = insert(user_movie).values(user_id=curr_user.id, movie_id=movie_id)
        await session.execute(add_to_favorite_stmt)
        await session.commit()

        return {
            "status": "success",
            "data": None,
            "details": "The movie has been successfully added"
        }
    except Exception:

        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while adding movie"
        })


@router.delete("/remove-from-favorite/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_favorite(movie_id: int, session: AsyncSession = Depends(get_async_session),
                               curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        stmt = (delete(user_movie).
                where(user_movie.c.user_id == curr_user.id, user_movie.c.movie_id == movie_id))
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": "The movie has been successfully removed"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while removing movie"
        })


@router.get("/is_favorite", status_code=status.HTTP_200_OK)
async def is_favorite(movie_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        is_fav = await session.execute(
            select(user_movie).where(user_movie.c.user_id == curr_user.id, user_movie.c.movie_id == movie_id))
        button_status = is_fav.scalar_one_or_none() is not None

        return {
            "status": "success",
            "data": button_status,
            "details": f"is favorite success"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while searching movies"
        })


@router.get("/get-movie-list", status_code=status.HTTP_200_OK)
async def get_movie_list(session: AsyncSession = Depends(get_async_session),
                         curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        stmt = (select(movie).
                join(user_movie, movie.c.movie_id == user_movie.c.movie_id).
                where(user_movie.c.user_id == curr_user.id))

        result = await session.execute(stmt)
        movies = [row[1] for row in result.fetchall()]
        return {
            "status": "success",
            "data": movies,
            "details": f"Movie list was fetched successfully"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while searching movies"
        })


@router.get("/users_data", status_code=status.HTTP_200_OK)
async def get_user_movies_dict(session: AsyncSession = Depends(get_async_session)) -> Dict[int, List[int]]:
    # Query the user_movie table
    stmt = select(user_movie.c.user_id, user_movie.c.movie_id)
    result = await session.execute(stmt)
    rows = result.fetchall()

    # Create a default_dict to store the results
    user_movies = defaultdict(list)

    # Populate the dictionary
    for row in rows:
        user_id, movie_id = row
        user_movies[user_id].append(movie_id)

    # Convert default_dict to regular dict
    return dict(user_movies)


@router.post("/post-comment", status_code=status.HTTP_201_CREATED)
async def post_comment(request: Comment, session: AsyncSession = Depends(get_async_session),
                       curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        stmt = insert(comment).values(user_id=curr_user.id,
                                      movie_id=request.movie_id,
                                      content=request.content,
                                      rating=request.rating)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": "The comment has been successfully posted"}
    except Exception:

        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while posting comment"
        })


@router.get("/recommendations", status_code=status.HTTP_200_OK)
@cache(expire=30)
async def get_recommendations(session: AsyncSession = Depends(get_async_session),
                              curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        recommendations_data = await search_algo(curr_user.id, session)
        return {
            "status": "success",
            "data": {
                "movies": recommendations_data['recommendations'],
                "percentage": recommendations_data['percentage'],
                "soulmate": recommendations_data['soulmate']
            },
            "details": "Recommendations were found successfully "}

    except Exception as e:

        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while searching for recommendations   {e}"
        })
