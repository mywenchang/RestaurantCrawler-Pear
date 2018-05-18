# coding=utf-8

from flask import Blueprint, jsonify, request

from pear.utils.logger import logger
from pear.web.controllers.mt_crawler_controller import commit_mt_crawler_task

config_mt_crawler_router = Blueprint('config_mt_crawler', __name__, url_prefix='/config_mt_crawler')


@config_mt_crawler_router.route('/commit_crawler', methods=['POST'])
def commit_task():
    locations = request.json
    success = True
    if not isinstance(locations, list):
        return jsonify(message=u'数据错误', success=False), 400
    for item in locations:
        try:
            address = item['address']
            ll = item['lng_lat'].split(',')
            lng = ll[0]
            lat = ll[1]
            commit_mt_crawler_task.put(address=address, lng=lng, lat=lat, cookies=request.cookies)
        except IndexError:
            return jsonify(message=u'坐标组合错误', success=False), 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return jsonify(message=e.__str__(), success=False), 400
    return jsonify(success=success)
