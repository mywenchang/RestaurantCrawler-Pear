# coding=utf-8
import logging

from flask import jsonify, Blueprint, make_response
from flask.app import request

from pear.models.crawler import CrawlerDao
from pear.utils.authorize import authorize
from pear.web.controller.crawler_controller import create_crawler, get_ele_msg_code, login_ele_by_mobile, get_captchas

crawlers_router = Blueprint('crawlers', __name__, url_prefix='/crawlers')

logger = logging.getLogger('')


@crawlers_router.route('', methods=['GET', 'POST'])
@crawlers_router.route('/<int:crawler_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authorize
def handle_crawlers(crawler_id=None):
    if request.method == 'GET':
        if crawler_id:
            crawler = CrawlerDao.get_by_id(crawler_id)
            return jsonify(_wrap_result(crawler))
        else:
            page = request.args.get('page', 1)
            per_page = request.args.get('per_page', 20)
            status = request.args.get('status', None)
            crawlers = CrawlerDao.batch_get_by_status(page=int(page), per_page=int(per_page), status=status)
            return jsonify({
                'page': page,
                'per_page': per_page,
                'data': [_wrap_result(item) for item in crawlers]})
    elif request.method == 'POST':
        source = request.form.get('source')
        type = request.form.get('type')
        args = request.form.get('args')
        create_crawler.put(source=source, type=type, args=args)
        return jsonify({'status': 'ok'}), 202
    elif request.method == 'PUT':
        return 'put'
    elif request.method == 'PATCH':
        return 'patch'
    elif request.method == 'DELETE':
        return 'delete'
    return 'crawler'


@crawlers_router.route('/get_ele_code', methods=['POST'])
@authorize
def handle_login_ele():
    mobile = request.json.get('mobile')
    logger.info('mobile:{}'.format(mobile))
    success, token = get_ele_msg_code(mobile)
    if not success:
        c_image, c_hash = get_captchas(mobile)
        c_value = '验证码'
        logger.info(c_value)
        success, token = get_ele_msg_code(mobile, captcha_value=c_value, captch_hash=c_hash)
    resp = make_response(jsonify({'status': 'ok'}))
    resp.set_cookie(mobile, token)
    return resp


@crawlers_router.route('/login_ele_by_mobile', methods=['POST'])
@authorize
def handle_login_by_mobile():
    mobile = request.form.get('mobile')
    code = request.form.get('code')
    return login_ele_by_mobile(mobile, code, request.cookies.get(mobile))


@crawlers_router.route('/configs', methods=['GET'])
@authorize
def handel_crawlers_configs():
    return jsonify({
        "data": [
            {
                "args": [
                    "headers",
                    "cookies"
                ],
                "type": "restaurant",
                "name": "饿了么商家",
                "source": "ele"
            },
            {
                "args": [
                    "headers",
                    "cookies"
                ],
                "type": "dish",
                "name": "饿了么商家菜品",
                "source": "ele"
            },
            {
                "args": [
                    "headers",
                    "cookies"
                ],
                "type": "restaurant",
                "name": "美团商家",
                "source": "meituan"
            }
        ],
        "total": 3
    })


def _wrap_result(item):
    return {
        'id': item.id,
        'status': item.status,
        'created': item.created.strftime('%Y-%d-%m %H:%M:%S'),
        'finished': item.finished.strftime('%Y-%d-%m %H:%M:%S') if item.finished else '',
        'args': item.args,
        'info': item.info,
        'extras': item.extras,
        'total': item.total,
        'count': item.data_count
    }
