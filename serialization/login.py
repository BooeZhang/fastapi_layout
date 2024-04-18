from pydantic import BaseModel

from models.user import UserRes


class LoginReq(BaseModel):
    """
    登录请求参数
    """

    username: str
    password: str


class LoginRes(BaseModel):
    """
    登录响应参数
    """

    access_token: str
    expire: int
    refresh_token: str
    refresh_expire: int
    user_info: UserRes
