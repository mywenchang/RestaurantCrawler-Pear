# coding=utf-8

from sqlalchemy import select

from pear.models.base import BaseDao
from pear.models.tables import rate


class RateDao(BaseDao):

    @classmethod
    def create(cls, rating_start, rated_at, rating_text, time_spent_desc, restaurant_id):
        sql = rate.insert().values(
            rating_start=rating_start,
            rated_at=rated_at,
            rating_text=rating_text,
            time_spent_desc=time_spent_desc,
            restaurant_id=restaurant_id
        )
        return cls.insert(sql)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id, rating_start=-1, page=1, per_page=20):
        sql = select([rate]).where(
            rate.c.restaurant_id == restaurant_id
        )
        if rating_start > 0:
            sql = sql.where(
                rate.c.rating_start == rating_start
            )
        return cls.get_list(sql, page, per_page)

    @classmethod
    def wrap_item(cls, item):
        return {
            'id': item.id,
            'rating_start': item.rating_start,
            'rated_at': item.rated_at,
            'rating_text': item.rating_text,
            'time_spent_desc': item.time_spent_desc,
            'restaurant_id': item.restaurant_id
        }
