# coding=utf-8
import logging

from flask import jsonify, Blueprint
from flask.app import request
from pear.models.crawler import CrawlerDao
from pear.web.controller.crawler_controller import start_crawl

crawlers_router = Blueprint('crawlers', __name__, url_prefix='/crawlers')

logger = logging.getLogger('')


@crawlers_router.route('', methods=['GET', 'POST'])
@crawlers_router.route('/<int:crawler_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def crawlers(crawler_id=None):
    logger.info(request.form)
    if request.method == 'GET':
        # 爬虫信息
        if crawler_id:
            crawler = CrawlerDao.get_by_id(crawler_id)
            return jsonify(crawler.to_dict())
        else:
            page = request.form.get('page', 1)
            per_page = request.form.get('per_page', 20)
            status = request.form.get('status', None)
            crawlers = CrawlerDao.batch_get_by_status(page=page, per_page=per_page, status=status)
            return jsonify([item.to_dict() for item in crawlers])
    elif request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            source = request.form.get('source')
            type = request.form.get('type')
            args = request.form.get('args')
            start_crawl.deque(source=source, type=type, action=action, args=args)
            return jsonify({'status': 'ok'})
    elif request.method == 'PUT':
        # 更新某个爬虫信息(提供该爬虫所有信息)
        return 'put'
    elif request.method == 'PATCH':
        # 更新某个爬虫信息(提供该爬虫部分信息)
        return 'patch'
    elif request.method == 'DELETE':
        # 删除某个爬虫
        return 'delete'
    return 'crawler'
