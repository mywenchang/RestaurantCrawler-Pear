# coding=utf-8

import requests

from pear.crawlers import Crawlers
from pear.crawlers import crawler_types
from pear.jobs.job_queue import JobQueue
from pear.utils.logger import logger

queue = JobQueue()


@queue.task('crawlers')
def new_crawler(crawler, cookies, args):
    logger.info('{}-{}-{}'.format(crawler, cookies, args))
    c_type = 0
    for k, v in crawler_types.iteritems():
        if v == crawler_types:
            c_type = k
            break
    crawler = Crawlers[crawler](c_type, cookies, args)
    crawler.crawl()


def get_ele_msg_code(mobile_phone, captcha_value='', captch_hash=''):
    url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    payload = {
        'mobile': mobile_phone,
        'captcha_value': captcha_value,
        'captcha_hash': captch_hash
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'origin': 'https://h5.ele.me',
        'referer': 'https://h5.ele.me/login/'
    }
    token = ''
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            token = data.get('validate_token', '')
            return True, token, ''
        msg = data
        return False, token, msg
    except Exception as e:
        msg = e.message.__str__()
    return False, token, msg


def get_captchas(mobile_phone):
    url = 'https://www.ele.me/restapi/eus/v3/captchas'
    payload = {
        'captcha_str': mobile_phone
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'origin': 'https://h5.ele.me',
        'referer': 'https://h5.ele.me/login/'
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('captcha_image'), data.get('captcha_hash')
    except Exception as e:
        logger.error(e, exc_info=True)


def login_ele_by_mobile(mobile_phone, sms_code, sms_token):
    url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
    payload = {
        "mobile": mobile_phone,
        "validate_code": sms_code,
        "validate_token": sms_token
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'origin': 'https://h5.ele.me',
        'referer': 'https://h5.ele.me/login/'
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        if resp.status_code == 200:
            return True, resp.cookies, resp.text
        return False, resp.cookies, resp.text
    except Exception as e:
        logger.error(e, exc_info=True)


def get_ele_city_list():
    url = 'https://www.ele.me/restapi/shopping/v1/cities'
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data
    except Exception as e:
        logger.error(e, exc_info=True)


def search_ele_address(key):
    url = 'https://www.ele.me/restapi/v2/pois'
    params = {
        'extras[]': 'count',
        'geohash': 'wm6jbj1skd7d',
        'keyword': key,
        'limit': 20,
        'type': 'nearby'
    }
    try:
        resp = requests.get(url, timeout=5, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return data
    except Exception as e:
        logger.error(e, exc_info=True)


def get_ele_restaurants(geohash, latitude, longitude, cookies, offset=0, limit=24):
    url = 'https://www.ele.me/restapi/shopping/restaurants'
    params = {
        'geohash': geohash,
        'latitude': latitude,
        'longitude': longitude,
        'offset': offset,
        'limit': limit,
        'extras[]': 'activities'
    }
    try:
        resp = requests.get(url, timeout=5, params=params, cookies=cookies)
        if resp.status_code == 200:
            data = resp.json()
            return data
    except Exception as e:
        logger.error(e, exc_info=True)
