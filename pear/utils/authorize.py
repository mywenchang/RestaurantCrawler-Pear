# coding=utf-8
from flask import session, jsonify, request


def authorize(func):
    def wrapper(*args, **kwargs):
        user_name = request.cookies.get('user')
        name = session.get(user_name)
        if not name:
            return jsonify(msg='Need Log'), 401
        return func(*args, **kwargs)

    return wrapper
