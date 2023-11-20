from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.index import Message
from store.mysql.dependencies import get_db_session

router = APIRouter()


@router.get("/", response_model=Message)
def user(db: AsyncSession = Depends(get_db_session)) -> Message:
    select(User).where('user_name = sss')
