from fastapi import APIRouter, Depends
from redis.asyncio import ConnectionPool, Redis

from schemas.index import Message
from store.redis.dependency import get_redis_pool

router = APIRouter()


@router.get("/", response_model=Message)
async def index(redis_pool: ConnectionPool = Depends(get_redis_pool)) -> Message:
    msg = Message(message='hello world')
    async with Redis(connection_pool=redis_pool) as redis:
        await redis.set("key", "value")
    return msg

