# coding=utf-8

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class UserMetrics(Base):
    __tablename__ = 'user_metrics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="user_metrics")
    weight = Column(Float)
    squat = Column(Float)
    bench = Column(Float)
    deadlift = Column(Float)
    date = Column(Date)

    def __init__(self, user, weight, squat, bench, deadlift, date):
        self.user = user
        self.weight = weight
        self.squat = squat
        self.bench = bench
        self.deadlift = deadlift
        self.date = date


class DummyUserMetrics():

    def __init__(self, weight, squat, bench, deadlift, date):
        self.weight = weight
        self.squat = squat
        self.bench = bench
        self.deadlift = deadlift
        self.date = date