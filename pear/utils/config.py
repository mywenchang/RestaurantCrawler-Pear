config = {
    'mysql': 'mysql+pymysql://root:jiyang147852@localhost/db_pear?charset=utf8',
    'beanstalk': {
        'host': '0.0.0.0',
        'port': 11300
    },
    'logging_formatter': '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
}

MYSQL_CONFIG = config['mysql']
BEANSTALK_CONFIG = config['beanstalk']
LOGGING_FORMATTER = config['logging_formatter']
IS_DEBUG = False
