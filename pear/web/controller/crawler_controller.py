# coding=utf-8

import logging

import requests

from pear.crawlers import Crawlers
from pear.jobs.job_queue import JobQueue
from pear.utils.config import LOGGING_FORMATTER

logging.basicConfig(format=LOGGING_FORMATTER, level=logging.INFO)
logger = logging.getLogger('')

queue = JobQueue()


def _wrap_action(source, type):
    return '{}_{}_crawler'.format(source, type)


@queue.task('crawlers')
def new_crawler(u_id, source, type, cookies, args):
    action = _wrap_action(source, type)
    if action not in Crawlers.keys():
        logger.warn('Not found crawler for action:{}'.format(action))
        return
    crawler = Crawlers[action](u_id, cookies, args)
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
        resp = requests.post(url, json=payload, headers=headers)
        data = resp.json()
        if resp.status_code == 200:
            token = data.get('validate_token', '')
            return True, token, ''
        msg = data
        return False, token, msg
    except Exception as e:
        msg = e.message
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
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('captcha_image'), data.get('captcha_hash')
    except Exception as e:
        logger.error(e.message)


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
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            return True, resp.cookies, resp.content
        return False, resp.cookies, resp.content
    except Exception as e:
        logger.error(e.message)
