from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jiang147852@localhost/db_pear'
db = SQLAlchemy(app)
from pear_web.handlers import crawler, data_analyse
