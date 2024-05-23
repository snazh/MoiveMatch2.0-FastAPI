from pydantic import BaseModel


class AddMovie(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True
