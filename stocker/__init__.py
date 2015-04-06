#!/var/www/stocker/venv/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
db.create_all()

from . import views, model, controller
