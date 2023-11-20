from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.model import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))
