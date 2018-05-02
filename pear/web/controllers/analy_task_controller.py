# coding=utf-8

from pear.models.analyse_task import AnalyseTaskDao
from pear.jobs.job_queue import JobQueue


@JobQueue.task('crawlers')
def save_analyse_data(u_id, data, _type, crawler_one, crawler_two=None):
    AnalyseTaskDao.create(u_id, data, crawler_one, crawler_two, _type)
