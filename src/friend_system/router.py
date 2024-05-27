from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from src.friend_system.service import FriendService
from src.auth.base_config import get_current_user_or_redirect
from src.database import get_async_session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)


@router.post("/add-friend/{friend_id}", status_code=status.HTTP_201_CREATED)
async def add_friend(friend_id: int, session: AsyncSession = Depends(get_async_session),
                     curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):  # checking for current user
            return curr_user  # redirects to the /pages/login/page (frontend)

        if curr_user.id == friend_id:  # preventing adding yourself to the friend list
            raise HTTPException(status_code=500)
        await FriendService(curr_user.id).add_friend(friend_id, session)

        return {
            "status": "success",
            "data": None,
            "details": "The friend has been successfully added"}
    except IntegrityError as e:
        await session.rollback()  # Preventing adding non-existent user
        # Check for ForeignKeyViolationError
        if 'ForeignKeyViolationError' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "status": "error",
                "data": None,
                "details": "The friend with the given ID does not exist."
            })
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "status": "error",
                "data": None,
                "details": f"Database error: {e.orig}"
            })
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while adding the friend"
        })


@router.get("/is-friend/{user_id}", status_code=status.HTTP_200_OK)
async def friend_status(user_id: int, session: AsyncSession = Depends(get_async_session),
                        curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        is_friend = await FriendService(curr_user.id).is_friend(user_id, session)
        return {
            "is_friend": is_friend
        }
    except Exception:
        raise HTTPException(status_code=500, detail={"is_friend": None})


@router.delete("/delete-friend/{friend_id}", status_code=status.HTTP_200_OK)
async def delete_friend(friend_id: int, session: AsyncSession = Depends(get_async_session),
                        curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        is_friend = await FriendService(curr_user.id).is_friend(friend_id, session)
        if is_friend:

            await FriendService(curr_user.id).delete_friend(friend_id, session)
            return {
                "status": "success",
                "data": None,
                "details": "The friend has been successfully deleted"
            }
        else:
            raise HTTPException(status_code=500)

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while deleting the friend"
        })


@router.get("/get-friends-list/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_friends(session: AsyncSession = Depends(get_async_session),
                           curr_user=Depends(get_current_user_or_redirect)):
    try:
        if isinstance(curr_user, RedirectResponse):
            return curr_user
        friends = await FriendService(curr_user.id).get_friends_list(session)

        return {
            "status": "success",
            "data": {
                "friends": friends,
                "count": len(friends)
            },
            "details": f"Friends of {curr_user.id} were fetched successfully"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while fetching {curr_user.id}'s friends"
        })
