# coding=utf-8


def set_cookie(resp, key, value, max_age=None):
    """
    设置响应的cookie
    :param resp: Response对象
    :param key:  key
    :param value: value
    :param max_age: cookie超时时间，单位秒
    :return:
    """
    if max_age:
        resp.set_cookie(key=key, value=value, max_age=max_age)
    else:
        resp.set_cookie(key=key, value=value)
