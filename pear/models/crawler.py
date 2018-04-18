# coding=utf-8

import json
from datetime import datetime
from sqlalchemy import update, select, and_, func

from pear.models.base import BaseDao
from pear.models.tables import crawler
from pear.utils.const import Crawler_Status


class CrawlerDao(BaseDao):

    @classmethod
    def create(cls, u_id, type, args, info=None, extras=None):
        sql = crawler.insert().values(
            status=Crawler_Status.Crawling,
            created=datetime.now(),
            u_id=u_id,
            type=type
        )
        if args is not None:
            sql = sql.values(args=args)
        if extras is not None:
            sql = sql.values(extras=extras)
        if info is not None:
            sql = sql.values(info=info)
        return cls.insert(sql)

    @classmethod
    def update_by_id(cls, crawler_id, u_id, status=None, data_count=None, total=None, finished=None, info=None,
                     extras=None):
        sql = update(crawler).where(and_(crawler.c.id == crawler_id, crawler.c.u_id == u_id))
        if status:
            sql = sql.values(status=status)
        if data_count:
            sql = sql.values(data_count=data_count)
        if total:
            sql = sql.values(total=total)
        if finished:
            sql = sql.values(finished=finished)
        if info:
            sql = sql.values(info=info)
        if extras:
            sql = sql.values(extras=extras)
        cls.update(sql)

    @classmethod
    def get_by_id(cls, crawler_id, u_id, status=None):
        sql = select([crawler]).where(and_(crawler.c.id == crawler_id, crawler.c.u_id == u_id))
        if status:
            sql = sql.where(crawler.c.status == status)
        return cls.get_one(sql)

    @classmethod
    def batch_get_by_status(cls, u_id, page=1, per_page=20, status=None):
        sql = select([crawler]).where(crawler.c.u_id == u_id).order_by(crawler.c.id.asc())
        count_sql = select([func.count(crawler.c.id)]).where(crawler.c.u_id == u_id)
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
        return {
            'id': item.id,
            'status': item.status,
            'created': item.created.strftime('%Y-%d-%m %H:%M:%S'),
            'finished': item.finished.strftime('%Y-%d-%m %H:%M:%S') if item.finished else '',
            'args': json.loads(item.args) if item.args else None,
            'info': item.info,
            'extras': item.extras,
            'total': item.total,
            'count': item.data_count,
            'type': item.type
        }
