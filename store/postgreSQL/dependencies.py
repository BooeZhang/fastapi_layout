from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from loguru import logger as log

from utils.erroron.base import CustomException


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    async with AsyncSession(request.app.state.db_engine) as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            if not isinstance(e, CustomException):
                log.error(f"db error: {e}")
            await session.rollback()
            raise
