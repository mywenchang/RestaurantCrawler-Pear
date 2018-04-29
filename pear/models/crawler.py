# coding=utf-8

from datetime import datetime
from sqlalchemy import update, select, and_, func

from pear.models.base import BaseDao
from pear.models.dish import EleDishDao
from pear.models.restaurant import RestaurantDao
from pear.models.tables import crawler
from pear.utils.const import Crawler_Status


class CrawlerDao(BaseDao):

    @classmethod
    def create(cls, u_id, restaurant_id, source, type, args=None, info=None, extras=None):
        sql = crawler.insert().values(
            status=Crawler_Status.Crawling,
            created=datetime.now(),
            u_id=u_id,
            restaurant_id=restaurant_id,
            type=type,
            source=source
        )
        if args is not None:
            sql = sql.values(args=args)
        if extras is not None:
            sql = sql.values(extras=extras)
        if info is not None:
            sql = sql.values(info=info)
        return cls.insert(sql)

    @classmethod
    def update_by_id(cls, crawler_id, u_id, status=None, data_count=None, finished=None, info=None, extras=None):
        sql = update(crawler).where(
            and_(crawler.c.id == crawler_id, crawler.c.u_id == u_id))
        if status:
            sql = sql.values(status=status)
        if data_count:
            sql = sql.values(data_count=data_count)
        if finished:
            sql = sql.values(finished=finished)
        if info:
            sql = sql.values(info=info)
        if extras:
            sql = sql.values(extras=extras)
        cls.update(sql)

    @classmethod
    def get_by_id(cls, crawler_id, u_id, status=None):
        sql = select([crawler]).where(
            and_(crawler.c.id == crawler_id, crawler.c.u_id == u_id))
        if status:
            sql = sql.where(crawler.c.status == status)
        return cls.get_one(sql)

    @classmethod
    def batch_get_by_status(cls, u_id, page=1, per_page=20, status=None):
        sql = select([crawler]).where(crawler.c.u_id ==
                                      u_id).order_by(crawler.c.id.desc())
        count_sql = select([func.count(crawler.c.id)]
                           ).where(crawler.c.u_id == u_id)
        if status is not None:
            sql = sql.where(crawler.c.status == status)
            count_sql = count_sql.where(crawler.c.status == status)
        return cls.get_list(sql, page, per_page, count_sql)

    @classmethod
    def delete(cls, crawler_ids, u_id):
        if isinstance(crawler_ids, list):
            sql = crawler.delete().where(crawler.c.id in crawler_ids)
        else:
            sql = crawler.delete().where(crawler.c.id == crawler_ids)
        sql = sql.where(crawler.c.u_id == u_id)
        cls.update(sql)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None
        restaurant = RestaurantDao.get_by_restaurant_id(item.restaurant_id)
        dishes, _ = EleDishDao.get_by_crawler_id(item.id)
        return {
            'id': item.id,
            'status': item.status if item.data_count > 0 else 2,
            'created': item.created.strftime('%Y-%m-%d %H:%M:%S'),
            'finished': item.finished.strftime('%Y-%m-%d %H:%M:%S') if item.finished else '',
            'args': item.args,
            'info': item.info,
            'extras': item.extras,
            'count': item.data_count,
            'restaurant': restaurant,
            'dishes': dishes,
            'type': item.type,
            'source': item.source,
            'key': item.id
        }
