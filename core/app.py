from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.handle_exception import register_exception
from middleware import register_middleware
from settings import settings
from core.lifetime import register_startup_event, register_shutdown_event
from core.log import configure_logging
from router.api_router import api_router


def get_application():
    """
    应用程序的主要构造函数
    :return:
    """
    configure_logging()
    app = FastAPI(
        debug=settings.debug,
        docs_url="/api/docs",
        redoc_url=None,
        reload=True,
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    register_startup_event(app)
    register_shutdown_event(app)
    register_middleware(app)
    register_exception(app)

    app.include_router(router=api_router)
    return app
