from app.database import db

fields = db.Table('fields',
                  db.Column('idea_id', db.ForeignKey('idea.id')),
                  db.Column('field_id', db.ForeignKey('field.id')),
                 )

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    
members = db.Table('members', 
                   db.Column('idea_id', db.ForeignKey('idea.id')),
                   db.Column('monkey_id', db.ForeignKey('monkey.id')),
                  )

class IdeaStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    ideas = db.relationship('Idea', backref='status', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('monkey.id'))
    fields = db.relationship('Field', secondary=fields, backref=db.backref('ideas', lazy='dynamic'))
    monkeys = db.relationship('Monkey', secondary=members, backref=db.backref('memberin', lazy='dynamic'))
    is_public = db.Column(db.Boolean, default=True)
    status_id = db.Column(db.Integer, db.ForeignKey('idea_status.id'))
    requests = db.relationship('JoinRequest', backref='idea', lazy='dynamic')
    suggestions = db.relationship('Suggestion', backref='idea', lazy='joined')
    # todo: add date_published fuck
    
    def __init__(self, title, body, author_id, is_public):
        self.title = title
        self.body = body
        self.author_id = author_id
        self.is_public = is_public
        
    def __repr__(self):
        return self.title