# coding=utf-8
from pear_web import db


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    restaurant_id = db.Column(db.Integer)  # 所属商家
    rating = db.Column(db.Float)  # 评分
    month_sales = db.Column(db.Integer)  # 月销量
    rating_count = db.Column(db.Integer)  # 月评价数

    def __init__(self, name=None, restaurant_id=None, rating=None, month_sales=None, rating_count=None):
        self.name = name
        self.restaurant_id = restaurant_id
        self.rating = rating
        self.month_sales = month_sales
        self.rating_count = rating_count
