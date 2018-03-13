# coding=utf-8

from datetime import datetime
from sqlalchemy import select, and_

from pear.models.tables import engine, user


class UserDao(object):
    conn = engine.connect()

    @classmethod
    def get_by_id(cls, u_id):
        sql = select([user]).where(user.c.id == u_id)
        return cls.conn.execute(sql).first()

    @classmethod
    def get_by_args(cls, passwd, name=None, email=None, moible=None):
        sql = select([user]).where(user.c.passwd == passwd)
        if name:
            sql = sql.where(and_(
                user.c.name == name
            ))
        if email:
            sql = sql.where(and_(user.c.email == email))
        if moible:
            sql = sql.where(and_(user.c.mobile == moible))
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
