# coding=utf-8
from flask import Blueprint
from flask.app import request

data_router = Blueprint('analyse', __name__, url_prefix='/analyse')


@data_router.route('/', methods=['GET', 'POST'])
@data_router.route('/<int:analyse_id>', methods=['GET', 'POST'])
def handle_analyse(analyse_id=None):
    if request.method == 'GET':
        return 'get'
    elif request.method == 'POST':
        return 'post'
    return 'analyse'
