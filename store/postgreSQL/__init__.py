from fastapi import FastAPI
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session, select
from models import *
from models.user import User

from settings import settings
from utils import timex


class Database:
    """
    数据库
    """

    def __init__(self):
        self.engine: Engine = None

    def close_connection(self) -> None:
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def open_connection(self) -> None:
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(
            str(settings.db_url), echo=settings.db_echo, connect_args=connect_args
        )

    def attach_to_app(self, app: FastAPI):
        self.open_connection()
        app.state.db_engine = self.engine
        SQLModel.metadata.create_all(self.engine)
        self.init_super_user()

    def init_super_user(self):
        """
        初始化超级用户
        """
        _user = User(
            name=settings.super_user,
            pwd=settings.super_user_pwd,
            create_time=timex.get_now_timestamp(),
            update_time=timex.get_now_timestamp(),
        )
        _user.hash_password()
        with Session(self.engine) as sessions:
            statement = select(User).where(User.name == settings.super_user)
            result = sessions.exec(statement).first()
            if result is None:
                sessions.add(_user)
                sessions.commit()


database = Database()
