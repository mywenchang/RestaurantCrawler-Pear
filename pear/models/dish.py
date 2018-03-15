# coding=utf-8

from pear.models.base import BaseDao
from pear.models.tables import dish


class DishDao(BaseDao):

    @classmethod
    def create(cls, restaurant_id, name, rating, moth_sales, rating_count, crawler_id):
        sql = dish.insert().values(
            restaurant_id=restaurant_id,
            name=name,
            rating=rating,
            moth_sales=moth_sales,
            rating_count=rating_count,
            crawler_id=crawler_id
        )
        cls.insert(sql)

    @classmethod
    def wrap_item(cls, item):
        return {
            "restaurant_id": item.restaurant_id,
            "name": item.name,
            "rating": item.rating,
            "moth_sales": item.moth_sales,
            "rating_count": item.rating_count,
            "crawler_id": item.crawler_id
        }
