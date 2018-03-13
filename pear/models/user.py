# coding=utf-8

from datetime import datetime
from pear.models.tables import engine, user
from sqlalchemy import select, or_


class UserDao(object):
    conn = engine.connect()

    @classmethod
    def get_by_id(cls, u_id):
        sql = select([user]).where(user.c.id == u_id)
        return cls.conn.execute(sql).first()

    @classmethod
    def is_exist(cls, name=None, email=None, mobile=None):
        sql = select([user])
        if name:
            sql = sql.where(user.c.name == name)
        if email:
            sql = sql.where(user.c.email == email)
        if mobile:
            sql = sql.where(user.c.mobile == mobile)
        return cls.conn.execute(sql).first()

    @classmethod
    def get_by_args(cls, passwd, account=None):
        sql = select([user]).where(user.c.passwd == passwd)
        if account:
            sql = sql.where(
                or_(
                    user.c.name == account,
                    user.c.mobile == account,
                    user.c.email == account
                )
            )
        return cls.conn.execute(sql).first()

    @classmethod
    def create(cls, name, passwd, email, mobile):
        sql = user.insert().values(
            name=name,
            passwd=passwd,
            created=datetime.now()
        )
        if email:
            sql = sql.values(email=email)
        if mobile:
            sql = sql.values(mobile=mobile)
        return cls.conn.execute(sql).inserted_primary_key[0]
