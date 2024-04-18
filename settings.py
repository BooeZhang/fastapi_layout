import enum
from typing import Optional

from pydantic.v1 import BaseSettings
from yarl import URL


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """日志级别."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    应用配置
    """

    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    # uvicorn 工作进程数量
    workers_count: int = 1
    # 当前环境
    environment: str = "dev"
    log_level: LogLevel = LogLevel.INFO

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_pass: str = "root"
    db_base: str = "fastapi_layout"
    db_echo: bool = True
    super_user: str = "admin"
    super_user_pwd: str = "admin123456"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    rabbit_host: str = "fastapi_layout-rmq"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"
    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    jwt_key = "jwtss"
    jwt_algorithm = "HS256"
    jwt_time_out = 3600  # 秒

    # 运行环境
    # 可接受的值: 回测, 实时交易, 'fitness'.
    trading_mode = ""

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """

        # return URL.build(
        #     scheme="sqlite",
        #     host=self.db_host,
        #     port=self.db_port,
        #     user=self.db_user,
        #     password=self.db_pass,
        #     path=f"/{self.db_base}",
        # )
        return "sqlite:///./test.postgreSQL"

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"

        if self.redis_user is None or self.redis_pass is None:
            return URL.build(
                scheme="redis",
                host=self.redis_host,
                port=self.redis_port,
                path=path,
            )
        else:
            return URL.build(
                scheme="redis",
                host=self.redis_host,
                port=self.redis_port,
                user=self.redis_user,
                password=self.redis_pass,
                path=path,
            )

    @property
    def rabbit_url(self) -> URL:
        """
        Assemble RabbitMQ URL from settings.

        :return: rabbit URL.
        """
        return URL.build(
            scheme="amqp",
            host=self.rabbit_host,
            port=self.rabbit_port,
            user=self.rabbit_user,
            password=self.rabbit_pass,
            path=self.rabbit_vhost,
        )

    class Config:
        env_file = ".env"
        env_prefix = "FASTAPI_LAYOUT_"
        env_file_encoding = "utf-8"


settings = Settings()
