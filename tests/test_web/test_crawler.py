# coding=utf-8

import json
import unittest

from pear.web.app import init_app


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = init_app().test_client()
        resp = self.app.post('/auth/login', data=json.dumps(dict(account='guest', password='guest')),
                             content_type='application/json')
        u_id = resp.headers.get('Set-cookie').split(';')[0][5:]
        self.app.set_cookie('localhost', 'u_id', u_id)

    def test_get_ele_pic_code(self):
        mobile = '18502823774'
        rv = self.app.get('/crawlers/ele_pic_code?mobile={}'.format(mobile))
        print(rv.data)
        self.assertEquals(200, rv.status_code)

    def test_create_crawler(self):
        rv = self.app.post('/crawlers', data=json.dumps(dict(
            source='ele',
            type='restaurant'
        )), content_type='application/json')
        print(rv.data)
        self.assertEqual(202, rv.status_code)
