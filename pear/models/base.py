# coding=utf-8

from pear.models.tables import engine


class BaseDao(object):

    @classmethod
    def insert(cls, sql):
        result_proxy = engine.connect().execute(sql)
        primary_key = result_proxy.inserted_primary_key[0]
        result_proxy.close()
        return primary_key

    @classmethod
    def update(cls, sql):
        result_proxy = engine.connect().execute(sql)
        result_proxy.close()

    @classmethod
    def get_one(cls, sql):
        result = engine.connect().execute(sql)
        data = None
        if result.returns_rows:
            data = cls.wrap_item(result.first())
        result.close()
        return data

    @classmethod
    def get_list(cls, sql, page, per_page, count_sql=None):
        if page != -1:
            sql = sql.limit(per_page).offset((page - 1) * per_page)
        result_proxy = engine.connect().execute(sql)
        result = [cls.wrap_item(item) for item in result_proxy.fetchall()]
        result_proxy.close()
        count = 0
        if count_sql is not None:
            result_proxy = engine.connect().execute(count_sql)
            count = result_proxy.fetchone()[0]
            result_proxy.close()
        return result, count

    @classmethod
    def wrap_item(cls, item):
        """
        wrap sqlalchemy.engine.result.RowProxy -> dict
        :param item: sqlalchemy.engine.result.RowProxy
        :return: dict
        """
        raise NotImplementedError
