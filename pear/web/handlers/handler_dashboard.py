# coding=utf-8

from flask import Blueprint, request, jsonify

dashboard_router = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_router.route('')
def index():
    u_id = request.cookies.get('u_id')
    return jsonify({})
