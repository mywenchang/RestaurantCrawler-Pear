# coding=utf-8

import requests
import time

from pear.utils.logger import logger


def get_hot_city():
    url = 'http://api.map.baidu.com'
    query = {
        'qt': 'cur',
        'wd': u'全国',
        'ie': 'utf-8',
        'oue': 1,
        'fromproduct': 'jsapi',
        'res': 'api',
        'ak': 'l1efF5xp00r6mHIeesGh5amG'
    }
    try:
        resp = requests.get(url, params=query, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data
        return None
    except Exception as e:
        logger.error(e, exc_info=True)


def search_address(key):
    url = 'http://map.baidu.com/su'
    query = {
        'wd': key,
        'cid': 75,
        'type': 0,
        't': time.time() * 1000,
        'from': 'jsapi'
    }
    try:
        resp = requests.get(url, params=query, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data
        return None
    except Exception as e:
        logger.error(e, exc_info=True)
