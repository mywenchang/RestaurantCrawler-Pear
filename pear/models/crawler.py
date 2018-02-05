# coding=utf-8

from datetime import datetime
from sqlalchemy import update, select

from pear.models.tables import crawler, engine
from pear.utils.const import Crawler_Status


class CrawlerDao(object):
    conn = engine.connect()

    @classmethod
    def create(cls, args, info=None, extra=None):
        sql = crawler.insert().values(
            status=Crawler_Status.Crawling,
            created=datetime.now()
        )
        if args is not None:
            sql = sql.insert().values(args=args)
        if extra is not None:
            sql = sql.insert().values(extra=extra)
        return cls.conn.execute(sql)

    @classmethod
    def update_by_id(cls, crawler_id, status=None, total=None, finished=None):
        sql = update(crawler).where(crawler.c.id == crawler_id)
        if status is not None:
            sql = sql.values(status=status)
        if total is not None:
            sql = sql.values(total=total)
        if finished is not None:
            sql = sql.values(finished=finished)
        cls.conn.execute(sql)

    @classmethod
    def get_by_id(cls, crawler_id, status=None):
        sql = select(crawler).where(crawler.c.id == crawler_id)
        if status is not None:
            sql = sql.where(crawler.c.status == status)
        return cls.conn.execute(sql)
