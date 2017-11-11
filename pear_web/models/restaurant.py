from pear_web import db


class Restaurant(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(20))
    source = db.Column(db.Integer(1))
    sales = db.Column(db.Integer)
    arrive_time = db.Column(db.Integer)
    start_fee = db.Column(db.Integer)
    send_fee = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, name=None, source=None, arriv_time=None, start_fee=None, send_fee=None, score=None):
        self.name = name
        self.source = source
        self.arrive_time = arriv_time
        self.start_fee = start_fee
        self.send_fee = send_fee
        self.score = score
