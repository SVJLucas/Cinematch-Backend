from datetime import datetime
from pydantic import BaseModel


class MovieGenre(BaseModel):
    movie_genre_id: str

    class Config:
        from_attributes = True


class MovieGenrePost(BaseModel):
    name: str


class MovieGenreResponse(MovieGenre):
    name: str
    created_at: datetime


class MovieGenreUpdate(MovieGenre):
    name: str


class MovieGenreDelete(MovieGenre):
    pass
