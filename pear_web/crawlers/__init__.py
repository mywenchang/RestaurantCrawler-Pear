# coding=utf-8

from pear_web.crawlers import crawler_ele

Crawlers = dict({
    'create_ele_restaurant_crawler': crawler_ele.CrawlEleRestaurants,
    'create_ele_dish_crawler': crawler_ele.CrawlEleDishes
})
