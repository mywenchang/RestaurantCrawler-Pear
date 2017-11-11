# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SqlAlchemy配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jiyang147852@localhost/db_pear'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from pear_web.handlers import crawler, data_analyse
