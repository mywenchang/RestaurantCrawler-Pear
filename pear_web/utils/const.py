# coding=utf-8
# 数据来源
class Source(object):
    ELE = 1
    MEI_TUAN = 2


class Crawler_Status(object):
    Crawling = 0,
    DONE = 1,
    Error = 2


# 支持的action
SUPPORT_ACTIONS = ['create_ele_restaurant_crawler', 'create_ele_dish_crawler']
