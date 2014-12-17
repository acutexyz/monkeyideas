from datetime import datetime
from passlib.hash import pbkdf2_sha512
from app.utils import enum, DuplicateSuggestionError
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Profession(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    name = db.Column(
        db.String(80), 
        unique=True
    )
    
    monkeys = db.relationship(
        'Monkey', 
        backref='profession', 
        lazy='dynamic'
    )
    
    def __repr__(self):
        return self.name
    

class Monkey(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    email = db.Column(
        db.String(100), 
        unique=True
    )
    
    password = db.Column(
        db.String(1200)
    )
    
    fullname = db.Column(
        db.String(100)
    )
    
    about = db.Column(
        db.String(200)
    )
    
    profession_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'profession.id', 
            ondelete='SET NULL'
        )
    )
    
    is_public = db.Column(
        db.Boolean, 
        default=True
    )
    
    birthyear = db.Column(
        db.Integer
    ) #
    
    sex = db.Column(
        db.Boolean
    ) #
    
    facebook = db.Column(
        db.String(100)
    ) #
    
    twitter = db.Column(
        db.String(100)
    ) #
    
    ideas = db.relationship(
        'Idea', 
        backref='author', 
        lazy='dynamic'
    ) #todo make joined
    
    requests = db.relationship(
        'JoinRequest', 
        backref='monkey', 
        lazy='dynamic'
    ) # by me -->
    
    suggestions = db.relationship(
        'Suggestion', 
        backref='monkey', 
        lazy='dynamic'
    ) # to me <--
        
    def set_password(self, password):
        self.password = pbkdf2_sha512.encrypt(password)
        
    def verify_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)
    
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
    
    def suggestions_made_to(self, monkey):
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
        """Returns ideas query that had not been suggested
        to given monkey yet.
        """
        suggested = Idea.query.join(Suggestion) \
                              .filter(Idea.author_id==self.id, 
                                      Suggestion.monkey_id==monkey.id) \
                              .all()
        return Idea.query.filter(Idea.author_id==self.id, 
                                 Idea.id.notin_([i.id for i in suggested]))
           
    def is_member_of(self, idea):
        return self in idea.monkeys
    
    def requested_to_join(self, idea):
        """Returns True if this monkey already requested to 
        join this idea and 
        request is still pending (i.e. status=SENT)
        """
        for r in self.requests:
            if r.idea_id == idea.id and \
                r.status == JoinRequestStatus.SENT:
                return True
        return False
    
    def is_author_of(self, idea):
        return idea.author_id == self.id


fields = db.Table(
    'fields', 
    db.Column(
        'idea_id', 
        db.ForeignKey(
            'idea.id', 
            ondelete='CASCADE'
        )
    ),
    db.Column(
        'field_id', 
        db.ForeignKey(
            'field.id', 
            ondelete='CASCADE'
        )
    )
)


class Field(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    name = db.Column(
        db.String(80), 
        unique=True
    )
    
    def __repr__(self):
        return self.name
    

members = db.Table(
    'members', 
    db.Column(
        'idea_id', 
        db.ForeignKey(
            'idea.id', 
            ondelete='CASCADE'
        )
    ),
    db.Column(
        'monkey_id', 
        db.ForeignKey(
            'monkey.id', 
            ondelete='CASCADE'
        )
    )
)


class IdeaStatus(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    name = db.Column(
        db.String(150), 
        unique=True
    )
    
    ideas = db.relationship(
        'Idea', 
        backref='status', 
        lazy='dynamic'
    )
    
    def __repr__(self):
        return self.name
    

class Idea(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    title = db.Column(
        db.String(80)
    )
    
    body = db.Column(
        db.Text
    )
    
    author_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'monkey.id', 
            ondelete='SET NULL'
        )
    )
    
    fields = db.relationship(
        'Field', 
        secondary=fields, 
        backref=db.backref(
            'ideas', 
            lazy='dynamic'
        )
    )
    
    monkeys = db.relationship(
        'Monkey', 
        secondary=members,
        backref=db.backref(
            'memberin', 
            lazy='dynamic'
        )
    )
    
    is_public = db.Column(
        db.Boolean, 
        default=True
    )
    
    status_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'idea_status.id', 
            ondelete='SET NULL'
        )
    )
    
    requests = db.relationship(
        'JoinRequest', 
        backref='idea', 
        lazy='dynamic'
    )
    
    suggestions = db.relationship(
        'Suggestion', 
        backref='idea', 
        lazy='joined'
    )
    
    # todo: add date_published
    
    def __repr__(self):
        return self.title
    
    def add_member(self, monkey):
        if monkey.id == self.author_id:
            raise Exception(
                'Author can not become member of an idea'
            )
        if monkey in self.monkeys:
            raise Exception(
                'Monkey is already a member'
            )
            
        self.monkeys.append(monkey)
        
        # todo: remove suggestions of this idea made to monkey 
    
    
JoinRequestStatus = enum(
    SENT=0,
    ACCEPTED=1,
    DECLINED=2
)
    

class JoinRequest(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    monkey_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'monkey.id', 
            ondelete='CASCADE'
        )
    )
    
    idea_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'idea.id', 
            ondelete='CASCADE'
        )
    )
    
    status = db.Column(
        db.Integer, 
        default=JoinRequestStatus.SENT
    ) # default?
    
    date_sent = db.Column(
        db.DateTime
    )
    
    message = db.Column(
        db.String(200)
    )
    
    def __init__(self, monkey, idea, message=''):
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
            raise Exception(
                'Author can not join own idea'
            )
        
        if monkey.is_member_of(idea):
            raise Exception(
                'Monkey is already member of this idea'
            )
        
        if monkey.requested_to_join(idea):
            raise Exception(
                'Monkey had already requested to join this idea'
            )
        
    
class Suggestion(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    monkey_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'monkey.id', 
            ondelete='CASCADE'
        )
    )
    
    idea_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'idea.id', 
            ondelete='CASCADE'
        )
    )
    
    date_sent = db.Column(
        db.DateTime
    )
    
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
            raise Exception('Monkey not found')
        idea = Idea.query.get(self.idea_id)
        if idea is None:
            raise Exception('Idea not found')
            
        if idea.author_id == self.monkey_id:
            raise Exception(
                'Can not suggest an idea to its author'
            )
            
        for suggestion in monkey.suggestions:
            if suggestion.idea_id == self.idea_id:
                raise DuplicateSuggestionError()
        
    def __repr__(self):   
        return '"' + self.idea.title + '" -> ' + self.monkey.fullname
