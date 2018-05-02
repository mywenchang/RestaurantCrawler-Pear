# coding=utf-8
import os

config = {
    'mysql': 'mysql+pymysql://{}?charset=utf8mb4'.format(os.getenv('pear_web_mysql')),
    'beanstalk': {
        'host': '0.0.0.0',
        'port': 11300
    },
    'logging_formatter': '%(asctime)s [%(process)d] %(filename)s %(lineno)d %(levelname)s: %(message)s'
}

IS_DEBUG = bool(os.getenv('is_debug', False))
MYSQL_CONFIG = config['mysql']
BEANSTALK_CONFIG = config['beanstalk']
LOGGING_FORMATTER = config['logging_formatter']
DOMAIN = '.youcute.cn'
ELE_LOGIN_MAX_AGE = 60 * 30  # 饿了么登录成功的cookie超时时间，30分钟
USER_LOGIN_MAX_AGE = 30 * 24 * 60 * 60  # 用户登录的cookie超时时间，一个月
