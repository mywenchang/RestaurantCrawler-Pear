# coding=utf-8

from flask import Flask

app = Flask(__name__)


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
    app.run(debug=True)
