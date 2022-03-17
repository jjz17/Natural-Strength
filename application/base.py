# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os


user = 'root'
password = 'jiajia2002'
database = 'pythonlogin'

# user = os.environ.get('USER')
# password = os.environ.get('PASSWORD')
# database = os.environ.get('DATABASE')
create_string = f"mysql+pymysql://{user}:{password}@localhost:3306/{database}"

engine = create_engine(create_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()