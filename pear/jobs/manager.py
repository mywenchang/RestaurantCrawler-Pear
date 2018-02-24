# coding=utf-8


from multiprocessing import Process, cpu_count

MAX_WORKER = cpu_count() * 2


def main():
    from pear.jobs.job_queue import Worker
    # for count in range(MAX_WORKER):
    worker = Worker(['default', 'crawlers'])
    worker.run()
        # process = Process(target=worker.run, name=worker.worker_id)
        # process.start()


if __name__ == '__main__':
    main()
