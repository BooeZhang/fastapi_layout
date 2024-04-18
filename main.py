import uvicorn

from core.app import get_application
from settings import settings


app = get_application()


def main():
    uvicorn.run(
        "core.app:get_application",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
