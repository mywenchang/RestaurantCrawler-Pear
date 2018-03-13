# coding=utf-8
import json
import logging

from flask import Blueprint
from flask import request, jsonify, session, Response
from pear.models.user import UserDao
from pear.utils.authorize import authorize

user_router = Blueprint('user', __name__, url_prefix='/user')

logger = logging.getLogger('')


@user_router.route('/log_in', methods=['POST'])
def log_in():
    passwd = request.form.get('passwd')
    account = request.form.get('account')
    if not passwd or not account:
        return jsonify(message='Need Name/Email/Mobile'), 400
    user = UserDao.get_by_args(passwd, account)
    if not user:
        return jsonify(message='Not user.')
    session[user.id] = user.name
    logger.info(user)
    resp = Response(json.dumps(dict(message='Log in success')), mimetype='application/json')
    resp.set_cookie(key='u_id', value=str(user.id))
    return resp


@user_router.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form.get('email')
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    if UserDao.is_exist(email=email, name=name, mobile=mobile):
        return jsonify(message='User existed!'), 409
    passwd = request.form.get('passwd')
    if not passwd and not mobile:
        return jsonify(message='Must have password and mobile.'), 400
    u_id = UserDao.create(name=name, passwd=passwd, email=email, mobile=mobile)
    resp = Response(json.dumps(dict(message='Sign up success')), mimetype='application/json')
    resp.set_cookie(key='u_id', value=str(u_id))
    return resp


@user_router.route('/', methods=['GET'])
@authorize
def get_info():
    u_id = request.cookies.get('u_id')
    user = UserDao.get_by_id(u_id)
    if not user:
        return jsonify(message='Need Log'), 401
    return jsonify(data=_wrap_user(user))


def _wrap_user(item):
    return {
        'id': item.id,
        'name': item.name,
        'mobile': item.mobile,
        'created': item.created.strftime('%Y-%d-%m %H:%M:%S')
    }
