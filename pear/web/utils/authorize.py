# coding=utf-8
from functools import wraps

from flask import session, request, jsonify
from pear.utils.logger import logger


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u_id = request.cookies.get('u_id')
        authorized = u_id and session.get(u_id)
        logger.info(u'authorize user_id:{}, authorized:{}'.format(u_id, authorized))
        if not authorized:
            return jsonify(message=u"需要登录"), 401
        return func(*args, **kwargs)

    return wrapper
