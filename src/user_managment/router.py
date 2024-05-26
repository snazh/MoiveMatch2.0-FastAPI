from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from src.user_managment.service import UserService
from src.movie_algo.service import GetUserMovie
from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session

router = APIRouter(
    prefix="/users-management",
    tags=["Users Management"]
)


@router.get("/get-current-user", status_code=status.HTTP_200_OK)
async def get_current_user(curr_user=Depends(get_current_user_or_redirect)):

    return {"isAuthenticated": True}


@router.get("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user_movies = await GetUserMovie(user_id).get_movies(session)
        user_data = await UserService(user_id).get_specific_user(session)

        return {
            "status": "success",
            "data": {
                "movies": user_movies,
                "user": user_data
            },
            "details": "User profile has been fetched"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while fetching user profile"
        })


@router.get("/my_profile", status_code=status.HTTP_200_OK)
async def get_my_profile(session: AsyncSession = Depends(get_async_session),
                         curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        user_movies = await GetUserMovie(curr_user.id).get_movies(session)
        user_data = await UserService(curr_user.id).get_specific_user(session)

        return {
            "status": "success",
            "data": {
                "movies": user_movies,
                "user": user_data
            },
            "details": "Your profile has been fetched"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while fetching your profile"
        })
