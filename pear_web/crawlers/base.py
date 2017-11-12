# coding=utf-8
import json
from datetime import datetime

from pear_web import db
from pear_web.models.crawler import Crawler
from pear_web.utils.const import Crawler_Status


class BaseCrawler(object):
    def __init__(self, args):
        super(BaseCrawler, self).__init__()
        args = json.dumps(args)
        crawler = Crawler(created=datetime.now(), args=args)
        db.session.add(crawler)
        db.session.commit()
        self.crawler = crawler

    def crawl(self):
        raise NotImplemented

    def done(self, total):
        """
        爬虫任务结束
        :param total: 爬取到的总数据
        """
        self.crawler.status = Crawler_Status.DONE
        self.crawler.total = total
        self.crawler.finished = datetime.now()
        db.session.commit()

    def error(self, info):
        self.crawler.status = Crawler_Status.Error
        self.crawler.finished = datetime.now()
        self.crawler.info = info
        db.session.commit()

    def insert_extras(self, extras):
        self.crawler.extras = json.dumps(extras)
        db.session.commit()

    def update_count(self, count):
        """
        更新当前已经爬取的数据量
        :param count: 当前爬取到的数据量
        """
        self.crawler.data_count = count
        db.session.commit()
