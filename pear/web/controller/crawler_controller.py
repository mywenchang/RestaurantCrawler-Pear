# coding=utf-8

from pear.crawlers import Crawlers
from pear.jobs.job_queue import Router
import logging

router = Router()
logger = logging.getLogger('')


def _wrap_action(action, source, type):
    return '{}_{}_{}_crawler'.format(action, source, type)


@router.job(tube='crawlers')
def start_crawl(source, type, action, args=None):
    action = _wrap_action(action, source, type)
    logger.info(action)
    if action not in Crawlers.keys():
        return
    crawler = Crawlers[action]()
    crawler.crawl()
