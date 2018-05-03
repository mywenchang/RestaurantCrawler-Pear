# coding=utf-8

import re
from numbers import Number

REGEX = r'\d+(.\d+)?'


def get_number_from_str(str):
    """
    从一下字符串中提取数字
    配送费:￥0
    起送:￥10
    4.5分
    30分钟
    """
    if not str:
        return 0
    str = str.strip()
    match = re.match(REGEX, str)
    if match:
        num = match.group(0)
        try:
            return int(num)
        except ValueError:
            return float(num)
    return 0
