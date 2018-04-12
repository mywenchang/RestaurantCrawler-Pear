# coding=utf-8

import json
import unittest

from datetime import datetime

from pear.models.crawler import CrawlerDao
from pear.models.user import UserDao
from pear.web.app import get_application


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.app = get_application().test_client()
        self.user_id = UserDao.create('t', 't', 't@t.com', '1')
        self.c_id = [
            CrawlerDao.create(self.user_id, 1, '', '', ''),
            CrawlerDao.create(self.user_id, 2, '', '', '')
        ]
        for i in self.c_id:
            CrawlerDao.update_by_id(i, self.user_id, status=1, data_count=10, total=10, finished=datetime.now())
        self.app.set_cookie('localhost', 'u_id', str(self.user_id))
        with self.app.session_transaction() as session:
            session[str(self.user_id)] = 't'

    def test_get_all_task(self):
        re = self.app.get('/crawler_tasks?page=1&per_page=10&status=1')
        data = json.loads(re.data)
        self.assertEqual(200, re.status_code)
        self.assertEqual(1, data['page'])
        self.assertEqual(2, data['total'])

    def tearDown(self):
        UserDao.delete(self.user_id)
        CrawlerDao.delete([self.c_id], self.user_id)
