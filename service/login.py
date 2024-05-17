from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

import repo
from middleware.unify_json import unify_json
from models.user import UserRes
from serialization.login import LoginReq, LoginRes
from store.postgreSQL.dependencies import get_db_session
from utils import jwtx
from utils.erroron import code

router = APIRouter()


@router.post("/login", summary="登陆", response_model=LoginRes)
@unify_json
async def login(
    param: LoginReq, db: AsyncSession = Depends(get_db_session)
) -> LoginRes:
    """
    登录
    """
    _user = await repo.get_user_by_name(db, param.username)
    if not _user or not _user.check_pwd(param.password):
        raise code.ErrUserNameOrPwd()

    access_token, access_expire = jwtx.create_access_token(
        {"user_id": _user.id, "username": _user.name}
    )

    ref_token, ref_expire = jwtx.create_refresh_token(
        {"user_id": _user.id, "username": _user.name}
    )
    user_info = UserRes.model_validate(_user)
    return LoginRes(
        user_info=user_info,
        access_token=access_token,
        expire=access_expire,
        refresh_token=ref_token,
        refresh_expire=ref_expire,
    )
