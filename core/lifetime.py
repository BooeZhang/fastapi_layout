from typing import Callable, Awaitable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from store.mysql.lifetime import shutdown_mysql, init_mysql
from store.redis.lifetime import init_redis, shutdown_redis
from utils.db.create_database import create_db_and_tables


def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    集成 prometheus
    :param app:
    :return:
    """
    # PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
    #     app,
    # ).expose(app, should_gzip=True, name="prometheus_metrics")
    pass


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    在 fast api 启动时执行一些操作
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        init_mysql(app)
        init_redis(app)
        # init_rabbit(app)
        # await init_kafka(app)
        # setup_prometheus(app)
        app.middleware_stack = app.build_middleware_stack()
        await create_db_and_tables()

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    在应用程序关闭时清理资源
    :param app:
    :return:
    """
    @app.on_event("shutdown")
    async def _shutdown() -> None:
        # if not broker.is_worker_process:
        #     await broker.shutdown()
        await shutdown_mysql(app)

        await shutdown_redis(app)
        # await shutdown_rabbit(app)
        # await shutdown_kafka(app)

    return _shutdown
