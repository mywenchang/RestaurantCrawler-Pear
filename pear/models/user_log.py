# coding=utf-8

from sqlalchemy.sql import select, func

from pear.models.base import BaseDao
from pear.models.tables import user_log


class UserLogDao(BaseDao):

    @classmethod
    def get_by_user(cls, u_id, page=-1, per_page=20):
        sql = select([user_log]).where(user_log.c.user_id == u_id)
        count_sql = select([func.count(user_log.c.id)]).where(user_log.c.user_id == u_id)
        return cls.get_list(sql, page=page, per_page=per_page, count_sql=count_sql)

    @classmethod
    def create(cls, u_id, action_name, action_args=None):
        sql = user_log.insert().values(
            user_id=u_id,
            action_name=action_name,
            action_args=action_args)
        return cls.insert(sql)

    @classmethod
    def wrap_item(cls, item):
        return {
            'id': item.id,
            'user_id': item.user_id,
            'action_name': item.action_name,
            'action_args': item.action_args
        }
