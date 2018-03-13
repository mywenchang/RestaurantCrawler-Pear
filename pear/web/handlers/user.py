# coding=utf-8
import logging

from flask import Blueprint
from pear.models.user import UserDao
from pear.utils.authorize import authorize

user_router = Blueprint('user', __name__, url_prefix='/user')

logger = logging.getLogger('')


@user_router.route('/log_in', methods=['POST'])
def log_in():
    UserDao.get_by_id('')


@user_router.route('/sign_up', methods=['POST'])
def sign_up():
    pass


@user_router.route('/', methods=['GET'])
@authorize
def get_info():
    pass
