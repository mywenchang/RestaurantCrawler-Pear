# coding=utf-8

from flask import Blueprint, jsonify, request
from pear.web.controllers import mt_crawler_controller

config_mt_crawler_router = Blueprint('config_mt_crawler', __name__, url_prefix='/config_mt_crawler')


@config_mt_crawler_router.route('/search_address')
def search_address():
    key = request.args.get('key')
    city = request.args.get('city')
    data = mt_crawler_controller.get_place_by_region(key, city)
    return jsonify(data)


@config_mt_crawler_router.route('/get_area_page')
def area_page():
    key = request.args.get('key')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    location = mt_crawler_controller.get_area_page(key, lat, lng)
    mt_crawler_controller.get_restaurants(location)
    return jsonify(location=location)

"""
3565863.78666
11598884.3118

marks[]: 30.656917,104.195018
marks[]: 30.652963,104.188051
marks[]: 30.653164,104.190516
marks[]: 30.681403,104.153661
marks[]: 30.993124,103.622414
"""