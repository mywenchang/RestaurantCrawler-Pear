# coding=utf-8

import requests
from geohash2 import geohash

from pear.utils.const import SOURCE, HOT_CITIES
from pear.utils.logger import logger
from pear.utils.mem_cache import mem_cache
from pear.web.controllers.comm import save_ele_restaurants


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
        msg = data.get('message')
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
            return True, data.get('captcha_image'), data.get('captcha_hash')
        logger.error(u'get_ele_pic_failed: {}'.format(resp.content))
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return False, None, None


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


@mem_cache()
def get_ele_city_list():
    url = 'https://www.ele.me/restapi/shopping/v1/cities'
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            cities = []
            for k, v in data.iteritems():
                item = [i for i in data[k] if i['name'] in HOT_CITIES]
                cities.extend(item)
            return cities
    except Exception as e:
        logger.error(e, exc_info=True)


@mem_cache()
def search_ele_address(key, latitude, longitude):
    url = 'https://www.ele.me/restapi/v2/pois'
    _geohash = geohash.encode(latitude=float(
        latitude), longitude=float(longitude))
    logger.info('geohash: {}'.format(_geohash))
    params = {
        'extras[]': 'count',
        'geohash': _geohash,
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
        logger.info(resp.headers)
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                image_path = item['image_path']
                save_ele_restaurants.put(
                    source=SOURCE.ELE,
                    restaurant_id=item['id'],
                    name=item['name'],
                    sales=item['recent_order_num'],
                    arrive_time=item['order_lead_time'],
                    send_fee=item['float_delivery_fee'],
                    score=item['rating'],
                    latitude=item['latitude'],
                    longitude=item['longitude'],
                    image='https://fuss10.elemecdn.com/{}/{}/{}.{}'.format(image_path[0:1], image_path[1:3],
                                                                           image_path[3:],
                                                                           image_path[32:])
                )
            return data
    except Exception as e:
        logger.error(e, exc_info=True)
