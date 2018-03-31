# coding=utf-8

import logging
import os

from flask import Flask, request, send_file
from flask_swagger_ui import get_swaggerui_blueprint

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s', level=logging.INFO)
SWAGGER_URL = '/doc'
SWAGGER_API_LOCATION = './swagger.yaml'


def install_modules(app):
    from pear.web.handlers.handler_dashboard import dashboard_router
    from pear.web.handlers.handler_user import user_router
    from pear.web.handlers.handler_crawler import crawlers_router
    from pear.web.handlers.handler_authorize import authorize_router
    app.register_blueprint(dashboard_router)
    app.register_blueprint(user_router)
    app.register_blueprint(crawlers_router)
    app.register_blueprint(authorize_router)
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_API_LOCATION,
                                                   config={'app_name': u'数据分析后台接口文档'})
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def get_application():
    app = Flask(__name__)
    install_modules(app)
    app.secret_key = "pear_web_secret_key"

    @app.route("/check_health", methods=["GET"])
    def check_health():
        return 'OK'

    @app.route('/doc/swagger.yaml')
    def swagger_doc():
        return send_file('static/swagger.yaml')

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
        response.headers.add('Access-Control-Allow-Headers', 'content-type, accept')
        return response

    return app


application = get_application()


def main():
    is_debug = os.getenv('is_debug', False)
    application.run(debug=is_debug, port=9999)
