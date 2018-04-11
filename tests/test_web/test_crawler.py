# coding=utf-8

import json
import unittest

from pear.web.app import get_application


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = get_application().test_client()
        resp = self.app.post('/auth/login', data=json.dumps(dict(account='jiyang', password='jiyang')),
                             content_type='application/json')
        u_id = resp.headers.get('Set-cookie').split(';')[0][5:]
        self.app.set_cookie('localhost', 'u_id', u_id)

    def test_get_ele_pic_code(self):
        mobile = '18502823774'
        rv = self.app.get('/config_ele_crawler/pic_code?mobile={}'.format(mobile))
        self.assertEquals(200, rv.status_code)

    def test_create_crawler(self):
        request_data = [{
            'latitude': 1,
            'longitude': 2,
            'restaurant': {
                'id': 1,
                'latitude': 2,
                'longitude': 3
            }
        }]
        rv = self.app.post('/crawler_tasks', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(200, rv.status_code)
