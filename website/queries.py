# coding=utf-8

# 1 - imports
from user import User
from base import Session
from user_metrics import UserMetrics

# 2 - extract a session
session = Session()

# 3 - extract all users
users = session.query(User).all()

# 4 - print movies' details
print('\n### All Users:')
for user in users:
    print(f'{user.username} was born on {user.birth_date}')
print('')