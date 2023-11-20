from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.unify_json import unify_json
from models.user import User
from schemas.index import Message
from store.mysql.dependencies import get_db_session

router = APIRouter()


@router.get("/", response_model=Message)
@unify_json
async def user(db: AsyncSession = Depends(get_db_session)) -> Message:
    stmt = select(User).where(User.name == "spongebob")
    result = await db.execute(stmt)
    print(result)
    msg = Message(message='hello world')
    return msg
