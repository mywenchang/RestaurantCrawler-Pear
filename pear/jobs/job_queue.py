# coding=utf-8

import json

import beanstalkc
import signal
import time

from pear.jobs.utils import import_module_by_str
from pear.utils.config import BEANSTALK_CONFIG
from pear.utils.logger import logger


class Subscriber(object):
    FUN_MAP = {}

    def __init__(self, func, tube):
        logger.info('register func:{} to tube:{}.'.format(func.__name__, tube))
        Subscriber.FUN_MAP.setdefault(tube, {})
        Subscriber.FUN_MAP[tube][func.__name__] = func


class JobQueue(object):
    @classmethod
    def task(cls, tube):
        def wrapper(func):
            Subscriber(func, tube)
            return Putter(func, tube)

        return wrapper


class Putter(object):
    def __init__(self, func, tube):
        self.func = func
        self.tube = tube

    # 直接调用返回
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    # 推给离线队列
    def put(self, **kwargs):
        args = {
            'func_name': self.func.__name__,
            'tube': self.tube,
            'kwargs': kwargs
        }
        beanstalk = beanstalkc.Connection(host=BEANSTALK_CONFIG['host'], port=BEANSTALK_CONFIG['port'])
        try:
            beanstalk.use(self.tube)
            job_id = beanstalk.put(json.dumps(args))
            return job_id
        finally:
            beanstalk.close()


class Worker(object):
    worker_id = 0

    def __init__(self, tubes):
        self.beanstalk = beanstalkc.Connection(host=BEANSTALK_CONFIG['host'], port=BEANSTALK_CONFIG['port'])
        self.tubes = tubes
        self.reserve_timeout = 20
        self.timeout_limit = 1000
        self.kick_period = 600
        self.signal_shutdown = False
        self.release_delay = 0
        self.age = 0
        self.signal_shutdown = False
        signal.signal(signal.SIGTERM, lambda signum, frame: self.graceful_shutdown())
        Worker.worker_id += 1
        import_module_by_str('pear.web.controllers.comm')
        import_module_by_str('pear.web.controllers.analy_task_controller')

    def subscribe(self):
        if isinstance(self.tubes, list):
            for tube in self.tubes:
                if tube not in Subscriber.FUN_MAP.keys():
                    logger.error('tube:{} not register!'.format(tube))
                    continue
                self.beanstalk.watch(tube)
        else:
            if self.tubes not in Subscriber.FUN_MAP.keys():
                logger.error('tube:{} not register!'.format(self.tubes))
                return
            self.beanstalk.watch(self.tubes)

    def run(self):
        self.subscribe()
        while True:
            if self.signal_shutdown:
                break
            if self.signal_shutdown:
                logger.info("graceful shutdown")
                break
            job = self.beanstalk.reserve(timeout=self.reserve_timeout)  # 阻塞获取任务，最长等待 timeout
            if not job:
                continue
            try:
                self.on_job(job)
                self.delete_job(job)
            except beanstalkc.CommandFailed as e:
                logger.error(e, exc_info=True)
            except Exception as e:
                logger.error(e, exc_info=True)
                kicks = job.stats()['kicks']
                if kicks < 3:
                    self.bury_job(job)
                else:
                    message = json.loads(job.body)
                    logger.error("Kicks reach max. Delete the job", extra={'body': message})
                    self.delete_job(job)

    @classmethod
    def on_job(cls, job):
        start = time.time()
        msg = json.loads(job.body)
        tube = msg.get('tube')
        func_name = msg.get('func_name')
        try:
            func = Subscriber.FUN_MAP[tube][func_name]
            kwargs = msg.get('kwargs')
            logger.info(u'run {} args:{}'.format(func_name, kwargs))
            func(**kwargs)
        except Exception as e:
            logger.error(e.message, exc_info=True)
        cost = time.time() - start
        logger.info('{} cost {} s'.format(func_name, cost))

    @classmethod
    def delete_job(cls, job):
        try:
            job.delete()
        except beanstalkc.CommandFailed as e:
            logger.warning(e, exc_info=1)

    @classmethod
    def bury_job(cls, job):
        try:
            job.bury()
        except beanstalkc.CommandFailed as e:
            logger.warning(e, exc_info=1)

    def graceful_shutdown(self):
        self.signal_shutdown = True
