# coding=utf-8
from sqlalchemy import Table, create_engine, MetaData
from pear.utils.config import MYSQL_CONFIG

engine = create_engine(MYSQL_CONFIG, convert_unicode=True, echo=False)
metadata = MetaData(bind=engine)

crawler = Table('crawler', metadata, autoload=True)
dish = Table('dish', metadata, autoload=True)
restaurant = Table('restaurant', metadata, autoload=True)
