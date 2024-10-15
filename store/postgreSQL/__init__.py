from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

from settings import settings
from utils import timex

from rest.user.model import User


class Database:
    def __init__(self):
        self.engine: AsyncEngine | None = None

    async def close_connection(self) -> None:
        if self.engine:
            await self.engine.dispose()
            self.engine = None

    def open_connection(self) -> None:
        self.engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)

    async def attach_to_app(self, app: FastAPI) -> AsyncEngine:
        self.open_connection()

        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        await self.init_super_user()

        return self.engine

    async def init_super_user(self):
        """
        初始化超级用户
        """
        _user = User(
            name=settings.super_user,
            password=settings.super_user_pwd,
            create_time=timex.get_now_timestamp(),
            update_time=timex.get_now_timestamp(),
        )
        _user.hash_password()

        async with AsyncSession(self.engine) as session:
            statement = select(User).where(User.name == settings.super_user)
            result = await session.exec(statement)
            if result.first() is None:
                session.add(_user)
                await session.commit()


database = Database()
