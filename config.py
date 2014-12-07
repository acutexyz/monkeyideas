import os


SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/monkeys' \
                          if os.environ.get('DATABASE_URL') is None \
                          else os.environ['DATABASE_URL']
SECRET_KEY = 'secretkey1'
ITEMS_PER_PAGE = 15
