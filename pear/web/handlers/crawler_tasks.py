# coding=utf-8

from flask import jsonify, Blueprint, request

from pear.models.crawler import CrawlerDao
from pear.models.dish import DishDao
from pear.models.rate import RateDao
from pear.utils.logger import logger
from pear.web.utils.authorize import authorize
from pear.web.controllers.comm import create_crawler_funcs

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
    # 菜品
    dishes, dish_total = DishDao.get_by_crawler_id(crawler_id, page=-1)
    # 评论
    rate, rate_total = RateDao.get_by_crawler_id(crawler_id, page=-1)
    return jsonify(
        crawler=crawler,
        dish={'total': dish_total, 'data': dishes},
        rate={'total': rate_total, 'data': rate}
    )


@crawler_tasks_router.route('/status/<int:crawler_id>')
@authorize
def get_crawler_status(crawler_id):
    u_id = request.cookies.get('u_id')
    crawler = CrawlerDao.get_by_id(crawler_id, u_id)
    logger.info(crawler['count'])
    return jsonify(crawler)


@crawler_tasks_router.route('', methods=['POST'])
@authorize
def create_crawler():
    source = request.args.get('source')
    if source not in ['ele', 'meituan']:
        return jsonify(succcess=False, message=u'不支持的来源:{}'.format(source)), 400
    return create_crawler_funcs[source](request)


@crawler_tasks_router.route('/<int:crawler_id>', methods=['DELETE'])
@authorize
def delete_crawler(crawler_id):
    u_id = request.cookies.get('u_id')
    CrawlerDao.delete(crawler_id, u_id)
    return jsonify(status="ok")
