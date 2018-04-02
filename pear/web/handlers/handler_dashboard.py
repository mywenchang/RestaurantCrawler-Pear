# coding=utf-8

from flask import Blueprint, request, jsonify

dashboard_router = Blueprint('dashboard', __name__)


@dashboard_router.route('/')
def index():
    u_id = request.cookies.get('u_id')
    data = {
        "crawlers": [
            {
                "name": u"饿了么",
                "source": "ele"
            },
            {
                "name": u"美团",
                "source": "meituan"
            }
        ],
        "tasks": [{"id":"1", "type": "dish", "source":"ele", "total": 400, "current": 200, "status":0 }],
        "u_id": u_id
    }
    return jsonify(data)
