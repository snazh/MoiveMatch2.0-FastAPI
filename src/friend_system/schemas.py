from typing import List, Optional

from pydantic import BaseModel
from src.auth.schemas import UserRead


class Friend(BaseModel):
    user_id: int
    friend_id: int




class FriendResponseModel(BaseModel):
    user: UserRead
    friend: UserRead

    class Config:
        from_attributes = True


class FriendsListResponseModel(BaseModel):
    status: str
    data: Optional[List[FriendResponseModel]]
    details: str
