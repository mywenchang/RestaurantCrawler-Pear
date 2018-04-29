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
