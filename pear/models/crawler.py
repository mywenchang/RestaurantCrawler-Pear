# coding=utf-8

from datetime import datetime
from sqlalchemy import update, select, delete, and_

from pear.models.tables import crawler, engine
from pear.utils.const import Crawler_Status


class CrawlerDao(object):
    conn = engine.connect()

    @classmethod
    def create(cls, u_id, args, info=None, extra=None):
        sql = crawler.insert().values(
            status=Crawler_Status.Crawling,
            created=datetime.now(),
            u_id=u_id
        )
        if args is not None:
            sql = sql.values(args=args)
        if extra is not None:
            sql = sql.values(extra=extra)
        return cls.conn.execute(sql).inserted_primary_key[0]

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
        cls.conn.execute(sql)

    @classmethod
    def get_by_id(cls, crawler_id, u_id, status=None):
        sql = select([crawler]).where(and_(crawler.c.id == crawler_id, crawler.c.u_id == u_id))
        if status:
            sql = sql.where(crawler.c.status == status)
        return cls._wrap_result(cls.conn.execute(sql).first())

    @classmethod
    def batch_get_by_status(cls, u_id, page=1, per_page=20, status=None):
        sql = select([crawler]).where(crawler.c.u_id == u_id)
        sql = sql.limit(per_page).offset((page - 1) * per_page).order_by(crawler.c.id.asc())
        if status:
            sql = sql.where(crawler.c.status == status)
        return [cls._wrap_result(item) for item in cls.conn.execute(sql).fetchall()]

    @classmethod
    def delete(cls, crawler_ids, u_id):
        if isinstance(crawler_ids, list):
            sql = delete([crawler]).where(crawler.c.id in crawler_ids)
        else:
            sql = delete([crawler]).where(crawler.c.id == crawler_ids)
        sql = sql.where(crawler.c.u_id == u_id)
        cls.conn.execute(sql)

    @classmethod
    def _wrap_result(cls, item):
        return {
            'id': item.id,
            'status': item.status,
            'created': item.created.strftime('%Y-%d-%m %H:%M:%S'),
            'finished': item.finished.strftime('%Y-%d-%m %H:%M:%S') if item.finished else '',
            'args': item.args,
            'info': item.info,
            'extras': item.extras,
            'total': item.total,
            'count': item.data_count
        }
