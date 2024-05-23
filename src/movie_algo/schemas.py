from pydantic import BaseModel
from src.auth.schemas import UserRead


class UserMovie(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True


class Comment(BaseModel):
    movie_id: int
    content: str
    rating: float

    class Config:
        from_attributes = True


class CommentResponseModel(BaseModel):
    user: UserRead
    movie_id: int
    content: str
    rating: float

    class Config:
        from_attributes = True
