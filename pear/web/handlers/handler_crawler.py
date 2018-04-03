# coding=utf-8
import logging

from flask import jsonify, Blueprint, request, Response

from pear.crawlers import Crawlers
from pear.models.crawler import CrawlerDao
from pear.utils.authorize import authorize
from pear.web.controllers.controller_crawler import new_crawler, get_ele_msg_code, login_ele_by_mobile, get_captchas

crawlers_router = Blueprint('crawlers', __name__, url_prefix='/crawlers')

logger = logging.getLogger('')


@crawlers_router.route('/<int:crawler_id>', methods=['GET'])
@authorize
def get_crawler(crawler_id=None):
    u_id = request.cookies.get('u_id')
    crawler = CrawlerDao.get_by_id(crawler_id, u_id)
    return jsonify(data=crawler)


@crawlers_router.route('', methods=['GET'])
@authorize
def get_crawlers():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 20)
    status = request.args.get('status', None)
    u_id = request.cookies.get('u_id')
    crawlers = CrawlerDao.batch_get_by_status(u_id, page=int(page), per_page=int(per_page), status=status)
    return jsonify({'per_page': per_page, 'data': crawlers})


@crawlers_router.route('', methods=['POST'])
@authorize
def create_crawler():
    source = request.json.get('source')
    type = request.json.get('type')
    crawler = '{}_{}_crawler'.format(source, type)
    if crawler not in Crawlers.keys():
        return jsonify(message='Not find {}'.format(crawler)), 400
    args = request.json.get('args')
    cookies = request.cookies
    try:
        new_crawler.put(crawler=crawler, cookies=cookies, args=args)
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
@crawlers_router.route('/ele_pic_code', methods=['GET'])
@authorize
def get_pic_code():
    mobile = request.args.get('mobile')
    ele_image_base64, ele_image_token = get_captchas(mobile)
    logging.info(u'饿了么图片验证码:{}\n{}'.format(ele_image_base64, ele_image_token))
    return jsonify(ele_image_base64=ele_image_base64, ele_image_token=ele_image_token)


# 获取短信验证码
@crawlers_router.route('/ele_sms_code', methods=['GET'])
@authorize
def get_sms_code():
    mobile = request.args.get('mobile')
    pic_code = request.args.get('pic_code', '')
    image_token = request.args.get('image_token', '')
    success, ele_sms_token, msg = get_ele_msg_code(mobile, pic_code, image_token)
    return jsonify(success=success, ele_sms_token=ele_sms_token, message=msg)


# 通过短信验证码登录
@crawlers_router.route('/login_ele', methods=['GET'])
@authorize
def login_ele():
    mobile = request.args.get('mobile')
    sms_code = request.args.get('ele_sms_code', '')
    sms_token = request.args.get('ele_sms_token', '')
    success, cookies, content = login_ele_by_mobile(mobile, sms_code, sms_token)
    if success:
        resp = Response(jsonify(success=success, message=content), mimetype='application/json')
        for i, v in cookies.iteritems():
            resp.set_cookie(i, v)
        return resp
    return jsonify(success=False, message=content)


# --------------------------------------------

@crawlers_router.route('/configs', methods=['GET'])
@authorize
def crawlers_configs():
    return jsonify({
        "data": [
            {
                "platform": "ele",
                "types": [
                    {
                        "name": u"商家",
                        "value": "restaurant"
                    },
                    {
                        "name": u"菜品",
                        "value": "dish"
                    }
                ]
            }
        ]
    })
