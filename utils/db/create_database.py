from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from models.model import BaseModel
from settings import settings


async def create_database() -> None:
    """
    创建数据库
    """
    engine = create_async_engine(str(settings.db_url.with_path("/")))

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                f" WHERE SCHEMA_NAME='{settings.db_base}';",
            ),
        )
        database_exists = database_existance.scalar() == 1
        if not database_exists:

            async with engine.connect() as conn:  # noqa: WPS440
                await conn.execute(
                    text(
                        f"CREATE DATABASE {settings.db_base};",
                    ),
                )


async def drop_database() -> None:
    """Drop current database."""
    engine = create_async_engine(str(settings.db_url.with_path(settings.db_base)))
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE {settings.db_base};"))


async def create_db_and_tables():
    engine = create_async_engine(str(settings.db_url.with_path(settings.db_base)))
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
