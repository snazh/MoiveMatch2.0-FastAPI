from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session
from src.friend_system.models import friendship

router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)


@router.post("/add-friend", status_code=status.HTTP_201_CREATED)
async def add_friend(friend_id: int, session: AsyncSession = Depends(get_async_session),
                     curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        stmt = insert(friendship).values(user_id=curr_user.id, friend_id=friend_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": "The friend has been successfully added"}
    except Exception as e:

        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while adding the friend{e}"
        })


@router.delete("/delete-friend/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_friend(friend_id: int, session: AsyncSession = Depends(get_async_session),
                        curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        stmt = delete(friendship).where(friendship.c.user_id == curr_user.id, friendship.c.friend_id == friend_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": "The friend has been successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while deleting the friend: {str(e)}"
        })


@router.get("/get-friends-list/{user_id}", status_code=status.HTTP_200_OK)
async def get_friends_list(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        fetch_ids = select(friendship).where(friendship.c.user_id == user_id)
        result1 = await session.execute(fetch_ids)

        friends = [{"id": row[1]} for row in result1.all()]

        return {
            "status": "success",
            "data": friends,
            "details": f"Friends of {user_id} were fetched successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while finding friends {e}"
        })



