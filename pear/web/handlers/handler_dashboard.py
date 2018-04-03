# coding=utf-8

from flask import Blueprint, request, jsonify

dashboard_router = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_router.route('')
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
        "crawler_tasks": [
            {"id": "1", "type": "dish", "source": "ele", "total": 400, "current": 200, "status": -1},
            {"id": "2", "type": "dish", "source": "ele", "total": 400, "current": 400, "status": 1},
            {"id": "3", "type": "dish", "source": "ele", "total": 400, "current": 260, "status": 0},
            {"id": "4", "type": "dish", "source": "ele", "total": 500, "current": 500, "status": 0},
        ],
        "analyse_tasks": [
            {"id": "1", "type": "dish", "source": "ele", "total": 400, "current": 200, "status": -1},
            {"id": "2", "type": "dish", "source": "ele", "total": 400, "current": 300, "status": 0}
        ],
        "u_id": u_id
    }
    return jsonify(data)
