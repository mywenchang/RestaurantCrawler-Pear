# coding=utf-8

import json

from flask import jsonify, Blueprint, request

from pear.models.crawler import CrawlerDao
from pear.models.dish import EleDishDao
from pear.models.rate import EleRateDao
from pear.models.restaurant import EleRestaurantDao
from pear.utils.authorize import authorize
from pear.web.controllers.controller_crawler import commit_crawler_task

crawler_tasks_router = Blueprint('tasks_router', __name__, url_prefix='/crawler_tasks')


@crawler_tasks_router.route('', methods=['GET'])
@authorize
def get_tasks():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    status = request.args.get('status')
    u_id = request.cookies.get('u_id')
    if status is not None:
        status = int(status)
    crawlers, total = CrawlerDao.batch_get_by_status(u_id, page=page, per_page=per_page, status=status)
    return jsonify({'page': page, "per_page": per_page, 'total': total, 'data': crawlers})


@crawler_tasks_router.route('/<int:crawler_id>', methods=['GET'])
@authorize
def get_crawler(crawler_id=None):
    u_id = request.cookies.get('u_id')
    crawler = CrawlerDao.get_by_id(crawler_id, u_id)
    if not crawler:
        return jsonify(crawler=None)
    # 商家
    restaurant_id = crawler.get('args').get('restaurant').get('id')
    restaurant = EleRestaurantDao.get_by_restaurant_id(int(restaurant_id))
    # 菜品
    dishes, dish_total = EleDishDao.get_by_crawler_id(crawler_id, page=-1)
    # 评论
    rate, rate_total = EleRateDao.get_by_crawler_id(crawler_id, page=-1)
    return jsonify(
        crawler=crawler,
        dish={'total': dish_total, 'data': dishes},
        rate={'total': rate_total, 'data': rate},
        restaurant=restaurant
    )


@crawler_tasks_router.route('', methods=['POST'])
@authorize
def create_crawler():
    try:
        cookies = request.cookies
        data_list = request.json
        for data in data_list:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if not data.get('restaurant') or not latitude or not longitude:
                return jsonify(success=False), 404
            args = {
                'restaurant': data.get('restaurant'),
                'latitude': latitude,
                'longitude': longitude
            }
            commit_crawler_task.put(source='ele', cookies=cookies, args=args)
    except Exception as e:
        return jsonify(success=False, message=e.message.__str__()), 500
    return jsonify(success=True), 200


@crawler_tasks_router.route('/<int:crawler_id>', methods=['PUT'])
@authorize
def update_crawler(crawler_id):
    return jsonify(status="ok")


@crawler_tasks_router.route('/<int:crawler_id>', methods=['DELETE'])
@authorize
def delete_crawler(crawler_id):
    return jsonify(status="ok")
