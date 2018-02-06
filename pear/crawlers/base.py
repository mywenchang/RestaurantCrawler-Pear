# coding=utf-8

from datetime import datetime
from pear.models.crawler import CrawlerDao
from pear.utils.const import Crawler_Status


class BaseCrawler(object):
    def __init__(self, args):
        self.id = CrawlerDao.create(args=args)

    def crawl(self):
        raise NotImplemented

    def done(self, total):
        """
        爬虫任务结束
        :param total: 爬取到的总数据
        """
        CrawlerDao.update_by_id(self.id, status=Crawler_Status.DONE, total=total, finished=datetime.now())

    def error(self, info):
        pass

    def insert_extras(self, extras):
        pass

    def update_count(self, count):
        """
        更新当前已经爬取的数据量
        :param count: 当前爬取到的数据量
        """
        CrawlerDao.update_by_id(self.id, total=count)
