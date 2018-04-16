# coding=utf-8

import logging

from flask import Flask, request, jsonify

from pear.utils.config import IS_DEBUG

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s', level=logging.INFO)


def install_modules(app):
    from pear.web.handlers.handler_dashboard import dashboard_router
    from pear.web.handlers.handler_user import user_router
    from pear.web.handlers.handler_config_ele_crawler import config_ele_crawler_router
    from pear.web.handlers.handler_authorize import authorize_router
    from pear.web.handlers.handler_crawler_tasks import crawler_tasks_router
    app.register_blueprint(dashboard_router)
    app.register_blueprint(user_router)
    app.register_blueprint(config_ele_crawler_router)
    app.register_blueprint(authorize_router)
    app.register_blueprint(crawler_tasks_router)


def get_application():
    app = Flask(__name__)
    install_modules(app)
    app.secret_key = "pear_web_secret_key"

    @app.route("/")
    def index():
        return jsonify(status='ok')

    @app.before_request
    def before_request():
        logging.info('visitor: '.format(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))

    @app.after_request
    def after_request(response):
        # 允许跨域(Access-Control-Allow-Credentials 为 true 时，值不能为*，必须为指定的 protocol://host:port)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        # 和前端 fetch 的credentials选项配合，使其可以获取cookie
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        # 当 Access-Control-Allow-Credentials 为 true 时，需要指定允许的header key
        response.headers.add('Access-Control-Allow-Headers', 'content-type, accept, Access-Control-Allow-Origin')
        return response

    return app


application = get_application()


def main():
    application.run(debug=IS_DEBUG, port=9999, host='0.0.0.0')
