import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from settings import settings


class Redisx:
    """
    redis
    """

    def __init__(self):
        self.redis_pool: ConnectionPool | None = None

    async def close_connection(self) -> None:
        if self.redis_pool:
            await self.redis_pool.aclose()
            self.redis_pool = None

    def open_connection(self) -> None:
        self.redis_pool = redis.ConnectionPool.from_url(str(settings.redis_url))

    def attach_to_app(self) -> ConnectionPool:
        self.open_connection()
        return self.redis_pool


redis_pool = Redisx()
