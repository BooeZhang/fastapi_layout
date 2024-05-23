from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.handle_exception import register_exception
from middleware import register_middleware
from router import register_api_routes
from settings import settings

from core.log import configure_logging
from store.postgreSQL import database
from store.redis import redis_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.attach_to_app(app)
    redis_pool.attach_to_app(app)
    yield
    await database.close_connection()
    await redis_pool.close_connection()


def get_application():
    """
    应用程序的主要构造函数
    :return:
    """
    configure_logging()
    app = FastAPI(
        debug=settings.debug,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url=None,
        reload=True,
        openapi_url="/api/openapi.json" if settings.debug else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    register_middleware(app)
    register_exception(app)
    register_api_routes(app)
    return app
