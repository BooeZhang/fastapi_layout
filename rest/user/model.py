import bcrypt
from sqlmodel import SQLModel, Field

from rest.common.model import ModelBase


class UserBase(SQLModel):
    """
    user 基础字段
    """

    name: str = Field(index=True)
    password: str


class User(ModelBase, UserBase, table=True):
    """
    user 表
    """

    def hash_password(self):
        pwd = self.password.encode("utf8")
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(pwd, salt).decode("utf8")

    def check_pwd(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), self.pwd.encode("utf8"))


class UserRes(ModelBase):
    """
    user 响应
    """

    name: str
