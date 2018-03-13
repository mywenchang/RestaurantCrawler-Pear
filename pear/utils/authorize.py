# coding=utf-8
from functools import wraps

from flask import session, jsonify, request


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u_id = request.cookies.get('u_id')
        name = session.get(u_id)
        if not name:
            return jsonify(msg='Need Log'), 401
        return func(*args, **kwargs)

    return wrapper
