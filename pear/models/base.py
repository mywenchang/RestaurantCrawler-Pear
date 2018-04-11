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
        return cls.wrap_item(cls.conn.execute(sql).first())

    @classmethod
    def get_list(cls, sql, page, per_page, count_sql=None):
        sql = sql.limit(per_page).offset((page - 1) * per_page)
        result = [cls.wrap_item(item) for item in cls.conn.execute(sql).fetchall()]
        count = 0
        if count_sql is not None:
            count = cls.conn.execute(count_sql).fetchone()[0]
        return result, count

    @classmethod
    def wrap_item(cls, item):
        """
        wrap sqlalchemy.engine.result.RowProxy -> dict
        :param item: sqlalchemy.engine.result.RowProxy
        :return: dict
        """
        raise NotImplementedError
