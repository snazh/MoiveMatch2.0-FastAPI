from collections import defaultdict
from typing import Dict, List
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session
from src.movie_algo.models import user_movie, comment, movie
from src.movie_algo.schemas import Comment
from src.movie_algo.service import search_algo
from src.movie_api.router import get_movie_brief_data
from src.movie_algo.service import MovieAlgoService
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/movie-algo",
    tags=["Movie Algo"]
)


@router.post("/add-to-favorite/{movie_id}", status_code=status.HTTP_201_CREATED)
async def add_to_favorite(movie_id: int,
                          session: AsyncSession = Depends(get_async_session),
                          curr_user=Depends(get_current_user_or_redirect),
                          movie_data=Depends(get_movie_brief_data)):
    try:
        if isinstance(curr_user, RedirectResponse):  # delete it if you need clear back-end
            return curr_user

        await MovieAlgoService(curr_user.id).add_movie(movie_id, movie_data['data'], session)

        return {
            "status": "success",
            "data": None,
            "details": "The movie has been successfully added"
        }
    except IntegrityError:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Movie with ID {movie_id} is already added for user {curr_user.id}"
        })
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
        if isinstance(curr_user, RedirectResponse):  # delete it if you need clear back-end
            return curr_user
        is_fav = await MovieAlgoService(curr_user.id).is_favorite(movie_id, session)
        if is_fav:

            await MovieAlgoService(curr_user.id).delete_movie(movie_id, session)
            return {
                "status": "success",
                "data": None,
                "details": "The movie has been successfully deleted"
            }
        else:
            raise HTTPException(status_code=500)
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

        button_status = await MovieAlgoService(curr_user.id).is_favorite(movie_id, session)

        return {
            "button_status": button_status
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "button_status": None,
        })


@router.get("/get-movie-list", status_code=status.HTTP_200_OK)
async def get_movie_list(session: AsyncSession = Depends(get_async_session),
                         curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        movies = await MovieAlgoService(curr_user.id).get_movie_list(session)
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
