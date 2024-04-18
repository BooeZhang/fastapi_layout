from sqlmodel import Session, select

from models.user import User


def get_user_by_name(db: Session, username: str) -> User:
    """
    根据用户名获取用户
    """
    stmt = select(User).where(User.name == username)
    result = db.exec(stmt)
    return result.first()
