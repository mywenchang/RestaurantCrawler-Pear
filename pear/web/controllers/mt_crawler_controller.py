# coding=utf-8

from pear.crawlers import CRAWLER_TYPES
from pear.crawlers.crawler_meituan import CrawlerMeiTuan
from pear.jobs.job_queue import JobQueue


@JobQueue.task('crawlers')
def commit_mt_crawler_task(address, lng, lat, cookies):
    crawler = CrawlerMeiTuan(CRAWLER_TYPES['meituan_crawler'], cookies=cookies, address=address, lng=lng, lat=lat)
    crawler.crawl()
