# coding=utf-8

from sqlalchemy import select, func
from sqlalchemy.sql import and_

from pear.models.base import BaseDao
from pear.models.tables import rate


class RateDao(BaseDao):

    @classmethod
    def create(cls, restaurant_crawler_id, rating_id, rating_start, rated_at, rating_text, time_spent_desc, food_id, food_name, food_star, food_rate, restaurant_id):
        sql = rate.insert().values(
            restaurant_crawler_id=restaurant_crawler_id,
            rating_id=rating_id,
            rating_start=rating_start,
            rated_at=rated_at,
            rating_text=rating_text,
            time_spent_desc=time_spent_desc,
            food_id=food_id, food_name=food_name, food_star=food_star, food_rate=food_rate,
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
        count_sql = select([func.count(rate.c.id)]).where(
            and_(
                rate.c.restaurant_crawler_id == restaurant_crawler_id,
                rate.c.restaurant_id == restaurant_id
            ))
        if rating_start > 0:
            sql = sql.where(rate.c.rating_start == rating_start)
            count_sql.where(rate.c.rating_start == restaurant_id)
        return cls.get_list(sql, page, per_page, count_sql)

    @classmethod
    def get_by_crawler_id(cls, crawler_id, page=1, per_page=20):
        sql = select([rate]).where(rate.c.restaurant_crawler_id == crawler_id)
        count_sql = select([func.count(rate.c.id)]).where(rate.c.restaurant_crawler_id == crawler_id)
        return cls.get_list(sql, page, per_page, count_sql)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None
        return {
            'id': item.id,
            'rating_id': item.rating_id,
            'rating_start': item.rating_start,
            'rated_at': item.rated_at,
            'rating_text': item.rating_text,
            'time_spent_desc': item.time_spent_desc,
            'restaurant_id': item.restaurant_id,
            'restaurant_crawler_id': item.restaurant_crawler_id,
            'food_id': item.food_id,
            'food_name': item.food_name,
            'food_star': item.food_star,
            'food_rate': item.food_rate,
            'key': item.id
        }
