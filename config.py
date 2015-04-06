import os

basedir = os.path.abspath(os.path.dirname(__file__))

#database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://stalker:Vdmscdn1!@localhost/stocker'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#celery configuration
CELERY_BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'ampq'
CELERY_TIMEZONE = 'UTC'

#Other Flask Stuff
DEBUG = True
SECRET_KEY = 'development key'

#Login Information
USERNAME = 'stalker'
PASSWORD = 'Vdmscdn1!'
