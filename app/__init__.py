from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
import os

app = Flask(__name__)
app.config.from_pyfile(os.getcwd() + '/config.py')

db = SQLAlchemy(app)

import views, models