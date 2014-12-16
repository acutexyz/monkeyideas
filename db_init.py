from app.factory import create_app
from app.models import db, Field, Profession, IdeaStatus, Monkey
import os

app = create_app(os.getcwd() + '/config.py')

ctx = app.app_context()
ctx.push()

db.app = app
db.drop_all()
db.create_all()

fields = [
    'Education', 
    'Healthcare', 
    'Communications', 
    'E-commerce/Commerce',
    'Business Automation', 
    'Finance/Marketing', 
    'Social Networks'
]

for name in fields:
    field = Field(name)
    db.session.add(field)
    
professions = [
    'Software Engineer', 
    'Designer', 
    'Business/Marketing', 
    'Investor', 
    'DevOps Engineer', 
    'Lawyer'
]

for name in professions:
    profession = Profession(name)
    db.session.add(profession)

idea_statuses = [
    'Just in mind. No further step is done yet.',
    'Made a research and proved the idea is good.',
    'I already implemented it, I need a team.',
    'Product is ready. So is my team. Need investors.'
]

for name in idea_statuses:
    status = IdeaStatus(name)
    db.session.add(status)
    
db.session.commit()

monkey = Monkey(
    email="aidanxyz@gmail.com", 
    fullname="Aidan Zhakypov", 
    about="Web enthusiast from Central Asia.", 
    profession_id=1
)
monkey.set_password("123qwe")

db.session.add(monkey)

db.session.commit()

ctx.pop()
