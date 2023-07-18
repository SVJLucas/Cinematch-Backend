from datetime import datetime
from pydantic import BaseModel


class Rating(BaseModel):
    rating_id: str

    class Config:
        from_attributes = True


class RatingPost(BaseModel):
    user_id: str
    movie_id: str
    score: float


class RatingResponse(Rating):
    user_id: str
    movie_id: str
    score: float
    created_at: datetime


class RatingUpdate(BaseModel):
    user_id: str
    movie_id: str
    score: float


class RatingDelete(Rating):
    pass
