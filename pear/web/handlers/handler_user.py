# coding=utf-8

from flask import Blueprint, request

from pear.utils.authorize import authorize

user_router = Blueprint('user', __name__, url_prefix='/user')


@user_router.route('/')
@authorize
def get_user_info():
    u_id = request.cookies.get('u_id')
