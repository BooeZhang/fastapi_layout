from dataclasses import dataclass

from utils.erroron.base import CustomException


@dataclass
class AuthorizationException(Exception):
    """
    无权限错误
    """

    code: int = 403
    msg: str = "无权限"


@dataclass
class ErrUserNameOrPwd(CustomException):
    code: int = 1000
    msg: str = "用户名或密码错误"


@dataclass
class ErrTokenExpired(CustomException):
    code: int = 1001
    msg: str = "token 过期"


@dataclass
class ErrTokenInvalid(CustomException):
    code: int = 1002
    msg: str = "token 无效"


@dataclass
class ErrNotLogin(CustomException):
    code: int = 1003
    msg: str = "未登录或非法访问"


@dataclass
class ErrNotFoundUser(CustomException):
    code: int = 1004
    msg: str = "用户不存在"


@dataclass
class ErrUserRepeat(CustomException):
    code: int = 1005
    msg: str = "用户重复"
