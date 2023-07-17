from datetime import datetime
from pydantic import BaseModel


class Movie(BaseModel):
    movie_id: str

    class Config:
        from_attributes = True


class MoviePost(BaseModel):
    name: str


class MovieResponse(Movie):
    name: str
    created_at: datetime


class MovieUpdate(Movie):
    name: str


class MovieDelete(Movie):
    pass
