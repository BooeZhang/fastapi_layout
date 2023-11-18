from typing import Any
from pydantic import BaseModel


class Base(BaseModel):
    code: int = 200
    msg: str = "ok"
