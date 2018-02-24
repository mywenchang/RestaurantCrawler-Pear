config = {
    'mysql': 'mysql+pymysql://jiyang:jiyang147852@localhost/db_pear',
    'beanstalk': {
        'host': '0.0.0.0',
        'port': 11300
    }
}

MYSQL_CONFIG = config['mysql']
BEANSTALK_CONFIG = config['beanstalk']
IS_DEBUG = False
