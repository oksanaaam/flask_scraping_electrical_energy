from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarketData(Base):
    __tablename__ = 'market_data'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    price = Column(Float)
    volume = Column(Float)
