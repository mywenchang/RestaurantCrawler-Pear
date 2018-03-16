# coding=utf-8

from pear.crawlers import crawler_ele

Crawlers = dict({
    'ele_restaurant_crawler': crawler_ele.CrawlEleRestaurant,
    'ele_dish_crawler': crawler_ele.CrawlEleDishes,
    'ele_rate_crawler': crawler_ele.CrawlerEleShopRate
})

crawler_types = dict({
    1: 'ele_restaurant_crawler',
    2: 'ele_dish_crawler',
    3: 'ele_rate_crawler'
})
