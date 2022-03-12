
from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, Date, Float
from base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    birth_date = Column(Date)
    weight = Column(Float)
    squat = Column(Float)
    bench = Column(Float)
    deadlift = Column(Float)
    email = Column(String)

    def __init__(self, username, password, birth_date, email, weight=0, squat=0, bench=0, deadlift=0):
        self.username = username
        self.password = password
        self.birth_date = birth_date
        self.email = email
        self.weight = weight
        self.squat = squat
        self.bench = bench
        self.deadlift = deadlift