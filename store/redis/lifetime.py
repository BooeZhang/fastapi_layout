from fastapi import FastAPI
from redis.asyncio import ConnectionPool
from settings import settings


def init_redis(app: FastAPI) -> None:
    """
    创建 redis 连接
    :param app:
    :return:
    """
    app.state.redis_pool = ConnectionPool.from_url(
        str(settings.redis_url),
    )


async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    关闭 redis 连接
    :param app:
    :return:
    """
    await app.state.redis_pool.disconnect()
