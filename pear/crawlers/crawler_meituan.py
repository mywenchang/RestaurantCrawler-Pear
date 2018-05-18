# coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pear.crawlers.base import BaseCrawler
from pear.utils.const import SOURCE
from pear.utils.logger import logger
from pear.utils.tool import get_number_from_str
from pear.web.controllers.comm import save_ele_restaurants

CHROME_DRIVE_PATH = 'etc/chrome_driver'
_LXSDK_S = '%7C%7C0'


def get_soup(data):
    return BeautifulSoup(data, 'html5lib')


def get_headless_chrome(option_dict=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    if isinstance(option_dict, dict):
        for k, v in option_dict.items():
            options.add_argument(u'{}="{}"'.format(k, v))
    elif option_dict and not isinstance(option_dict, list):
        raise Exception("option_list must be list")
    browser = webdriver.Chrome(executable_path=CHROME_DRIVE_PATH, options=options)
    return browser


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
        '_lxsdk_s': _LXSDK_S
    }
    location = None
    try:
        resp = requests.get(url, params=query, timeout=5, headers=headers, allow_redirects=False, cookies=cookies)
        logger.info('get home page resp: {} {} {}'.format(resp.status_code, resp.content, resp.headers))
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            location = resp.json()
        elif resp.status_code == 302:
            location = resp.headers.get('location')
        else:
            logger.error(resp.content)
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return location


class CrawlerMeiTuan(BaseCrawler):

    def __init__(self, c_type, cookies, address, lng, lat):
        self.restaurant_id = int(time.time())
        self.address = address
        self.lng = lng
        self.lat = lat
        super(CrawlerMeiTuan, self).__init__(SOURCE.MEI_TUAN, c_type, self.restaurant_id, cookies, None)

    def crawl(self):
        location = get_area_page(self.address, self.lat, self.lng)
        if not location or '404' in location:
            logger.error(u'{} not find location page.'.format(self.address))
            return
        logger.info(u'{} location page: {}'.format(self.address, location))
        headers = [
            'host="waimai.meituan.com"',
            'referer="http://waimai.meituan.com/"',
            'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"'
        ]
        browser = get_headless_chrome(headers)
        browser.get(location)
        browser.delete_all_cookies()
        new_cookies = {
            'name': '_lxsdk_s', 'value': _LXSDK_S
        }
        browser.add_cookie(new_cookies)
        browser.execute_script('window.open("{}")'.format(location))
        browser.close()
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
        if '403' in browser.page_source:
            logger.error('got 403 {}'.format(location))
            return
        WebDriverWait(browser, 10, 0.5).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'rest-li')))
        restaurant_list_page = browser.page_source
        self.get_restaurant_data(restaurant_list_page)
        restaurant_list = browser.find_elements_by_css_selector('div.restaurant')


    def get_restaurant_data(self, page_source):
        sp = get_soup(page_source)
        restaurants_list_li = sp.find_all('li', class_='fl rest-li')
        for item in restaurants_list_li:
            restaurant_element = item.find('div', class_='restaurant')
            if not restaurant_element:
                continue
            try:
                name = restaurant_element['data-title']
                restaurant_id = int(restaurant_element['data-poiid'])
                self.restaurant_id = restaurant_id
                img_src = restaurant_element.find('div', class_='preview').find('img', class_='scroll-loading')['src']
                # 评价
                score = get_number_from_str(restaurant_element.find('span', class_='score-num').get_text())
                # 消费多少元才配送
                start_send_fee = get_number_from_str(
                    restaurant_element.find('span', class_='start-price').get_text())
                # 配送费
                send_fee = get_number_from_str(restaurant_element.find('span', class_='send-price').get_text())
                # 配送时间
                arrive_time = get_number_from_str(restaurant_element.find('span', class_='send-time').get_text())
                save_ele_restaurants.put(restaurant_id=restaurant_id, name=name, source=SOURCE.MEI_TUAN,
                                         arrive_time=arrive_time, send_fee=send_fee, score=score, image=img_src)
            except Exception as e:
                logger.error(e)
