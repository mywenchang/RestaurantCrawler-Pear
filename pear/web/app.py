# coding=utf-8

import logging
import os

from flask import Flask

app = Flask(__name__)
logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s', level=logging.INFO)


@app.route("/check_health", methods=["GET"])
def check_health():
    return 'OK'


def install_modules():
    from pear.web.handlers.handler_dashboard import dashboard_router
    from pear.web.handlers.handler_user import user_router
    from pear.web.handlers.handler_crawler import crawlers_router
    from pear.web.handlers.handler_authorize import authorize_router
    app.register_blueprint(dashboard_router)
    app.register_blueprint(user_router)
    app.register_blueprint(crawlers_router)
    app.register_blueprint(authorize_router)


def init_app():
    install_modules()
    app.secret_key = "pear_web_secret_key"
    return app


def main():
    init_app()
    is_debug = os.getenv('is_debug', False)
    app.run(debug=is_debug)
