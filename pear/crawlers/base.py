# coding=utf-8
import json
import logging

from datetime import datetime
from pear.models.crawler import CrawlerDao
from pear.utils.const import Crawler_Status

logger = logging.getLogger('')


class BaseCrawler(object):
    def __init__(self, source, c_type, cookies, args):
        self.cookies = cookies
        self.u_id = cookies.get('u_id')
        self.id = CrawlerDao.create(self.u_id, source, c_type, args=json.dumps(args))

    def crawl(self):
        raise NotImplemented

    def done(self, total):
        CrawlerDao.update_by_id(self.id, self.u_id, status=Crawler_Status.DONE, total=total, finished=datetime.now())

    def error(self, info):
        CrawlerDao.update_by_id(self.id, self.u_id, status=Crawler_Status.Error, info=info, finished=datetime.now())
        logger.error(info)

    def insert_extras(self, extras):
        CrawlerDao.update_by_id(self.id, self.u_id, extras=extras)

    def update_count(self, count):
        CrawlerDao.update_by_id(self.id, self.u_id, data_count=count)

    def __str__(self):
        return "crawler-{}".format(self.id)
