from app.factory import create_app
from app.models import db, Field, Profession
import os

app = create_app(os.getcwd() + '/config.py')

ctx = app.app_context()
ctx.push()

db.app = app
db.create_all()

fields = ['E-commerce/Commerce', 'Education', 'Medicine', 'Social networks', 'Automation Solutions', 'Finance']

for name in fields:
    field = Field(name)
    db.session.add(field)
    
professions = ['Software Engineer', 'Designer', 'Business/Marketing', 'Investor', 'DevOps Engineer', 'Lawyer']

for name in professions:
    profession = Profession(name)
    db.session.add(profession)
    
db.session.commit()

ctx.pop()