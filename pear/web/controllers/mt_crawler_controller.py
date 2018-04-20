# coding=utf-8

import requests

from pear.utils.logger import logger


# 1 输入城市+地点搜索商圈 get_place_by_region
# 2 传递关键词和经纬度获取商家 get_area_page
# 3 获取商家列表 get_restaurants

def get_place_by_region(key, region):
    url = 'http://api.map.baidu.com/place/v2/suggestion'
    query = {
        'query': key,
        'region': region,
        'output': 'json',
        'ak': 'g1PsktRjKH07jaAsDcYny7qIYZfAdxUQ'
    }
    try:
        resp = requests.get(url, params=query, timeout=5, allow_redirects=False)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            data = resp.json()
            return data
        else:
            logger.error(resp.content)
        return None
    except Exception as e:
        logger.error(e, exc_info=True)


def get_area_page(key, lat, lng):
    url = 'http://waimai.meituan.com/geo/geohash'
    query = {
        'lat': lat,
        'lng': lng,
        'addr': key,
        'from': 'm'
    }
    headers = {
        'host': 'waimai.meituan.com',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    cookies = {
        '_lxsdk_s': '123'
    }
    try:
        resp = requests.get(url, params=query, timeout=5, headers=headers, allow_redirects=False, cookies=cookies)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            data = resp.json()
            return data
        elif resp.status_code == 302:
            location = resp.headers.get('location')
            return location
        else:
            logger.error(resp.content)
        return None
    except Exception as e:
        logger.error(e, exc_info=True)


def get_restaurants(location):
    headers = {
        'host': 'waimai.meituan.com',
        'referer': 'http://waimai.meituan.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    cookies = {
        '_lxsdk_s': '123'
    }
    try:
        resp = requests.get(location, timeout=5, headers=headers, cookies=cookies)
        cookies = resp.cookies
        logger.info(cookies)
        logger.info(resp.headers)
        for k, v in cookies.items():
            logger.info('{}: {}'.format(k, v))
    except Exception as e:
        logger.error(e, exc_info=True)
