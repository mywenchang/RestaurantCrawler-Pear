# coding=utf-8

import logging

from pear.crawlers import Crawlers
from pear.jobs.job_queue import JobQueue
from pear.utils.config import LOGGING_FORMATTER

logging.basicConfig(format=LOGGING_FORMATTER, level=logging.INFO)
logger = logging.getLogger('')

queue = JobQueue()


def _wrap_action(source, type):
    return '{}_{}_crawler'.format(source, type)


@queue.task('crawlers')
def create_crawler(source, type, args):
    action = _wrap_action(source, type)
    if action not in Crawlers.keys():
        logger.warn('Not found crawler for action:{}'.format(action))
        return
    crawler = Crawlers[action](args)
    crawler.crawl()
