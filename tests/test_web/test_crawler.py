# coding=utf-8

import json
import unittest

from pear.web.app import get_application
from pear.models.user import UserDao


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = get_application().test_client()
        self.user_id = UserDao.create('n', 'p', 'e', '1111')
        self.app.set_cookie('localhost', 'u_id', str(self.user_id))
        with self.app.session_transaction() as session:
            session[str(self.user_id)] = 1

    def test_get_ele_pic_code(self):
        mobile = '18502823774'
        rv = self.app.get('/config_ele_crawler/pic_code?mobile={}'.format(mobile))
        self.assertEquals(200, rv.status_code)

    def test_create_crawler(self):
        request_data = [{
            'latitude': 1,
            'longitude': 2,
            'ele_restaurant': {
                'id': 1,
                'latitude': 2,
                'longitude': 3
            }
        }]
        rv = self.app.post('/crawler_tasks', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(200, rv.status_code)

    def tearDown(self):
        UserDao.delete(self.user_id)
