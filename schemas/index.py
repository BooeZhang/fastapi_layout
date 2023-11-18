from pydantic import BaseModel

from schemas.base import Base


class _Message(BaseModel):
    message: str


class Message(BaseModel):
    message: str



