from typing import List, Any

from pydantic import BaseModel

from rest.user.model import UserRes


class ByIds(BaseModel):
    """
    根据 id 列表操作
    """

    ids: List[int]


class PageInfo(BaseModel):
    """
    分页请求参数
    """

    page: int
    page_size: int

    def safety(self):
        """数安全处理"""
        if self.page <= 1:
            self.page = 0

        if self.page_size <= 0:
            self.page_size = 10

        if self.page_size > 50:
            self.page_size = 50

    def offset(self) -> int:
        """分页 offset 计算"""

        if self.page > 0:
            return (self.page - 1) * self.page_size

        return self.page


class ListMetaRes(BaseModel):
    """
    分页响应
    """

    page: int
    page_size: int
    data: List[Any]
    total: int


class Message(BaseModel):
    message: str


class LoginReq(BaseModel):
    """登录请求参数"""

    username: str
    password: str


class LoginRes(BaseModel):
    """登录响应参数"""

    access_token: str
    expire: int
    refresh_token: str
    refresh_expire: int
    user_info: UserRes
