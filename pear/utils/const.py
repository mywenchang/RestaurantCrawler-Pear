# coding=utf-8
# 数据来源

class SOURCE(object):
    ELE = 1
    MEI_TUAN = 2


SOURCES = {
    1: u'饿了么',
    2: u'美团外卖'
}


class Crawler_Status(object):
    Crawling = 0,
    DONE = 1,
    Error = 2


class AnalyTaskType(object):
    SINGLE = 1,
    MULTI = 2


HOT_CITIES = [
    u"北京",
    u"上海",
    u"深圳",
    u"广州",
    u"成都",
    u"杭州",
    u"武汉",
    u"重庆",
    u"南京",
    u"天津",
    u"苏州",
    u"西安",
    u"长沙",
    u"沈阳",
    u"青岛",
    u"郑州",
    u"大连",
    u"东莞",
    u"宁波",
    u"厦门",
    u"福州",
    u"无锡",
    u"合肥",
    u"昆明",
    u"哈尔滨",
    u"济南",
    u"佛山",
    u"长春",
    u"温州",
    u"石家庄",
    u"南宁",
    u"常州",
    u"泉州",
    u"南昌",
    u"贵阳",
    u"太原",
    u"烟台",
    u"嘉兴",
    u"南通",
    u"金华",
    u"珠海",
    u"惠州",
    u"徐州",
    u"海口",
    u"乌鲁木齐",
    u"绍兴",
    u"中山",
    u"台州",
    u"兰州"
]
