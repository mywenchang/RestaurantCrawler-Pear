# coding=utf-8

from pear.crawlers import crawler_ele

CRAWLERS = dict({
    'ele_crawler': crawler_ele.CrawlEleDishes,
    'ele_rate_crawler': crawler_ele.CrawlerEleShopRate
})

CRAWLER_TYPES = dict({
    1: 'ele_crawler',
    2: 'meituan_crawler',
    3: 'ele_rate_crawler'
})
