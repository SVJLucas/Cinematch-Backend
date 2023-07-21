from datetime import datetime
from pydantic import BaseModel


class Rating(BaseModel):
    rating_id: str

    class Config:
        from_attributes = True


class RatingPost(BaseModel):
    # There's no need to pass the user_id
    movie_id: str
    score: float


class RatingResponse(Rating):
    user_id: str
    movie_id: str
    score: float
    created_at: datetime


class RatingUpdate(BaseModel):
    # There's no need to pass the user_id, neither the movie_id
    score: float


class RatingDelete(Rating):
    pass
