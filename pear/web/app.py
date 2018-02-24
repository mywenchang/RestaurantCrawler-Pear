# coding=utf-8

import logging

from flask import Flask

from pear.utils.config import IS_DEBUG

app = Flask(__name__)
logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s', level=logging.INFO)


@app.route("/", methods=["GET"])
def check_health():
    return 'OK'


def install_modules(app):
    from pear.web.handlers.crawler import crawlers_router
    from pear.web.handlers.data_analyse import data_router
    app.register_blueprint(crawlers_router)
    app.register_blueprint(data_router)


def init_app():
    install_modules(app)
    return app


def main():
    init_app()
    app.logger.info('e12')
    app.run(debug=IS_DEBUG)
