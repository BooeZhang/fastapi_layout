from typing import AsyncGenerator

from redis.asyncio import Redis
from loguru import logger as log
from starlette.requests import Request


async def get_redis_client(request: Request) -> AsyncGenerator[Redis, None]:
    """
    Returns connection client.
    I use pools, so you don't acquire connection till the end of the service.

    :param request: current request.
    :returns:  redis connection pool.
    """

    async with Redis(connection_pool=request.app.state.redis_pool) as client:
        try:
            yield client
        except Exception as e:
            log.error(f"[REDIS]: redis client error: {e}")
            raise
        finally:
            await client.close()
    return
