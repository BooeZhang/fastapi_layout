from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from rest.user.model import User


async def get_user_by_name(db: AsyncSession, username: str) -> User:
    """
    根据用户名获取用户
    """
    stmt = select(User).where(User.name == username)
    result = await db.exec(stmt)
    return result.first()
