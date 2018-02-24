# coding=utf-8

import logging

from pear.crawlers import Crawlers
from pear.jobs.job_queue import JobQueue

logger = logging.getLogger('')

queue = JobQueue()


def _wrap_action(action, source, type):
    return '{}_{}_{}_crawler'.format(action, source, type)


@queue.task('crawlers')
def create_crawler(action, source, type, args):
    action = _wrap_action(action, source, type)
    if action not in Crawlers.keys():
        logger.warn('Not found crawler for action:{}'.format(action))
        return
    crawler = Crawlers[action](args)
    logger.info(crawler)
    crawler.crawl()
