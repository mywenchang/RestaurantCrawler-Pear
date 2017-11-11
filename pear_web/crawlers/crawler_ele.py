# coding=utf-8

import requests

from pear_web import db
from pear_web.models.dish import Dish
from pear_web.models.restaurant import Restaurant
from pear_web.utils.const import Source


def crawl_ele_restaurants(page_size=24, page_offset=0, latitude='30.64995', longitude='104.18755'):
    """
    爬取饿了么商铺ids
    :param page_size: 每一页数据量
    :param page_offset: 偏移量
    :param latitude: 区域维度 默认为成大范围
    :param longitude: 区域经度 默认为成大范围
    :return:
    """
    url = "https://www.ele.me/restapi/shopping/restaurants"

    querystring = {"geohash": "wm6n6gehcuu", "latitude": latitude, "limit": page_size,
                   "longitude": longitude, "offset": page_offset, "sign": "1509166638215", "terminal": "web"}

    headers = {
        'accept': "application/json, text/plain, */*",
        'x-devtools-emulate-network-conditions-client-id': "ce48550f-bbf1-4e22-b92e-075cdb7b73a9",
        'x-shard': "loc={},{}".format(longitude, latitude),
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        'referer': "https://www.ele.me/place/wm6n6gehcuu?latitude={}&longitude={}".format(latitude, longitude),
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        # 'cookie': "perf_ssid=l5pxqby9al72st9gqdp0kc4p89afap06_2017-10-13; ubt_ssid=1ysevte3hs2nhl4h1z4bmx4euy9yvv2j_2017-10-13; _utrace=18c18dc9c3b53f1d6a6ba83f168a8510_2017-10-13; eleme__ele_me=02038b5ff8b2aece84f0511134efbd56%3Ae942e185c846cc98c786675bfb0aa287650ad65f; SID=ZfELIJEqG1a53Da7J1Tv93vJBeFrH03w28PA; track_id=1507910287%7C7c2243dac1d2fece4f5aef441e581946afad1b9afdfc71e8b4%7C52226a795ee9108249a2a5c536fc8ba9; USERID=274692274",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != requests.codes.ok:
        return
    list = response.json()
    for item in list:
        restaurant = Restaurant(
            restaurant_id=item.get('id'),
            name=item.get('name'),
            source=Source.ELE,
            arrive_time=item.get('order_lead_time'),
            start_fee=item.get('float_minimum_order_amount'),
            send_fee=item.get('float_delivery_fee'),
            score=item.get('rating'),
            sales=item.get('recent_order_num'),
            latitude=item.get('latitude'),
            longitude=item.get('longitude')
        )
        db.session.add(restaurant)
    db.session.commit()
    # 递归查询直到没有数据
    page_size = len(list)
    if page_size < 1:
        return
    page_offset += page_size
    crawl_ele_restaurants(page_size, page_offset)


def crawl_ele_dishes(restaurant_id, latitude, longitude):
    url = "https://www.ele.me/restapi/shopping/v2/menu"

    querystring = {"restaurant_id": restaurant_id}

    headers = {
        'accept': "application/json, text/plain, */*",
        'x-shard': "shopid={};loc={},{}".format(restaurant_id, latitude, longitude),
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        'referer': "https://www.ele.me/shop/{}".format(restaurant_id),
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        # 'cookie': "perf_ssid=l5pxqby9al72st9gqdp0kc4p89afap06_2017-10-13; ubt_ssid=1ysevte3hs2nhl4h1z4bmx4euy9yvv2j_2017-10-13; _utrace=18c18dc9c3b53f1d6a6ba83f168a8510_2017-10-13; eleme__ele_me=02038b5ff8b2aece84f0511134efbd56%3Ae942e185c846cc98c786675bfb0aa287650ad65f; SID=ZfELIJEqG1a53Da7J1Tv93vJBeFrH03w28PA; USERID=274692274; track_id=1507910287%7C7c2243dac1d2fece4f5aef441e581946afad1b9afdfc71e8b4%7C52226a795ee9108249a2a5c536fc8ba9; perf_ssid=l5pxqby9al72st9gqdp0kc4p89afap06_2017-10-13; ubt_ssid=1ysevte3hs2nhl4h1z4bmx4euy9yvv2j_2017-10-13; _utrace=18c18dc9c3b53f1d6a6ba83f168a8510_2017-10-13; eleme__ele_me=02038b5ff8b2aece84f0511134efbd56%3Ae942e185c846cc98c786675bfb0aa287650ad65f; SID=ZfELIJEqG1a53Da7J1Tv93vJBeFrH03w28PA; track_id=1507910287%7C7c2243dac1d2fece4f5aef441e581946afad1b9afdfc71e8b4%7C52226a795ee9108249a2a5c536fc8ba9; firstEnterUrlInSession=https%3A//www.ele.me/shop/1525314; pageReferrInSession=https%3A//www.ele.me/place/wm6n6gehcuu%3Flatitude%3D30.64995%26longitude%3D104.18755; USERID=274692274",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != requests.codes.ok:
        return
    dishes = response.json()
    for item in dishes:
        foods = item.get('foods')
        for item in foods:
            dish = Dish(
                name=item.get('name'),
                restaurant_id=item.get('restaurant_id'),
                rating=item.get('rating'),
                month_sales=item.get('month_sales'),
                rating_count=item.get('rating_count')
            )
            db.session.add(dish)
        db.session.commit()
