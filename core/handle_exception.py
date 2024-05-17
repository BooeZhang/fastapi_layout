from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request

from utils.erroron.base import CustomException
from utils.erroron.code import AuthorizationException


def register_exception(app):

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(
        request: Request, e: AuthorizationException
    ):
        """
        认证异常处理
        """
        return ORJSONResponse(
            status_code=403,
            content=jsonable_encoder({"code": e.code, "msg": e.msg, "data": None}),
        )

    @app.exception_handler(CustomException)
    async def authentication_exception_handler(request: Request, e: CustomException):
        """
        统一异常处理
        """
        return ORJSONResponse(
            status_code=200,
            content=jsonable_encoder({"code": e.code, "msg": e.msg, "data": None}),
        )

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc):
        return await http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        return await request_validation_exception_handler(request, exc)
