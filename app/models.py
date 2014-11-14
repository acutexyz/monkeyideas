from datetime import datetime
from passlib.hash import md5_crypt
from app.utils import enum, DuplicateSuggestionException
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    monkeys = db.relationship('Monkey', backref='profession', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    
class Monkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(64))
    fullname = db.Column(db.String(100))
    about = db.Column(db.String(200))
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'))
    is_public = db.Column(db.Boolean, default=True)
    birthyear = db.Column(db.Integer) #
    sex = db.Column(db.Boolean) #
    facebook = db.Column(db.String(100)) #
    twitter = db.Column(db.String(100)) #
    ideas = db.relationship('Idea', backref='author', lazy='dynamic') #todo make joined
    requests = db.relationship('JoinRequest', backref='monkey', lazy='dynamic') # by me -->
    suggestions = db.relationship('Suggestion', backref='monkey', lazy='dynamic') # to me <--
        
    def __init__(self, email, fullname, about, profession_id):
        self.email = email
        self.fullname = fullname
        self.about = about
        self.profession_id = profession_id
        
    def set_password(self, password):
        self.password = md5_crypt.encrypt(password) # if md5_crypt.verify(raw, hash):
        
    def verify_password(self, password):
        return md5_crypt.verify(password, self.password)
    
    def __repr__(self):
        return self.fullname
    
    # Following four methods are for Flask-Login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
    def suggestions_made(self, monkey):
        """Returns the number of suggestions already made 
        by this (self) monkey to given monkey.
        """
        count = 0
        for idea in self.ideas:
            for suggestion in idea.suggestions:
                if suggestion.monkey_id == monkey.id:
                    count += 1
        return count
    
    def get_ideas_to_suggest(self, monkey):
        """Returns ideas that had not been suggested
        to given monkey yet.
        """
        ideas = []
        for idea in self.ideas:
            suggested = False
            for suggestion in monkey.suggestions:
                if idea.id == suggestion.idea_id:
                    suggested = True
            if not suggested:
                ideas.append(idea)
        return ideas
    
    def is_member_of(self, idea):
        return self in idea.monkeys
    
    def requested_to_join(self, idea):
        """Returns True if this monkey already 
        requested to join this idea
        """
        for r in self.requests:
            if r.idea_id == idea.id:
                return True
        return False
    
    def is_author_of(self, idea):
        return idea.author_id == self.id

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
    
    
JoinRequestStatus = enum(
    SENT=0,
    ACCEPTED=1,
    DECLINED=2
)
    
class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monkey_id = db.Column(db.Integer, db.ForeignKey('monkey.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))
    status = db.Column(db.Integer, default=JoinRequestStatus.SENT) # default?
    date_sent = db.Column(db.DateTime)
    message = db.Column(db.String(200))
    
    def __init__(self, monkey, idea, message=""):
        self.monkey_id = monkey.id
        self.idea_id = idea.id
        self.date_sent = datetime.utcnow()
        self.message = message
        self.status = JoinRequestStatus.SENT
        self.validate(monkey, idea)
        
    def __repr__(self):
        return self.monkey.fullname + ' -> "' + self.idea.title + '"'
    
    def validate(self, monkey, idea):
        """If not valid raises an error.
        Should be called before saving the object.
        """
        if monkey.is_author_of(idea):
            raise Exception("Author can't join own idea")
        
        if monkey.is_member_of(idea):
            raise Exception("Monkey is already engaged in this idea")
        
        if monkey.requested_to_join(idea):
            raise Exception("Monkey had already requested to join this idea")
        
    
class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monkey_id = db.Column(db.Integer, db.ForeignKey('monkey.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))
    date_sent = db.Column(db.DateTime)
    
    def __init__(self, monkey_id, idea_id):
        self.monkey_id = monkey_id
        self.idea_id = idea_id
        self.date_sent = datetime.utcnow()
        self.validate()
        
    def validate(self):
        """If not valid raises an error.
        Should be called before saving the object.
        """
        monkey = Monkey.query.get(self.monkey_id)
        if monkey is None:
            raise Exception("This is no monkey id")
        for suggestion in monkey.suggestions:
            if suggestion.idea_id == self.idea_id:
                raise DuplicateSuggestionException()
        
    def __repr__(self):   
        return '"' + self.idea.title + '" -> ' + self.monkey.fullname