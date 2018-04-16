# coding=utf-8
import json
import logging

import requests

from pear.crawlers.base import BaseCrawler
from pear.models.dish import DishDao
from pear.models.rate import RateDao

logger = logging.getLogger('')


# 爬取菜品
class CrawlEleDishes(BaseCrawler):
    def __init__(self, c_type, cookies, args=None):
        super(CrawlEleDishes, self).__init__(c_type, cookies, args)
        self.url = 'https://www.ele.me/restapi/shopping/v2/menu'
        self.args = args
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

    def crawl(self):
        logger.info('start_craw_ele_dishes_{}'.format(self.restaurant_id))
        response = requests.get(self.url, headers=self.headers, params=self.querystring, cookies=self.cookies)
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
                food_id = food_item.get('food_id')
                price = food_item.get('specfoods')[0].get('price')
                DishDao.create(food_id, restaurant_id, name, rating, month_sales, rating_count, price, self.id)
                total += 1
                self.update_count(total)

        self.done(total)
        dish_crawler = CrawlerEleShopRate(3, self.cookies, self.id, self.args)
        dish_crawler.crawl()


# 爬取评论
class CrawlerEleShopRate(BaseCrawler):
    def __init__(self, c_type, cookies, restaurant_crawler_id, args=None):
        super(CrawlerEleShopRate, self).__init__(c_type, cookies, args)
        self.page_size = 10
        self.page_offset = 0
        self.restaurant_crawler_id = restaurant_crawler_id
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
        logger.info('start_crawl_ele_rate_{}'.format(self.restaurant_id))
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
            food_list = item.get('item_rating_list')
            for food in food_list:
                food_id = food.get('food_id')
                food_name = food.get('rate_name')
                food_star = food.get('rating_star')
                food_rate = food.get('rating_text')
                RateDao.create(self.restaurant_crawler_id, rating_star, rated_at, rating_text, time_spent_desc,
                               food_id, food_name, food_star, food_rate, self.restaurant_id)
        data_size = len(data)
        if data_size < 1:
            self.done(self.page_offset)
            return
        self.page_offset += data_size
        self.querystring['offset'] = self.page_offset
        self.update_count(self.page_offset)
        self.crawl()
