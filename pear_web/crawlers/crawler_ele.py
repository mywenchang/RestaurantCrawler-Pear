# coding=utf-8

import requests

from pear_web.crawlers.base import BaseCrawler
from pear_web import db
from pear_web.models.dish import Dish
from pear_web.models.restaurant import Restaurant
from pear_web.utils.const import Source


class CrawlEleRestaurants(BaseCrawler):
    def __init__(self, args):
        super(CrawlEleRestaurants, self).__init__(args)
        self.url = 'https://www.ele.me/restapi/shopping/restaurants'
        self.page_size = 24
        self.page_offset = 0
        if args.get('extras'):
            self.latitude = args.get('extras').get('latitude', 30.64995)
            self.longitude = args.get('extras').get('longitude', 104.18755)
        else:
            self.latitude = '30.64995'
            self.longitude = '104.18755'
        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "loc={},{}".format(self.longitude, self.latitude),
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
            'referer': "https://www.ele.me/place/wm6n6gehcuu?latitude={}&longitude={}".format(self.latitude,
                                                                                              self.longitude),
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache",
        }
        self.querystring = {"geohash": "wm6n6gehcuu", "latitude": self.latitude, "limit": self.page_size,
                            "longitude": self.longitude, "offset": self.page_offset, "sign": "1509166638215",
                            "terminal": "web"}
        extras = {
            "headers": self.headers,
            "query": self.querystring
        }
        self.insert_extras(extras)

    def crawl(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        print self.querystring
        if response.status_code != requests.codes.ok:
            self.error('status_code != 200')
            return
        list = response.json()
        for item in list:
            restaurant = Restaurant(
                restaurant_id=item.get('id'),
                name=item.get('name'),
                source=Source.ELE,
                arrive_time=item.get('order_lead_time'),
                start_fee=item.get('float_minimum_order_amount'),
                send_fee=item.get('float_delivery_fee'),
                score=item.get('rating'),
                sales=item.get('recent_order_num'),
                latitude=item.get('latitude'),
                longitude=item.get('longitude')
            )
            db.session.add(restaurant)
        db.session.commit()
        # 递归查询直到没有数据
        data_size = len(list)
        if data_size < 1:
            self.done(self.page_offset)
            return
        self.page_offset += data_size
        self.querystring['offset'] = self.page_offset
        self.update_count(self.page_offset)
        self.crawl()


class CrawlEleDishes(BaseCrawler):
    def __init__(self, args):
        super(CrawlEleDishes, self).__init__(args)
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
                dish = Dish(
                    name=item.get('name'),
                    restaurant_id=item.get('restaurant_id'),
                    rating=item.get('rating'),
                    month_sales=item.get('month_sales'),
                    rating_count=item.get('rating_count')
                )
                db.session.add(dish)
                total += 1
                self.update_count(total)
            db.session.commit()
        self.done(total)
