# coding=utf-8

from flask import abort, jsonify
from flask.app import request

from pear_web import app
from pear_web.crawlers import Crawlers
from pear_web.models.crawler import Crawler
from pear_web.utils.const import SUPPORT_ACTIONS


@app.route('/crawlers', methods=['GET', 'POST'])
@app.route('/crawlers/<int:crawler_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def crawlers(crawler_id=None):
    action = request.form.get('action')
    if request.method == 'GET':
        # 爬虫信息
        if crawler_id:
            crawler = Crawler.query.get(crawler_id)
            return jsonify(crawler.to_dict())
        else:
            crawlers = Crawler.query.all()
            return jsonify([item.to_dict() for item in crawlers])
    elif request.method == 'POST':
        if action == 'create':
            type = request.form.get('type')
            source = request.form.get('source')
            action = _wrap_action(action, source, type)
            if action not in SUPPORT_ACTIONS:
                abort(400)
            crawler = Crawlers[action](request.form)
            crawler.start()
            return jsonify({'status': 'ok'})

        return 'post'
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


def _wrap_action(action, source, type):
    return '{}_{}_{}_crawler'.format(action, source, type)
