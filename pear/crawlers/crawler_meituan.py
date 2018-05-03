# coding=utf-8

from pear.crawlers.base import BaseCrawler


class CrawlerMeiTuanRestaurant(BaseCrawler):

    def __init__(self, source, c_type, restaurant_id, cookies, args):
        super(CrawlerMeiTuanRestaurant, self).__init__(source, c_type, restaurant_id, cookies, args)
