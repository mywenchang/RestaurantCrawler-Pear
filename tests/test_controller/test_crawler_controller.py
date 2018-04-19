# coding=utf-8

import unittest
from pear.web.controllers import ele_crawler_controller


class TestCrawlerController(unittest.TestCase):

    def setUp(self):
        super(TestCrawlerController, self).setUp()

    def tearDown(self):
        super(TestCrawlerController, self).tearDown()

    def test_get_ele_restaurants(self):
        ele_crawler_controller.get_ele_restaurants('wm6n6gujs78t', '30.651446', '104.189026', None)
