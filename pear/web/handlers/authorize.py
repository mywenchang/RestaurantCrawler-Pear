# coding=utf-8

import json

from flask import Blueprint, request, jsonify, session, Response

from pear.models.user import UserDao
from pear.web.utils.set_cookie import set_cookie
from pear.utils.config import USER_LOGIN_MAX_AGE

authorize_router = Blueprint('auth', __name__, url_prefix='/auth')


@authorize_router.route('/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password')
    account = data.get('account')
    user = UserDao.get_by_args(password, account)
    if not user:
        return jsonify(status='false', message=u'密码错误'), 401
    session[user['id']] = user['name']
    resp = Response(json.dumps({'status': 'ok', 'user': user}), mimetype='application/json')
    set_cookie(resp, 'u_id', str(user['id']), max_age=USER_LOGIN_MAX_AGE)
    return resp


@authorize_router.route('/logout')
def logout():
    u_id = request.cookies.get('u_id')
    if u_id:
        session.pop(u_id, None)
    return jsonify(status='ok')


@authorize_router.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('mail')
    name = data.get('name')
    mobile = data.get('mobile')
    password = data.get('password')
    sms_code = data.get('smsCode')
    if UserDao.is_exist(email=email, name=name, mobile=mobile):
        return jsonify(status='false', message=u'用户已经存在'), 409
    if not password or not mobile:
        return jsonify(status='false', message=u'缺少密码或手机号'), 400
    u_id = UserDao.create(name, password, email, mobile)
    session[u_id] = name
    return jsonify(status='ok', message=u"注册成功", uId=u_id)
