# coding=utf-8
import json

from datetime import datetime
from sqlalchemy import select

from pear.models.base import BaseDao
from pear.models.tables import analyse_task_table as table
from pear.utils.logger import logger


class AnalyseTaskDao(BaseDao):

    @classmethod
    def create(cls, u_id, data, crawler_one, crawler_two, _type):
        sql = table.insert().values(
            user_id=u_id,
            created=datetime.now(),
            data=data,
            crawler_id_one=crawler_one,
            crawler_id_two=crawler_two,
            type=_type
        )
        return cls.insert(sql)

    @classmethod
    def batch_get_by_u_id(cls, u_id, _type=None, crawler_one=None, crawler_two=None):
        sql = select([table]).where(table.c.user_id == u_id)
        if _type:
            sql = sql.where(
                table.c.type == _type
            )
        if crawler_one:
            sql = sql.where(
                table.c.crawler_id_one == crawler_one
            )
        if crawler_two:
            sql = sql.where(
                table.c.crawler_id_two == crawler_two
            )
        sql = sql.order_by(table.c.id.desc())
        return cls.get_list(sql)

    @classmethod
    def get_by_u_id(cls, u_id, _type=None, crawler_one=None, crawler_two=None):
        sql = select([table]).where(table.c.user_id == u_id)
        if _type:
            sql = sql.where(
                table.c.type == _type
            )
        if crawler_one:
            sql = sql.where(
                table.c.crawler_id_one == crawler_one
            )
        if crawler_two:
            sql = sql.where(
                table.c.crawler_id_two == crawler_two
            )
        sql = sql.order_by(table.c.id.desc())
        return cls.get_one(sql)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None

        def load_data():
            try:
                data = json.loads(item.data)
            except Exception as e:
                logger.error(e)
                return None
            else:
                return data

        return {
            'id': item.id,
            'key': item.id,
            'user_id': item.user_id,
            'created': item.created.strftime('%Y-%m-%d %H:%M:%S'),
            'data': load_data(),
            'crawler_one': item.crawler_id_one,
            'crawler_two': item.crawler_id_two,
            'type': item.type
        }
