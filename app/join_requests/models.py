from app.database import db

from datetime import datetime
from app.utils import enum

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