import inspect
from functools import wraps
from typing import Callable, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse


_RT = TypeVar("_RT")


def unify_json(fn: Callable[..., _RT]) -> Callable[..., _RT]:
    """
    统一响应格式
    """

    @wraps(fn)
    async def wrapper(*args, **kwargs) -> _RT:
        if inspect.iscoroutinefunction(fn):
            resp = await fn(*args, **kwargs) or []
        else:
            resp = fn(*args, **kwargs) or []

        return ORJSONResponse(
            content=jsonable_encoder({"code": 200, "msg": "OK", "data": resp})
        )

    return wrapper
