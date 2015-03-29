import os

basedir = os.path.abspath(os.path.dirname(__file__))


#database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://stalker:Vdmscdn1!@localhost/stocker'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Other Flask Stuff
DEBUG = True
SECRET_KEY = 'development key'