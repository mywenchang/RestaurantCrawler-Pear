# coding=utf-8
from functools import wraps

from flask import session, request, jsonify
from pear.utils.logger import logger


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u_id = request.cookies.get('u_id')
        logger.info('authorize user_id {}'.format(u_id))
        if not u_id or session.get(u_id) is None:
            return jsonify(message=u"需要登录"), 401
        return func(*args, **kwargs)

    return wrapper
