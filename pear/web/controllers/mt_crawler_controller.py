# coding=utf-8

from bs4 import BeautifulSoup

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pear.utils.const import SOURCE
from pear.utils.logger import logger
from pear.utils.tool import get_number_from_str
from pear.web.controllers.comm import save_ele_restaurants


def __get_soup(data):
    return BeautifulSoup(data, 'html5lib')


# 1 传递关键词和经纬度获取商家 get_area_page
#     a. 根据地点和经纬度获取特定的页面地址
#     b. 请求页面获得 uuid
# 2 结合 uuid 构造请求获取商家列表 get_restaurants
def __get_headless_chrome(option_list=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    if isinstance(option_list, list):
        for item in option_list:
            options.add_argument(item)
    elif option_list and not isinstance(option_list, list):
        raise Exception("option_list must be list")
    browser = webdriver.Chrome(executable_path='etc/chrome_driver', options=options)
    return browser


def __get_area_page(key, lat, lng):
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
        '_lxsdk_s': '%7C%7C0'
    }
    location = None
    try:
        resp = requests.get(url, params=query, timeout=5, headers=headers, allow_redirects=False, cookies=cookies)
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


def __get_uuid(location):
    if not location:
        return None, None
    headers = {
        'host': 'waimai.meituan.com',
        'referer': 'http://waimai.meituan.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    cookies = {
        '_lxsdk_s': '%7C%7C0'
    }
    url = location
    try:
        resp = requests.get(url, timeout=5, headers=headers, cookies=cookies)
        cookies = resp.cookies
        uuid = cookies.get('w_uuid')
        logger.info('uuid:', uuid)
        return uuid, cookies
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return None, None


def __get_restaurant_data(page_source):
    sp = __get_soup(page_source)
    restaurants_list_li = sp.find_all('li', class_='fl rest-li')
    items = []
    for item in restaurants_list_li:
        restaurant_element = item.find('div', class_='restaurant')
        if not restaurant_element:
            continue
        try:
            name = restaurant_element['data-title']
            restaurant_id = restaurant_element['data-poiid']
            img_src = restaurant_element.find('div', class_='preview').find('img', class_='scroll-loading')['src']
            # 评价
            score = get_number_from_str(restaurant_element.find('span', class_='score-num').get_text())
            # 消费多少元才配送
            start_send_fee = get_number_from_str(restaurant_element.find('span', class_='start-price').get_text())
            # 配送费
            send_fee = get_number_from_str(restaurant_element.find('span', class_='send-price').get_text())
            # 配送时间
            arrive_time = get_number_from_str(restaurant_element.find('span', class_='send-time').get_text())
            items.append({
                'name': name,
                'id': restaurant_id,
                'img_src': img_src,
                'score': score,
                'start_send_fee': start_send_fee,
                'send_fee': send_fee,
                'arrive_time': arrive_time
            })
            save_ele_restaurants.put(
                restaurant_id=restaurant_id, name=name, source=SOURCE.MEI_TUAN, arrive_time=arrive_time,
                send_fee=send_fee, score=score, image=img_src
            )
        except Exception as e:
            logger.error(e)
    return items


def get_restaurants(address, lat, lng):
    location = __get_area_page(address, lat, lng)
    logger.info('location:{}'.format(location))
    if not location:
        return False, None, None, None
    headers = [
        'host="waimai.meituan.com"',
        'referer="http://waimai.meituan.com/"',
        'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"'
    ]
    browser = __get_headless_chrome(headers)
    browser.get(location)
    browser.delete_all_cookies()
    new_cookies = {
        'name': '_lxsdk_s', 'value': '%7C%7C0'
    }
    browser.add_cookie(new_cookies)
    browser.execute_script('window.open("{}")'.format(location))
    browser.close()
    browser.implicitly_wait(10)
    for handle in browser.window_handles:
        browser.switch_to.window(handle)
    try:
        if '403' in browser.page_source:
            return False, None, None, u'爬虫请求被403拒绝'
        page = 1
        while True:
            try:
                # WebDriverWait(browser, 50, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.isloading')))
                load_more = browser.find_element_by_css_selector('div.isloading')
                if u'扫描左下角二维码查看更多商家' in load_more.text:
                    break
                load_more.click()
                logger.info('current_page:{}'.format(page))
                page += 1
                time.sleep(page)
            except Exception as e:
                logger.error(e, exc_info=True)
                break
        restaurants = __get_restaurant_data(browser.page_source)
        return True, restaurants, browser.get_cookies(), None
    except Exception as e:
        logger.error(e, exc_info=True)
        return False, None, None, e.__str__()
    finally:
        browser.quit()
