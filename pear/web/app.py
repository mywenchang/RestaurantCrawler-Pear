# coding=utf-8

from flask import Flask, request, jsonify

from pear.utils.config import IS_DEBUG
from pear.utils.logger import logger

application = Flask(__name__)
application.secret_key = "pear_web_secret_key"


def install_modules():
    from pear.web.handlers.user import user_router
    from pear.web.handlers.config_ele_crawler import config_ele_crawler_router
    from pear.web.handlers.authorize import authorize_router
    from pear.web.handlers.crawler_tasks import crawler_tasks_router
    from pear.web.handlers.config_meituan_crawler import config_mt_crawler_router
    from pear.web.handlers.data_analyse import data_router
    application.register_blueprint(user_router)
    application.register_blueprint(config_ele_crawler_router)
    application.register_blueprint(config_mt_crawler_router)
    application.register_blueprint(authorize_router)
    application.register_blueprint(crawler_tasks_router)
    application.register_blueprint(data_router)


install_modules()


@application.route("/")
def index():
    return jsonify(status='ok')


@application.before_request
def before_request():
    logger.info(request.path)


@application.after_request
def after_request(response):
    # 允许跨域(Access-Control-Allow-Credentials 为 true 时，值不能为*，必须为指定的 protocol://host:port)
    origin = request.headers.get('origin')
    response.headers.add('Access-Control-Allow-Origin', origin)
    # 和前端 fetch 的credentials选项配合，使其可以获取cookie
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    # 当 Access-Control-Allow-Credentials 为 true 时，需要指定允许的header key
    response.headers.add('Access-Control-Allow-Headers', 'content-type, accept, Access-Control-Allow-Origin')
    #
    response.headers.add('Access-Control-Allow-Methods', 'DELETE, PATCH, POST, PUT,GET, OPTIONS')

    return response
