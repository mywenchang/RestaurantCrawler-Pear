# coding=utf-8
import json
import logging

import requests
import time

from pear.crawlers.base import BaseCrawler
from pear.models.dish import DishDao
from pear.models.rate import RateDao
from pear.utils.const import SOURCE

logger = logging.getLogger('')


# 爬取菜品
class CrawlEleDishes(BaseCrawler):
    def __init__(self, c_type, cookies, args=None):
        self.url = 'https://www.ele.me/restapi/shopping/v2/menu'
        self.args = args
        if not args:
            args = {}
        self.restaurant = args.get('restaurant')
        self.restaurant_id = self.restaurant.get('id')
        self.latitude = args.get('latitude')
        self.longitude = args.get('longitude')
        self.cookies = cookies
        super(CrawlEleDishes, self).__init__(SOURCE.ELE, c_type, self.restaurant_id, cookies, args)
        self.querystring = {"restaurant_id": self.restaurant_id}
        self.headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "shopid={};loc={},{}".format(self.restaurant_id, self.restaurant.get('latitude'),
                                                    self.restaurant.get('longitude')),
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

    def __crawl_rate(self, total):
        url = 'https://www.ele.me/restapi/ugc/v1/restaurant/{}/ratings'.format(
            self.restaurant_id)
        headers = {
            'accept': "application/json, text/plain, */*",
            'x-shard': "shopid={};loc={},{}".format(self.restaurant_id, self.restaurant.get('latitude'),
                                                    self.restaurant.get('longitude')),
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
            'referer': "https://www.ele.me/shop/{}".format(self.restaurant_id),
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            'cache-control': "no-cache",
        }
        page_size = 10
        page_offset = 0
        while True:
            querystring = {
                "limit": page_size,
                "offset": page_offset,
                "record_type": 1
            }
            logger.info('start_crawl_ele_rate_{}'.format(self.restaurant_id))
            response = requests.request("GET", url, headers=headers, params=querystring, cookies=self.cookies)
            if response.status_code != requests.codes.ok:
                self.error(json.dumps(response.json()))
                return
            data = response.json()
            for item in data:
                rating_id = int(time.time())
                rating_star = item.get('rating_star')
                rated_at = item.get('rated_at')
                rating_text = item.get('rating_text')
                time_spent_desc = item.get('time_spent_desc')
                food_list = item.get('item_rating_list')
                for food in food_list:
                    food_id = food.get('food_id')
                    food_name = food.get('rate_name')
                    food_star = food.get('rating_star')
                    food_rate = food.get('rating_text')
                    RateDao.create(self.id, rating_id, rating_star, rated_at, rating_text, time_spent_desc, food_id,
                                   food_name, food_star, food_rate, self.restaurant_id)
            data_size = len(data)
            if data_size < 1:
                return
            page_offset += data_size
            self.update_count(total + page_offset)

    def crawl(self):
        logger.info('start_craw_ele_dishes_{}'.format(self.restaurant_id))
        response = requests.get(
            self.url, headers=self.headers, params=self.querystring, cookies=self.cookies)
        if response.status_code != requests.codes.ok:
            self.error(json.dumps(response.json()))
            return
        dishes = response.json()
        total = 0
        for item in dishes:
            foods = item.get('foods')
            for food_item in foods:
                name = food_item.get('name'),
                restaurant_id = food_item.get('restaurant_id'),
                rating = food_item.get('rating'),
                month_sales = food_item.get('month_sales'),
                rating_count = food_item.get('rating_count')
                food_id = food_item.get('specfoods')[0].get('food_id')
                price = food_item.get('specfoods')[0].get('price')
                DishDao.create(food_id, restaurant_id, name, rating, month_sales, rating_count, price, self.id)
                total += 1
                self.update_count(total)
        try:
            self.__crawl_rate(total=total)
        except Exception as e:
            logger.error(e, exc_info=True)
        self.done()
