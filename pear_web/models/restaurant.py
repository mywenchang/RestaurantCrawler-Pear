from pear_web import db


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    name = db.Column(db.VARCHAR)
    source = db.Column(db.Integer)
    sales = db.Column(db.Integer)
    arrive_time = db.Column(db.Integer)
    start_fee = db.Column(db.Float)
    send_fee = db.Column(db.Float)
    score = db.Column(db.Float)
    latitude = db.Column(db.VARCHAR)
    longitude = db.Column(db.VARCHAR)

    def __init__(self, restaurant_id=None, name=None, source=None, arrive_time=None, start_fee=None, send_fee=None,
                 score=None, sales=None, latitude=None, longitude=None):
        self.restaurant_id = restaurant_id
        self.name = name
        self.source = source
        self.arrive_time = arrive_time
        self.start_fee = start_fee
        self.send_fee = send_fee
        self.score = score
        self.sales = sales
        self.latitude = latitude
        self.longitude = longitude
