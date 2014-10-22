from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/monkeys'
app.config['SECRET_KEY'] = 'secretkey1'

db = SQLAlchemy(app)

import views, models