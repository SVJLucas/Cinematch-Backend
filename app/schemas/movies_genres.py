from datetime import datetime
from pydantic import BaseModel


class MovieGenre(BaseModel):
    movie_genre_id: str

    class Config:
        from_attributes = True


class MovieGenrePost(BaseModel):
    movie_id: str
    genre_id: str


class MovieGenreResponse(MovieGenre):
    movie_id: str
    genre_id: str
    created_at: datetime


class MovieGenreUpdate(BaseModel):
    movie_id: str
    genre_id: str


class MovieGenreDelete(MovieGenre):
    pass
