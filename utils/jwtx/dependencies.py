from typing import Annotated

from fastapi import Header, Depends
from starlette.requests import Request

from utils.erroron import code
from utils.jwtx import jwtx
from utils.jwtx.jwtx import UserClaim


def get_token_claim(
    request: Request,
    token: Annotated[str, Depends(jwtx.oauth2_scheme)],
    authorization: Annotated[str | None, Header()] = None,
) -> UserClaim:
    """
    解析 token 获取用户信息
    """
    if authorization == "" or authorization is None:
        raise code.ErrNotLogin

    token_info = authorization.split(" ")
    if len(token_info) != 2:
        raise code.ErrNotLogin

    token = token_info[1]

    return jwtx.check_access_token(token)
