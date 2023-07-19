from datetime import datetime
from typing import List
from pydantic import BaseModel


class Recommendation(BaseModel):
    recommendation_id: str

    class Config:
        from_attributes = True


class RecommendationPost(BaseModel):
    user_id: str
    movie_id: str


class RecommendationResponse(Recommendation):
    user_id: str
    movie_id: str
    created_at: datetime


class RecommendationUpdate(BaseModel):
    user_id: str
    movie_id: str


class RecommendationDelete(Recommendation):
    pass


class RecommendationByGenre(BaseModel):
    genres: List[str]
