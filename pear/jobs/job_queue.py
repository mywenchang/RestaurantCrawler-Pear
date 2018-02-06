# coding=utf-8

import json
import logging.config
from collections import defaultdict

import beanstalkc
import time
from pear.utils.config import BEANSTALK_CONFIG

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)
logger = logging.getLogger('')


class Subscriber(object):
    func_map = defaultdict(dict)

    def __init__(self, func, tube, **kwargs):
        func_name = func.__name__
        if func_name in Subscriber.func_map[tube]:
            raise RuntimeError('already defined func {0} on {1}'.format(func_name, tube))
        Subscriber.func_map[tube][func_name] = func
        logger.info('defined {} to {}'.format(func_name, tube))
        self.tube = tube
        self.kwargs = kwargs


class Router(object):
    def job(self, tube='default', **kwargs):
        def wrapper(func):
            Subscriber(func=func, tube=tube, kwargs=kwargs)
            return Putter(tube=tube, func=func, **kwargs)

        return wrapper


class Putter(object):
    def __init__(self, tube, func, **kwargs):
        self.tube = tube
        self.func = func
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def enqueue(self, *args, **kwargs):
        msg = {
            'func_name': self.func.__name__,
            'args': args,
            'kwargs': kwargs
        }
        logger.info(msg)
        return self.push(msg)

    def push(self, msg):
        beanstalk = beanstalkc.Connection(host=BEANSTALK_CONFIG['host'], port=BEANSTALK_CONFIG['port'])
        beanstalk.use(self.tube)
        job_id = beanstalk.put(json.dumps(msg))
        return job_id


class Worker(object):
    def __init__(self, tubes):
        self.beanstalk = beanstalkc.Connection(host=BEANSTALK_CONFIG['host'], port=BEANSTALK_CONFIG['port'])
        self.tubes = tubes
        self.reserve_timeout = 20
        self.timeout_limit = 1000
        self.kick_period = 600
        self.signal_shutdown = False
        self.release_delay = 0
        self.age = 0

    def subscribe(self):
        if isinstance(self.tubes, list):
            for tube in self.tubes:
                self.beanstalk.watch(tube)
        else:
            self.beanstalk.watch(self.tubes)

    def run(self):
        self.subscribe()
        self.will_kick = time.time() + 10
        while True:
            if self.signal_shutdown:
                logger.info("graceful shutdown")
                break
            if time.time() < self.will_kick:
                job = self.beanstalk.reserve(timeout=self.reserve_timeout)
                if not job:
                    continue
                try:
                    if self.age:
                        age = job.stats()['age']
                        if age > self.age:
                            logger.warning("Job expired . Delete the job: {0}".format(Compressor.decompress(job.body)))
                            self.delete_job(job)
                            continue
                    job_timeouts = job.stats()['timeouts']
                    if job_timeouts > self.timeout_limit:
                        logger.warning("Job expired . Delete the job: {0}".format(Compressor.decompress(job.body)))
                        self.delete_job(job)
                        continue
                    self.on_job(job)
                    self.delete_job(job)
                except beanstalkc.CommandFailed as e:
                    logger.warning(e, exc_info=1)
                except:
                    kicks = job.stats()['kicks']
                    if kicks < 3:
                        self.bury_job(job)
                    else:
                        message = json.loads(job.body)
                        logger.error("Kicks reach max. Delete the job", extra={'body': message})
                        self.delete_job(job)
            else:
                number = self.kick(100)
                logger.warning("I kicked {0} buried jobs".format(number))
                self.will_kick = time.time() + (self.kick_period if number > 0 else 2 * self.kick_period)

    def on_job(self, job):
        start_time = time.time()
        jid = job.jid
        stats = job.stats()
        tube = stats['tube']
        msg = json.loads(job.body)
        func_name = msg['func_name']
        funs = Subscriber.func_map[tube]
        if func_name not in funs:
            return
        func = funs[func_name]
        try:
            func(*msg['args'], **msg['kwargs'])
        except Exception as e:
            logger.error(e)
        cost = (time.time() - start_time) * 1000
        logger.info('call job {}: {} OK {}ms'.format(jid, func_name, cost))

    def delete_job(self, job):
        try:
            job.delete()
        except beanstalkc.CommandFailed as e:
            logger.warning(e, exc_info=1)

    def bury_job(self, job):
        try:
            job.bury()
        except beanstalkc.CommandFailed as e:
            logger.warning(e, exc_info=1)

    def kick(self, n=1000):
        total = 0
        for tube in self.tubes:
            self.beanstalk.use(tube)
            for i in range(n):
                job = self.beanstalk.peek_buried()
                if job:
                    total += self.beanstalk.kick()
                else:
                    break
        return total


def main():
    worker = Worker(['crawlers'])
    worker.run()
