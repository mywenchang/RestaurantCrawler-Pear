# coding=utf-8

from flask import Flask, request, jsonify

from pear.utils.config import IS_DEBUG
from pear.utils.logger import logger


def install_modules(app):
    from pear.web.handlers.user import user_router
    from pear.web.handlers.config_ele_crawler import config_ele_crawler_router
    from pear.web.handlers.authorize import authorize_router
    from pear.web.handlers.crawler_tasks import crawler_tasks_router
    from pear.web.handlers.ele_data_analyse import data_router
    app.register_blueprint(user_router)
    app.register_blueprint(config_ele_crawler_router)
    app.register_blueprint(authorize_router)
    app.register_blueprint(crawler_tasks_router)
    app.register_blueprint(data_router)


def get_application():
    app = Flask(__name__)
    install_modules(app)
    app.secret_key = "pear_web_secret_key"

    @app.route("/")
    def index():
        return jsonify(status='ok')

    @app.before_request
    def before_request():
        origin = request.headers.get('origin')
        address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        logger.info(u'origin: {}, address:{}, method:{}'.format(origin, address, request.method))

    @app.after_request
    def after_request(response):
        # 允许跨域(Access-Control-Allow-Credentials 为 true 时，值不能为*，必须为指定的 protocol://host:port)
        origin = request.headers.get('origin')
        response.headers.add('Access-Control-Allow-Origin', origin)
        # 和前端 fetch 的credentials选项配合，使其可以获取cookie
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        # 当 Access-Control-Allow-Credentials 为 true 时，需要指定允许的header key
        response.headers.add('Access-Control-Allow-Headers', 'content-type, accept, Access-Control-Allow-Origin')
        return response

    logger.info(app.url_map)

    return app


application = get_application()


def main():
    application.run(debug=IS_DEBUG, port=7777, host='0.0.0.0')
