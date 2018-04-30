# coding=utf-8

from pear.utils.config import IS_DEBUG, DOMAIN


def set_cookie(resp, key, value):
    """
    设置响应的cookie
    :param resp: Response对象
    :param key:  key
    :param value: value
    :return:
    """
    if IS_DEBUG:
        resp.set_cookie(key=key, value=value)
    else:
        resp.set_cookie(key=key, value=value, domain=DOMAIN)
