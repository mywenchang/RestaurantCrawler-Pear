# coding=utf-8

from datetime import datetime
from sqlalchemy import select, or_

from pear.models.base import BaseDao
from pear.models.tables import user


class UserDao(BaseDao):

    @classmethod
    def get_by_id(cls, u_id):
        sql = select([user]).where(user.c.id == u_id)
        return cls.get_one(sql)

    @classmethod
    def is_exist(cls, name=None, email=None, mobile=None):
        sql = select([user])
        if name:
            sql = sql.where(or_(user.c.name == name))
        if email:
            sql = sql.where(or_(user.c.email == email))
        if mobile:
            sql = sql.where(or_(user.c.mobile == mobile))
        return cls.get_one(sql)

    @classmethod
    def get_by_args(cls, password, account=None):
        sql = select([user]).where(user.c.passwd == password)
        if account is None:
            return None
        if account:
            sql = sql.where(
                or_(
                    user.c.name == account,
                    user.c.mobile == account,
                    user.c.email == account
                )
            )
        return cls.get_one(sql)

    @classmethod
    def create(cls, name, password, email, mobile):
        sql = user.insert().values(
            name=name,
            passwd=password,
            created=datetime.now()
        )
        if email:
            sql = sql.values(email=email)
        if mobile:
            sql = sql.values(mobile=mobile)
        return cls.insert(sql)

    @classmethod
    def delete(cls, id):
        sql = user.delete().where(user.c.id == id)
        return cls.update(sql)

    @classmethod
    def add_visitor_count(cls, u_id):
        count = cls.get_by_id(u_id)['visitor_count']
        sql = user.update().where(user.c.id == u_id).values(
            visitor_count=count + 1
        )
        return cls.update(sql)

    @classmethod
    def wrap_item(cls, item):
        if not item:
            return None
        return {
            'name': item.name,
            'mobile': item.mobile,
            'email': item.email,
            'id': item.id,
            'visitor_count': item.visitor_count
        }
