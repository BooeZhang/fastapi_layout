import logging
import sys
from typing import Union, Any

from loguru import logger

from settings import settings


def record_formatter(record: dict[str, Any]) -> str:  # pragma: no cover
    """
    格式化日志输出
    """
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level: <8}</level> "
        # "| <magenta>trace_id={extra[trace_id]}</magenta> "
        # "| <blue>span_id={extra[span_id]}</blue> "
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>\n"
    )

    # record["extra"]["span_id"] = 0
    # record["extra"]["trace_id"] = 0
    if record["exception"]:
        log_format = f"{log_format}{{exception}}"

    return log_format


class InterceptHandler(logging.Handler):
    """
    拦截所有日志请求并将它们传递给 loguru

    详细信息，查看：
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        将日志传递给 logru
        :param record:
        :return:
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def configure_logging() -> None:
    """
    配置日志
    :return:
    """
    intercept_handler = InterceptHandler()
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []
        if logger_name.startswith("taskiq."):
            logging.getLogger(logger_name).root.handlers = [intercept_handler]

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # set logs output, level and format
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level.value,
        format=record_formatter,  # type: ignore
    )
