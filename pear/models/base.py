# coding=utf-8

from pear.models.tables import engine
from pear.utils.logger import logger


class BaseDao(object):
    __conn = engine.connect()

    @classmethod
    def insert(cls, sql):
        return cls.__conn.execute(sql).inserted_primary_key[0]

    @classmethod
    def update(cls, sql):
        result_proxy = cls.__conn.execute(sql)
        result_proxy.close()

    @classmethod
    def get_one(cls, sql):
        result = cls.__conn.execute(sql)
        if result.returns_rows:
            return cls.wrap_item(result.first())
        result.close()
        return None

    @classmethod
    def get_list(cls, sql, page, per_page, count_sql=None):
        if page != -1:
            sql = sql.limit(per_page).offset((page - 1) * per_page)
        result_proxy = cls.__conn.execute(sql)
        result = [cls.wrap_item(item) for item in result_proxy.fetchall()]
        result_proxy.close()
        count = 0
        if count_sql is not None:
            result_proxy = cls.__conn.execute(count_sql)
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

    @classmethod
    def close_conn(cls):
        logger.info('close database connect')
        cls.__conn.close()
