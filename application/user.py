
from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, Date

from application.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    birth_date = Column(Date)
    email = Column(String)
    sex = Column(Integer)

    def __init__(self, username, password, birth_date, email, sex):
        self.username = username
        self.password = password
        self.birth_date = birth_date
        self.email = email
        self.sex = sex