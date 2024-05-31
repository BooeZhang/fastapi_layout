from sqlmodel import SQLModel, Field

from utils import timex


class ModelBase(SQLModel):
    """
    数据模型基础字段
    """

    id: int | None = Field(default=None, primary_key=True)
    create_time: int = Field(default=timex.get_now_timestamp())
    update_time: int = Field(default=timex.get_now_timestamp())
