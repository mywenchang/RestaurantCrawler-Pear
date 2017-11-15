# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pear_web.utils.confg import config

app = Flask(__name__)

# SqlAlchemy配置
mysql_conf = config['mysql']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(
    user=mysql_conf['user'], password=mysql_conf['password'], host=mysql_conf['host'], database=mysql_conf['database'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from pear_web.handlers import crawler, data_analyse
