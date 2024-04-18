from typing import AsyncGenerator

from sqlmodel import Session
from starlette.requests import Request
from loguru import logger as log

from utils.erroron.base import CustomException


async def get_db_session(request: Request) -> AsyncGenerator[Session, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    with Session(request.app.state.db_engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            if not isinstance(e, CustomException):
                log.error(f"db error: {e}")
            session.rollback()
            raise
