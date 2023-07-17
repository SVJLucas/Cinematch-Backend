from datetime import datetime
from pydantic import BaseModel


class Movie(BaseModel):
    movie_id: str

    class Config:
        from_attributes = True


class MoviePost(BaseModel):
    title: str
    synopsis: str
    year: int
    image_url: str
    rating: float


class MovieResponse(Movie):
    title: str
    synopsis: str
    year: int
    image_url: str
    rating: float
    created_at: datetime


class MovieUpdate(BaseModel):
    title: str
    synopsis: str
    year: int
    image_url: str
    rating: float


class MovieDelete(Movie):
    pass
