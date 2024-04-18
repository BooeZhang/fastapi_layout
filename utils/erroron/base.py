class CustomException(Exception):
    """
    自定义异常基类
    """

    code: int = 1
    msg: str = "error"
