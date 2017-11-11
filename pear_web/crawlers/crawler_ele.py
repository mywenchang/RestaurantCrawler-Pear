# coding=utf-8

import requests


def crawl_ele_restaurants(page_size=24, page_offset=0, latitude='30.64995', longitude='104.18755'):
    '''
    爬取饿了么商铺ids
    :param page_size: 每一页数据量
    :param page_offset: 偏移量
    :param latitude: 区域维度 默认为成大范围
    :param longitude: 区域经度 默认为成大范围
    :return:
    '''
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
        'cookie': "perf_ssid=l5pxqby9al72st9gqdp0kc4p89afap06_2017-10-13; ubt_ssid=1ysevte3hs2nhl4h1z4bmx4euy9yvv2j_2017-10-13; _utrace=18c18dc9c3b53f1d6a6ba83f168a8510_2017-10-13; eleme__ele_me=02038b5ff8b2aece84f0511134efbd56%3Ae942e185c846cc98c786675bfb0aa287650ad65f; SID=ZfELIJEqG1a53Da7J1Tv93vJBeFrH03w28PA; track_id=1507910287%7C7c2243dac1d2fece4f5aef441e581946afad1b9afdfc71e8b4%7C52226a795ee9108249a2a5c536fc8ba9; USERID=274692274",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != requests.codes.ok:
        return
    list = response.json()
    # TODO 存入数据库

    # 递归查询直到没有数据
    page_size = len(list)
    if page_size < 1:
        return
    page_offset += page_size
    crawl_ele_restaurants(page_size, page_offset)
