import arrow

local = "CST"


def get_now_timestamp() -> int:
    """
    获取当前秒级时间戳
    :return:
    """
    return arrow.now(local).int_timestamp
