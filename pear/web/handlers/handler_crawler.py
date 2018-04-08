# coding=utf-8
import json
import logging

from flask import jsonify, Blueprint, request, Response

from pear.crawlers import Crawlers
from pear.models.crawler import CrawlerDao
from pear.utils.authorize import authorize
from pear.web.controllers.controller_crawler import new_crawler, get_ele_msg_code, login_ele_by_mobile, get_captchas, \
    get_ele_city_list, search_ele_address, get_ele_restaurants

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
        return jsonify(success=False, message=e.message.__str__()), 500
    return jsonify(success=True, message='create crawler success'), 202


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
    return jsonify(success=True, ele_image_base64=ele_image_base64, ele_image_token=ele_image_token)


# 获取短信验证码
@crawlers_router.route('/ele_sms_code', methods=['GET'])
@authorize
def get_sms_code():
    mobile = request.args.get('mobile')
    pic_code = request.args.get('ele_pic_code', '')
    image_token = request.args.get('ele_image_token', '')
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
    data = json.dumps({
        'success': True
    })
    if success:
        resp = Response(data, mimetype='application/json')
        for i, v in cookies.iteritems():
            resp.set_cookie(i, v)
        resp.set_cookie('ele_has_login', '1')
        return resp
    return jsonify(success=False)


# --------------------------------------------

@crawlers_router.route('/ele_cities')
def fetch_ele_cites():
    city_dict = get_ele_city_list()
    if city_dict:
        return jsonify(city_dict)
    else:
        return []


@crawlers_router.route('/search_ele_address')
def ele_address():
    keyword = request.args.get('key')
    data = search_ele_address(keyword)
    if data:
        return jsonify(data)
    else:
        return jsonify([])


@crawlers_router.route('/get_ele_restaurants', methods=['POST'])
def ele_restaurants():
    cookies = request.cookies
    address = request.json
    offset = 0
    limit = 24
    result = []
    ids = set()
    while True:
        data = get_ele_restaurants(address.get('geohash'), address.get('latitude'), address.get('longitude'),
                                   offset=offset, limit=limit, cookies=cookies)
        if data:
            for item in data:
                if item.get('id') not in ids:
                    result.append(item)
                    ids.add(item.get('id'))
            offset += limit
        else:
            return jsonify(result)


@crawlers_router.route('/configs', methods=['GET'])
@authorize
def crawlers_configs():
    platform = request.args.get('platform')
    data = {
        "ele": [
            {
                "type": "restaurant",
                "name": u"商家",
                "args": [
                    {
                        "key": "latitude",
                        "description": u"纬度",
                        "default": "30.64995"
                    }, {
                        "key": "longitude",
                        "description": u"经度",
                        "default": "104.18755"
                    }, {
                        "key": "limit",
                        "description": u"数据总量(-1 表示无限制)",
                        "default": -1
                    }
                ]
            }, {
                "type": "dish",
                "name": u"菜品",
                "args": [
                    {
                        "key": "latitude",
                        "description": u"纬度",
                        "default": "30.64995"
                    }, {
                        "key": "longitude",
                        "description": u"经度",
                        "default": "104.18755"
                    }, {
                        "key": "restaurant_id",
                        "description": u"店铺",
                        "default": 1
                    }
                ]
            }
        ],
        "meituan": []
    }
    return jsonify(sucess=True, configs=data.get(platform))
