#! /bin/sh

echo '|-------------------start web server--------------------------|'
bin/gunicorn pear.web.app:application -w 4 -b 0.0.0.0:9999&

echo '|-------------------start beanstalk server--------------------|'
beanstalkd&

echo '|-------------------start beanstalk work----------------------|'
bin/job_queue&