from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings


def init_mysql(app: FastAPI) -> None:
    """
    初始化 mysql 数据库
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def shutdown_mysql(app: FastAPI) -> None:  # pragma: no cover
    """
    关闭 mysql 连接
    :param app:
    :return:
    """
    await app.state.db_engine.dispose()
