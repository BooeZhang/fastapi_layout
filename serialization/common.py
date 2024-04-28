from typing import List, Any

from pydantic import BaseModel


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
