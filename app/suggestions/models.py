from app.database import db

from datetime import datetime
from app.utils import DuplicateSuggestionException

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