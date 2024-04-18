from calendar import timegm
from datetime import datetime, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from loguru import logger as log
from pydantic import BaseModel

from settings import settings
from utils.erroron import code


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserClaim(BaseModel):
    """
    jwt 解析
    """

    user_id: int
    username: str
    exp: int


def create_access_token(v: dict) -> (str, int):
    """
    创建访问 token
    """
    expire = utc_timestamp() + settings.jwt_time_out
    _v = {"exp": expire, "role_id": [1]}
    v.update(_v)
    key = settings.jwt_key
    algorithm = settings.jwt_algorithm
    encoded = jwt.encode(v, key, algorithm=algorithm)
    return encoded, expire


def create_refresh_token(v: dict) -> (str, int):
    """
    创建刷新 token
    """
    expire = utc_timestamp() + settings.jwt_time_out + 600
    _v = {"exp": expire}
    v.update(_v)
    key = settings.jwt_key
    algorithm = settings.jwt_algorithm
    encoded = jwt.encode(v, key, algorithm=algorithm)
    return encoded, expire


def check_access_token(v: str) -> UserClaim:
    """
    解析 token
    """
    try:
        v = jwt.decode(v, settings.jwt_key, algorithms=[settings.jwt_algorithm])
        return UserClaim(**v)
    except jwt.ExpiredSignatureError:
        raise code.ErrTokenExpired()
    except Exception as e:
        log.error(f"token： {v} 解析失败, err: {e}")
        raise code.ErrTokenInvalid()


def utc_timestamp() -> int:
    return timegm(datetime.now(tz=timezone.utc).utctimetuple())


if __name__ == "__main__":
    print(utc_timestamp())
