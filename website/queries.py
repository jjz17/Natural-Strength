# coding=utf-8

# 1 - imports
from user import User
from base import Session
from user_metrics import UserMetrics
from datetime import date

# 2 - extract a session
session = Session()

# 3 - extract all users
users = session.query(User).all()

# 4 - print movies' details
print('\n### All Users:')
for user in users:
    print(f'{user.username} was born on {user.birth_date}')
print('')

# 5 - get users born after the given date
users = session.query(User) \
    .filter(User.birth_date > date(2000, 1, 1)) \
    .all()

print('### Young Users:')
for user in users:
    print(f'{user.username} was born after 2000')
print('')

# # 6 - movies that Dwayne Johnson participated
# the_rock_movies = session.query(Movie) \
#     .join(Actor, Movie.actors) \
#     .filter(Actor.name == 'Dwayne Johnson') \
#     .all()

# print('### Dwayne Johnson movies:')
# for movie in the_rock_movies:
#     print(f'The Rock starred in {movie.title}')
# print('')

# # 7 - get actors that have house in Glendale
# glendale_stars = session.query(Actor) \
#     .join(ContactDetails) \
#     .filter(ContactDetails.address.ilike('%glendale%')) \
#     .all()

# print('### Actors that live in Glendale:')
# for actor in glendale_stars:
#     print(f'{actor.name} has a house in Glendale')
# print('')
