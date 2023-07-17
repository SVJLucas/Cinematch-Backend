from datetime import datetime
from pydantic import BaseModel


class Genre(BaseModel):
    genre_id: str

    class Config:
        from_attributes = True


class GenrePost(BaseModel):
    name: str


class GenreResponse(Genre):
    name: str
    created_at: datetime


class GenreUpdate(BaseModel):
    name: str


class GenreDelete(Genre):
    pass
