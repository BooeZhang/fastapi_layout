from fastapi import APIRouter, Depends

from redis.asyncio import Redis

from middleware.unify_json import unify_json
from rest.common.schemas import Message

from store.redis.dependency import get_redis_client

router = APIRouter()


@router.get("/", response_model=Message)
@unify_json
async def index(redis_client: Redis = Depends(get_redis_client)) -> Message:
    msg = Message(message="hello world")
    await redis_client.set("key", "value")
    return msg
