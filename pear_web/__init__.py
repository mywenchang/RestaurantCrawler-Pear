from flask import Flask

app = Flask(__name__)

from pear_web.handlers import crawler, data_analyse
