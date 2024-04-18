from pydantic import BaseModel


class _Message(BaseModel):
    message: str


class Message(BaseModel):
    message: str
