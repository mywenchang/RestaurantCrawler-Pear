# coding=utf-8

import json
import unittest

from mock import patch

from pear.web.app import get_application


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = get_application().test_client()
        resp = self.app.post('/auth/login', data=json.dumps(dict(account='jiyang', password='jiyang')),
                             content_type='application/json')
        u_id = resp.headers.get('Set-cookie').split(';')[0][5:]
        self.app.set_cookie('localhost', 'u_id', u_id)

    @patch('pear.web.handlers.handler_crawler_tasks.CrawlerDao')
    def test_get_all_task(self, mock_dao):
        mock_dao.batch_get_by_status.return_value = ([], 0)
        re = self.app.get('/crawler_tasks?page=9999&per_page=2&status=0')
        data = json.loads(re.data)
        self.assertEqual(200, re.status_code)
        self.assertEqual(9999, data['page'])
