# coding=utf-8
import logging

from flask import jsonify, Blueprint, request, Response

from pear.models.crawler import CrawlerDao
from pear.utils.authorize import authorize
from pear.web.controller.crawler_controller import new_crawler, get_ele_msg_code, login_ele_by_mobile, get_captchas

crawlers_router = Blueprint('crawlers', __name__, url_prefix='/crawlers')

logger = logging.getLogger('')


@crawlers_router.route('/<int:crawler_id>', methods=['GET'])
@authorize
def get_crawler(crawler_id=None):
    u_id = request.cookies.get('u_id')
    crawler = CrawlerDao.get_by_id(crawler_id, u_id)
    return jsonify(data=crawler)


@crawlers_router.route('/', methods=['GET'])
@authorize
def get_crawlers():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 20)
    status = request.args.get('status', None)
    u_id = request.cookies.get('u_id')
    crawlers = CrawlerDao.batch_get_by_status(u_id, page=int(page), per_page=int(per_page), status=status)
    return jsonify({'per_page': per_page, 'data': crawlers})


@crawlers_router.route('/', methods=['POST'])
@authorize
def create_crawler():
    source = request.form.get('source')
    type = request.form.get('type')
    args = request.form.get('args')
    u_id = request.cookies.get('u_id')
    try:
        new_crawler.put(u_id=u_id, source=source, type=type, args=args)
    except Exception as e:
        return jsonify(message=e.message.__str__()), 500
    return jsonify(message='create crawler success'), 202


@crawlers_router.route('/<int:crawler_id>', methods=['PUT'])
@authorize
def update_crawler(crawler_id):
    return jsonify(status="ok")


@crawlers_router.route('/<int:crawler_id>', methods=['DELETE'])
@authorize
def delete_crawler(crawler_id):
    return jsonify(status="ok")


# ------------------登录饿了么-----------------

"""
登录饿了么流程:
 输入手机号 -> 获取验证码图片 -> 输入验证码图片上字符 -> 获取登录短信验证码 -> 输入短信验证码，登录饿了么-> 获取登录成功的token存储到cookie
"""


# 获取图片验证码
@crawlers_router.route('/get_ele_pic_code', methods=['GET'])
@authorize
def get_pic_code():
    mobile = request.args.get('mobile')
    image_base64, image_token = get_captchas(mobile)
    return jsonify(image_base64=image_base64, image_token=image_token)


# 输入图片验证码字符，然后获取短信验证码
@crawlers_router.route('/get_sms_code', methods=['GET'])
@authorize
def get_sms_code():
    mobile = request.args.get('mobile')
    pic_code = request.args.get('pic_code')
    image_token = request.args.get('image_token')
    success, sms_token, msg = get_ele_msg_code(mobile, pic_code, image_token)
    return jsonify(success=success, sms_token=sms_token, message=msg)


# 输入短信验证码登录
@crawlers_router.route('/login_ele', methods=['POST'])
@authorize
def login_ele():
    mobile = request.json.get('mobile')
    sms_code = request.json.get('sms_code')
    sms_token = request.json.get('sms_token')
    success, cookies, content = login_ele_by_mobile(mobile, sms_code, sms_token)
    if success:
        resp = Response(jsonify(success=success))
        for i, v in cookies.iteritems():
            resp.set_cookie(i, v)
        return resp
    return jsonify(success=success, message=content)


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
