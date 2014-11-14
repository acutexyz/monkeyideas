from app.database import db

from passlib.hash import md5_crypt

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