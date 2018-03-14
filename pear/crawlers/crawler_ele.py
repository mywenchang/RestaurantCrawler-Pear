# coding=utf-8
import json
import logging

import requests

from pear.crawlers.base import BaseCrawler
from pear.utils.const import Source

logger = logging.getLogger('')


class CrawlEleRestaurants(BaseCrawler):
    def __init__(self, u_id, args=None):
        super(CrawlEleRestaurants, self).__init__(u_id, args)
        self.url = 'https://www.ele.me/restapi/shopping/restaurants'
        self.page_size = 24
        self.page_offset = 0
        self.latitude = 30.64995
        self.longitude = 104.18755
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
        self.sign = '1509166638215'
        self.geohash = 'wm6n6gehcuu'
        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "loc={},{}".format(self.longitude, self.latitude),
            'user-agent': self.user_agent,
            'referer': self.referer,
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache"
        }
        if args:
            args = json.loads(args)
            if args.get('latitude'):
                self.latitude = args.get('latitude')
            if args.get('longitude'):
                self.longitude = args.get('longitude')
            if args.get('user-agent'):
                self.user_agent = args.get('user_agent')
            if args.get('sign'):
                self.sign = args.get('sign')
            if args.get('geohash'):
                self.geohash = args.get('geohash')
            if args.get('cookies'):
                self.cookies = args.get('cookies',
                                        {'USERID': '274692274', 'SID': 'DJPjUIwmk1bLeowGPT6y3msqlNn4kKhJHWLA'})
            if args.get('headers'):
                self.headers.update(args.get('headers'))
        self.referer = "https://www.ele.me/place/{}?latitude={}&longitude={}".format(self.geohash, self.latitude,
                                                                                     self.longitude)
        self.querystring = {"geohash": self.geohash,
                            "latitude": self.latitude,
                            "limit": self.page_size,
                            "longitude": self.longitude,
                            "offset": self.page_offset,
                            "sign": self.sign,
                            "terminal": "web"}
        extras = {
            "headers": self.headers,
            "query": self.querystring
        }
        self.insert_extras(json.dumps(extras))

    def crawl(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring,
                                    cookies=self.cookies)
        if response.status_code != requests.codes.ok:
            self.error(json.dumps(response.json()))
            self.done(self.page_offset)
            return
        data = response.json()
        for item in data:
            restaurant_id = item.get('id'),
            name = item.get('name'),
            source = Source.ELE,
            arrive_time = item.get('order_lead_time'),
            start_fee = item.get('float_minimum_order_amount'),
            send_fee = item.get('float_delivery_fee'),
            score = item.get('rating'),
            sales = item.get('recent_order_num'),
            latitude = item.get('latitude'),
            longitude = item.get('longitude')
            # TODO insert into db

        # 递归查询直到没有数据
        data_size = len(data)
        logger.info('crawler page offset:{}'.format(self.page_offset))
        logger.info('crawler data size:{}'.format(data_size))
        if data_size < 1:
            self.done(self.page_offset)
            return
        self.page_offset += data_size
        self.querystring['offset'] = self.page_offset
        self.update_count(self.page_offset)
        self.crawl()


class CrawlEleDishes(BaseCrawler):
    def __init__(self, u_id, args):
        super(CrawlEleDishes, self).__init__(u_id, args)
        self.url = 'https://www.ele.me/restapi/shopping/v2/menu'
        self.restaurant_id = args.get('restaurant_id')
        self.latitude = args.get('latitude')
        self.longitude = args.get('longitude')
        self.querystring = {"restaurant_id": self.restaurant_id}

        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "shopid={};loc={},{}".format(self.restaurant_id, self.latitude, self.longitude),
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
            'referer': "https://www.ele.me/shop/{}".format(self.restaurant_id),
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache",
        }

        extras = {
            'headers': self.headers,
            'query': self.querystring
        }
        self.insert_extras(extras)

    def crawl(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        if response.status_code != requests.codes.ok:
            self.error('response code != 200')
            return
        dishes = response.json()
        total = 0
        for item in dishes:
            foods = item.get('foods')
            for item in foods:
                # dish = Dish(
                #     name=item.get('name'),
                #     restaurant_id=item.get('restaurant_id'),
                #     rating=item.get('rating'),
                #     month_sales=item.get('month_sales'),
                #     rating_count=item.get('rating_count')
                # )
                # db.session.add(dish)
                total += 1
                self.update_count(total)
                # db.session.commit()
        self.done(total)
