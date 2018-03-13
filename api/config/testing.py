import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data-dev.sqlite')

DEBUG = True
TESTING = True
IGNORE_AUTH = False
SECRET_KEY = 'top-secret!'
SQLALCHEMY_DATABASE_URI = 'mysql://doroto:doroto@' + os.environ.get('DATABASE_URL') + "/doroto"