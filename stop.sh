#! /bin/sh

echo '-------------------kill gunicorn--------------------------'
kill `ps -ef |grep bin/gunicorn |grep -v grep| awk '{print $2}'`

echo '-------------------kill job_queue--------------------------'
kill `ps -ef |grep bin/job_queue |grep -v grep| awk '{print $2}'`
