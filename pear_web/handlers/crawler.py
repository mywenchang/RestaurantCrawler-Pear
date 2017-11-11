# coding=utf-8
from flask.app import request

from pear_web import app
from pear_web.crawlers import crawler_ele


@app.route('/crawlers', methods=['GET', 'POST'])
@app.route('/crawlers/<int:crawler_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def crawlers(crawler_id=None):
    if request.method == 'GET':
        # 返回所有爬虫
        return 'get'
    elif request.method == 'POST':
        # 新建一个爬虫
        crawler_ele.crawl_ele_restaurants()
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
