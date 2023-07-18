from datetime import datetime
from pydantic import BaseModel


class Admin(BaseModel):
    admin_id: str

    class Config:
        from_attributes = True


class AdminPost(BaseModel):
    name: str
    password: str


class AdminResponse(Admin):
    name: str
    password: str
    created_at: datetime


class AdminUpdate(BaseModel):
    name: str
    password: str


class AdminDelete(Admin):
    pass
