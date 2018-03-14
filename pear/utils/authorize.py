# coding=utf-8
from functools import wraps

from flask import session, request, jsonify
import logging

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s', level=logging.INFO)
logger = logging.getLogger('')


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u_id = request.cookies.get('u_id')
        name = session.get(u_id)
        logger.info('authorize u_id={} name={}'.format(u_id, name))
        if not name:
            return jsonify(message="Need Log"), 401
        return func(*args, **kwargs)

    return wrapper
