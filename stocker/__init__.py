#!/usr/bin/python
from flask import Flask, session, g, redirect, url_for, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
db.create_all()

from . import views, model, controller
