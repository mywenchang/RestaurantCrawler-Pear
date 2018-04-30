import os

config = {
    'mysql': 'mysql+pymysql://{}?charset=utf8mb4'.format(os.getenv('pear_web_mysql')),
    'beanstalk': {
        'host': '0.0.0.0',
        'port': 11300
    },
    'logging_formatter': '%(asctime)s [%(process)d] %(filename)s %(lineno)d %(levelname)s: %(message)s'
}

MYSQL_CONFIG = config['mysql']
BEANSTALK_CONFIG = config['beanstalk']
LOGGING_FORMATTER = config['logging_formatter']
IS_DEBUG = bool(os.getenv('is_debug', False))
DOMAIN = '.youcute.cn'
