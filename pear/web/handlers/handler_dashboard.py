# coding=utf-8

from flask import Blueprint, request, jsonify

from pear.models.crawler import CrawlerDao

dashboard_router = Blueprint('dashboard', __name__)


@dashboard_router.route('/')
def index():
    u_id = request.cookies.get('u_id')
    data = {
        "crawlers": [
            {
                "name": u"饿了么",
                "type": "ele"
            },
            {
                "name": u"美团",
                "type": "meituan"
            }
        ],
        "u_id": u_id
    }
    if u_id:
        crawlers = CrawlerDao.batch_get_by_status(u_id)
        data["tasks"] = crawlers
    return jsonify(data=data)
