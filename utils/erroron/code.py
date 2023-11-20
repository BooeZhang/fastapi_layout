from dataclasses import dataclass

from utils.erroron.base import CustomException


@dataclass
class Test(CustomException):
    code: int = 1
    msg: str = "ssss"
