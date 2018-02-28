# coding=utf-8

from pear.crawlers import crawler_ele

Crawlers = dict({
    'ele_restaurant_crawler': crawler_ele.CrawlEleRestaurants,
    'ele_dish_crawler': crawler_ele.CrawlEleDishes
})
