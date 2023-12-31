from fastapi import APIRouter, Depends
from redis.asyncio import ConnectionPool, Redis

from middleware.unify_json import unify_json
from schemas.index import Message
from store.redis.dependency import get_redis_pool
from utils.erroron.code import Test

router = APIRouter()


@router.get("/", response_model=Message)
@unify_json
async def index(redis_pool: ConnectionPool = Depends(get_redis_pool)) -> Message:
    msg = Message(message='hello world')
    async with Redis(connection_pool=redis_pool) as redis:
        await redis.set("key", "value")
        raise Test()
    return msg

