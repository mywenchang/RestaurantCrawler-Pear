# coding=utf-8

import json

from flask import Blueprint, request, jsonify, session, Response

from pear.models.user import UserDao

authorize_router = Blueprint('auth', __name__, url_prefix='/auth')


@authorize_router.route('/login', methods=['POST'])
def login():
    password = request.json.get('password')
    account = request.json.get('account')
    if not password or not account:
        return jsonify(message='Need account(Name/Email/Mobile).'), 400
    user = UserDao.get_by_args(password, account)
    if not user:
        return jsonify(message='{} not exist.'.format(account)), 401
    session[user['id']] = user['name']
    resp = Response(json.dumps(dict(message='Login Success.')), mimetype='application/json')
    resp.headers.add('Access-Control-Allow-Credentials', 'true')
    resp.set_cookie(key='u_id', value=str(user['id']))
    return resp


@authorize_router.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    name = request.json.get('name')
    mobile = request.json.get('mobile')
    password = request.json.get('password')
    if UserDao.is_exist(email=email, name=name, mobile=mobile):
        return jsonify(message='User existed.'), 409
    if not password or not mobile:
        return jsonify(message='Must have password and mobile.'), 400
    UserDao.create(name, password, email, mobile)
    return jsonify(message="SignUp Success.")
