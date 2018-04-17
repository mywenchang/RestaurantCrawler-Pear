# coding=utf-8
from sqlalchemy import func

from pear.models.base import BaseDao
from pear.models.tables import ele_dish
from sqlalchemy.sql import select


class EleDishDao(BaseDao):

    @classmethod
    def create(cls, food_id, restaurant_id, name, rating, moth_sales, rating_count, price, crawler_id):
        sql = ele_dish.insert().values(
            food_id=food_id,
            restaurant_id=restaurant_id,
            name=name,
            rating=rating,
            moth_sales=moth_sales,
            rating_count=rating_count,
            price=price,
            crawler_id=crawler_id
        )
        return cls.insert(sql)

    @classmethod
    def get_by_crawler_id(cls, crawler_id, page=1, per_page=20):
        sql = select([ele_dish]).where(
            ele_dish.c.crawler_id == crawler_id
        )
        count_sql = select([func.count(ele_dish.c.id)]).where(ele_dish.c.crawler_id == crawler_id)
        return cls.get_list(sql, page, per_page, count_sql)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None
        return {
            "food_id": item.food_id,
            "restaurant_id": item.restaurant_id,
            "name": item.name,
            "rating": item.rating,
            "moth_sales": item.moth_sales,
            "rating_count": item.rating_count,
            "price": item.price,
            "crawler_id": item.crawler_id
        }
