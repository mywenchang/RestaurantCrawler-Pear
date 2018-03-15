# coding=utf-8

from pear.models.tables import engine


class BaseDao(object):
    conn = engine.connect()

    @classmethod
    def insert(cls, sql):
        return cls.conn.execute(sql).inserted_primary_key[0]

    @classmethod
    def update(cls, sql):
        cls.conn.execute(sql)

    @classmethod
    def get_one(cls, sql):
        return cls.__wrap_item(cls.conn.execute(sql).first())

    @classmethod
    def get_list(cls, sql, page, per_page):
        sql = sql.limit(per_page).offset((page - 1) * per_page)
        return [cls.__wrap_item(item) for item in cls.conn.execute(sql).fetchall()]

    @classmethod
    def __wrap_item(cls, item):
        """
        wrap sqlalchemy.engine.result.RowProxy -> dict
        :param item: sqlalchemy.engine.result.RowProxy
        :return: dict
        """
        raise NotImplementedError
