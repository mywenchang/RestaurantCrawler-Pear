# coding=utf-8

from functools import wraps

import time

__CREATED = 'created'
__EXPIRATION = 'expiration'
__RESULT = 'result'


def mem_cache(expiration=60 * 60 * 60):
    """
    内存缓存
    :param expiration: 过期时间(秒)
    :return:
    """

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = u'{}_{}_{}'.format(func.__name__, args, kwargs)
            entity = cache.get(key, None)
            if entity:
                now = int(time.time())
                created = entity.get(__CREATED)
                expires = entity.get(__EXPIRATION)
                if now - created > expires:
                    # cache expires
                    cache[key] = None
                else:
                    return cache[key][__RESULT]

            # add to cache
            cache.setdefault(key, {})
            result = func(*args, **kwargs)
            cache[key] = {
                __CREATED: int(time.time()),
                __EXPIRATION: expiration,
                __RESULT: result
            }
            return result

        return wrapper

    return decorator
