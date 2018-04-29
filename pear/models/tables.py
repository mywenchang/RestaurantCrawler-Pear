# coding=utf-8
from sqlalchemy import Table, create_engine, MetaData

from pear.utils.config import MYSQL_CONFIG, IS_DEBUG

engine = create_engine(MYSQL_CONFIG, echo=False)
metadata = MetaData(bind=engine)

crawler = Table('crawler', metadata, autoload=True)
user = Table('user', metadata, autoload=True)
ele_dish = Table('ele_dish', metadata, autoload=True)
restaurant = Table('restaurant', metadata, autoload=True)
ele_rate = Table('ele_rate', metadata, autoload=True)
user_log = Table('user_log', metadata, autoload=True)
