# coding=utf-8

from pear.crawlers import crawler_ele

CRAWLERS = dict({
    'ele_crawler': crawler_ele.CrawlEleDishes
})

CRAWLER_TYPES = dict({
    1: 'ele_crawler',
    2: 'meituan_crawler'
})
