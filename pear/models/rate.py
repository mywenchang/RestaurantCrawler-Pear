# coding=utf-8

from sqlalchemy import select

from pear.models.base import BaseDao
from pear.models.tables import rate
from sqlalchemy.sql import and_


class RateDao(BaseDao):

    @classmethod
    def create(cls, restaurant_crawler_id, rating_start, rated_at, rating_text, time_spent_desc, restaurant_id):
        sql = rate.insert().values(
            restaurant_crawler_id=restaurant_crawler_id,
            rating_start=rating_start,
            rated_at=rated_at,
            rating_text=rating_text,
            time_spent_desc=time_spent_desc,
            restaurant_id=restaurant_id
        )
        return cls.insert(sql)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_crawler_id, restaurant_id, rating_start=-1, page=1, per_page=20):
        sql = select([rate]).where(
            and_(
                rate.c.restaurant_id == restaurant_id,
                rate.c.restaurant_crawler_id == restaurant_crawler_id
            )
        )
        if rating_start > 0:
            sql = sql.where(
                rate.c.rating_start == rating_start
            )
        return cls.get_list(sql, page, per_page)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None
        return {
            'id': item.id,
            'rating_start': item.rating_start,
            'rated_at': item.rated_at,
            'rating_text': item.rating_text,
            'time_spent_desc': item.time_spent_desc,
            'restaurant_id': item.restaurant_id,
            'restaurant_crawler_id': item.restaurant_crwaler_id
        }
