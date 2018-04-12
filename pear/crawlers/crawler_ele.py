# coding=utf-8
import json
import logging

import requests

from pear.crawlers.base import BaseCrawler
from pear.models.dish import DishDao
from pear.models.rate import RateDao
from pear.models.restaurant import RestaurantDao
from pear.utils.const import SOURCE

logger = logging.getLogger('')


# 爬取商家
class CrawlEleRestaurant(BaseCrawler):
    def __init__(self, c_type, cookies, args=None):
        super(CrawlEleRestaurant, self).__init__(c_type, cookies, args)
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
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache"
        }
        self.cookies = cookies
        self.limit = -1
        if not args:
            args = {}
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
            self.cookies.update(args.get('cookies'))
        if args.get('headers'):
            self.headers.update(args.get('headers'))
        if args.get('limit'):
            self.limit = int(args.get('limit'))
        self.referer = "https://www.ele.me/place/{}?latitude={}&longitude={}".format(self.geohash, self.latitude,
                                                                                     self.longitude)
        self.headers['referer'] = self.referer
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
            source = SOURCE.ELE,
            arrive_time = item.get('order_lead_time'),
            start_fee = item.get('float_minimum_order_amount'),
            send_fee = item.get('float_delivery_fee'),
            score = item.get('rating'),
            sales = item.get('recent_order_num'),
            latitude = item.get('latitude'),
            longitude = item.get('longitude')
            RestaurantDao.create(restaurant_id, name, source, sales, arrive_time, start_fee, send_fee, score, latitude,
                                 longitude, self.id)

        # 递归查询直到没有数据
        data_size = len(data)
        if data_size < 1 or (0 < self.limit <= data_size):
            self.done(self.page_offset)
            return
        self.page_offset += data_size
        self.querystring['offset'] = self.page_offset
        self.update_count(self.page_offset)
        self.crawl()


# 爬取菜品
class CrawlEleDishes(BaseCrawler):
    def __init__(self, c_type, cookies, args=None):
        super(CrawlEleDishes, self).__init__(c_type, cookies, args)
        self.url = 'https://www.ele.me/restapi/shopping/v2/menu'
        if not args:
            args = {}
        restaurant = args.get('restaurant')
        self.restaurant_id = restaurant.get('id')
        self.latitude = args.get('latitude')
        self.longitude = args.get('longitude')
        self.cookies = cookies
        self.querystring = {"restaurant_id": self.restaurant_id}
        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "shopid={};loc={},{}".format(self.restaurant_id, restaurant.get('latitude'),
                                                    restaurant.get('longitude')),
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
        self.insert_extras(json.dumps(extras))
        self.dish_crawler = CrawlEleDishes(3, cookies, args)

    def crawl(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring,
                                    cookies=self.cookies)
        if response.status_code != requests.codes.ok:
            self.error('response code != 200')
            return
        dishes = response.json()
        total = 0
        for item in dishes:
            logging.info(item)
            foods = item.get('foods')
            for food_item in foods:
                name = food_item.get('name'),
                restaurant_id = food_item.get('restaurant_id'),
                rating = food_item.get('rating'),
                month_sales = food_item.get('month_sales'),
                rating_count = food_item.get('rating_count')
                DishDao.create(restaurant_id, name, rating, month_sales, rating_count, self.id)
                total += 1
                self.update_count(total)

        self.done(total)
        self.dish_crawler.crawl()


# 爬取评论
class CrawlerEleShopRate(BaseCrawler):
    def __init__(self, cookies, args=None):
        super(CrawlerEleShopRate, self).__init__(cookies, args)
        self.page_size = 10
        self.page_offset = 0
        restaurant = args.get('restaurant')
        self.restaurant_id = restaurant.get('id')
        self.latitude = args.get('latitude')
        self.longitude = args.get('longitude')
        self.url = 'https://www.ele.me/restapi/ugc/v1/restaurant/{}/ratings'.format(self.restaurant_id)
        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "shopid={};loc={},{}".format(self.restaurant_id, restaurant.get('latitude'),
                                                    restaurant.get('longitude')),
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
            'referer': "https://www.ele.me/shop/{}".format(self.restaurant_id),
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache",
        }
        self.querystring = {
            "limit": self.page_size,
            "offset": self.page_offset,
            "record_type": 1
        }
        extras = {
            'headers': self.headers,
            'query': self.querystring
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
            rating_star = item.get('rating_star')
            rated_at = item.get('rated_at')
            rating_text = item.get('rating_text')
            time_spent_desc = item.get('time_spent_desc')
            RateDao.create(rating_star, rated_at, rating_text, time_spent_desc, self.restaurant_id)
        data_size = len(data)
        if data_size < 1:
            self.done(self.page_offset)
            return
        self.page_offset += data_size
        self.querystring['offset'] = self.page_offset
        self.update_count(self.page_offset)
        self.crawl()
