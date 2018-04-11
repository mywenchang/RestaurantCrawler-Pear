# coding=utf-8
from sqlalchemy import Table, create_engine, MetaData

from pear.utils.config import MYSQL_CONFIG, IS_DEBUG

engine = create_engine(MYSQL_CONFIG, echo=IS_DEBUG)
metadata = MetaData(bind=engine)

crawler = Table('crawler', metadata, autoload=True)
dish = Table('dish', metadata, autoload=True)
restaurant = Table('restaurant', metadata, autoload=True)
user = Table('user', metadata, autoload=True)
rate = Table('rate', metadata, autoload=True)
