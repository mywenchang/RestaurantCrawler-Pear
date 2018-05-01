#! /bin/sh

echo '|-------------------start web server--------------------------|'
bin/gunicorn pear.web.app:application -w 4 -b 0.0.0.0:7777