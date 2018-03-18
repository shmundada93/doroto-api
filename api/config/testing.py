import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data-dev.sqlite')

DEBUG = True
TESTING = True
IGNORE_AUTH = False
SECRET_KEY = 'top-secret!'
SQLALCHEMY_DATABASE_URI = 'mysql://doroto:doroto@' + os.environ['DATABASE_URL'] + "/doroto"
UPLOAD_FOLDER = '/home/doroto/uploads/'
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])
CELERY_BROKER_URL= 'redis://{}:6379'.format(os.environ['REDIS_HOST'])
CELERY_BACKEND_URL= 'redis://{}:6379'.format(os.environ['REDIS_HOST'])
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_ACCESS_KEY_SECRET = os.environ['AWS_ACCESS_KEY_SECRET']
AWS_REGION = os.environ['AWS_REGION']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
GOOGLE_CLOUD_KEY = os.environ['GOOGLE_CLOUD_KEY']
FLASK_CONFIG = os.environ.get('FLASK_CONFIG', 'testing')