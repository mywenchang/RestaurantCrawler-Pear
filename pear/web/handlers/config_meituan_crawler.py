# coding=utf-8

from flask import Blueprint, jsonify

config_mt_crawler_router = Blueprint('config_mt_crawler', __name__, url_prefix='/config_mt_crawler')


@config_mt_crawler_router.route('/search_address/<string:key>')
def search_address(key):
    return jsonify(key)
