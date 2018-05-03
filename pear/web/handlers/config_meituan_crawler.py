# coding=utf-8
import json

from flask import Blueprint, jsonify, request, Response

from pear.utils.logger import logger
from pear.web.controllers import mt_crawler_controller
from pear.web.utils.set_cookie import set_cookie

config_mt_crawler_router = Blueprint('config_mt_crawler', __name__, url_prefix='/config_mt_crawler')


@config_mt_crawler_router.route('/restaurant_list')
def restaurant_list():
    address = request.args.get('address')
    lat_lng = request.args.get('lat_lng')
    try:
        ll = lat_lng.split(',')
        lng = ll[0]
        lat = ll[1]
    except IndexError:
        return jsonify(message=u'坐标组合错误', success=False), 400
    except Exception as e:
        logger.error(e, exc_info=True)
        return jsonify(message=e.__str__(), success=False), 400
    success, data, cookies, msg = mt_crawler_controller.get_restaurants(address, lat, lng)

    resp = Response(json.dumps(
        {
            'success': success,
            'data': data,
            'msg': msg
        }
    ))

    return resp
