# coding=utf-8

import unittest

from pear.web.app import init_app


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = init_app().test_client()

    def test_login(self):
        rv = self.app.post('/crawlers/get_ele_code', data=dict(
            mobile='18502823774'
        ))
        self.assertEquals(200, rv.status_code)

    def test_create_crawler(self):
        rv = self.app.post('/crawlers', data=dict(
            source='ele',
            type='restaurant'
        ))
        self.assertEqual(200, rv.status_code)
