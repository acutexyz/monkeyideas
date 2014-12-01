from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app.factory import create_app
import os
from app.models import db

app = create_app(os.getcwd() + '/config.py')

ctx = app.app_context()
ctx.push()

db.app = app

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    ctx.pop()
