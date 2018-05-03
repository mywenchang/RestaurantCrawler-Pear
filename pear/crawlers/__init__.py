# coding=utf-8

from pear.crawlers import crawler_ele

CRAWLERS = dict({
    'ele_crawler': crawler_ele.CrawlEleDishes
})

CRAWLER_TYPES = dict({
    'ele_crawler': 1,
    'meituan_crawler': 2
})
