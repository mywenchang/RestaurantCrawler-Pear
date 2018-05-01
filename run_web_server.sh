#! /bin/sh

echo '|-------------------start web server--------------------------|'
bin/gunicorn pear.web.app:application -w 4 -b 127.0.0.1:7777