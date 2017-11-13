import json

from pear_web import db
from datetime import datetime
from pear_web.utils.const import Crawler_Status


class Crawler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    args = db.Column(db.String)
    info = db.Column(db.String)
    extras = db.Column(db.String)
    data_count = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, created=None, args=None):
        self.created = created
        self.args = args
        self.status = Crawler_Status.Crawling

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'created': self.created.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created, datetime) else '',
            'finished': self.finished.isoformat() if isinstance(self.finished, datetime) else '',
            'args': json.loads(self.args) if self.args else '',
            'info': self.info,
            'extras': json.loads(self.extras) if self.extras else '',
            'data_count': self.data_count,
            'total': self.total
        }
