import json
from typing import Callable

import orjson
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response
from fastapi.requests import Request


class UnifyJson(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response_body = [chunk async for chunk in response.body_iterator]
        copy_body = orjson.loads(response_body[0].decode('utf8'))
        data = {
            'code': 200,
            'msg': 'Ok',
            'data': copy_body
        }
        _dd = orjson.dumps(data)
        response.headers['content-length'] = str(len(_dd))
        response_body[0] = _dd
        print(response_body)

        response.body_iterator = iterate_in_threadpool(iter(response_body))
        return response
