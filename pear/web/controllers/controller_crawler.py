# coding=utf-8

import requests

from pear.crawlers import CRAWLER_TYPES, CRAWLERS
from pear.jobs.job_queue import JobQueue
from pear.models.restaurant import RestaurantDao
from pear.utils.const import SOURCE
from pear.utils.logger import logger

queue = JobQueue()


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


def get_ele_captchas(mobile_phone):
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
            for item in data:
                save_ele_restaurants.put(
                    source=SOURCE.ELE,
                    restaurant_id=item['id'],
                    name=item['name'],
                    sales=item['recent_order_num'],
                    arrive_time=item['order_lead_time'],
                    send_fee=item['float_delivery_fee'],
                    score=item['rating'],
                    latitude=item['latitude'],
                    longitude=item['longitude']
                )
            return data
    except Exception as e:
        logger.error(e, exc_info=True)


@queue.task('crawlers')
def commit_crawler_task(source, cookies, args):
    crawler_str = "{}_crawler".format(source)
    match_crawler = CRAWLERS.get(crawler_str)
    if not match_crawler:
        logger.error('{} NOT MATCH!'.format(crawler_str))
        return
    crawler_type = 0
    for k, v in CRAWLER_TYPES.iteritems():
        if v == crawler_str:
            crawler_type = k
            break
    crawler = match_crawler(crawler_type, cookies, args)
    crawler.crawl()


@queue.task('crawlers')
def save_ele_restaurants(restaurant_id, name, source, sales, arrive_time, send_fee, score, latitude, longitude):
    restaurant = RestaurantDao.get_by_restaurant_id(restaurant_id)
    if restaurant:
        RestaurantDao.update_by_restaurant_id(restaurant_id, name=name, source=source, sales=sales,
                                              arrive_time=arrive_time, send_fee=send_fee, score=score,
                                              latitude=latitude, longitude=longitude)
    else:
        RestaurantDao.create(restaurant_id, name, source, sales, arrive_time, send_fee, score, latitude, longitude)
