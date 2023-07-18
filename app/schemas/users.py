from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: str

    class Config:
        from_attributes = True


class UserPost(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(User):
    name: str
    email: str
    password: str
    created_at: datetime


class UserUpdate(BaseModel):
    name: str
    email: str
    password: str


class UserDelete(User):
    pass
