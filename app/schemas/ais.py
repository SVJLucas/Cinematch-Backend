from datetime import datetime
from pydantic import BaseModel


class Ai(BaseModel):
    ai_id: str

    class Config:
        from_attributes = True


class AiPost(BaseModel):
    name: str
    password: str


class AiResponse(Ai):
    name: str
    created_at: datetime


class AiUpdate(BaseModel):
    name: str
    password: str


class AiDelete(Ai):
    pass
