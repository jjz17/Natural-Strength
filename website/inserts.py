# coding=utf-8

# 1 - imports
from datetime import datetime
from datetime import date

from user import User
from base import Session, engine, Base
from user_metrics import UserMetrics

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create users
jz = User('JZ', 'a', date(2002, 7, 19), 'j@j.j')

# 5 - add user metrics to users
jz_met1 = UserMetrics(jz, 5, 5, 5, 5, datetime.now())

# 6 - persist data
session.add(jz)

session.add(jz_met1)

# 7 - commit and close session
session.commit()
session.close()
