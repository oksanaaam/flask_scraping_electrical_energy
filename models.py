from config import db


class MarketData(db.Model):
    __tablename__ = "market_data"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    hour = db.Column(db.String)
    price = db.Column(db.Float)
    volume = db.Column(db.Float)

    def __init__(self, date, hour, price, volume):
        self.date = date
        self.hour = hour
        self.price = price
        self.volume = volume
